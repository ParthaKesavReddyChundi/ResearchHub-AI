"""
ResearchHub-AI — Analysis View
Query input, pipeline progress, 16-section results.
"""

import streamlit as st
import threading
import time
import json
from api.client import ResearchHubAPI
from components.cards import render_all_sections
from components.animations import PIPELINE_STAGES, render_agent_progress


def _run_analysis_bg(api, token, query, ws_id, holder):
    try:
        result = api.run_analysis(token, query, ws_id)
        holder["data"] = result
        holder["done"] = True
    except Exception as e:
        holder["error"] = str(e)
        holder["done"] = True


def render_analysis_page(api: ResearchHubAPI):
    token = st.session_state.get("token", "")
    ws_id = st.session_state.get("workspace_id")
    ws_name = st.session_state.get("workspace_name", "")

    # ── Sidebar ───────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 16px;">
            <h2 style="font-family:Newsreader,Georgia,serif; font-size:1.3rem;
                       color:#004D4D; margin-bottom:0;">ResearchHub</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Dashboard", use_container_width=True, key="back"):
            st.session_state.pop("analysis_result", None)
            st.session_state.pop("analysis_query", None)
            st.session_state["page"] = "dashboard"
            st.rerun()

        st.markdown("---")

        if st.session_state.get("analysis_result"):
            st.markdown("<div style='font-size:0.78rem; font-weight:600; color:#8A8578; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;'>Sections</div>", unsafe_allow_html=True)
            nav = [
                ("🔍", "Direct Answer"), ("📚", "Papers"), ("🧠", "Knowledge Graph"),
                ("📊", "Comparison"), ("🚧", "Gaps"), ("💡", "Insights"),
                ("🌟", "Novelty"), ("📈", "Trends"), ("🛠️", "Tools"),
                ("🧪", "Experiments"), ("📘", "Roadmap"), ("🧩", "Arguments"),
                ("🧼", "Critique"), ("📚", "Lit Review"), ("🔐", "Confidence"),
                ("📝", "Pipeline"),
            ]
            for emoji, label in nav:
                st.markdown(f"<div style='font-size:0.82rem; padding:2px 0; color:#4A4A4A;'>{emoji} {label}</div>", unsafe_allow_html=True)

        if ws_name:
            st.markdown("---")
            st.markdown(f"<div style='font-size:0.78rem; color:#B0A999;'>📂 {ws_name}</div>", unsafe_allow_html=True)

    # ── Main ──────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:24px;">
        <h1 style="font-family:Newsreader,Georgia,serif; font-size:2rem; font-weight:500;
                   color:#004D4D; margin-bottom:4px;">Research Analysis</h1>
        <p style="color:#8A8578; font-size:0.88rem;">
            Enter a research topic — 11 AI agents will produce a comprehensive analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Search bar
    prefilled = st.session_state.pop("analysis_query", "")

    st.markdown('<div class="big-search">', unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    with c1:
        query = st.text_input(
            "Query", value=prefilled,
            placeholder="e.g. transformer attention mechanisms, CRISPR gene editing safety...",
            key="q_input", label_visibility="collapsed"
        )
    with c2:
        clicked = st.button("Analyze →", use_container_width=True, key="run")
    st.markdown('</div>', unsafe_allow_html=True)

    should_run = clicked or (prefilled and not st.session_state.get("analysis_result"))

    # ── Run Analysis ──────────────────────────────────────
    if should_run and query:
        st.session_state.pop("analysis_result", None)
        st.session_state["analysis_query_display"] = query

        holder = {"done": False, "data": None, "error": None}
        thread = threading.Thread(target=_run_analysis_bg,
                                  args=(api, token, query, ws_id, holder), daemon=True)
        thread.start()

        progress_ph = st.empty()
        stage = 0
        total = len(PIPELINE_STAGES)

        while not holder["done"]:
            with progress_ph.container():
                st.markdown(f"""
                <div style="text-align:center; margin:24px 0 8px;">
                    <h3 style="font-family:Newsreader,Georgia,serif; color:#004D4D; font-weight:500;">
                        Analysis in progress
                    </h3>
                    <p style="color:#8A8578; font-size:0.88rem;">
                        11 AI agents are analyzing your topic — typically 30-90 seconds
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(render_agent_progress(min(stage, total - 1)), unsafe_allow_html=True)
                st.progress(min((stage + 1) / total, 0.95))
            stage += 1
            for _ in range(10):
                if holder["done"]: break
                time.sleep(0.5)

        progress_ph.empty()

        if holder.get("error"):
            err = holder["error"]
            if "timeout" in err.lower():
                st.error("⏱ Analysis timed out. Please try again.")
            elif "401" in err:
                st.error("Session expired. Please sign in again.")
                st.session_state["page"] = "login"
                st.rerun()
            elif "Connection" in err:
                st.error("Cannot reach backend at localhost:8000.")
            else:
                st.error(f"Analysis failed: {err}")
        elif holder.get("data"):
            data = holder["data"]
            result = data.get("result", {})
            t = data.get("pipeline_time_seconds", 0)
            st.session_state["analysis_result"] = result

            st.markdown(f"""
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px;
                        padding:12px 18px; margin-bottom:20px; display:flex; align-items:center; gap:10px;
                        animation:fadeIn 0.3s ease;">
                <span style="font-size:1.2rem;">✓</span>
                <span style="font-weight:600; color:#15803D; font-size:0.9rem;">Analysis complete</span>
                <span style="color:#8A8578; font-size:0.82rem; margin-left:8px;">⏱ {t:.1f}s</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────
    result = st.session_state.get("analysis_result")
    if result:
        dq = st.session_state.get("analysis_query_display", "")
        if dq:
            st.markdown(f"""
            <div style="margin-bottom:20px;">
                <div style="font-size:0.72rem; color:#B0A999; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Results for</div>
                <h2 style="font-family:Newsreader,Georgia,serif; font-size:1.4rem; font-weight:500; color:#1A1A1A; margin-top:4px;">
                    {dq}
                </h2>
            </div>
            """, unsafe_allow_html=True)

        ec1, ec2, _ec3 = st.columns([1, 1, 4])
        with ec1:
            json_str = json.dumps(result, indent=2, default=str)
            st.download_button("↓ Export JSON", json_str, file_name="analysis.json", mime="application/json")
        with ec2:
            if st.button("📋 Copy"):
                st.code(json_str[:500] + "...", language="json")

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        render_all_sections(result)

    elif not should_run:
        st.markdown("""
        <div style="text-align:center; padding:80px 20px;">
            <div style="font-size:3rem; margin-bottom:16px; opacity:0.2;">🔬</div>
            <h2 style="font-family:Newsreader,Georgia,serif; color:#8A8578; font-weight:400; font-size:1.4rem;">
                Ready to analyze
            </h2>
            <p style="color:#B0A999; font-size:0.9rem; max-width:480px; margin:8px auto;">
                Enter any research topic and click Analyze. Our agents will search papers,
                extract insights, score novelty, forecast trends, and much more.
            </p>
            <div style="margin-top:28px; display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
                <span class="tag tag-teal">Gene editing safety</span>
                <span class="tag tag-blue">Transformer architectures</span>
                <span class="tag tag-green">Drug discovery AI</span>
                <span class="tag tag-amber">Climate change ML</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
