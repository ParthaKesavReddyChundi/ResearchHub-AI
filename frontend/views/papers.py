"""
ResearchHub-AI — Paper Management
"""

import streamlit as st
from api.client import ResearchHubAPI


def render_papers_page(api: ResearchHubAPI):
    token = st.session_state.get("token", "")
    ws_id = st.session_state.get("workspace_id")
    ws_name = st.session_state.get("workspace_name", "Workspace")

    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 16px;">
            <h2 style="font-family:Newsreader,Georgia,serif; font-size:1.3rem;
                       color:#004D4D; margin-bottom:0;">ResearchHub</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Dashboard", use_container_width=True, key="back"):
            st.session_state["page"] = "dashboard"
            st.rerun()

    st.markdown(f"""
    <div style="margin-bottom:24px;">
        <h1 style="font-family:Newsreader,Georgia,serif; font-size:2rem; font-weight:500;
                   color:#004D4D; margin-bottom:4px;">Papers — {ws_name}</h1>
        <p style="color:#8A8578; font-size:0.88rem;">Upload and manage research papers</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="soon-badge" style="margin-bottom:24px;">
        🚀 <strong>RAG-Enhanced Analysis (Coming Soon)</strong> — Upload papers for retrieval-augmented analysis from your edge device
    </div>
    """, unsafe_allow_html=True)

    if not ws_id:
        st.warning("Select a workspace from the dashboard first.")
        return

    # Upload
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-hdr">
        <span class="sec-emoji">📤</span>
        <span class="sec-title">Upload Paper</span>
        <span class="sec-sub">Add a PDF research paper to this workspace</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed", key="paper_up")
    if uploaded:
        if st.button("Upload", key="up_btn"):
            try:
                r = api.upload_paper(token, ws_id, (uploaded.name, uploaded, "application/pdf"))
                st.success(f"Uploaded: {r.get('filename', uploaded.name)}")
                st.rerun()
            except Exception as e:
                st.error(str(e))
    st.markdown('</div>', unsafe_allow_html=True)

    # List
    st.markdown('<div class="section-card" style="margin-top:12px;">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-hdr">
        <span class="sec-emoji">📚</span>
        <span class="sec-title">Papers in Workspace</span>
        <span class="sec-sub">Currently uploaded research papers</span>
    </div>
    """, unsafe_allow_html=True)

    try:
        papers = api.list_papers(token, ws_id)
    except Exception:
        papers = []

    if papers:
        for p in papers:
            fn = p.get("filename", "Unknown")
            st.markdown(f"""
            <div class="paper-item">
                <span style="font-size:1.1rem; margin-right:8px;">📄</span>
                <span style="font-weight:500; font-size:0.9rem;">{fn}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:28px 16px;">
            <div style="font-size:2rem; opacity:0.2; margin-bottom:8px;">📄</div>
            <p style="color:#B0A999; font-size:0.88rem;">No papers uploaded yet</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
