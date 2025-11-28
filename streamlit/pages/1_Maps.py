# streamlit/pages/1_Maps.py

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from theme import PALETTE, DEPT_COLORS, inject_base_css

# Shared styles
inject_base_css()

st.title("🗺️ Maps & Service Desk Overview")
st.write(
    "High-level view of ticket patterns, system architecture, and ownership "
    "across HR, IT, and Finance."
)


# ---- Data Loader ----
@st.cache_data
def load_ticket_data() -> pd.DataFrame:
    """Load and combine ticket samples from HR, IT, and Finance."""
    root = Path(__file__).resolve().parents[2]

    hr_path = root / "agents" / "hr" / "examples" / "hr_tickets.csv"
    it_path = root / "agents" / "it" / "examples" / "it_tickets.csv"
    fin_path = root / "agents" / "finance" / "examples" / "finance_tickets.csv"

    frames = []
    if hr_path.exists():
        hr = pd.read_csv(hr_path)
        hr["department"] = "HR"
        frames.append(hr)

    if it_path.exists():
        it = pd.read_csv(it_path)
        it["department"] = "IT"
        frames.append(it)

    if fin_path.exists():
        fin = pd.read_csv(fin_path)
        fin["department"] = "Finance"
        frames.append(fin)

    if not frames:
        return pd.DataFrame()

    all_tickets = pd.concat(frames, ignore_index=True)

    # Parse date columns if present
    for col in ["created_at", "resolved_at"]:
        if col in all_tickets.columns:
            all_tickets[col] = pd.to_datetime(all_tickets[col], errors="coerce")

    return all_tickets


tab1, tab2, tab3 = st.tabs(
    ["Ticket Patterns", "System Architecture", "Responsibility Map"]
)

