"""
Credit Risk Portfolio Monitoring & AI Analytics Dashboard
---------------------------------------------------------
Assignment: Credit Risk Portfolio Analytics – Take-Home Assignment (v2)
Author: pundhiranshul <anshulpundhirwork@gmail.com>

Entry Point:
    streamlit run app/app.py
"""
import os
import sys
from pathlib import Path
from PIL import Image
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent

for p in [str(APP_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Load Environment Variables & Synchronize Streamlit Secrets ──────────────
try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env", override=False)
except Exception:
    pass

# Force Streamlit secrets into the OS environment for the Gemini SDK
try:
    if hasattr(st, "secrets"):
        if "GEMINI_API_KEY" in st.secrets:
            os.environ["GEMINI_API_KEY"] = str(st.secrets["GEMINI_API_KEY"]).strip("'\" \t\r\n")
        if "GEMINI_MODEL" in st.secrets:
            os.environ["GEMINI_MODEL"] = str(st.secrets["GEMINI_MODEL"]).strip("'\" \t\r\n")
        for k, v in st.secrets.items():
            if isinstance(v, str):
                os.environ.setdefault(k, str(v).strip("'\" \t\r\n"))
                os.environ.setdefault(k.upper(), str(v).strip("'\" \t\r\n"))
            elif hasattr(v, "items"):
                for sub_k, sub_v in v.items():
                    if isinstance(sub_v, str):
                        clean_v = str(sub_v).strip("'\" \t\r\n")
                        os.environ.setdefault(f"{k}_{sub_k}".upper(), clean_v)
                        if sub_k.lower() in ("api_key", "key") and k.lower() in ("gemini", "openai"):
                            os.environ.setdefault(f"{k.upper()}_API_KEY", clean_v)
                        if sub_k.lower() == "model" and k.lower() in ("gemini", "openai"):
                            os.environ.setdefault(f"{k.upper()}_MODEL", clean_v)
except Exception:
    pass


try:
    try:
        from config import FAVICON_PATH
        from theme import get_css
        from data import load_all_dashboard_data
        from components import (
            render_error_boundary,
            render_sidebar_filters,
            render_top_header,
            render_kpis,
            render_top_nav,
            render_page_header,
            render_ai_assistant_panel,
        )
        from views import (
            render_portfolio_view,
            render_account_deep_dive,
            render_anomaly_queue,
            render_strategic_insights,
        )
    except (ModuleNotFoundError, ImportError, KeyError):
        from app.config import FAVICON_PATH
        from app.theme import get_css
        from app.data import load_all_dashboard_data
        from app.components import (
            render_error_boundary,
            render_sidebar_filters,
            render_top_header,
            render_kpis,
            render_top_nav,
            render_page_header,
            render_ai_assistant_panel,
        )
        from app.views import (
            render_portfolio_view,
            render_account_deep_dive,
            render_anomaly_queue,
            render_strategic_insights,
        )
except KeyError:
    import time
    time.sleep(0.5)
    st.rerun()
from src.llm_assistant import GroundedPortfolioAssistant

# ── Page Configuration ───────────────────────────────────────────────────────────
fav_img = Image.open(FAVICON_PATH) if FAVICON_PATH.exists() else "📊"
st.set_page_config(
    page_title="Credit Risk Portfolio Analytics",
    page_icon=fav_img,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global State Initialization ──────────────────────────────────────────────────
if "app_theme" not in st.session_state:
    st.session_state["app_theme"] = "light"
is_dark = (st.session_state["app_theme"] == "dark")

if "font_scale" not in st.session_state:
    st.session_state["font_scale"] = 100
font_scale = int(st.session_state.get("font_scale", 100))

if "active_nav" not in st.session_state:
    st.session_state["active_nav"] = "Portfolio View"


if "show_chat_assistant" not in st.session_state:
    st.session_state["show_chat_assistant"] = False

if "site_landed" not in st.session_state:
    st.session_state["site_landed"] = True
    st.session_state["ensure_sidebar_open"] = True

if st.session_state.get("active_nav") == "Ask the Portfolio":
    st.session_state["active_nav"] = "Portfolio View"
    st.session_state["show_chat_assistant"] = True
    st.session_state["auto_close_sidebar"] = True
    st.session_state["refresh_chat_questions"] = True

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "anomaly_decisions" not in st.session_state:
    st.session_state["anomaly_decisions"] = {}

# ── Layout & View State ──────────────────────────────────────────────────────────
show_chat = st.session_state.get("show_chat_assistant", False)
active_page = st.session_state.get("active_nav", "Portfolio View")

# ── Inject Dynamic Theme CSS First (Ensures styles & font-scale apply globally) ───
st.markdown(get_css(is_dark, font_scale, show_chat), unsafe_allow_html=True)

# ── Fixed Top Header Bar (Unified horizontal space: Burger, Title, Font/Theme) ───
render_top_header(is_dark, font_scale)

# ── Coordinate Sidebar State (Expand on landing/close, collapse on chat open) ────
auto_close = show_chat and st.session_state.get("auto_close_sidebar", False)
ensure_open = st.session_state.get("ensure_sidebar_open", False) and not show_chat
if auto_close or ensure_open:
    trigger_id = f"sb_{'close' if auto_close else 'open'}_{st.session_state.get('nav_counter', 0)}"
    st.iframe(
        f"""<script>
        (function() {{
            // Trigger: {trigger_id}
            const doc = window.parent.document;
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;
            const isExpanded = sidebar.getAttribute('aria-expanded') === 'true' || sidebar.getAttribute('data-collapsed') !== 'true';
            const shouldClose = {'true' if auto_close else 'false'};
            const shouldOpen = {'true' if ensure_open else 'false'};
            if ((shouldClose && isExpanded) || (shouldOpen && !isExpanded)) {{
                const btn = doc.querySelector('[data-testid="stExpandSidebarButton"] button, [data-testid="collapsedControl"] button, [data-testid="stSidebarCollapseButton"] button, button[aria-label="Collapse sidebar"], button[aria-label="Expand sidebar"]');
                if (btn) btn.click();
            }}
        }})();
        </script>""",
        height=1,
    )
    st.session_state["auto_close_sidebar"] = False
    st.session_state["ensure_sidebar_open"] = False


# ── Data Pipeline ────────────────────────────────────────────────────────────────
df_master, analytics_json, df_queue = load_all_dashboard_data()

# ── Sidebar & Filtering ──────────────────────────────────────────────────────────
fdf, api_choice, user_api_key = render_sidebar_filters(df_master, is_dark)

# ── Main Site Content (Render views when accounts match, else helpful warning) ───
if len(fdf) == 0:
    st.warning("No accounts match the current filters. Adjust your selection in the sidebar.")
else:
    render_kpis(fdf)
    render_top_nav(active_page, show_chat)
    render_page_header(active_page, fdf)

    try:
        if active_page == "Portfolio View":
            render_portfolio_view(fdf, is_dark)
        elif active_page == "Account Deep-Dive":
            render_account_deep_dive(df_master, fdf, is_dark)
        elif active_page == "Anomaly Review Queue":
            render_anomaly_queue(df_master, df_queue, is_dark)
        elif active_page == "Strategic Insights":
            render_strategic_insights(analytics_json, is_dark)
    except Exception as exc:
        render_error_boundary(exc)

# ── Fixed Right Drawer Assistant Panel (Lazy mounted only when drawer open) ────────
with st.container(key="ask_portfolio_side_panel"):
    if show_chat:
        try:
            assistant = GroundedPortfolioAssistant(
                api_key=user_api_key or None,
                provider=api_choice,
                df_override=fdf,
            )
            render_ai_assistant_panel(assistant, is_dark)
        except Exception as exc:
            render_error_boundary(exc)
