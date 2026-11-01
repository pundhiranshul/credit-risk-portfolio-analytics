"""
Page 3 View: Anomaly Review Queue & Human-in-the-Loop Triage.
"""

import streamlit as st
import pandas as pd
import numpy as np

try:
    from config import ANOMALY_METADATA_SPEC, REPO_ROOT
    from theme import color_currency
except (ModuleNotFoundError, ImportError):
    from app.config import ANOMALY_METADATA_SPEC, REPO_ROOT
    from app.theme import color_currency


def render_anomaly_queue(df_master: pd.DataFrame, df_queue: pd.DataFrame, is_dark: bool):
    """Render the dual-lens anomaly detection review queue and officer triage workflow."""
    with st.expander("AI Feature 2 - Governance Specification", expanded=False):
        st.markdown(f"**Feature:** {ANOMALY_METADATA_SPEC['feature_name']}")
        for k, label in [
            ("trigger", "Trigger"),
            ("false_positive", "False Positive"),
            ("false_negative", "False Negative"),
            ("human_in_the_loop", "Human-in-the-Loop"),
        ]:
            st.markdown(f"- **{label}:** {ANOMALY_METADATA_SPEC[k]}")

    # Filter queue to accounts present in current filtered view (df_master/fdf) and apply session decisions
    q_all = df_queue[df_queue["account_id"].isin(df_master["account_id"])].copy()
    if "anomaly_decisions" not in st.session_state:
        st.session_state["anomaly_decisions"] = {}
    saved_decisions = st.session_state.get("anomaly_decisions", {})
    for acc_id, dec_payload in saved_decisions.items():
        mask = q_all["account_id"] == acc_id
        if mask.any():
            q_all.loc[mask, "review_decision"] = dec_payload.get("decision", "Pending Review")
            q_all.loc[mask, "analyst_notes"] = dec_payload.get("notes", "")

    q_flag = q_all[q_all["is_anomaly_flagged"]].copy()

    # KPI strip (dynamically reflects saved session decisions)
    ak1, ak2, ak3, ak4 = st.columns(4)
    anom_kpis = [
        ("Flagged Accounts", f"{len(q_flag):,}", f"{len(q_flag)/max(len(q_all), 1):.1%} of cohort"),
        ("Pending Review", f"{(q_flag['review_decision'] == 'Pending Review').sum():,}", "Action required"),
        ("Confirmed Anomalies", f"{(q_flag['review_decision'].isin(['Confirmed Anomaly (Escalated)', 'Flagged for Field Audit'])).sum():,}", "Escalated"),
        ("Dismissed", f"{(q_flag['review_decision'] == 'Dismissed (Benign)').sum():,}", "Cleared as benign"),
    ]
    for col, (label, val, sub) in zip([ak1, ak2, ak3, ak4], anom_kpis):
        with col:
            st.markdown(
                f'<div class="anomaly-kpi">'
                f'<div class="anomaly-kpi-label">{label}</div>'
                f'<div class="anomaly-kpi-value">{val}</div>'
                f'<div class="anomaly-kpi-sub">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if q_flag.empty:
        st.info("No flagged anomalies match the active sidebar filter criteria.")
        return

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Account Triage</div>', unsafe_allow_html=True)

    flag_ids = list(q_flag["account_id"].unique())
    sel_flag = st.selectbox("Flagged Account ID", flag_ids)
    flag_row = q_flag[q_flag["account_id"] == sel_flag].iloc[0]

    txt_color = "#E8E8E8" if is_dark else "#111111"
    sub_color = "#8A8A97"
    loan_amt_str = color_currency(f"${flag_row['loan_amount']:,.0f}")
    income_str = color_currency(f"${flag_row['annual_income']:,.0f}")

    st.markdown(
        f"<div style='font-size:0.86rem;margin-bottom:6px;'>"
        f"<span style='color:{sub_color};'>Account</span> "
        f"<strong style='color:{txt_color};'>{flag_row['account_id']}</strong>"
        f"&nbsp;&nbsp;<span style='color:{sub_color};'>Score</span> "
        f"<strong style='color:{txt_color};'>{flag_row['anomaly_score']:.1f}/100</strong>"
        f"&nbsp;&nbsp;<span style='color:{sub_color};'>Category</span> "
        f"<strong style='color:{txt_color};'>{flag_row['anomaly_category']}</strong>"
        f"</div>"
        f"<div style='font-size:0.84rem;color:{sub_color};margin-bottom:12px;'>"
        f"Loan type: <span style='color:{txt_color};'>{flag_row['loan_type']}</span>"
        f" · {loan_amt_str}"
        f" · Income {income_str}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("**Flagged reasons:**")
    reasons = flag_row["flag_reasons"]
    if isinstance(reasons, (list, tuple, np.ndarray, pd.Series)):
        for r in reasons:
            st.markdown(f"- {r}")
    elif isinstance(reasons, str):
        import ast
        try:
            parsed = ast.literal_eval(reasons)
            if isinstance(parsed, (list, tuple, np.ndarray)):
                for r in parsed:
                    st.markdown(f"- {r}")
            else:
                st.markdown(f"- {reasons}")
        except Exception:
            st.markdown(f"- {reasons}")
    else:
        st.markdown(f"- {reasons}")

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    st.markdown("**Credit Officer Triage**")

    cur_dec = flag_row.get("review_decision", "Pending Review")
    dec_opts = ["Pending Review", "Confirmed Anomaly (Escalated)", "Dismissed (Benign)", "Flagged for Field Audit"]
    if cur_dec not in dec_opts:
        cur_dec = "Pending Review"
    dec_choice = st.selectbox("Decision", dec_opts, index=dec_opts.index(cur_dec))
    notes = st.text_area(
        "Analyst Notes",
        value=flag_row.get("analyst_notes", ""),
        placeholder="Document rationale for confirmation or dismissal...",
        height=100,
    )

    if st.button("Save Decision", type="primary"):
        st.session_state["anomaly_decisions"][sel_flag] = {
            "decision": dec_choice,
            "notes": notes,
            "officer": "pundhiranshul",
            "ts": str(pd.Timestamp.now()),
        }
        # Persist to parquet on disk so decisions survive reloads
        try:
            queue_path = REPO_ROOT / "data" / "processed" / "anomaly_review_queue.parquet"
            if queue_path.exists():
                disk_q = pd.read_parquet(queue_path)
                disk_q.loc[disk_q["account_id"] == sel_flag, "review_decision"] = dec_choice
                disk_q.loc[disk_q["account_id"] == sel_flag, "analyst_notes"] = notes
                disk_q.to_parquet(queue_path, index=False)
                st.cache_data.clear()
        except Exception:
            pass
        st.success(f"Saved decision for `{sel_flag}`: `{dec_choice}`")
        st.rerun()

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:20px 0 16px 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-label">Full Flagged Queue - Top 50</div>', unsafe_allow_html=True)
    display_cols = [
        "account_id", "loan_type", "loan_amount", "anomaly_score",
        "anomaly_category", "risk_tier", "repay_max_dpd", "review_decision",
    ]
    st.dataframe(q_flag[display_cols].head(50), width="stretch", hide_index=True)
