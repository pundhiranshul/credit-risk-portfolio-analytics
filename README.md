# 📊 Credit Risk Portfolio Analytics & AI Monitoring Platform

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-green.svg)]()
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

> An enterprise-grade credit risk monitoring dashboard featuring dual-lens anomaly detection and a zero-hallucination, grounded LLM assistant. Built for the **Credit Risk Portfolio Analytics – Take-Home Assignment (v2)**.

**Author:** Anshul Pundhir (`anshulpundhirwork@gmail.com`)  
**Repository:** `pundhiranshul/credit-risk-portfolio-analytics` 

---

## 🛠 1. Environment Specification

- **Python Version Required:** `Python 3.11` (Compatible with `3.11+`)

---

## 🚀 2. Quickstart (3-Step Execution)

Deploy the complete data pipeline, train the ML models, and launch the interactive dashboard using **exactly three commands**:

```bash
# 1. Install all pinned dependencies
pip install -r requirements.txt

# 2. Execute the ETL pipeline, train models, and generate artifacts (including 1-page PDFs)
python src/build.py

# 3. Launch the interactive monitoring dashboard
streamlit run app/app.py
```

---

## 🔑 3. LLM API Key Configuration & Fallback Engine

### Setting the API Key
To enable live LLM synthesis, set your API key in a local `.env` file (copied from `.env.example`) or input it directly via the dashboard's sidebar UI.

```bash
# Option A: Google Gemini API (Recommended)
GEMINI_API_KEY=your_gemini_api_key_here

# Option B: OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
```

### Zero-Crash Deterministic Fallback (No Key Required)
> **Resilience Standard:** If **no API key** is provided, the application will not crash or degrade. It automatically routes queries to a **Deterministic Grounded Engine (Offline Mode)**. 
> 
> In this mode, user inquiries (e.g., *"Which loan type has the highest default rate?"*) are parsed and answered using pre-computed, verified analytical tables. Every response cites exact figures, Pandas formulas, and data table origins with **zero risk of hallucination**.

---

## 📋 4. Assessment Brief Item Mapping

Every requirement detailed in the assignment brief maps directly to a specific architectural component in this repository:

| Brief Requirement | Primary Component | Implementation Highlights |
| :--- | :--- | :--- |
| **1. Data Ingestion & DQ** | `src/ingestion.py` | Joins 5 raw tables; standardizes labels; resolves missing data via cohort medians and `_isna` audit flags; retains 100% of the 14,685 loan records. |
| **2. Portfolio Analytics** | `src/analytics.py` | Profiles the portfolio across 5 dimensions (Income, Region, Age, Employment, Loan Type); delivers 5 strategic insights with actionable "So What" takeaways. |
| **3. Default Model** | `src/model.py`, `src/features.py` | Benchmarks Logistic Regression against a LightGBM Champion. Outputs AUC, KS, Gini, local TreeSHAP drivers, and formal PSI/CSI monitoring specifications. |
| **4. Interactive Dashboard** | `app/app.py` | Streamlit executive application featuring a Portfolio View, Account Deep-Dive, interactive multi-select filters, and embedded AI modules. |
| **5. AI 1: "Ask the Portfolio"** | `src/llm_assistant.py` | Grounded NLP copilot (Gemini/OpenAI/Offline). Cites exact figures; dynamically rejects out-of-scope/macroeconomic queries. |
| **6. AI 2: Anomaly Detection** | `src/anomaly.py` | Dual-lens outlier engine evaluating self-history drops and peer-group Isolation Forest clustering. Includes a HITL Confirm/Dismiss triage queue. |
| **7. Architecture Diagram** | `docs/architecture.pdf` | **Strictly 1 Page.** Details end-to-end data flow, tech stack, LLM payload specifics, and data privacy boundaries. |
| **8. Solution Overview** | `docs/solution_overview.pdf` | **Strictly 1 Page.** Executive summary covering dashboard views, AI governance (Trigger/FP/FN/HITL), model metrics, and IT production requirements. |
| **9. Unit Testing** | `tests/` | Comprehensive PyTest suite verifying row retention, model discrimination benchmarks, AI contracts, and exact PDF page-count constraints. |

---

## 🗂 5. Repository Layout

```text
├── README.md                           # Python version, 3-command run instructions, brief mapping
├── requirements.txt                    # Pinned package dependencies (e.g., pandas==2.2.3)
├── .env.example                        # Configuration template (keys only, no secret values)
├── app/
│   └── app.py                          # Streamlit dashboard entry point
├── src/                                # Core logic: Ingestion, Analytics, ML, and AI features
│   ├── ingestion.py                    # ETL, intentional DQ imputation, and master join
│   ├── features.py                     # Feature engineering, scaling, and encodings
│   ├── analytics.py                    # Portfolio profiling and strategic insights
│   ├── model.py                        # Baseline & champion models, SHAP, and drift monitoring
│   ├── anomaly.py                      # Dual-lens anomaly detection and triage queue
│   ├── llm_assistant.py                # Grounded Q&A engine (Gemini / OpenAI / Offline)
│   ├── generate_docs.py                # Automated 1-page PDF generator and validator
│   └── build.py                        # Single-command end-to-end pipeline orchestrator
├── data/
│   └── raw/                            # The 5 provided CSVs & Data Dictionary
│       ├── customers.csv
│       ├── loan_accounts.csv
│       ├── bureau_credit.csv
│       ├── repayment_history.csv
│       ├── collections_events.csv
│       └── DATA_DICTIONARY.md
├── docs/
│   ├── architecture.pdf                # Exactly 1 page: Pipeline, tools, LLM calls
│   └── solution_overview.pdf           # Exactly 1 page: Views, AI governance, metrics, IT specs
└── tests/                              # Automated test suite (32 unit tests)
    ├── test_ingestion.py               # Verifies 0 dropped rows and DQ resolution
    ├── test_analytics.py               # Verifies profiling dimensions and insights
    ├── test_model.py                   # Verifies model discrimination benchmarks (AUC/KS)
    ├── test_ai_features.py             # Verifies grounded assistant constraints and anomaly queue
    └── test_docs.py                    # Verifies both PDFs strictly adhere to 1-page limits
```

*(Note: The `data/processed/` directory containing transformed parquet datasets, trained model binaries, and analytics caches is built deterministically via `python src/build.py` and is intentionally git-ignored to maintain repository hygiene.)*

---

## ✅ 6. Verification & Automated Testing

To verify the integrity of the pipeline, data transformations, and 1-page PDF constraints, run the automated test suite:

```bash
pytest tests/ -v
```