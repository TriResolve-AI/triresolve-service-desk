from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

import streamlit as st

# ---------------------------------------------------------------------
# Make repo root importable so we can use config + backend helpers
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from theme import PALETTE, inject_base_css  # type: ignore
from config import settings  # type: ignore
from backend.services.azure_client import (  # type: ignore
    orchestrator_chat,
    domain_agent_chat,
)

# ---------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------
inject_base_css()

st.title("🧩 TriNexa Assistant")

st.write(
    """
    This is the **front door** to the orchestration layer.

    TriNexa will eventually:
    - Classify intent  
    - Route to IT / HR / Finance agents  
    - Aggregate responses back to the user  
    """
)

# ---------------------------------------------------------------------
# Dev mode toggle (global + per-session)
# ---------------------------------------------------------------------
if "force_dev_mode" not in st.session_state:
    st.session_state.force_dev_mode = False

col1, col2 = st.columns([1.2, 3])

with col1:
    st.checkbox(
        "Force Dev Mode (local demo)",
        key="force_dev_mode",
        help="Use canned responses instead of calling Azure OpenAI.",
    )

effective_dev_mode = settings.DEV_MODE or st.session_state.force_dev_mode

with col2:
    if effective_dev_mode:
        st.markdown(
            """
            <div class="tri-banner tri-banner-dev">
                🧪 Dev Mode Active — using canned responses (no live Azure calls).
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="tri-banner tri-banner-live">
                ✅ Live Mode — calling the TriNexa orchestrator via Azure OpenAI (SDK).
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------
# Department selector
# ---------------------------------------------------------------------
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Auto"

st.markdown("<p class='section-label'>Choose a department (optional)</p>", unsafe_allow_html=True)
cols = st.columns(4)

buttons = [
    ("Auto", "Auto"),
    ("IT Agent", "IT"),
    ("HR Agent", "HR"),
    ("Finance Agent", "Finance"),
]

for col, (label, domain) in zip(cols, buttons):
    with col:
        selected = st.session_state.selected_domain == domain
        if st.button(
            label,
            type="primary" if selected else "secondary",
            key=f"dept_{domain}",
            kwargs=None,
        ):
            st.session_state.selected_domain = domain

st.markdown("---")

# ---------------------------------------------------------------------
# Ticket form + response area
# ---------------------------------------------------------------------
col_form, col_result = st.columns([1.2, 1.8])

with col_form:
    title = st.text_input("Short summary", placeholder="e.g. 'password reset'")
    description = st.text_area(
        "Details",
        placeholder="Explain what's happening...",
        height=150,
    )
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], index=1)

    submit = st.button("Submit to TriNexa", type="primary")

with col_result:
    st.markdown("### Orchestrator Response")

    if submit:
        if not description and not title:
            st.warning("Please enter a short summary or some details first.")
        else:
            # Build a unified message for the orchestrator/agents
            user_message = (
                f"Title: {title or 'N/A'}\n"
                f"Priority: {priority}\n"
                f"Details: {description or 'N/A'}"
            )

            selected = st.session_state.selected_domain

            try:
                with st.spinner("Processing request via TriNexa..."):
                    if effective_dev_mode:
                        # Let azure_client's dev-mode logic produce a canned reply
                        reply_text = orchestrator_chat(user_message)
                        routed_domain = "Dev (simulated)"
                    else:
                        if selected == "Auto":
                            reply_text = orchestrator_chat(user_message)
                            routed_domain = "Auto (orchestrator decides)"
                        else:
                            # Route directly to the chosen domain agent
                            reply_text = domain_agent_chat(
                                user_message,
                                domain=selected.lower(),
                            )
                            routed_domain = selected

            except Exception as exc:  # noqa: BLE001
                st.error(
                    "⚠️ Error calling Azure OpenAI. "
                    "Please verify your AZURE_OPENAI_* settings in Streamlit secrets.\n\n"
                    f"Details: {exc}"
                )
            else:
                # Very simple "classification" summary using UI state
                st.markdown(
                    f"""
                    <div class="tr-card" style="border-left: 4px solid {PALETTE['deep_blue']}">
                        <strong>Routing</strong><br/>
                        Mode: <b>{"Dev" if effective_dev_mode else "Live"}</b><br/>
                        Department (requested): <b>{selected}</b><br/>
                        Department (routed): <b>{routed_domain}</b><br/>
                        <div style="font-size:0.85rem; opacity:0.9; margin-top:0.5rem;">
                            (For this hackathon UI, routing metadata is inferred from your selection.
                            The full classifier + workflow logic lives in the backend / Foundry project.)
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Main assistant reply
                st.markdown(
                    f"""
                    <div class="tr-card" style="border-left: 4px solid {PALETTE['coral']}">
                        <strong>Assistant Reply</strong><br/>
                        <div style="white-space:pre-wrap; font-size:0.95rem; margin-top:0.5rem;">
                            {reply_text}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
