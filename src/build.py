"""
Master Automated Build Script
------------------------------
Executes the full end-to-end credit risk pipeline:
1. Ingestion & Quality Cleaning (load 5 raw tables, resolve defects, master join).
2. Portfolio Analytics (profiling across dimensions, cross-cuts, 5 strategic insights).
3. Default Modeling (train Logistic Regression baseline & LightGBM champion, compute AUC, KS, Gini, SHAP, PSI).
4. Anomaly Detection (dual-lens self-history and peer leverage outlier queue generation).

Run:
    python src/build.py

Author: pundhiranshul <anshulpundhirwork@gmail.com>
"""

import sys
import time
import logging
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build")

from src.ingestion import run_ingestion_pipeline
from src.analytics import run_portfolio_analytics
from src.model import run_modeling_pipeline
from src.anomaly import build_anomaly_review_queue
from src.generate_docs import generate_all_docs


def run_full_build():
    """Executes all pipeline stages sequentially with timing logs."""
    start_total = time.time()
    logger.info("=" * 60)
    logger.info("STARTING CREDIT RISK PORTFOLIO ANALYTICS FULL BUILD")
    logger.info("Author: pundhiranshul <anshulpundhirwork@gmail.com>")
    logger.info("=" * 60)

    # Stage 1: Ingestion & Data Quality
    t0 = time.time()
    logger.info("\n>>> STAGE 1: Data Ingestion & Quality Engineering...")
    master_df = run_ingestion_pipeline()
    logger.info("Stage 1 completed in %.2f seconds (Shape: %s).", time.time() - t0, master_df.shape)

    # Stage 2: Portfolio Analytics & Strategic Insights
    t1 = time.time()
    logger.info("\n>>> STAGE 2: Portfolio Analytics & Profiling...")
    analytics_data = run_portfolio_analytics()
    logger.info("Stage 2 completed in %.2f seconds (5 strategic insights generated).", time.time() - t1)

    # Stage 3: Default Prediction Model & Monitoring
    t2 = time.time()
    logger.info("\n>>> STAGE 3: Default Prediction Modeling (Baseline & Champion)...")
    eval_results = run_modeling_pipeline()
    lgb_m = eval_results["metrics"]["lightgbm"]
    logger.info(
        "Stage 3 completed in %.2f seconds (Champion LightGBM: AUC=%.4f, KS=%.2f%%, Gini=%.4f).",
        time.time() - t2, lgb_m["auc"], lgb_m["ks_stat_pct"], lgb_m["gini"]
    )

    # Stage 4: Anomaly Detection Queue
    t3 = time.time()
    logger.info("\n>>> STAGE 4: Dual-Lens Anomaly Detection Queue Generation...")
    queue_df = build_anomaly_review_queue()
    flagged_count = int(queue_df["is_anomaly_flagged"].sum())
    logger.info(
        "Stage 4 completed in %.2f seconds (%d accounts flagged for review).",
        time.time() - t3, flagged_count
    )

    # Stage 5: PDF Documentation & Page Count Validation
    t4 = time.time()
    logger.info("\n>>> STAGE 5: Generating and Validating 1-Page PDFs (docs/)...")
    generate_all_docs()
    logger.info("Stage 5 completed in %.2f seconds (both PDFs verified strictly 1 page).", time.time() - t4)

    total_time = time.time() - start_total
    logger.info("\n" + "=" * 60)
    logger.info("MASTER BUILD COMPLETED SUCCESSFULLY in %.2f seconds!", total_time)
    logger.info("All processed artifacts, models, reports, and review queues are ready.")
    logger.info("Dashboard can now be launched via: streamlit run app/app.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_full_build()
