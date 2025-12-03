from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

import requests
import streamlit as st

# -------------------------------------------------------------------
# Ensure both repo root and /streamlit on sys.path
# -------------------------------------------------------------------
HERE = Path(__file__).resolve()
STREAMLIT_DIR = HERE.parents[1]  # .../streamlit
ROOT = HERE.parents[2]           # repo root

for p in (STREAMLIT_DIR, ROOT):
    if str(p) not in sys.path:
        sys.path.append(str(p))

from theme import PALETTE, inject_base_css  # type: ignore
from config import settings  # type: ignore

# -------------------------------------------------------------------
# Foundry (Azure AI Project) configuration
# -------------------------------------------------------------------
# Base project endpoint, e.g.
#   https://trinexa-openai.services.ai.azure.com/api/projects/trinexa-foundry
AIPROJECT_BASE = (settings.aiproject_endpoint or "").rstrip("/")

# Your workflow application name in Foundry
WORKFLOW_APP_NAME = "trinexa-classify-orchestrate"

# API version for Activity Protocol
WORKFLOW_API_VERSION = "2025-11-15-preview"


def get_foundry_workflow_url() -> str:
    """
    Build the ActivityProtocol URL for the TriNexa orchestrator workflow.
    """
    if not AIPROJECT_BASE:
        raise RuntimeError(
            "AZURE_AIPROJECT_ENDPOINT is not configured. "
            "Set it in Streamlit secrets under [azure]."
        )

    return (
        f"{AIPROJECT_BASE}"
        f"/applications/{WORKFLOW_APP_NAME}"
        f"/protocols/activityprotocol"
        f"?api-version={WORKFLOW_API_VERSION}"
    )


def call_trinexa_workflow(ticket_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call the TriNexa Foundry workflow via ActivityProtocol.

    ticket_payload is the UI payload:
        {title, description, priority, domain}
    """
    url = get_foundry_workflow_url()

    # Prefer a dedicated project key if provided; fall back to OpenAI key.
    api_key = settings.aiproject_resource_id or settings.openai_api_key
    if not api_key:
        raise RuntimeError(
            "No Foundry API key configured. Set AZURE_AIPROJECT_RESOURCE_ID or "
            "AZURE_OPENAI_API_KEY in Streamlit secrets."
        )

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    body = {
        "input": {
            "title": ticket_payload.get("title"),
            "description": ticket_payload.get("description"),
            "priority": ticket_payload.get("priority"),
            "department": ticket_payload.get("domain"),
            # Also pass full ticket in case the workflow expects `ticket`.
            "ticket": ticket_payload,
        }
    }

    resp = requests.post(url, json=body, headers=headers, timeout=40)
    if not resp.ok:
        try:
            err_json = resp.json()
        except Exception:
            err_json = resp.text
        raise RuntimeError(f"Error code: {resp.status_code} - {err_json}")

    data = resp.json()
    # Standard ActivityProtocol response shape:
    #   { "status": "...", "outputs": { ... } }
    outputs = data.get("outputs") or data
    return outputs


# -------------------------------------------------------------------
# Fake response for Dev Mode (no Foundry call)
# -------------------------------------------------------------------
def fake_orchestrator_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    dept = payload.get("domain") or "IT"
    if dept == "Auto":
        dept = "IT"

    summary = (payload.get("description") or "")[:80] + "..."
    return {
        "classification": {
            "department": dept,
            "confidence": 0.92,
            "rationale": (
                "Dev mode: canned classification response. "
                "In live mode, the TriNexa workflow would classify this ticket."
            ),
        },
        "response": {
            "agent_name": f"{dept} Agent",
            "department": dept,
            "summary": f"Dev-mode response for {dept}. Summary: {summary}",
            "steps": (
                "- This is a simulated response because Dev Mode is enabled "
                "or Foundry is unreachable.\n"
                f"- In live mode, the workflow would invoke the {dept} agent.\n"
                "- Use this for demoing the UI when Azure is offline.\n"
            ),
        },
    }


# -------------------------------------------------------------------
# Department color fallback (in case theme.DEPT_COLORS missing)
# -------------------------------------------------------------------
try:
    from theme import DEPT_COLORS  # type: ignore
except Exception:
    DEPT_COLORS = {
        "IT": PALETTE["coral"],
        "HR": PALETTE["gold"],
        "Finance": PALETTE["teal"],
    }

# -------------------------------------------------------------------
# Shared styles
# -------------------------------------------------------------------
inject_base_css()

# -------------------------------------------------------------------
# UI Header
# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# Dev mode toggle (no backend health check anymore)
# -------------------------------------------------------------------
if "force_dev_mode" not in st.session_state:
    st.session_state.force_dev_mode = False

col1, col2 = st.columns([1.2, 3])

with col1:
    st.checkbox(
        "Force Dev Mode (local demo)",
        key="force_dev_mode",
        help="Use canned responses instead of calling the Foundry workflow.",
    )

effective_dev_mode = bool(st.session_state.force_dev_mode)

with col2:
    if effective_dev_mode:
        st.markdown(
            """
            <div class="tri-banner tri-banner-dev">
                🧪 Dev Mode Active — using canned responses (no Foundry calls).
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="tri-banner tri-banner-live">
                ✅ Live Mode — calling the TriNexa orchestrator workflow
                (Azure AI Foundry).
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------------------------------------------------------------------
# Department selector buttons
# -------------------------------------------------------------------
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
        # We'll live with the deprecation warning for use_container_width;
        # this keeps the layout nice for now.
        if st.button(
            label,
            type=btn_type,
            key=f"dept_{domain}",
            use_container_width=True,
        ):
            st.session_state.selected_domain = domain

st.markdown("---")

# -------------------------------------------------------------------
# Ticket Form
# -------------------------------------------------------------------
col_form, col_result = st.columns([1.2, 1.8])

with col_form:
    title = st.text_input("Short summary", placeholder="e.g. 'password reset'")
    description = st.text_area(
        "Details",
        placeholder="Explain what's happening...",
        height=150,
    )
    priority = st.selectbox(
        "Priority", ["Low", "Medium", "High", "Critical"], index=1
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

            with st.spinner("Processing request via TriNexa..."):
                try:
                    if effective_dev_mode:
                        data = fake_orchestrator_response(payload)
                    else:
                        data = call_trinexa_workflow(payload)
                except Exception as exc:
                    st.error(
                        f"⚠️ Error running TriNexa orchestrator:\n\n{exc}"
                    )
                    st.stop()

            clf = data.get("classification", {}) or {}
            agent = data.get("response", {}) or {}

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

            with st.expander("Raw workflow outputs (debug)"):
                st.json(data)
