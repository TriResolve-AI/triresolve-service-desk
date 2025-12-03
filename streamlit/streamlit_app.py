# streamlit/streamlit_app.py

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make repo root importable so we can use theme, etc.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from theme import inject_base_css  # type: ignore

st.set_page_config(
    page_title="TriResolve AI Service Desk",
    page_icon="🧩",
    layout="wide",
)

inject_base_css()

# ---------------------- UI ---------------------- #

st.title("TriResolve AI – Service Desk")

st.write(
    """
Welcome to **TriResolve AI**, powered by the **TriNexa** multi-agent orchestrator.

Use the sidebar on the left to explore:

- 🗺 **Maps** – architecture & workflow visualizations  
- 🤖 **Assistant** – front door into the TriNexa orchestrator  
- ℹ️ **About** – project context, team, and tech stack  

This app showcases how we:
- Use **Azure OpenAI** deployments (gpt-4.1, gpt-4o, gpt-4.1-mini)  
- Combine **IT / HR / Finance / Specialist agents** behind a single assistant  
- Keep a path open to **Azure AI Foundry workflows** for future orchestration
"""
)

st.markdown("---")

col1, col2 = st.columns([1.4, 1])

with col1:
    st.subheader("How to use this demo")

    st.markdown(
        """
1. Go to **Assistant** in the sidebar.  
2. Describe an issue (e.g., *“Need VPN after password reset”*).  
3. Optionally choose a department (IT / HR / Finance) or leave on **Auto**.  
4. Submit and see how TriNexa responds.

Behind the scenes, the Assistant page calls our **Azure OpenAI** deployments
via a shared backend client.  
"""
    )

with col2:
    st.subheader("Tech stack (high-level)")
    st.markdown(
        """
- **Streamlit** UI  
- **Azure OpenAI** (gpt-4.1, gpt-4o, gpt-4.1-mini)  
- **Python backend helpers** (`backend/services/azure_client.py`)  
- **Azure AI Foundry project** (`trinexa-foundry`) for agents & workflows
"""
    )
