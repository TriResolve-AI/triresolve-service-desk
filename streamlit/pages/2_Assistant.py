# streamlit/pages/2_Assistant.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import sys

import requests
import streamlit as st

# ---------------------------------------------------------------------
# Make sure the repo root is on sys.path so we can import config, etc.
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from theme import PALETTE, inject_base_css  # DEPT_COLORS comes via fallback below

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

from config import settings  # now safe because sys.path is fixed

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
# Backend config + health / dev-mode detection
# ---------------------------------------------------------------------
BACKEND_URL = settings._get("backend", "BACKEND_URL", "http://localhost:8000").rstrip("/")


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
# Department selection buttons – will be styled via CSS to match Maps
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
        # Nice empty-state message
        st.info("Submit a ticket on the left to see the orchestrator in action.")
    else:
        if not title or not description:
            st.warning("Please provide both a **summary** and **details**.")
        else:
            full_description = description
            if st.session_state.selected_domain != "Auto":
                full_description = (
                    f"[Preferred department: {st.session_state.selected_domain}] "
                    + description
                )

            payload: Dict[str, Any] = {
                "title": title,
                "description": full_description,
                "priority": priority,
                # Let the backend know if we're forcing dev-mode
                "dev_mode": effective_dev_mode,
            }

            url = f"{BACKEND_URL}/tickets/process"

            with st.spinner("Asking TriNexa and domain agents..."):
                try:
                    resp = requests.post(url, json=payload, timeout=45)
                    resp.raise_for_status()
                    data = resp.json()
                except Exception as exc:  # noqa: BLE001
                    st.error(
                        f"Error contacting backend at `{url}`. "
                        f"Check that FastAPI is running and reachable.\n\n{exc}"
                    )
                else:
                    clf = data.get("classification", {}) or {}
                    agent = data.get("response", {}) or {}

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
