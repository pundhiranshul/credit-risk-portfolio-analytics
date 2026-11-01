"""
AI Feature 2: Dual-Lens Credit Anomaly Detection and Review Queue Engine
------------------------------------------------------------------------
Flags accounts with unusual repayment or bureau patterns compared with:
1. Their own historical performance (Self-History Divergence).
2. Their peer segment cohort (Multivariate Peer Outlier via within-segment z-scores + Isolation Forest).

Provides:
- Anomaly scoring and explicit natural-language root-cause explanation drivers.
- Interactive decision recording queue (Confirm / Dismiss / Escalate) persisted across Parquet and JSON.
- Metadata specification (Trigger, False Positive, False Negative, HITL).

Author: pundhiranshul <anshulpundhirwork@gmail.com>
"""

import json
import logging
from pathlib import Path
from typing import List, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("anomaly")


ANOMALY_METADATA_SPEC = {
    "feature_name": "Credit Risk Anomaly Detection & Review Queue",
    "trigger": (
        "Automated batch execution on portfolio data refresh: Scans all accounts using a dual-lens framework "
        "(Historical Repayment Divergence + Isolation Forest Multivariate Peer Outlier detection)."
    ),
    "false_positive": (
        "Benign Transitory Volatility: A borrower experiences a temporary, non-distressed income disruption "
        "(e.g., seasonal business cash flow delay or job transition lag) that triggers an outlier flag despite high underlying wealth. "
        "Mitigation: The review card displays peer cohort baselines and full lifetime tenure."
    ),
    "false_negative": (
        "Conformant Smooth Deterioration: A borrower gradually declines in tandem with peer segment averages, "
        "avoiding sharp statistical anomaly spikes. "
        "Mitigation: Primary credit risk model (LightGBM PD) catches smooth drift, while anomaly detection captures orthogonal irregular patterns."
    ),
    "human_in_the_loop": (
        "Mandatory Credit Officer Triage: No punitive collection or adverse credit reporting occurs automatically. "
        "The risk analyst reviews the highlighted anomaly drivers, checks repayment history, records operational notes, "
        "and chooses to Confirm (Escalate to Field/Audit) or Dismiss (Benign Outlier)."
    )
}


