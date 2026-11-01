"""
Unit Tests for Credit Default Prediction Model and Monitoring Engine
---------------------------------------------------------------------
Validates:
1. Model artifacts existence and loadability.
2. Discrimination performance metrics (AUC, KS, Gini).
3. Risk tier monotonic calibration.
4. Correct behavior of the Population Stability Index (PSI) function.
5. Completeness of scored master portfolio table.
"""

import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import pytest

from src.model import calculate_psi, calculate_ks_statistic


@pytest.fixture(scope="module")
def model_metrics():
    metrics_path = Path("data/processed/models/model_evaluation_metrics.json")
    if not metrics_path.exists():
        from src.build import run_full_build
        run_full_build()
    with open(metrics_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def scored_accounts():
    scores_path = Path("data/processed/account_risk_scores.parquet")
    if not scores_path.exists():
        pytest.fail(f"Scored accounts file not found at {scores_path}")
    return pd.read_parquet(scores_path)


def test_models_exist_on_disk():
    """Ensures serialized model joblib files exist and load successfully."""
    lr_file = Path("data/processed/models/logistic_regression.joblib")
    lgb_file = Path("data/processed/models/lightgbm_champion.joblib")
    assert lr_file.exists(), f"Logistic regression model file missing: {lr_file}"
    assert lgb_file.exists(), f"LightGBM champion model file missing: {lgb_file}"

    lr_model = joblib.load(lr_file)
    lgb_model = joblib.load(lgb_file)
    assert lr_model is not None
    assert lgb_model is not None


def test_discrimination_metrics_benchmark(model_metrics):
    """Ensures models exceed Basel credit risk scorecard discrimination minimums."""
    lr_m = model_metrics["metrics"]["logistic_regression"]
    lgb_m = model_metrics["metrics"]["lightgbm"]

    # Regulatory minimum benchmarks: AUC > 0.60, KS > 20%, Gini > 0.20
    assert lr_m["auc"] >= 0.65, f"Logistic regression AUC below benchmark: {lr_m['auc']}"
    assert lr_m["ks_stat_pct"] >= 20.0, f"Logistic regression KS below benchmark: {lr_m['ks_stat_pct']}"
    assert lr_m["gini"] >= 0.30, f"Logistic regression Gini below benchmark: {lr_m['gini']}"

    assert lgb_m["auc"] >= 0.65, f"LightGBM AUC below benchmark: {lgb_m['auc']}"
    assert lgb_m["ks_stat_pct"] >= 20.0, f"LightGBM KS below benchmark: {lgb_m['ks_stat_pct']}"
    assert lgb_m["gini"] >= 0.30, f"LightGBM Gini below benchmark: {lgb_m['gini']}"


def test_risk_tier_monotonic_separation(scored_accounts):
    """Ensures realized default rate strictly increases from Low Risk to Critical Risk."""
    assert len(scored_accounts) == 14685, f"Expected 14,685 scored accounts, got {len(scored_accounts)}"
    assert scored_accounts["predicted_pd"].isna().sum() == 0, "Predicted probabilities contain nulls"

    tier_dr = scored_accounts.groupby("risk_tier")["target_default"].mean()
    assert tier_dr["Low Risk"] < tier_dr["Medium Risk"], "Low risk tier default rate not below Medium"
    assert tier_dr["Medium Risk"] < tier_dr["High Risk"], "Medium risk tier default rate not below High"
    assert tier_dr["High Risk"] < tier_dr["Critical Risk"], "High risk tier default rate not below Critical"


def test_psi_stability_calculator():
    """Validates that calculate_psi correctly assigns Green status to identical distributions."""
    np.random.seed(42)
    baseline = np.random.beta(2, 8, size=1000)
    production_identical = baseline.copy()
    res_identical = calculate_psi(baseline, production_identical)
    assert res_identical["psi_value"] < 0.01
    assert "Green" in res_identical["status"]

    # Shifted distribution should trigger Amber or Red
    production_shifted = np.random.beta(5, 5, size=1000)
    res_shifted = calculate_psi(baseline, production_shifted)
    assert res_shifted["psi_value"] > 0.10
    assert "Amber" in res_shifted["status"] or "Red" in res_shifted["status"]
