"""
Theme, CSS, styling utilities, and Plotly theme formatters.
"""
import re
import plotly.graph_objects as go

def color_currency(text: str) -> str:
    """Highlight dollar signs preceding numbers with a dedicated dollar-green span."""
    if not isinstance(text, str):
        return text
    return re.sub(r'\$(\s*\d)', r'<span class="dollar-sign">$</span>\1', text)



def get_css(dark: bool, font_scale: int = 115, show_chat: bool = False) -> str:
    if dark:
        bg        = "#121013"
        panel     = "#1A181C"
        border    = "rgba(255,255,255,0.08)"
        text      = "#EDEDED"
        subtext   = "#A1A1AA"
        inputbg   = "#242226"
        inputbrd  = "rgba(255,255,255,0.10)"
        divider   = "rgba(255,255,255,0.07)"
        hover_bg  = "#242226"
        nav_actbg = "#2C2A2E"
        nav_acttxt = "#FFFFFF"
        nav_txt   = "#A1A1AA"
        table_hdr = "#201E22"
        badge_bg  = "#242226"
        badge_txt = "#EDEDED"
        badge_brd = "rgba(255,255,255,0.10)"
        toggle_bg = "#242226"
        toggle_brd= "rgba(255,255,255,0.10)"
        toggle_active_bg = "#EAE5DB"
        toggle_active_txt = "#111111"
        toggle_txt= "#A1A1AA"
        scrollthumb = "#3F3F46"
        kpi_bg    = "#1A181C"
        kpi_brd   = "rgba(255,255,255,0.08)"
        card_bg   = "#1A181C"
        card_brd  = "rgba(255,255,255,0.08)"
        stapp_bg  = "#121013"
        header_bg = "rgba(18,16,19,0.96)"
        sidebar_bg = "#1A181C"
        sidebar_brd = "rgba(255,255,255,0.08)"
        tag_bg    = "#242226"
        tag_txt   = "#EDEDED"
        tag_brd   = "rgba(255,255,255,0.10)"
        insight_accent = "#EDEDED"
        dollar_green = "#34D399"
    else:
        bg        = "#F4EFE6"
        panel     = "#FAF5ED"
        border    = "rgba(0,0,0,0.08)"
        text      = "#111111"
        subtext   = "#555555"
        inputbg   = "#FFFFFF"
        inputbrd  = "rgba(0,0,0,0.12)"
        divider   = "rgba(0,0,0,0.07)"
        hover_bg  = "rgba(0,0,0,0.04)"
        nav_actbg = "#EAE5DB"
        nav_acttxt = "#111111"
        nav_txt   = "#555555"
        table_hdr = "#FAF5ED"
        badge_bg  = "#FAF5ED"
        badge_txt = "#111111"
        badge_brd = "rgba(0,0,0,0.08)"
        toggle_bg = "#FAF5ED"
        toggle_brd= "rgba(0,0,0,0.10)"
        toggle_active_bg = "#2C2C2C"
        toggle_active_txt = "#FFFFFF"
        toggle_txt= "#555555"
        scrollthumb = "#D1C9BE"
        kpi_bg    = "#FAF5ED"
        kpi_brd   = "rgba(0,0,0,0.08)"
        card_bg   = "#FAF5ED"
        card_brd  = "rgba(0,0,0,0.08)"
        stapp_bg  = "#F4EFE6"
        header_bg = "rgba(244,239,230,0.96)"
        sidebar_bg = "#FAF5ED"
        sidebar_brd = "rgba(0,0,0,0.08)"
        tag_bg    = "#FAF5ED"
        tag_txt   = "#111111"
        tag_brd   = "rgba(0,0,0,0.08)"
        insight_accent = "#111111"
        dollar_green = "#059669"

    import base64

    def _b64_svg(svg_code: str) -> str:
        return "data:image/svg+xml;base64," + base64.b64encode(svg_code.encode("utf-8")).decode("ascii")

    if dark:
        # Dark mode: show Sun icon (to switch to light mode) — exact monochrome Lucide Sun (Screenshot 3)
        _sun_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='4'/><path d='M12 2v2'/><path d='M12 20v2'/><path d='m4.93 4.93 1.41 1.41'/><path d='m17.66 17.66 1.41 1.41'/><path d='M2 12h2'/><path d='M20 12h2'/><path d='m6.34 17.66-1.41 1.41'/><path d='m19.07 4.93-1.41 1.41'/></svg>"
        _sun_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#EDEDED' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='4'/><path d='M12 2v2'/><path d='M12 20v2'/><path d='m4.93 4.93 1.41 1.41'/><path d='m17.66 17.66 1.41 1.41'/><path d='M2 12h2'/><path d='M20 12h2'/><path d='m6.34 17.66-1.41 1.41'/><path d='m19.07 4.93-1.41 1.41'/></svg>"
        toggle_svg = _b64_svg(_sun_svg)
        toggle_svg_hover = _b64_svg(_sun_hover_svg)

        # Dark mode: Burger icon (3 lines) to expand sidebar
        _burger_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><line x1='3' x2='21' y1='5.5' y2='5.5'/><line x1='3' x2='21' y1='12' y2='12'/><line x1='3' x2='21' y1='18.5' y2='18.5'/></svg>"
        _burger_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='#EDEDED' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round'><line x1='3' x2='21' y1='5.5' y2='5.5'/><line x1='3' x2='21' y1='12' y2='12'/><line x1='3' x2='21' y1='18.5' y2='18.5'/></svg>"
        burger_svg = _b64_svg(_burger_svg)
        burger_svg_hover = _b64_svg(_burger_hover_svg)

        # Dark mode: Close icon (X) to collapse sidebar
        _close_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        _close_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#EDEDED' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        close_svg = _b64_svg(_close_svg)
        close_svg_hover = _b64_svg(_close_hover_svg)

        # Dark mode: Plus icon (+) for New Chat - enlarged
        _plus_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><line x1='12' y1='5' x2='12' y2='19'/><line x1='5' y1='12' x2='19' y2='12'/></svg>"
        _plus_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#FFFFFF' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><line x1='12' y1='5' x2='12' y2='19'/><line x1='5' y1='12' x2='19' y2='12'/></svg>"
        plus_svg = _b64_svg(_plus_svg)
        plus_svg_hover = _b64_svg(_plus_hover_svg)

        # Dark mode: Info icon (?) for Governance Specification
        _info_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3'/><line x1='12' y1='17' x2='12.01' y2='17'/></svg>"
        _info_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#FFFFFF' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3'/><line x1='12' y1='17' x2='12.01' y2='17'/></svg>"
        info_svg = _b64_svg(_info_svg)
        info_hover_svg = info_svg_hover = _b64_svg(_info_hover_svg)

        # Dark mode: Panel close icon (✕) - enlarged
        _panel_close_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        _panel_close_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#FFFFFF' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        panel_close_svg = _b64_svg(_panel_close_svg)
        panel_close_hover_svg = _b64_svg(_panel_close_hover_svg)

        # Dark mode: Back arrow icon (←)
        _back_arrow_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#A1A1AA' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='m12 19-7-7 7-7'/><path d='M19 12H5'/></svg>"
        _back_arrow_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#FFFFFF' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='m12 19-7-7 7-7'/><path d='M19 12H5'/></svg>"
        back_arrow_svg = _b64_svg(_back_arrow_svg)
        back_arrow_hover_svg = _b64_svg(_back_arrow_hover_svg)
    else:
        # Light mode: show Moon icon (to switch to dark mode) — exact monochrome Lucide Moon (Screenshot 2)
        _moon_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#374151' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401'/></svg>"
        _moon_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#111111' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401'/></svg>"
        toggle_svg = _b64_svg(_moon_svg)
        toggle_svg_hover = _b64_svg(_moon_hover_svg)

        # Light mode: Burger icon (3 lines) to expand sidebar
        _burger_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='#374151' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><line x1='3' x2='21' y1='5.5' y2='5.5'/><line x1='3' x2='21' y1='12' y2='12'/><line x1='3' x2='21' y1='18.5' y2='18.5'/></svg>"
        _burger_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='#111111' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round'><line x1='3' x2='21' y1='5.5' y2='5.5'/><line x1='3' x2='21' y1='12' y2='12'/><line x1='3' x2='21' y1='18.5' y2='18.5'/></svg>"
        burger_svg = _b64_svg(_burger_svg)
        burger_svg_hover = _b64_svg(_burger_hover_svg)

        # Light mode: Close icon (X) to collapse sidebar
        _close_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#374151' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        _close_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#111111' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        close_svg = _b64_svg(_close_svg)
        close_svg_hover = _b64_svg(_close_hover_svg)

        # Light mode: Plus icon (+) for New Chat - enlarged
        _plus_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#4B5563' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><line x1='12' y1='5' x2='12' y2='19'/><line x1='5' y1='12' x2='19' y2='12'/></svg>"
        _plus_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#111827' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><line x1='12' y1='5' x2='12' y2='19'/><line x1='5' y1='12' x2='19' y2='12'/></svg>"
        plus_svg = _b64_svg(_plus_svg)
        plus_svg_hover = _b64_svg(_plus_hover_svg)

        # Light mode: Info icon (?) for Governance Specification
        _info_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#4B5563' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3'/><line x1='12' y1='17' x2='12.01' y2='17'/></svg>"
        _info_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#111827' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3'/><line x1='12' y1='17' x2='12.01' y2='17'/></svg>"
        info_svg = _b64_svg(_info_svg)
        info_hover_svg = info_svg_hover = _b64_svg(_info_hover_svg)

        # Light mode: Panel close icon (✕) - enlarged
        _panel_close_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#4B5563' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        _panel_close_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#111827' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M18 6 6 18'/><path d='m6 6 12 12'/></svg>"
        panel_close_svg = _b64_svg(_panel_close_svg)
        panel_close_hover_svg = _b64_svg(_panel_close_hover_svg)

        # Light mode: Back arrow icon (←)
        _back_arrow_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#4B5563' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='m12 19-7-7 7-7'/><path d='M19 12H5'/></svg>"
        _back_arrow_hover_svg = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#111827' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='m12 19-7-7 7-7'/><path d='M19 12H5'/></svg>"
        back_arrow_svg = _b64_svg(_back_arrow_svg)
        back_arrow_hover_svg = _b64_svg(_back_arrow_hover_svg)

    return f"""
<style>
@import url('https://cdn.jsdelivr.net/fontsource/css/google-sans:vf@latest/index.css');
@import url('https://cdn.jsdelivr.net/fontsource/css/google-sans-text:vf@latest/index.css');
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, button, input, select, textarea {{
    font-family: 'Google Sans', 'Google Sans Text', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: {font_scale}% !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}}

p, span, label, div {{
    font-family: 'Google Sans', 'Google Sans Text', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* ── Base ─────────────────────────────────────────── */
:root {{
    --primary-color: {"#EAE5DB" if dark else "#2C2A2E"} !important;
    --background-color: {stapp_bg} !important;
    --secondary-background-color: {panel} !important;
    --text-color: {text} !important;
    font-size: {font_scale}% !important;
}}

.stApp {{
    background-color: {stapp_bg} !important;
    color: {text} !important;
}}
/* ── Completely remove native Streamlit creamy header block while preserving sidebar controls ── */
header[data-testid="stHeader"],
[data-testid="stHeader"] {{
    background: transparent !important;
    background-color: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
    border: none !important;
    box-shadow: none !important;
    pointer-events: none !important;
    z-index: 9999999 !important;
    overflow: visible !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
}}

header[data-testid="stHeader"] [data-testid="stToolbar"],
[data-testid="stToolbar"] {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    pointer-events: none !important;
    overflow: visible !important;
    height: 0 !important;
    min-height: 0 !important;
    position: relative !important;
    z-index: 9999999 !important;
}}

header[data-testid="stHeader"] [data-testid="stToolbarActions"],
header[data-testid="stHeader"] [data-testid="stMainMenu"],
header[data-testid="stHeader"] [data-testid="manage-app-button"],
header[data-testid="stHeader"] .stAppDeployButton,
header[data-testid="stHeader"] [data-testid="stStatusWidget"] {{
    display: none !important;
    visibility: hidden !important;
}}

/* ── Sidebar Toggle Controls at the Same Spot (top: 11px; left: 16px) ── */
/* When Collapsed: Burger button opens the left sidebar (No Box, Vertically Middle Justified) */
header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
[data-testid="stExpandSidebarButton"],
button[data-testid="stExpandSidebarButton"] {{
    position: fixed !important;
    top: 21px !important;
    left: 16px !important;
    z-index: 99999999 !important;
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
    min-height: 44px !important;
    max-width: 44px !important;
    max-height: 44px !important;
    padding: 0 !important;
    border-radius: 9px !important;
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    border-color: transparent !important;
    cursor: pointer !important;
    pointer-events: auto !important;
    visibility: visible !important;
    opacity: 1 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    outline: none !important;
    margin: 0 !important;
}}

header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]:hover,
[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stExpandSidebarButton"]:hover {{
    background-color: {hover_bg} !important;
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}}

header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]:focus,
header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]:active,
[data-testid="stExpandSidebarButton"]:focus,
[data-testid="stExpandSidebarButton"]:active,
button[data-testid="stExpandSidebarButton"]:focus,
button[data-testid="stExpandSidebarButton"]:active {{
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}}

header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]::after,
[data-testid="stExpandSidebarButton"]::after,
button[data-testid="stExpandSidebarButton"]::after {{
    content: "" !important;
    display: block !important;
    width: 28px !important;
    height: 28px !important;
    background-image: url("{burger_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    pointer-events: none !important;
    transition: transform 0.15s ease !important;
}}

header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]:hover::after,
[data-testid="stExpandSidebarButton"]:hover::after,
button[data-testid="stExpandSidebarButton"]:hover::after {{
    background-image: url("{burger_svg_hover}") !important;
    transform: scale(1.08) !important;
}}

header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"] *,
[data-testid="stExpandSidebarButton"] *,
button[data-testid="stExpandSidebarButton"] * {{
    display: none !important;
}}

/* When Expanded: Close button (X) collapses the left sidebar at the SAME spot (top: 24px; left: 16px) */
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] {{
    position: fixed !important;
    top: 24px !important;
    left: 16px !important;
    z-index: 99999999 !important;
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    min-height: 38px !important;
    max-width: 38px !important;
    max-height: 38px !important;
    margin: 0 !important;
    padding: 0 !important;
    visibility: visible !important;
    opacity: 1 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    pointer-events: auto !important;
}}

[data-testid="stSidebarCollapseButton"] button {{
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
    min-height: 44px !important;
    max-width: 44px !important;
    max-height: 44px !important;
    padding: 0 !important;
    border-radius: 9px !important;
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    border-color: transparent !important;
    cursor: pointer !important;
    pointer-events: auto !important;
    visibility: visible !important;
    opacity: 1 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    outline: none !important;
    margin: 0 !important;
}}

[data-testid="stSidebarCollapseButton"] button:hover {{
    background-color: {hover_bg} !important;
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}}

[data-testid="stSidebarCollapseButton"] button:focus,
[data-testid="stSidebarCollapseButton"] button:active {{
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}}

[data-testid="stSidebarCollapseButton"] button::after {{
    content: "" !important;
    display: block !important;
    width: 26px !important;
    height: 26px !important;
    background-image: url("{close_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    pointer-events: none !important;
    transition: transform 0.15s ease !important;
}}

[data-testid="stSidebarCollapseButton"] button:hover::after {{
    background-image: url("{close_svg_hover}") !important;
    transform: scale(1.08) !important;
}}

[data-testid="stSidebarCollapseButton"] button * {{
    display: none !important;
}}

/* When sidebar is collapsed, ensure close button is completely hidden so burger button receives clicks cleanly */
[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarCollapseButton"],
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"],
[data-collapsed="true"] [data-testid="stSidebarCollapseButton"] {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}}

/* ── Main Site & Sidebar Layout Coordination ── */
{"/* ── CHAT OPEN MODE (Overlay Left Panel) ── */" if show_chat else "/* ── NORMAL SITE MODE (In-flow Left Panel, Never Masked) ── */"}

.stApp section[data-testid="stMain"],
.stApp [data-testid="stMain"] {{
    padding-top: 0 !important;
    margin-left: {"0" if show_chat else "320px"} !important;
    left: 0 !important;
    margin-right: {"440px" if show_chat else "0"} !important;
    width: {"calc(100% - 440px)" if show_chat else "calc(100% - 320px)"} !important;
    max-width: {"calc(100% - 440px)" if show_chat else "calc(100% - 320px)"} !important;
    box-sizing: border-box !important;
    transition: margin-left 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                margin-right 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                width 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                max-width 0.32s cubic-bezier(0.4, 0, 0.2, 1) !important;
    will-change: margin-left, margin-right, width, max-width;
}}
.stApp section[data-testid="stMain"] .block-container,
.stApp [data-testid="stMain"] .block-container {{
    padding-top: 104px !important;
    padding-left: 28px !important;
    padding-right: 28px !important;
    padding-bottom: 2rem !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    transition: padding 0.32s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

[data-testid="stSidebarHeader"],
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
    visibility: visible !important;
}}
[data-testid="stSidebarContent"],
[data-testid="stSidebar"] [data-testid="stSidebarContent"],
[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
}}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
    padding: 0 22px 2.5rem 22px !important;
    box-sizing: border-box !important;
}}
[data-testid="stSidebar"] .block-container {{
    padding-top: 0 !important;
    padding-left: 22px !important;
    padding-right: 22px !important;
    padding-bottom: 2.5rem !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"],
section[data-testid="stSidebar"] {{
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    bottom: 0 !important;
    height: 100vh !important;
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {sidebar_brd} !important;
    z-index: {999995 if show_chat else 99990} !important;
    box-shadow: {("8px 0 36px rgba(0, 0, 0, 0.45)" if dark else "8px 0 36px rgba(0, 0, 0, 0.16)") if show_chat else "none"} !important;
    margin-left: 0 !important;
    transform: translateX(0) !important;
    cursor: default !important;
    user-select: auto !important;
    transition: transform 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                width 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                min-width 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                max-width 0.32s cubic-bezier(0.4, 0, 0.2, 1) !important;
    will-change: transform, width;
}}
/* Sidebar Content Container - fills full width of sidebar and never shrinks during interactions */
[data-testid="stSidebarContent"],
[data-testid="stSidebar"] [data-testid="stSidebarContent"],
[data-testid="stSidebar"] > div:first-child {{
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    height: 100vh !important;
    overflow-y: auto !important;
    box-sizing: border-box !important;
}}

/* Completely disable and hide Streamlit's native sidebar resize handle so that hovering, clicking, or holding the border line does not activate re-resizable's drag overlay or jump states */
[data-testid="stSidebarResizeHandle"],
div:has(> [data-testid="stSidebarResizeHandle"]),
[data-testid="stSidebar"] [data-testid="stSidebarResizeHandle"],
[data-testid="stSidebar"] ~ [data-testid="stSidebarResizeHandle"],
[data-testid="stSidebar"] > div:last-child:not([data-testid="stSidebarContent"]):has([data-testid="stSidebarResizeHandle"]),
[data-testid="stSidebar"] > div[style*="cursor: col-resize"] {{
    display: none !important;
    pointer-events: none !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    cursor: default !important;
    user-select: none !important;
}}

/* Prevent re-resizable overlay backdrop from interfering with layout or clicks */
[data-testid="stSidebar"] > div.__resizable_base__,
[data-testid="stSidebar"] > div[style*="position: fixed"] {{
    display: none !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
}}

[data-testid="stSidebar"][aria-expanded="false"],
[data-testid="stSidebar"][data-collapsed="true"] {{
    transform: translateX(-100%) !important;
    box-shadow: none !important;
    pointer-events: none !important;
    visibility: hidden !important;
    margin-left: 0 !important;
}}

/* Dynamic sync when sidebar is collapsed by user in normal mode */
{f'''
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) section[data-testid="stMain"],
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stMain"],
.stApp:has([data-testid="stSidebar"][data-collapsed="true"]) section[data-testid="stMain"],
.stApp:has([data-testid="stSidebar"][data-collapsed="true"]) [data-testid="stMain"],
.stApp:has([data-testid="stExpandSidebarButton"]) section[data-testid="stMain"],
.stApp:has([data-testid="stExpandSidebarButton"]) [data-testid="stMain"] {{
    margin-left: 0 !important;
    left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}}
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) .st-key-top_app_header_bar,
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) div[data-testid="stContainer"].st-key-top_app_header_bar,
.stApp:has([data-testid="stSidebar"][data-collapsed="true"]) .st-key-top_app_header_bar,
.stApp:has([data-testid="stSidebar"][data-collapsed="true"]) div[data-testid="stContainer"].st-key-top_app_header_bar,
.stApp:has([data-testid="stExpandSidebarButton"]) .st-key-top_app_header_bar,
.stApp:has([data-testid="stExpandSidebarButton"]) div[data-testid="stContainer"].st-key-top_app_header_bar {{
    left: 0 !important;
    width: 100% !important;
}}
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(1),
.stApp:has([data-testid="stSidebar"][data-collapsed="true"]) .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(1),
.stApp:has([data-testid="stExpandSidebarButton"]) .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(1) {{
    display: flex !important;
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    flex: 0 0 50px !important;
}}
.stApp:has([data-testid="stSidebar"][aria-expanded="true"]) .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(1),
.stApp:not(:has([data-testid="stExpandSidebarButton"])) .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(1) {{
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    flex: 0 0 0 !important;
}}
''' if not show_chat else ''}
[data-testid="stSidebar"] * {{ color: {text}; }}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {{ color: {text} !important; }}
[data-testid="stSidebar"] hr {{ border-color: {divider} !important; }}

/* Sidebar Sticky Header (Credit Risk Filters locked in horizontal plane of Portfolio Risk & Governance) */
[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(.sidebar-sticky-header),
div[data-testid="stElementContainer"]:has(.sidebar-sticky-header) {{
    position: sticky !important;
    top: 0 !important;
    z-index: 9999 !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    margin: 0 -22px 14px -22px !important;
    padding: 0 !important;
    background-color: {sidebar_bg} !important;
    background: {sidebar_bg} !important;
    border-bottom: 1px solid {"rgba(255,255,255,0.08)" if dark else "rgba(0,0,0,0.06)"} !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}}
[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(.sidebar-sticky-header) > div[data-testid="stMarkdown"],
[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(.sidebar-sticky-header) div[data-testid="stMarkdownContainer"] {{
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    display: block !important;
}}
.sidebar-sticky-header {{
    position: relative !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    background-color: {sidebar_bg} !important;
    background: {sidebar_bg} !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    padding: 0 !important;
    margin: 0 !important;
}}
[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(.sidebar-sticky-header) p {{
    margin: 0 !important;
    padding: 0 !important;
}}
.sidebar-sticky-title {{
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.015em !important;
    text-align: center !important;
    color: {"#FFFFFF" if dark else "#0F172A"} !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: nowrap !important;
    pointer-events: none !important;
}}
.sidebar-sticky-divider {{
    display: none !important;
}}

/* ── Custom scrollbar ─────────────────────────────── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {scrollthumb}; border-radius: 2px; }}

/* ── Top Center Branding (Horizontally & Vertically Center Justified) ── */
.top-center-brand {{
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    text-align: center !important;
    font-size: 1.82rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.015em !important;
    color: {text} !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
    white-space: nowrap !important;
    pointer-events: none !important;
    z-index: 10 !important;
}}

/* ── Top Navigation Bar Buttons (Intelligent class-based typography & compact padding) ── */
.st-key-top_nav_bar [data-testid="stHorizontalBlock"] {{
    gap: 6px !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
}}

.st-key-top_nav_bar [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
    min-width: 0 !important;
    flex: 1 1 0 !important;
    padding: 0 !important;
}}

.st-key-top_nav_bar div[data-testid="stButton"]:not(.st-key-btn_ask_portfolio_cta):not(.st-key-nav_btn_ask_portfolio) button,
button[key^="topnav_"] {{
    font-size: clamp(0.85rem, 0.98vw, 0.94rem) !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
    padding: 8px 10px !important;
    min-height: 42px !important;
    height: 42px !important;
    border-radius: 8px !important;
    line-height: 1.30 !important;
    transition: all 0.15s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}}

.st-key-top_nav_bar div[data-testid="stButton"]:not(.st-key-btn_ask_portfolio_cta):not(.st-key-nav_btn_ask_portfolio) button *,
button[key^="topnav_"] * {{
    font-size: clamp(0.85rem, 0.98vw, 0.94rem) !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
    line-height: 1.30 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}}

.st-key-top_nav_bar div[data-testid="stButton"]:not(.st-key-btn_ask_portfolio_cta):not(.st-key-nav_btn_ask_portfolio) button:hover,
button[key^="topnav_"]:hover {{
    transform: translateY(-1px) !important;
}}

/* ── Keyframes for Persistent Attention ── */
@keyframes persistentPulse {{
    0%, 100% {{
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4),
                    0 0 0 1px rgba(168, 85, 247, 0.3);
    }}
    50% {{
        box-shadow: 0 6px 22px rgba(139, 92, 246, 0.65),
                    0 0 0 2px rgba(192, 132, 252, 0.6);
    }}
}}

/* ── Base Button Styling (Persistent Attention) ── */
.st-key-btn_ask_portfolio_cta button,
.st-key-nav_btn_ask_portfolio button {{
    position: relative !important;
    overflow: hidden !important;
    border-radius: 999px !important;
    padding: 0.45rem 1.15rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.015em !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(192, 132, 252, 0.6) !important;
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #C026D3 100%) !important;
    animation: persistentPulse 3.5s ease-in-out infinite !important;
    transition: transform 0.22s ease, filter 0.22s ease, box-shadow 0.22s ease !important;
    min-height: 42px !important;
    height: 42px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
}}

/* ── Disable any sweeping glint pseudo-elements that cause light leakage ── */
.st-key-btn_ask_portfolio_cta button::after,
.st-key-nav_btn_ask_portfolio button::after {{
    display: none !important;
    content: none !important;
}}

/* ── Hover Micro-Interactions ── */
.st-key-btn_ask_portfolio_cta button:hover,
.st-key-nav_btn_ask_portfolio button:hover {{
    transform: translateY(-2px) scale(1.02) !important;
    filter: brightness(1.1) !important;
    box-shadow: 0 8px 26px rgba(124, 58, 237, 0.65),
                0 0 0 2px rgba(233, 213, 255, 0.85) !important;
}}

.st-key-btn_ask_portfolio_cta button:active,
.st-key-nav_btn_ask_portfolio button:active {{
    transform: translateY(0px) scale(0.98) !important;
}}

.st-key-btn_ask_portfolio_cta button p,
.st-key-btn_ask_portfolio_cta button span,
.st-key-btn_ask_portfolio_cta button div,
.st-key-nav_btn_ask_portfolio button p,
.st-key-nav_btn_ask_portfolio button span,
.st-key-nav_btn_ask_portfolio button div {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.25) !important;
}}

/* ── General Interactive Buttons (Proportional Class-Based Sizing) ── */
div[data-testid="stButton"]:not(.st-key-top_nav_bar *):not(.st-key-gcp_chat_header_sticky *):not(.st-key-gcp_suggested_questions_wrap *):not(.st-key-top_app_header_bar *) button {{
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 7px 16px !important;
    min-height: 38px !important;
    line-height: 1.30 !important;
    border-radius: 8px !important;
}}

div[data-testid="stButton"]:not(.st-key-top_nav_bar *):not(.st-key-gcp_chat_header_sticky *):not(.st-key-gcp_suggested_questions_wrap *):not(.st-key-top_app_header_bar *) button * {{
    font-size: 0.88rem !important;
    line-height: 1.30 !important;
}}

/* ── Fixed Top Header Bar (Unified horizontal space: Burger room, Title, Controls) ── */
.st-key-top_app_header_bar,
div[data-testid="stContainer"].st-key-top_app_header_bar {{
    position: fixed !important;
    top: 0 !important;
    left: {"0" if show_chat else "320px"} !important;
    right: {"440px" if show_chat else "0px"} !important;
    width: {"auto" if show_chat else "calc(100% - 320px)"} !important;
    max-width: none !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    z-index: 99980 !important;
    background-color: {"rgba(18, 16, 19, 0.94)" if dark else "rgba(250, 245, 237, 0.96)"} !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border-bottom: 1px solid {border} !important;
    padding: 0 16px 0 16px !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    transition: left 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                right 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                width 0.32s cubic-bezier(0.4, 0, 0.2, 1) !important;
    will-change: left, right, width;
}}

.st-key-top_app_header_bar > div,
.st-key-top_app_header_bar [data-testid="stHorizontalBlock"] {{
    width: 100% !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin: 0 !important;
    padding: 0 !important;
    position: static !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"] {{
    display: flex !important;
    align-items: center !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    padding: 0 !important;
    margin: 0 !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(1) {{
    justify-content: flex-start !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(2) {{
    justify-content: center !important;
    position: static !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(2) [data-testid="stElementContainer"],
.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(2) [data-testid="stMarkdown"] {{
    position: static !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(3) {{
    justify-content: flex-end !important;
    margin-left: auto !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(3) [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
    gap: 8px !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}}

.st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(3) [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    margin: 0 !important;
    padding: 0 !important;
}}

/* All containers in utility column stretch to 86px and center their buttons vertically */
.st-key-top_app_header_bar [data-testid="stElementContainer"],
.st-key-top_app_header_bar div[data-testid="stButton"],
.st-key-font_dec_btn,
.st-key-font_inc_btn,
.st-key-top_theme_toggle_btn {{
    height: 86px !important;
    min-height: 86px !important;
    max-height: 86px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
}}

/* ── Proportional Top Right Utility Controls (Font Size A- / A+ & Theme Toggle) ── */
/* Vertical Middle Justify & Remove Boxes */
.st-key-font_dec_btn button,
.st-key-font_inc_btn button,
.st-key-top_theme_toggle_btn button,
.st-key-top_theme_toggle_btn button[kind="secondary"],
div[data-testid="stButton"].st-key-top_theme_toggle_btn button {{
    width: 44px !important;
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    min-width: 44px !important;
    max-width: 44px !important;
    padding: 0 !important;
    border-radius: 9px !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    color: {subtext} !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    align-self: center !important;
    transition: all 0.15s ease !important;
    box-sizing: border-box !important;
    margin: 0 auto !important;
    box-shadow: none !important;
    outline: none !important;
    cursor: pointer !important;
}}

.st-key-font_dec_btn button *,
.st-key-font_inc_btn button * {{
    font-size: 19px !important;
    line-height: 1 !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    margin: 0 !important;
    padding: 0 !important;
    color: {subtext} !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.st-key-font_dec_btn button:hover,
.st-key-font_inc_btn button:hover,
.st-key-top_theme_toggle_btn button:hover,
.st-key-top_theme_toggle_btn button[kind="secondary"]:hover,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button:hover {{
    background: {hover_bg} !important;
    background-color: {hover_bg} !important;
    color: {text} !important;
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}}

.st-key-font_dec_btn button:focus,
.st-key-font_dec_btn button:active,
.st-key-font_inc_btn button:focus,
.st-key-font_inc_btn button:active,
.st-key-top_theme_toggle_btn button:focus,
.st-key-top_theme_toggle_btn button:active,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button:focus,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button:active {{
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}}

.st-key-font_dec_btn button:hover *,
.st-key-font_inc_btn button:hover * {{
    color: {text} !important;
}}

/* Theme toggle icon: Moon / Sun */
.st-key-top_theme_toggle_btn button::after,
.st-key-top_theme_toggle_btn button[kind="secondary"]::after,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button::after {{
    content: "" !important;
    display: block !important;
    width: 26px !important;
    height: 26px !important;
    background-image: url("{toggle_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    pointer-events: none !important;
    transition: transform 0.15s ease !important;
    margin: 0 auto !important;
}}

.st-key-top_theme_toggle_btn button:hover::after,
.st-key-top_theme_toggle_btn button[kind="secondary"]:hover::after,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button:hover::after {{
    background-image: url("{toggle_svg_hover}") !important;
    transform: scale(1.08) !important;
}}

.st-key-top_theme_toggle_btn button > div,
.st-key-top_theme_toggle_btn button p,
.st-key-top_theme_toggle_btn button span {{
    display: none !important;
}}

/* ── Dollar Green Currency Styling ── */
.dollar-sign, .cur-sym {{
    color: {dollar_green} !important;
    font-weight: 600 !important;
    display: inline !important;
}}

/* ── Sidebar nav items ────────────────────────────── */
.nav-section-label {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: {subtext} !important;
    padding: 0 4px !important;
    margin: 18px 0 8px 0 !important;
}}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] small {{
    padding-left: 2px !important;
}}
.nav-item {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 8px 12px;
    border-radius: 7px;
    font-size: 0.94rem;
    font-weight: 400;
    color: {nav_txt};
    cursor: pointer;
    transition: all 0.12s;
    margin-bottom: 2px;
    text-decoration: none;
    border: none;
    background: transparent;
    width: 100%;
    text-align: left;
}}
.nav-item:hover {{
    background: {hover_bg};
    color: {nav_acttxt};
}}
.nav-item.active {{
    background: {nav_actbg};
    color: {nav_acttxt};
    font-weight: 500;
}}
.nav-item .nav-icon {{
    width: 16px;
    text-align: center;
    opacity: 0.7;
    font-size: 0.90rem;
}}
.nav-item.active .nav-icon {{ opacity: 1; }}

/* ── Filter checkboxes — clean & intuitive ────────────────── */
[data-testid="stSidebar"] [data-testid="stCheckbox"] {{
    margin-bottom: 2px !important;
    padding: 3px 6px !important;
    border-radius: 6px !important;
    transition: background 0.12s ease !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"]:hover {{
    background: {hover_bg} !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"] label {{
    font-size: 0.90rem !important;
    cursor: pointer !important;
}}

/* Checked state: subtle tinted box with vibrant green tick scaled slightly larger than the box */
[data-testid="stSidebar"] [data-testid="stCheckbox"] input[type="checkbox"]:checked + div {{
    background-color: {"rgba(16, 185, 129, 0.16)" if dark else "rgba(16, 185, 129, 0.12)"} !important;
    border: 1.5px solid #10B981 !important;
    border-radius: 4px !important;
    overflow: visible !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"] input[type="checkbox"]:checked + div svg {{
    color: #10B981 !important;
    stroke: #10B981 !important;
    fill: #10B981 !important;
    stroke-width: 2.5px !important;
    display: block !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: scale(1.35) !important;
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.25)) !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[type="checkbox"]:checked) label p {{
    color: {text} !important;
    font-weight: 500 !important;
}}

/* Unchecked state: Clean transparent empty box with clear border */
[data-testid="stSidebar"] [data-testid="stCheckbox"] input[type="checkbox"]:not(:checked) + div {{
    background-color: transparent !important;
    border: 1.5px solid {"rgba(255,255,255,0.30)" if dark else "rgba(0,0,0,0.26)"} !important;
    border-radius: 4px !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"] input[type="checkbox"]:not(:checked) + div svg {{
    display: none !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"] input[type="checkbox"]:not(:checked):hover + div {{
    border-color: {"rgba(255,255,255,0.6)" if dark else "rgba(0,0,0,0.5)"} !important;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[type="checkbox"]:not(:checked)) label p {{
    color: {subtext} !important;
    font-weight: 400 !important;
}}

/* ── Ask the Portfolio Fixed Right Panel (Smooth curtain drawing in and out) ── */
.st-key-ask_portfolio_side_panel,
div[data-testid="stContainer"].st-key-ask_portfolio_side_panel {{
    position: fixed !important;
    top: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 440px !important;
    max-width: 440px !important;
    height: 100vh !important;
    max-height: 100vh !important;
    z-index: 99990 !important;
    background-color: {"#1E1F25" if dark else "#F8FAFC"} !important;
    background: {"#1E1F25" if dark else "#F8FAFC"} !important;
    border-left: 1.5px solid {"rgba(255, 255, 255, 0.12)" if dark else "rgba(0, 0, 0, 0.12)"} !important;
    overflow-y: auto !important;
    padding: 0 20px 36px 20px !important;
    box-sizing: border-box !important;
    transform: {"translateX(0)" if show_chat else "translateX(100%)"} !important;
    box-shadow: {"-8px 0 32px rgba(0, 0, 0, 0.45)" if (show_chat and dark) else ("-8px 0 32px rgba(0, 0, 0, 0.08)" if show_chat else "none")} !important;
    pointer-events: {"auto" if show_chat else "none"} !important;
    transition: transform 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.32s cubic-bezier(0.4, 0, 0.2, 1) !important;
    will-change: transform;
}}

.st-key-ask_portfolio_side_panel > div {{
    width: 100% !important;
    max-width: 100% !important;
}}


/* Unified Full-Width Chat Input Card */
.st-key-ask_portfolio_side_panel [data-testid="stForm"],
.st-key-ask_portfolio_side_panel form[data-testid="stForm"],
.st-key-ask_portfolio_side_panel div[data-testid="stForm"] {{
    position: relative !important;
    background-color: {"#252731" if dark else "#FDFBF7"} !important;
    background: {"#252731" if dark else "#FDFBF7"} !important;
    border: 1.5px solid {"rgba(255,255,255,0.18)" if dark else "rgba(0,0,0,0.18)"} !important;
    border-radius: 14px !important;
    padding: 10px 12px 10px 12px !important;
    box-sizing: border-box !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
    width: 100% !important;
    margin-bottom: 8px !important;
    min-height: 56px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"]:focus-within,
.st-key-ask_portfolio_side_panel form[data-testid="stForm"]:focus-within,
.st-key-ask_portfolio_side_panel div[data-testid="stForm"]:focus-within {{
    border-color: {"#818CF8" if dark else "#6366F1"} !important;
    box-shadow: 0 0 0 2.5px {"rgba(99,102,241,0.25)" if dark else "rgba(99,102,241,0.18)"} !important;
}}

/* Textarea occupies 100% full width of the card */
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div[data-testid="stTextArea"],
.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stElementContainer"]:has(textarea) {{
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    border: none !important;
    background: transparent !important;
}}

/* Remove inner box inside chat window (stTextAreaRootElement & base-input), keeping only the outer card */
.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stTextAreaRootElement"],
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div[data-testid="stTextAreaRootElement"],
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div[data-baseweb="textarea"],
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div[data-baseweb="base-input"],
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div[data-testid="stTextArea"] > div {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
    width: 100% !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stTextAreaRootElement"]:focus-within,
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div[data-testid="stTextAreaRootElement"]:focus-within {{
    border: none !important;
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] textarea {{
    color: {text} !important;
    font-size: 0.94rem !important;
    line-height: 1.45 !important;
    font-family: inherit !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    resize: none !important;
    padding: 2px 44px 4px 2px !important;
    box-sizing: border-box !important;
    width: 100% !important;
    min-height: 42px !important;
    overflow-y: auto !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] textarea::placeholder {{
    color: {subtext} !important;
    opacity: 0.70 !important;
    font-size: 0.90rem !important;
}}

/* Neutralize submit button wrapper so position: absolute anchors to the outer card */
.st-key-ask_portfolio_side_panel [data-testid="stForm"] > div[data-testid="stElementContainer"]:last-child,
.st-key-ask_portfolio_side_panel [data-testid="stForm"] > div[data-testid="stElementContainer"]:nth-child(2),
.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stElementContainer"]:has([data-testid="stFormSubmitButton"]),
.st-key-ask_portfolio_side_panel [data-testid="stForm"] div:has(> [data-testid="stFormSubmitButton"]) {{
    position: static !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
}}

/* Send Button: Anchored at bottom-right inside the purple chat card */
.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stFormSubmitButton"] {{
    position: absolute !important;
    right: 10px !important;
    bottom: 10px !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 20 !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    max-width: 32px !important;
    max-height: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 0.85 !important;
    pointer-events: auto !important;
    transform: scale(1) !important;
    transition: opacity 0.18s cubic-bezier(0.16, 1, 0.3, 1), transform 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}

/* When user enters any text: Send button spawns cleanly at bottom-right */
.st-key-ask_portfolio_side_panel [data-testid="stForm"].has-input [data-testid="stFormSubmitButton"],
.st-key-ask_portfolio_side_panel [data-testid="stForm"]:has(textarea:not(:placeholder-shown)) [data-testid="stFormSubmitButton"] {{
    opacity: 1 !important;
    pointer-events: auto !important;
    transform: scale(1) !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stFormSubmitButton"] button {{
    height: 32px !important;
    min-height: 32px !important;
    max-height: 32px !important;
    width: 32px !important;
    min-width: 32px !important;
    max-width: 32px !important;
    padding: 0 !important;
    border-radius: 8px !important;
    background-color: {"#6366F1" if dark else "#1E1F25"} !important;
    background: {"#6366F1" if dark else "#1E1F25"} !important;
    border: none !important;
    color: #FFFFFF !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.90rem !important;
    cursor: pointer !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    transition: all 0.15s ease !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stFormSubmitButton"] button:hover {{
    background-color: {"#4F46E5" if dark else "#000000"} !important;
    background: {"#4F46E5" if dark else "#000000"} !important;
    transform: scale(1.08) !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stFormSubmitButton"] button:active {{
    transform: scale(0.92) !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stFormSubmitButton"] button p,
.st-key-ask_portfolio_side_panel [data-testid="stForm"] [data-testid="stFormSubmitButton"] button span {{
    color: #FFFFFF !important;
    font-size: 0.90rem !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

/* Sticky Header for Ask the Portfolio Drawer (remains locked at top when chat is scrolled) */
.st-key-ask_portfolio_side_panel [data-testid="stElementContainer"]:has(.st-key-gcp_chat_header_sticky),
.st-key-ask_portfolio_side_panel div:has(> .st-key-gcp_chat_header_sticky),
.st-key-gcp_chat_header_sticky,
div[data-testid="stContainer"].st-key-gcp_chat_header_sticky {{
    position: sticky !important;
    top: 0 !important;
    z-index: 99999 !important;
    background-color: {"#1E1F25" if dark else "#F8FAFC"} !important;
    background: {"#1E1F25" if dark else "#F8FAFC"} !important;
}}

.st-key-ask_portfolio_side_panel [data-testid="stElementContainer"]:has(.st-key-gcp_chat_header_sticky) {{
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    box-shadow: none !important;
}}

.st-key-gcp_chat_header_sticky,
div[data-testid="stContainer"].st-key-gcp_chat_header_sticky {{
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    padding-top: 18px !important;
    padding-bottom: 12px !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    box-sizing: border-box !important;
    border-bottom: 1px solid {"rgba(255,255,255,0.08)" if dark else "rgba(0,0,0,0.06)"} !important;
    box-shadow: none !important;
}}
.st-key-gcp_chat_header_sticky hr {{
    display: none !important;
}}

/* Horizontal block inside header: Strictly Horizontal Single Row, Vertically Centered */
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"],
div[data-testid="stContainer"].st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
    min-height: 40px !important;
    height: 40px !important;
    max-height: 40px !important;
    gap: 6px !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}}

/* Ensure all nested column blocks align flex items on the exact same vertical center */
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] [data-testid="stVerticalBlockBorderWrapper"],
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"],
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] [data-testid="stElementContainer"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    margin: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
}}

/* Column 1: Title Column - Full flex space, Left-aligned, Vertically Centered */
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) {{
    flex: 1 1 auto !important;
    min-width: 0 !important;
    max-width: none !important;
    width: auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}}

.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) [data-testid="stVerticalBlockBorderWrapper"],
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) [data-testid="stVerticalBlock"],
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) [data-testid="stElementContainer"],
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) [data-testid="stMarkdownContainer"] {{
    width: 100% !important;
    max-width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
}}

.st-key-gcp_chat_header_sticky [data-testid="stMarkdownContainer"] p {{
    margin: 0 !important;
    padding: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    line-height: 1 !important;
    height: 40px !important;
}}

.gcp-assist-header-left {{
    display: inline-flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}}

.gcp-assist-title {{
    font-size: 1.32rem !important;
    font-weight: 700 !important;
    color: {"#FFFFFF" if dark else "#0F172A"} !important;
    letter-spacing: -0.015em !important;
    line-height: 1 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: inline-flex !important;
    align-items: center !important;
    text-align: left !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 40px !important;
}}

/* Action Buttons (?, +, ✕) Placed Horizontally Side by Side */
.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:not(:first-child) {{
    flex: 0 0 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    width: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    margin: 0 !important;
    padding: 0 !important;
}}

/* Action button containers (+ and ✕): Enlarge icons, Completely Remove Square Boundaries */
.st-key-gcp_chat_header_sticky div[data-testid="stButton"],
.st-key-gcp_btn_new_chat,
.st-key-gcp_btn_close_panel,
div.st-key-gcp_btn_new_chat,
div.st-key-gcp_btn_close_panel,
.st-key-welcome_gov_spec_btn,
div.st-key-welcome_gov_spec_btn {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto !important;
    padding: 0 !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    min-height: 36px !important;
    max-height: 36px !important;
}}

.st-key-gcp_chat_header_sticky button,
.st-key-gcp_chat_header_sticky div[data-testid="stButton"] button,
.st-key-gcp_chat_header_sticky button[kind="secondary"],
.st-key-gcp_btn_new_chat button,
.st-key-gcp_btn_close_panel button,
div.st-key-gcp_btn_new_chat button,
div.st-key-gcp_btn_close_panel button,
.st-key-welcome_gov_spec_btn button,
div.st-key-welcome_gov_spec_btn button {{
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    min-height: 36px !important;
    max-height: 36px !important;
    padding: 0 !important;
    margin: 0 auto !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    border-width: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    cursor: pointer !important;
    position: relative !important;
    transition: all 0.15s ease !important;
}}

.st-key-gcp_chat_header_sticky button:hover,
.st-key-gcp_chat_header_sticky div[data-testid="stButton"] button:hover,
.st-key-gcp_btn_new_chat button:hover,
.st-key-gcp_btn_close_panel button:hover,
div.st-key-gcp_btn_new_chat button:hover,
div.st-key-gcp_btn_close_panel button:hover,
.st-key-welcome_gov_spec_btn button:hover,
div.st-key-welcome_gov_spec_btn button:hover {{
    background: {hover_bg} !important;
    background-color: {hover_bg} !important;
    border: none !important;
    border-color: transparent !important;
    border-width: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    transform: scale(1.10) !important;
}}

.st-key-gcp_chat_header_sticky button:focus,
.st-key-gcp_chat_header_sticky button:active,
.st-key-gcp_btn_new_chat button:focus,
.st-key-gcp_btn_close_panel button:focus,
.st-key-gcp_btn_new_chat button:active,
.st-key-gcp_btn_close_panel button:active,
.st-key-welcome_gov_spec_btn button:focus,
.st-key-welcome_gov_spec_btn button:active {{
    border: none !important;
    border-color: transparent !important;
    border-width: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    background: {hover_bg} !important;
    background-color: {hover_bg} !important;
}}

.st-key-gcp_chat_header_sticky button > div,
.st-key-gcp_chat_header_sticky button p,
.st-key-gcp_btn_new_chat button > div,
.st-key-gcp_btn_new_chat button p,
.st-key-gcp_btn_close_panel button > div,
.st-key-gcp_btn_close_panel button p,
.st-key-welcome_gov_spec_btn button > div,
.st-key-welcome_gov_spec_btn button p {{
    display: none !important;
    visibility: hidden !important;
}}

/* Enlarged + icon (20px) */
.st-key-gcp_btn_new_chat button::after,
div.st-key-gcp_btn_new_chat button::after {{
    content: "" !important;
    display: block !important;
    width: 20px !important;
    height: 20px !important;
    background-image: url("{plus_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    pointer-events: none !important;
    margin: auto !important;
    transition: transform 0.15s ease !important;
}}
.st-key-gcp_btn_new_chat button:hover::after,
div.st-key-gcp_btn_new_chat button:hover::after {{
    background-image: url("{plus_svg_hover}") !important;
    transform: scale(1.08) !important;
}}

/* Enlarged ✕ icon (19px) */
.st-key-gcp_btn_close_panel button::after,
div.st-key-gcp_btn_close_panel button::after {{
    content: "" !important;
    display: block !important;
    width: 19px !important;
    height: 19px !important;
    background-image: url("{panel_close_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    pointer-events: none !important;
    margin: auto !important;
    transition: transform 0.15s ease !important;
}}
.st-key-gcp_btn_close_panel button:hover::after,
div.st-key-gcp_btn_close_panel button:hover::after {{
    background-image: url("{panel_close_hover_svg}") !important;
    transform: scale(1.08) !important;
}}

/* Welcome screen Governance Specification ? icon (19px) */
.st-key-welcome_gov_spec_btn button::after,
div.st-key-welcome_gov_spec_btn button::after {{
    content: "" !important;
    display: block !important;
    width: 19px !important;
    height: 19px !important;
    background-image: url("{info_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    pointer-events: none !important;
    margin: auto !important;
    transition: transform 0.15s ease !important;
}}
.st-key-welcome_gov_spec_btn button:hover::after,
div.st-key-welcome_gov_spec_btn button:hover::after {{
    background-image: url("{info_hover_svg}") !important;
    transform: scale(1.08) !important;
}}

/* ── Governance View Sticky Header & Action Buttons in Side Drawer ── */
.st-key-gcp_gov_header_sticky,
div[data-testid="stContainer"].st-key-gcp_gov_header_sticky {{
    position: sticky !important;
    top: 0 !important;
    z-index: 99995 !important;
    background-color: {"#1E1F25" if dark else "#F8FAFC"} !important;
    background: {"#1E1F25" if dark else "#F8FAFC"} !important;
    padding-top: 16px !important;
    padding-bottom: 12px !important;
    margin: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
    border-bottom: 1px solid {"rgba(255, 255, 255, 0.08)" if dark else "rgba(0, 0, 0, 0.08)"} !important;
}}

.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
    min-height: 40px !important;
    gap: 6px !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}}

.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) {{
    flex: 0 0 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    width: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) {{
    flex: 1 1 auto !important;
    min-width: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) {{
    flex: 0 0 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    width: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.gcp-gov-header-title {{
    font-size: 0.90rem !important;
    font-weight: 700 !important;
    color: {"#FFFFFF" if dark else "#0F172A"} !important;
    letter-spacing: -0.01em !important;
    line-height: 1.25 !important;
    display: flex !important;
    align-items: center !important;
    text-align: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 4px !important;
    white-space: normal !important;
    word-break: normal !important;
    overflow: visible !important;
}}

.st-key-gcp_btn_gov_back button,
.st-key-gcp_btn_gov_close button,
div.st-key-gcp_btn_gov_back button,
div.st-key-gcp_btn_gov_close button {{
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    max-width: 34px !important;
    min-height: 34px !important;
    max-height: 34px !important;
    padding: 0 !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
    background: {"rgba(255, 255, 255, 0.06)" if dark else "rgba(0, 0, 0, 0.04)"} !important;
    background-color: {"rgba(255, 255, 255, 0.06)" if dark else "rgba(0, 0, 0, 0.04)"} !important;
    border: 1px solid {"rgba(255, 255, 255, 0.14)" if dark else "rgba(0, 0, 0, 0.12)"} !important;
    box-shadow: none !important;
    outline: none !important;
    cursor: pointer !important;
    color: {text} !important;
    transition: all 0.15s ease !important;
}}

.st-key-gcp_btn_gov_back button:hover,
.st-key-gcp_btn_gov_close button:hover,
div.st-key-gcp_btn_gov_back button:hover,
div.st-key-gcp_btn_gov_close button:hover {{
    background: {"rgba(255, 255, 255, 0.14)" if dark else "rgba(0, 0, 0, 0.08)"} !important;
    border-color: {"rgba(255, 255, 255, 0.30)" if dark else "rgba(0, 0, 0, 0.22)"} !important;
    color: {text} !important;
    transform: scale(1.08) !important;
}}

.st-key-gcp_btn_gov_back button p,
.st-key-gcp_btn_gov_back button span,
.st-key-gcp_btn_gov_close button p,
.st-key-gcp_btn_gov_close button span {{
    display: flex !important;
    visibility: visible !important;
    align-items: center !important;
    justify-content: center !important;
    color: {text} !important;
    font-size: 1.12rem !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
}}
.gcp-welcome-title {{
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    line-height: 1.20 !important;
    color: {text} !important;
    letter-spacing: -0.02em !important;
    margin-top: 6px !important;
    margin-bottom: 6px !important;
}}
.gcp-welcome-subtitle {{
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    line-height: 1.30 !important;
    color: {text} !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 12px !important;
}}
.gcp-welcome-list {{
    font-size: 0.83rem !important;
    color: {subtext} !important;
    line-height: 1.48 !important;
    margin: 0 0 14px 18px !important;
    padding: 0 !important;
}}
.gcp-welcome-list li {{
    margin-bottom: 4px !important;
}}

/* Welcome Screen Container (Flows naturally from top, zero dead empty space) */
.st-key-gcp_welcome_body_container,
div[data-testid="stContainer"].st-key-gcp_welcome_body_container {{
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
    box-sizing: border-box !important;
    padding-top: 14px !important;
    padding-bottom: 16px !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}}

.st-key-gcp_welcome_body_container > div {{
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}}
.gcp-accuracy-note {{
    display: flex !important;
    align-items: flex-start !important;
    gap: 6px !important;
    font-size: 0.74rem !important;
    line-height: 1.35 !important;
    color: {"#FCA5A5" if dark else "#B91C1C"} !important;
    background: {"rgba(239, 68, 68, 0.08)" if dark else "rgba(239, 68, 68, 0.05)"} !important;
    border: 1px solid {"rgba(239, 68, 68, 0.20)" if dark else "rgba(239, 68, 68, 0.15)"} !important;
    border-radius: 6px !important;
    padding: 5px 8px !important;
    margin-bottom: 6px !important;
}}
.gcp-accuracy-icon {{
    font-size: 0.80rem !important;
    line-height: 1.1 !important;
    flex-shrink: 0 !important;
}}

/* Tight, Compact Suggested Questions (zero-scroll default state) */
.st-key-gcp_suggested_questions_wrap,
div[data-testid="stContainer"].st-key-gcp_suggested_questions_wrap {{
    display: flex !important;
    flex-direction: column !important;
    gap: 5px !important;
    margin-top: 4px !important;
    margin-bottom: 6px !important;
    border: none !important;
    padding: 0 !important;
}}
.st-key-gcp_suggested_questions_wrap div[data-testid="stElementContainer"] {{
    margin: 0 !important;
    padding: 0 !important;
}}
.st-key-gcp_suggested_questions_wrap div[data-testid="stButton"] {{
    margin: 0 !important;
    padding: 0 !important;
}}
.st-key-gcp_suggested_questions_wrap div[data-testid="stButton"] button {{
    border-radius: 8px !important;
    background: {"#252731" if dark else "#FDFBF7"} !important;
    border: 1px solid {"rgba(255,255,255,0.11)" if dark else "rgba(0,0,0,0.11)"} !important;
    color: {text} !important;
    font-size: 0.80rem !important;
    font-weight: 500 !important;
    line-height: 1.30 !important;
    padding: 6px 10px !important;
    min-height: 32px !important;
    height: auto !important;
    text-align: left !important;
    justify-content: flex-start !important;
    display: flex !important;
    align-items: center !important;
    box-shadow: none !important;
    margin: 0 !important;
    transition: all 0.15s ease !important;
}}
.st-key-gcp_suggested_questions_wrap div[data-testid="stButton"] button * {{
    font-size: 0.80rem !important;
    line-height: 1.30 !important;
}}
.st-key-gcp_suggested_questions_wrap div[data-testid="stButton"] button:hover {{
    background: {"#303440" if dark else "#F1EDE5"} !important;
    border-color: {"rgba(129, 140, 248, 0.45)" if dark else "rgba(79, 70, 229, 0.35)"} !important;
    color: {"#FFFFFF" if dark else "#0F172A"} !important;
    transform: translateY(-1px) !important;
}}

.gcp-disclaimer {{
    font-size: 0.74rem !important;
    color: {subtext} !important;
    opacity: 0.75 !important;
    text-align: center !important;
    margin-top: 6px !important;
    line-height: 1.35 !important;
}}

.gcp-disclaimer-top {{
    font-size: 0.80rem !important;
    color: {subtext} !important;
    opacity: 0.85 !important;
    text-align: center !important;
    margin: 14px 0 16px 0 !important;
    line-height: 1.45 !important;
}}

.gcp-user-bubble-row {{
    display: flex !important;
    justify-content: flex-end !important;
    width: 100% !important;
    margin: 6px 0 14px 0 !important;
}}

.gcp-user-bubble {{
    background: {"#3B4252" if dark else "#E2E8F0"} !important;
    color: {"#FFFFFF" if dark else "#0F172A"} !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 10px 20px !important;
    max-width: 85% !important;
    font-size: 1.02rem !important;
    font-weight: 500 !important;
    line-height: 1.48 !important;
    word-break: break-word !important;
    box-shadow: {"0 2px 8px rgba(0,0,0,0.25)" if dark else "0 1px 4px rgba(0,0,0,0.06)"} !important;
}}

.gcp-assistant-bubble {{
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    margin-bottom: 16px !important;
    width: 100% !important;
}}

.gcp-status-line {{
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    font-size: 0.94rem !important;
    font-weight: 500 !important;
    color: {"#94A3B8" if dark else "#64748B"} !important;
    margin-bottom: 2px !important;
}}

.gcp-sparkle-small {{
    font-size: 1.15rem !important;
    line-height: 1 !important;
    background: linear-gradient(135deg, #60A5FA 0%, #A855F7 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}}

.gcp-answer-body,
.st-key-gcp_streaming_answer_wrap,
div[data-testid="stContainer"].st-key-gcp_streaming_answer_wrap {{
    background: {"#252731" if dark else "#FFFFFF"} !important;
    border: 1px solid {"rgba(255,255,255,0.09)" if dark else "rgba(0,0,0,0.08)"} !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    font-size: 1.02rem !important;
    line-height: 1.60 !important;
    color: {text} !important;
    word-break: break-word !important;
    box-shadow: {"0 2px 8px rgba(0,0,0,0.18)" if dark else "0 2px 8px rgba(0,0,0,0.04)"} !important;
}}

.st-key-gcp_streaming_answer_wrap p,
.st-key-gcp_streaming_answer_wrap span,
.st-key-gcp_streaming_answer_wrap div,
.st-key-gcp_streaming_answer_wrap li {{
    font-size: 1.02rem !important;
    line-height: 1.60 !important;
    color: {text} !important;
}}

.st-key-gcp_streaming_answer_wrap strong,
.st-key-gcp_streaming_answer_wrap b {{
    font-weight: 600 !important;
    color: {"#FFFFFF" if dark else "#0F172A"} !important;
}}

.st-key-gcp_streaming_answer_wrap ul,
.st-key-gcp_streaming_answer_wrap ol {{
    margin: 8px 0 !important;
    padding-left: 20px !important;
}}

/* ── GCP Assistant Provenance Architecture ── */
.gcp-provenance-box {{
    margin-top: 10px !important;
    padding: 10px 12px !important;
    background: {"rgba(255, 255, 255, 0.03)" if dark else "#F8FAFC"} !important;
    border: 1px solid {"rgba(255, 255, 255, 0.08)" if dark else "#E2E8F0"} !important;
    border-radius: 8px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}}
.gcp-prov-chips-row {{
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
}}
.gcp-prov-chip {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    font-size: 0.80rem !important;
    padding: 4px 10px !important;
    background: {"rgba(255, 255, 255, 0.05)" if dark else "#FFFFFF"} !important;
    border: 1px solid {"rgba(255, 255, 255, 0.08)" if dark else "#E2E8F0"} !important;
    border-radius: 6px !important;
    box-shadow: {"0 1px 2px rgba(0,0,0,0.12)" if dark else "0 1px 2px rgba(0,0,0,0.03)"} !important;
}}
.prov-icon {{
    font-size: 0.85rem !important;
    line-height: 1 !important;
}}
.prov-key {{
    color: {subtext} !important;
    font-weight: 500 !important;
    font-size: 0.76rem !important;
}}
.prov-val {{
    color: {text} !important;
    font-weight: 600 !important;
    font-family: 'JetBrains Mono', 'SF Mono', monospace !important;
    font-size: 0.78rem !important;
}}
.gcp-prov-derived-row {{
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    align-items: center !important;
    padding-top: 6px !important;
    border-top: 1px dashed {"rgba(255, 255, 255, 0.08)" if dark else "#E2E8F0"} !important;
}}
.prov-derived-lbl {{
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-weight: 600 !important;
    color: {subtext} !important;
    margin-right: 2px !important;
}}
.prov-table-tag {{
    display: inline-flex !important;
    align-items: center !important;
    font-size: 0.74rem !important;
    font-family: 'JetBrains Mono', 'SF Mono', monospace !important;
    font-weight: 500 !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    background: {"rgba(99, 102, 241, 0.14)" if dark else "rgba(79, 70, 229, 0.08)"} !important;
    color: {"#A5B4FC" if dark else "#4F46E5"} !important;
    border: 1px solid {"rgba(99, 102, 241, 0.28)" if dark else "rgba(79, 70, 229, 0.20)"} !important;
}}
.gcp-provenance-bar {{
    font-size: 0.82rem !important;
    color: {subtext} !important;
    opacity: 0.85 !important;
    margin-top: 4px !important;
    padding-left: 2px !important;
}}
.gcp-provenance-bar b {{
    color: {text} !important;
    font-weight: 600 !important;
}}

/* ── Executive Chat Architecture ────────────────── */
.chat-query-row {{
    display: flex !important;
    justify-content: flex-end !important;
    width: 100% !important;
    margin-top: 18px !important;
    margin-bottom: 12px !important;
}}
@keyframes chatCardFadeIn {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.chat-query-box {{
    background: {"#2A2632" if dark else "#222026"} !important;
    border: 1px solid {"rgba(255,255,255,0.14)" if dark else "rgba(0,0,0,0.18)"} !important;
    border-radius: 14px 14px 3px 14px !important;
    padding: 12px 18px !important;
    max-width: 92% !important;
    min-width: 200px !important;
    box-shadow: {"0 3px 12px rgba(0,0,0,0.35)" if dark else "0 3px 12px rgba(0,0,0,0.12)"} !important;
    display: flex !important;
    flex-direction: column !important;
    animation: chatCardFadeIn 0.16s ease-out !important;
}}
.chat-query-header {{
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 16px !important;
    margin-bottom: 6px !important;
    padding-bottom: 4px !important;
    border-bottom: 1px solid {"rgba(255,255,255,0.10)" if dark else "rgba(255,255,255,0.12)"} !important;
}}
.chat-query-role {{
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: {"#C4B5FD" if dark else "#E2DDD5"} !important;
    text-transform: uppercase !important;
}}
.chat-query-ts {{
    font-size: 0.76rem !important;
    color: {"#A1A1AA" if dark else "#A8A29E"} !important;
}}
.chat-query-text {{
    font-size: 0.98rem !important;
    font-weight: 500 !important;
    color: #FFFFFF !important;
    line-height: 1.5 !important;
    word-break: break-word !important;
}}

.chat-resp-box {{
    background: {card_bg};
    border: 1px solid {card_brd};
    border-radius: 12px;
    padding: 14px 18px;
    margin: 6px 0 16px 0;
    max-width: 100% !important;
    box-shadow: {"0 2px 10px rgba(0,0,0,0.20)" if dark else "0 2px 10px rgba(0,0,0,0.03)"};
    word-break: break-word;
    overflow-wrap: break-word;
    animation: chatCardFadeIn 0.20s ease-out !important;
}}
.chat-resp-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}}
.chat-resp-title {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: {subtext};
    text-transform: uppercase;
}}
.chat-badge {{
    font-size: 0.78rem;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 4px;
}}
.badge-fallback {{
    background: {"rgba(245, 158, 11, 0.12)" if dark else "#FEF3C7"};
    color: {"#FBBF24" if dark else "#92400E"};
    border: 1px solid {"rgba(245, 158, 11, 0.25)" if dark else "#FDE68A"};
}}
.badge-gemini {{
    background: {"rgba(59, 130, 246, 0.12)" if dark else "#EFF6FF"};
    color: {"#60A5FA" if dark else "#1D4ED8"};
    border: 1px solid {"rgba(59, 130, 246, 0.25)" if dark else "#BFDBFE"};
}}
.badge-openai {{
    background: {"rgba(16, 185, 129, 0.12)" if dark else "#ECFDF5"};
    color: {"#34D399" if dark else "#047857"};
    border: 1px solid {"rgba(16, 185, 129, 0.25)" if dark else "#A7F3D0"};
}}
.badge-offline {{
    background: {"rgba(255,255,255,0.06)" if dark else "#F3F4F6"};
    color: {subtext};
    border: 1px solid {"rgba(255,255,255,0.1)" if dark else "#E5E7EB"};
}}

.chat-resp-content {{
    font-size: 0.96rem;
    line-height: 1.6;
    color: {text};
    margin-bottom: 12px;
    word-break: break-word;
    overflow-wrap: break-word;
}}
.chat-resp-content p {{
    margin: 0 0 8px 0;
    color: {text};
}}
.chat-resp-content p:last-child {{
    margin-bottom: 0;
}}
.chat-resp-content strong, .chat-resp-content b {{
    color: {text};
    font-weight: 600;
}}
.chat-resp-content ul, .chat-resp-content ol {{
    margin: 4px 0 8px 20px;
    padding: 0;
}}
.chat-resp-content li {{
    margin-bottom: 4px;
}}

.chat-provenance-bar {{
    border-top: 1px dashed {"rgba(255,255,255,0.09)" if dark else "rgba(0,0,0,0.09)"};
    padding-top: 10px;
    font-size: 0.80rem;
    color: {subtext};
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
}}
.chat-provenance-bar b {{
    color: {text};
    font-weight: 500;
}}
.meta-sep {{
    color: {subtext};
    opacity: 0.4;
}}

/* ── Divider ──────────────────────────────────────── */
hr, .stDivider {{
    border-color: {divider} !important;
}}

/* ── KPI cards ────────────────────────────────────── */
[data-testid="stHorizontalBlock"]:has(.kpi-card) {{
    display: flex !important;
    align-items: stretch !important;
    gap: {"8px" if show_chat else "12px"} !important;
}}

[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] {{
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    min-width: 0 !important;
    flex: 1 1 0 !important;
}}

[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] > div[data-testid="stElementContainer"] {{
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 auto !important;
    height: 100% !important;
    min-width: 0 !important;
}}

[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] div[data-testid="stMarkdown"],
[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] div[data-testid="stMarkdownContainer"] {{
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 auto !important;
    height: 100% !important;
    width: 100% !important;
    min-width: 0 !important;
}}

.kpi-card {{
    background: {kpi_bg};
    border: 1px solid {kpi_brd};
    border-radius: 8px;
    padding: {"10px 10px" if show_chat else "12px 14px"};
    box-sizing: border-box !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    min-height: {"92px" if show_chat else "98px"} !important;
    overflow: hidden !important;
}}
.kpi-label {{
    font-size: {"0.70rem" if show_chat else "0.75rem"} !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: {"0.025em" if show_chat else "0.05em"} !important;
    color: {subtext} !important;
    margin-bottom: 4px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.25 !important;
}}
.kpi-value {{
    font-size: {"1.48rem" if show_chat else "1.64rem"} !important;
    font-weight: 600 !important;
    color: {text} !important;
    line-height: 1.18 !important;
    letter-spacing: -0.02em !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}}
.kpi-sub {{
    font-size: {"0.76rem" if show_chat else "0.80rem"} !important;
    color: {subtext} !important;
    margin-top: 3px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.25 !important;
}}

/* ── Page Header & Clear Section Separation ────────────────────── */
.page-header-wrap {{
    margin-top: 2px !important;
    margin-bottom: 24px !important;
    padding-bottom: 16px !important;
    border-bottom: 1px solid {"rgba(255,255,255,0.08)" if dark else "rgba(0,0,0,0.08)"} !important;
}}

.page-title {{
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: {text} !important;
    margin: 0 0 8px 0 !important;
    letter-spacing: -0.015em !important;
    line-height: 1.25 !important;
}}

.page-header-wrap:not(:has(.page-sub)) .page-title {{
    margin-bottom: 0 !important;
}}

.page-sub,
.page-desc {{
    margin: 0 !important;
    line-height: 1.4 !important;
}}

.page-sub-badge {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    font-size: 0.90rem !important;
    font-weight: 500 !important;
    color: {subtext} !important;
    background-color: {"rgba(255,255,255,0.05)" if dark else "rgba(0,0,0,0.04)"} !important;
    border: 1px solid {"rgba(255,255,255,0.09)" if dark else "rgba(0,0,0,0.07)"} !important;
    border-radius: 6px !important;
    padding: 4px 11px !important;
    letter-spacing: 0.01em !important;
}}

/* ── Section labels ───────────────────────────────── */
.section-label {{
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: {subtext} !important;
    margin-top: 2px !important;
    margin-bottom: 14px !important;
    display: block !important;
}}

/* ── Insight cards ────────────────────────────────── */
.insight-card {{
    background: {card_bg};
    border: 1px solid {card_brd};
    border-radius: 8px;
    padding: 20px 22px;
    margin-bottom: 12px;
}}
.insight-no {{
    font-size: 0.76rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {subtext};
    margin-bottom: 8px;
}}
.insight-title {{
    font-size: 1.30rem;
    font-weight: 600;
    color: {text};
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}}
.insight-obs {{
    font-size: 1.05rem;
    color: {subtext};
    line-height: 1.6;
    margin: 0 0 12px 0;
}}
.insight-highlight {{
    display: inline-block;
    font-size: 0.90rem;
    font-weight: 600;
    padding: 3px 10px;
    background: {badge_bg};
    border: 1px solid {badge_brd};
    border-radius: 4px;
    color: {badge_txt};
    margin-bottom: 12px;
    letter-spacing: 0.01em;
}}
.insight-sowhat {{
    background: {hover_bg};
    border-left: 3px solid {insight_accent};
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    font-size: 1.02rem;
    color: {text};
    line-height: 1.55;
}}
.insight-sowhat-label {{
    font-size: 0.84rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {subtext};
    display: block;
    margin-bottom: 4px;
}}

/* ── Anomaly KPI strip ────────────────────────────── */
.anomaly-kpi {{
    background: {kpi_bg};
    border: 1px solid {kpi_brd};
    border-radius: 8px;
    padding: 16px 18px;
    text-align: center;
}}
.anomaly-kpi-label {{
    font-size: 0.90rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {subtext};
    margin-bottom: 6px;
}}
.anomaly-kpi-value {{
    font-size: 1.85rem;
    font-weight: 600;
    color: {text};
    letter-spacing: -0.02em;
}}
.anomaly-kpi-sub {{
    font-size: 0.94rem;
    color: {subtext};
    margin-top: 3px;
}}

/* ── Profile rows ─────────────────────────────────── */
.profile-row {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid {divider};
    font-size: 0.94rem;
}}
.profile-row:last-child {{ border-bottom: none; }}
.profile-key {{ color: {subtext}; font-weight: 400; }}
.profile-val {{ color: {text}; font-weight: 500; }}

/* ── Expander (Filter Heads & Accordions) ────────── */
[data-testid="stExpander"],
[data-testid="stSidebar"] [data-testid="stExpander"] {{
    background: {panel} !important;
    background-color: {panel} !important;
    border: 1px solid {border} !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    margin-bottom: 10px !important;
}}
[data-testid="stExpander"] details,
[data-testid="stSidebar"] [data-testid="stExpander"] details {{
    background: {panel} !important;
    background-color: {panel} !important;
    border: none !important;
}}
[data-testid="stExpander"] summary,
[data-testid="stSidebar"] [data-testid="stExpander"] summary,
[data-testid="stExpander"] details summary,
[data-testid="stSidebar"] [data-testid="stExpander"] details summary {{
    background: {"#201E22" if dark else "#EFEAE0"} !important;
    background-color: {"#201E22" if dark else "#EFEAE0"} !important;
    border-bottom: 1px solid {border} !important;
    color: {text} !important;
    padding: 8px 12px !important;
    border-radius: 7px 7px 0 0 !important;
    cursor: pointer !important;
    transition: background 0.15s ease !important;
}}
[data-testid="stExpander"] details:not([open]) summary,
[data-testid="stSidebar"] [data-testid="stExpander"] details:not([open]) summary {{
    border-bottom: none !important;
    border-radius: 7px !important;
}}
[data-testid="stExpander"] summary:hover,
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover,
[data-testid="stExpander"] details summary:hover,
[data-testid="stSidebar"] [data-testid="stExpander"] details summary:hover {{
    background: {hover_bg} !important;
    background-color: {hover_bg} !important;
}}
[data-testid="stExpander"] summary *,
[data-testid="stSidebar"] [data-testid="stExpander"] summary *,
[data-testid="stExpander"] details summary *,
[data-testid="stSidebar"] [data-testid="stExpander"] details summary * {{
    color: {text} !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
}}
[data-testid="stExpander"] summary svg,
[data-testid="stSidebar"] [data-testid="stExpander"] summary svg,
[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"],
[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {{
    color: {text} !important;
    fill: {text} !important;
    stroke: {text} !important;
}}
[data-testid="stExpanderDetails"],
[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
    background: {panel} !important;
    background-color: {panel} !important;
    padding: 10px 12px !important;
    border: none !important;
}}
[data-testid="stChatMessage"] {{
    background: {card_bg} !important;
    border: 1px solid {card_brd} !important;
    border-radius: 8px !important;
}}

/* Buttons */
button[kind="secondary"] {{
    background-color: {"#1C1A1E" if dark else "#FAF5ED"} !important;
    color: {"#A1A1AA" if dark else "#555555"} !important;
    border: 1px solid {"rgba(255,255,255,0.08)" if dark else "rgba(0,0,0,0.10)"} !important;
    border-radius: 6px !important;
    font-size: 0.90rem !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}}
button[kind="secondary"]:hover {{
    background-color: {hover_bg} !important;
    color: {text} !important;
    border-color: {"rgba(255,255,255,0.20)" if dark else "rgba(0,0,0,0.22)"} !important;
}}
button[kind="primary"] {{
    background: {"#2D2A30" if dark else "#E8E2D8"} !important;
    color: {"#FFFFFF" if dark else "#111111"} !important;
    font-weight: 600 !important;
    border: 1px solid {"rgba(255,255,255,0.18)" if dark else "rgba(0,0,0,0.18)"} !important;
    border-radius: 6px !important;
    font-size: 0.90rem !important;
    box-shadow: {"0 1px 2px rgba(0,0,0,0.2)" if dark else "0 1px 2px rgba(0,0,0,0.06)"} !important;
    transition: all 0.15s ease !important;
}}
button[kind="primary"]:hover {{
    background: {"#38343C" if dark else "#DFD8CD"} !important;
    color: {"#FFFFFF" if dark else "#111111"} !important;
}}

/* Tabs */
div[data-baseweb="tab-list"] {{
    border-bottom: 1px solid {divider} !important;
    gap: 0 !important;
}}
button[role="tab"] {{
    color: {subtext} !important;
    font-size: 0.92rem !important;
    font-weight: 400 !important;
    padding: 10px 16px !important;
    border-radius: 0 !important;
}}
button[role="tab"][aria-selected="true"] {{
    color: {text} !important;
    font-weight: 600 !important;
    border-bottom: 2px solid {text} !important;
}}

/* ── Text inputs, Textareas & Selectboxes (Analyst Notes, Account ID, AI Provider, etc.) ── */
div[data-testid="stSelectbox"],
div[data-testid="stMultiSelect"],
div[data-testid="stTextInput"],
div[data-testid="stTextArea"] {{
    color: {text} !important;
}}

div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] label p,
div[data-testid="stSelectbox"] label span,
div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"],
div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] *,
div[data-testid="stMultiSelect"] label,
div[data-testid="stMultiSelect"] label p,
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] label p,
div[data-testid="stTextArea"] label,
div[data-testid="stTextArea"] label p,
div[data-testid="stTextArea"] label span,
div[data-testid="stTextArea"] [data-testid="stWidgetLabel"],
div[data-testid="stTextArea"] [data-testid="stWidgetLabel"] * {{
    color: {text} !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    margin-bottom: 4px !important;
}}

/* Selectbox, TextInput & TextArea Main Containers (BaseWeb & Streamlit 1.40+ emotion components) */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stSelectbox"] div:has(> input),
div[data-testid="stSelectbox"] div:has(input),
div[data-testid="stSelectbox"] [class*="e1oobldh0"],
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] [role="combobox"],
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"],
div[data-testid="stMultiSelect"] div[data-baseweb="select"],
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
div[data-baseweb="input"],
div[data-baseweb="input"] > div,
div[data-testid="stTextInput"] div:has(> input),
div[data-testid="stTextInput"] div:has(input),
div[data-testid="stTextArea"] > div,
div[data-testid="stTextArea"] div[data-baseweb="textarea"],
div[data-testid="stTextArea"] div[data-baseweb="textarea"] > div,
div[data-testid="stTextArea"] [data-testid="stTextAreaRootElement"],
div[data-baseweb="textarea"],
div[data-baseweb="textarea"] > div,
.st-key-sidebar_ai_provider_select,
.st-key-sidebar_ai_provider_select > div,
.st-key-sidebar_ai_provider_select div:has(input),
.st-key-sidebar_ai_provider_select [class*="e1oobldh0"],
[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div,
[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div > div,
[data-testid="stSidebar"] div[data-testid="stSelectbox"] div:has(input),
[data-testid="stSidebar"] div[data-testid="stSelectbox"] [class*="e1oobldh0"],
[data-testid="stSidebar"] div[data-testid="stTextInput"] div:has(input) {{
    background-color: {inputbg} !important;
    background: {inputbg} !important;
    border: 1px solid {inputbrd} !important;
    border-color: {inputbrd} !important;
    color: {text} !important;
    border-radius: 8px !important;
}}

div[data-testid="stSelectbox"] div:has(input):focus-within,
div[data-testid="stSelectbox"] div[data-focus-within],
div[data-baseweb="input"]:focus-within,
div[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within,
div[data-testid="stTextArea"] [data-testid="stTextAreaRootElement"]:focus-within,
div[data-baseweb="textarea"]:focus-within {{
    border-color: {"#6366F1" if dark else "#4F46E5"} !important;
    box-shadow: 0 0 0 1px {"#6366F1" if dark else "#4F46E5"} !important;
}}

/* Selectbox input field & typography */
div[data-testid="stSelectbox"] input,
div[data-testid="stSelectbox"] input[role="combobox"],
div[data-testid="stSelectbox"] [class*="e1oobldh1"],
div[data-testid="stTextInput"] input,
.st-key-sidebar_ai_provider_select input,
[data-testid="stSidebar"] div[data-testid="stSelectbox"] input,
[data-testid="stSidebar"] div[data-testid="stTextInput"] input {{
    color: {text} !important;
    -webkit-text-fill-color: {text} !important;
    background-color: transparent !important;
    background: transparent !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    line-height: 1.4 !important;
}}

/* Textarea input field & typography */
div[data-testid="stTextArea"] textarea {{
    color: {text} !important;
    -webkit-text-fill-color: {text} !important;
    background-color: transparent !important;
    background: transparent !important;
    font-size: 0.88rem !important;
    line-height: 1.5 !important;
}}

div[data-testid="stTextArea"] textarea::placeholder {{
    color: {subtext} !important;
    opacity: 0.7 !important;
}}

/* Dropdown Arrow Buttons & SVGs */
div[data-testid="stSelectbox"] button,
div[data-testid="stSelectbox"] [class*="e1oobldh2"],
div[data-testid="stSelectbox"] svg,
div[data-baseweb="select"] svg,
div[data-baseweb="input"] svg,
[data-testid="stSidebar"] div[data-testid="stSelectbox"] button,
[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {{
    fill: {subtext} !important;
    color: {subtext} !important;
    background-color: transparent !important;
    background: transparent !important;
}}

/* Virtual Dropdown List (Streamlit 1.40+ stSelectboxVirtualDropdown & BaseWeb popover) */
div[data-testid="stSelectboxVirtualDropdown"],
div[data-testid="stSelectboxVirtualDropdown"] > div,
div[class*="e1oobldh4"],
div[class*="e1oobldh5"],
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
ul[role="listbox"] {{
    background-color: {card_bg} !important;
    background: {card_bg} !important;
    border: 1px solid {border} !important;
    border-radius: 8px !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, {"0.55" if dark else "0.12"}) !important;
    color: {text} !important;
}}

div[data-testid="stSelectboxVirtualDropdown"] [role="option"],
div[data-testid="stSelectboxVirtualDropdown"] li,
div[data-testid="stSelectboxVirtualDropdown"] div[class*="e1oobldh"],
div[data-baseweb="menu"] [role="option"],
ul[role="listbox"] li {{
    color: {text} !important;
    background-color: transparent !important;
    background: transparent !important;
    border-radius: 6px !important;
    font-size: 0.86rem !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
}}

div[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover,
div[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
div[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"],
div[data-testid="stSelectboxVirtualDropdown"] li:hover,
div[data-baseweb="menu"] [role="option"]:hover,
ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {{
    background-color: {"rgba(255, 255, 255, 0.08)" if dark else "rgba(0, 0, 0, 0.05)"} !important;
    background: {"rgba(255, 255, 255, 0.08)" if dark else "rgba(0, 0, 0, 0.05)"} !important;
    color: {text} !important;
}}

input, textarea {{
    color: {text} !important;
    background: transparent !important;
}}

/* Multiselect tags */
[data-baseweb="tag"],
[data-testid="stMultiSelectTag"] {{
    background: {tag_bg} !important;
    border: 1px solid {tag_brd} !important;
    border-radius: 4px !important;
    box-shadow: none !important;
}}
[data-baseweb="tag"] span,
[data-baseweb="tag"] div,
[data-baseweb="tag-text"],
[data-testid="stMultiSelectTag"] * {{
    color: {tag_txt} !important;
    background: transparent !important;
    font-size: 0.86rem !important;
}}
[data-baseweb="tag"] svg {{
    fill: {subtext} !important;
}}

/* BaseWeb Select options popover / dropdown menu */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"],
div[data-baseweb="menu"] {{
    background-color: {panel} !important;
    background: {panel} !important;
    border: 1px solid {border} !important;
    border-radius: 6px !important;
}}
div[data-baseweb="popover"] li,
div[data-baseweb="menu"] li,
li[role="option"] {{
    background-color: transparent !important;
    color: {text} !important;
    font-size: 0.90rem !important;
}}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"],
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {{
    background-color: {hover_bg} !important;
    color: {text} !important;
}}

/* Dataframe */
[data-testid="stDataFrame"] {{
    border: 1px solid {border} !important;
    border-radius: 6px !important;
    overflow: hidden;
}}
[data-testid="stDataFrame"] th {{
    background: {table_hdr} !important;
    color: {subtext} !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}}
[data-testid="stDataFrame"] td {{
    color: {text} !important;
    font-size: 0.90rem !important;
}}

/* Metric */
[data-testid="stMetricValue"] {{
    color: {text} !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
}}
[data-testid="stMetricLabel"] {{
    color: {subtext} !important;
    font-size: 0.85rem !important;
}}

/* Success / info / warning banners */
[data-testid="stAlert"] {{
    border-radius: 6px !important;
    font-size: 0.90rem !important;
}}

/* ── Bottom Fixed Bar & Chat Input Area ─────────────────── */
[data-testid="stBottom"] {{
    background-color: {stapp_bg} !important;
    background: {stapp_bg} !important;
    border-top: 1px solid {border} !important;
    box-shadow: {"0 -4px 20px rgba(0,0,0,0.35)" if dark else "0 -4px 20px rgba(0,0,0,0.03)"} !important;
    padding-bottom: 12px !important;
    padding-top: 8px !important;
}}
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] {{
    background-color: transparent !important;
    background: transparent !important;
}}
[data-testid="stChatInput"] {{
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
}}
[data-testid="stChatInput"] > div {{
    background-color: {inputbg} !important;
    background: {inputbg} !important;
    border: 1.5px solid {inputbrd} !important;
    border-radius: 12px !important;
    box-shadow: {"0 2px 10px rgba(0,0,0,0.30)" if dark else "0 2px 10px rgba(0,0,0,0.04)"} !important;
    padding: 6px 14px !important;
    min-height: 52px !important;
    display: flex !important;
    align-items: center !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}}
[data-testid="stChatInput"] > div:focus-within {{
    border-color: {"rgba(255,255,255,0.35)" if dark else "rgba(0,0,0,0.35)"} !important;
    box-shadow: {"0 3px 14px rgba(255,255,255,0.08)" if dark else "0 3px 14px rgba(0,0,0,0.08)"} !important;
}}
[data-testid="stChatInputTextArea"] {{
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: {text} !important;
    font-size: 0.94rem !important;
    line-height: 1.5 !important;
    padding: 8px 6px !important;
    min-height: 38px !important;
    max-height: 160px !important;
    resize: none !important;
    font-family: inherit !important;
}}
[data-testid="stChatInputTextArea"]::placeholder {{
    color: {subtext} !important;
    opacity: 0.8 !important;
    font-size: 0.90rem !important;
}}
[data-testid="stChatInputTextArea"]:focus {{
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Chat input submit button — locked vertically centered, clean icon with no stray lines */
[data-testid="stChatInputSubmitButton"] {{
    align-self: center !important;
    margin: auto 0 auto 8px !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    min-height: 36px !important;
    max-width: 36px !important;
    max-height: 36px !important;
    border-radius: 8px !important;
    background-color: {"#2E2B31" if dark else "#E4DED5"} !important;
    border: 1px solid {"rgba(255,255,255,0.15)" if dark else "rgba(0,0,0,0.14)"} !important;
    outline: none !important;
    box-shadow: none !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    transition: all 0.15s ease !important;
    flex-shrink: 0 !important;
    cursor: pointer !important;
}}
[data-testid="stChatInputSubmitButton"] svg {{
    fill: {"#EDEDED" if dark else "#111111"} !important;
    stroke: none !important;
    color: {"#EDEDED" if dark else "#111111"} !important;
    width: 18px !important;
    height: 18px !important;
}}
[data-testid="stChatInputSubmitButton"] svg * {{
    stroke: none !important;
}}
[data-testid="stChatInputSubmitButton"] svg path[fill="none"] {{
    display: none !important;
    stroke: none !important;
}}
[data-testid="stChatInputSubmitButton"]:hover {{
    background-color: {"#3E3A42" if dark else "#D8D1C7"} !important;
    border-color: {"rgba(255,255,255,0.30)" if dark else "rgba(0,0,0,0.25)"} !important;
}}
[data-testid="stChatInputSubmitButton"]:disabled {{
    opacity: 0.35 !important;
    cursor: not-allowed !important;
}}
/* ── Completely Suppress "Press Enter to submit form" and all helper instructions ── */
[data-testid="InputInstructions"],
div[data-testid="InputInstructions"],
span[data-testid="InputInstructions"],
small[data-testid="InputInstructions"],
.stTextArea small,
.stTextInput small,
[data-testid="stForm"] small,
[data-testid="stForm"] [data-testid="InputInstructions"],
[data-testid="stChatInputInstructions"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    width: 0 !important;
    pointer-events: none !important;
    position: absolute !important;
}}

/* Zero-dimension script runner iframes replacing deprecated st.components.v1.html */
iframe.stIFrame[title$="_script_runner"],
div[data-testid="stElementContainer"]:has(iframe[title$="_script_runner"]),
div[data-testid="stIFrame"]:has(iframe[title$="_script_runner"]) {{
    display: inline !important;
    position: absolute !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
    overflow: hidden !important;
    border: none !important;
}}

/* ── Scroll Down Nudge Button (First-Load Smooth Transition-In) ── */
html {{
    scroll-behavior: smooth !important;
}}

/* Final enforcement: theme toggle button icon is never overridden */
.st-key-top_theme_toggle_btn button::after,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button::after {{
    content: "" !important;
    display: block !important;
    width: 20px !important;
    height: 20px !important;
    background-image: url("{toggle_svg}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
}}
.st-key-top_theme_toggle_btn button:hover::after,
div[data-testid="stButton"].st-key-top_theme_toggle_btn button:hover::after {{
    background-image: url("{toggle_svg_hover}") !important;
    transform: scale(1.08) !important;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   RESPONSIVE & MOBILE VIEW FRIENDLY DESIGN
   Breakpoints: Tablets (<= 992px), Mobile Phones (<= 768px), Compact (<= 480px)
   ═══════════════════════════════════════════════════════════════════════════ */


/* ── Tablets & Mobile (<= 880px): Stack Top Navigation Vertically ── */
@media (max-width: 880px) {{
    .st-key-top_nav_bar,
    div[data-testid="stContainer"].st-key-top_nav_bar {{
        width: 100% !important;
        max-width: 100% !important;
        padding: 4px 0 !important;
    }}
    .st-key-top_nav_bar [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: column !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        width: 100% !important;
        overflow-x: visible !important;
    }}
    .st-key-top_nav_bar [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    .st-key-top_nav_bar div[data-testid="stColumn"] {{
        display: block !important;
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    .st-key-top_nav_bar div[data-testid="stButton"],
    .st-key-top_nav_bar div[data-testid="stButton"] > button,
    .st-key-top_nav_bar div[data-testid="stButton"]:not(.st-key-btn_ask_portfolio_cta):not(.st-key-nav_btn_ask_portfolio) button,
    .st-key-btn_ask_portfolio_cta button,
    .st-key-nav_btn_ask_portfolio button,
    button[key^="topnav_"] {{
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 44px !important;
        min-height: 44px !important;
        padding: 8px 16px !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        box-sizing: border-box !important;
    }}
    .st-key-top_nav_bar div[data-testid="stButton"] button *,
    .st-key-btn_ask_portfolio_cta button *,
    .st-key-nav_btn_ask_portfolio button *,
    button[key^="topnav_"] * {{
        font-size: 0.92rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}
    .st-key-btn_ask_portfolio_cta button,
    .st-key-nav_btn_ask_portfolio button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
    }}
}}

/* ── Mobile Phones (<= 768px) ── */
@media (max-width: 768px) {{
    /* Reset main site and header to full width on mobile screens */
    .stApp section[data-testid="stMain"],
    .stApp [data-testid="stMain"] {{
        margin-left: 0 !important;
        left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }}
    .st-key-top_app_header_bar,
    div[data-testid="stContainer"].st-key-top_app_header_bar {{
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
    }}

    /* Main container padding */
    .stApp .block-container {{
        padding-top: 66px !important;
        padding-left: 12px !important;
        padding-right: 12px !important;
        padding-bottom: 2rem !important;
    }}

    /* Default: Stack content columns vertically on mobile (except chat header) */
    .stApp [data-testid="stAppViewContainer"] > .main [data-testid="stHorizontalBlock"]:not(.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"]):not(.st-key-ask_portfolio_side_panel [data-testid="stHorizontalBlock"]) {{
        display: flex !important;
        flex-direction: column !important;
        gap: 14px !important;
    }}
    .stApp [data-testid="stAppViewContainer"] > .main [data-testid="stHorizontalBlock"]:not(.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"]):not(.st-key-ask_portfolio_side_panel [data-testid="stHorizontalBlock"]) > div[data-testid="stColumn"] {{
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
    }}

    /* Fixed Top Header on Mobile */
    .st-key-top_app_header_bar,
    div[data-testid="stContainer"].st-key-top_app_header_bar {{
        height: 68px !important;
        max-height: 68px !important;
        padding: 0 8px !important;
    }}
    .st-key-top_app_header_bar [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 0 !important;
        width: 100% !important;
        position: static !important;
    }}
    .st-key-top_app_header_bar div[data-testid="stColumn"]:first-child {{
        width: 38px !important;
        min-width: 38px !important;
        max-width: 38px !important;
        flex: 0 0 38px !important;
    }}
    .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(2) {{
        flex: 1 1 auto !important;
        min-width: 0 !important;
        max-width: none !important;
        width: auto !important;
        overflow: hidden !important;
        text-align: center !important;
        position: static !important;
    }}
    .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(3) {{
        flex: 0 0 auto !important;
        min-width: fit-content !important;
        max-width: none !important;
        width: auto !important;
        margin-left: auto !important;
    }}
    .top-center-brand {{
        font-size: 1.08rem !important;
        line-height: 1 !important;
        letter-spacing: -0.01em !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        padding: 0 4px !important;
    }}
    .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(3) [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: flex-end !important;
        align-items: center !important;
        gap: 4px !important;
        width: auto !important;
    }}
    .st-key-top_app_header_bar div[data-testid="stColumn"]:nth-child(3) [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: fit-content !important;
        max-width: none !important;
    }}

    /* Mobile Header Layout Containers */
    .st-key-top_app_header_bar [data-testid="stElementContainer"],
    .st-key-top_app_header_bar div[data-testid="stButton"],
    .st-key-font_dec_btn,
    .st-key-font_inc_btn,
    .st-key-top_theme_toggle_btn {{
        height: 62px !important;
        min-height: 62px !important;
        max-height: 62px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Mobile Sidebar Toggle Buttons (No Box) */
    header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
    [data-testid="stExpandSidebarButton"],
    button[data-testid="stExpandSidebarButton"],
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button {{
        top: 17px !important;
        left: 8px !important;
        width: 34px !important;
        height: 34px !important;
        min-width: 34px !important;
        max-width: 34px !important;
        min-height: 34px !important;
        max-height: 34px !important;
        border-radius: 7px !important;
        border: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
        background-color: transparent !important;
    }}
    header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]::after,
    [data-testid="stExpandSidebarButton"]::after,
    button[data-testid="stExpandSidebarButton"]::after {{
        width: 17px !important;
        height: 17px !important;
    }}
    [data-testid="stSidebarCollapseButton"] button::after {{
        width: 15px !important;
        height: 15px !important;
    }}

    /* Mobile Utility Buttons (A-, A+, Theme toggle - No Box, Vertically Middle Justified) */
    .st-key-font_dec_btn button,
    .st-key-font_inc_btn button,
    .st-key-top_theme_toggle_btn button,
    .st-key-top_theme_toggle_btn button[kind="secondary"],
    div[data-testid="stButton"].st-key-top_theme_toggle_btn button {{
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        max-width: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        border-radius: 7px !important;
        border: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
        background-color: transparent !important;
        align-self: center !important;
        margin: 0 auto !important;
    }}
    .st-key-font_dec_btn button *,
    .st-key-font_inc_btn button * {{
        font-size: 13px !important;
    }}
    .st-key-top_theme_toggle_btn button::after,
    .st-key-top_theme_toggle_btn button[kind="secondary"]::after,
    div[data-testid="stButton"].st-key-top_theme_toggle_btn button::after {{
        width: 16px !important;
        height: 16px !important;
        margin: 0 auto !important;
    }}

    /* Mobile Top Navigation: Vertically Stacked Full-Width Buttons */
    .st-key-top_nav_bar,
    div[data-testid="stContainer"].st-key-top_nav_bar {{
        width: 100% !important;
        max-width: 100% !important;
        padding: 4px 0 !important;
    }}
    .st-key-top_nav_bar [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: column !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        width: 100% !important;
        overflow-x: visible !important;
    }}
    .st-key-top_nav_bar [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    .st-key-top_nav_bar div[data-testid="stColumn"] {{
        display: block !important;
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    .st-key-top_nav_bar div[data-testid="stButton"],
    .st-key-top_nav_bar div[data-testid="stButton"] > button,
    .st-key-top_nav_bar div[data-testid="stButton"]:not(.st-key-btn_ask_portfolio_cta):not(.st-key-nav_btn_ask_portfolio) button,
    .st-key-btn_ask_portfolio_cta button,
    .st-key-nav_btn_ask_portfolio button,
    button[key^="topnav_"] {{
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 44px !important;
        min-height: 44px !important;
        padding: 8px 16px !important;
        font-size: 0.90rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        box-sizing: border-box !important;
    }}
    .st-key-top_nav_bar div[data-testid="stButton"] button *,
    .st-key-btn_ask_portfolio_cta button *,
    .st-key-nav_btn_ask_portfolio button *,
    button[key^="topnav_"] * {{
        font-size: 0.90rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}
    .st-key-btn_ask_portfolio_cta button,
    .st-key-nav_btn_ask_portfolio button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }}

    /* Responsive 2-Column KPI Strip */
    [data-testid="stHorizontalBlock"]:has(.kpi-card) {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }}
    [data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] {{
        flex: 1 1 calc(50% - 6px) !important;
        min-width: calc(50% - 6px) !important;
        max-width: calc(50% - 6px) !important;
        width: calc(50% - 6px) !important;
    }}
    [data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"]:last-child:nth-child(odd) {{
        flex: 1 1 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        width: 100% !important;
    }}
    .kpi-card {{
        padding: 10px 12px !important;
    }}
    .kpi-value {{
        font-size: 1.35rem !important;
    }}
    .kpi-label {{
        font-size: 0.74rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}
    .kpi-sub {{
        font-size: 0.70rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}

    /* Responsive 2-Column Anomaly Queue KPIs */
    [data-testid="stHorizontalBlock"]:has(.anomaly-kpi) {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }}
    [data-testid="stHorizontalBlock"]:has(.anomaly-kpi) > div[data-testid="stColumn"] {{
        flex: 1 1 calc(50% - 6px) !important;
        min-width: calc(50% - 6px) !important;
        max-width: calc(50% - 6px) !important;
        width: calc(50% - 6px) !important;
    }}
    .anomaly-kpi {{
        padding: 10px 12px !important;
    }}
    .anomaly-kpi-value {{
        font-size: 1.35rem !important;
    }}

    /* Responsive Metrics Grid (Account Deep Dive 4 metrics -> 2x2 grid) */
    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }}
    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > div[data-testid="stColumn"] {{
        flex: 1 1 calc(50% - 6px) !important;
        min-width: calc(50% - 6px) !important;
        max-width: calc(50% - 6px) !important;
        width: calc(50% - 6px) !important;
    }}

    /* Full-Width Mobile Charts */
    div[data-testid="stPlotlyChart"],
    .js-plotly-plot,
    .plot-container {{
        width: 100% !important;
        max-width: 100% !important;
    }}

    /* Touch-Scrollable DataFrames */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {{
        width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }}

    /* Left Sidebar Mobile Drawer */
    [data-testid="stSidebar"] {{
        width: min(340px, 86vw) !important;
        min-width: min(340px, 86vw) !important;
        max-width: min(340px, 86vw) !important;
        box-shadow: 6px 0 28px rgba(0,0,0,0.45) !important;
    }}
    [data-testid="stSidebarContent"],
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
    }}
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }}
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
        flex: 1 1 50% !important;
        min-width: 0 !important;
        max-width: 50% !important;
        width: 50% !important;
    }}

    /* Right Drawer Sheet on Compact Phones Only */
    @media (max-width: 580px) {{
        .st-key-ask_portfolio_side_panel,
        div[data-testid="stContainer"].st-key-ask_portfolio_side_panel {{
            width: 100vw !important;
            max-width: 100vw !important;
            min-width: 100vw !important;
            padding: 16px 14px 28px 14px !important;
            z-index: 999999 !important;
        }}
        .stApp section[data-testid="stMain"],
        .stApp [data-testid="stMain"] {{
            margin-right: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
        }}
        .st-key-top_app_header_bar,
        div[data-testid="stContainer"].st-key-top_app_header_bar {{
            right: 0 !important;
        }}
    }}
    .st-key-ask_portfolio_side_panel,
    div[data-testid="stContainer"].st-key-ask_portfolio_side_panel {{
        padding: 0 16px 32px 16px !important;
    }}
    .st-key-gcp_chat_header_sticky,
    div[data-testid="stContainer"].st-key-gcp_chat_header_sticky {{
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        box-shadow: none !important;
    }}
    .st-key-ask_portfolio_side_panel [data-testid="stHorizontalBlock"]:not(.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"]):not(.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"]) {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 8px !important;
    }}
    .st-key-ask_portfolio_side_panel [data-testid="stHorizontalBlock"]:not(.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"]):not(.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"]) > div[data-testid="stColumn"] {{
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: fit-content !important;
        max-width: none !important;
    }}
    .st-key-ask_portfolio_side_panel [data-testid="stHorizontalBlock"]:not(.st-key-gcp_chat_header_sticky [data-testid="stHorizontalBlock"]):not(.st-key-gcp_gov_header_sticky [data-testid="stHorizontalBlock"]) > div[data-testid="stColumn"]:first-child {{
        flex: 1 1 auto !important;
    }}

    .gcp-assist-title {{
        font-size: 1.15rem !important;
    }}
    .gcp-welcome-title {{
        font-size: 1.40rem !important;
    }}
    .gcp-welcome-subtitle {{
        font-size: 0.92rem !important;
    }}

    /* Typography Adjustments */
    .page-header-wrap {{
        margin-bottom: 18px !important;
        padding-bottom: 12px !important;
    }}
    .page-title {{
        font-size: 1.30rem !important;
    }}
    .page-sub {{
        font-size: 0.88rem !important;
    }}
    .insight-card {{
        padding: 14px 16px !important;
    }}
    .insight-title {{
        font-size: 1.15rem !important;
    }}
    .insight-obs {{
        font-size: 0.94rem !important;
    }}
}}

/* ── Compact Mobile Phones (<= 480px) ── */
@media (max-width: 480px) {{
    .top-center-brand {{
        font-size: 0.92rem !important;
    }}
    .kpi-card {{
        padding: 8px 10px !important;
    }}
    .kpi-value {{
        font-size: 1.25rem !important;
    }}
    .kpi-label {{
        font-size: 0.70rem !important;
    }}
}}

/* ── Dialog / Modal Backdrop & Site Blurring ── */
div[data-baseweb="modal"] div[data-baseweb="backdrop"],
div[data-testid="stModalBackdrop"],
div[data-baseweb="backdrop"] {{
    background-color: {"rgba(0, 0, 0, 0.65)" if dark else "rgba(15, 23, 42, 0.40)"} !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
}}

.stApp:has([data-baseweb="modal"]) section[data-testid="stMain"],
.stApp:has([data-testid="stModal"]) section[data-testid="stMain"],
.stApp:has([data-baseweb="modal"]) .st-key-top_app_header_bar,
.stApp:has([data-testid="stModal"]) .st-key-top_app_header_bar,
.stApp:has([data-baseweb="modal"]) [data-testid="stSidebar"],
.stApp:has([data-testid="stModal"]) [data-testid="stSidebar"],
.stApp:has([data-baseweb="modal"]) .st-key-ask_portfolio_side_panel,
.stApp:has([data-testid="stModal"]) .st-key-ask_portfolio_side_panel {{
    filter: blur(6px) !important;
    transition: filter 0.25s ease !important;
}}

/* ── Modal / Dialog Comprehensive Dark & Light Styling ── */
div[data-testid="stDialog"],
div[data-testid="stDialog"] > div,
div[data-testid="stDialogBody"],
div[data-testid="stModal"],
div[data-testid="stModal"] > div,
div[data-baseweb="modal"] [role="dialog"],
div[data-baseweb="modal"] [role="dialog"] > div,
div[data-baseweb="modal"] [data-testid="stDialog"],
div[data-baseweb="modal"] [data-testid="stDialog"] > div {{
    background-color: {card_bg} !important;
    background: {card_bg} !important;
    color: {text} !important;
}}

div[data-testid="stDialog"],
div[data-testid="stModal"],
div[data-baseweb="modal"] [role="dialog"] {{
    border: 1px solid {border} !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, {"0.60" if dark else "0.15"}) !important;
    color: {text} !important;
    z-index: 99999999 !important;
    width: min(480px, 92vw) !important;
    max-width: min(480px, 92vw) !important;
}}

div[data-testid="stDialog"] > div,
div[data-testid="stModal"] > div,
div[data-baseweb="modal"] [role="dialog"] > div {{
    max-width: 100% !important;
    width: 100% !important;
}}

div[data-testid="stDialog"] header,
div[data-testid="stDialog"] [data-testid="stDialogHeader"],
div[data-testid="stModal"] header,
div[data-testid="stModal"] [data-testid="stDialogHeader"],
div[data-baseweb="modal"] [role="dialog"] header {{
    background: transparent !important;
    border-bottom: 1px solid {divider} !important;
    padding-bottom: 6px !important;
    margin-bottom: 10px !important;
}}

div[data-testid="stDialog"] [data-testid="stDialogHeader"] *,
div[data-testid="stDialog"] header *,
div[data-testid="stModal"] [data-testid="stDialogHeader"] *,
div[data-baseweb="modal"] [role="dialog"] h2,
div[data-baseweb="modal"] [role="dialog"] h3 {{
    color: {text} !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
}}

/* Close Button (✕) */
div[data-testid="stDialog"] button,
div[data-testid="stDialog"] button[aria-label="Close"],
div[data-testid="stModal"] button[aria-label="Close"],
div[data-baseweb="modal"] [role="dialog"] button {{
    color: {subtext} !important;
    background: transparent !important;
    border: none !important;
}}
div[data-testid="stDialog"] button:hover,
div[data-baseweb="modal"] [role="dialog"] button:hover {{
    color: {text} !important;
}}
div[data-testid="stDialog"] button svg,
div[data-baseweb="modal"] [role="dialog"] button svg {{
    fill: {subtext} !important;
    stroke: {subtext} !important;
}}
div[data-testid="stDialog"] button:hover svg,
div[data-baseweb="modal"] [role="dialog"] button:hover svg {{
    fill: {text} !important;
    stroke: {text} !important;
}}

/* ── Governance Specification Modal Content Cards ── */
.gov-dialog-container {{
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
    padding: 0 !important;
    width: 100% !important;
}}

.gov-dialog-header-badge {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 3px 10px !important;
    border-radius: 6px !important;
    background: {"rgba(99, 102, 241, 0.16)" if dark else "rgba(79, 70, 229, 0.08)"} !important;
    color: {"#A5B4FC" if dark else "#4F46E5"} !important;
    border: 1px solid {"rgba(99, 102, 241, 0.30)" if dark else "rgba(79, 70, 229, 0.18)"} !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 2px !important;
    width: fit-content !important;
}}

.gov-card {{
    background: {"#242226" if dark else "#FFFFFF"} !important;
    border: 1px solid {border} !important;
    border-radius: 8px !important;
    padding: 9px 12px !important;
}}

.gov-card-title {{
    font-size: 0.70rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: {"#818CF8" if dark else "#4F46E5"} !important;
    margin-bottom: 3px !important;
}}

.gov-card-desc {{
    font-size: 0.82rem !important;
    line-height: 1.42 !important;
    color: {text} !important;
}}

/* Hide streamlit decoration */
#MainMenu, footer {{ visibility: hidden; }}
</style>
"""



