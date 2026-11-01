"""
Header, utility bar, KPI metrics strip, and top navigation components.
"""
import streamlit as st
import pandas as pd
try:
    from config import NAV_ITEMS, PAGE_META
    from theme import color_currency
except (ModuleNotFoundError, ImportError):
    from app.config import NAV_ITEMS, PAGE_META
    from app.theme import color_currency


def render_top_header(is_dark: bool, font_scale: int):
    """Render fixed top header bar containing brand title and utility controls in one row."""
    with st.container(key="top_app_header_bar"):
        c_left, c_title, c_util = st.columns([1.5, 7.0, 1.5], gap="small")
        with c_title:
            st.markdown(
                "<div class='top-center-brand'>Portfolio Risk & Governance</div>",
                unsafe_allow_html=True
            )
        with c_util:
            u1, u2, u3 = st.columns(3, gap="small")
            with u1:
                if st.button("A-", key="font_dec_btn", help="Decrease font size"):
                    st.session_state["font_scale"] = max(70, font_scale - 5)
                    st.rerun()
            with u2:
                if st.button("A+", key="font_inc_btn", help="Increase font size"):
                    st.session_state["font_scale"] = min(140, font_scale + 5)
                    st.rerun()
            with u3:
                theme_tip = "Switch to Light Mode" if is_dark else "Switch to Dark Mode"
                if st.button("", key="top_theme_toggle_btn", help=theme_tip):
                    st.session_state["app_theme"] = "dark" if not is_dark else "light"
                    st.rerun()


def render_kpis(fdf: pd.DataFrame):
    """Render the 5 executive KPI summary cards."""
    total_exp = float(fdf["loan_amount"].sum())
    high_risk_exp = float(fdf[fdf["risk_tier"].isin(["High Risk", "Critical Risk"])]["loan_amount"].sum())
    avg_dti = float(fdf["debt_to_income_ratio"].mean())

    kpis = [
        ("Total Exposure",       f"${total_exp/1e6:.1f}M",              f"{len(fdf):,} accounts"),
        ("Default Rate",         f"{fdf['target_default'].mean():.2%}", f"{int(fdf['target_default'].sum()):,} defaults"),
        ("Avg Loan Size",        f"${fdf['loan_amount'].mean():,.0f}",  f"Avg IR {fdf['interest_rate_pct'].mean():.1f}%"),
        ("High/Crit. Exposure",  f"${high_risk_exp/1e6:.1f}M",         f"{high_risk_exp/total_exp:.1%} of total"),
        ("Avg DTI",              f"{avg_dti:.2f}",                     f"Avg income ${fdf['annual_income'].mean():,.0f}"),
    ]

    k1, k2, k3, k4, k5 = st.columns(5)
    for col, (label, value, sub) in zip([k1, k2, k3, k4, k5], kpis):
        with col:
            st.markdown(
                f'<div class="kpi-card">'
                f'<div class="kpi-label" title="{label}">{label}</div>'
                f'<div class="kpi-value">{color_currency(value)}</div>'
                f'<div class="kpi-sub" title="{sub}">{color_currency(sub)}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:14px 0 12px 0;'>",
        unsafe_allow_html=True
    )


def render_top_nav(active_page: str, chat_is_open: bool):
    """
    Render top navigation bar.
    When chat panel is open, 'Ask the Portfolio' is hidden.
    When chat panel is closed, 'Ask the Portfolio' respawns on the far right.
    """
    if active_page not in ["Portfolio View", "Account Deep-Dive", "Anomaly Review Queue", "Strategic Insights"]:
        active_page = "Portfolio View"
        st.session_state["active_nav"] = "Portfolio View"

    if chat_is_open:
        nav_list = [item for item in NAV_ITEMS if item[0] != "Ask the Portfolio"]
    else:
        nav_list = NAV_ITEMS

    with st.container(key="top_nav_bar"):
        nav_cols = st.columns(len(nav_list), gap="small")

        for col, (label, icon) in zip(nav_cols, nav_list):
            with col:
                if label == "Ask the Portfolio":
                    is_chat_open = chat_is_open
                    if st.button(
                        "✦ Ask the Portfolio",
                        key="btn_ask_portfolio_cta",
                        use_container_width=True,
                    ):
                        new_state = not is_chat_open
                        st.session_state["show_chat_assistant"] = new_state
                        if new_state:
                            st.session_state["auto_close_sidebar"] = True
                            st.session_state["refresh_chat_questions"] = True
                        else:
                            st.session_state["ensure_sidebar_open"] = True
                        st.rerun()
                else:
                    is_active = (active_page == label)
                    btn_type = "primary" if is_active else "secondary"
                    if st.button(f"{icon}  {label}", key=f"topnav_{label}", type=btn_type, use_container_width=True):
                        st.session_state["active_nav"] = label
                        st.rerun()

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:10px 0 14px 0;'>",
        unsafe_allow_html=True
    )


def render_page_header(active_page: str, fdf: pd.DataFrame):
    """Render page title, descriptive subtext, and subtle scroll nudge indicator."""
    raw_title, raw_desc = PAGE_META.get(active_page, ("Dashboard", ""))
    if "{accounts" in raw_desc:
        desc = raw_desc.format(accounts=len(fdf), default_rate=fdf['target_default'].mean())
    else:
        desc = (raw_desc or "").strip()

    sub_html = f'<div class="page-sub"><span class="page-sub-badge">{desc}</span></div>' if desc else ""
    st.markdown(
        f'<div class="page-header-wrap">'
        f'<div class="page-title">{raw_title}</div>'
        f'{sub_html}'
        f'</div>',
        unsafe_allow_html=True
    )
