from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

import streamlit as st

# ---------------------------------------------------------------------
# Ensure both /streamlit and repo root are on sys.path
# ---------------------------------------------------------------------
HERE = Path(__file__).resolve()
STREAMLIT_DIR = HERE.parents[1]   # .../streamlit
ROOT = HERE.parents[2]            # repo root

for p in (STREAMLIT_DIR, ROOT):
    if str(p) not in sys.path:
        sys.path.append(str(p))

from theme import PALETTE, inject_base_css  # type: ignore
from config import settings  # type: ignore
from backend.services.azure_client import (  # type: ignore
    orchestrator_chat,
    domain_agent_chat,
)

# ---------------------------------------------------------------------
# Fallback department colors
# ---------------------------------------------------------------------
try:
    from theme import DEPT_COLORS  # type: ignore
except Exception:
    DEPT_COLORS = {
        "IT": PALETTE["coral"],
        "HR": PALETTE["gold"],
        "Finance": PALETTE["teal"],
    }

# ---------------------------------------------------------------------
# Fake response for Dev Mode (no Azure calls)
# ---------------------------------------------------------------------
def fake_orchestrator_response(payload: Dict[str, Any], dept: str) -> Dict[str, Any]:
    if dept == "Auto":
        dept = "IT"

    summary = (payload.get("description") or "")[:80] + "..."
    return {
        "classification": {
            "department": dept,
            "confidence": 0.92,
            "rationale": (
                "Dev mode: canned classification response. "
                "In live mode, the TriNexa classifier + orchestrator would "
                "evaluate and route this ticket."
            ),
        },
        "response": {
            "agent_name": f"{dept} Agent",
            "department": dept,
            "summary": f"Dev-mode response for {dept}. Summary: {summary}",
            "steps": (
                "- This is a simulated response because Dev Mode is enabled.\n"
                f"- In live mode, TriNexa would invoke the {dept} domain agent "
                "through Azure OpenAI.\n"
            ),
        },
    }


# ---------------------------------------------------------------------
# Shared styles
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
# Dev mode toggle (UI + global setting)
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

# Also mirror into env so azure_client can see it if needed
os.environ["TRIRESOLVE_DEV_MODE"] = "true" if effective_dev_mode else "false"

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
                ✅ Live Mode — calling the TriNexa orchestrator pipeline via Azure OpenAI (SDK).
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------
# Department selector buttons (original behavior)
# ---------------------------------------------------------------------
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Auto"

st.markdown(
    "<p class='section-label'>Choose a department (optional)</p>",
    unsafe_allow_html=True,
)
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
        btn_type = "primary" if selected else "secondary"
        # We keep use_container_width for now; the deprecation is just a warning.
        if st.button(
            label,
            type=btn_type,
            key=f"dept_{domain}",
            use_container_width=True,
        ):
            st.session_state.selected_domain = domain

st.markdown("---")

# ---------------------------------------------------------------------
# Ticket Form + Orchestrator Response
# ---------------------------------------------------------------------
col_form, col_result = st.columns([1.2, 1.8])

with col_form:
    title = st.text_input("Short summary", placeholder="e.g. 'password reset'")
    description = st.text_area(
        "Details",
        placeholder="Explain what's happening...",
        height=150,
    )
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Critical"],
        index=1,
    )

    submit = st.button("Submit to TriNexa", type="primary", key="submit_ticket")

with col_result:
    st.markdown("### Orchestrator Response")

    if submit:
        if not title and not description:
            st.warning("Please provide at least a summary or details for your ticket.")
        else:
            payload = {
                "title": title or "(no title)",
                "description": description or "(no description)",
                "priority": priority,
                "domain": st.session_state.selected_domain,
            }

            selected = st.session_state.selected_domain

            # Build a unified message string for the models
            user_message = (
                f"Title: {payload['title']}\n"
                f"Priority: {priority}\n"
                f"Details: {payload['description']}"
            )

            try:
                with st.spinner("Processing request via TriNexa..."):
                    if effective_dev_mode:
                        data = fake_orchestrator_response(payload, selected)
                        clf = data.get("classification", {}) or {}
                        agent = data.get("response", {}) or {}
                    else:
                        # Live SDK call: orchestrator or specific domain agent
                        if selected == "Auto":
                            reply_text = orchestrator_chat(user_message)
                            routed = "Auto (orchestrator decides)"
                        else:
                            reply_text = domain_agent_chat(
                                user_message,
                                domain=selected.lower(),
                            )
                            routed = selected

                        # Synthesize a classification/agent structure for the UI
                        clf = {
                            "department": routed,
                            "confidence": "—",
                            "rationale": (
                                "Live mode: routed using Azure OpenAI deployments. "
                                "For this UI, routing metadata is inferred from your selection."
                            ),
                        }
                        agent = {
                            "agent_name": "TriNexa Assistant",
                            "department": routed,
                            "summary": reply_text,
                            "steps": "",
                        }

            except Exception as exc:  # noqa: BLE001
                st.error(
                    "⚠️ Error calling Azure OpenAI. "
                    "Please verify your AZURE_OPENAI_* settings in Streamlit secrets.\n\n"
                    f"Details: {exc}"
                )
            else:
                # Classification card
                st.markdown(
                    f"""
                    <div class="tr-card" style="border-left: 4px solid {PALETTE['deep_blue']}">
                        <strong>Classification</strong><br/>
                        Department: <b>{clf.get('department','—')}</b><br/>
                        Confidence: {clf.get('confidence','—')}</b><br/>
                        <div style="font-size:0.85rem; opacity:0.9;">
                            {clf.get('rationale','')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                dept = (
                    agent.get("department")
                    or clf.get("department")
                    or payload.get("domain")
                    or "—"
                )
                dept_color = DEPT_COLORS.get(dept, PALETTE["deep_blue"])

                # Agent card
                st.markdown(
                    f"""
                    <div class="tr-card" style="border-left: 4px solid {dept_color}">
                        <strong>Agent:</strong> {agent.get('agent_name','—')}<br/>
                        <strong>Department:</strong> {dept}<br/><br/>
                        <strong>Summary</strong><br/>
                        {agent.get('summary','—')}<br/><br/>
                        <strong>Recommended Steps</strong><br/>
                        <pre style="white-space:pre-wrap; font-size:0.85rem;">
{(agent.get('steps') or '').strip()}
                        </pre>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("Raw data (debug)"):
                    st.json({"classification": clf, "response": agent})

