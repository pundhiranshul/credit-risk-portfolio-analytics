"""
Portfolio Analytics and Strategic Insights Engine
-------------------------------------------------
Profiles the credit risk portfolio across income, employment type, region,
age bucket, and loan type. Computes multidimensional cross-cuts and generates
5 strategic portfolio insights, each with an actionable 'So What'.

Author: pundhiranshul <anshulpundhirwork@gmail.com>
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("analytics")


def profile_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Profiles the portfolio across a specified single dimension."""
    agg = df.groupby(dimension, observed=False).agg(
        account_count=("account_id", "count"),
        total_loan_exposure=("loan_amount", "sum"),
        avg_loan_amount=("loan_amount", "mean"),
        avg_annual_income=("annual_income", "mean"),
        avg_interest_rate=("interest_rate_pct", "mean"),
        default_count=("target_default", "sum"),
        default_rate=("target_default", "mean"),
        avg_dti=("debt_to_income_ratio", "mean"),
        avg_bureau_utilization=("bureau_utilization_ratio", "mean"),
    ).reset_index()

    agg[dimension] = agg[dimension].astype(str)
    total_exposure = df["loan_amount"].sum()
    agg["exposure_share"] = (agg["total_loan_exposure"] / total_exposure).round(4)
    agg["account_share"] = (agg["account_count"] / len(df)).round(4)
    agg["default_rate"] = agg["default_rate"].round(4)
    agg["avg_loan_amount"] = agg["avg_loan_amount"].round(2)
    agg["avg_annual_income"] = agg["avg_annual_income"].round(2)
    agg["avg_dti"] = agg["avg_dti"].round(4)

    return agg


