"""
Page 4 View: Strategic Insights & Executive Policy Prescriptions.
"""
import streamlit as st
try:
    from theme import color_currency
except (ModuleNotFoundError, ImportError):
    from app.theme import color_currency


def render_strategic_insights(analytics_json: dict, is_dark: bool):
    """Render top 5 data-driven portfolio findings and actionable policy prescriptions."""
    st.caption("Each insight includes the data observation, a key metric, and an actionable policy prescription.")
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    insights = analytics_json.get("insights", [])
    if not insights:
        st.info("Run `python src/build.py` to generate insights.")
    else:
        for ins in insights:
            st.markdown(
                f'<div class="insight-card">'
                f'<div class="insight-no">Finding #{ins["id"]}</div>'
                f'<h4 class="insight-title">{ins["title"]}</h4>'
                f'<span class="insight-highlight">{color_currency(ins["metric_highlight"])}</span>'
                f'<p class="insight-obs">{color_currency(ins["observation"])}</p>'
                f'<div class="insight-sowhat">'
                f'<span class="insight-sowhat-label">Actionable So What</span>'
                f'{color_currency(ins["so_what"])}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