# =========================
# TAB 1: Ticket Patterns
# =========================
with tab1:
    st.subheader("Ticket Volume & Trends")

    df = load_ticket_data()

    if df.empty:
        st.warning(
            "No ticket data found. Please verify CSV paths under "
            "`agents/*/examples/*.csv`."
        )
    else:
        # Department chips legend
        st.markdown(
            f"""
            <div style="margin-bottom: 0.5rem;">
              <span class="dept-chip"
                    style="background-color:{DEPT_COLORS['Finance']}33;
                           border:1px solid {DEPT_COLORS['Finance']};">
                Finance
              </span>
              <span class="dept-chip"
                    style="background-color:{DEPT_COLORS['HR']}33;
                           border:1px solid {DEPT_COLORS['HR']};">
                HR
              </span>
              <span class="dept-chip"
                    style="background-color:{DEPT_COLORS['IT']}33;
                           border:1px solid {DEPT_COLORS['IT']};">
                IT
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Department filter
        selected_dept = st.radio(
            "Filter by department",
            ["All", "Finance", "HR", "IT"],
            horizontal=True,
        )

        if selected_dept == "All":
            df_view = df.copy()
        else:
            df_view = df[df["department"] == selected_dept]

        # KPIs
        total_tickets = len(df_view)
        status_lower = (
            df_view["status"].str.lower() if "status" in df_view.columns else None
        )

        open_tickets = (
            df_view[status_lower.eq("open")].shape[0]
            if status_lower is not None
            else None
        )
        resolved_tickets = (
            df_view[status_lower.eq("resolved")].shape[0]
            if status_lower is not None
            else None
        )

        k1, k2, k3 = st.columns(3)
        k1.metric("Total Tickets", total_tickets)
        if open_tickets is not None:
            k2.metric("Open Tickets", open_tickets)
        if resolved_tickets is not None:
            k3.metric("Resolved Tickets", resolved_tickets)

        # Tickets by department (always from full dataset)
        st.markdown("### Tickets by Department")

        if "department" in df.columns:
            if "ticket_id" in df.columns:
                by_dept = df.groupby("department")["ticket_id"].count()
            else:
                by_dept = df.groupby("department").size()

            chart_data = by_dept.reset_index().rename(
                columns={0: "ticket_count", "ticket_id": "ticket_count"}
            )

            dept_order = ["Finance", "HR", "IT"]
            chart = (
                alt.Chart(chart_data)
                .mark_bar()
                .encode(
                    x=alt.X("department:N", sort=dept_order, title="Department"),
                    y=alt.Y("ticket_count:Q", title="Tickets"),
                    color=alt.Color(
                        "department:N",
                        scale=alt.Scale(
                            domain=dept_order,
                            range=[
                                DEPT_COLORS["Finance"],
                                DEPT_COLORS["HR"],
                                DEPT_COLORS["IT"],
                            ],
                        ),
                        legend=None,
                    ),
                )
                .properties(height=320)
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No 'department' column found in the dataset.")

        # Tickets over time (using filtered view)
        if "created_at" in df_view.columns and "department" in df_view.columns:
            st.markdown("### Ticket Volume Over Time")

            daily = (
                df_view.dropna(subset=["created_at"])
                .groupby([df_view["created_at"].dt.date, "department"])
                .size()
                .reset_index(name="ticket_count")
            )

            time_chart = (
                alt.Chart(daily)
                .mark_line(point=True)
                .encode(
                    x=alt.X("created_at:T", title="Date"),
                    y=alt.Y("ticket_count:Q", title="Tickets"),
                    color=alt.Color(
                        "department:N",
                        scale=alt.Scale(
                            domain=["Finance", "HR", "IT"],
                            range=[
                                DEPT_COLORS["Finance"],
                                DEPT_COLORS["HR"],
                                DEPT_COLORS["IT"],
                            ],
                        ),
                        title="Department",
                    ),
                )
                .properties(height=320)
            )

            st.altair_chart(time_chart, use_container_width=True)
        else:
            st.info(
                "No 'created_at' column available for time-series view, "
                "or department labels missing."
            )

        # Category vs Status pivot
        st.markdown("### Ticket Category vs Status")

        category_col = "category" if "category" in df_view.columns else None
        status_col = "status" if "status" in df_view.columns else None

        if category_col and status_col:
            pivot = pd.pivot_table(
                df_view,
                index=category_col,
                columns=status_col,
                values="ticket_id" if "ticket_id" in df_view.columns else status_col,
                aggfunc="count",
                fill_value=0,
            )
            st.dataframe(pivot, use_container_width=True)
        else:
            st.info(
                "Category / status breakdown not available "
                "(missing 'category' or 'status' columns)."
            )

# =========================
# TAB 2: System Architecture
# =========================
with tab2:
    st.subheader("System Architecture & Routing")

    st.write(
        "Tickets flow from end users through a classifier and the TriNexa "
        "orchestrator into HR, IT, and Finance agents, which are connected "
        "to the relevant systems of record."
    )

    assets_dir = Path(__file__).resolve().parents[1] / "assets"
    arch_path = assets_dir / "triresolve_architecture.png"

    if arch_path.exists():
        st.image(
            str(arch_path),
            caption="TriResolve AI – Multi-Agent Architecture",
            use_container_width=True,
        )
    else:
        st.warning(
            "Architecture diagram not found yet. "
            "Please add 'triresolve_architecture.png' to streamlit/assets."
        )

    st.markdown(
        """
        **Legend**

        - 🖣️ User Channels: Teams, Email, Web Portal  
        - 🔵 Classifier & Orchestrator (TriNexa)  
        - 🟢 Domain Agents: HR, IT, Finance  
        - 🗄️ Data Sources: HRIS, IAM, ERP, Ticket DB
        """
    )

# =========================
# TAB 3: Responsibility Map
# =========================
with tab3:
    st.subheader("Responsibility Map (RACI)")

    st.write(
        "High-level view of which agent is responsible for common service desk tasks. "
        "This clarifies routing and ownership."
    )

    data = {
        "Task": [
            "Ticket classification",
            "Employee onboarding",
            "Password reset",
            "VPN / access issues",
            "Benefits & PTO questions",
            "Vendor onboarding",
            "Invoice status / AP",
        ],
        "Classifier": ["R", "I", "I", "I", "I", "I", "I"],
        "Orchestrator (TriNexa)": ["A", "C", "C", "C", "C", "C", "C"],
        "HR Agent": ["I", "R", "I", "I", "R", "I", "I"],
        "IT Agent": ["I", "I", "R", "R", "I", "I", "I"],
        "Finance Agent": ["I", "I", "I", "I", "I", "R", "R"],
    }

    raci_df = pd.DataFrame(data)
    st.dataframe(raci_df, use_container_width=True)

    st.markdown(
        """
        **Key**

        - **R** = Responsible (does the work)  
        - **A** = Accountable (owns the outcome)  
        - **C** = Consulted (provides input)  
        - **I** = Informed (kept in the loop)
        """
    )
