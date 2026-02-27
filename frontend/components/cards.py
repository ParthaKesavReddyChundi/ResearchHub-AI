"""
ResearchHub-AI — Section Card Renderers (Elicit/Litmaps-inspired)
Professional, clean rendering for all 16 analysis output sections.
"""

import streamlit as st
import json
from typing import Any, Dict, List

from components.charts import create_gauge, create_horizontal_bars, create_timing_chart


# ── Helpers ──────────────────────────────────────────────────────

def _g(data, *keys, default=""):
    """Safe nested get."""
    cur = data
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k, default)
        elif isinstance(cur, list) and isinstance(k, int) and k < len(cur):
            cur = cur[k]
        else:
            return default
    return cur if cur is not None else default


def _section_open(emoji: str, title: str, subtitle: str) -> str:
    return f"""
    <div class="section-card">
        <div class="section-hdr">
            <span class="sec-emoji">{emoji}</span>
            <span class="sec-title">{title}</span>
            <span class="sec-sub">{subtitle}</span>
        </div>
    """

def _section_close() -> str:
    return "</div>"

def _pill(text: str, variant: str = "teal") -> str:
    return f'<span class="pill pill-{variant}">{text}</span>'

def _tag(text: str, variant: str = "") -> str:
    cls = f"tag tag-{variant}" if variant else "tag"
    return f'<span class="{cls}">{text}</span>'

def _score_bar(label: str, value: float, max_val: float = 100) -> str:
    pct = min(100, (value / max_val) * 100) if max_val else 0
    cls = "fill-green" if value >= 70 else ("fill-amber" if value >= 40 else "fill-red")
    return f"""
    <div style="margin:6px 0;">
        <div style="display:flex; justify-content:space-between; font-size:0.82rem;">
            <span style="font-weight:500; color:#4A4A4A;">{label}</span>
            <span style="color:#8A8578; font-weight:600;">{value:.0f}</span>
        </div>
        <div class="score-bar"><div class="score-fill {cls}" style="width:{pct}%"></div></div>
    </div>
    """

