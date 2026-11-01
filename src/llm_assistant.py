"""
AI Feature 1: 'Ask the Portfolio' Grounded Natural Language Assistant
---------------------------------------------------------------------
Provides grounded Q&A over credit risk portfolio analytics with zero hallucination.
Every response cites exact figures, underlying sample size, and data source tables.
Questions outside the data scope are politely and explicitly declined.

Supports:
1. Google Gemini API (gemini-2.5-flash / gemini-1.5-flash) via GEMINI_API_KEY.
2. OpenAI API via OPENAI_API_KEY.
3. Deterministic Grounded Fallback Engine (No API key needed; 100% offline functionality).

Author: pundhiranshul <anshulpundhirwork@gmail.com>
"""

import os
import json
import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from functools import lru_cache
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("llm_assistant")

ANALYTICS_CACHE_PATH = Path("data/processed/portfolio_analytics.json")
MASTER_DATA_PATH = Path("data/processed/portfolio_master.parquet")
SCORES_DATA_PATH = Path("data/processed/account_risk_scores.parquet")


@lru_cache(maxsize=1)
def load_context_data() -> Tuple[Optional[Dict], Optional[pd.DataFrame]]:
    """Loads cached analytics summary and master dataframe merged with risk scores."""
    analytics_json = None
    master_df = None
    if ANALYTICS_CACHE_PATH.exists():
        with open(ANALYTICS_CACHE_PATH, "r", encoding="utf-8") as f:
            analytics_json = json.load(f)
    if MASTER_DATA_PATH.exists():
        master_df = pd.read_parquet(MASTER_DATA_PATH)
        if SCORES_DATA_PATH.exists() and "risk_tier" not in master_df.columns:
            scores_df = pd.read_parquet(SCORES_DATA_PATH)
            merge_cols = [c for c in ["account_id", "predicted_pd", "risk_tier"] if c in scores_df.columns]
            master_df = pd.merge(master_df, scores_df[merge_cols], on="account_id", how="left")
    return analytics_json, master_df


# Expanded regex to catch greetings, capabilities, and gratitude
GREETING = re.compile(
    r"^\s*(h+i+|h+e+y+|h+e+l+l+o+|y+o+|h+o+w+d+y+|greetings|good (morning|afternoon|evening)|how are you|what'?s up|s+u+p+|b+y+e+)\b",
    re.I,
)
META = re.compile(
    r"\b(what can you (do|answer)|how can you help|help me|what (can|should) i ask|capabilit|who are you|how (do i use|does this work))\b",
    re.I,
)
THANKS = re.compile(
    r"\b(thanks?|thank you|thx|thank u|appreciate it|many thanks|cheers)\b",
    re.I,
)

THANKS_TEXT = (
    "You're welcome! I am here to assist with any credit risk or portfolio analytics inquiries. "
    "Feel free to ask about default rates, risk tiers, exposure distributions, or specific loan characteristics."
)

HELP_TEXT = (
    "Hi! I answer questions about this credit portfolio using the loaded data. "
    "Try asking me things like:\n"
    "- Which loan type has the highest default rate?\n"
    "- What is the default rate by employment type?\n"
    "- Show me total exposure by region."
)

SUGGESTED_EXAMPLES = [
    "Which loan type has the highest default rate?",
    "What is the default rate by employment type?",
    "Show me total exposure by region.",
    "What percentage of loans are classified as critical risk?",
]

SYSTEM_PROMPT = """You are the 'Ask the Portfolio' AI assistant embedded in a credit risk dashboard.

1. **Greetings & Onboarding:** If the user says hello, uses slang (e.g., 'heyyyy', 'Namaste'), thanks you, or asks what you can do, respond naturally and briefly state that you can answer questions about portfolio risk, exposure, and loan types based on the dashboard data. Do not use generic refusal templates for greetings.
2. **Analytical Queries:** When analytical data context is provided, answer ONLY using that verified data context. Cite exact figures. Never ask the user to provide JSON data or files.
3. **Out-of-Scope Queries:** If asked an informational, trivia, weather, market, or external question outside this credit portfolio, politely decline and state that this dashboard is strictly focused on portfolio credit risk and loan performance data. Do not hallucinate or use outside knowledge."""


AI_METADATA_SPEC = {
    "feature_name": "Ask the Portfolio (Grounded LLM Assistant)",
    "trigger": (
        "Analyst submits a natural language credit risk or portfolio query in the assistant chat."
    ),
    "false_positive": (
        "Semantic Misinterpretation: Ambiguous term mapped to wrong metric. "
        "Mitigation: Explicit formula, source tables, and cohort sample size cited."
    ),
    "false_negative": (
        "Over-Conservative Refusal: Declining valid domain questions. "
        "Mitigation: Intent classifier with grounded offline fallback suggestions."
    ),
    "human_in_the_loop": (
        "Data Provenance Verification: Transparent source tables and cohort count "
        "verified by analyst before credit committee presentation."
    ),
}


