"""
Feature Engineering and Data Preparation for Credit Risk Modeling
------------------------------------------------------------------
Defines feature sets, categorical encodings, train/test splitting,
and preprocessors for both Logistic Regression (baseline) and LightGBM (champion).

Note on Leakage Prevention:
Post-delinquency collections recovery actions (collections_events.csv) are intentionally
excluded from the default prediction feature matrix so the model strictly uses
origination, demographic, external credit bureau, and repayment behavior signals.

Author: pundhiranshul <anshulpundhirwork@gmail.com>
"""

from typing import List, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


NUMERIC_FEATURES: List[str] = [
    # Demographics & Solvency Ratios
    "annual_income",
    "age",
    "years_employed",
    "num_dependents",
    "years_at_residence",
    "customer_tenure_months",
    "debt_to_income_ratio",
    "loan_to_income_ratio",
    "estimated_monthly_emi",
    # Loan Contract Attributes
    "loan_amount",
    "interest_rate_pct",
    "tenure_months",
    "collateral_flag",
    "loan_seasoning_months",
    # External Bureau Behavior
    "bureau_total_lines",
    "bureau_active_lines",
    "bureau_closed_lines",
    "bureau_written_off_lines",
    "bureau_nbfc_fintech_lines",
    "bureau_total_sanctioned",
    "bureau_total_outstanding",
    "bureau_max_dpd",
    "bureau_avg_dpd",
    "bureau_has_written_off",
    "bureau_utilization_ratio",
    "bureau_nbfc_share",
    # Monthly Repayment History & Trailing Momentum
    "repay_months_count",
    "repay_payment_ratio",
    "repay_prior_pay_ratio",
    "repay_missed_rate",
    "repay_max_dpd",
    "repay_avg_dpd",
    "repay_late_count",
    "repay_missed_count",
    "repay_ontime_count",
    "repay_ever_30dpd",
    "repay_ever_60dpd",
    "repay_ever_90dpd",
    "repay_recent_pay_ratio",
    "repay_recent_max_dpd",
    "repay_recent_late_or_missed",
    "repay_dpd_trend",
    "repay_last_outstanding_balance",
    # Data Quality Audit Indicators
    "years_employed_isna",
    "interest_rate_pct_isna",
    "bureau_dpd_isna",
]

CATEGORICAL_FEATURES: List[str] = [
    "loan_type",
    "loan_purpose",
    "employment_type",
    "occupation_sector",
    "education_level",
    "gender",
    "region",
    "city_tier",
    "housing_type",
    "marital_status",
    "disbursal_channel",
]

TARGET_COL: str = "target_default"


def prepare_modeling_data(
    df: pd.DataFrame, test_size: float = 0.20, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits the master portfolio dataset into train and test sets with stratification
    on the target_default column.
    """
    feature_cols = [c for c in (NUMERIC_FEATURES + CATEGORICAL_FEATURES) if c in df.columns]
    X = df[feature_cols].copy()
    y = df[TARGET_COL].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test


def get_logistic_regression_preprocessor() -> ColumnTransformer:
    """Creates a scikit-learn ColumnTransformer for standard scaling and one-hot encoding."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )


def format_for_lightgbm(df_features: pd.DataFrame) -> pd.DataFrame:
    """Formats categorical columns as pandas category dtypes for native LightGBM processing."""
    df_out = df_features.copy()
    for col in CATEGORICAL_FEATURES:
        if col in df_out.columns:
            df_out[col] = df_out[col].astype("category")
    return df_out
