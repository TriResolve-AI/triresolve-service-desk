import sys
from pathlib import Path

import streamlit as st
import requests

# Add streamlit folder to path for theme import
sys.path.insert(0, str(Path(__file__).parent.parent))
from theme import inject_base_css, page_header

# --- PAGE CONFIG ---
st.set_page_config(page_title="TriResolve Assistant", page_icon="💬", layout="wide")

inject_base_css()  # global theming

# Extra CSS JUST for the big agent cards
st.markdown(
    """
    <style>
    .agent-row {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    .agent-card {
        text-align: center;
    }
    .agent-card button {
        border-radius: 18px;
        border: 4px solid #F7F4EF;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 1.8rem 0;
        width: 100%;
        box-shadow: 0 10px 24px rgba(0,0,0,0.10);
    }
    .agent-it button {
        background-color: #E65C4E;  /* IT = coral */
        color: #FFFFFF;
    }
    .agent-hr button {
        background-color: #F2A83B;  /* HR = gold */
        color: #0E3B66;
    }
    .agent-finance button {
        background-color: #3BC5BE;  /* Finance = teal */
        color: #0E3B66;
    }
    .agent-card button:hover {
        filter: brightness(1.03);
        transform: translateY(-2px);
        transition: all 0.12s ease-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Standard page header using your logo and tagline
page_header(
    "Need help?",
    "Select which agent best suits your needs, or just start typing below.",
)

st.markdown("")  # a little spacing

# Row of agent cards
st.markdown('<div class="agent-row">', unsafe_allow_html=True)
cols = st.columns(3)

if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None

with cols[0]:
    st.markdown('<div class="agent-card agent-it">', unsafe_allow_html=True)
    if st.button("IT AGENT", key="btn_it"):
        st.session_state.selected_domain = "it"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[1]:
    st.markdown('<div class="agent-card agent-hr">', unsafe_allow_html=True)
    if st.button("HR AGENT", key="btn_hr"):
        st.session_state.selected_domain = "hr"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[2]:
    st.markdown('<div class="agent-card agent-finance">', unsafe_allow_html=True)
    if st.button("FINANCE AGENT", key="btn_finance"):
        st.session_state.selected_domain = "finance"
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Show which agent is currently selected
if st.session_state.selected_domain:
    st.info(f"🎯 Routing to the **{st.session_state.selected_domain.upper()}** domain agent.")
else:
    st.caption("Tip: You can click an agent above to route directly, or let the orchestrator decide automatically.")

st.divider()

# --- Backend integration ---
API_URL = "http://localhost:8000/orchestrator"  # adjust for your backend

user_query = st.text_area("Describe your request:", height=140, placeholder="I can't access VPN after the latest change...")

if st.button("Submit request", key="submit_request"):
    if not user_query.strip():
        st.warning("Please enter a request description before submitting.")
    else:
        with st.spinner("Routing your request through TriNexa and domain agents..."):
            try:
                # Build request payload - include selected domain if any
                payload = {"ticket": user_query}
                if st.session_state.selected_domain:
                    payload["domain"] = st.session_state.selected_domain

                resp = requests.post(API_URL, json=payload, timeout=30)
            except requests.RequestException as e:
                st.error("🚨 Could not reach the TriResolve backend. Please try again.")
                st.caption(f"Details: {e}")
            else:
                if resp.status_code != 200:
                    st.error("⚠️ The service returned an error while processing your request.")
                    st.caption(f"Status: {resp.status_code} • Body: {resp.text[:500]}")
                else:
                    data = resp.json()

                    # Adjust keys based on your backend response
                    result = data.get("response", data)

                    st.success("✅ Request processed successfully.")

                    final_answer = result.get("final_answer") or result
                    agents_consulted = result.get("agents_consulted", [])

                    st.subheader("💬 Response")
                    st.write(final_answer)

                    if agents_consulted:
                        st.subheader("🧩 Agents Involved")
                        st.write(", ".join(agents_consulted))

