"""
ResearchHub-AI — Dashboard
Workspace sidebar + analysis history in main area.
"""

import streamlit as st
from api.client import ResearchHubAPI


def render_dashboard(api: ResearchHubAPI):
    token = st.session_state.get("token", "")

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 16px;">
            <h2 style="font-family:Newsreader,Georgia,serif; font-size:1.3rem;
                       color:#004D4D; margin-bottom:0;">ResearchHub</h2>
            <p style="font-size:0.78rem; color:#B0A999; margin:2px 0 0;">AI Research Analysis</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<div style='font-size:0.82rem; color:#8A8578; margin-bottom:12px;'>👤 {st.session_state.get('user_email', '')}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div style='font-size:0.78rem; font-weight:600; color:#8A8578; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;'>Workspaces</div>", unsafe_allow_html=True)

        try:
            workspaces = api.list_workspaces(token)
        except Exception:
            workspaces = []
            st.error("Could not load workspaces.")

        if workspaces:
            ws_names = [w.get("name", f"Workspace {w.get('id')}") for w in workspaces]
            ws_ids = [w.get("id") for w in workspaces]
            idx = 0
            if "workspace_id" in st.session_state:
                try: idx = ws_ids.index(st.session_state["workspace_id"])
                except ValueError: idx = 0
            selected = st.selectbox("Workspace", ws_names, index=idx, label_visibility="collapsed")
            i = ws_names.index(selected)
            st.session_state["workspace_id"] = ws_ids[i]
            st.session_state["workspace_name"] = ws_names[i]
        else:
            st.markdown("<p style='font-size:0.85rem; color:#B0A999;'>No workspaces yet.</p>", unsafe_allow_html=True)

        with st.expander("＋ New workspace"):
            new_name = st.text_input("Name", placeholder="My Research Project", key="new_ws", label_visibility="collapsed")
            if st.button("Create", key="create_ws"):
                if new_name:
                    try:
                        ws = api.create_workspace(token, new_name)
                        st.session_state["workspace_id"] = ws.get("id")
                        st.session_state["workspace_name"] = new_name
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        if workspaces and st.session_state.get("workspace_id"):
            with st.expander("Delete workspace"):
                st.warning(f"Delete **{st.session_state.get('workspace_name', '')}**?")
                if st.button("Confirm delete", key="del_ws"):
                    try:
                        api.delete_workspace(token, st.session_state["workspace_id"])
                        del st.session_state["workspace_id"]
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        st.markdown("---")
        if st.button("📄 Papers", use_container_width=True, key="nav_papers"):
            st.session_state["page"] = "papers"
            st.rerun()
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("Sign out", use_container_width=True, key="logout"):
            for k in ["token", "user_email", "workspace_id", "workspace_name", "analysis_result"]:
                st.session_state.pop(k, None)
            st.session_state["page"] = "login"
            st.rerun()

    # ── Main ──────────────────────────────────────────────────
    ws_name = st.session_state.get("workspace_name", "Research")

    st.markdown(f"""
    <div style="margin-bottom:28px;">
        <h1 style="font-family:Newsreader,Georgia,serif; font-size:2rem; font-weight:500;
                   color:#004D4D; margin-bottom:4px;">{ws_name}</h1>
        <p style="color:#8A8578; font-size:0.88rem;">Research analysis history and quick actions</p>
    </div>
    """, unsafe_allow_html=True)

    # Search bar
    st.markdown('<div class="big-search">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        query_input = st.text_input(
            "Search", placeholder="What do you want to research? e.g. transformer attention mechanisms in NLP",
            key="dash_q", label_visibility="collapsed"
        )
    with col2:
        if st.button("Analyze →", use_container_width=True, key="dash_go"):
            if query_input:
                st.session_state["analysis_query"] = query_input
                st.session_state["page"] = "analysis"
                st.rerun()
            else:
                st.warning("Enter a research topic.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # History
    ws_id = st.session_state.get("workspace_id")
    if ws_id:
        try:
            history = api.get_history(token, ws_id)
        except Exception:
            history = []

        if history:
            st.markdown("<div style='font-size:0.78rem; font-weight:600; color:#8A8578; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;'>Past Analyses</div>", unsafe_allow_html=True)
            for item in history[:20]:
                aid = item.get("id", "")
                query = item.get("query", "Untitled")
                created = item.get("created_at", "")[:16].replace("T", " · ")
                st.markdown(f"""
                <div class="history-item">
                    <div style="font-weight:500; font-size:0.92rem; color:#1A1A1A; margin-bottom:3px;">{query}</div>
                    <div style="font-size:0.78rem; color:#B0A999;">{created}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("View results →", key=f"v_{aid}"):
                    try:
                        full = api.get_result(token, aid)
                        st.session_state["analysis_result"] = full.get("result", {})
                        st.session_state["analysis_query_display"] = query
                        st.session_state["page"] = "analysis"
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
        else:
            st.markdown("""
            <div style="text-align:center; padding:60px 20px;">
                <div style="font-size:2.5rem; margin-bottom:14px; opacity:0.3;">🔬</div>
                <h3 style="font-family:Newsreader,Georgia,serif; color:#8A8578; font-weight:400; font-size:1.2rem;">
                    No analyses yet
                </h3>
                <p style="color:#B0A999; font-size:0.88rem; margin-top:6px;">
                    Enter a research topic above and click Analyze
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Select or create a workspace to begin.")
