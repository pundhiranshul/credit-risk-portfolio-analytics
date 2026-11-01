"""
Automated 1-Page PDF Generator and Page Count Validator
-------------------------------------------------------
Generates the two mandatory executive PDF deliverables required by the assignment brief:
1. docs/architecture.pdf: End-to-end pipeline flow, libraries/tools, embedded AI systems, and explicit LLM data boundary.
2. docs/solution_overview.pdf: Risk analyst guide, AI governance matrix, model performance scorecard, top 3 insights, and IT production requirements.

STRICT ENFORCEMENT:
The brief states: 'Submit exactly two documents, each one page, as PDF... Content beyond one page will not be read.'
This script validates that both PDFs are strictly and exactly 1 page.

Author: Anshul Pundhir <anshulpundhirwork@gmail.com>
"""

import json
import logging
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)
import pypdf

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("generate_docs")

DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)
METRICS_PATH = Path("data/processed/models/model_evaluation_metrics.json")


class HorizontalRule(Flowable):
    """Draws a crisp full-width solid horizontal rule."""

    def __init__(self, width: float, thickness: float = 1.5, color: colors.Color = colors.HexColor("#0F172A")):
        super().__init__()
        self.rule_width = width
        self.thickness = thickness
        self.color = color
        self.width = width
        self.height = thickness

    def wrap(self, availWidth, availHeight):
        return (self.rule_width, self.thickness)

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.rule_width, self.thickness, stroke=0, fill=1)
        self.canv.restoreState()


class PillGroup(Flowable):
    """Renders rows of rounded indigo pill badges (e.g., Python 3.12, Pandas) inside a table cell."""

    def __init__(self, rows: list[list[str]], font_size: float = 7.5):
        super().__init__()
        self.rows = rows
        self.font_size = font_size
        self.pill_h = 12.0
        self.row_gap = 2.0
        self.col_gap = 3.0
        self.pad_x = 4.2
        self.height = len(rows) * self.pill_h + max(0, len(rows) - 1) * self.row_gap
        self.width = 115.0

    def wrap(self, availWidth, availHeight):
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFont("Helvetica-Bold", self.font_size)
        y = self.height - self.pill_h
        for row in self.rows:
            x = 0.0
            for label in row:
                tw = c.stringWidth(label, "Helvetica-Bold", self.font_size)
                pw = tw + 2 * self.pad_x
                c.setFillColor(colors.HexColor("#E0E7FF"))
                c.setStrokeColor(colors.HexColor("#E0E7FF"))
                c.roundRect(x, y, pw, self.pill_h, radius=2.5, stroke=1, fill=1)
                c.setFillColor(colors.HexColor("#3730A3"))
                c.drawString(x + self.pad_x, y + 3.3, label)
                x += pw + self.col_gap
            y -= self.pill_h + self.row_gap
        c.restoreState()


def _make_footer_callback(left_margin: float, right_margin: float, bottom_y: float, doc_title: str):
    """Returns a ReportLab page callback that renders the standard footer and sets PDF title metadata."""

    def _draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setTitle(doc_title)
        canvas.setAuthor("Anshul Pundhir (anshulpundhirwork@gmail.com)")
        canvas.setFont("Helvetica", 8.5)
        canvas.setFillColor(colors.HexColor("#64748B"))
        page_w = A4[0]
        canvas.drawString(left_margin, bottom_y, "Credit Risk Portfolio Analytics")
        canvas.drawRightString(page_w - right_margin, bottom_y, "Page 1 of 1")
        canvas.restoreState()

    return _draw_footer


def _section_banner(text: str, width: float, height: float, font_size: float, left_pad: float = 5.0) -> Table:
    """Creates a light-slate section header bar matching the reference design."""
    style = ParagraphStyle(
        f"SecHdr_{font_size}",
        fontName="Helvetica-Bold",
        fontSize=font_size,
        leading=font_size + 2.0,
        textColor=colors.HexColor("#0F172A"),
    )
    tbl = Table([[Paragraph(text, style)]], colWidths=[width], rowHeights=[height])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), left_pad),
                ("RIGHTPADDING", (0, 0), (-1, -1), left_pad),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return tbl


