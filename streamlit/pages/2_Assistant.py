# streamlit/pages/2_Assistant.py

from __future__ import annotations

from typing import Any, Dict

import requests
import streamlit as st

from theme import PALETTE, DEPT_COLORS, inject_base_css

# Shared styles
inject_base_css()

st.title("🤝 TriNexa Assistant")

st.write(
    """
    This is the **front door** to the orchestration layer.

    TriNexa will eventually:
    - Classify intent  
    - Route to IT / HR / Finance agents  
    - Aggregate responses back to the user  
    """
)

st.markdown("<p class='section-label'>Choose a department (optional)</p>", unsafe_allow_html=True)

if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Auto"

# Shared styles
inject_base_css()

def agent_button(label: str, domain: str, key: str) -> None:
    """Render a department selection button."""
    is_selected = st.session_state.selected_domain == domain
    # Use st.button for functionality with CSS-based styling
    if st.button(label, key=key, use_container_width=True, type="secondary" if not is_selected else "primary"):
        st.session_state.selected_domain = domain
        st.rerun()


c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("Auto", key="btn_auto", use_container_width=True):
        st.session_state.selected_domain = "Auto"
    st.caption("Let TriNexa pick the best agent.")

with c2:
    agent_button("IT Agent", "IT", "btn_it")

with c3:
    agent_button("HR Agent", "HR", "btn_hr")

with c4:
    agent_button("Finance Agent", "Finance", "btn_fin")


st.markdown("---")
st.markdown("<p class='section-label'>Describe your request</p>", unsafe_allow_html=True)

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

    if submit:
        if not title or not description:
            st.warning("Please provide both a **summary** and **details**.")
        else:
            from config import settings  # imported lazily so config can read secrets/env

            backend_url = settings._get('backend', 'BACKEND_URL', 'http://localhost:8000').rstrip("/")
            url = f"{backend_url}/tickets/process"

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
                        f"Check that FastAPI is running.\n\n{exc}"
                    )
                else:
                    clf = data.get("classification", {})
                    agent = data.get("response", {})

                    # Classification card
                    st.markdown(
                        f"""
                        <div class="tr-card" style="border-left: 4px solid {PALETTE['primary_blue']}">
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
                    dept_color = DEPT_COLORS.get(dept, PALETTE["primary_blue"])

                    st.markdown(
                        f"""
                        <div class="tr-card" style="border-left: 4px solid {dept_color}">
                            <strong>Agent:</strong> {agent.get('agent_name', 'TriResolve Agent')}<br/>
                            <strong>Department:</strong> {dept}<br/><br/>
                            <strong>Summary</strong><br/>
                            {agent.get('summary', '—')}<br/><br/>
                            <strong>Recommended steps</strong><br/>
                            <pre style="white-space:pre-wrap; font-size:0.85rem;">
{agent.get('steps', '').strip()}
                            </pre>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander("Raw response (debug)"):
                        st.json(data)
