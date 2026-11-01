"""
Unit Tests for Portfolio Analytics Engine
-----------------------------------------
Validates:
1. Correct profiling across all 5 dimensions (income, employment, region, age, loan type).
2. Presence and validity of all 5 strategic insights and actionable 'So What' entries.
3. Cross-dimensional cut accuracy.
4. Consistency between summary totals and ground truth portfolio numbers.
"""

import json
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def analytics_data():
    json_path = Path("data/processed/portfolio_analytics.json")
    if not json_path.exists():
        from src.build import run_full_build
        run_full_build()
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_portfolio_summary_totals(analytics_data):
    """Ensures portfolio summary matches ground truth totals."""
    summary = analytics_data["portfolio_summary"]
    assert summary["total_accounts"] == 14685
    assert summary["total_defaults"] == 2364
    assert abs(summary["overall_default_rate"] - 0.1610) < 1e-3
    assert summary["total_exposure"] > 600_000_000


def test_all_five_dimensions_profiled(analytics_data):
    """Ensures income, employment_type, region, age_bucket, and loan_type exist."""
    required_dims = ["income_tier", "employment_type", "region", "age_bucket", "loan_type"]
    profiles = analytics_data["profiles"]
    for dim in required_dims:
        assert dim in profiles, f"Dimension '{dim}' missing from analytics profiles"
        assert len(profiles[dim]) > 0, f"Dimension '{dim}' has empty profile records"


def test_five_strategic_insights_structure(analytics_data):
    """Ensures exactly 5 strategic insights exist with observation and actionable so_what."""
    insights = analytics_data["insights"]
    assert len(insights) == 5, f"Expected 5 strategic insights, got {len(insights)}"
    for ins in insights:
        assert "id" in ins
        assert "title" in ins and len(ins["title"]) > 5
        assert "observation" in ins and len(ins["observation"]) > 20
        assert "so_what" in ins and len(ins["so_what"]) > 20
        assert "key_figures" in ins and len(ins["key_figures"]) > 0


def test_cross_dimensional_cuts(analytics_data):
    """Ensures cross-cuts exist and contain valid default rate metrics."""
    cross_cuts = analytics_data["cross_cuts"]
    assert "income_x_loan_default_rate" in cross_cuts
    assert "employment_x_loan_default_rate" in cross_cuts

    # Verify low-income mortgage default rate is elevated
    inc_x_loan = cross_cuts["income_x_loan_default_rate"]
    assert "Mortgage" in inc_x_loan
    mortgage_rates = inc_x_loan["Mortgage"]
    assert mortgage_rates["Low (<25%)"] > mortgage_rates["High (>75%)"]