def _load_latest_metrics() -> dict:
    """Loads latest model evaluation metrics from JSON, with safe fallback defaults."""
    default_m = {
        "logistic_regression": {"auc": 0.6620, "ks_stat_pct": 24.78, "gini": 0.3240, "brier_score": 0.1274},
        "lightgbm": {"auc": 0.6657, "ks_stat_pct": 25.57, "gini": 0.3314, "brier_score": 0.1274},
    }
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("metrics", default_m)
        except Exception as e:
            logger.warning("Could not read model metrics JSON (%s), using defaults.", e)
    return default_m


def build_architecture_pdf(output_path: str = "docs/architecture.pdf"):
    """
    Builds docs/architecture.pdf (Strictly 1 Page, A4):
    1. End-to-End Pipeline Flow (Raw Data to Executive Dashboard)
    2. Embedded AI Systems Architecture & Data Boundaries
    """
    left_margin = 51.0
    right_margin = 50.7756  # Printable width = 493.5 pt on A4 (595.2756 pt)
    content_width = A4[0] - left_margin - right_margin  # 493.5 pt

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=42.0,
        bottomMargin=42.0,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ArchTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14.0,
        leading=17.0,
        textColor=colors.HexColor("#0F172A"),
    )
    subtitle_style = ParagraphStyle(
        "ArchSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.0,
        leading=12.0,
        textColor=colors.HexColor("#3B82F6"),
    )
    th_style = ParagraphStyle(
        "ArchTH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
    )
    cell_style = ParagraphStyle(
        "ArchCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.3,
        textColor=colors.HexColor("#1E293B"),
    )

    story = []

    # ── Header ──
    story.append(Paragraph("SYSTEM ARCHITECTURE", title_style))
    story.append(Spacer(1, 5.0))
    story.append(
        Paragraph(
            "Credit Risk Portfolio Analytics | Anshul Pundhir (anshulpundhirwork@gmail.com)",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 7.5))
    story.append(HorizontalRule(content_width, thickness=1.5, color=colors.HexColor("#0F172A")))
    story.append(Spacer(1, 9.0))

    # ── Section 1: End-to-End Pipeline Flow (Raw Data to Executive Dashboard) ──
    story.append(
        _section_banner(
            "1. End-to-End Pipeline Flow (Raw Data to Executive Dashboard)",
            width=content_width,
            height=20.25,
            font_size=10.5,
            left_pad=6.0,
        )
    )
    story.append(Spacer(1, 3.0))

    flow_rows = [
        [
            Paragraph("<b>Stage &amp; Script</b>", th_style),
            Paragraph("<b>Libraries &amp; Tools</b>", th_style),
            Paragraph("<b>Data Flow, Operations &amp; Intentional Quality Treatments</b>", th_style),
        ],
        [
            Paragraph(
                "<b>1. Raw Ingestion &amp;<br/>QC</b><br/>"
                "<font name='Courier' size='8.2'>src/ingestion.py</font>",
                cell_style,
            ),
            PillGroup([["Python 3.12", "Pandas"], ["NumPy", "PyArrow"]]),
            Paragraph(
                "<b>Inputs:</b> 5 raw CSVs (customers, loans, bureau_credit, repayment_history, collections).<br/>"
                "<b>Operations:</b> Standardizes string labels (e.g., gender), applies caps to anomalous numeric bounds "
                "(tenure exceeding age), and imputes missing interest rates via loan-type medians. Resolves missing "
                "employment data using cohort medians, inserting strict <font name='Courier' size='8.2'>_is_na</font> audit "
                "flags for regulatory tracing. Outputs validated Parquet files.",
                cell_style,
            ),
        ],
        [
            Paragraph(
                "<b>2. Feature Store</b><br/>"
                "<font name='Courier' size='8.2'>src/features.py</font><br/>"
                "<font name='Courier' size='8.2'>src/analytics.py</font>",
                cell_style,
            ),
            PillGroup([["Scikit-Learn", "Pandas"]]),
            Paragraph(
                "<b>Operations:</b> Aggregates external bureau trade-lines to borrower grain (utilization, total lines, "
                "write-offs). Computes monthly payment roll-rates and trailing 3-month momentum. Calculates annualized DTI "
                "and principal LTI. <b>Critical Step:</b> Strictly filters all post-default collections events to prevent "
                "target data leakage into the training set.",
                cell_style,
            ),
        ],
        [
            Paragraph(
                "<b>3. ML &amp; Anomaly<br/>Engine</b><br/>"
                "<font name='Courier' size='8.2'>src/model.py</font><br/>"
                "<font name='Courier' size='8.2'>src/anomaly.py</font>",
                cell_style,
            ),
            PillGroup([["LightGBM", "SHAP", "SciPy"], ["Joblib"]]),
            Paragraph(
                "<b>Operations:</b> Trains an interpretable Logistic Regression benchmark alongside a depth-constrained "
                "LightGBM champion model. Pre-computes per-account <b>TreeSHAP</b> local attribution vectors. Runs a "
                "dual-lens unsupervised anomaly engine (Lens 1: Trailing payment drop heuristics; Lens 2: Cohort-normalized "
                "Isolation Forest) to flag pre-bureau risk outliers.",
                cell_style,
            ),
        ],
        [
            Paragraph(
                "<b>4. Dashboard (UI)</b><br/>"
                "<font name='Courier' size='8.2'>app/app.py</font><br/>"
                "<font name='Courier' size='8.2'>app/views/*</font>",
                cell_style,
            ),
            PillGroup([["Streamlit", "Plotly"]]),
            Paragraph(
                "<b>Operations:</b> Interactive interface featuring Portfolio Overview (macro KPIs, multidimensional "
                "heatmaps), Account Deep-Dive (gauge charts, SHAP waterfall, repayment timelines), Anomaly Triage Queue, "
                "and the LLM-powered natural language Copilot.",
                cell_style,
            ),
        ],
    ]

    t_flow = Table(flow_rows, colWidths=[99.0, 123.0, 271.5])
    t_flow.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, 0), 4.5),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 4.5),
                ("TOPPADDING", (0, 1), (-1, -1), 5.0),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 5.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5.0),
            ]
        )
    )
    story.append(t_flow)
    story.append(Spacer(1, 9.0))

    # ── Section 2: Embedded AI Systems Architecture & Data Boundaries ──
    story.append(
        _section_banner(
            "2. Embedded AI Systems Architecture &amp; Data Boundaries",
            width=content_width,
            height=20.25,
            font_size=10.5,
            left_pad=6.0,
        )
    )
    story.append(Spacer(1, 3.0))

    ai_rows = [
        [
            Paragraph("<b>AI Feature</b>", th_style),
            Paragraph("<b>Trigger &amp; Module</b>", th_style),
            Paragraph("<b>Mechanics, LLM Calls &amp; Data Payload (Privacy Shield)</b>", th_style),
        ],
        [
            Paragraph(
                "<b>Ask the<br/>Portfolio</b><br/><br/>(Natural<br/>Language Q&amp;A)",
                cell_style,
            ),
            Paragraph(
                "<b>Trigger:</b> Analyst submits<br/>query in UI.<br/>"
                "<b>Module:</b><br/><font name='Courier' size='8.2'>src/llm_assistant.py</font>",
                cell_style,
            ),
            Paragraph(
                "<b>Mechanism:</b> The query is intercepted and its intent is mapped. A deterministic Pandas backend "
                "computes the exact answer using the filtered dashboard state. The LLM is called strictly to format the "
                "response into conversational prose.<br/>"
                "<b>LLM Call:</b> <font name='Courier' size='8.2'>Google Gemini API</font> or "
                "<font name='Courier' size='8.2'>OpenAI API</font>.<br/>"
                "<b>Payload Sent:</b> ONLY a JSON block containing pre-aggregated metrics (cohort default rates, dollar "
                "exposure, total n-count, and calculation formula).<br/>"
                "<b>Privacy Shield:</b> ZERO raw customer PII (no account IDs, names, or transaction rows) is ever "
                "transmitted across the external API network boundary.",
                cell_style,
            ),
        ],
        [
            Paragraph(
                "<b>Anomaly<br/>Detection</b><br/><br/>(Dual-Lens<br/>Outliers)",
                cell_style,
            ),
            Paragraph(
                "<b>Trigger:</b> Batch run on data<br/>refresh.<br/>"
                "<b>Module:</b> <font name='Courier' size='8.2'>src/anomaly.py</font>",
                cell_style,
            ),
            Paragraph(
                "<b>Mechanism:</b> Entirely localized, deterministic, and offline (No LLM network call). "
                "<b>Lens 1:</b> Tracks 3-month payment velocity drop. <b>Lens 2:</b> "
                "<font name='Courier' size='8.2'>sklearn.ensemble.IsolationForest</font> identifies multidimensional peer "
                "outliers based on cohort-normalized DTI, LTI, and bureau utilization matrices. Flags accounts scoring &gt;= 35.",
                cell_style,
            ),
        ],
    ]

    t_ai = Table(ai_rows, colWidths=[74.25, 123.0, 296.25])
    t_ai.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, 0), 4.5),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 4.5),
                ("TOPPADDING", (0, 1), (-1, -1), 5.0),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 5.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5.0),
            ]
        )
    )
    story.append(t_ai)

    footer_cb = _make_footer_callback(left_margin, right_margin, bottom_y=36.0, doc_title="System Architecture")
    doc.build(story, onFirstPage=footer_cb)
    logger.info("Generated %s", output_path)


