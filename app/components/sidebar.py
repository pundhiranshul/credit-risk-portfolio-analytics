"""
Sidebar component for portfolio filtering and AI assistant configuration.
"""
import os
import streamlit as st
import pandas as pd


@st.cache_data
def _get_filter_metadata(df_master: pd.DataFrame) -> dict:
    return {
        "loan_types": sorted(df_master["loan_type"].unique()),
        "loan_counts": df_master["loan_type"].value_counts().to_dict(),
        "tiers": ["Low Risk", "Medium Risk", "High Risk", "Critical Risk"],
        "tier_counts": df_master["risk_tier"].value_counts().to_dict(),
        "regions": sorted(df_master["region"].unique()),
        "region_counts": df_master["region"].value_counts().to_dict(),
    }


def _get_secret(key_name: str) -> str:
    # 1. Check os.environ (direct, uppercase, lowercase)
    val = os.getenv(key_name) or os.getenv(key_name.upper()) or os.getenv(key_name.lower())
    if val:
        return str(val).strip("'\" \t\r\n")

    # 2. Check st.secrets
    try:
        if hasattr(st, "secrets"):
            if key_name in st.secrets:
                return str(st.secrets[key_name]).strip("'\" \t\r\n")
            if key_name.upper() in st.secrets:
                return str(st.secrets[key_name.upper()]).strip("'\" \t\r\n")
            if key_name.lower() in st.secrets:
                return str(st.secrets[key_name.lower()]).strip("'\" \t\r\n")

            # Check nested table e.g. [gemini] api_key = ...
            prefix, _, subkey = key_name.partition("_")
            if prefix and subkey:
                for p in (prefix.lower(), prefix.upper()):
                    if p in st.secrets and hasattr(st.secrets[p], "get"):
                        sec = st.secrets[p]
                        for s in (subkey.lower(), subkey.upper(), "key" if "key" in subkey.lower() else subkey.lower()):
                            if sec.get(s):
                                return str(sec.get(s)).strip("'\" \t\r\n")
    except Exception:
        pass
    return ""


