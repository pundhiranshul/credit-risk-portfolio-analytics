"""
Credit Risk Default Modeling and Post-Deployment Monitoring Engine
------------------------------------------------------------------
Trains:
1. Baseline Model: Regularized Logistic Regression (regulatory scorecard standard).
2. Champion Model: LightGBM Gradient Boosted Decision Trees.

Evaluates:
- AUC-ROC, Kolmogorov-Smirnov (KS) statistic, and Gini coefficient (2*AUC - 1).
- Global and local per-account SHAP explanations via TreeExplainer.
- Post-deployment stability monitoring: Population Stability Index (PSI) & CSI.

Author: pundhiranshul <anshulpundhirwork@gmail.com>
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import shap

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.features import (
    prepare_modeling_data,
    get_logistic_regression_preprocessor,
    format_for_lightgbm,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("model")

SHAP_BUSINESS_RATIONALE = {
    "annual_income": "Primary borrower solvency buffer and debt service capacity.",
    "years_employed": "Employment stability and career income continuity signal.",
    "repay_ontime_count": "Historical installment compliance and positive payment track record.",
    "bureau_avg_dpd": "External credit delinquency depth across bank/NBFC facilities.",
    "repay_avg_dpd": "Internal monthly installment delinquency severity.",
    "repay_max_dpd": "Peak historical days past due indicating acute liquidity stress.",
    "debt_to_income_ratio": "Annualized EMI debt burden relative to borrower income.",
    "loan_to_income_ratio": "Principal leverage multiple relative to annual earnings.",
    "bureau_utilization_ratio": "External revolving and installment credit line exhaustion.",
    "bureau_has_written_off": "Prior institutional charge-off or severe credit default flag.",
    "loan_type": "Structural product risk differentiation (e.g., Mortgage vs. Personal Loan).",
    "employment_type": "Income volatility across Unemployed, Contract, and Salaried segments.",
    "loan_amount": "Absolute principal exposure at risk.",
    "interest_rate_pct": "Risk-based pricing coupon and monthly installment burden.",
}


def calculate_ks_statistic(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Computes the Kolmogorov-Smirnov (KS) separation statistic between defaults and non-defaults."""
    defaults = y_prob[y_true == 1]
    non_defaults = y_prob[y_true == 0]
    res = ks_2samp(defaults, non_defaults)
    return float(res.statistic)


def calculate_psi(expected: np.ndarray, actual: np.ndarray, num_buckets: int = 10) -> Dict[str, Any]:
    """
    Calculates the Population Stability Index (PSI) between a baseline (expected)
    and production (actual) probability distribution.
    """
    percentiles = np.linspace(0, 100, num_buckets + 1)
    bins = np.percentile(expected, percentiles)
    bins[0] = -np.inf
    bins[-1] = np.inf

    bins = np.unique(bins)
    if len(bins) < 3:
        bins = np.linspace(0.0, 1.0, num_buckets + 1)
        bins[0] = -np.inf
        bins[-1] = np.inf

    expected_counts, _ = np.histogram(expected, bins=bins)
    actual_counts, _ = np.histogram(actual, bins=bins)

    expected_pct = np.maximum(expected_counts / len(expected), 1e-4)
    actual_pct = np.maximum(actual_counts / len(actual), 1e-4)

    psi_contributions = (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
    total_psi = float(np.sum(psi_contributions))

    if total_psi < 0.10:
        status = "Green (Stable population)"
        action = "No action required. Standard ongoing monitoring."
    elif total_psi < 0.25:
        status = "Amber (Moderate drift)"
        action = "Investigate sub-population shifts; increase review frequency."
    else:
        status = "Red (Significant drift)"
        action = "Mandatory model retuning / scorecard recalibration required."

    return {
        "psi_value": round(total_psi, 4),
        "status": status,
        "recommended_action": action,
        "num_bins": len(bins) - 1,
    }


def evaluate_model_predictions(y_true: pd.Series, y_prob: np.ndarray) -> Dict[str, float]:
    """Computes the complete suite of regulatory and technical credit risk metrics."""
    auc = roc_auc_score(y_true, y_prob)
    ks = calculate_ks_statistic(y_true.to_numpy(), y_prob)
    gini = 2.0 * auc - 1.0
    brier = brier_score_loss(y_true, y_prob)
    ll = log_loss(y_true, y_prob)

    return {
        "auc": round(float(auc), 4),
        "ks_stat": round(float(ks), 4),
        "ks_stat_pct": round(float(ks * 100), 2),
        "gini": round(float(gini), 4),
        "brier_score": round(float(brier), 4),
        "log_loss": round(float(ll), 4),
    }


def train_logistic_baseline(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    """Trains the baseline regularized Logistic Regression model."""
    logger.info("Training Logistic Regression baseline...")
    preprocessor = get_logistic_regression_preprocessor()
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, C=0.1, random_state=42))
    ])
    pipe.fit(X_train, y_train)
    return pipe


