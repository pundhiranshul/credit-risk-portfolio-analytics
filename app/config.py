"""
Central configuration and constants for the Credit Risk Portfolio Analytics Dashboard.
"""
from pathlib import Path
from src.llm_assistant import AI_METADATA_SPEC
from src.anomaly import ANOMALY_METADATA_SPEC

REPO_ROOT = Path(__file__).resolve().parent.parent
FAVICON_PATH = REPO_ROOT / "app" / "assets" / "favicon.png"

TIER_COLORS = {
    "Low Risk":      "#16a34a",
    "Medium Risk":   "#d97706",
    "High Risk":     "#dc2626",
    "Critical Risk": "#7f1d1d",
}

PLOTLY_CONFIG = {
    "scrollZoom": False,
    "displayModeBar": "hover",
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "select2d", "lasso2d",
        "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d"
    ],
    "responsive": True,
}

NAV_ITEMS = [
    ("Portfolio View",        "▦"),
    ("Account Deep-Dive",     "◎"),
    ("Anomaly Review Queue",  "⚑"),
    ("Strategic Insights",    "◉"),
    ("Ask the Portfolio",     "✨"),
]

PAGE_META = {
    "Portfolio View":       ("Portfolio Risk Overview", ""),
    "Account Deep-Dive":    ("Account Risk Deep-Dive",  "Probability of default, solvency profile & risk drivers"),
    "Anomaly Review Queue": ("Anomaly Review Queue",     "Dual-lens detection · flagged accounts pending triage"),
    "Strategic Insights":   ("Strategic Insights",       "Top 5 data-driven portfolio findings & policy prescriptions"),
}
