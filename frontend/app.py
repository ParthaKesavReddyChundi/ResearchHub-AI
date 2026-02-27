"""
ResearchHub-AI — Main Streamlit Application
Entry point that wires together all pages, injects global CSS, and handles routing.
"""

import streamlit as st

# ── Page Config (MUST be the first Streamlit call) ────────────────
st.set_page_config(
    page_title="ResearchHub AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports (after set_page_config) ───────────────────────────────
from components.styles import get_global_css
from api.client import ResearchHubAPI
from views.login import render_login_page
from views.dashboard import render_dashboard
from views.analysis import render_analysis_page
from views.papers import render_papers_page


# ── Inject Global CSS ────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)


# ── Initialize API Client ────────────────────────────────────────
API_BASE_URL = "http://localhost:8000"
api = ResearchHubAPI(base_url=API_BASE_URL)


# ── Session State Defaults ────────────────────────────────────────
defaults = {
    "page": "login",
    "token": None,
    "user_email": None,
    "workspace_id": None,
    "workspace_name": None,
    "analysis_result": None,
    "analysis_query": None,
    "analysis_query_display": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Auth Guard ────────────────────────────────────────────────────
def is_authenticated() -> bool:
    return bool(st.session_state.get("token"))


# ── Router ────────────────────────────────────────────────────────
page = st.session_state.get("page", "login")

if not is_authenticated() and page != "login":
    st.session_state["page"] = "login"
    page = "login"

if page == "login":
    render_login_page(api)
elif page == "dashboard":
    render_dashboard(api)
elif page == "analysis":
    render_analysis_page(api)
elif page == "papers":
    render_papers_page(api)
else:
    st.session_state["page"] = "login"
    st.rerun()