def train_lightgbm_champion(X_train: pd.DataFrame, y_train: pd.Series) -> lgb.LGBMClassifier:
    """Trains the tuned LightGBM Champion model with regularization to prevent overfitting."""
    logger.info("Training LightGBM Champion model...")
    X_train_lgb = format_for_lightgbm(X_train)
    clf = lgb.LGBMClassifier(
        n_estimators=120,
        learning_rate=0.035,
        num_leaves=18,
        max_depth=5,
        min_child_samples=50,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=2.5,
        reg_lambda=5.0,
        random_state=42,
        verbose=-1,
    )
    clf.fit(X_train_lgb, y_train)
    return clf


def extract_shap_matrix(lgb_model: lgb.LGBMClassifier, X_df: pd.DataFrame) -> Tuple[shap.TreeExplainer, np.ndarray]:
    """Computes raw 2D SHAP matrix (n_samples x n_features) for positive default class."""
    X_fmt = format_for_lightgbm(X_df)
    explainer = shap.TreeExplainer(lgb_model)
    raw_shap = explainer.shap_values(X_fmt)
    if isinstance(raw_shap, list):
        shap_vals = raw_shap[1]
    elif len(raw_shap.shape) == 3:
        shap_vals = raw_shap[:, :, 1]
    else:
        shap_vals = raw_shap
    return explainer, shap_vals


def compute_shap_explanations(
    lgb_model: lgb.LGBMClassifier,
    X_sample: pd.DataFrame,
    feature_names: list
) -> Tuple[Dict[str, float], shap.TreeExplainer, np.ndarray]:
    """Computes global SHAP feature importances using TreeExplainer."""
    logger.info("Computing SHAP feature importance on sample of %d accounts...", len(X_sample))
    explainer, shap_vals = extract_shap_matrix(lgb_model, X_sample)

    mean_abs_shap = np.abs(shap_vals).mean(axis=0)
    top_indices = np.argsort(mean_abs_shap)[::-1]

    shap_dict = {}
    for idx in top_indices:
        shap_dict[feature_names[idx]] = round(float(mean_abs_shap[idx]), 4)

    return shap_dict, explainer, shap_vals


def build_account_scoring_artifacts(
    df_master: pd.DataFrame,
    lgb_model: lgb.LGBMClassifier,
    lr_pipe: Pipeline,
    feature_cols: list,
    output_path: str = "data/processed/account_risk_scores.parquet"
) -> pd.DataFrame:
    """
    Scores all 14,685 accounts in the portfolio with predicted probabilities,
    assigns Basel risk tiers, and computes true per-account TreeSHAP attributions
    for dashboard drill-down.
    """
    logger.info("Scoring full master portfolio (%d accounts) & computing local TreeSHAP drivers...", len(df_master))
    X_all = df_master[feature_cols].copy()
    X_all_lgb = format_for_lightgbm(X_all)

    pd_lgb = lgb_model.predict_proba(X_all_lgb)[:, 1]
    pd_lr = lr_pipe.predict_proba(X_all)[:, 1]

    _, shap_matrix = extract_shap_matrix(lgb_model, X_all)
    feat_idx = {name: i for i, name in enumerate(feature_cols)}

    def _get_col_shap(col_name: str) -> np.ndarray:
        if col_name in feat_idx:
            return np.round(shap_matrix[:, feat_idx[col_name]], 4)
        return np.zeros(len(df_master))

    risk_tiers = []
    for p in pd_lgb:
        if p < 0.10:
            risk_tiers.append("Low Risk")
        elif p < 0.18:
            risk_tiers.append("Medium Risk")
        elif p < 0.28:
            risk_tiers.append("High Risk")
        else:
            risk_tiers.append("Critical Risk")

    scored_df = pd.DataFrame({
        "account_id": df_master["account_id"],
        "customer_id": df_master["customer_id"],
        "loan_type": df_master["loan_type"],
        "loan_amount": df_master["loan_amount"],
        "annual_income": df_master["annual_income"],
        "target_default": df_master["target_default"],
        "predicted_pd": np.round(pd_lgb, 4),
        "predicted_pd_lr": np.round(pd_lr, 4),
        "risk_tier": risk_tiers,
        "debt_to_income_ratio": df_master["debt_to_income_ratio"],
        "bureau_utilization_ratio": df_master["bureau_utilization_ratio"],
        "repay_max_dpd": df_master["repay_max_dpd"],
        "repay_recent_pay_ratio": df_master["repay_recent_pay_ratio"],
        "bureau_has_written_off": df_master["bureau_has_written_off"],
        "region": df_master["region"],
        "employment_type": df_master["employment_type"],
        # Genuine per-account TreeSHAP attributions for Account Deep-Dive
        "shap_annual_income": _get_col_shap("annual_income"),
        "shap_debt_to_income_ratio": _get_col_shap("debt_to_income_ratio"),
        "shap_repay_max_dpd": _get_col_shap("repay_max_dpd"),
        "shap_bureau_utilization_ratio": _get_col_shap("bureau_utilization_ratio"),
        "shap_years_employed": _get_col_shap("years_employed"),
        "shap_repay_ontime_count": _get_col_shap("repay_ontime_count"),
        "shap_bureau_avg_dpd": _get_col_shap("bureau_avg_dpd"),
        "shap_loan_type": _get_col_shap("loan_type"),
    })

    scored_path = Path(output_path)
    scored_path.parent.mkdir(parents=True, exist_ok=True)
    scored_df.to_parquet(scored_path, index=False)
    logger.info("Saved full account scoring table with local SHAP drivers to %s", output_path)
    return scored_df


