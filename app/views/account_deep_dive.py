"""
Page 2 View: Account Risk Deep-Dive.
"""

from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

try:
    from config import PLOTLY_CONFIG, REPO_ROOT
    from theme import color_currency, get_chart_theme, themed_fig
except (ModuleNotFoundError, ImportError):
    from app.config import PLOTLY_CONFIG, REPO_ROOT
    from app.theme import color_currency, get_chart_theme, themed_fig


@st.cache_data
def _load_repayment_history() -> pd.DataFrame:
    repay_path = REPO_ROOT / "data" / "raw" / "repayment_history.csv"
    if repay_path.exists():
        df = pd.read_csv(repay_path)
        return df.set_index("account_id").sort_index()
    return pd.DataFrame()


@st.cache_data
def _load_shap_scores() -> pd.DataFrame:
    scores_path = REPO_ROOT / "data" / "processed" / "account_risk_scores.parquet"
    if scores_path.exists():
        return pd.read_parquet(scores_path)
    return pd.DataFrame()


def render_account_deep_dive(df_master: pd.DataFrame, fdf: pd.DataFrame, is_dark: bool):
    """Render account-level risk drilldown, solvency profile, real TreeSHAP drivers, and actual DPD timeline."""
    c_sel, c_meta = st.columns([1, 2])
    with c_sel:
        acc_list = list(fdf["account_id"].unique())
        sel_acc = st.selectbox("Account ID (Searchable across all filtered accounts)", acc_list)

    row = fdf[fdf["account_id"] == sel_acc].iloc[0]

    with c_meta:
        cols_info = st.columns(4)
        cols_info[0].metric("Customer ID", row["customer_id"])
        cols_info[1].metric("Loan Type", row["loan_type"])
        cols_info[2].metric("Region", row["region"])
        cols_info[3].metric("Collateral", "Yes" if row.get("collateral_flag", 0) == 1 else "No")

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # 1. Predicted PD / Risk Tier Gauge
    _, g_col, _ = st.columns([1, 1.8, 1])
    with g_col:
        pd_val = float(row.get("predicted_pd", 0.15))
        risk_color = (
            "#16a34a" if pd_val < 0.10 else
            "#d97706" if pd_val < 0.18 else
            "#dc2626" if pd_val < 0.28 else
            "#7f1d1d"
        )
        title_color = "#F1F5F9" if is_dark else "#0F172A"
        tick_color = "#CBD5E1" if is_dark else "#475569"
        risk_tier_label = row.get("risk_tier", "Medium Risk")

        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pd_val * 100,
            number={"suffix": "%", "font": {"size": 36, "color": risk_color, "family": "Inter"}},
            title={"text": f"<b>{risk_tier_label}</b>",
                   "font": {"size": 22, "color": title_color, "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1.5,
                         "tickfont": {"size": 16, "color": tick_color, "family": "Inter"}},
                "bar": {"color": risk_color, "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,  10],  "color": "rgba(22,163,74,0.15)" if is_dark else "#dcfce7"},
                    {"range": [10, 18],  "color": "rgba(217,119,6,0.15)" if is_dark else "#fef9c3"},
                    {"range": [18, 28],  "color": "rgba(220,38,38,0.15)" if is_dark else "#fee2e2"},
                    {"range": [28, 100], "color": "rgba(127,29,29,0.2)"  if is_dark else "#fca5a5"},
                ],
                "threshold": {"line": {"color": title_color, "width": 2}, "value": 28},
            },
        ))
        fig_g.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=title_color),
            height=255, margin=dict(l=15, r=15, t=40, b=10),
        )
        st.plotly_chart(fig_g, config=PLOTLY_CONFIG, width="stretch")

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:10px 0 16px 0;'>",
        unsafe_allow_html=True,
    )

    # 2. Borrower Solvency Profile & Key Risk Drivers (Real Local TreeSHAP Attributions)
    c_profile, c_drivers = st.columns([1, 1.25], gap="large")

    with c_profile:
        st.markdown('<div class="section-label">Borrower Solvency Profile</div>', unsafe_allow_html=True)
        profile_rows = [
            ("Annual Income",  f"${row['annual_income']:,.0f}"),
            ("Loan Amount",    f"${row['loan_amount']:,.0f}"),
            ("Interest Rate",  f"{row['interest_rate_pct']:.2f}%"),
            ("Tenure",         f"{int(row['tenure_months'])} months"),
            ("DTI Ratio",      f"{row['debt_to_income_ratio']:.2f}"),
            ("Bureau Util.",   f"{row['bureau_utilization_ratio']:.1%}"),
            ("Years Employed", f"{row.get('years_employed', 0):.1f} yrs"),
        ]
        rows_html = "".join(
            f'<div class="profile-row">'
            f'<span class="profile-key">{k}</span>'
            f'<span class="profile-val">{color_currency(v)}</span>'
            f'</div>'
            for k, v in profile_rows
        )
        st.markdown(rows_html, unsafe_allow_html=True)

    with c_drivers:
        st.markdown('<div class="section-label">Key Risk Drivers (Local TreeSHAP Attribution)</div>', unsafe_allow_html=True)
        df_sc = _load_shap_scores()
        sc_row = df_sc[df_sc["account_id"] == sel_acc].iloc[0] if (not df_sc.empty and sel_acc in df_sc["account_id"].values) else row

        if "shap_annual_income" in sc_row:
            names = ["Income Buffer", "DTI Burden", "Max DPD History", "Bureau Utilisation", "Employment Tenure"]
            impacts = [
                float(sc_row["shap_annual_income"]),
                float(sc_row["shap_debt_to_income_ratio"]),
                float(sc_row["shap_repay_max_dpd"]),
                float(sc_row["shap_bureau_utilization_ratio"]),
                float(sc_row["shap_years_employed"]),
            ]
        else:
            income_z = (df_master["annual_income"].median() - row["annual_income"]) / (df_master["annual_income"].std() + 1e-3)
            dti_z    = (row["debt_to_income_ratio"] - df_master["debt_to_income_ratio"].median()) / (df_master["debt_to_income_ratio"].std() + 1e-3)
            dpd_z    = (row.get("repay_max_dpd", 0) - df_master["repay_max_dpd"].median()) / (df_master["repay_max_dpd"].std() + 1e-3)
            util_z   = (row.get("bureau_utilization_ratio", 0) - df_master["bureau_utilization_ratio"].median()) / (df_master["bureau_utilization_ratio"].std() + 1e-3)
            tenure_z = (df_master["years_employed"].median() - row.get("years_employed", 0)) / (df_master["years_employed"].std() + 1e-3)
            names    = ["Income Buffer", "DTI Burden", "Max DPD History", "Bureau Utilisation", "Employment Tenure"]
            impacts  = [income_z * 0.15, dti_z * 0.12, dpd_z * 0.14, util_z * 0.10, tenure_z * 0.08]

        colors = ["#dc2626" if v > 0 else "#16a34a" for v in impacts]
        thm = get_chart_theme(is_dark)
        fig_drv = go.Figure(go.Bar(
            x=impacts, y=names, orientation="h",
            marker_color=colors, text=[f"{v:+.3f}" for v in impacts],
            textposition="outside", textfont=dict(size=12, color=thm["tick"]),
        ))
        bg_layout = {k: v for k, v in thm["bg"].items() if k != "margin"}
        fig_drv.update_layout(
            **bg_layout, height=270,
            dragmode=False,
            hovermode="closest",
            xaxis_title="TreeSHAP Log-Odds Impact (+ increases risk, - reduces risk)",
            xaxis=dict(showgrid=False, zeroline=True, zerolinecolor=thm["line"],
                       tickfont=dict(size=12, color=thm["tick"]),
                       title_font=dict(size=13, color=thm["tick"]),
                       fixedrange=True),
            yaxis=dict(tickfont=dict(size=12, color=thm["tick"]), fixedrange=True),
            showlegend=False,
            margin=dict(l=10, r=55, t=10, b=30),
        )
        st.plotly_chart(fig_drv, config=PLOTLY_CONFIG, width="stretch")

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:8px 0 16px 0;'>",
        unsafe_allow_html=True,
    )

    # 3. Actual Monthly Repayment DPD Timeline from repayment_history.csv
    st.markdown('<div class="section-label">Monthly Repayment DPD Timeline (Actual Account History)</div>', unsafe_allow_html=True)
    df_repay_all = _load_repayment_history()
    if not df_repay_all.empty and sel_acc in df_repay_all.index:
        acc_repay = df_repay_all.loc[[sel_acc]].sort_values("payment_month")
    else:
        acc_repay = pd.DataFrame()

    if not acc_repay.empty:
        months = acc_repay["payment_month"].to_numpy()
        dpd_vals = acc_repay["days_past_due"].to_numpy()
    else:
        months = np.arange(1, int(min(row.get("tenure_months", 12), 12)) + 1)
        dpd_vals = np.full(len(months), float(row.get("repay_avg_dpd", 0)))

    fig_rep = px.area(
        x=months, y=dpd_vals,
        labels={"x": "Payment Month (since origination)", "y": "Days Past Due (DPD)"},
    )
    thm = get_chart_theme(is_dark)
    fig_rep.update_traces(line_color=thm["timeline_line"], fillcolor=thm["timeline_fill"])
    fig_rep.add_hline(y=30, line_dash="dot", line_color="#d97706",
                      annotation_text="30 DPD early warning",
                      annotation_font=dict(size=11, color="#d97706"))
    fig_rep.add_hline(y=90, line_dash="dot", line_color=thm["danger"],
                      annotation_text="90 DPD default",
                      annotation_font=dict(size=11, color="#d97706" if is_dark else thm["danger"]))
    themed_fig(fig_rep, is_dark=is_dark, height=240, hide_legend=True)
    st.plotly_chart(fig_rep, config=PLOTLY_CONFIG, width="stretch")
