# streamlit/streamlit_app.py

import streamlit as st

# -------------------------------------------------------------------
# Brand palette (match Maps page)
# -------------------------------------------------------------------
PALETTE = {
    "deep_blue": "#00547D",     # header / chip
    "teal": "#1FB7A6",          # teal loop
    "gold": "#F3B147",          # gold loop
    "coral": "#F2654C",         # coral loop
    "soft_cream": "#FFF7E8",    # main background
    "ink": "#121826",           # dark text
}

st.set_page_config(
    page_title="TriResolve AI – Service Desk Platform",
    page_icon="🧠",
    layout="wide",
)

# -------------------------------------------------------------------
# Global CSS – fix contrast + layout
# -------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    /* App background */
    div.block-container {{
        background-color: {PALETTE["soft_cream"]};
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
    }}

    /* Sidebar gradient */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            {PALETTE["deep_blue"]} 0%,
            {PALETTE["teal"]} 100%
        );
    }}

    /* Global text colour (fix white-on-cream issue) */
    body, p, li, span, div, label {{
        color: {PALETTE["ink"]} !important;
    }}

    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: {PALETTE["ink"]} !important;
        font-weight: 700;
    }}

    /* Hero strip at the top */
    .triresolve-hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.2rem 0.8rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.7);
        color: {PALETTE["deep_blue"]};
        font-size: 0.8rem;
        font-weight: 600;
    }}

    .triresolve-hero-title {{
        font-size: 2.4rem;
        font-weight: 800;
        margin-top: 0.4rem;
        margin-bottom: 0.25rem;
    }}

    .triresolve-hero-subtitle {{
        font-size: 1rem;
        font-weight: 500;
        color: {PALETTE["deep_blue"]};
        opacity: 0.95;
    }}

    /* Status cards on the right */
    .status-card {{
        padding: 1.25rem 1.5rem;
        border-radius: 1.25rem;
        background: #FFFFFF;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
        border-left: 4px solid transparent;
        color: {PALETTE["ink"]};
    }}
    .status-card h4 {{
        margin: 0 0 0.25rem 0;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {PALETTE["deep_blue"]};
    }}
    .status-card p {{
        margin: 0;
        font-size: 0.9rem;
    }}

    .status-card--ui {{
        border-left-color: {PALETTE["teal"]};
    }}
    .status-card--backend {{
        border-left-color: {PALETTE["gold"]};
    }}
    .status-card--agents {{
        border-left-color: {PALETTE["coral"]};
    }}

    /* Domain pills */
    .domain-pill {{
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(0,0,0,0.06);
        background: #FFFFFF;
        font-size: 0.85rem;
        font-weight: 500;
        color: {PALETTE["deep_blue"]};
        margin-right: 0.4rem;
        margin-bottom: 0.3rem;
    }}

    .section-label {{
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.8rem;
        color: rgba(15,23,42,0.65);
        margin-bottom: 0.4rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# Main layout
# -------------------------------------------------------------------
st.markdown(
    """
    <div class="triresolve-hero-badge">
        <span>TriResolveAI</span>
        <span>Service Desk</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="triresolve-hero-title">
        TriResolve AI – Service Desk Platform
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="triresolve-hero-subtitle">
        Powered by <strong>TriNexa</strong>, your multi-domain orchestrator for IT, HR, and Finance.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")  # spacer

left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    st.write(
        """
        TriResolve AI is your **multi-agent service desk layer**:

        - Ingests tickets and signals from IT, HR, and Finance systems  
        - Routes them through **TriNexa**, the global orchestrator  
        - Delegates tasks to specialized agents (IT, HR, Finance, Architect, Security, Ops)  
        - Aggregates resolutions and surfaces them back in one unified workspace  
        """
    )

    st.markdown('<div class="section-label">Domains</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <span class="domain-pill">IT Service Desk</span>
        <span class="domain-pill">HR &amp; People Ops</span>
        <span class="domain-pill">Finance &amp; Spend</span>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<div class="section-label">Status</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="status-card status-card--ui">
            <h4>UI shell</h4>
            <p>Online in Streamlit, using the TriResolveAI brand system.</p>
        </div>
        <div class="status-card status-card--backend">
            <h4>Backend orchestration</h4>
            <p>FastAPI + Azure OpenAI orchestrator (TriNexa) wiring in progress.</p>
        </div>
        <div class="status-card status-card--agents">
            <h4>Agents</h4>
            <p>HR, IT, Finance agents configured in Azure AI Foundry with space to add Architect, Security, and Ops.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "Use the sidebar to navigate to **Maps**, **Assistant (TriNexa)**, and **About**."
)