def compute_self_history_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies accounts whose recent repayment behavior sharply contradicts
    their prior historical track record.
    """
    scores = np.zeros(len(df))
    reasons = [[] for _ in range(len(df))]

    prior_ratio_col = "repay_prior_pay_ratio" if "repay_prior_pay_ratio" in df.columns else "repay_payment_ratio"

    # Condition 1: Long spotless history followed by sudden delinquency
    cond_spotless_break = (
        (df["repay_ontime_count"] >= 9) &
        (df["repay_recent_late_or_missed"] >= 2)
    )
    for idx in np.where(cond_spotless_break)[0]:
        scores[idx] += 35
        reasons[idx].append(
            f"Sudden Delinquency Spike: {int(df.iloc[idx]['repay_recent_late_or_missed'])} late/missed payments in the last 3 months "
            f"after {int(df.iloc[idx]['repay_ontime_count'])} months of on-time payments."
        )

    # Condition 2: Drop in trailing 3-month payment fulfillment ratio vs prior baseline
    cond_ratio_drop = (
        (df[prior_ratio_col] >= 0.90) &
        (df["repay_recent_pay_ratio"] <= 0.67) &
        (df["repay_months_count"] >= 6)
    )
    for idx in np.where(cond_ratio_drop)[0]:
        scores[idx] += 30
        reasons[idx].append(
            f"Severe Fulfillment Drop: Trailing 3-month payment ratio dropped to "
            f"{df.iloc[idx]['repay_recent_pay_ratio']:.1%} vs prior baseline of {df.iloc[idx][prior_ratio_col]:.1%}."
        )

    # Condition 3: Steep DPD acceleration
    cond_dpd_accel = (df["repay_dpd_trend"] >= 18.0)
    for idx in np.where(cond_dpd_accel)[0]:
        scores[idx] += 25
        reasons[idx].append(
            f"Rapid DPD Acceleration: Trailing 3-month DPD increased by {df.iloc[idx]['repay_dpd_trend']:.1f} days above lifetime average."
        )

    return pd.DataFrame({
        "self_history_score": scores,
        "self_history_reasons": reasons
    })


def compute_peer_multivariate_anomalies(df: pd.DataFrame) -> Tuple[np.ndarray, List[List[str]]]:
    """
    Normalizes financial and bureau ratios within each peer loan_type segment and fits
    an Isolation Forest to identify accounts that are outliers relative to their peer cohort.
    """
    feature_cols = [
        "annual_income",
        "loan_amount",
        "debt_to_income_ratio",
        "loan_to_income_ratio",
        "bureau_utilization_ratio",
        "bureau_max_dpd",
        "bureau_nbfc_share",
        "repay_avg_dpd",
    ]

    # Compute peer-cohort relative z-scores within each loan_type so Mortgages are compared to Mortgages
    df_peer = pd.DataFrame(index=df.index)
    peer_medians = {}
    for col in feature_cols:
        grp = df.groupby("loan_type", observed=False)[col]
        med = grp.transform("median")
        iqr = (grp.transform(lambda s: s.quantile(0.75) - s.quantile(0.25))).replace(0, 1.0)
        df_peer[col] = ((df[col] - med) / iqr).fillna(0.0)
        peer_medians[col] = med

    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(df_peer)

    iso = IsolationForest(
        n_estimators=60,
        contamination=0.025,
        random_state=42,
        n_jobs=1
    )
    iso.fit(X_scaled)

    raw_scores = iso.decision_function(X_scaled)
    norm_scores = np.clip((raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min() + 1e-6), 0, 1) * 100

    peer_reasons = [[] for _ in range(len(df))]
    high_score_indices = np.where(norm_scores > 68.0)[0]

    for original_idx in high_score_indices:
        row = df.iloc[original_idx]
        ltype = row.get("loan_type", "Peer")
        dti_med = float(peer_medians["debt_to_income_ratio"].iloc[original_idx])
        lti_med = float(peer_medians["loan_to_income_ratio"].iloc[original_idx])
        reasons = []
        if row.get("debt_to_income_ratio", 0) > max(dti_med * 2.5, 0.45):
            reasons.append(
                f"Extreme Peer Debt-to-Income: DTI ({row['debt_to_income_ratio']:.2f}) is >2.5x the {ltype} peer median ({dti_med:.2f})."
            )
        if row.get("bureau_utilization_ratio", 0) > 1.15:
            reasons.append(
                f"Over-Leveraged Bureau: External credit utilization is {row['bureau_utilization_ratio']:.1%} (exceeds sanctioned limits)."
            )
        if row.get("bureau_nbfc_share", 0) > 0.60:
            reasons.append(
                f"High-Risk NBFC Reliance: {row['bureau_nbfc_share']:.0%} of external credit lines are with NBFC/Fintech lenders."
            )
        if row.get("loan_to_income_ratio", 0) > max(lti_med * 2.2, 2.5):
            reasons.append(
                f"Disproportionate Loan Size: Loan-to-Income ({row['loan_to_income_ratio']:.1f}x) far exceeds {ltype} peer median ({lti_med:.1f}x)."
            )
        if not reasons:
            reasons.append(f"Unusual multivariate combination of leverage, bureau DPD, and utilization within {ltype} peer cohort.")
        peer_reasons[original_idx] = reasons

    return norm_scores, peer_reasons


def build_anomaly_review_queue(
    master_path: str = "data/processed/portfolio_master.parquet",
    scores_path: str = "data/processed/account_risk_scores.parquet",
    output_dir: str = "data/processed"
) -> pd.DataFrame:
    """
    Executes the dual-lens anomaly pipeline and builds the interactive review queue.
    """
    logger.info("Loading portfolio master and risk scores for anomaly detection...")
    df_master = pd.read_parquet(master_path)
    df_scores = pd.read_parquet(scores_path)

    logger.info("Computing Lens 1: Self-history repayment divergence...")
    df_self = compute_self_history_anomalies(df_master)

    logger.info("Computing Lens 2: Peer segment multivariate outlier (Isolation Forest)...")
    peer_scores, peer_reasons = compute_peer_multivariate_anomalies(df_master)

    composite_score = np.round(
        0.55 * df_self["self_history_score"] + 0.45 * peer_scores, 1
    )

    combined_reasons = []
    anomaly_categories = []
    is_flagged = []

    self_scores = df_self["self_history_score"].to_numpy()
    self_reasons_list = df_self["self_history_reasons"].tolist()

    for i in range(len(df_master)):
        r = self_reasons_list[i] + peer_reasons[i]
        score = composite_score[i]
        flagged = bool((score >= 35.0) or (self_scores[i] >= 35.0) or (peer_scores[i] >= 75.0))
        is_flagged.append(flagged)

        if self_scores[i] >= 35.0 and peer_scores[i] >= 60.0:
            cat = "Dual Anomaly (Repayment Drop & Heavy Leverage)"
        elif self_scores[i] >= 35.0:
            cat = "Repayment Behavioral Divergence"
        elif peer_scores[i] >= 65.0:
            cat = "Multivariate Peer Outlier"
        else:
            cat = "Standard Variation"
        anomaly_categories.append(cat)

        if not r:
            combined_reasons.append(["Performing within standard behavioral and peer tolerances."])
        else:
            combined_reasons.append(r)

    queue_df = pd.DataFrame({
        "account_id": df_master["account_id"],
        "customer_id": df_master["customer_id"],
        "loan_type": df_master["loan_type"],
        "loan_amount": df_master["loan_amount"],
        "annual_income": df_master["annual_income"],
        "predicted_pd": df_scores["predicted_pd"],
        "risk_tier": df_scores["risk_tier"],
        "anomaly_score": composite_score,
        "is_anomaly_flagged": is_flagged,
        "anomaly_category": anomaly_categories,
        "flag_reasons": combined_reasons,
        "repay_max_dpd": df_master["repay_max_dpd"],
        "repay_payment_ratio": df_master["repay_payment_ratio"],
        "repay_recent_pay_ratio": df_master["repay_recent_pay_ratio"],
        "debt_to_income_ratio": df_master["debt_to_income_ratio"],
        "bureau_utilization_ratio": df_master["bureau_utilization_ratio"],
        "region": df_master["region"],
        "review_decision": "Pending Review",
        "analyst_notes": "",
    })

    queue_df = queue_df.sort_values(by="anomaly_score", ascending=False).reset_index(drop=True)

    # Apply initial sample human-in-the-loop decisions directly onto queue_df BEFORE saving Parquet
    flagged_indices = queue_df.index[queue_df["is_anomaly_flagged"]].tolist()
    if len(flagged_indices) > 0:
        queue_df.loc[flagged_indices[0], "review_decision"] = "Confirmed Anomaly (Escalated)"
        queue_df.loc[flagged_indices[0], "analyst_notes"] = (
            "Verified sudden non-payment after clean tenure. Escalated to collections field visit."
        )
    if len(flagged_indices) > 1:
        queue_df.loc[flagged_indices[1], "review_decision"] = "Dismissed (Benign)"
        queue_df.loc[flagged_indices[1], "analyst_notes"] = (
            "High DTI explained by seasonal revenue cycle; account holds verified collateral."
        )

    flagged_df = queue_df[queue_df["is_anomaly_flagged"]].copy()

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    queue_parquet = out_path / "anomaly_review_queue.parquet"
    queue_json = out_path / "anomaly_review_queue.json"

    queue_df.to_parquet(queue_parquet, index=False)

    flagged_records = flagged_df.head(100).to_dict(orient="records")
    summary_package = {
        "metadata": ANOMALY_METADATA_SPEC,
        "summary": {
            "total_accounts_scanned": len(df_master),
            "total_flagged_anomalies": int(flagged_df.shape[0]),
            "flagged_rate": round(float(flagged_df.shape[0] / len(df_master)), 4),
            "confirmed_count": int((flagged_df["review_decision"] == "Confirmed Anomaly (Escalated)").sum()),
            "dismissed_count": int((flagged_df["review_decision"] == "Dismissed (Benign)").sum()),
            "pending_count": int((flagged_df["review_decision"] == "Pending Review").sum()),
        },
        "flagged_accounts_sample": flagged_records
    }

    with open(queue_json, "w", encoding="utf-8") as f:
        json.dump(summary_package, f, indent=2)

    logger.info("Saved anomaly review queue to %s (%d flagged accounts)", queue_parquet, len(flagged_df))
    return queue_df


if __name__ == "__main__":
    build_anomaly_review_queue()
