# streamlit/streamlit_app.py

import requests
import streamlit as st

from config import settings  # uses your unified config helper

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TriResolve AI – Service Desk Platform",
    page_icon="🧠",
    layout="wide",
)

# --- BASIC THEME TWEAKS VIA CSS ---
st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .triresolve-hero h1 {
        font-size: 2.4rem !important;
        margin-bottom: 0.3rem;
    }
    .triresolve-hero h3 {
        font-size: 1.1rem !important;
        font-weight: 400;
        opacity: 0.9;
        margin-top: 0;
    }
    .section-label {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.8rem;
        color: #8a8d98;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.7rem;
        background: rgba(0, 213, 240, 0.12);
        color: #00d5f0;
        margin-right: 0.4rem;
    }
    .pill span {
        margin-left: 0.3rem;
    }
    .agent-badge {
        font-size: 0.8rem;
        padding: 0.2rem 0.5rem;
        border-radius: 999px;
        margin-right: 0.3rem;
        background: rgba(172, 70, 186, 0.12);
        color: #ac46ba;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR NAV USING PAGE LINKS ---
st.sidebar.title("TriResolve AI")
st.sidebar.write("Service Desk Platform")

st.sidebar.markdown("#### Navigation")
st.sidebar.page_link("streamlit_app.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/1_Maps.py", label="Maps", icon="🗺️")
st.sidebar.page_link("pages/2_Assistant.py", label="Assistant (TriNexa)", icon="🤖")
st.sidebar.page_link("pages/3_About.py", label="About", icon="ℹ️")

# --- BACKEND HEALTH CHECK ---
BACKEND_HEALTH_URL = settings.backend_url.rstrip("/") + "/health"


def check_backend_health() -> bool:
    try:
        resp = requests.get(BACKEND_HEALTH_URL, timeout=3)
        resp.raise_for_status()
        data = resp.json()
        return data.get("status") == "ok"
    except Exception:
        return False


# --- OVERVIEW CONTENT (MAIN AREA) ---
st.markdown(
    """
    <div class="triresolve-hero">
        <h1>TriResolve AI – Service Desk Platform</h1>
        <h3>Powered by TriNexa, your multi-domain orchestrator for IT, HR, and Finance.</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([2, 1])

with col1:
    st.write(
        """
        TriResolve AI is your **multi-agent service desk layer** that will eventually:

        - Ingest tickets and signals from IT, HR, and Finance systems  
        - Route them through **TriNexa**, the global orchestrator  
        - Delegate tasks to specialized agents  
        - Aggregate resolutions and surface them back in one unified workspace
        """
    )

with col2:
    st.markdown('<p class="section-label">Status</p>', unsafe_allow_html=True)

    ui_msg = "UI shell: online"
    st.success(ui_msg)

    if check_backend_health():
        st.success("Backend API: healthy")
    else:
        st.warning("Backend API: not reachable from Streamlit")

    st.info("Agent skills: wired via Azure OpenAI / Foundry deployments")

st.divider()
st.markdown('<p class="section-label">Domains</p>', unsafe_allow_html=True)
st.markdown(
    """
    <span class="agent-badge">IT Service Desk</span>
    <span class="agent-badge">HR & People Ops</span>
    <span class="agent-badge">Finance & Spend</span>
    """,
    unsafe_allow_html=True,
)