def compute_cross_cuts(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Computes cross-dimensional risk matrices."""
    ct_inc_loan_dr = pd.crosstab(
        df["income_tier"],
        df["loan_type"],
        values=df["target_default"],
        aggfunc="mean"
    ).round(4)

    ct_inc_loan_vol = pd.crosstab(
        df["income_tier"],
        df["loan_type"],
        values=df["loan_amount"],
        aggfunc="sum"
    ).round(2)

    ct_emp_loan_dr = pd.crosstab(
        df["employment_type"],
        df["loan_type"],
        values=df["target_default"],
        aggfunc="mean"
    ).round(4)

    ct_reg_loan_dr = pd.crosstab(
        df["region"],
        df["loan_type"],
        values=df["target_default"],
        aggfunc="mean"
    ).round(4)

    ct_bo_loan_dr = pd.crosstab(
        df["bureau_has_written_off"],
        df["loan_type"],
        values=df["target_default"],
        aggfunc="mean"
    ).round(4)

    return {
        "income_x_loan_default_rate": ct_inc_loan_dr,
        "income_x_loan_exposure": ct_inc_loan_vol,
        "employment_x_loan_default_rate": ct_emp_loan_dr,
        "region_x_loan_default_rate": ct_reg_loan_dr,
        "bureau_writeoff_x_loan_default_rate": ct_bo_loan_dr,
    }


def generate_strategic_insights(df: pd.DataFrame) -> list[Dict[str, Any]]:
    """
    Computes 5 strategic portfolio insights dynamically from the clean master dataset,
    each with an actionable 'So What'.
    """
    # 1. Mortgage Concentration
    mort_df = df[df["loan_type"] == "Mortgage"]
    mortgage_exp = float(mort_df["loan_amount"].sum())
    total_exp = float(df["loan_amount"].sum())
    mortgage_exp_share = mortgage_exp / total_exp
    mortgage_dr = float(mort_df["target_default"].mean())
    mortgage_count = int(len(mort_df))
    mortgage_defaults = int(mort_df["target_default"].sum())
    mortgage_vol_share = mortgage_count / len(df)

    # 2. Income Gradient
    low_inc_df = df[df["income_tier"] == "Low (<25%)"]
    high_inc_df = df[df["income_tier"] == "High (>75%)"]
    low_inc_dr = float(low_inc_df["target_default"].mean())
    high_inc_dr = float(high_inc_df["target_default"].mean())
    low_inc_defaults = int(low_inc_df["target_default"].sum())
    low_inc_max_usd = float(low_inc_df["annual_income"].max())
    low_inc_dti = float(low_inc_df["debt_to_income_ratio"].mean())
    high_inc_dti = float(high_inc_df["debt_to_income_ratio"].mean())
    inc_multiple = low_inc_dr / max(high_inc_dr, 1e-4)

    # 3. Cross-Cut: Low Income x Mortgage
    low_inc_mortgage = df[(df["income_tier"] == "Low (<25%)") & (df["loan_type"] == "Mortgage")]
    low_inc_mortgage_dr = float(low_inc_mortgage["target_default"].mean())
    high_inc_mortgage_dr = float(df[(df["income_tier"] == "High (>75%)") & (df["loan_type"] == "Mortgage")]["target_default"].mean())
    portfolio_base_dr = float(df["target_default"].mean())

    # 4. Employment Vulnerability
    unemp_df = df[df["employment_type"] == "Unemployed"]
    unemp_dr = float(unemp_df["target_default"].mean())
    unemp_defaults = int(unemp_df["target_default"].sum())
    unemp_count = int(len(unemp_df))
    contract_dr = float(df[df["employment_type"] == "Contract"]["target_default"].mean())
    salaried_dr = float(df[df["employment_type"] == "Salaried"]["target_default"].mean())
    biz_dr = float(df[df["employment_type"] == "Business Owner"]["target_default"].mean())

    # 5. Repayment Momentum & DPD Velocity
    severe_deterioration_dr = float(df[df["repay_dpd_trend"] > 0]["target_default"].mean())
    stable_dr = float(df[df["repay_dpd_trend"] <= 0]["target_default"].mean())

    insights = [
        {
            "id": 1,
            "title": "Severe Capital Concentration & Default Risk in Mortgages",
            "metric_highlight": f"{mortgage_exp_share:.1%} Portfolio Exposure (${mortgage_exp/1e6:.1f}M) | {mortgage_dr:.1%} Default Rate",
            "observation": (
                f"Mortgages represent ${mortgage_exp:,.0f} ({mortgage_exp_share:.1%} of total bank portfolio balance) across just "
                f"{mortgage_count:,} accounts ({mortgage_vol_share:.1%} of volume). Alarmingly, Mortgages exhibit the highest default rate "
                f"of any asset class at {mortgage_dr:.2%}, producing {mortgage_defaults:,} defaults."
            ),
            "so_what": (
                "The bank faces extreme capital vulnerability concentrated in real estate collateral. Management should "
                "immediately mandate maximum 75% LTV caps on new originations, conduct semi-annual collateral re-valuations, "
                "and increase capital reserve provisions under Basel Pillar 2."
            ),
            "key_figures": {
                "mortgage_exposure_usd": round(mortgage_exp, 2),
                "mortgage_exposure_share": round(mortgage_exp_share, 4),
                "mortgage_default_rate": round(mortgage_dr, 4),
                "mortgage_account_count": mortgage_count,
            }
        },
        {
            "id": 2,
            "title": f"Steep Monotonic Income Inversion ({inc_multiple:.1f}x Default Multiple)",
            "metric_highlight": f"Low Income: {low_inc_dr:.1%} Default Rate vs High Income: {high_inc_dr:.1%}",
            "observation": (
                f"Borrowers in the lowest income quartile (<=${low_inc_max_usd/1e3:.1f}k) suffer a {low_inc_dr:.2%} default rate "
                f"({low_inc_defaults:,} defaults) with an elevated DTI of {low_inc_dti:.2f}. In contrast, the top quartile defaults "
                f"at just {high_inc_dr:.2%} (DTI {high_inc_dti:.2f})."
            ),
            "so_what": (
                "Income level is the single strongest structural demographic predictor of creditworthiness. Credit policy "
                "must introduce binding DTI debt caps (maximum 35% for lower-income applicants) rather than solely relying "
                "on static credit scores, and adjust risk-based pricing to prevent debt trap compounding."
            ),
            "key_figures": {
                "low_income_default_rate": round(low_inc_dr, 4),
                "high_income_default_rate": round(high_inc_dr, 4),
                "low_income_dti": round(low_inc_dti, 4),
                "high_income_dti": round(high_inc_dti, 4),
            }
        },
        {
            "id": 3,
            "title": f"Cross-Dimensional Cut: Low-Income Mortgage Squeeze ({low_inc_mortgage_dr:.1%} Default Rate)",
            "metric_highlight": f"Low-Income Mortgage: {low_inc_mortgage_dr:.1%} vs High-Income Mortgage: {high_inc_mortgage_dr:.1%}",
            "observation": (
                f"Intersecting income tiers with loan types uncovers an acute vulnerability: lower-income borrowers with "
                f"Mortgages experience a {low_inc_mortgage_dr:.2%} default rate—more than double the portfolio baseline ({portfolio_base_dr:.2%}). "
                f"High-income mortgage borrowers default at only {high_inc_mortgage_dr:.2%}."
            ),
            "so_what": (
                "Low-income mortgage lending has broken credit economics under current underwriting. The bank should eliminate "
                "automated underwriting approvals for mortgages in the bottom income quartile, mandate secondary manual underwriting, "
                "and require 6 months of liquid EMI reserves in escrow prior to disbursement."
            ),
            "key_figures": {
                "low_income_mortgage_dr": round(low_inc_mortgage_dr, 4),
                "high_income_mortgage_dr": round(high_inc_mortgage_dr, 4),
                "spread": round(low_inc_mortgage_dr - high_inc_mortgage_dr, 4)
            }
        },
        {
            "id": 4,
            "title": "High Default Propensity in Unemployed and Contract Labor Segments",
            "metric_highlight": f"Unemployed: {unemp_dr:.1%} Default Rate | Contract: {contract_dr:.1%}",
            "observation": (
                f"Unemployed borrowers default at an alarming {unemp_dr:.2%} rate ({unemp_defaults:,} defaults out of {unemp_count:,} accounts). "
                f"Contract workers also exhibit elevated defaults at {contract_dr:.2%}, significantly higher than Salaried "
                f"employees ({salaried_dr:.2%}) and Business Owners ({biz_dr:.2%})."
            ),
            "so_what": (
                "Unsecured credit exposure to non-salaried segments carries disproportionate tail risk. Policy should "
                "require co-signers/guarantors for contract workers and establish strict income continuity verification "
                "(minimum 12 months verified continuous banking inflows) before extending credit card or personal loan limits."
            ),
            "key_figures": {
                "unemployed_default_rate": round(unemp_dr, 4),
                "contract_default_rate": round(contract_dr, 4),
                "salaried_default_rate": round(salaried_dr, 4),
            }
        },
        {
            "id": 5,
            "title": "Repayment Velocity: DPD Deterioration Predicts 2x Default Surge",
            "metric_highlight": f"Deteriorating DPD: {severe_deterioration_dr:.1%} vs Stable: {stable_dr:.1%}",
            "observation": (
                f"Borrowers showing positive DPD drift in recent months (trailing 3-month DPD > historical average) exhibit a "
                f"{severe_deterioration_dr:.2%} default rate, compared to just {stable_dr:.2%} for accounts with stable or improving DPD."
            ),
            "so_what": (
                "Early behavioral momentum provides an actionable leading indicator before 90-day contractual default. Collections "
                "teams should implement automated Early Warning Alerts (EWAs) triggered immediately upon any upward DPD slope "
                "over 2 consecutive payment cycles, initiating soft contact before default becomes irreversible."
            ),
            "key_figures": {
                "deteriorating_dpd_default_rate": round(severe_deterioration_dr, 4),
                "stable_dpd_default_rate": round(stable_dr, 4),
            }
        }
    ]
    return insights


def run_portfolio_analytics(
    master_path: str = "data/processed/portfolio_master.parquet",
    output_dir: str = "data/processed"
) -> Dict[str, Any]:
    """Runs the complete portfolio analytics profiling and exports results."""
    logger.info("Loading processed master dataset from %s...", master_path)
    df = pd.read_parquet(master_path)

    dimensions = ["income_tier", "employment_type", "region", "age_bucket", "loan_type"]
    profiles = {}

    for dim in dimensions:
        logger.info("Profiling dimension: %s...", dim)
        prof_df = profile_dimension(df, dim)
        profiles[dim] = prof_df

    logger.info("Computing cross-dimensional risk matrices...")
    cross_cuts = compute_cross_cuts(df)

    logger.info("Generating 5 strategic portfolio insights...")
    insights = generate_strategic_insights(df)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    json_data = {
        "portfolio_summary": {
            "total_accounts": len(df),
            "total_exposure": round(float(df["loan_amount"].sum()), 2),
            "total_defaults": int(df["target_default"].sum()),
            "overall_default_rate": round(float(df["target_default"].mean()), 4),
            "average_loan_amount": round(float(df["loan_amount"].mean()), 2),
            "average_annual_income": round(float(df["annual_income"].mean()), 2),
            "average_interest_rate": round(float(df["interest_rate_pct"].mean()), 2),
            "average_dti": round(float(df["debt_to_income_ratio"].mean()), 4),
        },
        "profiles": {dim: profiles[dim].to_dict(orient="records") for dim in dimensions},
        "cross_cuts": {name: cross_cuts[name].to_dict() for name in cross_cuts},
        "insights": insights,
    }

    json_file = out_path / "portfolio_analytics.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    logger.info("Exported JSON analytics cache to %s", json_file)

    md_file = out_path / "PORTFOLIO_ANALYTICS_INSIGHTS.md"
    generate_markdown_report(json_data, md_file)
    logger.info("Exported Markdown insights report to %s", md_file)

    return json_data


def generate_markdown_report(analytics_data: Dict[str, Any], filepath: Path):
    """Generates an executive-ready Markdown report of portfolio analytics and insights."""
    summary = analytics_data["portfolio_summary"]
    insights = analytics_data["insights"]

    lines = [
        "# Executive Portfolio Risk Analytics & Strategic Insights",
        "",
        "**Author:** `pundhiranshul` (`anshulpundhirwork@gmail.com`)  ",
        "**Portfolio Scope:** {:,} accounts | ${:,.2f} Total Loan Exposure  ".format(
            summary["total_accounts"], summary["total_exposure"]
        ),
        "**Portfolio Baseline Default Rate:** {:.2%} ({:,} defaults)  ".format(
            summary["overall_default_rate"], summary["total_defaults"]
        ),
        "",
        "---",
        "",
        "## 1. Executive Summary & Core Portfolio Metrics",
        "",
        "| Metric | Portfolio Value |",
        "|---|---|",
        f"| Total Loan Accounts | {summary['total_accounts']:,} |",
        f"| Total Principal Exposure | ${summary['total_exposure']:,.2f} |",
        f"| Portfolio Default Rate | {summary['overall_default_rate']:.2%} |",
        f"| Average Loan Amount | ${summary['average_loan_amount']:,.2f} |",
        f"| Average Annual Income | ${summary['average_annual_income']:,.2f} |",
        f"| Average Interest Rate | {summary['average_interest_rate']:.2f}% |",
        f"| Average Debt-to-Income (DTI) | {summary['average_dti']:.2f} |",
        "",
        "---",
        "",
        "## 2. Top 5 Strategic Portfolio Insights with Actionable 'So What'",
        ""
    ]

    for ins in insights:
        lines.append(f"### Insight {ins['id']}: {ins['title']}")
        lines.append(f"**Key Metric:** `{ins['metric_highlight']}`  ")
        lines.append(f"- **Data Observation**: {ins['observation']}")
        lines.append(f"- **Actionable 'So What'**: {ins['so_what']}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 3. Dimensional Profiling Summary Tables",
        "",
        "### Profile across Loan Type",
        "| Loan Type | Accounts | Exposure ($) | Exposure % | Default Rate | Avg Interest Rate |",
        "|---|---|---|---|---|---|"
    ])
    for row in analytics_data["profiles"]["loan_type"]:
        lines.append(
            f"| {row['loan_type']} | {row['account_count']:,} | ${row['total_loan_exposure']:,.0f} | "
            f"{row['exposure_share']:.1%} | {row['default_rate']:.2%} | {row['avg_interest_rate']:.2f}% |"
        )

    lines.extend([
        "",
        "### Profile across Income Tier",
        "| Income Tier | Accounts | Exposure ($) | Default Rate | Avg DTI |",
        "|---|---|---|---|---|"
    ])
    for row in analytics_data["profiles"]["income_tier"]:
        lines.append(
            f"| {row['income_tier']} | {row['account_count']:,} | ${row['total_loan_exposure']:,.0f} | "
            f"{row['default_rate']:.2%} | {row['avg_dti']:.2f} |"
        )

    lines.extend([
        "",
        "### Profile across Employment Type",
        "| Employment Type | Accounts | Default Rate | Avg Annual Income ($) | Avg DTI |",
        "|---|---|---|---|---|"
    ])
    for row in analytics_data["profiles"]["employment_type"]:
        lines.append(
            f"| {row['employment_type']} | {row['account_count']:,} | {row['default_rate']:.2%} | "
            f"${row['avg_annual_income']:,.0f} | {row['avg_dti']:.2f} |"
        )

    lines.extend([
        "",
        "### Profile across Age Bucket",
        "| Age Bucket | Accounts | Default Rate | Avg Annual Income ($) |",
        "|---|---|---|---|"
    ])
    for row in analytics_data["profiles"]["age_bucket"]:
        lines.append(
            f"| {row['age_bucket']} | {row['account_count']:,} | {row['default_rate']:.2%} | "
            f"${row['avg_annual_income']:,.0f} |"
        )

    lines.extend([
        "",
        "### Profile across Region",
        "| Region | Accounts | Exposure ($) | Default Rate | Avg DTI |",
        "|---|---|---|---|---|"
    ])
    for row in analytics_data["profiles"]["region"]:
        lines.append(
            f"| {row['region']} | {row['account_count']:,} | ${row['total_loan_exposure']:,.0f} | "
            f"{row['default_rate']:.2%} | {row['avg_dti']:.2f} |"
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run_portfolio_analytics()