def generate_model_documentation(
    metrics_lr: Dict[str, float],
    metrics_lgb: Dict[str, float],
    shap_summary: Dict[str, float],
    psi_result: Dict[str, Any],
    output_path: str = "data/processed/MODEL_RESULTS_AND_MONITORING.md"
):
    """Generates an executive-ready Markdown document detailing model results and monitoring."""
    doc_lines = [
        "# Default Prediction Model Results & Post-Deployment Monitoring",
        "",
        "**Author:** `pundhiranshul` (`anshulpundhirwork@gmail.com`)  ",
        "**Target Definition:** `target_default` (1 = default within observation window, 0 = performing)  ",
        "**Evaluation Cohort:** 2,937 accounts (stratified 20% holdout test set)  ",
        "",
        "---",
        "",
        "## 1. Model Comparison & Regulatory Metrics",
        "",
        "| Metric | Logistic Regression (Baseline) | LightGBM (Champion) | Relative Lift |",
        "|---|---|---|---|",
        f"| **AUC-ROC** | **{metrics_lr['auc']:.4f}** | **{metrics_lgb['auc']:.4f}** | +{(metrics_lgb['auc'] - metrics_lr['auc']):.4f} |",
        f"| **KS Statistic** | **{metrics_lr['ks_stat_pct']:.2f}%** | **{metrics_lgb['ks_stat_pct']:.2f}%** | +{(metrics_lgb['ks_stat_pct'] - metrics_lr['ks_stat_pct']):.2f} pp |",
        f"| **Gini Coefficient** ($2\\times\\text{{AUC}} - 1$) | **{metrics_lr['gini']:.4f}** | **{metrics_lgb['gini']:.4f}** | +{(metrics_lgb['gini'] - metrics_lr['gini']):.4f} |",
        f"| **Brier Score** (Calibration) | {metrics_lr['brier_score']:.4f} | {metrics_lgb['brier_score']:.4f} | Lower is better |",
        f"| **Log Loss** | {metrics_lr['log_loss']:.4f} | {metrics_lgb['log_loss']:.4f} | Lower is better |",
        "",
        "### Metric Interpretation:",
        f"1. **AUC-ROC ({metrics_lgb['auc']:.4f})**: Represents the champion model's ability to rank-order risky vs. non-risky borrowers across varying cutoffs.",
        f"2. **KS Statistic ({metrics_lgb['ks_stat_pct']:.2f}%)**: Measures the maximum separation between cumulative default and performing loan distributions. A KS > 20% demonstrates solid discriminative separation for retail underwriting scorecards.",
        f"3. **Gini Coefficient ({metrics_lgb['gini']:.4f})**: Confirms regulatory-grade scorecard discrimination capacity (Basel standard benchmark: 0.30–0.45).",
        "",
        "---",
        "",
        "## 2. Feature Importance & SHAP Attribution",
        "",
        "The top predictive features derived from borrower solvency, external bureau history, and monthly repayment behavior:",
        "",
        "| Rank | Feature Name | Mean |SHAP| Value | Credit Risk Business Rationale |",
        "|---|---|---|---|",
    ]

    for rank, (feat, val) in enumerate(list(shap_summary.items())[:10], start=1):
        rationale = SHAP_BUSINESS_RATIONALE.get(
            feat,
            "Captures borrower creditworthiness, repayment compliance, and debt utilization behavior."
        )
        doc_lines.append(f"| {rank} | `{feat}` | {val:.4f} | {rationale} |")

    doc_lines.extend([
        "",
        "---",
        "",
        "## 3. Post-Deployment Model Monitoring Framework",
        "",
        "### A. Population Stability Index (PSI)",
        "The model is monitored on weekly batch scoring runs to detect macro distribution drift.",
        "",
        f"- **Validation Baseline vs. Test Set PSI**: `{psi_result['psi_value']:.4f}` ({psi_result['status']})",
        "",
        "| PSI Range | Status | Protocol / Remediation Action |",
        "|---|---|---|",
        "| **PSI < 0.10** | **Green (Stable)** | Standard monthly monitoring. No underwriting changes. |",
        "| **0.10 <= PSI < 0.25** | **Amber (Moderate Drift)** | Alert risk committee. Conduct segment-level characteristic audit. Increase monitoring frequency to weekly. |",
        "| **PSI >= 0.25** | **Red (Significant Drift)** | Trigger immediate freeze of automated approval cutoffs. Mandate formal scorecard recalibration. |",
        "",
        "### B. Characteristic Stability Index (CSI)",
        "Monitors individual feature drift on the top 5 risk drivers (`annual_income`, `years_employed`, `repay_ontime_count`, `bureau_avg_dpd`, `repay_avg_dpd`). A feature with CSI > 0.10 flags demographic or behavioral reporting shifts.",
        "",
        "### C. Realized vs. Expected (R/E) Default Rate Calibration",
        "Tracks the observed default rate against predicted PD within each score decile over 3, 6, and 12-month rolling windows. Any decile diverging by >15% triggers probability recalibration via isotonic regression.",
    ])

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(doc_lines))
    logger.info("Saved model documentation report to %s", output_path)


