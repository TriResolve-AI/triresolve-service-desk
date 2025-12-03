from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

import streamlit as st

# -------------------------------------------------------------------------
# Ensure both repo root and /streamlit are on sys.path
# -------------------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]          # /triresolve-service-desk
STREAMLIT_DIR = THIS_FILE.parents[1]      # /triresolve-service-desk/streamlit

for p in (REPO_ROOT, STREAMLIT_DIR):
    if str(p) not in sys.path:
        sys.path.append(str(p))

# Theme + styling
from theme import PALETTE, inject_base_css  # type: ignore

# Backend orchestrator + schemas
from backend.api.schemas import TicketCreate, TicketResult  # type: ignore
from backend.services.orchestrator import process_ticket  # type: ignore

# -------------------------------------------------------------------------
# Department color fallback (in case theme.DEPT_COLORS missing)
# -------------------------------------------------------------------------
try:
    from theme import DEPT_COLORS  # type: ignore
except Exception:
    DEPT_COLORS = {
        "IT": PALETTE["coral"],
        "HR": PALETTE["gold"],
        "Finance": PALETTE["teal"],
    }


# -------------------------------------------------------------------------
# Fake response for Dev Mode
# -------------------------------------------------------------------------
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
                "In live mode, TriNexa classifier would evaluate this."
            ),
        },
        "response": {
            "agent_name": f"{dept} Agent",
            "department": dept,
            "summary": f"Dev-mode response for {dept}.",
            "steps": (
                "- This is a simulated response because the backend is not running.\n"
                f"- The orchestrator would normally invoke the {dept} agent.\n"
                "- Use this UI to demo the workflow.\n"
            ),
        },
    }


# -------------------------------------------------------------------------
# Call orchestrator directly (no HTTP)
# -------------------------------------------------------------------------
def submit_ticket(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call the Python orchestrator directly instead of going through FastAPI.

    This uses the same `process_ticket` pipeline that the FastAPI /tickets/process
    endpoint would call, but runs in-process inside Streamlit.
    """
    try:
        selected_domain = payload.get("domain")
        if selected_domain == "Auto":
            selected_domain = None  # let classifier decide

        # Some versions of TicketCreate may not accept `domain`; fall back gracefully.
        try:
            ticket = TicketCreate(
                title=payload.get("title") or "ticket",
                description=payload.get("description") or "",
                priority=payload.get("priority") or "Medium",
                domain=selected_domain,  # type: ignore[arg-type]
            )
        except TypeError:
            ticket = TicketCreate(
                title=payload.get("title") or "ticket",
                description=payload.get("description") or "",
                priority=payload.get("priority") or "Medium",
            )

        result: TicketResult = process_ticket(ticket, force_dev=False)
        return result.model_dump()  # type: ignore[attr-defined]

    except Exception as exc:
        return {"error": str(exc)}


# -------------------------------------------------------------------------
# Shared styles
# -------------------------------------------------------------------------
inject_base_css()

# -------------------------------------------------------------------------
# UI Header
# -------------------------------------------------------------------------
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

# -------------------------------------------------------------------------
# Dev mode toggle (now purely manual)
# -------------------------------------------------------------------------
if "force_dev_mode" not in st.session_state:
    st.session_state.force_dev_mode = False

col1, col2 = st.columns([1.2, 3])

with col1:
    st.checkbox(
        "Force Dev Mode (local demo)",
        key="force_dev_mode",
        help="Use canned responses instead of calling Azure / Foundry.",
    )

effective_dev_mode = bool(st.session_state.force_dev_mode)

with col2:
    if effective_dev_mode:
        st.markdown(
            """
            <div class="tri-banner tri-banner-dev">
                🧪 Dev Mode Active — using canned responses only.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="tri-banner tri-banner-live">
                ✅ Live Mode — calling the TriNexa orchestrator pipeline
                (Azure AI Foundry / Azure OpenAI).
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------------------------------------------------------------------------
# Department selector buttons
# -------------------------------------------------------------------------
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
        if st.button(label, type="primary" if selected else "secondary"):
            st.session_state.selected_domain = domain

st.markdown("---")

# -------------------------------------------------------------------------
# Ticket Form
# -------------------------------------------------------------------------
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
        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "domain": st.session_state.selected_domain,
        }

        with st.spinner("Processing request via TriNexa..."):
            if effective_dev_mode:
                data = fake_orchestrator_response(payload, st.session_state.selected_domain)
            else:
                data = submit_ticket(payload)

        if data.get("error"):
            st.error(
                "⚠️ Error running TriNexa orchestrator:\n\n"
                f"{data.get('error')}"
            )
        else:
            clf = data.get("classification", {})
            agent = data.get("response", {})

            # Classification card
            st.markdown(
                f"""
                <div class="tr-card" style="border-left: 4px solid {PALETTE['deep_blue']}">
                    <strong>Classification</strong><br/>
                    Department: <b>{clf.get('department','—')}</b><br/>
                    Confidence: {clf.get('confidence','—')}<br/>
                    <div style="font-size:0.85rem; opacity:0.9;">{clf.get('rationale','')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            dept = agent.get("department") or clf.get("department") or "—"
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

            with st.expander("Raw response (debug)"):
                st.json(data)
