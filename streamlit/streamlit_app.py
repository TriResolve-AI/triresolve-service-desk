# streamlit/streamlit_app.py

from pathlib import Path

import streamlit as st

from theme import PALETTE, inject_base_css

# ---- Page config (only here, not in sub-pages) ----
st.set_page_config(
    page_title="TriResolve AI – Service Desk Platform",
    page_icon="🧠",
    layout="wide",
)

# Inject shared CSS
inject_base_css()

# ---- Try to load logo ----
logo_path = Path(__file__).parent / "assets" / "triresolve_logo.png"

col_logo, col_title = st.columns([1, 3])

with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=110)
    else:
        st.markdown(
            f"<div class='pill'>TriResolveAI<span>Service Desk</span></div>",
            unsafe_allow_html=True,
        )

with col_title:
    st.markdown(
        """
        <div class="triresolve-hero">
            <h1>TriResolve AI – Service Desk Platform</h1>
            <h3>Powered by <b>TriNexa</b>, your multi-domain orchestrator for IT, HR, and Finance.</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")
st.markdown(
    "<p class='section-label'>Overview</p>",
    unsafe_allow_html=True,
)

left, right = st.columns([1.7, 1.3])

with left:
    st.write(
        """
        TriResolve AI is your **multi-agent service desk layer**:

        - Ingests tickets and signals from IT, HR, and Finance systems  
        - Routes them through **TriNexa**, the global orchestrator  
        - Delegates tasks to specialized agents (IT, HR, Finance, Architect, Security, Ops)  
        - Aggregates resolutions and surfaces them back in one unified workspace
        """
    )

    st.markdown("### Domains")
    st.markdown(
        """
        <span class="agent-badge">IT Service Desk</span>
        <span class="agent-badge">HR & People Ops</span>
        <span class="agent-badge">Finance & Spend</span>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown("### Status")

    st.markdown(
        f"""
        <div class="tr-card" style="border-left: 4px solid {PALETTE['teal']}">
            <strong>UI shell</strong><br/>
            Online in Streamlit, using the TriResolveAI brand system.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        f"""
        <div class="tr-card" style="border-left: 4px solid {PALETTE['gold']}">
            <strong>Backend orchestration</strong><br/>
            FastAPI + Azure OpenAI orchestrator (TriNexa) wiring in progress.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        f"""
        <div class="tr-card" style="border-left: 4px solid {PALETTE['coral']}">
            <strong>Agents</strong><br/>
            HR, IT, Finance agents configured in Azure AI Foundry, with space
            to add Architect, Security, and Ops.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "Use the sidebar to navigate to **Maps**, **Assistant (TriNexa)**, and **About**."
)
