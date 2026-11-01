"""
AI Assistant right drawer panel ('Ask the Portfolio') component.
Matches Google Cloud Assist:
- State 1: Welcome banner, bullet points, spec expander, and suggestion chips.
- State 2: Active chat wipes welcome banner & chips, showing conversation thread with bottom input.
- Plus icon ('＋') resets conversation and returns to the initial Welcome interface.
"""
import random
import time
import re
import markdown
import streamlit as st
import pandas as pd

# 1. Define the Fast-Path Interceptor patterns at the top of the file
GREETING = re.compile(
    r"^\s*(hi|hey|hello|yo|howdy|greetings|good (morning|afternoon|evening)|how are you|what'?s up|bye)\b",
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

HELP_TEXT = (
    "Hi! I answer questions about this credit portfolio using the loaded data. "
    "Try asking me things like:\n"
    "- Which loan type has the highest default rate?\n"
    "- What is the default rate by employment type?\n"
    "- Show me total exposure by region."
)

THANKS_TEXT = (
    "You're welcome! I am here to assist with any credit risk or portfolio analytics inquiries. "
    "Feel free to ask about default rates, risk tiers, exposure distributions, or specific loan characteristics."
)

try:
    from config import AI_METADATA_SPEC
    from theme import color_currency
except (ModuleNotFoundError, ImportError):
    from app.config import AI_METADATA_SPEC
    from app.theme import color_currency
from src.llm_assistant import GroundedPortfolioAssistant

QUESTION_BANK = [
    "Which loan type has the highest default rate?",
    "What is total portfolio exposure and average loan size?",
    "What is default rate for low-income borrowers?",
    "What is unemployment risk impact on defaults?",
    "Which geographic region carries the greatest loss exposure?",
    "How does bureau utilization affect probability of default?",
    "What percentage of loans are classified as critical risk?",
    "Compare default rates between secured and unsecured loans.",
    "What is the average debt-to-income (DTI) across default accounts?",
    "Which income tier has the lowest delinquency rate?",
    "What is the total loss exposure in High & Critical risk tiers?",
    "What is the average interest rate for critical risk borrowers?",
    "How does employment tenure correlate with loan default?",
    "Which loan type has the lowest overall default rate?",
    "What is the portfolio distribution across risk tiers?",
]


def render_chat_query(q: str, ts: str):
    """Render the user query bubble (Google Cloud right-aligned pill)."""
    st.markdown(
        f"""
        <div class="gcp-user-bubble-row">
            <div class="gcp-user-bubble">{q}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stream_text_words(text: str):
    """Yields text word-by-word with an organic conversational typing pace."""
    if not text:
        return
    words = text.split(" ")
    n_words = len(words)
    delay = max(0.012, min(0.025, 0.85 / max(n_words, 1)))
    for i, w in enumerate(words):
        yield w + (" " if i < len(words) - 1 else "")
        time.sleep(delay)


def should_show_provenance(r: dict) -> bool:
    """Helper for provenance card display (disabled)."""
    return False


def render_provenance_box_html(r: dict) -> str:
    """Provenance metadata card is disabled per UI requirements."""
    return ""


def render_chat_response(r: dict, is_dark: bool):
    """Render the assistant response card with 'Done thinking'."""
    clean_ans = color_currency(r.get("answer", ""))
    ans_html = markdown.markdown(clean_ans, extensions=["extra", "nl2br"])
    
    html_content = f"""<div class="gcp-assistant-bubble">
    <div class="gcp-status-line">
        <span class="gcp-sparkle-small">✨</span>
        <span class="gcp-status-text">Done thinking</span>
    </div>
    <div class="gcp-answer-body">
        {ans_html}
    </div>
</div>"""

    st.markdown(html_content, unsafe_allow_html=True)


def render_governance_dialog():
    """Toggles AI Feature 1 Governance Specification directly inside the chat drawer panel."""
    st.session_state["show_gov_spec"] = True
    st.rerun()


def render_ai_assistant_panel(assistant: GroundedPortfolioAssistant, is_dark: bool):
    """Render the Google Cloud-style 'Ask the Portfolio' side drawer."""
    # ── State: Governance Specification View inside Side Drawer ──
    if st.session_state.get("show_gov_spec", False):
        with st.container(key="gcp_gov_header_sticky"):
            back_col, title_col, close_col = st.columns([1.0, 7.5, 1.0], gap="small", vertical_alignment="center")
            with back_col:
                if st.button("←", key="gcp_btn_gov_back", help="Back to chat", type="secondary"):
                    st.session_state["show_gov_spec"] = False
                    st.rerun()
            with title_col:
                st.markdown(
                    '<div class="gcp-gov-header-title">'
                    'AI Feature 1 — Governance Specification'
                    '</div>',
                    unsafe_allow_html=True
                )
            with close_col:
                if st.button("✕", key="gcp_btn_gov_close", help="Close assistant panel", type="secondary"):
                    st.session_state["show_gov_spec"] = False
                    st.session_state["show_chat_assistant"] = False
                    st.session_state["ensure_sidebar_open"] = True
                    st.rerun()

        with st.container(key="gcp_gov_body_container"):
            st.markdown(
                f"""
                <div class="gov-dialog-container" style="padding-top:10px;padding-bottom:24px;">
                    <div class="gov-dialog-header-badge">
                        <span class="gov-badge-text">{AI_METADATA_SPEC['feature_name']}</span>
                    </div>
                    <div class="gov-card">
                        <div class="gov-card-title">Operational Trigger</div>
                        <div class="gov-card-desc">{AI_METADATA_SPEC['trigger']}</div>
                    </div>
                    <div class="gov-card">
                        <div class="gov-card-title">False Positive Risk & Mitigation</div>
                        <div class="gov-card-desc">{AI_METADATA_SPEC['false_positive']}</div>
                    </div>
                    <div class="gov-card">
                        <div class="gov-card-title">False Negative Risk & Mitigation</div>
                        <div class="gov-card-desc">{AI_METADATA_SPEC['false_negative']}</div>
                    </div>
                    <div class="gov-card">
                        <div class="gov-card-title">Human-in-the-Loop Protocol</div>
                        <div class="gov-card-desc">{AI_METADATA_SPEC['human_in_the_loop']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        return

    # 1. Header (Title: Ask the Portfolio, Action buttons: ?, +, ✕) — Sticky at top of drawer
    with st.container(key="gcp_chat_header_sticky"):
        title_col, info_col, add_col, close_col = st.columns([7.0, 1.0, 1.0, 1.0], gap="small", vertical_alignment="center")
        with title_col:
            st.markdown(
                '<div class="gcp-assist-header-left"><span class="gcp-assist-title">Ask the Portfolio</span></div>',
                unsafe_allow_html=True
            )
        with info_col:
            if st.button("?", key="welcome_gov_spec_btn", help="AI Governance Specification", type="secondary"):
                st.session_state["show_gov_spec"] = True
                st.rerun()
        with add_col:
            if st.button("+", key="gcp_btn_new_chat", help="Start new conversation", type="secondary"):
                st.session_state["chat_history"] = []
                st.session_state["suggested_questions"] = random.sample(QUESTION_BANK, 5)
                st.session_state["show_gov_spec"] = False
                st.rerun()
        with close_col:
            if st.button("✕", key="gcp_btn_close_panel", help="Close assistant panel", type="secondary"):
                st.session_state["show_gov_spec"] = False
                st.session_state["show_chat_assistant"] = False
                st.session_state["ensure_sidebar_open"] = True
                st.rerun()

    chat_history = st.session_state.get("chat_history", [])

    # Refresh 5 random questions whenever flagged (e.g., panel opened) or uninitialized
    if st.session_state.get("refresh_chat_questions", False) or "suggested_questions" not in st.session_state:
        st.session_state["suggested_questions"] = random.sample(QUESTION_BANK, 5)
        st.session_state["refresh_chat_questions"] = False

    # ═══════════════════════════════════════════════════════════════════════
    # STATE 1: WELCOME SCREEN (When chat history is empty)
    # ═══════════════════════════════════════════════════════════════════════
    if not chat_history:
        with st.container(key="gcp_welcome_body_container"):
            st.markdown(
                f"""
                <div class="gcp-welcome-title">Welcome</div>
                <div class="gcp-welcome-subtitle">What can I help you with?</div>
                <ul class="gcp-welcome-list">
                    <li>Explore portfolio default drivers & risk segments</li>
                    <li>Review estimated exposure distributions & income cuts</li>
                    <li>Analytical heuristics computed from cohort sample</li>
                    <li>Verify critical credit figures against official bank records</li>
                </ul>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)

            with st.form("gcp_welcome_form", clear_on_submit=True):
                welcome_input = st.text_area(
                    "Prompt",
                    placeholder="Ask the Portfolio",
                    label_visibility="collapsed",
                    key="gcp_welcome_prompt",
                    height=52,
                )
                welcome_submitted = st.form_submit_button("➤", type="primary")

            prompts = st.session_state.get("suggested_questions", QUESTION_BANK[:5])
            chip_q = None
            with st.container(key="gcp_suggested_questions_wrap"):
                for idx, p in enumerate(prompts):
                    if st.button(p, key=f"gcp_q_{idx}", use_container_width=True, type="secondary"):
                        chip_q = p

            st.markdown(
                """
                <div class="gcp-disclaimer">
                    AI assistance is exploratory and may contain inaccuracies. Verify key outputs before taking underwriting action.
                </div>
                """,
                unsafe_allow_html=True
            )

        run_q = chip_q or (welcome_input.strip() if welcome_submitted and welcome_input.strip() else None)
        if run_q:
            now_ts = pd.Timestamp.now().strftime("%H:%M:%S")
            # Step 1: Immediately append user question to chat history with r=None and rerun so UI renders it first
            st.session_state["chat_history"].append({
                "q": run_q,
                "r": None,
                "ts": now_ts
            })
            st.rerun()

    # ═══════════════════════════════════════════════════════════════════════
    # STATE 2: ACTIVE CHAT SCREEN (Google Cloud style - Welcome & chips wiped!)
    # ═══════════════════════════════════════════════════════════════════════
    else:
        st.markdown(
            """
            <div class="gcp-disclaimer-top">
                Explore credit risk insights. Verify critical computations with official bank reporting.
            </div>
            """,
            unsafe_allow_html=True
        )

        clicked_suggested = None
        for idx, item in enumerate(chat_history):
            # STEP 1: Always render the user question first
            render_chat_query(item["q"], item.get("ts", ""))

            # If response is already calculated, render it directly from cache
            if item.get("r") is not None:
                render_chat_response(item["r"], is_dark)
                suggested = item["r"].get("suggested_questions", [])
                if suggested and idx == len(chat_history) - 1:
                    st.markdown(
                        "<div style='font-size:0.80rem;font-weight:600;margin:6px 0 6px 2px;color:rgba(128,128,128,0.85);'>💡 Suggested Questions (click to run):</div>",
                        unsafe_allow_html=True,
                    )
                    for s_i, sq in enumerate(suggested):
                        if st.button(f"✦ {sq}", key=f"chat_sugg_{idx}_{s_i}", use_container_width=True, type="secondary"):
                            clicked_suggested = sq
            else:
                # STEP 2: Check Fast-Path BEFORE triggering spinners or backend APIs
                prompt_text = item["q"].strip()
                is_thanks = bool(THANKS.search(prompt_text))
                is_chit_chat = bool(GREETING.search(prompt_text) or META.search(prompt_text))
                
                # Check if prompt contains analytical domain keywords (e.g. "default", "loan", "exposure")
                analytical_kw = re.compile(
                    r"\b(loan|rate|default|exposure|portfolio|risk|income|tier|dti|delinquen|unemploy|utiliz|balance|borrower|grade|loss)\b",
                    re.I,
                )
                has_data_intent = bool(analytical_kw.search(prompt_text))

                status_box = st.empty()
                is_live_llm = ("Gemini" in getattr(assistant, "mode", "")) or ("OpenAI" in getattr(assistant, "mode", ""))
                is_offline_fast_path = (not is_live_llm) and (is_thanks or is_chit_chat) and not has_data_intent

                if is_offline_fast_path:
                    # Fast-path: Instant local response for greetings/thanks in Offline mode without backend spinner
                    status_box.markdown(
                        """
                        <div class="gcp-status-line">
                            <span class="gcp-sparkle-small">✨</span>
                            <span class="gcp-status-text">Done thinking</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    resp_answer = THANKS_TEXT if is_thanks else HELP_TEXT
                    resp = {
                        "answer": resp_answer,
                        "source": "Portfolio Assistant Guide",
                        "sources": [],
                        "sample_size": "N/A (Chit-chat / Onboarding)",
                        "status": "answered",
                        "intent": "chitchat",
                        "mode": getattr(assistant, "mode", "Deterministic Grounded Engine (Offline)"),
                        "suggested_questions": QUESTION_BANK[:4],
                    }
                else:
                    # Live LLM (Gemini / OpenAI) or Analytical query: Route to assistant.ask with thinking spinner
                    status_box.markdown(
                        """
                        <div class="gcp-status-line">
                            <span class="gcp-sparkle-small">✨</span>
                            <span class="gcp-status-text">Thinking...</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if "Gemini" in getattr(assistant, "mode", ""):
                        spinner_msg = "Consulting Gemini..."
                    elif "OpenAI" in getattr(assistant, "mode", ""):
                        spinner_msg = "Consulting OpenAI..."
                    else:
                        spinner_msg = "Analyzing portfolio..."

                    with st.spinner(spinner_msg):
                        resp = assistant.ask(item["q"])

                    status_box.markdown(
                        """
                        <div class="gcp-status-line">
                            <span class="gcp-sparkle-small">✨</span>
                            <span class="gcp-status-text">Done thinking</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # STEP 3: Display the response organically via word-by-word streaming
                with st.container(key="gcp_streaming_answer_wrap"):
                    raw_ans = resp.get("answer", "")
                    st.write_stream(stream_text_words(raw_ans))


                # STEP 4: Save assistant response to history so subsequent reruns don't recalculate
                item["r"] = resp
                st.session_state["chat_history"][idx]["r"] = resp

                suggested = resp.get("suggested_questions", [])
                if suggested:
                    st.markdown(
                        "<div style='font-size:0.80rem;font-weight:600;margin:6px 0 6px 2px;color:rgba(128,128,128,0.85);'>💡 Suggested Questions (click to run):</div>",
                        unsafe_allow_html=True,
                    )
                    for s_i, sq in enumerate(suggested):
                        if st.button(f"✦ {sq}", key=f"chat_sugg_{idx}_{s_i}", use_container_width=True, type="secondary"):
                            clicked_suggested = sq

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

        with st.form("gcp_active_chat_form", clear_on_submit=True):
            followup_input = st.text_area(
                "Prompt",
                placeholder="Ask the Portfolio",
                label_visibility="collapsed",
                key="gcp_followup_prompt",
                height=52,
            )
            followup_submitted = st.form_submit_button("➤", type="primary")

        run_q = clicked_suggested or (followup_input.strip() if followup_submitted and followup_input.strip() else None)
        if run_q:
            now_ts = pd.Timestamp.now().strftime("%H:%M:%S")
            # Step 1: Immediately append question to history with r=None and rerun so UI renders it first
            st.session_state["chat_history"].append({
                "q": run_q,
                "r": None,
                "ts": now_ts
            })
            st.rerun()

    # ── Interactive Client Script: Shift+Enter for newlines, auto-expansion & widen drawer ─
    st.iframe(
        r"""
        <script>
        (function() {
            function getParentDoc() {
                try {
                    if (window.parent && window.parent.document && window.parent.document.body) {
                        return window.parent.document;
                    }
                } catch(e) {}
                try {
                    if (window.top && window.top.document && window.top.document.body) {
                        return window.top.document;
                    }
                } catch(e) {}
                return document;
            }

            const parentDoc = getParentDoc();
            if (!parentDoc) return;

            function submitChatForm(ta, form) {
                if (!form) return;
                const val = (ta.value || '').trim();
                if (val.length === 0) return;

                ta.dispatchEvent(new Event('input', { bubbles: true }));
                ta.dispatchEvent(new Event('change', { bubbles: true }));
                ta.blur();

                const panel = parentDoc.querySelector('.st-key-ask_portfolio_side_panel');
                const main = parentDoc.querySelector('section[data-testid="stMain"]');
                const header = parentDoc.querySelector('.st-key-top_app_header_bar');
                if (panel) panel.classList.remove('chat-expanded-width');
                if (main) main.classList.remove('chat-panel-expanded-main');
                if (header) header.classList.remove('chat-panel-expanded-header');
                form.classList.remove('has-input');

                const btn = form.querySelector('[data-testid="stFormSubmitButton"] button') ||
                            form.querySelector('button[data-testid*="FormSubmit"]') ||
                            form.querySelector('button[type="submit"]') ||
                            form.querySelector('button');
                if (btn) {
                    btn.click();
                }
            }

            if (!parentDoc._chatEnterKeyGlobalBound) {
                parentDoc._chatEnterKeyGlobalBound = true;
                parentDoc.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.isComposing) {
                        const ta = e.target;
                        if (ta && ta.tagName === 'TEXTAREA') {
                            const form = ta.closest('form') || ta.closest('[data-testid="stForm"]');
                            const isChat = form && (
                                form.closest('.st-key-ask_portfolio_side_panel') ||
                                ta.getAttribute('aria-label') === 'Prompt' ||
                                ta.placeholder === 'Ask the Portfolio'
                            );
                            if (isChat) {
                                if (!e.shiftKey) {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    e.stopImmediatePropagation();
                                    submitChatForm(ta, form);
                                }
                            }
                        }
                    }
                }, true);
            }

            function closeSidebarIfOpen() {
                try {
                    const collapseBtn = parentDoc.querySelector('button[aria-label="Collapse sidebar"]') ||
                                        parentDoc.querySelector('[data-testid="stSidebarCollapseButton"] button');
                    if (collapseBtn) {
                        collapseBtn.click();
                    }
                } catch(e) {}
            }

            if (!parentDoc._chatAskPortfolioClickBound) {
                parentDoc._chatAskPortfolioClickBound = true;
                parentDoc.addEventListener('click', function(e) {
                    const btn = e.target && e.target.closest('button');
                    if (!btn) return;
                    const isAskBtn = btn.closest('.st-key-btn_ask_portfolio_cta') ||
                                     btn.closest('.st-key-nav_btn_ask_portfolio') ||
                                     (btn.innerText || btn.textContent || '').includes('Ask the Portfolio') ||
                                     (btn.innerText || btn.textContent || '').includes('AI Copilot');
                    if (isAskBtn) {
                        closeSidebarIfOpen();
                    }
                }, true);
            }

            function setupChatTextareas() {
                try {
                    const panel = parentDoc.querySelector('.st-key-ask_portfolio_side_panel');
                    const main = parentDoc.querySelector('section[data-testid="stMain"]');
                    const header = parentDoc.querySelector('.st-key-top_app_header_bar');
                    if (panel) panel.classList.remove('chat-expanded-width');
                    if (main) main.classList.remove('chat-panel-expanded-main');
                    if (header) header.classList.remove('chat-panel-expanded-header');

                    if (panel) {
                        const chatHeader = panel.querySelector('.st-key-gcp_chat_header_sticky');
                        if (chatHeader) {
                            const wrapper = chatHeader.closest('[data-testid="stElementContainer"]') || chatHeader.parentElement;
                            if (wrapper && wrapper.style.position !== 'sticky') {
                                wrapper.style.setProperty('position', 'sticky', 'important');
                                wrapper.style.setProperty('top', '0px', 'important');
                                wrapper.style.setProperty('z-index', '99999', 'important');
                                wrapper.style.setProperty('margin', '0px', 'important');
                                wrapper.style.setProperty('padding', '0px', 'important');
                                wrapper.style.setProperty('width', '100%', 'important');
                                wrapper.style.setProperty('box-shadow', 'none', 'important');
                            }
                        }
                    }

                    const tas = panel ? panel.querySelectorAll('textarea') : [];
                    tas.forEach(ta => {
                        function cleanInnerBoxAndPositionBtn() {
                            const form = ta.closest('form') || ta.closest('[data-testid="stForm"]');
                            if (form) {
                                const root = form.querySelector('[data-testid="stTextAreaRootElement"]');
                                if (root) {
                                    root.style.setProperty('border', 'none', 'important');
                                    root.style.setProperty('background', 'transparent', 'important');
                                    root.style.setProperty('box-shadow', 'none', 'important');
                                }
                                const btnWrap = form.querySelector('[data-testid="stFormSubmitButton"]');
                                if (btnWrap) {
                                    if (btnWrap.parentElement && btnWrap.parentElement !== form) {
                                        btnWrap.parentElement.style.setProperty('position', 'static', 'important');
                                    }
                                    btnWrap.style.setProperty('position', 'absolute', 'important');
                                    btnWrap.style.setProperty('right', '10px', 'important');
                                    btnWrap.style.setProperty('bottom', '10px', 'important');
                                }
                            }
                        }

                        function updateSendButton() {
                            cleanInnerBoxAndPositionBtn();
                            const val = (ta.value || '').trim();
                            const form = ta.closest('form') || ta.closest('[data-testid="stForm"]');
                            if (form) {
                                if (val.length > 0) {
                                    form.classList.add('has-input');
                                } else {
                                    form.classList.remove('has-input');
                                }
                            }
                        }

                        function adjustHeight() {
                            cleanInnerBoxAndPositionBtn();
                            updateSendButton();
                            ta.style.setProperty('height', 'auto', 'important');
                            const newH = Math.min(Math.max(ta.scrollHeight, 44), 180);
                            ta.style.setProperty('height', newH + 'px', 'important');
                        }

                        if (ta.dataset.shiftEnterBound !== 'true') {
                            ta.dataset.shiftEnterBound = 'true';

                            ta.addEventListener('keydown', function(e) {
                                if (e.key === 'Enter' && !e.isComposing) {
                                    if (!e.shiftKey) {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        e.stopImmediatePropagation();
                                        const form = ta.closest('form') || ta.closest('[data-testid="stForm"]');
                                        submitChatForm(ta, form);
                                    } else {
                                        setTimeout(adjustHeight, 10);
                                    }
                                }
                            }, true);

                            ta.addEventListener('input', adjustHeight);
                            ta.addEventListener('keyup', adjustHeight);
                            ta.addEventListener('change', adjustHeight);
                            ta.addEventListener('paste', () => setTimeout(adjustHeight, 10));
                            adjustHeight();
                        }
                    });
                } catch(e) {}
            }
            setupChatTextareas();
            if (window.MutationObserver && !parentDoc._chatPanelObserverAttached) {
                parentDoc._chatPanelObserverAttached = true;
                const obs = new MutationObserver(setupChatTextareas);
                obs.observe(parentDoc.body, { childList: true, subtree: true });
            }
        })();
        </script>
        """,
        height=1,
    )

