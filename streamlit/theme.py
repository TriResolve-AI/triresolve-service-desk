# streamlit/theme.py

"""
Shared theme + palette helpers for the TriResolve AI Streamlit app.
Import this in all pages:

    from theme import PALETTE, DEPT_COLORS, inject_base_css
"""

import streamlit as st

# --- Core TriResolveAI palette (from logo) ---
PALETTE = {
    "primary_blue": "#005B8F",   # text + strong accents
    "teal": "#2EB7A5",           # teal loop
    "gold": "#F4B23E",           # golden loop
    "coral": "#E8654F",          # coral/red loop
    "cream": "#F5F1E5",          # band behind text
    "sky_top": "#227C9D",        # top of gradient background
    "sky_bottom": "#F2EDE2",     # bottom of gradient background
}

# Department color mapping (loops mapped to domains)
DEPT_COLORS = {
    "Finance": PALETTE["gold"],
    "HR": PALETTE["teal"],
    "IT": PALETTE["coral"],
}


def inject_base_css() -> None:
    """Inject global CSS so all pages share the same look & feel."""

    st.markdown(
        f"""
        <style>
        /* ---------- Layout + background ---------- */
        div.block-container {{
            padding-top: 2.5rem;
            padding-bottom: 2.5rem;
            background: linear-gradient(
                180deg,
                {PALETTE["cream"]} 0%,
                {PALETTE["sky_bottom"]} 100%
            );
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(
                180deg,
                {PALETTE["primary_blue"]} 0%,
                {PALETTE["teal"]} 100%
            );
            color: #F9FAFB;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: #F9FAFB !important;
        }}

        /* ---------- Typography ---------- */
        h1, h2, h3, h4, h5 {{
            color: {PALETTE["primary_blue"]};
            letter-spacing: 0.02em;
        }}

        .triresolve-hero h1 {{
            font-size: 2.4rem !important;
            margin-bottom: 0.3rem;
        }}

        .triresolve-hero h3 {{
            font-size: 1.1rem !important;
            font-weight: 400;
            opacity: 0.9;
            margin-top: 0;
        }}

        .section-label {{
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.8rem;
            color: #6B7280;
        }}

        /* ---------- Chips & badges ---------- */
        .pill {{
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background: rgba(0, 91, 143, 0.07);
            color: {PALETTE["primary_blue"]};
            margin-right: 0.4rem;
        }}

        .pill span {{
            margin-left: 0.3rem;
        }}

        .agent-badge {{
            display: inline-flex;
            align-items: center;
            font-size: 0.8rem;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            margin-right: 0.4rem;
            background: rgba(0, 91, 143, 0.05);
            color: {PALETTE["primary_blue"]};
            border: 1px solid rgba(0, 91, 143, 0.12);
        }}

        .dept-chip {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.8rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.5rem;
            color: #0F172A;
        }}

        /* ---------- Card-like containers ---------- */
        .tr-card {{
            border-radius: 18px;
            padding: 1.1rem 1.3rem;
            background: rgba(255, 255, 255, 0.85);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button {{
            border-radius: 999px;
            border: none;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        /* ---------- Text input + text area ---------- */
        textarea, input[type="text"] {{
            border-radius: 12px !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
