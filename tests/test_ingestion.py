"""
Unit Tests for Data Ingestion and Quality Cleaning Pipeline
------------------------------------------------------------
Validates:
1. Exact row count preservation (14,685 accounts; 0 dropped rows).
2. Preserved target default count and rate (16.10%).
3. Proper categorical standardization (gender cleaned to Male/Female).
4. Zero unexpected missing values in core modeled attributes (including age_bucket).
5. Imputation indicator integrity (_isna and _invalid_flag flags).
6. Logical constraints (years_employed <= age - 18, years_at_residence <= age).
"""

from pathlib import Path
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def master_df():
    parquet_path = Path("data/processed/portfolio_master.parquet")
    if not parquet_path.exists():
        from src.build import run_full_build
        run_full_build()
    return pd.read_parquet(parquet_path)


def test_row_count_preservation(master_df):
    """Ensures not a single account was dropped during multi-table joins."""
    assert len(master_df) == 14685, f"Expected 14,685 rows, got {len(master_df)}"


def test_target_default_preservation(master_df):
    """Ensures target default rate and count exactly match the ground truth."""
    defaults = master_df["target_default"].sum()
    default_rate = master_df["target_default"].mean()
    assert defaults == 2364, f"Expected 2,364 defaults, got {defaults}"
    assert abs(default_rate - 0.16098) < 1e-4, f"Expected ~16.10% default rate, got {default_rate:.4%}"


def test_gender_standardization(master_df):
    """Ensures 'M' and 'F' variations were cleanly standardized."""
    unique_genders = set(master_df["gender"].unique())
    assert unique_genders.issubset({"Male", "Female", "Unknown"}), f"Unexpected gender values: {unique_genders}"


def test_zero_nulls_in_key_features(master_df):
    """Ensures no unhandled nulls exist in key analytical and risk features."""
    key_features = [
        "account_id",
        "customer_id",
        "loan_type",
        "loan_amount",
        "interest_rate_pct",
        "annual_income",
        "years_employed",
        "num_dependents",
        "years_at_residence",
        "age_bucket", 
        "bureau_utilization_ratio",
        "bureau_max_dpd",
        "repay_payment_ratio",
        "repay_recent_pay_ratio",
        "debt_to_income_ratio",
        "target_default",
    ]
    for col in key_features:
        assert col in master_df.columns, f"Column '{col}' missing from master dataset"
        null_count = master_df[col].isna().sum()
        assert null_count == 0, f"Column '{col}' contains {null_count} unexpected null values."


def test_missingness_indicator_flags(master_df):
    """Validates that _isna and _invalid_flag audit flags exist and are strictly binary."""
    flag_cols = [
        "years_employed_isna",
        "years_employed_invalid_flag",
        "num_dependents_isna",
        "years_at_residence_isna",
        "years_at_residence_invalid_flag",
        "interest_rate_pct_isna",
        "bureau_dpd_isna",
    ]
    for col in flag_cols:
        assert col in master_df.columns, f"Indicator flag {col} missing from master dataset"
        unique_vals = set(master_df[col].unique())
        assert unique_vals.issubset({0, 1}), f"Flag {col} has non-binary values: {unique_vals}"


def test_logical_tenure_constraints(master_df):
    """Ensures impossible tenures (years_employed > age - 18, years_at_residence > age) were corrected."""
    invalid_emp = master_df[master_df["years_employed"] > (master_df["age"] - 18).clip(lower=0)]
    assert len(invalid_emp) == 0, f"Found {len(invalid_emp)} rows with years_employed > (age - 18)."

    invalid_res = master_df[master_df["years_at_residence"] > master_df["age"]]
    assert len(invalid_res) == 0, f"Found {len(invalid_res)} rows with years_at_residence > age."
