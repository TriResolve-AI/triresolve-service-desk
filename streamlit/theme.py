"""
TriResolveAI Streamlit theme helpers.

- PALETTE: single source of truth for brand colors
- inject_base_css(): loads styles/theme.css and injects it into the app

Usage in a page:

    from theme import PALETTE, inject_base_css

    inject_base_css()
    # now build your Streamlit layout

"""

from __future__ import annotations

from pathlib import Path
import streamlit as st

# --- Brand Palette (Final TriResolveAI) --------------------------------------

PALETTE = {
    "deep_blue": "#00547D",   # Primary blue (logo top)
    "teal": "#1FB7A6",        # Teal loop
    "gold": "#F3B147",        # Gold loop
    "coral": "#F2654C",       # Coral loop
    "cream": "#FFF7E8",       # Soft background
    "ink": "#121826",         # Primary text
}


def _theme_css_path() -> Path:
    """Return the path to the base CSS file."""
    return Path(__file__).parent / "styles" / "theme.css"


def inject_base_css() -> None:
    """
    Inject the shared TriResolveAI theme CSS.

    This:
    - sets global background / text colors
    - styles sidebar, buttons, and basic cards
    - defines utility classes used across pages
    """
    css_path = _theme_css_path()

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
    else:
        # Very small fallback so the app is still readable
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

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
