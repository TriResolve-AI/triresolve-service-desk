from __future__ import annotations

from typing import Any, Dict

import requests
import streamlit as st

from theme import PALETTE, DEPT_COLORS, inject_base_css

# -------------------------------------------------------------------
# Shared theme / CSS
# -------------------------------------------------------------------
inject_base_css()

# Extra CSS just for this page
st.markdown(
    """
    <style>
    .tr-assistant-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tr-assistant-subtitle {
        font-size: 0.95rem;
        opacity: 0.9;
        margin-bottom: 0.75rem;
    }

    .section-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: rgba(0,0,0,0.55);
        margin-top: 0.75rem;
        margin-bottom: 0.25rem;
    }

    .tr-card {
        border-radius: 0.75rem;
        padding: 0.9rem 1rem;
        background-color: #FFF7E8;
        border: 1px solid rgba(0,0,0,0.04);
        margin-top: 0.5rem;
    }

    /* Department button row - color match with Maps page:
       1: Auto (deep blue) 
       2: IT (coral)
       3: HR (gold)
       4: Finance (teal)
    */
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"]:nth-child(1) button {
        background-color: #00547D !important;  /* deep blue */
        color: white !important;
        border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"]:nth-child(2) button {
        background-color: #F2654C !important;  /* IT - coral */
        color: white !important;
        border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"]:nth-child(3) button {
        background-color: #F3B147 !important;  /* HR - gold */
        color: white !important;
        border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"]:nth-child(4) button {
        background-color: #1FB7A6 !important;  /* Finance - teal */
        color: white !important;
        border: none !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
        opacity: 0.92 !important;
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# Backend helpers
# -------------------------------------------------------------------
def get_backend_url() -> str:
    """
    Resolve the backend URL.

    Priority:
      1) st.secrets["BACKEND_URL"] (for Streamlit Cloud)
      2) default: http://localhost:8000
    """
    raw = st.secrets.get("BACKEND_URL", "http://localhost:8000")
    return str(raw).rstrip("/")


def check_dev_mode() -> bool:
    """
    Ask the backend /health endpoint if it's running in dev mode.
    Expects JSON like: {"status": "ok", "dev_mode": true}
    """
    backend = get_backend_url()
    health_url = f"{backend}/health"

    try:
        r = requests.get(health_url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return bool(data.get("dev_mode", False))
    except Exception:
        # If health endpoint is missing or backend down, just assume false.
        return False


BACKEND_DEV_MODE = check_dev_mode()

# -------------------------------------------------------------------
# Session defaults
# -------------------------------------------------------------------
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Auto"

if "force_dev_mode" not in st.session_state:
    st.session_state.force_dev_mode = False


def set_department(domain: str) -> None:
    st.session_state.selected_domain = domain


# -------------------------------------------------------------------
# Header + Dev indicators
# -------------------------------------------------------------------
with st.container():
    st.markdown(
        "<div class='tr-assistant-title'>"
        "<h2 style='margin-bottom:0;'>🧩 TriNexa Assistant</h2>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tr-assistant-subtitle">
        This is the <strong>front door</strong> to the orchestration layer.<br/>
        TriNexa will eventually classify intent, route across IT / HR / Finance, 
        and aggregate responses back to the user.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Small top bar row: Dev banner + toggle + status text
    c_dev1, c_dev2 = st.columns([1.2, 2.8])

    with c_dev1:
        # UI toggle: forces dev mode via query param ?dev=1
        st.session_state.force_dev_mode = st.toggle(
            "Force Dev Mode (local demo)",
            value=st.session_state.force_dev_mode,
            help="When on, tickets include ?dev=1 so the backend can return canned demo responses even if global dev mode is off.",
        )

    with c_dev2:
        # Banner-ish status text (based on backend + toggle)
        if st.session_state.force_dev_mode:
            st.markdown(
                """
                <div style="
                    background-color:#F2654C;
                    padding:0.45rem 0.75rem;
                    border-radius:0.5rem;
                    color:white;
                    font-size:0.85rem;
                    border-left:6px solid #c64532;
                    ">
                    ⚠️ <strong>Demo override:</strong> This UI is forcing <em>Dev Mode</em> for all tickets in this session.
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif BACKEND_DEV_MODE:
            st.markdown(
                """
                <div style="
                    background-color:#F3B147;
                    padding:0.45rem 0.75rem;
                    border-radius:0.5rem;
                    color:#3b2a00;
                    font-size:0.85rem;
                    border-left:6px solid #d39a35;
                    ">
                    ℹ️ Backend is running in <strong>Dev Mode</strong> (environment flag).
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="
                    background-color:#1FB7A6;
                    padding:0.45rem 0.75rem;
                    border-radius:0.5rem;
                    color:#012f2b;
                    font-size:0.85rem;
                    border-left:6px solid #158376;
                    ">
                    ✅ Backend is running in <strong>Live Azure mode</strong>.
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("<p class='section-label'>Choose a department (optional)</p>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Department selector row
# -------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("Auto", key="btn_auto", use_container_width=True):
        set_department("Auto")
with c2:
    if st.button("IT Agent", key="btn_it", use_container_width=True):
        set_department("IT")
with c3:
    if st.button("HR Agent", key="btn_hr", use_container_width=True):
        set_department("HR")
with c4:
    if st.button("Finance Agent", key="btn_fin", use_container_width=True):
        set_department("Finance")

st.caption(f"Let TriNexa pick the best agent, or pin to: **{st.session_state.selected_domain}**.")

st.markdown("---")
st.markdown("<p class='section-label'>Describe your request</p>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Form + Response columns
# -------------------------------------------------------------------
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

    submit = st.button("Submit to TriNexa", type="primary", use_container_width=False)

with col_result:
    st.markdown("### Orchestrator Response")

    if submit:
        if not title or not description:
            st.warning("Please provide both a **summary** and **details**.")
        else:
            backend_url = get_backend_url()
            url = f"{backend_url}/tickets/process"

            # If UI is forcing dev mode, append ?dev=1 for backend to honor
            if st.session_state.force_dev_mode:
                url = f"{url}?dev=1"

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
            }

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

                    # Classification card
                    st.markdown(
                        f"""
                        <div class="tr-card" style="border-left: 4px solid {PALETTE.get('deep_blue', '#00547D')}">
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

                    # Agent response card
                    dept = agent.get("department", "—")
                    dept_color = DEPT_COLORS.get(dept, PALETTE.get("deep_blue", "#00547D"))

                    summary = agent.get("summary", "").strip() or "—"
                    steps = (agent.get("steps", "") or "").strip()

                    st.markdown(
                        f"""
                        <div class="tr-card" style="border-left: 4px solid {dept_color}">
                            <strong>Agent:</strong> {agent.get('agent_name', 'TriResolve Agent')}<br/>
                            <strong>Department:</strong> {dept}<br/><br/>
                            <strong>Summary</strong><br/>
                            {summary}<br/><br/>
                            <strong>Recommended steps</strong><br/>
                            <pre style="white-space:pre-wrap; font-size:0.85rem; margin-top:0.35rem;">
{steps}
                            </pre>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander("Raw response (debug)"):
                        st.json(data)
    else:
        st.info("Submit a ticket on the left to see the orchestrator in action.")