def _stat(val, label, color="#004D4D") -> str:
    return f"""
    <div class="stat-box">
        <div class="stat-val" style="color:{color};">{val}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


# ═══════════════════════════════════════════════════════════════
# 1. Direct Answer (Hero)
# ═══════════════════════════════════════════════════════════════

def render_direct_answer(data: Dict):
    da = data.get("direct_answer", data)
    query = _g(da, "query")
    intent = _g(da, "intent", default={})
    papers = _g(da, "papers_found", default=0)
    sources = _g(da, "sources", default={})

    html = f"""
    <div class="hero-card">
        <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:2px;
                    opacity:0.7; margin-bottom:10px; font-weight:600;">Research Query</div>
        <h2 style="font-family:Newsreader,Georgia,serif; font-size:1.6rem; font-weight:500;
                   margin-bottom:24px; line-height:1.35;">{query}</h2>
        <div style="display:flex; gap:20px; flex-wrap:wrap; align-items:center;">
    """
    html += f"""
            <div style="background:rgba(255,255,255,0.12); border-radius:8px; padding:12px 20px;">
                <div style="font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; opacity:0.7;">Papers</div>
                <div style="font-size:1.6rem; font-weight:600; font-family:Newsreader,serif;">{papers}</div>
            </div>
    """
    for src, count in (sources.items() if isinstance(sources, dict) else []):
        icon = "📄" if src.lower() == "arxiv" else "🏥"
        html += f"""
            <div style="background:rgba(255,255,255,0.12); border-radius:8px; padding:12px 20px;">
                <div style="font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; opacity:0.7;">{icon} {src}</div>
                <div style="font-size:1.6rem; font-weight:600; font-family:Newsreader,serif;">{count}</div>
            </div>
        """
    qt = _g(intent, "query_type")
    pf = _g(intent, "primary_focus")
    if qt:
        html += f"""
            <div style="margin-left:auto; text-align:right; opacity:0.85;">
                <div style="font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; opacity:0.7;">Type</div>
                <div style="font-size:0.95rem; font-weight:500;">{qt}</div>
                <div style="font-size:0.78rem; opacity:0.7; margin-top:2px;">{pf}</div>
            </div>
        """
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 2. Context Summary
# ═══════════════════════════════════════════════════════════════

def render_context_summary(data: Dict):
    cs = data.get("context_summary", data)
    papers = cs.get("papers", []) if isinstance(cs, dict) else []
    total = cs.get("total_papers", len(papers)) if isinstance(cs, dict) else 0

    html = _section_open("📚", "Papers Found", f"{total} papers retrieved from arXiv and PubMed")
    st.markdown(html, unsafe_allow_html=True)

    if not papers:
        st.info("No papers returned.")
    else:
        for i, p in enumerate(papers[:20]):
            title = p.get("title", "Untitled")
            authors = p.get("authors", [])
            auth_str = ", ".join(authors[:3]) + ("…" if len(authors) > 3 else "")
            source = p.get("source", "")
            url = p.get("url", "")
            abstract = p.get("abstract", "")
            src_cls = "teal" if source.lower() == "arxiv" else "blue"

            with st.expander(f"{title}", expanded=(i == 0)):
                meta_html = _pill(source.upper(), src_cls)
                if auth_str:
                    meta_html += f" &nbsp; <span style='font-size:0.83rem; color:#4A4A4A;'>{auth_str}</span>"
                st.markdown(meta_html, unsafe_allow_html=True)
                if abstract:
                    st.markdown(f"<p style='font-size:0.88rem; color:#4A4A4A; line-height:1.65; margin-top:8px;'>{abstract[:600]}{'…' if len(abstract)>600 else ''}</p>", unsafe_allow_html=True)
                if url:
                    st.markdown(f"[Read full paper →]({url})")

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 3. Knowledge Graph
# ═══════════════════════════════════════════════════════════════

def render_knowledge_graph(data: Dict):
    kg = data.get("knowledge_graph", data)
    if not isinstance(kg, dict): kg = {}

    html = _section_open("🧠", "Knowledge Graph", "Connections between key concepts in the literature")
    st.markdown(html, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(_stat(kg.get("node_count", 0), "Concepts"), unsafe_allow_html=True)
    with c2:
        st.markdown(_stat(kg.get("edge_count", 0), "Connections", "#006D6D"), unsafe_allow_html=True)
    with c3:
        clusters = kg.get("clusters", [])
        st.markdown(_stat(len(clusters), "Clusters", "#3D8B8B"), unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    concepts = kg.get("key_concepts", [])
    if concepts:
        st.markdown("**Key Concepts**")
        for c in concepts[:10]:
            name = c.get("name", str(c)) if isinstance(c, dict) else str(c)
            cent = c.get("centrality", 0) if isinstance(c, dict) else 0
            st.markdown(_score_bar(name, cent * 100), unsafe_allow_html=True)

    hidden = kg.get("hidden_connections", [])
    if hidden:
        st.markdown("**Hidden Connections**")
        for hc in hidden[:8]:
            fr, to = hc.get("from", ""), hc.get("to", "")
            via = " → ".join(hc.get("via", [])) or "direct"
            st.markdown(f"<div style='padding:4px 0; font-size:0.85rem;'>{_tag(fr, 'teal')} → <span style='color:#8A8578; font-size:0.8rem;'>via {via}</span> → {_tag(to, 'blue')}</div>", unsafe_allow_html=True)

    gi = kg.get("graph_insights", "")
    if gi:
        st.markdown(f"<p style='font-size:0.88rem; color:#4A4A4A; line-height:1.6; margin-top:12px;'>{gi}</p>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 4. Comparison
# ═══════════════════════════════════════════════════════════════

def render_comparison(data: Dict):
    comp = data.get("comparison", data)
    if not isinstance(comp, dict): comp = {}

    html = _section_open("📊", "Methodology Comparison", "How different approaches compare across the literature")
    st.markdown(html, unsafe_allow_html=True)

    tab_conf = {
        "Similarities": ("methodology_similarities", "green"),
        "Differences": ("methodology_differences", "red"),
        "Strengths": ("strengths", "blue"),
        "Weaknesses": ("weaknesses", "amber"),
        "Trade-offs": ("performance_tradeoffs", "teal"),
    }
    tabs = st.tabs(list(tab_conf.keys()))
    for tab, (label, (key, color)) in zip(tabs, tab_conf.items()):
        items = comp.get(key, [])
        with tab:
            if items:
                tags_html = " ".join([_tag(str(it), color) for it in items[:20]])
                st.markdown(f"<div style='line-height:2.2; padding:8px 0;'>{tags_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='muted small'>No {label.lower()} data.</p>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 5. Gap Analysis
# ═══════════════════════════════════════════════════════════════

def render_gap_analysis(data: Dict):
    ga = data.get("gap_analysis", data)
    if not isinstance(ga, dict): ga = {}

    html = _section_open("🚧", "Research Gaps", "Where the field falls short and what to explore next")
    st.markdown(html, unsafe_allow_html=True)

    sections = [
        ("🔁", "Repeated Limitations", "repeated_limitations"),
        ("🧪", "Underexplored Combinations", "underexplored_combinations"),
        ("📏", "Missing Benchmarks", "missing_benchmarks"),
        ("⚡", "Conflicting Findings", "conflicting_findings"),
        ("✨", "Novel Research Directions", "novel_research_directions"),
    ]
    for icon, label, key in sections:
        items = ga.get(key, [])
        if items:
            is_novel = key == "novel_research_directions"
            with st.expander(f"{icon} {label} ({len(items)})", expanded=is_novel):
                for item in items:
                    border_col = "#16A34A" if is_novel else "#E8E3DA"
                    st.markdown(f"<div style='padding:6px 0 6px 14px; font-size:0.88rem; border-left:2px solid {border_col}; margin-bottom:6px; color:#4A4A4A;'>{item}</div>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 6. Deep Insights
# ═══════════════════════════════════════════════════════════════

def render_deep_insights(data: Dict):
    di = data.get("deep_insights", data)
    if not isinstance(di, dict): di = {}

    html = _section_open("💡", "Deep Insights", "Patterns and trends extracted across all papers")
    st.markdown(html, unsafe_allow_html=True)

    cats = [
        ("🔬", "Unique Methods", "unique_methods"),
        ("📂", "Common Datasets", "common_datasets"),
        ("📐", "Metrics", "evaluation_metrics"),
        ("⚠️", "Limitations", "recurring_limitations"),
        ("🌱", "Emerging Themes", "emerging_themes"),
    ]
    cols = st.columns(len(cats))
    for col, (icon, label, key) in zip(cols, cats):
        items = di.get(key, [])
        with col:
            st.markdown(f"<div style='font-weight:600; font-size:0.82rem; color:#8A8578; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:8px;'>{icon} {label}</div>", unsafe_allow_html=True)
            if items:
                for item in items[:6]:
                    st.markdown(f"<div style='font-size:0.84rem; color:#4A4A4A; padding:4px 0; border-bottom:1px solid #F2EDE4;'>{item}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='font-size:0.8rem; color:#B0A999;'>—</span>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 7. Novelty Score
# ═══════════════════════════════════════════════════════════════

def render_novelty_score(data: Dict):
    ns = data.get("novelty_score", data)
    if not isinstance(ns, dict): ns = {}

    html = _section_open("🌟", "Novelty Score", "How unique and impactful is this research area?")
    st.markdown(html, unsafe_allow_html=True)

    overall = float(ns.get("overall_score", 0))
    c1, c2 = st.columns([1, 1.4])
    with c1:
        fig = create_gauge(overall, "Overall Novelty")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c2:
        subs = [
            ("Uniqueness", ns.get("uniqueness_score", 0)),
            ("Scientific Novelty", ns.get("scientific_novelty_score", 0)),
            ("Practical Novelty", ns.get("practical_novelty_score", 0)),
            ("Low Redundancy", ns.get("redundancy_risk_score", 0)),
            ("Opportunity", ns.get("opportunity_score", 0)),
        ]
        for label, val in subs:
            st.markdown(_score_bar(label, float(val)), unsafe_allow_html=True)

    explanation = ns.get("explanation", "")
    if explanation:
        st.markdown(f"<p style='font-size:0.88rem; color:#4A4A4A; line-height:1.6;'>{explanation}</p>", unsafe_allow_html=True)

    opp = ns.get("opportunity_areas", [])
    if opp:
        tags = " ".join([_tag(f"✨ {a}", "teal") for a in opp])
        st.markdown(f"<div style='margin-top:8px;'><strong style='font-size:0.82rem; color:#8A8578;'>OPPORTUNITY AREAS</strong><div style='margin-top:6px; line-height:2.2;'>{tags}</div></div>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 8. Trend Forecast
# ═══════════════════════════════════════════════════════════════

def render_trend_forecast(data: Dict):
    tf = data.get("trend_forecast", data)
    if not isinstance(tf, dict): tf = {}

    html = _section_open("📈", "Trend Forecast", "Where this research area is heading over the next 1-3 years")
    st.markdown(html, unsafe_allow_html=True)

    cur = tf.get("current_research_direction", "")
    if cur:
        st.markdown(f"<div style='background:#FAF8F3; border:1px solid #E8E3DA; border-radius:8px; padding:14px 18px; margin-bottom:16px; font-size:0.9rem; line-height:1.6; color:#4A4A4A;'><strong style='color:#004D4D;'>Current Direction:</strong> {cur}</div>", unsafe_allow_html=True)

    trends = tf.get("method_adoption_trends", [])
    if trends:
        st.markdown("<strong style='font-size:0.88rem;'>Method Trends</strong>", unsafe_allow_html=True)
        for t in trends[:8]:
            method = t.get("method", str(t)) if isinstance(t, dict) else str(t)
            trend = t.get("trend", "") if isinstance(t, dict) else ""
            reason = t.get("reason", "") if isinstance(t, dict) else ""
            arrow = "↑" if trend == "rising" else ("↓" if trend == "declining" else "→")
            color = "#16A34A" if trend == "rising" else ("#DC2626" if trend == "declining" else "#CA8A04")
            st.markdown(f"<div style='padding:5px 0; font-size:0.88rem;'><span style='color:{color}; font-weight:700; font-size:1rem;'>{arrow}</span> <strong>{method}</strong> <span style='color:#8A8578; font-size:0.82rem;'>— {reason}</span></div>", unsafe_allow_html=True)

    p1 = tf.get("one_year_predictions", [])
    p3 = tf.get("three_year_predictions", [])
    if p1 or p3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<strong style='font-size:0.85rem;'>📅 1-Year Outlook</strong>", unsafe_allow_html=True)
            for p in p1[:6]:
                st.markdown(f"<div style='font-size:0.85rem; padding:3px 0; color:#4A4A4A;'>• {p}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<strong style='font-size:0.85rem;'>🔮 3-Year Outlook</strong>", unsafe_allow_html=True)
            for p in p3[:6]:
                st.markdown(f"<div style='font-size:0.85rem; padding:3px 0; color:#4A4A4A;'>• {p}</div>", unsafe_allow_html=True)

    rising = tf.get("rising_topics", [])
    declining = tf.get("declining_topics", [])
    if rising or declining:
        r1, r2 = st.columns(2)
        with r1:
            if rising:
                tags = " ".join([_tag(f"↑ {t}", "green") for t in rising[:8]])
                st.markdown(f"<div style='margin-top:8px;'><strong style='font-size:0.82rem; color:#8A8578;'>RISING</strong><div style='margin-top:4px; line-height:2.2;'>{tags}</div></div>", unsafe_allow_html=True)
        with r2:
            if declining:
                tags = " ".join([_tag(f"↓ {t}", "red") for t in declining[:8]])
                st.markdown(f"<div style='margin-top:8px;'><strong style='font-size:0.82rem; color:#8A8578;'>DECLINING</strong><div style='margin-top:4px; line-height:2.2;'>{tags}</div></div>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 9. Recommended Methods & Datasets
# ═══════════════════════════════════════════════════════════════

def render_recommended_methods(data: Dict):
    rmd = data.get("recommended_methods_datasets", data)
    if not isinstance(rmd, dict): rmd = {}

    html = _section_open("🛠️", "Recommended Tools", "Methods, datasets, and metrics for this research area")
    st.markdown(html, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<strong style='font-size:0.82rem; color:#8A8578; text-transform:uppercase; letter-spacing:0.04em;'>Methods</strong>", unsafe_allow_html=True)
        for m in rmd.get("recommended_methods", [])[:10]:
            st.markdown(f"<div style='margin:3px 0;'>{_tag(str(m), 'teal')}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<strong style='font-size:0.82rem; color:#8A8578; text-transform:uppercase; letter-spacing:0.04em;'>Datasets</strong>", unsafe_allow_html=True)
        for d in rmd.get("recommended_datasets", [])[:10]:
            st.markdown(f"<div style='margin:3px 0;'>{_tag(str(d), 'blue')}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<strong style='font-size:0.82rem; color:#8A8578; text-transform:uppercase; letter-spacing:0.04em;'>Metrics</strong>", unsafe_allow_html=True)
        for e in rmd.get("evaluation_metrics", [])[:10]:
            st.markdown(f"<div style='margin:3px 0;'>{_tag(str(e), 'green')}</div>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 10. Experiment Suggestions
# ═══════════════════════════════════════════════════════════════

def render_experiment_suggestions(data: Dict):
    es = data.get("experiment_suggestions", data)
    if not isinstance(es, list):
        es = [es] if es else []

    html = _section_open("🧪", "Experiment Ideas", "Concrete experiments and explorations to try next")
    st.markdown(html, unsafe_allow_html=True)

    for i, item in enumerate(es[:12], 1):
        text = str(item)
        is_exp = text.lower().startswith("experiment")
        pill_type = "teal" if is_exp else "blue"
        pill_label = "EXPERIMENT" if is_exp else "EXPLORE"
        st.markdown(f"""
        <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 16px;
                    border-left:2px solid {'#004D4D' if is_exp else '#2563EB'};
                    margin-bottom:8px; background:#FEFDFB; border-radius:0 6px 6px 0;">
            <span style="font-weight:700; color:#004D4D; font-family:Newsreader,serif; font-size:1.1rem; min-width:24px;">{i}</span>
            <div>
                {_pill(pill_label, pill_type)}
                <p style="font-size:0.88rem; color:#4A4A4A; margin:6px 0 0; line-height:1.55;">{text}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 11. Researcher Roadmap
