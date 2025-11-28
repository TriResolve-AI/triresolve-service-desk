import streamlit as st
import requests

API_URL = "http://localhost:8000/orchestrator"  # adjust for your backend

st.header("🧠 TriResolve Assistant")

ticket = st.text_area("Describe your issue", placeholder="I can't access VPN after the latest change...")

if st.button("Submit Ticket"):
    if not ticket.strip():
        st.warning("Please enter a ticket description before submitting.")
    else:
        with st.spinner("Routing your ticket through TriNexa and domain agents..."):
            try:
                resp = requests.post(API_URL, json={"ticket": ticket}, timeout=30)
            except requests.RequestException as e:
                st.error("🚨 Could not reach the TriResolve backend. Please try again.")
                st.caption(f"Details: {e}")
            else:
                if resp.status_code != 200:
                    st.error("⚠️ The service returned an error while processing your ticket.")
                    st.caption(f"Status: {resp.status_code} • Body: {resp.text[:500]}")
                else:
                    data = resp.json()

                    # Adjust keys based on your backend response
                    result = data.get("response", data)

                    st.success("✅ Ticket processed successfully.")

                    final_answer = result.get("final_answer") or result
                    agents_consulted = result.get("agents_consulted", [])

                    st.subheader("💬 Response")
                    st.write(final_answer)

                    if agents_consulted:
                        st.subheader("🧩 Agents Involved")
                        st.write(", ".join(agents_consulted))
