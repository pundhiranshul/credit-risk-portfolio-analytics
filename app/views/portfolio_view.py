"""
Page 1 View: Executive Portfolio Risk Overview.
"""

import re
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

try:
    from config import PLOTLY_CONFIG, TIER_COLORS
    from theme import get_chart_theme, themed_fig
except (ModuleNotFoundError, ImportError):
    from app.config import PLOTLY_CONFIG, TIER_COLORS
    from app.theme import get_chart_theme, themed_fig


DIM_MAP = {
    "Loan Type": "loan_type",
    "Region": "region",
    "Income": "income_band",
    "Employment": "employment_type",
    "Age": "age_band",
    "Risk Tier": "risk_tier",
}


@st.fragment
def render_dimensional_profiler(fdf: pd.DataFrame, df_master: pd.DataFrame, is_dark: bool):
    dim_map = DIM_MAP

    c_lbl, c_sel = st.columns([1, 1])
    with c_lbl:
        st.markdown('<div class="section-label">Dimensional Profiler</div>', unsafe_allow_html=True)
    with c_sel:
        sel_dim_label = st.selectbox(
            "Split by Dimension",
            list(dim_map.keys()),
            index=0,
            label_visibility="collapsed",
            key="dim_profiler_select",
        )

    dim_col = dim_map[sel_dim_label]

    # Ensure aliases exist on fdf and df_master
    for df_obj in (fdf, df_master):
        if "income_band" not in df_obj.columns and "income_tier" in df_obj.columns:
            df_obj.loc[:, "income_band"] = df_obj["income_tier"]
        if "age_band" not in df_obj.columns and "age_bucket" in df_obj.columns:
            df_obj.loc[:, "age_band"] = df_obj["age_bucket"]

    # Fixed category order from master so bars animate to/from 0 smoothly when filtered
    if dim_col == "risk_tier":
        all_cats = ["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]
    elif dim_col in ("income_band", "income_tier"):
        all_cats = ["Low (<25%)", "Lower-Mid (25-50%)", "Upper-Mid (50-75%)", "High (>75%)"]
    elif dim_col in ("age_band", "age_bucket"):
        all_cats = ["18-30", "31-45", "46-60", "60+"]
    elif hasattr(df_master[dim_col], "cat"):
        all_cats = list(df_master[dim_col].cat.categories)
    else:
        all_cats = sorted(df_master[dim_col].dropna().unique())

    grouped = (
        fdf.groupby(dim_col, observed=False)
        .agg(
            exposure=("loan_amount", "sum"),
            default_rate=("target_default", "mean"),
            count=("account_id", "count"),
        )
        .reindex(all_cats, fill_value=0)
        .reset_index()
    )
    grouped["default_rate"] = grouped["default_rate"].fillna(0.0)

    thm = get_chart_theme(is_dark)
    fig_dim = go.Figure()
    fig_dim.add_trace(go.Bar(
        x=grouped[dim_col],
        y=grouped["exposure"] / 1e6,
        name="Exposure ($M)",
        marker_color=thm["bar"],
        yaxis="y",
    ))
    fig_dim.add_trace(go.Scatter(
        x=grouped[dim_col],
        y=grouped["default_rate"] * 100,
        name="Default Rate (%)",
        mode="lines+markers",
        marker=dict(color=thm["danger"], size=7),
        line=dict(color=thm["danger"], width=2),
        yaxis="y2",
    ))

    max_exp = float(grouped["exposure"].max() / 1e6) if not grouped.empty and grouped["exposure"].max() > 0 else 1.0
    max_rate = float(grouped["default_rate"].max() * 100) if not grouped.empty and grouped["default_rate"].max() > 0 else 1.0

    is_income = (dim_col in ("income_band", "income_tier"))
    xaxis_cfg = dict(
        showgrid=False, linecolor=thm["line"],
        tickfont=dict(size=12, color=thm["tick"]),
        title_font=dict(size=13, color=thm["tick"]),
        categoryorder="array",
        categoryarray=all_cats,
        fixedrange=True,
    )
    if is_income:
        xaxis_cfg.update(
            tickmode="array",
            tickvals=all_cats,
            ticktext=[c.replace(" ", "<br>") for c in all_cats],
            tickangle=0,
        )

    bg_dim = {k: v for k, v in thm["bg"].items() if k != "margin"}
    fig_dim.update_layout(
        **bg_dim, height=330 if is_income else 320,
        dragmode=False,
        hovermode="x unified",
        uirevision=f"dim_profiler_{dim_col}_{is_dark}",
        transition={"duration": 450, "easing": "cubic-in-out"},
        xaxis=xaxis_cfg,
        yaxis=dict(
            title="Exposure ($M)", showgrid=True, gridcolor=thm["grid"],
            tickfont=dict(size=12, color=thm["tick"]),
            title_font=dict(size=13, color=thm["tick"]),
            range=[0, max(max_exp * 1.15, 0.1)],
            fixedrange=True,
        ),
        yaxis2=dict(
            title="Default Rate (%)", overlaying="y", side="right",
            showgrid=False, ticksuffix="%",
            tickfont=dict(size=12, color=thm["danger"]),
            title_font=dict(size=13, color=thm["danger"]),
            range=[0, max(max_rate * 1.5, 5.0)],
            fixedrange=True,
        ),
        legend=dict(
            orientation="h", yanchor="top", y=-0.24 if is_income else -0.18,
            xanchor="center", x=0.5,
            font=dict(size=12, color=thm["tick"]),
            itemclick=False, itemdoubleclick=False,
        ),
        margin=dict(l=10, r=10, t=10, b=42 if is_income else 10),
    )
    st.plotly_chart(fig_dim, config=PLOTLY_CONFIG, width="stretch", key="chart_dimensional_profiler")


def render_portfolio_view(fdf: pd.DataFrame, is_dark: bool, df_master: pd.DataFrame = None, **kwargs):
    """Render the high-level executive portfolio risk metrics and charts."""
    if df_master is None:
        try:
            from data import load_all_dashboard_data
            df_master, _, _ = load_all_dashboard_data()
        except Exception:
            df_master = fdf

    col_a, col_b = st.columns([1, 1.2], gap="large")

    with col_a:
        st.markdown('<div class="section-label">Risk Tier Composition</div>', unsafe_allow_html=True)
        TIER_ORDER = ["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]
        TIER_COLORS_MAP = {
            "Low Risk": "#10B981",
            "Medium Risk": "#F59E0B",
            "High Risk": "#F97316",
            "Critical Risk": "#EF4444",
        }

        tier_counts = fdf["risk_tier"].value_counts().reindex(TIER_ORDER, fill_value=0)
        total_acc = int(tier_counts.sum())
        r = 78
        circ = 2 * 3.14159265 * r

        cumulative_pct = 0.0
        circles_svg = []
        legend_items = []

        for tier in TIER_ORDER:
            cnt = int(tier_counts[tier])
            pct = (cnt / total_acc) if total_acc > 0 else 0.0
            dash = pct * circ
            gap = circ - dash
            offset = -cumulative_pct * circ
            cumulative_pct += pct
            color = TIER_COLORS_MAP.get(tier, "#94A3B8")
            opacity = "1" if cnt > 0 else "0.15"

            circles_svg.append(
                f'<circle class="live-annular-seg" cx="110" cy="110" r="{r}" '
                f'fill="none" stroke="{color}" stroke-width="26" '
                f'stroke-dasharray="{dash:.2f} {gap:.2f}" '
                f'stroke-dashoffset="{offset:.2f}" '
                f'style="transition: stroke-dasharray 0.55s cubic-bezier(0.22,1,0.36,1), '
                f'stroke-dashoffset 0.55s cubic-bezier(0.22,1,0.36,1), opacity 0.35s ease; '
                f'opacity:{opacity};">'
                f'<title>{tier}: {cnt:,} accounts ({pct*100:.1f}%)</title></circle>'
            )
            legend_items.append(
                f'<div style="display:flex;align-items:center;justify-content:space-between;'
                f'padding:4px 0;opacity:{"1" if cnt > 0 else "0.4"};transition:opacity 0.3s ease;">'
                f'<span style="display:flex;align-items:center;gap:8px;font-size:0.82rem;">'
                f'<span style="width:10px;height:10px;border-radius:50%;background:{color};display:inline-block;"></span>'
                f'{tier}</span>'
                f'<span style="font-weight:600;font-size:0.82rem;font-variant-numeric:tabular-nums;">'
                f'{cnt:,} <span style="opacity:0.65;font-weight:400;">({pct*100:.1f}%)</span></span></div>'
            )

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;justify-content:space-around;gap:16px;padding:12px 8px;height:320px;box-sizing:border-box;">
                <div style="position:relative;width:220px;height:220px;flex-shrink:0;">
                    <svg width="220" height="220" viewBox="0 0 220 220" style="transform:rotate(-90deg);">
                        <circle cx="110" cy="110" r="{r}" fill="none"
                                stroke="{'rgba(255,255,255,0.06)' if is_dark else 'rgba(0,0,0,0.06)'}"
                                stroke-width="26"/>
                        {"".join(circles_svg)}
                    </svg>
                    <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                                align-items:center;justify-content:center;pointer-events:none;">
                        <div style="font-size:1.35rem;font-weight:700;font-variant-numeric:tabular-nums;color:{'#F1F5F9' if is_dark else '#0F172A'};">
                            {total_acc:,}
                        </div>
                        <div style="font-size:0.72rem;opacity:0.65;text-transform:uppercase;letter-spacing:0.05em;color:{'#94A3B8' if is_dark else '#64748B'};">
                            Active Accounts
                        </div>
                    </div>
                </div>
                <div style="flex:1;min-width:150px;max-width:210px;color:{'#F1F5F9' if is_dark else '#0F172A'};">
                    {"".join(legend_items)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        render_dimensional_profiler(fdf, df_master, is_dark)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:12px 0 20px 0;'>", unsafe_allow_html=True)
    
    col_c, col_d = st.columns(2, gap="large")
    
    with col_c:
        st.markdown('<div class="section-label">Cross-Cut: Income Tier × Loan Type Default Rate (%)</div>', unsafe_allow_html=True)
        ct = pd.crosstab(
            fdf["income_tier"], fdf["loan_type"],
            values=fdf["target_default"], aggfunc="mean"
        ) * 100
        
        fig_heat = px.imshow(
            ct.round(1), text_auto=False,
            color_continuous_scale="RdYlGn_r",
            labels=dict(x="Loan Type", y="Income Tier", color="Default %"),
            aspect="auto",
        )
        themed_fig(fig_heat, is_dark=is_dark, height=300, hide_legend=False)
        
        z_min = float(ct.values.min()) if ct.size > 0 else 0.0
        z_max = float(ct.values.max()) if ct.size > 0 else 100.0
        z_range = max(z_max - z_min, 1e-6)
        
        annotations = []
        for row_label in ct.index:
            for col_label in ct.columns:
                val = ct.loc[row_label, col_label]
                if pd.isna(val):
                    continue
                norm_val = max(0.0, min(1.0, (val - z_min) / z_range))
                rgb_str = pc.sample_colorscale("RdYlGn_r", [norm_val])[0]
                nums = [float(x) for x in re.findall(r"[\d\.]+", rgb_str)[:3]]
                lum = 0.299 * nums[0] + 0.587 * nums[1] + 0.114 * nums[2]
                text_color = "#111827" if lum > 140 else "#FFFFFF"
                annotations.append(
                    dict(
                        x=col_label, y=row_label, text=f"<b>{val:.1f}</b>",
                        font=dict(size=13, color=text_color),
                        showarrow=False,
                    )
                )
                
        fig_heat.update_layout(annotations=annotations, margin=dict(l=10, r=10, t=10, b=10))
        thm = get_chart_theme(is_dark)
        fig_heat.update_xaxes(tickfont=dict(size=12, color=thm["tick"]), title_font=dict(size=13, color=thm["tick"]))
        fig_heat.update_yaxes(tickfont=dict(size=12, color=thm["tick"]), title_font=dict(size=13, color=thm["tick"]))
        fig_heat.update_coloraxes(colorbar=dict(
            tickfont=dict(size=11, color=thm["tick"]),
            title=dict(text="Default %", font=dict(size=12, color=thm["tick"])),
        ))
        st.plotly_chart(fig_heat, config=PLOTLY_CONFIG, width="stretch")

    with col_d:
        st.markdown('<div class="section-label">Origination Vintage Trends</div>', unsafe_allow_html=True)
        if "origination_date" in fdf.columns:
            vintage_df = fdf.assign(
                vintage_month=pd.to_datetime(fdf["origination_date"]).dt.to_period("M").astype(str)
            )
            vintage_g = vintage_df.groupby("vintage_month").agg(
                exposure=("loan_amount", "sum"),
                default_rate=("target_default", "mean")
            ).reset_index().sort_values("vintage_month")
            
            fig_vint = go.Figure()
            fig_vint.add_trace(go.Bar(
                x=vintage_g["vintage_month"],
                y=vintage_g["exposure"] / 1e6,
                name="Exposure ($M)",
                marker_color=thm["bar"],
                yaxis="y",
            ))
            fig_vint.add_trace(go.Scatter(
                x=vintage_g["vintage_month"],
                y=vintage_g["default_rate"] * 100,
                name="Default Rate (%)",
                mode="lines",
                marker=dict(color=thm["danger"]),
                line=dict(color=thm["danger"], width=2.5),
                yaxis="y2",
            ))
            
            max_v_exp = float(vintage_g["exposure"].max() / 1e6) if not vintage_g.empty else 1.0
            max_v_rate = float(vintage_g["default_rate"].max() * 100) if not vintage_g.empty else 1.0
            
            bg_vint = {k: v for k, v in thm["bg"].items() if k != "margin"}
            fig_vint.update_layout(
                **bg_vint, height=300,
                dragmode=False, hovermode="x unified",
                xaxis=dict(showgrid=False, linecolor=thm["line"],
                           tickfont=dict(size=10, color=thm["tick"]),
                           fixedrange=True, nticks=8),
                yaxis=dict(showgrid=True, gridcolor=thm["grid"], range=[0, max_v_exp * 1.15],
                           tickfont=dict(size=11, color=thm["tick"]), fixedrange=True),
                yaxis2=dict(overlaying="y", side="right", showgrid=False, ticksuffix="%",
                            range=[0, max_v_rate * 1.5], tickfont=dict(size=11, color=thm["danger"]), fixedrange=True),
                legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, font=dict(size=12, color=thm["tick"])),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_vint, config=PLOTLY_CONFIG, width="stretch")
        else:
            st.info("Origination date not available for vintage trends.")
            
    st.markdown("<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:8px 0 20px 0;'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Segment Performance Summary</div>', unsafe_allow_html=True)
    
    sel_dim_label = st.session_state.get("dim_profiler_select", "Loan Type")
    sel_dim = DIM_MAP.get(sel_dim_label, "loan_type")

    if "income_band" not in fdf.columns and "income_tier" in fdf.columns:
        fdf.loc[:, "income_band"] = fdf["income_tier"]
    if "age_band" not in fdf.columns and "age_bucket" in fdf.columns:
        fdf.loc[:, "age_band"] = fdf["age_bucket"]
    
    perf = fdf.groupby(sel_dim, observed=False).agg(
        Accounts=("account_id", "count"),
        Total_Balance=("loan_amount", "sum"),
        Avg_Balance=("loan_amount", "mean"),
        Avg_Income=("annual_income", "mean"),
        Default_Rate=("target_default", "mean"),
        Avg_DTI=("debt_to_income_ratio", "mean"),
        Bureau_Util=("bureau_utilization_ratio", "mean"),
    ).reset_index()
    
    perf["Total_Balance"] = perf["Total_Balance"].apply(lambda x: f"${x:,.0f}")
    perf["Avg_Balance"] = perf["Avg_Balance"].apply(lambda x: f"${x:,.0f}")
    perf["Avg_Income"] = perf["Avg_Income"].apply(lambda x: f"${x:,.0f}")
    perf["Default_Rate"] = perf["Default_Rate"].apply(lambda x: f"{x:.2%}")
    perf["Avg_DTI"] = perf["Avg_DTI"].apply(lambda x: f"{x:.2f}")
    perf["Bureau_Util"] = perf["Bureau_Util"].apply(lambda x: f"{x:.1%}")
    perf.rename(columns={sel_dim: sel_dim_label}, inplace=True)
    
    st.dataframe(perf, width="stretch", hide_index=True)
