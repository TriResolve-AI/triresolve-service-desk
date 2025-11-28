 TriResolve AI – Maps Page Implementation (For Megan)

Below are the steps and the full `1_Maps.py` code for the **Maps & Service Desk Overview** page in Streamlit, including the brand colors and department-specific styling.

---
## 1️⃣ What this page should do

- Load sample tickets from:
  - `agents/hr/examples/hr_tickets.csv`
  - `agents/it/examples/it_tickets.csv`
  - `agents/finance/examples/finance_tickets.csv`
- Show **ticket patterns** (KPIs, tickets by department, tickets over time, category vs status).
- Display the **system architecture diagram** (PNG) for the multi‑agent flow.
- Provide a **responsibility map (RACI)** for HR, IT, Finance, Classifier, and Orchestrator.
- Use the TriResolve brand colors:
  - `#227C9D` – Cerulean (primary blue)
  - `#17C3B2` – Light Sea Green (Finance)
  - `#FFCB77` – Apricot Cream (HR)
  - `#FEF9EF` – Floral White (background)
  - `#FE6D73` – Grapefruit Pink (IT)

---
## 2️⃣ Where this file lives

Create (or replace) the file:

```text
streamlit/pages/1_Maps.py
```

Run Streamlit from the repo root:

```bash
streamlit run streamlit/streamlit_app.py
```

This will auto‑load the `1_Maps.py` file as the **“Maps & Service Desk Overview”** page.

---
## 3️⃣ Full 1_Maps.py code (copy/paste)

```python
import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path

# ---- Brand Palette ----
PALETTE = {
    "cerulean": "#227C9D",
    "sea_green": "#17C3B2",
    "apricot": "#FFCB77",
    "floral_white": "#FEF9EF",
    "grapefruit": "#FE6D73",
}

DEPT_COLORS = {
    "Finance": PALETTE["sea_green"],     # green-ish
    "HR": PALETTE["apricot"],           # yellow-ish
    "IT": PALETTE["grapefruit"],        # red-ish
}

# ---- Page Config ----
st.set_page_config(
    page_title="Maps – TriResolve AI",
    page_icon="🗺️",
    layout="wide",
)

# ---- Global Styles (background, sidebar, chips) ----
st.markdown(
    f"""
    <style>
    /* Main content background */
    div.block-container {{
        background-color: {PALETTE["floral_white"]};
    }}

    /* Sidebar gradient */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            {PALETTE["cerulean"]} 0%,
            {PALETTE["sea_green"]} 100%
        );
    }}

    /* Headings */
    h1, h2, h3, h4 {{
        color: {PALETTE["cerulean"]};
    }}

    /* Department chips */
    .dept-chip {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        margin-right: 0.4rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #0F172A;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🗺️ Maps & Service Desk Overview")
st.write(
    "High-level view of ticket patterns, system architecture, and ownership "
    "across HR, IT, and Finance."
)


# ---- Data Loader ----
@st.cache_data
def load_ticket_data() -> pd.DataFrame:
    """Load and combine ticket samples from HR, IT, and Finance."""
    hr = pd.read_csv("agents/hr/examples/hr_tickets.csv")
    it = pd.read_csv("agents/it/examples/it_tickets.csv")
    finance = pd.read_csv("agents/finance/examples/finance_tickets.csv")

    hr["department"] = "HR"
    it["department"] = "IT"
    finance["department"] = "Finance"

    all_tickets = pd.concat([hr, it, finance], ignore_index=True)

    # Parse date columns if present
    for col in ["created_at", "resolved_at"]:
        if col in all_tickets.columns:
            all_tickets[col] = pd.to_datetime(all_tickets[col], errors="coerce")

    return all_tickets


# ---- Tabs ----
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
        st.warning("No ticket data found. Please verify CSV paths.")
    else:
        # Department color legend chips
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

        # Department filter "buttons"
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

        kpi_cols = st.columns(3)
        kpi_cols[0].metric("Total Tickets", total_tickets)
        if open_tickets is not None:
            kpi_cols[1].metric("Open Tickets", open_tickets)
        if resolved_tickets is not None:
            kpi_cols[2].metric("Resolved Tickets", resolved_tickets)

        st.markdown("### Tickets by Department")

        if "department" in df.columns:
            # Group on full dataset so chart always shows all depts
            by_dept = (
                df.groupby("department")["ticket_id"].count()
                if "ticket_id" in df.columns
                else df.groupby("department").size()
            )

            chart_data = (
                by_dept.reset_index()
                .rename(columns={0: "ticket_count"})
            )
            if "ticket_id" in df.columns:
                chart_data = chart_data.rename(columns={"ticket_id": "ticket_count"})

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
```

---
## 4️⃣ Quick notes for Megan

- Double‑check that the CSVs you generate have at least these columns: `ticket_id`, `status`, `created_at`, `category` (or update the code if names differ).
- Make sure the architecture diagram is saved as `streamlit/assets/triresolve_architecture.png`.
- Once this file is in place, run the app from the repo root:

  ```bash
  streamlit run streamlit/streamlit_app.py
  ```

- You should see a **“Maps & Service Desk Overview”** page with three tabs and the new color palette applied.
