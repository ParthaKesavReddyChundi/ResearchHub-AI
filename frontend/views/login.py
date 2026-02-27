"""
ResearchHub-AI — Login / Register Page
"""

import streamlit as st
from api.client import ResearchHubAPI


def render_login_page(api: ResearchHubAPI):
    # Hide sidebar on login
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
        .stApp [data-testid="stToolbar"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

    # Center card
    _l, center, _r = st.columns([1.2, 1, 1.2])

    with center:
        st.markdown("""
        <div class="login-wrap">
            <div class="login-brand">
                <h1>ResearchHub</h1>
                <p>AI-powered scientific reasoning</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        mode = st.radio("", ["Sign in", "Create account"], horizontal=True, label_visibility="collapsed")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="you@university.edu", key="auth_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="auth_pwd")

        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        if mode == "Create account":
            if st.button("Create account", use_container_width=True):
                if not email or not password:
                    st.error("Please fill in both fields.")
                    return
                try:
                    api.register(email, password)
                    st.success("Account created — switch to Sign in.")
                except Exception as e:
                    msg = str(e)
                    if "400" in msg or "409" in msg:
                        st.error("This email is already registered.")
                    else:
                        st.error(f"Registration failed: {msg}")
        else:
            if st.button("Sign in", use_container_width=True):
                if not email or not password:
                    st.error("Please fill in both fields.")
                    return
                try:
                    result = api.login(email, password)
                    token = result.get("access_token", "")
                    if token:
                        st.session_state["token"] = token
                        st.session_state["user_email"] = email
                        st.session_state["page"] = "dashboard"
                        st.rerun()
                    else:
                        st.error("Login failed — no token.")
                except Exception as e:
                    msg = str(e)
                    if "401" in msg:
                        st.error("Invalid email or password.")
                    elif "Connection" in msg:
                        st.error("Cannot reach the backend at localhost:8000.")
                    else:
                        st.error(f"Login failed: {msg}")

        st.markdown("""
        <div style="text-align:center; margin-top:32px; font-size:0.78rem; color:#B0A999;">
            11 AI agents · arXiv + PubMed · 16-section deep analysis
        </div>
        """, unsafe_allow_html=True)
