"""
Data loading and caching pipelines for the Credit Risk Portfolio Analytics Dashboard.
"""
import json
import streamlit as st
import pandas as pd
try:
    from config import REPO_ROOT
except (ModuleNotFoundError, ImportError):
    from app.config import REPO_ROOT
from src.anomaly import build_anomaly_review_queue


@st.cache_data
def load_all_dashboard_data():
    """
    Load master portfolio dataset, risk scores, analytics JSON, and anomaly queue.
    Cached for instant cross-tab transitions.
    """
    data_dir = REPO_ROOT / "data" / "processed"
    master_path = data_dir / "portfolio_master.parquet"
    scores_path = data_dir / "account_risk_scores.parquet"
    analytics_path = data_dir / "portfolio_analytics.json"
    queue_path = data_dir / "anomaly_review_queue.parquet"

    if not master_path.exists():
        with st.spinner("Initial setup: Running ingestion and training models (~8s)..."):
            from src.build import run_full_build
            run_full_build()

    df = pd.read_parquet(master_path)

    if scores_path.exists():
        df_sc = pd.read_parquet(scores_path)
    else:
        df_sc = df[["account_id", "target_default"]].copy()
        df_sc["predicted_pd"] = df_sc["target_default"]
        df_sc["risk_tier"] = "Medium Risk"

    if "predicted_pd" not in df.columns:
        df = pd.merge(df, df_sc[["account_id", "predicted_pd", "risk_tier"]], on="account_id", how="left")

    TIER_CAT = pd.CategoricalDtype(
        categories=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"],
        ordered=True,
    )
    if "risk_tier" in df.columns:
        df["risk_tier"] = df["risk_tier"].astype(TIER_CAT)
    for col in ["loan_type", "region", "delinquency_status"]:
        if col in df.columns:
            df[col] = df[col].astype("category")

    if "income_tier" in df.columns and "income_band" not in df.columns:
        df["income_band"] = df["income_tier"]
    if "age_bucket" in df.columns and "age_band" not in df.columns:
        df["age_band"] = df["age_bucket"]

    analytics = {}
    if analytics_path.exists():
        with open(analytics_path) as f:
            analytics = json.load(f)

    df_q = pd.read_parquet(queue_path) if queue_path.exists() else build_anomaly_review_queue()

    return df, analytics, df_q
