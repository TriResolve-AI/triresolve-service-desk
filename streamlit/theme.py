"""Theme utilities for TriResolve Streamlit UI.

This module provides consistent styling and page header components
that can be reused across all Streamlit pages.
"""

import streamlit as st


def inject_base_css() -> None:
    """Inject global base CSS for consistent theming across all pages."""
    st.markdown(
        """
        <style>
        .main {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .triresolve-hero h1 {
            font-size: 2.4rem !important;
            margin-bottom: 0.3rem;
        }
        .triresolve-hero h3 {
            font-size: 1.1rem !important;
            font-weight: 400;
            opacity: 0.9;
            margin-top: 0;
        }
        .section-label {
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.8rem;
            color: #8a8d98;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.7rem;
            background: rgba(0, 213, 240, 0.12);
            color: #00d5f0;
            margin-right: 0.4rem;
        }
        .pill span {
            margin-left: 0.3rem;
        }
        .agent-badge {
            font-size: 0.8rem;
            padding: 0.2rem 0.5rem;
            border-radius: 999px;
            margin-right: 0.3rem;
            background: rgba(172, 70, 186, 0.12);
            color: #ac46ba;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(
    title: str,
    subtitle: str,
    logo_path: str | None = None,
) -> None:
    """Render a consistent page header with optional logo.

    Args:
        title: Main heading text.
        subtitle: Secondary descriptive text.
        logo_path: Optional path to a logo image file.
    """
    if logo_path:
        try:
            st.image(logo_path, width=120)
        except Exception:
            # If logo fails to load, continue without it
            pass

    st.markdown(
        f"""
        <div class="triresolve-hero">
            <h1>{title}</h1>
            <h3>{subtitle}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
