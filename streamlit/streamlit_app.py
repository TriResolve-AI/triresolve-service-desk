import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TriResolve AI – Service Desk Platform",
    page_icon="🧠",
    layout="wide"
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

# --- SIDEBAR NAV ---
st.sidebar.title("TriResolve AI")
st.sidebar.write("Service Desk Platform")

nav = st.sidebar.radio(
    "Navigation",
    ["Overview", "Maps", "Assistant (TriNexa)", "About"],
