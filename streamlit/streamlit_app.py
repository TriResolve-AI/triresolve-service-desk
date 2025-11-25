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
)

# --- OVERVIEW SECTION ---
if nav == "Overview":
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
        st.success("UI shell: online")
        st.info("Backend orchestration: coming next")
        st.info("Agent skills: to be wired to Azure OpenAI / SK")

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

# --- MAPS SECTION ---
elif nav == "Maps":
    st.header("Agent & Workflow Maps")

    st.markdown(
        """
        This section will show **visual maps** of how TriNexa routes work:

        - Event → Orchestrator (TriNexa) → Domain agent  
        - Escalation paths & fallbacks  
        - Real-time status of in-flight tickets  

        For the hackathon, this will likely be backed by a simple data model and
        one or more diagrams (e.g., Mermaid, images, or Streamlit charts).
        """
    )

    st.info("Placeholder: we’ll plug in the architecture diagram + runbooks from `/docs` here.")

# --- ASSISTANT (TRINEXA) SECTION ---
elif nav == "Assistant (TriNexa)":
    st.header("TriNexa Assistant")

    st.write(
        """
        This is the **front door** to the orchestration layer.

        For now, it's a local placeholder UI.  
        Later, it will call your Azure OpenAI / Semantic Kernel backend to:
        - Classify intent  
        - Route to IT / HR / Finance agents  
        - Aggregate responses back to the user
        """
    )

    user_input = st.text_input("Ask TriNexa something:", placeholder="e.g. 'Reset my VPN access' or 'Where is my reimbursement?'")

    if user_input:
        st.markdown("### Prototype response")
        st.write(
            f"""
            _(Mock)_ TriNexa would:

            1. Classify: understand this as `\"{user_input}\"`
            2. Decide which domain agent to call (IT / HR / Finance)
            3. Orchestrate one or more tool calls
            4. Return the summarized resolution here
            """
        )

# --- ABOUT SECTION ---
elif nav == "About":
    st.header("About TriResolve AI & TriNexa")

    st.write(
        """
        **TriResolve AI** is a multi-agent service desk platform built for the hackathon.

        - **TriResolve AI** = the user-facing workspace  
        - **TriNexa** = the orchestration brain that coordinates domain agents  
        - **Agents** = IT, HR, Finance (and future domains)  

        The goal is to show how a **single assistant** can safely route and resolve
        work across multiple teams, powered by Azure, Semantic Kernel, and an
        extensible agent architecture.
        """
    )

    st.markdown("---")
    st.caption("Hackathon build • This page will evolve as the architecture solidifies.")