def get_chart_theme(dark: bool) -> dict:
    if dark:
        return dict(
            bg=dict(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#C8C8D0", size=12),
                margin=dict(l=10, r=10, t=40, b=10),
            ),
            grid="rgba(255,255,255,0.06)",
            line="rgba(255,255,255,0.08)",
            tick="#8A8A97",
            text="#E8E8E8",
            bar="#4A4A5A",
            danger="#f87171",
            timeline_line="#C8C8D0",
            timeline_fill="rgba(200,200,208,0.08)",
        )
    else:
        return dict(
            bg=dict(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#111111", size=12),
                margin=dict(l=10, r=10, t=40, b=10),
            ),
            grid="#EDE8E2",
            line="#E4DDD4",
            tick="#6B6B78",
            text="#111111",
            bar="#94A3B8",
            danger="#dc2626",
            timeline_line="#111111",
            timeline_fill="rgba(17,17,17,0.06)",
        )




def themed_fig(fig, is_dark: bool = False, height: int = 340, hide_legend: bool = False) -> go.Figure:
    thm = get_chart_theme(is_dark)
    fig.update_layout(
        **thm["bg"],
        height=height,
        dragmode=False,
        hovermode="closest",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=12, color=thm["tick"]),
        ),
    )
    if hide_legend:
        fig.update_layout(showlegend=False)
    fig.update_xaxes(
        showgrid=False,
        linecolor=thm["line"],
        tickfont=dict(size=12, color=thm["tick"]),
        title_font=dict(size=13, color=thm["tick"]),
        fixedrange=True,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=thm["grid"],
        linecolor=thm["line"],
        tickfont=dict(size=12, color=thm["tick"]),
        title_font=dict(size=13, color=thm["tick"]),
        fixedrange=True,
    )
    return fig