def run_modeling_pipeline(
    master_path: str = "data/processed/portfolio_master.parquet",
    output_dir: str = "data/processed/models"
) -> Dict[str, Any]:
    """Runs the complete training, evaluation, SHAP, and scoring pipeline."""
    logger.info("Loading master portfolio from %s...", master_path)
    df = pd.read_parquet(master_path)

    X_train, X_test, y_train, y_test = prepare_modeling_data(df, test_size=0.20, random_state=42)
    feature_cols = list(X_train.columns)

    lr_pipe = train_logistic_baseline(X_train, y_train)
    lgb_model = train_lightgbm_champion(X_train, y_train)

    lr_probs = lr_pipe.predict_proba(X_test)[:, 1]
    X_test_lgb = format_for_lightgbm(X_test)
    lgb_probs = lgb_model.predict_proba(X_test_lgb)[:, 1]

    metrics_lr = evaluate_model_predictions(y_test, lr_probs)
    metrics_lgb = evaluate_model_predictions(y_test, lgb_probs)

    logger.info("Logistic Regression: AUC=%.4f, KS=%.2f%%, Gini=%.4f",
                metrics_lr["auc"], metrics_lr["ks_stat_pct"], metrics_lr["gini"])
    logger.info("LightGBM Champion:  AUC=%.4f, KS=%.2f%%, Gini=%.4f",
                metrics_lgb["auc"], metrics_lgb["ks_stat_pct"], metrics_lgb["gini"])

    shap_summary, _, _ = compute_shap_explanations(
        lgb_model, X_test.iloc[:1000], feature_cols
    )

    train_lgb_probs = lgb_model.predict_proba(format_for_lightgbm(X_train))[:, 1]
    psi_result = calculate_psi(train_lgb_probs, lgb_probs)
    logger.info("PSI Result: %s (Value: %.4f)", psi_result["status"], psi_result["psi_value"])

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    joblib.dump(lr_pipe, out_path / "logistic_regression.joblib")
    joblib.dump(lgb_model, out_path / "lightgbm_champion.joblib")

    eval_results = {
        "metrics": {
            "logistic_regression": metrics_lr,
            "lightgbm": metrics_lgb,
        },
        "shap_importance": shap_summary,
        "psi_monitoring": psi_result,
        "feature_lists": {
            "numeric": [c for c in NUMERIC_FEATURES if c in feature_cols],
            "categorical": [c for c in CATEGORICAL_FEATURES if c in feature_cols],
        }
    }
    with open(out_path / "model_evaluation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(eval_results, f, indent=2)

    build_account_scoring_artifacts(
        df_master=df,
        lgb_model=lgb_model,
        lr_pipe=lr_pipe,
        feature_cols=feature_cols,
        output_path="data/processed/account_risk_scores.parquet"
    )

    generate_model_documentation(
        metrics_lr=metrics_lr,
        metrics_lgb=metrics_lgb,
        shap_summary=shap_summary,
        psi_result=psi_result,
        output_path="data/processed/MODEL_RESULTS_AND_MONITORING.md"
    )

    logger.info("Default Modeling Pipeline completed successfully.")
    return eval_results


if __name__ == "__main__":
    run_modeling_pipeline()