def render_sidebar_filters(df_master: pd.DataFrame, is_dark: bool):
    """
    Render portfolio filters and AI assistant provider selection in the sidebar.
    Returns (filtered_df, api_choice, user_api_key).
    """
    meta = _get_filter_metadata(df_master)
    all_loan_types = meta["loan_types"]
    all_tiers = meta["tiers"]
    all_regions = meta["regions"]

    for lt in all_loan_types:
        st.session_state.setdefault(f"chk_lt_{lt}", True)
    for rt in all_tiers:
        st.session_state.setdefault(f"chk_rt_{rt}", True)
    for rg in all_regions:
        st.session_state.setdefault(f"chk_rg_{rg}", True)

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-sticky-header"><div class="sidebar-sticky-title">Credit Risk Filters</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div class='nav-section-label'>Portfolio Filters</div>", unsafe_allow_html=True)

        # Determine current selections
        sel_loan_types = [lt for lt in all_loan_types if st.session_state.get(f"chk_lt_{lt}", True)]
        sel_tiers = [rt for rt in all_tiers if st.session_state.get(f"chk_rt_{rt}", True)]
        sel_regions = [rg for rg in all_regions if st.session_state.get(f"chk_rg_{rg}", True)]

        # Cross-filtered counts (each dimension filtered by the OTHER two active dimensions)
        lt_live = df_master[df_master["risk_tier"].isin(sel_tiers) & df_master["region"].isin(sel_regions)]["loan_type"].value_counts()
        rt_live = df_master[df_master["loan_type"].isin(sel_loan_types) & df_master["region"].isin(sel_regions)]["risk_tier"].value_counts()
        rg_live = df_master[df_master["loan_type"].isin(sel_loan_types) & df_master["risk_tier"].isin(sel_tiers)]["region"].value_counts()

        # 1. Loan Types
        with st.expander(f"Loan Types ({len(sel_loan_types)}/{len(all_loan_types)})", expanded=True):
            fb1, fb2 = st.columns(2)
            if fb1.button("Select All", key="btn_all_loans", width="stretch"):
                for lt in all_loan_types:
                    st.session_state[f"chk_lt_{lt}"] = True
                st.rerun()
            if fb2.button("Clear", key="btn_clear_loans", width="stretch"):
                for lt in all_loan_types:
                    st.session_state[f"chk_lt_{lt}"] = False
                st.rerun()
            for lt in all_loan_types:
                st.checkbox(f"{lt} ({int(lt_live.get(lt, 0)):,})", key=f"chk_lt_{lt}")

        # 2. Risk Tiers
        with st.expander(f"Risk Tiers ({len(sel_tiers)}/{len(all_tiers)})", expanded=False):
            tb1, tb2 = st.columns(2)
            if tb1.button("Select All", key="btn_all_tiers", width="stretch"):
                for rt in all_tiers:
                    st.session_state[f"chk_rt_{rt}"] = True
                st.rerun()
            if tb2.button("Clear", key="btn_clear_tiers", width="stretch"):
                for rt in all_tiers:
                    st.session_state[f"chk_rt_{rt}"] = False
                st.rerun()
            for rt in all_tiers:
                st.checkbox(f"{rt} ({int(rt_live.get(rt, 0)):,})", key=f"chk_rt_{rt}")

        # 3. Regions
        with st.expander(f"Regions ({len(sel_regions)}/{len(all_regions)})", expanded=False):
            rb1, rb2 = st.columns(2)
            if rb1.button("Select All", key="btn_all_regs", width="stretch"):
                for rg in all_regions:
                    st.session_state[f"chk_rg_{rg}"] = True
                st.rerun()
            if rb2.button("Clear", key="btn_clear_regs", width="stretch"):
                for rg in all_regions:
                    st.session_state[f"chk_rg_{rg}"] = False
                st.rerun()
            for rg in all_regions:
                st.checkbox(f"{rg} ({int(rg_live.get(rg, 0)):,})", key=f"chk_rg_{rg}")

        st.session_state["filter_loan_types"] = set(sel_loan_types)
        st.session_state["filter_risk_tiers"] = set(sel_tiers)
        st.session_state["filter_regions"] = set(sel_regions)

        st.markdown(
            f"<hr style='border:none;border-top:1px solid {'rgba(255,255,255,0.07)' if is_dark else '#EDE8E2'};margin:14px 0;'>",
            unsafe_allow_html=True,
        )

        st.markdown("<div class='nav-section-label'>AI Assistant</div>", unsafe_allow_html=True)
        default_gemini = _get_secret("GEMINI_API_KEY")
        default_openai = _get_secret("OPENAI_API_KEY")
        default_idx = 1 if default_gemini else (2 if default_openai else 0)

        api_choice = st.selectbox(
            "Provider",
            ["Offline Mode", "Google Gemini", "OpenAI"],
            index=default_idx,
            label_visibility="collapsed",
            key="sidebar_ai_provider_select",
        )
        user_api_key = ""
        gemini_model = _get_secret("GEMINI_MODEL") or os.getenv("GEMINI_MODEL", "")
        if "Gemini" in api_choice:
            user_api_key = default_gemini
            if user_api_key:
                if gemini_model:
                    st.caption(f"Google Gemini active ({gemini_model})")
                else:
                    st.caption("Google Gemini active")
            else:
                st.caption("Deterministic offline mode active")
        elif "OpenAI" in api_choice:
            user_api_key = default_openai
            if user_api_key:
                st.caption("OpenAI active")
            else:
                st.caption("Deterministic offline mode active")
        else:
            st.caption("Deterministic offline mode active")

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        st.caption("pundhiranshul · anshulpundhirwork@gmail.com")

    fdf = df_master[
        df_master["loan_type"].isin(sel_loan_types)
        & df_master["risk_tier"].isin(sel_tiers)
        & df_master["region"].isin(sel_regions)
    ].copy()
    return fdf, api_choice, user_api_key
