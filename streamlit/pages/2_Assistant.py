# streamlit/pages/2_Assistant.py

import requests
import streamlit as st

from config import settings  # uses your config.py helper

# Build backend /chat URL from config backend_url
BACKEND_CHAT_URL = settings.backend_url.rstrip("/") + "/chat"


# -------------------------------
# Small layout + style helpers
# -------------------------------

def init_session_state() -> None:
    """Ensure required keys exist in st.session_state."""
    if "selected_domain" not in st.session_state:
        st.session_state["selected_domain"] = None  # "it" | "hr" | "finance"
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []  # list[dict]


def domain_label(domain: str | None) -> str:
    if domain is None:
        return "Orchestrator (auto-route)"
    mapping = {
        "it": "IT Service Desk",
        "hr": "HR & People Ops",
        "finance": "Finance & Spend",
    }
    return mapping.get(domain, domain.capitalize())


def render_header() -> None:
    st.title("TriNexa Assistant")
    st.caption("Front door to the TriResolve multi-agent service desk.")

    st.markdown(
        """
TriNexa is your **orchestrator** for IT, HR, and Finance requests.

1. Classifies the request  
2. Routes it to the right domain agent  
3. Aggregates responses back in one conversation  
        """
    )


def render_domain_cards() -> None:
    """Three colored cards to pick the domain (orchestrator vs direct)."""

    st.subheader("Which team do you need?")

    col1, col2, col3 = st.columns(3)

    def card(label: str, domain_key: str | None, bg: str):
        is_active = st.session_state["selected_domain"] == domain_key
        border = "3px solid #ffffff" if is_active else "1px solid rgba(255,255,255,0.2)"
        alpha = "0.9" if is_active else "0.85"

        button_label = f"**{label}**"
        style = f"""
        <style>
        .tri-card-{label.replace(" ", "-").lower()} {{
            background: {bg}CC;
            border-radius: 16px;
            border: {border};
            padding: 1.25rem 0.75rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
        }}
        .tri-card-{label.replace(" ", "-").lower()}:hover {{
            background: {bg}{alpha.replace(".", "")};
            transform: translateY(-2px);
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)

        if st.button(
            button_label,
            key=f"btn-{label}",
            use_container_width=True,
        ):
            st.session_state["selected_domain"] = domain_key

        st.markdown(
            f'<div class="tri-card-{label.replace(" ", "-").lower()}">{label}</div>',
            unsafe_allow_html=True,
        )

    with col1:
        card("IT Agent", "it", "#FE6D73")        # coral / red
    with col2:
        card("HR Agent", "hr", "#FFCB77")        # warm yellow
    with col3:
        card("Finance Agent", "finance", "#17C3B2")  # teal


def render_domain_status() -> None:
    domain = st.session_state["selected_domain"]
    st.markdown("---")
    st.write(
        f"**Routing mode:** {domain_label(domain)}  "
        "· You can switch domains at any time by clicking another card."
    )


def call_backend(message: str) -> str:
    """Call FastAPI /chat endpoint and return the reply text."""
    domain = st.session_state["selected_domain"]

    payload = {
        "message": message,
        "domain": domain,  # None → orchestrator decides
    }

    try:
        resp = requests.post(BACKEND_CHAT_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("reply", "(No reply content returned.)")
    except Exception as exc:  # broad catch ok for UI
        return f"⚠️ Error calling backend: {exc}"


def render_chat_ui() -> None:
    st.subheader("Ask TriNexa something")

    # Show chat history
    for turn in st.session_state["chat_history"]:
        with st.chat_message("user"):
            st.write(turn["user"])
        with st.chat_message("assistant"):
            st.write(turn["assistant"])

    # New input
    user_message = st.chat_input(
        "Describe your issue or question…",
    )

    if not user_message:
        return

    # Echo user message in UI
    with st.chat_message("user"):
        st.write(user_message)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Routing through TriNexa…"):
            reply = call_backend(user_message)
            st.write(reply)

    # Persist in session_state
    st.session_state["chat_history"].append(
        {"user": user_message, "assistant": reply}
    )


# -------------------------------
# Page entrypoint
# -------------------------------
def main() -> None:
    init_session_state()
    render_header()
    render_domain_cards()
    render_domain_status()
    render_chat_ui()


if __name__ == "__main__":
    main()
