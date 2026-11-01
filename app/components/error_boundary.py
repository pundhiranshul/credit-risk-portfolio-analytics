"""
Error boundary and diagnostic reporting system for robust application fault-tolerance.
"""
import sys
import json
import hashlib
import traceback
import urllib.parse
from datetime import datetime, timezone
import streamlit as st
try:
    from config import REPO_ROOT
except (ModuleNotFoundError, ImportError):
    from app.config import REPO_ROOT


def generate_diagnostics_report(exc: Exception | None = None, user_note: str = "") -> dict:
    """Generate a sanitized system and incident diagnostic payload for auditing."""
    ts = datetime.now(timezone.utc).isoformat()
    raw_hash = f"{ts}-{str(exc)}-{st.session_state.get('active_nav', '')}"
    inc_id = f"INC-{hashlib.md5(raw_hash.encode()).hexdigest()[:8].upper()}"

    sanitized_state = {}
    for k, v in st.session_state.items():
        if any(term in k.lower() for term in ["key", "token", "secret", "password"]):
            sanitized_state[k] = "[REDACTED]"
        elif isinstance(v, (set, list)):
            sanitized_state[k] = list(v)
        elif isinstance(v, (int, float, str, bool)):
            sanitized_state[k] = v
        else:
            sanitized_state[k] = str(type(v))

    tb_str = traceback.format_exc() if exc else "N/A (Proactive Diagnostics Report)"

    return {
        "incident_id": inc_id,
        "timestamp_utc": ts,
        "application": "Credit Risk Portfolio Analytics",
        "author": "pundhiranshul",
        "admin_email": "anshulpundhirwork@gmail.com",
        "active_view": st.session_state.get("active_nav", "Unknown"),
        "error_type": type(exc).__name__ if exc else "Manual Diagnostics",
        "error_message": str(exc) if exc else "No error (User-initiated diagnostic export)",
        "user_note": user_note,
        "filters": {
            "loan_types": list(st.session_state.get("filter_loan_types", [])),
            "risk_tiers": list(st.session_state.get("filter_risk_tiers", [])),
            "regions": list(st.session_state.get("filter_regions", [])),
        },
        "session_state": sanitized_state,
        "environment": {
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
            "streamlit_version": st.__version__,
            "theme": st.session_state.get("app_theme", "light"),
            "font_scale": st.session_state.get("font_scale", 100),
        },
        "traceback": tb_str,
    }


def render_error_boundary(exc: Exception):
    """Render an error dialogue box with download report and send report buttons inside."""
    report = generate_diagnostics_report(exc)
    report_json = json.dumps(report, indent=2)
    inc_id = report["incident_id"]

    try:
        log_dir = REPO_ROOT / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / "incidents.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- {report['timestamp_utc']} {inc_id} ---\n{report_json}\n")
    except Exception:
        pass

    with st.container(border=True):
        st.error(
            f"**Script Execution Error**\n\n"
            f"`{type(exc).__name__}: {str(exc)}`\n\n"
            f"*Incident ID: `{inc_id}` · View: `{report['active_view']}` · Time: {report['timestamp_utc']}*"
        )
        with st.expander("🔍 View Technical Stack Trace", expanded=False):
            st.code(report["traceback"], language="python")

        c1, c2, c3 = st.columns([1.5, 1.5, 1.2])
        with c1:
            st.download_button(
                label="📥 Download Error Report",
                data=report_json,
                file_name=f"error_report_{inc_id.lower()}.json",
                mime="application/json",
                type="primary",
                use_container_width=True,
                key=f"dl_err_{inc_id}"
            )
        with c2:
            subject = urllib.parse.quote(f"[Credit Risk Analytics] Error Incident {inc_id}")
            body = urllib.parse.quote(
                f"Admin Team,\n\nAn application error occurred in Credit Risk Portfolio Analytics:\n\n"
                f"Incident ID: {inc_id}\n"
                f"View: {report['active_view']}\n"
                f"Error: {report['error_type']} - {report['error_message']}\n"
                f"Timestamp: {report['timestamp_utc']}\n\n"
                f"Traceback snippet:\n{report['traceback'][:600]}\n"
            )
            mailto_url = f"mailto:anshulpundhirwork@gmail.com?subject={subject}&body={body}"

            if st.button("📨 Send Report to Admins", key=f"btn_report_{inc_id}", use_container_width=True):
                st.session_state[f"reported_{inc_id}"] = True

            if st.session_state.get(f"reported_{inc_id}", False):
                st.success(f"Incident #{inc_id} logged. [Click here to email admins]({mailto_url})")

        with c3:
            if st.button("🔄 Reset & Reload", key=f"btn_reload_{inc_id}", use_container_width=True):
                st.rerun()
