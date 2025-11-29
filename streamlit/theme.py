"""
TriResolveAI Streamlit theme helpers.

- PALETTE: single source of truth for brand colors
- DEPT_COLORS: per-department accent colors
- inject_base_css(): loads styles/theme.css AND injects
  department button overrides used in Assistant

Usage:

    from theme import PALETTE, DEPT_COLORS, inject_base_css
    inject_base_css()
"""

from __future__ import annotations

from pathlib import Path
import streamlit as st

# -----------------------------------------------------------------------------
# Brand Palette (Final TriResolveAI)
# -----------------------------------------------------------------------------
PALETTE = {
    "deep_blue": "#00547D",   # Primary blue
    "teal": "#1FB7A6",        # Finance / teal
    "gold": "#F3B147",        # HR / gold
    "coral": "#F2654C",       # IT / coral/red
    "cream": "#FFF7E8",       # App background
    "ink": "#121826",         # Main text

    # Back-compat aliases
    "primary_blue": "#00547D",
    "green": "#1FB7A6",
    "yellow": "#F3B147",
    "red": "#F2654C",
}

# -----------------------------------------------------------------------------
# Department-specific colors
# -----------------------------------------------------------------------------
DEPT_COLORS = {
    "IT": PALETTE["red"],            # Coral / red
    "HR": PALETTE["yellow"],         # Gold / yellow
    "Finance": PALETTE["green"],     # Teal / green
    "Auto": PALETTE["primary_blue"], # Default
}

# -----------------------------------------------------------------------------
# Theme CSS Loader
# -----------------------------------------------------------------------------
def _theme_css_path() -> Path:
    return Path(__file__).parent / "styles" / "theme.css"


def inject_base_css() -> None:
    """
    Inject:
    - Base theme.css (colors, typography, cards, sidebar)
    - Department button CSS overrides (Auto / IT / HR / Finance)
    """
    css_path = _theme_css_path()

    # Load external CSS if exists
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
    else:
        # Minimal fallback
        css = f"""
        :root {{
            --tri-deep-blue: {PALETTE["deep_blue"]};
            --tri-teal: {PALETTE["teal"]};
            --tri-gold: {PALETTE["gold"]};
            --tri-coral: {PALETTE["coral"]};
            --tri-cream: {PALETTE["cream"]};
            --tri-ink: {PALETTE["ink"]};
        }}

        html, body, .stApp {{
            background-color: var(--tri-cream);
            color: var(--tri-ink);
        }}
        """

    # -------------------------------------------------------------------------
    # Custom department button overrides (your block)
    # -------------------------------------------------------------------------
    dept_button_css = f"""
    <style>
    /* Shared pill shape */
    #dept-buttons .stButton>button {{
        border-radius: 30px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
        border: none;
    }}

    /* AUTO */
    button[kind="primary"][id="btn_auto"] {{
        background-color: {PALETTE['deep_blue']} !important;
        color: white !important;
    }}
    button[id="btn_auto"] {{
        background-color: rgba(0,84,125,0.15) !important;
        color: {PALETTE['deep_blue']} !important;
    }}

    /* IT */
    button[kind="primary"][id="btn_it"] {{
        background-color: {PALETTE['coral']} !important;
        color: white !important;
    }}
    button[id="btn_it"] {{
        background-color: rgba(242,101,76,0.18) !important;
        color: {PALETTE['coral']} !important;
    }}

    /* HR */
    button[kind="primary"][id="btn_hr"] {{
        background-color: {PALETTE['gold']} !important;
        color: black !important;
    }}
    button[id="btn_hr"] {{
        background-color: rgba(243,177,71,0.22) !important;
        color: #8a6500 !important;
    }}

    /* FINANCE */
    button[kind="primary"][id="btn_finance"] {{
        background-color: {PALETTE['teal']} !important;
        color: white !important;
    }}
    button[id="btn_finance"] {{
        background-color: rgba(31,183,166,0.18) !important;
        color: {PALETTE['teal']} !important;
    }}
    </style>
    """

    # Inject both theme.css + dynamic button CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(dept_button_css, unsafe_allow_html=True)
