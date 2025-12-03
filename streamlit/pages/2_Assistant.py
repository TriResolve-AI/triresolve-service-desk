# streamlit/pages/2_Assistant.py

from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Dict, Any

import streamlit as st
import requests

# ---------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------
HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
STREAMLIT_DIR = HERE.parents[1]

for p in (ROOT, STREAMLIT_DIR):
    if str(p) not in sys.path:
        sys.path.append(str(p))

from theme import PALETTE, inject_base_css  # type: ignore
from config import settings  # type: ignore
from backend.services.azure_client import orchestrator_chat, domain_agent_chat  # type: ignore

# ---------------------------------------------------------------
# Colors
# ---------------------------------------------------------------
try:
    from theme import DEPT_COLORS  # type: ignore
except Exception:
    DEPT_COLORS = {
        "IT": PALETTE["coral"],
        "HR": PALETTE["gold"],
        "Finance": PALETTE["teal"],
    }

# ---------------------------------------------------------------
# Foundry Workflow Calling
# ---------------------------------------------------------------
WORKFLOW_NAME = "trinexa-classify-orchestrate"
WORKFLOW_API_VERSION = "2025-11-15-preview"

def build_foundry_url() -> str:
    base = settings.aiproject_endpoint.rstrip("/")
    return (
        f"{base}/applications/{WORKFLOW_NAME}"
        f"/protocols/activityprotocol"
        f"?api-version={WORKFLOW_API_VERSION}"
    )

def call_foundry_workflow(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Calls Azure AI Foundry workflow correctly."""
    url = build_foundry_url()
    api_key = settings.aiproject_api_key  # ✔ Correct key

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    body = {"input": payload}

    resp = requests.post(url, json=body, headers=headers, timeout=40)
    if not resp.ok:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise RuntimeError(f"Error {resp.status_code}: {detail}")

    data = resp.json()
    return data.get("outputs") or data


# ---------------------------------------------------------------
# Dev mode fallback for demos
# ---------------------------------------------------------------
def fake_response(payload: Dict[str, Any], dept: str):
    if dept == "Auto":
        dept = "IT"

    summary = (payload["description"] or "")[:80]
    return {
        "classification": {
            "department": dept,
            "confidence": 0.99,
            "rationale": "Dev mode activated.",
        },
        "response": {
            "agent_name": f"{dept} Agent",
            "department": dept,
            "summary": f"Simulated summary for {dept}: {summary}",
            "steps": "- This is a simulated response.\n- Azure not called.\n",
        },
    }


# ---------------------------------------------------------------
# UI
# ---------------------------------------------------------------
inject_base_css()
st.title("🧩 TriNexa Assistant")

# Dev mode toggle
if "force_dev_mode" not in st.session_state:
    st.session_state.force_dev_mode = False

dev_col, banner_col = st.columns([1.2, 3])
with dev_col:
    st.checkbox("Force Dev Mode", key="force_dev_mode")

effective_dev = settings.DEV_MODE or st.session_state.force_dev_mode
os.environ["TRIRESOLVE_DEV_MODE"] = "true" if effective_dev else "false"

with banner_col:
    if effective_dev:
        st.markdown(
            "<div class='tri-banner tri-banner-dev'>🧪 Dev Mode Active</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='tri-banner tri-banner-live'>✅ Live Mode Enabled</div>",
            unsafe_allow_html=True,
        )

# Department buttons
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Auto"

st.markdown("<p class='section-label'>Choose a department</p>", unsafe_allow_html=True)
colA, colB, colC, colD = st.columns(4)

for col, (label, val) in zip(
    (colA, colB, colC, colD),
    [("Auto", "Auto"), ("IT Agent", "IT"), ("HR Agent", "HR"), ("Finance Agent", "Finance")],
):
    with col:
        selected = st.session_state.selected_domain == val
        if st.button(label, type="primary" if selected else "secondary", use_container_width=True):
            st.session_state.selected_domain = val

st.markdown("---")

# Form
col_form, col_res = st.columns([1.2, 1.8])

with col_form:
    title = st.text_input("Short summary")
    description = st.text_area("Details", height=150)
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], index=1)
    submit = st.button("Submit", type="primary")

with col_res:
    st.markdown("### Orchestrator Response")

    if submit:
        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "department": st.session_state.selected_domain,
        }

        if effective_dev:
            result = fake_response(payload, st.session_state.selected_domain)
        else:
            try:
                result = call_foundry_workflow(payload)
            except Exception as e:
                st.error(f"⚠️ Error calling Foundry workflow:<br>{e}", unsafe_allow_html=True)
                st.stop()

        clf = result.get("classification", {})
        agent = result.get("response", {})

        # Classification card
        st.markdown(
            f"""
            <div class="tr-card" style="border-left: 4px solid {PALETTE['deep_blue']}">
                <strong>Classification</strong><br/>
                Department: <b>{clf.get('department')}</b><br/>
                Confidence: {clf.get('confidence')}</b><br/>
                <div style="font-size:0.85rem;">{clf.get('rationale')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        dept = agent.get("department") or clf.get("department")
        color = DEPT_COLORS.get(dept, PALETTE["deep_blue"])

        st.markdown(
            f"""
            <div class="tr-card" style="border-left: 4px solid {color}">
                <strong>Agent:</strong> {agent.get('agent_name')}<br/>
                <strong>Department:</strong> {dept}<br/><br/>
                <strong>Summary</strong><br/>{agent.get('summary')}<br/><br/>
                <strong>Recommended Steps</strong><br/>
                <pre>{agent.get('steps')}</pre>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Raw output (debug)"):
            st.json(result)