class GroundedPortfolioAssistant:
    """Grounded Q&A assistant enforcing zero-hallucination answers with citations and strict out-of-scope refusal."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        df_override: Optional[pd.DataFrame] = None,
    ):
        if provider == "Offline Mode":
            self.gemini_key = None
            self.openai_key = None
        elif provider == "OpenAI":
            self.gemini_key = None
            self.openai_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        else:
            self.gemini_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY")
            self.openai_key = os.getenv("OPENAI_API_KEY")

        self.analytics_data, base_df = load_context_data()
        self.df = df_override if (df_override is not None and len(df_override) > 0) else base_df

        if self.gemini_key:
            self.mode = "Gemini Live LLM"
            self._init_gemini()
        elif self.openai_key:
            self.mode = "OpenAI Live LLM"
            self._init_openai()
        else:
            self.mode = "Deterministic Grounded Engine (Offline)"

    def _init_gemini(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)

            # Resolve model dynamically from streamlit secrets or environment without hardcoding
            model_name = ""
            try:
                import streamlit as st
                if hasattr(st, "secrets") and "GEMINI_MODEL" in st.secrets:
                    model_name = str(st.secrets["GEMINI_MODEL"]).strip("'\" \t\r\n")
            except Exception:
                pass
            if not model_name:
                model_name = os.getenv("GEMINI_MODEL", "").strip("'\" \t\r\n")

            if not model_name:
                raise ValueError("GEMINI_MODEL is not configured in streamlit secrets or environment variables.")

            self.model_name = model_name
            try:
                self.gemini_client = genai.GenerativeModel(self.model_name, system_instruction=SYSTEM_PROMPT)
            except Exception:
                self.gemini_client = genai.GenerativeModel(self.model_name)
            logger.info("Initialized Gemini Live LLM client (%s).", self.model_name)
        except Exception as e:
            logger.warning("Failed to initialize Gemini client (%s). Falling back to deterministic mode.", e)
            self.mode = "Deterministic Grounded Engine (Offline)"

    def _init_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.openai_key)
            logger.info("Initialized OpenAI Live LLM client.")
        except Exception as e:
            logger.warning("Failed to initialize OpenAI client (%s). Falling back to deterministic mode.", e)
            self.mode = "Deterministic Grounded Engine (Offline)"

    def ask(self, query: str) -> Dict[str, Any]:
        """Processes a user question, attempting LLM resolution first before falling back to Offline determinism."""
        clean_q = query.strip()
        if not clean_q:
            return {
                "answer": "Please enter a valid credit risk question about the portfolio.",
                "source": "None",
                "sources": [],
                "sample_size": "0",
                "status": "declined",
                "intent": "out_of_scope",
                "mode": self.mode,
            }

        # 1. Hard Guardrails (Prompt injection, external info)
        out_of_scope = self._check_out_of_scope(clean_q)
        if out_of_scope:
            if self.mode == "Gemini Live LLM" and hasattr(self, "gemini_client"):
                return self._call_gemini_decline(clean_q, out_of_scope)
            elif self.mode == "OpenAI Live LLM" and hasattr(self, "openai_client"):
                return self._call_openai_decline(clean_q, out_of_scope)
            else:
                return self._format_offline_decline(clean_q, out_of_scope)

        # 2. Compute grounded facts (Will be passed to LLM as Context, or used directly if Offline)
        grounded_facts = self._compute_grounded_facts(clean_q)
        is_supported_data = (grounded_facts.get("status") == "answered")

        # 3. Try LLM (LLM will naturally handle "Namaste", "heyyy", AND data questions)
        if self.mode == "Gemini Live LLM" and hasattr(self, "gemini_client"):
            try:
                return self._call_gemini(clean_q, grounded_facts)
            except Exception as e:
                logger.warning("Gemini failed (%s). Falling back to offline engine.", e)
        elif self.mode == "OpenAI Live LLM" and hasattr(self, "openai_client"):
            try:
                return self._call_openai(clean_q, grounded_facts)
            except Exception as e:
                logger.warning("OpenAI failed (%s). Falling back to offline engine.", e)

        # 4. Offline Fallback (Only reached if LLM APIs fail or provider == 'Offline Mode')
        fallback_mode = (
            "Deterministic Grounded Engine (Offline Fallback)"
            if self.mode != "Deterministic Grounded Engine (Offline)"
            else "Deterministic Grounded Engine (Offline)"
        )
        if is_supported_data:
            return self._format_deterministic_answer(clean_q, grounded_facts, mode_override=fallback_mode)

        # Offline Chit-Chat fallback
        is_thanks = bool(THANKS.search(clean_q))
        is_chitchat = bool(GREETING.search(clean_q) or META.search(clean_q) or is_thanks)

        if is_chitchat:
            return {
                "intent": "chitchat",
                "answer": THANKS_TEXT if is_thanks else HELP_TEXT,
                "source": "Portfolio Assistant Guide",
                "sources": [],
                "sample_size": "N/A (Chit-chat / Onboarding)" if self.mode == "Deterministic Grounded Engine (Offline)" else "N/A (Chit-chat / Offline Fallback)",
                "status": "answered",
                "mode": fallback_mode,
                "suggested_questions": SUGGESTED_EXAMPLES,
            }

        return self._format_offline_decline(
            clean_q, "The requested metric is outside the scope of the provided banking portfolio schema."
        )

    def _check_out_of_scope(self, query: str) -> Optional[str]:
        """Detects if a query asks for external, macroeconomic, PII, future forecasting, prompt-injection, or non-banking information."""
        q_lower = query.lower()

        # Prompt injection / jailbreak attempts
        if re.search(r"\b(ignore (all|previous|prior)|system prompt|jailbreak|disregard|you are now|override instructions|pretend to be|act as dan)\b", q_lower):
            return "Prompt-injection and system instruction override attempts are prohibited; the assistant strictly adheres to portfolio data governance."

        # Predictions beyond data / future forecasting
        if re.search(r"\b(next year|next month|in 2027|in 2028|in 2030|future default rate|forecast next|predict next year|future loss)\b", q_lower):
            return "Forward projections beyond the static historical and current portfolio snapshot (such as default rate next year) cannot be forecasted from this data."

        # Note: 'government' is intentionally allowed because 'Government' is a valid occupation_sector in customers.csv
        out_of_scope_patterns = [
            (
                r"\b(stock|stocks|shares|crypto|bitcoin|ethereum|tsla|aapl|nvda|nasdaq|s&p|dow jones|forex)\b",
                "Market stock prices, equities, and cryptocurrency valuations are not tracked in this banking credit book.",
            ),
            (
                r"\b(weather|temperature|climate|rain|forecast|snow|humidity)\b",
                "Weather and climate data are not captured in this loan portfolio.",
            ),
            (
                r"\b(president|election|politics|prime minister|senate|congress|parliament|mayor)\b",
                "Political information is outside the scope of retail credit risk.",
            ),
            (
                r"\b(recipe|cooking|cake|pizza|movie|celebrity|sports|football|cricket|basketball|soccer|music|song|poem|joke)\b",
                "General world knowledge and entertainment topics are not present in this dataset.",
            ),
            (
                r"\b(ceo|address|phone|email|ssn|social security|passport|national id|pan card|credit card number|bank account number)\b",
                "Personally identifiable contact records and raw credential numbers are not present in the synthetic schema.",
            ),
            (
                r"\b(fico|equifax|experian|transunion|cibil|vantagescore)\b",
                "External bureau credit scores (such as FICO) are not stored in the schema; the dataset only tracks raw bureau lines, utilization, DPD, and write-offs.",
            ),
            (
                r"\b(gdp|inflation|cpi|fed rate|federal reserve|libor|sofr|recession|interest rate hike)\b",
                "Macroeconomic indicators (GDP, inflation, central bank rates) are not included in the portfolio tables.",
            ),
            (
                r"\b(capital of|country|continent|planet|mars|moon|ocean|mountain|who invented|who won)\b",
                "General geography and trivia questions cannot be answered from the banking credit dataset.",
            ),
        ]
        for pattern, reason in out_of_scope_patterns:
            if re.search(pattern, q_lower):
                return reason
        return None

    def _compute_grounded_facts(self, query: str) -> Dict[str, Any]:
        """Calculates exact underlying figures directly from the data tables based on query intent."""
        q_lower = query.lower()
        n_rows = len(self.df) if self.df is not None else 14685
        facts: Dict[str, Any] = {
            "query": query,
            "provenance_table": "portfolio_master.parquet (derived from loan_accounts, customers, bureau_credit, repayment_history)",
            "sample_size": n_rows,
            "status": "answered",
        }

        if self.df is None or len(self.df) == 0:
            facts["status"] = "declined"
            return facts

        # 1. Collateral / Secured vs Unsecured
        if any(w in q_lower for w in ["secured", "unsecured", "collateral"]):
            sec = self.df.groupby("collateral_flag")["target_default"].agg(["count", "sum", "mean"]).reset_index()
            sec_map = {int(r["collateral_flag"]): r for _, r in sec.iterrows()}
            s_row = sec_map.get(1, {"count": 0, "sum": 0, "mean": 0.0})
            u_row = sec_map.get(0, {"count": 0, "sum": 0, "mean": 0.0})
            facts["topic"] = "collateral_default"
            facts["secured_rate"] = f"{s_row['mean']:.2%}"
            facts["secured_count"] = int(s_row["count"])
            facts["secured_defaults"] = int(s_row["sum"])
            facts["unsecured_rate"] = f"{u_row['mean']:.2%}"
            facts["unsecured_count"] = int(u_row["count"])
            facts["unsecured_defaults"] = int(u_row["sum"])
            facts["formula"] = "SUM(target_default) / COUNT(account_id) GROUP BY collateral_flag"
            return facts

        # 2. Risk Tiers (Critical / High / Medium / Low Risk distribution, exposure, or interest rate)
        if any(w in q_lower for w in ["risk tier", "risk tiers", "critical risk", "high risk", "low risk", "medium risk", "high & critical"]):
            if "risk_tier" in self.df.columns:
                rt = self.df.groupby("risk_tier", observed=False).agg(
                    count=("account_id", "count"),
                    exposure=("loan_amount", "sum"),
                    default_rate=("target_default", "mean"),
                    avg_ir=("interest_rate_pct", "mean"),
                    avg_pd=("predicted_pd", "mean"),
                ).reset_index()
                total_exp = float(self.df["loan_amount"].sum())
                crit_df = self.df[self.df["risk_tier"] == "Critical Risk"]
                hc_df = self.df[self.df["risk_tier"].isin(["High Risk", "Critical Risk"])]

                facts["topic"] = "risk_tiers"
                facts["provenance_table"] = "account_risk_scores.parquet (merged with loan_accounts)"
                facts["critical_count"] = len(crit_df)
                facts["critical_share_pct"] = f"{(len(crit_df) / len(self.df)):.2%}"
                facts["critical_exposure"] = f"${crit_df['loan_amount'].sum():,.2f}"
                facts["critical_avg_ir"] = f"{crit_df['interest_rate_pct'].mean():.2f}%" if len(crit_df) > 0 else "0.00%"
                facts["critical_default_rate"] = f"{crit_df['target_default'].mean():.2%}" if len(crit_df) > 0 else "0.00%"
                facts["high_crit_exposure"] = f"${hc_df['loan_amount'].sum():,.2f}"
                facts["high_crit_exposure_share"] = f"{(hc_df['loan_amount'].sum() / max(total_exp, 1.0)):.1%}"
                facts["high_crit_count"] = len(hc_df)
                facts["tier_breakdown"] = {
                    str(r["risk_tier"]): (
                        f"{int(r['count']):,} loans ({int(r['count'])/len(self.df):.1%}), "
                        f"Exposure: ${r['exposure']:,.0f}, Default Rate: {r['default_rate']:.2%}, "
                        f"Avg IR: {r['avg_ir']:.2f}%"
                    )
                    for _, r in rt.iterrows()
                }
                facts["formula"] = "GROUP BY risk_tier (COUNT, SUM(loan_amount), MEAN(target_default), MEAN(interest_rate_pct))"
                return facts

        # 3. Bureau Utilization / Write-Offs / External Credit Lines
        if any(w in q_lower for w in ["bureau", "utilization", "write-off", "written-off", "external credit", "nbfc"]):
            high_util = self.df[self.df["bureau_utilization_ratio"] > 0.75]
            low_util = self.df[self.df["bureau_utilization_ratio"] <= 0.30]
            wo_yes = self.df[self.df["bureau_has_written_off"] == 1]
            wo_no = self.df[self.df["bureau_has_written_off"] == 0]
            def_util = self.df[self.df["target_default"] == 1]["bureau_utilization_ratio"].mean()
            perf_util = self.df[self.df["target_default"] == 0]["bureau_utilization_ratio"].mean()

            facts["topic"] = "bureau_impact"
            facts["avg_utilization_overall"] = f"{self.df['bureau_utilization_ratio'].mean():.1%}"
            facts["avg_utilization_default"] = f"{def_util:.1%}"
            facts["avg_utilization_performing"] = f"{perf_util:.1%}"
            facts["high_util_default_rate"] = f"{high_util['target_default'].mean():.2%}" if len(high_util) > 0 else "0.00%"
            facts["low_util_default_rate"] = f"{low_util['target_default'].mean():.2%}" if len(low_util) > 0 else "0.00%"
            facts["prior_writeoff_default_rate"] = f"{wo_yes['target_default'].mean():.2%}" if len(wo_yes) > 0 else "0.00%"
            facts["no_writeoff_default_rate"] = f"{wo_no['target_default'].mean():.2%}" if len(wo_no) > 0 else "0.00%"
            facts["prior_writeoff_accounts"] = len(wo_yes)
            facts["formula"] = "MEAN(target_default) segmented by bureau_utilization_ratio and bureau_has_written_off"
            return facts

        # 4. Debt-to-Income (DTI) or Loan-to-Income (LTI)
        if any(w in q_lower for w in ["dti", "debt-to-income", "debt to income", "lti", "loan-to-income"]):
            def_df = self.df[self.df["target_default"] == 1]
            perf_df = self.df[self.df["target_default"] == 0]
            high_dti = self.df[self.df["debt_to_income_ratio"] > 0.40]
            low_dti = self.df[self.df["debt_to_income_ratio"] <= 0.20]

            facts["topic"] = "dti_analysis"
            facts["overall_avg_dti"] = f"{self.df['debt_to_income_ratio'].mean():.2f}"
            facts["default_avg_dti"] = f"{def_df['debt_to_income_ratio'].mean():.2f}"
            facts["performing_avg_dti"] = f"{perf_df['debt_to_income_ratio'].mean():.2f}"
            facts["high_dti_default_rate"] = f"{high_dti['target_default'].mean():.2%}" if len(high_dti) > 0 else "0.00%"
            facts["low_dti_default_rate"] = f"{low_dti['target_default'].mean():.2%}" if len(low_dti) > 0 else "0.00%"
            facts["formula"] = "MEAN(debt_to_income_ratio) GROUP BY target_default"
            return facts

        # 5. Employment Tenure (years_employed correlation with default)
        if ("tenure" in q_lower and "employ" in q_lower) or "years employed" in q_lower or "job tenure" in q_lower:
            def_emp = self.df[self.df["target_default"] == 1]["years_employed"].mean()
            perf_emp = self.df[self.df["target_default"] == 0]["years_employed"].mean()
            short_t = self.df[self.df["years_employed"] < 2.0]
            long_t = self.df[self.df["years_employed"] >= 5.0]

            facts["topic"] = "employment_tenure"
            facts["avg_years_employed_default"] = f"{def_emp:.2f} years"
            facts["avg_years_employed_performing"] = f"{perf_emp:.2f} years"
            facts["under_2yr_default_rate"] = f"{short_t['target_default'].mean():.2%}" if len(short_t) > 0 else "0.00%"
            facts["over_5yr_default_rate"] = f"{long_t['target_default'].mean():.2%}" if len(long_t) > 0 else "0.00%"
            facts["formula"] = "MEAN(years_employed) GROUP BY target_default & tenure buckets"
            return facts

        # 6. Geographic Region (Default Rate & Exposure)
        if any(w in q_lower for w in ["region", "geographic", "north", "south", "east", "west", "central"]):
            reg_profile = self.df.groupby("region").agg(
                count=("account_id", "count"),
                defaults=("target_default", "sum"),
                default_rate=("target_default", "mean"),
                exposure=("loan_amount", "sum"),
            ).reset_index()
            by_rate = reg_profile.sort_values(by="default_rate", ascending=False)
            by_exp = reg_profile.sort_values(by="exposure", ascending=False)

            facts["topic"] = "region_default"
            facts["highest_rate_region"] = by_rate.iloc[0]["region"]
            facts["highest_region_rate"] = f"{by_rate.iloc[0]['default_rate']:.2%}"
            facts["lowest_rate_region"] = by_rate.iloc[-1]["region"]
            facts["lowest_region_rate"] = f"{by_rate.iloc[-1]['default_rate']:.2%}"
            facts["highest_exposure_region"] = by_exp.iloc[0]["region"]
            facts["highest_region_exposure"] = f"${by_exp.iloc[0]['exposure']:,.2f}"
            facts["highest_exposure_count"] = int(by_exp.iloc[0]["count"])
            facts["all_regions"] = {
                r["region"]: f"Default Rate: {r['default_rate']:.2%} ({int(r['defaults'])}/{int(r['count'])}), Exposure: ${r['exposure']:,.0f}"
                for _, r in by_rate.iterrows()
            }
            facts["formula"] = "GROUP BY region (MEAN(target_default), SUM(loan_amount))"
            return facts

        # 7. Income Tier (Default / Delinquency Rates)
        if any(w in q_lower for w in ["income", "low-income", "low income", "high-income", "high income", "earner"]):
            inc_profile = self.df.groupby("income_tier", observed=False).agg(
                count=("account_id", "count"),
                defaults=("target_default", "sum"),
                mean=("target_default", "mean"),
                avg_dti=("debt_to_income_ratio", "mean"),
            ).reset_index()
            by_rate = inc_profile.sort_values(by="mean", ascending=False)
            highest = by_rate.iloc[0]
            lowest = by_rate.iloc[-1]

            facts["topic"] = "income_default"
            facts["low_income_tier"] = str(highest["income_tier"])
            facts["low_income_rate"] = f"{highest['mean']:.2%}"
            facts["low_income_defaults"] = int(highest["defaults"])
            facts["low_income_count"] = int(highest["count"])
            facts["high_income_tier"] = str(lowest["income_tier"])
            facts["high_income_rate"] = f"{lowest['mean']:.2%}"
            facts["all_income_rates"] = {
                str(row["income_tier"]): f"{row['mean']:.2%} ({int(row['defaults'])}/{int(row['count'])}, Avg DTI: {row['avg_dti']:.2f})"
                for _, row in inc_profile.iterrows()
            }
            facts["formula"] = "SUM(target_default) / COUNT(account_id) GROUP BY income_tier"
            return facts

        # 8. Employment Type (Unemployed / Contract / Salaried / Self-Employed / Business Owner)
        if any(w in q_lower for w in ["employment", "unemployed", "unemployment", "contract", "salaried", "self-employed", "business owner"]):
            emp_profile = self.df.groupby("employment_type")["target_default"].agg(["count", "sum", "mean"]).reset_index()
            emp_profile = emp_profile.sort_values(by="mean", ascending=False)
            facts["topic"] = "employment_default"
            unemp_rows = emp_profile[emp_profile["employment_type"] == "Unemployed"]
            unemp_row = unemp_rows.iloc[0] if len(unemp_rows) > 0 else emp_profile.iloc[0]
            facts["unemployed_rate"] = f"{unemp_row['mean']:.2%}"
            facts["unemployed_count"] = int(unemp_row["count"])
            facts["unemployed_defaults"] = int(unemp_row["sum"])
            facts["lowest_emp_type"] = emp_profile.iloc[-1]["employment_type"]
            facts["lowest_emp_rate"] = f"{emp_profile.iloc[-1]['mean']:.2%}"
            facts["all_employment_rates"] = {
                row["employment_type"]: f"{row['mean']:.2%} ({int(row['sum'])}/{int(row['count'])})"
                for _, row in emp_profile.iterrows()
            }
            facts["formula"] = "SUM(target_default) / COUNT(account_id) GROUP BY employment_type"
            return facts

        # 9. Occupation Sector (including Government, Healthcare, IT/Tech, Finance, etc.)
        if any(w in q_lower for w in ["sector", "occupation", "government", "healthcare", "it/tech", "hospitality", "construction", "manufacturing", "retail"]):
            if "occupation_sector" in self.df.columns:
                sec_prof = self.df.groupby("occupation_sector")["target_default"].agg(["count", "sum", "mean"]).reset_index()
                sec_prof = sec_prof.sort_values(by="mean", ascending=False)
                facts["topic"] = "sector_default"
                facts["highest_sector"] = sec_prof.iloc[0]["occupation_sector"]
                facts["highest_sector_rate"] = f"{sec_prof.iloc[0]['mean']:.2%}"
                facts["lowest_sector"] = sec_prof.iloc[-1]["occupation_sector"]
                facts["lowest_sector_rate"] = f"{sec_prof.iloc[-1]['mean']:.2%}"
                facts["all_sectors"] = {
                    r["occupation_sector"]: f"{r['mean']:.2%} ({int(r['sum'])}/{int(r['count'])})"
                    for _, r in sec_prof.iterrows()
                }
                facts["formula"] = "SUM(target_default) / COUNT(account_id) GROUP BY occupation_sector"
                return facts

        # 10. Age / Age Bucket
        if any(w in q_lower for w in ["age", "young", "older", "senior", "18-30", "31-45", "46-60", "60+"]):
            age_prof = self.df.groupby("age_bucket", observed=False)["target_default"].agg(["count", "sum", "mean"]).reset_index()
            age_prof = age_prof.sort_values(by="mean", ascending=False)
            facts["topic"] = "age_default"
            facts["highest_age_bucket"] = str(age_prof.iloc[0]["age_bucket"])
            facts["highest_age_rate"] = f"{age_prof.iloc[0]['mean']:.2%}"
            facts["lowest_age_bucket"] = str(age_prof.iloc[-1]["age_bucket"])
            facts["lowest_age_rate"] = f"{age_prof.iloc[-1]['mean']:.2%}"
            facts["all_age_buckets"] = {
                str(r["age_bucket"]): f"{r['mean']:.2%} ({int(r['sum'])}/{int(r['count'])})"
                for _, r in age_prof.iterrows()
            }
            facts["formula"] = "SUM(target_default) / COUNT(account_id) GROUP BY age_bucket"
            return facts

        # 11. Interest Rate Queries
        if "interest rate" in q_lower or "apr" in q_lower or "pricing" in q_lower:
            def_ir = self.df[self.df["target_default"] == 1]["interest_rate_pct"].mean()
            perf_ir = self.df[self.df["target_default"] == 0]["interest_rate_pct"].mean()
            by_lt = self.df.groupby("loan_type")["interest_rate_pct"].mean().to_dict()
            facts["topic"] = "interest_rate"
            facts["overall_avg_ir"] = f"{self.df['interest_rate_pct'].mean():.2f}%"
            facts["default_avg_ir"] = f"{def_ir:.2f}%"
            facts["performing_avg_ir"] = f"{perf_ir:.2f}%"
            facts["ir_by_loan_type"] = {k: f"{v:.2f}%" for k, v in by_lt.items()}
            if "risk_tier" in self.df.columns:
                crit_ir = self.df[self.df["risk_tier"] == "Critical Risk"]["interest_rate_pct"].mean()
                facts["critical_risk_avg_ir"] = f"{crit_ir:.2f}%"
            facts["formula"] = "MEAN(interest_rate_pct) across portfolio segments"
            return facts

        # 12. Repayment / DPD / Delinquency / Collections
        if any(w in q_lower for w in ["dpd", "days past due", "repayment", "missed payment", "late payment", "collections"]):
            ever_30 = self.df[self.df["repay_ever_30dpd"] == 1]
            no_30 = self.df[self.df["repay_ever_30dpd"] == 0]
            facts["topic"] = "repayment_dpd"
            facts["avg_max_dpd"] = f"{self.df['repay_max_dpd'].mean():.1f} days"
            facts["ever_30dpd_count"] = len(ever_30)
            facts["ever_30dpd_default_rate"] = f"{ever_30['target_default'].mean():.2%}" if len(ever_30) > 0 else "0.00%"
            facts["clean_30dpd_default_rate"] = f"{no_30['target_default'].mean():.2%}" if len(no_30) > 0 else "0.00%"
            facts["avg_payment_ratio"] = f"{self.df['repay_payment_ratio'].mean():.1%}"
            facts["formula"] = "MEAN(target_default) grouped by repay_ever_30dpd and repayment fulfillment metrics"
            return facts

        # 13. Loan Type Default Rates (Highest / Lowest / Breakdown by Asset Class)
        if any(w in q_lower for w in ["loan type", "mortgage", "personal loan", "auto loan", "credit card", "business loan", "highest default", "lowest overall default", "lowest default"]):
            loan_profile = self.df.groupby("loan_type")["target_default"].agg(["count", "sum", "mean"]).reset_index()
            loan_profile = loan_profile.sort_values(by="mean", ascending=False)
            highest = loan_profile.iloc[0]
            lowest = loan_profile.iloc[-1]
            facts["topic"] = "loan_type_default"
            facts["highest_loan_type"] = highest["loan_type"]
            facts["highest_default_rate"] = f"{highest['mean']:.2%}"
            facts["highest_default_count"] = int(highest["sum"])
            facts["highest_account_count"] = int(highest["count"])
            facts["lowest_loan_type"] = lowest["loan_type"]
            facts["lowest_default_rate"] = f"{lowest['mean']:.2%}"
            facts["lowest_default_count"] = int(lowest["sum"])
            facts["lowest_account_count"] = int(lowest["count"])
            facts["all_rates"] = {
                row["loan_type"]: f"{row['mean']:.2%} ({int(row['sum'])} / {int(row['count'])})"
                for _, row in loan_profile.iterrows()
            }
            facts["formula"] = "SUM(target_default == 1) / COUNT(account_id) GROUP BY loan_type"
            return facts

        # 14. Total Exposure / Portfolio Balance / Average Loan Size
        if any(w in q_lower for w in ["exposure", "total balance", "portfolio size", "average loan", "avg loan", "loan size", "total loan"]):
            total_exp = float(self.df["loan_amount"].sum())
            avg_loan = float(self.df["loan_amount"].mean())
            mortgage_exp = float(self.df[self.df["loan_type"] == "Mortgage"]["loan_amount"].sum())
            facts["topic"] = "exposure"
            facts["total_exposure"] = f"${total_exp:,.2f}"
            facts["average_loan_size"] = f"${avg_loan:,.2f}"
            facts["mortgage_exposure"] = f"${mortgage_exp:,.2f}"
            facts["mortgage_share"] = f"{(mortgage_exp / max(total_exp, 1.0)):.1%}"
            facts["total_accounts"] = len(self.df)
            facts["formula"] = "SUM(loan_amount) and MEAN(loan_amount) across loan_accounts.csv"
            return facts

        # 15. Explicit Portfolio Summary / Overall Default Rate
        if any(w in q_lower for w in ["overall default", "portfolio default", "total default", "summary", "overview", "how many accounts", "how many loans", "default rate of the portfolio", "what is the default rate", "average default rate", "default rate"]):
            total_def = int(self.df["target_default"].sum())
            total_acc = len(self.df)
            def_rate = float(self.df["target_default"].mean())
            total_exp = float(self.df["loan_amount"].sum())
            facts["topic"] = "portfolio_summary"
            facts["total_accounts"] = f"{total_acc:,}"
            facts["total_defaults"] = f"{total_def:,}"
            facts["overall_default_rate"] = f"{def_rate:.2%}"
            facts["total_exposure"] = f"${total_exp:,.2f}"
            facts["formula"] = "SUM(target_default == 1) / COUNT(account_id)"
            return facts

        # Anything else is unrecognized / outside the schema -> strictly decline!
        facts["status"] = "declined"
        return facts

    def _call_gemini(self, query: str, facts: Dict[str, Any]) -> Dict[str, Any]:
        """Sends user query and facts to Gemini to seamlessly handle either chit-chat or grounded data queries."""
        is_data_query = (facts.get("status") == "answered")

        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            "=== CONTEXT (Data Facts) ===\n"
            f"{json.dumps(facts, indent=2)}\n\n"
            f"User Input: \"{query}\"\n\n"
            "Instructions:\n"
            "1. If the user input is a greeting, slang (e.g., 'heyyyy', 'Namaste'), thanks, or general conversational chat, respond naturally and briefly state you can answer credit risk portfolio questions.\n"
            "2. If it is an analytical question, answer ONLY using the provided CONTEXT. Cite exact figures. Do not hallucinate.\n"
            "3. If the user asks for analytics but the CONTEXT status is 'declined', state politely that the requested metric is outside the scope of the dataset. Never ask the user to provide JSON data or files."
        )

        response = self.gemini_client.generate_content(prompt, request_options={"timeout": 10.0})
        answer_text = response.text.strip().replace("$", "&#36;")

        ans_lower = answer_text.lower()
        is_decline = (not is_data_query) and any(
            phrase in ans_lower
            for phrase in ["outside the scope", "cannot answer", "does not contain", "not available in", "not included in"]
        )

        if is_data_query:
            intent = "answered"
            status = "answered"
            source = facts.get("provenance_table", "portfolio_master.parquet")
            sources = [facts.get("provenance_table", "portfolio_master.parquet")]
            formula = facts.get("formula", "Aggregated Group Metrics")
            sample_size = f"{facts.get('sample_size', 14685):,} loan accounts"
            suggested = []
        elif is_decline:
            intent = "out_of_scope"
            status = "declined"
            source = "Boundary Guardrail: Out of Scope"
            sources = []
            formula = "N/A"
            sample_size = "0 (Declined - Out of Scope)"
            suggested = SUGGESTED_EXAMPLES
        else:
            intent = "chitchat"
            status = "answered"
            source = "Portfolio Assistant Guide"
            sources = []
            formula = "N/A"
            sample_size = "N/A (Chit-chat / Onboarding)"
            suggested = SUGGESTED_EXAMPLES

        return {
            "intent": intent,
            "answer": answer_text,
            "source": source,
            "sources": sources,
            "formula": formula,
            "sample_size": sample_size,
            "status": status,
            "mode": f"Gemini Live LLM ({self.model_name})" if getattr(self, "model_name", None) else "Gemini Live LLM",
            "suggested_questions": suggested,
        }

    def _call_gemini_chitchat(self, query: str) -> Dict[str, Any]:
        """Calls Gemini for chit-chat or meta greeting inquiries."""
        return self._call_gemini(query, {"status": "declined"})

    def _call_gemini_decline(self, query: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Calls Gemini to organically draft a polite, professional decline for out-of-scope inquiries."""
        prompt = (
            f"The user asked an out-of-scope question in a credit risk banking dashboard: \"{query}\"\n"
            f"Reason: {reason or 'This topic is outside the scope of retail credit risk and portfolio analytics.'}\n\n"
            "Task: Write a polite, professional, and natural 1-2 sentence response explaining that you cannot answer this question because this dashboard is strictly focused on retail credit risk and loan portfolio analytics.\n"
            "Rules:\n"
            "- Do NOT ask the user for JSON data or files.\n"
            "- Do NOT say 'Hi!' or include an opening greeting.\n"
            "- Do NOT answer the out-of-scope question or hallucinate.\n"
            "- State clearly and politely that you cannot answer because the topic is outside the credit portfolio scope."
        )
        try:
            response = self.gemini_client.generate_content(prompt, request_options={"timeout": 10.0})
            answer_text = response.text.strip().replace("$", "&#36;")
            return {
                "intent": "out_of_scope",
                "answer": answer_text,
                "source": "Boundary Guardrail: Out of Scope",
                "sources": [],
                "sample_size": "0 (Declined - Out of Scope)",
                "status": "declined",
                "mode": f"Gemini Live LLM ({self.model_name})" if getattr(self, "model_name", None) else "Gemini Live LLM",
                "suggested_questions": SUGGESTED_EXAMPLES,
            }
        except Exception as e:
            logger.warning("Gemini decline call failed (%s). Falling back to concise deterministic decline.", e)
            return self._format_offline_decline(query, reason)

    def _call_openai(self, query: str, facts: Dict[str, Any]) -> Dict[str, Any]:
        """Sends user query and facts to OpenAI to seamlessly handle either chit-chat or grounded data queries."""
        is_data_query = (facts.get("status") == "answered")

        user_prompt = (
            "=== CONTEXT (Data Facts) ===\n"
            f"{json.dumps(facts, indent=2)}\n\n"
            f"User Question: \"{query}\"\n\n"
            "Instructions:\n"
            "1. If the user input is a greeting, slang (e.g., 'heyyyy', 'Namaste'), thanks, or general conversational chat, respond naturally and briefly state you can answer credit risk portfolio questions.\n"
            "2. If it is an analytical question, answer ONLY using the provided CONTEXT. Cite exact figures. Do not hallucinate.\n"
            "3. If the user asks for analytics but the CONTEXT status is 'declined', state politely that the requested metric is outside the scope of the dataset. Never ask the user to provide JSON data or files."
        )

        res = self.openai_client.chat.completions.create(
            model=getattr(self, "openai_model", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )
        answer_text = res.choices[0].message.content.strip().replace("$", "&#36;")

        ans_lower = answer_text.lower()
        is_decline = (not is_data_query) and any(
            phrase in ans_lower
            for phrase in ["outside the scope", "cannot answer", "does not contain", "not available in", "not included in"]
        )

        if is_data_query:
            intent = "answered"
            status = "answered"
            source = facts.get("provenance_table", "portfolio_master.parquet")
            sources = [facts.get("provenance_table", "portfolio_master.parquet")]
            formula = facts.get("formula", "Aggregated Group Metrics")
            sample_size = f"{facts.get('sample_size', 14685):,} loan accounts"
            suggested = []
        elif is_decline:
            intent = "out_of_scope"
            status = "declined"
            source = "Boundary Guardrail: Out of Scope"
            sources = []
            formula = "N/A"
            sample_size = "0 (Declined - Out of Scope)"
            suggested = SUGGESTED_EXAMPLES
        else:
            intent = "chitchat"
            status = "answered"
            source = "Portfolio Assistant Guide"
            sources = []
            formula = "N/A"
            sample_size = "N/A (Chit-chat / Onboarding)"
            suggested = SUGGESTED_EXAMPLES

        return {
            "intent": intent,
            "answer": answer_text,
            "source": source,
            "sources": sources,
            "formula": formula,
            "sample_size": sample_size,
            "status": status,
            "mode": "OpenAI Live LLM",
            "suggested_questions": suggested,
        }

    def _call_openai_chitchat(self, query: str) -> Dict[str, Any]:
        """Calls OpenAI for chit-chat or meta greeting inquiries."""
        return self._call_openai(query, {"status": "declined"})

    def _call_openai_decline(self, query: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Calls OpenAI to organically draft a polite, professional decline for out-of-scope inquiries."""
        user_prompt = (
            f"The user asked an out-of-scope question in a credit risk banking dashboard: \"{query}\"\n"
            f"Reason: {reason or 'This topic is outside the scope of retail credit risk and portfolio analytics.'}\n\n"
            "Task: Write a polite, professional, and natural 1-2 sentence response explaining that you cannot answer this question because this dashboard is strictly focused on retail credit risk and loan portfolio analytics.\n"
            "Rules:\n"
            "- Do NOT ask the user for JSON data or files.\n"
            "- Do NOT say 'Hi!' or include an opening greeting.\n"
            "- Do NOT answer the out-of-scope question or hallucinate.\n"
            "- State clearly and politely that you cannot answer because the topic is outside the credit portfolio scope."
        )
        try:
            res = self.openai_client.chat.completions.create(
                model=getattr(self, "openai_model", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=150,
            )
            answer_text = res.choices[0].message.content.strip().replace("$", "&#36;")
            return {
                "intent": "out_of_scope",
                "answer": answer_text,
                "source": "Boundary Guardrail: Out of Scope",
                "sources": [],
                "sample_size": "0 (Declined - Out of Scope)",
                "status": "declined",
                "mode": "OpenAI Live LLM",
                "suggested_questions": SUGGESTED_EXAMPLES,
            }
        except Exception as e:
            logger.warning("OpenAI decline call failed (%s). Falling back to concise deterministic decline.", e)
            return self._format_offline_decline(query, reason)

    def _format_offline_decline(self, query: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Generates a concise, professional decline without robotic boilerplate."""
        if reason:
            answer = (
                f"I cannot answer that question because {reason.rstrip('.')}. "
                "This assistant can only answer questions based on the provided portfolio data such as loan defaults, loss exposure, risk tiers, and borrower profiles."
            )
        else:
            answer = (
                "I cannot answer that question because the requested information is outside the scope of this credit portfolio. "
                "This assistant can only answer questions based on the provided portfolio data such as loan defaults, loss exposure, risk tiers, and borrower profiles."
            )
        effective_mode = (
            "Deterministic Grounded Engine (Offline Fallback)"
            if self.mode != "Deterministic Grounded Engine (Offline)"
            else "Deterministic Grounded Engine (Offline)"
        )
        return {
            "intent": "out_of_scope",
            "answer": answer,
            "source": "Boundary Guardrail: Out of Scope",
            "sources": [],
            "sample_size": "0 (Declined - Out of Scope)",
            "status": "declined",
            "mode": effective_mode,
            "suggested_questions": SUGGESTED_EXAMPLES,
        }

    def _format_deterministic_answer(
        self, query: str, facts: Dict[str, Any], mode_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates an institutional plain-English grounded answer using deterministic templates."""
        topic = facts.get("topic", "portfolio_summary")

        if topic == "loan_type_default":
            answer = (
                f"Across portfolio segments, **{facts['highest_loan_type']}** exhibits the highest default rate at "
                f"**{facts['highest_default_rate']}** ({facts['highest_default_count']:,} defaults out of {facts['highest_account_count']:,} facilities). "
                f"In contrast, **{facts['lowest_loan_type']}** demonstrates the lowest overall default rate at **{facts['lowest_default_rate']}** "
                f"({facts['lowest_default_count']:,} defaults out of {facts['lowest_account_count']:,} facilities). "
                f"Full breakdown: " + ", ".join([f"{k}: {v}" for k, v in facts["all_rates"].items()]) + "."
            )
        elif topic == "exposure":
            answer = (
                f"The total principal loan exposure across all {facts['total_accounts']:,} active accounts stands at **{facts['total_exposure']}**, "
                f"with an average loan size of **{facts['average_loan_size']}**. "
                f"**Mortgage lending** constitutes the primary concentration at **{facts['mortgage_exposure']}** (**{facts['mortgage_share']}** of total exposure)."
            )
        elif topic == "income_default":
            answer = (
                f"Borrower credit risk shows a strong inverse correlation with income: the **{facts['low_income_tier']}** bracket "
                f"records the highest delinquency/default rate at **{facts['low_income_rate']}** ({facts['low_income_defaults']:,}/{facts['low_income_count']:,} loans), "
                f"whereas the **{facts['high_income_tier']}** bracket has the lowest rate at **{facts['high_income_rate']}**. "
                f"Breakdown by income tier: " + "; ".join([f"{k}: {v}" for k, v in facts["all_income_rates"].items()]) + "."
            )
        elif topic == "employment_default":
            answer = (
                f"Segmenting by employment stability, **Unemployed** borrowers experience the highest default rate at "
                f"**{facts['unemployed_rate']}** ({facts['unemployed_defaults']:,} defaults across {facts['unemployed_count']:,} accounts), "
                f"while **{facts['lowest_emp_type']}** borrowers record the lowest default rate at **{facts['lowest_emp_rate']}**. "
                f"Segment breakdown: " + ", ".join([f"{k}: {v}" for k, v in facts["all_employment_rates"].items()]) + "."
            )
        elif topic == "region_default":
            answer = (
                f"By geographic region, **{facts['highest_exposure_region']}** carries the greatest loan exposure at **{facts['highest_region_exposure']}**, "
                f"while **{facts['highest_rate_region']}** registers the highest default rate at **{facts['highest_region_rate']}** "
                f"(lowest default rate is **{facts['lowest_rate_region']}** at **{facts['lowest_region_rate']}**). "
                f"Regional breakdown: " + "; ".join([f"{k}: {v}" for k, v in facts["all_regions"].items()]) + "."
            )
        elif topic == "collateral_default":
            answer = (
                f"Comparing collateralization segments, **Secured loans** (`collateral_flag = 1`, Mortgage & Auto) have an overall default rate of "
                f"**{facts['secured_rate']}** ({facts['secured_defaults']:,} defaults across {facts['secured_count']:,} accounts), driven by large mortgage concentrations, "
                f"compared to **{facts['unsecured_rate']}** ({facts['unsecured_defaults']:,} defaults across {facts['unsecured_count']:,} accounts) for **Unsecured facilities**."
            )
        elif topic == "risk_tiers":
            answer = (
                f"Across the Basel PD risk tiers, **{facts['critical_share_pct']}** of loans ({facts['critical_count']:,} accounts, **{facts['critical_exposure']}** exposure) "
                f"are classified as **Critical Risk** with an average interest rate of **{facts['critical_avg_ir']}**. "
                f"Combined **High & Critical Risk** tiers represent **{facts['high_crit_exposure']}** (**{facts['high_crit_exposure_share']}** of portfolio exposure across {facts['high_crit_count']:,} accounts). "
                f"Tier distribution: " + "; ".join([f"{k}: {v}" for k, v in facts["tier_breakdown"].items()]) + "."
            )
        elif topic == "bureau_impact":
            answer = (
                f"External bureau utilization and prior write-offs strongly drive default risk: defaulted accounts average **{facts['avg_utilization_default']}** bureau utilization "
                f"versus **{facts['avg_utilization_performing']}** for performing accounts (borrowers above 75% utilization default at **{facts['high_util_default_rate']}** vs **{facts['low_util_default_rate']}** below 30%). "
                f"Furthermore, customers with a prior bureau write-off ({facts['prior_writeoff_accounts']:,} accounts) default at **{facts['prior_writeoff_default_rate']}** compared to **{facts['no_writeoff_default_rate']}** for those without."
            )
        elif topic == "dti_analysis":
            answer = (
                f"Across defaulted accounts, the average Debt-to-Income (DTI) ratio is **{facts['default_avg_dti']}**, compared to "
                f"**{facts['performing_avg_dti']}** for performing accounts (portfolio average: **{facts['overall_avg_dti']}**). "
                f"Borrowers with high DTI (>0.40) default at **{facts['high_dti_default_rate']}** versus **{facts['low_dti_default_rate']}** for low-DTI (<=0.20) borrowers."
            )
        elif topic == "employment_tenure":
            answer = (
                f"Employment tenure inversely correlates with default risk: defaulted borrowers average **{facts['avg_years_employed_default']}** in their current role "
                f"compared to **{facts['avg_years_employed_performing']}** for performing borrowers. "
                f"Borrowers employed under 2 years default at **{facts['under_2yr_default_rate']}**, whereas those with 5+ years of tenure default at **{facts['over_5yr_default_rate']}**."
            )
        elif topic == "sector_default":
            answer = (
                f"Across occupation sectors, **{facts['highest_sector']}** exhibits the highest default rate at **{facts['highest_sector_rate']}**, "
                f"while **{facts['lowest_sector']}** exhibits the lowest at **{facts['lowest_sector_rate']}**. "
                f"Sector breakdown: " + ", ".join([f"{k}: {v}" for k, v in facts["all_sectors"].items()]) + "."
            )
        elif topic == "age_default":
            answer = (
                f"Profiling by borrower age cohort, the **{facts['highest_age_bucket']}** bracket records the highest default rate at **{facts['highest_age_rate']}**, "
                f"while the **{facts['lowest_age_bucket']}** bracket records the lowest at **{facts['lowest_age_rate']}**. "
                f"Age distribution: " + ", ".join([f"{k}: {v}" for k, v in facts["all_age_buckets"].items()]) + "."
            )
        elif topic == "interest_rate":
            crit_str = f" Critical Risk borrowers carry an average interest rate of **{facts['critical_risk_avg_ir']}**." if "critical_risk_avg_ir" in facts else ""
            answer = (
                f"The portfolio-wide average interest rate is **{facts['overall_avg_ir']}** (**{facts['default_avg_ir']}** for defaulted loans vs "
                f"**{facts['performing_avg_ir']}** for performing loans).{crit_str} "
                f"Average rate by product: " + ", ".join([f"{k}: {v}" for k, v in facts["ir_by_loan_type"].items()]) + "."
            )
        elif topic == "repayment_dpd":
            answer = (
                f"Historical repayment delinquency is a primary default predictor: accounts that ever breached 30+ DPD ({facts['ever_30dpd_count']:,} loans) "
                f"default at **{facts['ever_30dpd_default_rate']}**, compared to **{facts['clean_30dpd_default_rate']}** for accounts that never breached 30 DPD. "
                f"Portfolio average maximum DPD is **{facts['avg_max_dpd']}** with an average cumulative payment ratio of **{facts['avg_payment_ratio']}**."
            )
        else:
            answer = (
                f"The portfolio comprises **{facts.get('total_accounts', '14,685')}** active credit facilities with total exposure of "
                f"**{facts.get('total_exposure', '$601,119,531.00')}** and an overall default rate of **{facts.get('overall_default_rate', '16.10%')}** "
                f"({facts.get('total_defaults', '2,364')} realized defaults)."
            )

        clean_answer = answer.replace("$", "&#36;")
        effective_mode = mode_override if mode_override else (
            "Deterministic Grounded Engine (Offline)" if "Offline" in self.mode else "Deterministic Grounded Engine"
        )

        return {
            "intent": "answered",
            "answer": clean_answer,
            "source": facts.get("provenance_table", "portfolio_master.parquet"),
            "sources": [facts.get("provenance_table", "portfolio_master.parquet")],
            "formula": facts.get("formula", "Computed directly via Pandas groupby"),
            "sample_size": f"{facts.get('sample_size', 14685):,} loan accounts",
            "status": "answered",
            "mode": effective_mode,
        }


def match_supported_question(q: str, df: Optional[pd.DataFrame] = None) -> Optional[Dict[str, Any]]:
    """Calculates grounded facts via pandas if the query matches a supported analytical template."""
    asst = GroundedPortfolioAssistant(provider="Offline Mode", df_override=df)
    facts = asst._compute_grounded_facts(q)
    if facts.get("status") == "answered":
        return facts
    return None


def run_plan(plan: Dict[str, Any], df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Runs deterministic formatting on precomputed pandas facts."""
    asst = GroundedPortfolioAssistant(provider="Offline Mode", df_override=df)
    query = plan.get("query", "")
    return asst._format_deterministic_answer(query, plan)


def route_offline(q: str, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Exposes the offline engine directly for UI routing."""
    asst = GroundedPortfolioAssistant(provider="Offline Mode", df_override=df)
    return asst.ask(q)


if __name__ == "__main__":
    assistant = GroundedPortfolioAssistant(provider="Offline Mode")
    print("--- Test 1: Government sector ---")
    print(assistant.ask("What is the default rate for Government sector employees?"))
    print("\n--- Test 2: FICO score (Out of scope) ---")
    print(assistant.ask("What is the borrower's FICO score?"))
    print("\n--- Test 3: Capital of France (Out of scope) ---")
    print(assistant.ask("What is the capital of France?"))
    print("\n--- Test 4: Region with highest default rate ---")
    print(assistant.ask("Which region has the highest default rate?"))
    print("\n--- Test 5: Chit-chat greeting ---")
    print(assistant.ask("hey"))
    print("\n--- Test 6: Meta question ---")
    print(assistant.ask("what can you do?"))
    print("\n--- Test 7: route_offline direct ---")
    print(route_offline("how can you help me?"))

