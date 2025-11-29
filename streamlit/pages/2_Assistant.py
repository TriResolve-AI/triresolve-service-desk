# streamlit/pages/2_Assistant.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import os
import sys

import requests
import streamlit as st

# ---------------------------------------------------------------------
# Ensure repo root is on sys.path (for theme imports, etc.)
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from theme import PALETTE, inject_base_css  # DEPT_COLORS comes via fallback below

# ---------------------------------------------------------------------
# Department colors (match Maps page intent)
# ---------------------------------------------------------------------
try:
    # If DEPT_COLORS is defined in theme.py, use it
    from theme import DEPT_COLORS  # type: ignore
except Exception:
    # Fallback mapping that matches the Maps page intent
    DEPT_COLORS = {
        "IT": PALETTE["coral"],      # IT = coral / red-ish
        "HR": PALETTE["gold"],       # HR = gold / yellow
        "Finance": PALETTE["teal"],  # Finance = teal / green-ish
    }

# ---------------------------------------------------------------------
# Backend configuration (env only – works on Streamlit Cloud)
# ---------------------------------------------------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

TICKETS_ENDPOINT = f"{BACKEND_URL}/tickets/process"
HEALTH_ENDPOINT = f"{BACKEND_URL}/health"

def fake_orchestrator_response(payload: Dict[str, Any], dept: str) -> Dict[str, Any]:
    """Local canned response used when running in dev/demo mode."""
    if dept == "Auto":
        dept = "IT"  # default for demo

    summary = payload.get("description", "")[:80] + "..."
    return {
        "classification": {
            "department": dept,
            "confidence": 0.92,
            "rationale": (
                "Dev mode: this is a canned classification for demo purposes. "
                "In live mode, the TriNexa classifier would score and route this."
            ),
        },
        "response": {
            "agent_name": f"{dept} Agent",
            "department": dept,
            "summary": f"Dev-mode response for {dept} – showing the orchestration UI.",
            "steps": (
                "- This is a simulated response because the backend is not running.\n"
                "- In the real system, the orchestrator would call the {dept} agent.\n"
                "- Use this screen to demo the workflow and UI to judges.\n"
            ),
        },
    }


def submit_ticket(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Call the FastAPI tickets endpoint."""
    try:
        resp = requests.post(TICKETS_ENDPOINT, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}


# Shared styles
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
# Backend health / dev-mode detection
# ---------------------------------------------------------------------


@st.cache_data(ttl=30)
def get_backend_health(base_url: str) -> Dict[str, Any] | None:
    """Ping the FastAPI /health endpoint to discover dev_mode, etc."""
    try:
        resp = requests.get(f"{base_url}/health", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


# Initialise session state
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Auto"

if "force_dev_mode" not in st.session_state:
    st.session_state.force_dev_mode = False

health = get_backend_health(BACKEND_URL)
backend_dev_mode = bool(health and health.get("dev_mode"))
effective_dev_mode = backend_dev_mode or st.session_state.force_dev_mode

# ---------------------------------------------------------------------
# Dev-mode banner + toggle row
# ---------------------------------------------------------------------
col_toggle, col_status = st.columns([1, 3])

with col_toggle:
    st.checkbox(
        "Force Dev Mode\n(local demo)",
        key="force_dev_mode",
        help="Use canned responses even if the backend is wired to Azure.",
    )

with col_status:
    if health is None:
        st.markdown(
            """
            <div class="tri-banner tri-banner-dev">
                ⚠️ Backend health endpoint not reachable – check that FastAPI is running.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif effective_dev_mode:
        st.markdown(
            """
            <div class="tri-banner tri-banner-dev">
                🧪 Running in Dev Mode – using canned responses for a safe demo.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="tri-banner tri-banner-live">
                ✅ Backend is running in Live Azure mode.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Recompute after toggle (user may have just clicked it)
effective_dev_mode = backend_dev_mode or st.session_state.force_dev_mode

# ---------------------------------------------------------------------
# Department selection buttons – styled via CSS to match Maps
# ---------------------------------------------------------------------
st.markdown("<p class='section-label'>Choose a department (optional)</p>", unsafe_allow_html=True)
st.markdown("<div id='dept-buttons'>", unsafe_allow_html=True)

cols = st.columns(4)
button_defs = [
    ("Auto", "Auto"),
    ("IT Agent", "IT"),
    ("HR Agent", "HR"),
    ("Finance Agent", "Finance"),
]

for col, (label, domain) in zip(cols, button_defs):
    with col:
        is_selected = st.session_state.selected_domain == domain
        btn_type = "primary" if is_selected else "secondary"
        if st.button(label, key=f"btn_{domain.lower()}", use_container_width=True, type=btn_type):
            st.session_state.selected_domain = domain

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p class='section-label'>Describe your request</p>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Ticket input form
# ---------------------------------------------------------------------
col_form, col_result = st.columns([1.3, 1.7])

with col_form:
    title = st.text_input("Short summary", placeholder="e.g. 'Cannot access VPN'")
    description = st.text_area(
        "Details",
        placeholder="Describe what's happening, affected systems, and any error messages.",
        height=160,
    )
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Critical"],
        index=1,
    )

    submit = st.button("Submit to TriNexa", type="primary")

with col_result:
    st.markdown("### Orchestrator Response")

    if not submit:
        ...
    else:
        ...
            payload: Dict[str, Any] = {
                ...
            }

            url = f"{BACKEND_URL}/tickets/process"

                        with st.spinner("Asking TriNexa and domain agents..."):
                # If we're in dev mode OR the backend health check failed,
                # skip FastAPI entirely and use a canned response.
                if effective_dev_mode or health is None:
                    data = fake_orchestrator_response(
                        payload,
                        st.session_state.selected_domain,
                    )
                else:
                    data = submit_ticket(payload)

                    # ---------------- Classification card ----------------
                    st.markdown(
                        f"""
                        <div class="tr-card" style="border-left: 4px solid {PALETTE['deep_blue']}">
                            <strong>Classification</strong><br/>
                            Department: <b>{clf.get('department', '—')}</b><br/>
                            Confidence: {clf.get('confidence', '—')}<br/>
                            <span style="font-size:0.85rem; opacity:0.9;">
                            {clf.get('rationale', '')}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("")

                    # ---------------- Agent response card ----------------
                    dept = agent.get("department") or clf.get("department") or "—"
                    dept_color = DEPT_COLORS.get(dept, PALETTE["deep_blue"])

                    st.markdown(
                        f"""
                        <div class="tr-card" style="border-left: 4px solid {dept_color}">
                            <strong>Agent:</strong> {agent.get('agent_name', 'TriResolve Orchestrator')}<br/>
                            <strong>Department:</strong> {dept}<br/><br/>
                            <strong>Summary</strong><br/>
                            {agent.get('summary', '—')}<br/><br/>
                            <strong>Recommended steps</strong><br/>
                            <pre style="white-space:pre-wrap; font-size:0.85rem;">
{(agent.get('steps') or '').strip()}
                            </pre>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander("Raw response (debug)"):
                        st.json(data)