def build_solution_overview_pdf(output_path: str = "docs/solution_overview.pdf"):
    """
    Builds docs/solution_overview.pdf (Strictly 1 Page, A4):
    1. Risk Analyst Guide (Dashboard Views)
    2. AI Governance Matrix (Triggers, Failure Modes & HITL)
    3. Model Performance Scorecard
    4. Top 3 Portfolio Insights & Strategic Actions
    5. Key Assumptions & IT Production Requirements
    """
    metrics = _load_latest_metrics()
    lr_m = metrics["logistic_regression"]
    lgb_m = metrics["lightgbm"]

    left_margin = 39.75
    right_margin = 39.5256  # Printable width = 516.0 pt on A4 (595.2756 pt)
    content_width = A4[0] - left_margin - right_margin  # 516.0 pt

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=31.0,
        bottomMargin=36.0,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "SolTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12.0,
        leading=14.5,
        textColor=colors.HexColor("#0F172A"),
    )
    subtitle_style = ParagraphStyle(
        "SolSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.0,
        leading=10.5,
        textColor=colors.HexColor("#3B82F6"),
    )
    th_style = ParagraphStyle(
        "SolTH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
    )
    cell_style = ParagraphStyle(
        "SolCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.75,
        textColor=colors.HexColor("#1E293B"),
    )
    bullet_style = ParagraphStyle(
        "SolBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.75,
        leftIndent=28.0,
        firstLineIndent=-9.0,
        spaceBefore=1.8,
        spaceAfter=1.8,
        textColor=colors.HexColor("#1E293B"),
    )

    story = []

    # ── Header ──
    story.append(Paragraph("SOLUTION OVERVIEW", title_style))
    story.append(Spacer(1, 3.5))
    story.append(
        Paragraph(
            "Credit Risk Portfolio Analytics | Anshul Pundhir (anshulpundhirwork@gmail.com)",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 5.5))
    story.append(HorizontalRule(content_width, thickness=1.5, color=colors.HexColor("#0F172A")))
    story.append(Spacer(1, 4.5))

    # ── 1. Risk Analyst Guide (Dashboard Views) ──
    story.append(
        _section_banner(
            "1. Risk Analyst Guide (Dashboard Views)",
            width=content_width,
            height=16.5,
            font_size=9.0,
            left_pad=4.5,
        )
    )
    story.append(Spacer(1, 1.5))

    guide_rows = [
        [
            Paragraph("<b>Dashboard View</b>", th_style),
            Paragraph("<b>Core Workflow &amp; Interactive Analytical Capabilities</b>", th_style),
        ],
        [
            Paragraph("<b>Portfolio Overview</b>", cell_style),
            Paragraph(
                "Monitors executive KPIs ($601.1M total exposure, 16.10% portfolio default rate), animated risk tier "
                "composition, interactive dimensional profiler (Loan Type, Region, Income, Employment, Age), and "
                "Income x Loan Type default heatmaps.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>Account Deep-Dive</b>", cell_style),
            Paragraph(
                "Single-loan diagnostic view. Features a predicted PD speedometer gauge, Basel risk tier badge, local "
                "<b>TreeSHAP</b> attribution waterfall of key risk factors, borrower financial profile, and actual "
                "12-month repayment DPD timeline.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>Anomaly Queue</b>", cell_style),
            Paragraph(
                "Proactive pre-bureau outlier triage queue powered by dual-lens scoring. Enables risk officers to record "
                "triage notes and persist Confirm/Dismiss decisions with instant live KPI updates.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>Strategic Insights</b>", cell_style),
            Paragraph(
                "Model governance benchmark comparing Logistic Regression vs LightGBM Champion with ROC/PR curves, "
                "feature importance ranking, and strategic risk concentration analytics.",
                cell_style,
            ),
        ],
    ]
    t_guide = Table(guide_rows, colWidths=[103.5, 412.5])
    t_guide.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, 0), 3.0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3.0),
                ("TOPPADDING", (0, 1), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 3.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
            ]
        )
    )
    story.append(t_guide)
    story.append(Spacer(1, 5.5))

    # ── 2. AI Governance Matrix (Triggers, Failure Modes & HITL) ──
    story.append(
        _section_banner(
            "2. AI Governance Matrix (Triggers, Failure Modes &amp; HITL)",
            width=content_width,
            height=16.5,
            font_size=9.0,
            left_pad=4.5,
        )
    )
    story.append(Spacer(1, 1.5))

    ai_rows = [
        [
            Paragraph("<b>AI Feature</b>", th_style),
            Paragraph("<b>Trigger</b>", th_style),
            Paragraph("<b>False Positives (FP) &amp; False Negatives (FN)</b>", th_style),
            Paragraph("<b>Human-in-the-Loop (HITL) Workflow</b>", th_style),
        ],
        [
            Paragraph("<b>Ask the Portfolio</b><br/><br/>(Grounded LLM)", cell_style),
            Paragraph("Analyst queries the chat input.", cell_style),
            Paragraph(
                "<b>FP:</b> Ambiguous term mapped to wrong metric (Mitigation: Always displays formula badge &amp; active cohort pill).<br/>"
                "<b>FN:</b> Valid query rejected as out-of-scope (Mitigation: Strict intent router with offline fallback).",
                cell_style,
            ),
            Paragraph(
                "The analyst must visually inspect the generated provenance metadata card (sample count, formula, source "
                "tables) before utilizing figures in credit committee reporting.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>Anomaly Detection</b><br/><br/>(Dual-Lens)", cell_style),
            Paragraph("Batch run on data refresh.", cell_style),
            Paragraph(
                "<b>FP:</b> Benign seasonal cash-flow delay flagged as an anomaly (Mitigation: UI shows peer cohort median context).<br/>"
                "<b>FN:</b> Gradual, peer-conforming decay missed (Mitigation: Caught by primary LightGBM PD model).",
                cell_style,
            ),
            Paragraph(
                "Interactive triage queue: Risk analyst reviews the account profile, enters investigative notes, and "
                "saves absolute Confirm/Dismiss decisions to an audit disk.",
                cell_style,
            ),
        ],
    ]
    t_ai = Table(ai_rows, colWidths=[77.25, 77.25, 180.75, 180.75])
    t_ai.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, 0), 3.0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3.0),
                ("TOPPADDING", (0, 1), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 3.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
            ]
        )
    )
    story.append(t_ai)
    story.append(Spacer(1, 5.5))

    # ── 3. Model Performance Scorecard ──
    story.append(
        _section_banner(
            "3. Model Performance Scorecard",
            width=content_width,
            height=16.5,
            font_size=9.0,
            left_pad=4.5,
        )
    )
    story.append(Spacer(1, 1.5))

    model_rows = [
        [
            Paragraph("<b>Model</b>", th_style),
            Paragraph("<b>AUC</b>", th_style),
            Paragraph("<b>KS Stat</b>", th_style),
            Paragraph("<b>Gini</b>", th_style),
            Paragraph("<b>Key Modeling Approach &amp; Validation</b>", th_style),
        ],
        [
            Paragraph("<b>Logistic Regression</b><br/><br/>(Baseline)", cell_style),
            Paragraph(f"{lr_m['auc']:.4f}", cell_style),
            Paragraph(f"{lr_m['ks_stat_pct']:.2f}%", cell_style),
            Paragraph(f"{lr_m['gini']:.4f}", cell_style),
            Paragraph(
                "Standard-scaled continuous + one-hot categorical features. L2 regularized benchmark scorecard for "
                "baseline regulatory compliance and pure linear explainability.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>LightGBM</b><br/><br/>(Champion)", cell_style),
            Paragraph(f"{lgb_m['auc']:.4f}", cell_style),
            Paragraph(f"{lgb_m['ks_stat_pct']:.2f}%", cell_style),
            Paragraph(f"{lgb_m['gini']:.4f}", cell_style),
            Paragraph(
                "Depth-constrained gradient boosted decision trees with early stopping and L1/L2 penalties. High "
                "non-linear interaction capture with robust interpretability via TreeSHAP.",
                cell_style,
            ),
        ],
    ]
    t_model = Table(model_rows, colWidths=[93.0, 51.75, 51.0, 51.75, 268.5])
    t_model.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, 0), 3.0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3.0),
                ("TOPPADDING", (0, 1), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 3.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
            ]
        )
    )
    story.append(t_model)
    story.append(Spacer(1, 5.5))

    # ── 4. Top 3 Portfolio Insights & Strategic Actions ──
    story.append(
        _section_banner(
            "4. Top 3 Portfolio Insights &amp; Strategic Actions",
            width=content_width,
            height=16.5,
            font_size=9.0,
            left_pad=4.5,
        )
    )
    story.append(Spacer(1, 1.5))

    ins_rows = [
        [
            Paragraph("<b>Strategic Finding &amp; Risk Concentration</b>", th_style),
            Paragraph("<b>Actionable 'So What' (Credit Policy Recommendation)</b>", th_style),
        ],
        [
            Paragraph(
                "<b>1. Mortgage Concentration Risk</b><br/><br/>"
                "Mortgages hold 52.3% of portfolio exposure ($314.5M) with a severe, portfolio-peak 24.65% default rate.",
                cell_style,
            ),
            Paragraph(
                "Impose hard 75% LTV origination caps, mandate semi-annual collateral reappraisals, and increase "
                "risk-weighted capital reserves for high-balance loans.",
                cell_style,
            ),
        ],
        [
            Paragraph(
                "<b>2. Monotonic Income Inversion</b><br/><br/>"
                "24.59% default rate in Low-Income (&lt;$48.5k) vs 9.70% in High-Income, representing a massive 2.5x disparity.",
                cell_style,
            ),
            Paragraph(
                "Enforce binding debt-to-income caps (max. 35% for lower-income applicants) rather than relying solely "
                "on static, historical bureau credit scores.",
                cell_style,
            ),
        ],
        [
            Paragraph(
                "<b>3. Low-Income Mortgage Squeeze</b><br/><br/>"
                "Low-Income Mortgages suffer a staggering 35.41% cross-cut default rate (&gt;2.2x portfolio baseline).",
                cell_style,
            ),
            Paragraph(
                "Discontinue automated underwriting approvals for this segment; mandate 6-month debt service escrow "
                "liquidity buffers prior to origination disbursement.",
                cell_style,
            ),
        ],
    ]
    t_ins = Table(ins_rows, colWidths=[180.75, 335.25])
    t_ins.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, 0), 3.0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3.0),
                ("TOPPADDING", (0, 1), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 3.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
            ]
        )
    )
    story.append(t_ins)
    story.append(Spacer(1, 5.5))

    # ── 5. Key Assumptions & IT Production Requirements ──
    story.append(
        _section_banner(
            "5. Key Assumptions &amp; IT Production Requirements",
            width=content_width,
            height=16.5,
            font_size=9.0,
            left_pad=4.5,
        )
    )
    story.append(Spacer(1, 3.0))

    bullets = [
        "&bull;  <b>Assumptions:</b> Synthetic loan distributions map linearly to real retail banking books; monthly repayment grain reflects true closing-cycle snapshots; external credit bureau updates incur a standard 30-day reporting lag.",
        "&bull;  <b>Automated Nightly ETL:</b> Scheduled orchestration from core banking systems (Finacle/Temenos) to a Snowflake/Databricks feature store with upstream schema validation contracts.",
        "&bull;  <b>Enterprise VPC LLM Gateway:</b> Private cloud endpoint (Google Vertex AI / Azure OpenAI) with managed secrets, zero data retention, and strict customer PII redaction filters.",
        "&bull;  <b>Persistent Audit Store &amp; MLflow:</b> A PostgreSQL relational database capturing all analyst anomaly triage decisions (for Basel III/IFRS 9 compliance), and an MLflow model registry with automated monthly retraining triggers when KS drops &gt;3% or PSI exceeds 0.20.",
    ]
    for b in bullets:
        story.append(Paragraph(b, bullet_style))

    footer_cb = _make_footer_callback(left_margin, right_margin, bottom_y=30.0, doc_title="Solution Overview")
    doc.build(story, onFirstPage=footer_cb)
    logger.info("Generated %s", output_path)


def validate_pdf_page_counts():
    """Asserts that both architecture.pdf and solution_overview.pdf are strictly 1 page each."""
    arch_pdf = DOCS_DIR / "architecture.pdf"
    sol_pdf = DOCS_DIR / "solution_overview.pdf"

    reader_arch = pypdf.PdfReader(str(arch_pdf))
    reader_sol = pypdf.PdfReader(str(sol_pdf))

    pages_arch = len(reader_arch.pages)
    pages_sol = len(reader_sol.pages)

    logger.info("Validation Check: architecture.pdf has %d page(s).", pages_arch)
    logger.info("Validation Check: solution_overview.pdf has %d page(s).", pages_sol)

    assert pages_arch == 1, f"ERROR: architecture.pdf has {pages_arch} pages, must be EXACTLY 1 page!"
    assert pages_sol == 1, f"ERROR: solution_overview.pdf has {pages_sol} pages, must be EXACTLY 1 page!"
    logger.info("PASSED: Both PDF documents are strictly and exactly 1 page!")


def generate_all_docs():
    """Generates both 1-page PDFs and asserts page counts."""
    build_architecture_pdf()
    build_solution_overview_pdf()
    validate_pdf_page_counts()


if __name__ == "__main__":
    generate_all_docs()