# ═══════════════════════════════════════════════════════════════

def render_researcher_roadmap(data: Dict):
    rm = data.get("researcher_roadmap", data)
    if not isinstance(rm, dict): rm = {}

    html = _section_open("📘", "Researcher Roadmap", "A 4-week plan to get up to speed in this area")
    st.markdown(html, unsafe_allow_html=True)

    roadmap = rm.get("roadmap", {})
    if isinstance(roadmap, dict):
        weeks = ["week_1", "week_2", "week_3", "week_4"]
        labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        colors = ["#004D4D", "#006D6D", "#3D8B8B", "#16A34A"]
        for wk, lbl, col in zip(weeks, labels, colors):
            wd = roadmap.get(wk, {})
            if not isinstance(wd, dict): continue
            theme = wd.get("theme", "")
            tasks = wd.get("tasks", [])
            resources = wd.get("resources", [])
            with st.expander(f"📅 {lbl}: {theme}", expanded=(wk == "week_1")):
                if tasks:
                    for t in tasks:
                        st.markdown(f"<div style='font-size:0.85rem; padding:3px 0; color:#4A4A4A;'>☐ {t}</div>", unsafe_allow_html=True)
                if resources:
                    st.markdown("<div style='margin-top:8px;'><strong style='font-size:0.8rem; color:#8A8578;'>Resources:</strong></div>", unsafe_allow_html=True)
                    for r in resources:
                        st.markdown(f"<div style='font-size:0.83rem; padding:2px 0; color:#4A4A4A;'>📎 {r}</div>", unsafe_allow_html=True)

    projects = rm.get("project_ideas", [])
    if projects:
        st.markdown("<strong style='font-size:0.88rem; display:block; margin-top:16px;'>Project Ideas</strong>", unsafe_allow_html=True)
        for proj in projects[:6]:
            if isinstance(proj, dict):
                title = proj.get("title", "")
                diff = proj.get("difficulty", "intermediate")
                desc = proj.get("description", "")
                d_cls = {"beginner": "green", "intermediate": "amber", "advanced": "red"}.get(diff, "teal")
                st.markdown(f"""
                <div style="padding:10px 14px; border:1px solid #E8E3DA; border-radius:8px; margin:6px 0; background:#FEFDFB;">
                    <strong style="font-size:0.88rem;">{title}</strong> {_pill(diff.upper(), d_cls)}
                    <p style="font-size:0.83rem; color:#4A4A4A; margin:4px 0 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"• {proj}")

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 12. Argument Strength
# ═══════════════════════════════════════════════════════════════

def render_argument_strength(data: Dict):
    args = data.get("argument_strength", data)
    if not isinstance(args, list):
        args = [args] if args else []

    html = _section_open("🧩", "Argument Strength", "How strong is the evidence behind key claims?")
    st.markdown(html, unsafe_allow_html=True)

    if args:
        for a in args[:12]:
            if not isinstance(a, dict): continue
            claim = a.get("claim", "")
            ev = a.get("evidence_strength", "")
            rel = a.get("reliability", "")
            missing = a.get("missing_evidence", "")
            bias = a.get("bias_indicators", "")
            ev_cls = {"strong": "green", "moderate": "amber", "weak": "red"}.get(ev, "gray")
            rel_cls = {"high": "green", "medium": "amber", "low": "red"}.get(rel, "gray")
            st.markdown(f"""
            <div style="padding:12px 16px; border-bottom:1px solid #E8E3DA;">
                <div style="font-weight:500; font-size:0.9rem; margin-bottom:6px;">{claim}</div>
                <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
                    {_pill('Evidence: ' + ev, ev_cls)}
                    {_pill('Reliability: ' + rel, rel_cls)}
                </div>
                {f'<div style="font-size:0.82rem; color:#8A8578; margin-top:6px;">Missing: {missing}</div>' if missing else ''}
                {f'<div style="font-size:0.82rem; color:#8A8578;">Bias: {bias}</div>' if bias else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No argument strength data.")

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 13. Scientific Critique
# ═══════════════════════════════════════════════════════════════

def render_scientific_critique(data: Dict):
    sc = data.get("scientific_critique", data)
    if not isinstance(sc, dict): sc = {}

    html = _section_open("🧼", "Scientific Critique", "Strengths, weaknesses, and methodological assessment")
    st.markdown(html, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<strong style='color:#16A34A; font-size:0.88rem;'>Strong Points</strong>", unsafe_allow_html=True)
        for sp in sc.get("strong_points", []):
            aspect = sp.get("aspect", str(sp)) if isinstance(sp, dict) else str(sp)
            detail = sp.get("detail", "") if isinstance(sp, dict) else ""
            st.markdown(f"""
            <div style="padding:10px 14px; border-left:2px solid #16A34A; margin:6px 0; background:#FAFDFB;">
                <strong style="font-size:0.85rem;">{aspect}</strong>
                <p style="font-size:0.82rem; color:#4A4A4A; margin:2px 0 0;">{detail}</p>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        st.markdown("<strong style='color:#DC2626; font-size:0.88rem;'>Weak Points</strong>", unsafe_allow_html=True)
        for wp in sc.get("weak_points", []):
            aspect = wp.get("aspect", str(wp)) if isinstance(wp, dict) else str(wp)
            detail = wp.get("detail", "") if isinstance(wp, dict) else ""
            severity = wp.get("severity", "moderate") if isinstance(wp, dict) else "moderate"
            sev_cls = {"major": "red", "moderate": "amber", "minor": "gray"}.get(severity, "amber")
            st.markdown(f"""
            <div style="padding:10px 14px; border-left:2px solid #DC2626; margin:6px 0; background:#FFFBFB;">
                <strong style="font-size:0.85rem;">{aspect}</strong> {_pill(severity.upper(), sev_cls)}
                <p style="font-size:0.82rem; color:#4A4A4A; margin:2px 0 0;">{detail}</p>
            </div>
            """, unsafe_allow_html=True)

    assessments = [
        ("Experimental Design", sc.get("experimental_design_assessment", "")),
        ("Reproducibility", sc.get("reproducibility_assessment", "")),
        ("Statistical Validity", sc.get("statistical_validity", "")),
        ("Dataset Quality", sc.get("dataset_quality", "")),
    ]
    non_empty = [(l, v) for l, v in assessments if v]
    if non_empty:
        st.markdown("<div style='margin-top:16px;'><strong style='font-size:0.85rem;'>Methodology Assessment</strong></div>", unsafe_allow_html=True)
        for label, value in non_empty:
            st.markdown(f"""
            <div style="padding:8px 14px; border:1px solid #E8E3DA; border-radius:6px; margin:4px 0; background:#FEFDFB;">
                <strong style='font-size:0.82rem; color:#004D4D;'>{label}</strong>
                <span style='font-size:0.82rem; color:#4A4A4A;'> — {value}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 14. Literature Review
# ═══════════════════════════════════════════════════════════════

def render_literature_review(data: Dict):
    lr = data.get("literature_review", data)
    text = lr if isinstance(lr, str) else str(lr)

    html = _section_open("📚", "Literature Review", "A comprehensive narrative review synthesized from the papers")
    st.markdown(html, unsafe_allow_html=True)

    if text and text.strip():
        st.markdown(f"<div style='font-size:0.92rem; line-height:1.75; color:#1A1A1A;'>{text}</div>" if "<" not in text[:10] else "", unsafe_allow_html=True)
        st.markdown(text)
        if st.button("📋 Copy to clipboard", key="copy_lr"):
            st.code(text[:2000], language="markdown")
    else:
        st.info("No literature review generated.")

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 15. Confidence Score
# ═══════════════════════════════════════════════════════════════

def render_confidence_score(data: Dict):
    cs = data.get("confidence_score", data)
    if not isinstance(cs, dict): cs = {}

    html = _section_open("🔐", "Confidence Score", "How reliable and comprehensive is this analysis?")
    st.markdown(html, unsafe_allow_html=True)

    score = float(cs.get("score", 0))
    max_s = float(cs.get("max_score", 100))

    c1, c2 = st.columns([1, 1.4])
    with c1:
        fig = create_gauge(score, "Confidence", max_s)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c2:
        breakdown = cs.get("breakdown", [])
        if breakdown:
            st.markdown("<strong style='font-size:0.85rem;'>Breakdown</strong>", unsafe_allow_html=True)
            for item in breakdown:
                text = str(item)
                icon = "✅" if any(w in text.lower() for w in ["strong", "success", "generat", "cover"]) else "⚠️"
                st.markdown(f"<div style='padding:4px 0; font-size:0.85rem; color:#4A4A4A;'>{icon} {text}</div>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 16. Explainability Log
# ═══════════════════════════════════════════════════════════════

def render_explainability_log(data: Dict):
    el = data.get("explainability_log", data)
    if not isinstance(el, dict): el = {}

    html = _section_open("📝", "Pipeline Details", "Which agents ran and how long each took")
    st.markdown(html, unsafe_allow_html=True)

    agents = el.get("agents_activated", [])
    total_agents = el.get("total_agents", len(agents))
    total_time = el.get("total_pipeline_time_seconds", 0)
    strategy = el.get("routing_strategy", "")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(_stat(f"{len(agents)}/{total_agents}", "Agents"), unsafe_allow_html=True)
    with c2:
        st.markdown(_stat(f"{total_time:.1f}s", "Total Time", "#006D6D"), unsafe_allow_html=True)
    with c3:
        st.markdown(_stat(strategy or "—", "Strategy", "#3D8B8B"), unsafe_allow_html=True)

    if agents:
        pills = " ".join([f'<span class="agent-pill agent-done">{a}</span>' for a in agents])
        st.markdown(f"<div style='line-height:2.2; margin:14px 0;'>{pills}</div>", unsafe_allow_html=True)

    timing = el.get("timing_breakdown", {})
    if isinstance(timing, dict) and timing:
        fig = create_timing_chart(list(timing.keys()), [float(v) for v in timing.values()])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    reasoning = el.get("reasoning_summary", "")
    if reasoning:
        with st.expander("Reasoning Summary"):
            st.markdown(f"<p style='font-size:0.88rem; color:#4A4A4A; line-height:1.6;'>{reasoning}</p>", unsafe_allow_html=True)

    st.markdown(_section_close(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# Master renderer
# ═══════════════════════════════════════════════════════════════

def render_all_sections(result: Dict):
    renderers = [
        ("direct_answer", render_direct_answer),
        ("context_summary", render_context_summary),
        ("knowledge_graph", render_knowledge_graph),
        ("comparison", render_comparison),
        ("gap_analysis", render_gap_analysis),
        ("deep_insights", render_deep_insights),
        ("novelty_score", render_novelty_score),
        ("trend_forecast", render_trend_forecast),
        ("recommended_methods_datasets", render_recommended_methods),
        ("experiment_suggestions", render_experiment_suggestions),
        ("researcher_roadmap", render_researcher_roadmap),
        ("argument_strength", render_argument_strength),
        ("scientific_critique", render_scientific_critique),
        ("literature_review", render_literature_review),
        ("confidence_score", render_confidence_score),
        ("explainability_log", render_explainability_log),
    ]
    for key, renderer in renderers:
        section_data = result.get(key)
        if section_data is not None:
            try:
                renderer({key: section_data})
            except Exception as e:
                st.warning(f"Error rendering {key}: {e}")
        else:
            try:
                renderer(result)
            except Exception:
                pass
