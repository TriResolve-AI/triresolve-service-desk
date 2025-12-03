# streamlit/pages/2_Assistant.py

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from openai import AzureOpenAI  # make sure `openai` package is installed

# ---------------------------------------------------------------------
# Path setup: ensure both /streamlit and repo root are importable
# ---------------------------------------------------------------------
HERE = Path(__file__).resolve()
STREAMLIT_DIR = HERE.parents[1]   # .../streamlit
ROOT = HERE.parents[2]            # repo root

for p in (STREAMLIT_DIR, ROOT):
    s = str(p)
    if s not in sys.path:
        sys.path.append(s)

from theme import PALETTE, inject_base_css  # type: ignore
from config import settings  # type: ignore

# ---------------------------------------------------------------------
# Azure OpenAI client (Next-gen SDK)
# ---------------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint=settings.openai_endpoint,
    api_key=settings.openai_api_key,
    api_version=settings.openai_api_version,
)

ORCHESTRATOR_MODEL = settings.d_orchestrator  # e.g. "gpt-4.1"


def call_orchestrator_chat(message: str, department: str | None = None) -> str:
    """Call Azure OpenAI directly as our 'orchestrator' brain."""
    system_parts = [
        "You are TriNexa, the orchestrator for the TriResolve AI service desk.",
        "You classify requests and respond with clear, actionable steps.",
        "You support the IT, HR, and Finance departments.",
    ]
    if department and department != "Auto":
        system_parts.append(f"Treat this as a {department} ticket.")

    system_prompt = " ".join(system_parts)

    resp = client.chat.completions.create(
        model=ORCHESTRATOR_MODEL,
        temperature=0.3,
        max_tokens=600,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    )
    return resp.choices[0].message.content or ""


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
                "In live mode, TriNexa (gpt-4.1) would classify and route this ticket."
            ),
        },
        "response": {
            "agent_name": f"{dept} Agent",
            "department": dept,
            "summary": f"Dev-mode response for {dept}. Summary: {summary}",
            "steps": (
                "- This is a simulated response because Dev Mode is enabled.\n"
                f"- In live mode, TriNexa would call Azure OpenAI ({dept} context).\n"
            ),
        },
    }


# ---------------------------------------------------------------------
# Shared styles & page header
# ---------------------------------------------------------------------
inject_base_css()

st.title("🧩 TriNexa Assistant")

st.write(
    """
This is the **front door** to the orchestration layer.

TriNexa will:
- Classify intent  
- Route to IT / HR / Finance agents  
- Aggregate responses back to the user  
"""
)

# ---------------------------------------------------------------------
# Dev mode toggle (UI + env flag)
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
                ✅ Live Mode — calling Azure OpenAI (gpt-4.1) via the TriNexa orchestrator.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------
# Department selector buttons
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
            dept = st.session_state.selected_domain
            payload = {
                "title": title or "(no title)",
                "description": description or "(no description)",
                "priority": priority,
                "department": dept,
            }

            try:
                if effective_dev_mode:
                    data = fake_orchestrator_response(payload, dept)
                else:
                    user_message = (
                        f"Title: {payload['title']}\n"
                        f"Priority: {priority}\n"
                        f"Department selection: {dept}\n"
                        f"Details: {payload['description']}"
                    )
                    reply_text = call_orchestrator_chat(user_message, dept)

                    data = {
                        "classification": {
                            "department": dept if dept != "Auto" else "Auto (orchestrator decides)",
                            "confidence": "—",
                            "rationale": (
                                "Live mode: classified and answered using Azure OpenAI "
                                f"model '{ORCHESTRATOR_MODEL}'."
                            ),
                        },
                        "response": {
                            "agent_name": "TriNexa Assistant",
                            "department": dept,
                            "summary": reply_text,
                            "steps": "",
                        },
                    }

            except Exception as exc:  # noqa: BLE001
                st.error(
                    "⚠️ Error calling Azure OpenAI. "
                    "Please verify your AZURE_OPENAI_* settings in Streamlit secrets.\n\n"
                    f"Details: {exc}"
                )
            else:
                clf = data.get("classification", {}) or {}
                agent = data.get("response", {}) or {}

                # Classification card
                st.markdown(
                    f"""
                    <div class="tr-card" style="border-left: 4px solid {PALETTE['deep_blue']}">
                        <strong>Classification</strong><br/>
                        Department: <b>{clf.get('department','—')}</b><br/>
                        Confidence: {clf.get('confidence','—')}<br/>
                        <div style="font-size:0.85rem; opacity:0.9;">
                            {clf.get('rationale','')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                resolved_dept = (
                    agent.get("department")
                    or clf.get("department")
                    or payload.get("department")
                    or "—"
                )
                dept_color = DEPT_COLORS.get(resolved_dept, PALETTE["deep_blue"])

                # Agent card
                st.markdown(
                    f"""
                    <div class="tr-card" style="border-left: 4px solid {dept_color}">
                        <strong>Agent:</strong> {agent.get('agent_name','—')}<br/>
                        <strong>Department:</strong> {resolved_dept}<br/><br/>
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
                    st.json(data)
