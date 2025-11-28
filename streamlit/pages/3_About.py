# streamlit/pages/3_About.py

from pathlib import Path

import streamlit as st

from theme import PALETTE, inject_base_css

inject_base_css()

st.title("ℹ️ About TriResolve AI & TriNexa")

logo_path = Path(__file__).resolve().parents[1] / "assets" / "triresolve_logo.png"
if logo_path.exists():
    st.image(str(logo_path), width=140)

st.write(
    """
    **TriResolve AI** is a multi-agent service desk platform built for the hackathon.

    - **TriResolve AI** = the user-facing workspace in Streamlit  
    - **TriNexa** = the orchestration brain that coordinates domain agents  
    - **Agents** = IT, HR, Finance (and future domains like Architect, Security, Ops)  

    The goal is to show how a **single assistant** can safely route and resolve
    work across multiple teams, powered by Azure, Semantic Kernel, and an
    extensible agent architecture.
    """
)

st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    st.markdown("<p class='section-label'>Tech Stack</p>", unsafe_allow_html=True)
    st.write(
        """
        - **Frontend:** Streamlit (Python)  
        - **Backend:** FastAPI  
        - **AI:** Azure OpenAI (or Azure AI Foundry)  
        - **Orchestration:** TriNexa multi-agent router  
        """
    )

with c2:
    st.markdown("<p class='section-label'>Design Principles</p>", unsafe_allow_html=True)
    st.write(
        """
        - Human-friendly ticket summaries and next steps  
        - Clear routing and ownership across departments  
        - Extensible agent model for new domains and tools  
        - Enterprise-ready: logging, observability, and runbooks  
        """
    )

st.markdown("---")
st.caption("Hackathon build • This page will evolve as the architecture solidifies.")
