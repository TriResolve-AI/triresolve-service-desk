# config.py
from __future__ import annotations

import os
from typing import Any, Optional


def _load_streamlit_secrets() -> Optional[dict[str, Any]]:
    """Safely try to load Streamlit secrets.

    When running inside Streamlit, we can read st.secrets.
    In other contexts (backend scripts, local tests), this may not exist.
    """
    try:
        import streamlit as st  # type: ignore

        return st.secrets  # type: ignore[no-any-return]
    except Exception:
        return None


class Settings:
    """Unified configuration loader for TriResolve / TriNexa.

    Priority order:
      1. Streamlit secrets (TOML)
      2. Environment variables
      3. Hard-coded default (when provided)
    """

    def __init__(self) -> None:
        self._secrets = _load_streamlit_secrets()

    # ------------- internal helper -------------

    def _get(self, section: str, key: str, default: Optional[str] = None) -> Optional[str]:
        # 1) Streamlit secrets: [section] key = "value"
        if self._secrets is not None and section in self._secrets:
            section_map = self._secrets[section]
            if key in section_map:
                val = section_map[key]
                return str(val) if val is not None else None

        # 2) Environment variables (upper-case key)
        env_key = key.upper()
        val = os.getenv(env_key)
        if val is not None:
            return val

        # 3) default
        return default

    # ------------- dev flag -------------

    @property
    def DEV_MODE(self) -> bool:
        """If true, UI should use canned responses instead of Azure."""
        # env overrides everything
        env_val = os.getenv("TRIRESOLVE_DEV_MODE")
        if env_val is not None:
            return env_val.lower() in ("1", "true", "yes")

        # otherwise read from secrets root (not [azure])
        if self._secrets is not None and "TRIRESOLVE_DEV_MODE" in self._secrets:
            return str(self._secrets["TRIRESOLVE_DEV_MODE"]).lower() in (
                "1",
                "true",
                "yes",
            )

        return False

    # ------------- Azure OpenAI (SDK) -------------

    @property
    def openai_endpoint(self) -> str:
        # Example: "https://trinexaai.openai.azure.com/"
        value = self._get("azure", "AZURE_OPENAI_ENDPOINT")
        if not value:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT is not configured.")
        return value.rstrip("/")

    @property
    def openai_api_key(self) -> str:
        value = self._get("azure", "AZURE_OPENAI_API_KEY")
        if not value:
            raise RuntimeError("AZURE_OPENAI_API_KEY is not configured.")
        return value

    @property
    def openai_api_version(self) -> str:
        # 2024-10-21-preview works for gpt-4.1 / gpt-4o
        return self._get("azure", "AZURE_OPENAI_API_VERSION", "2024-10-21-preview")  # type: ignore[return-value]

    # “Model” values here are what we pass to client.chat.completions.create(model=...)
    # In your secrets, these are currently set to "gpt-4.1", "gpt-4o", etc.
    @property
    def d_orchestrator(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR", "gpt-4.1") or "gpt-4.1"

    @property
    def d_classifier(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER", "gpt-4.1-mini") or "gpt-4.1-mini"

    @property
    def d_it(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_IT", "gpt-4o") or "gpt-4o"

    @property
    def d_hr(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_HR", "gpt-4.1") or "gpt-4.1"

    @property
    def d_finance(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_FINANCE", "gpt-4o") or "gpt-4o"

    @property
    def d_architect(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ARCHITECT", "gpt-4.1-mini") or "gpt-4.1-mini"

    @property
    def d_security(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_SECURITY", "gpt-4.1") or "gpt-4.1"

    @property
    def d_ops(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_OPS", "gpt-4o") or "gpt-4o"

    # ------------- (optional) Foundry fields, in case we use them later -------------

    @property
    def aiproject_endpoint(self) -> Optional[str]:
        return self._get("azure", "AZURE_AIPROJECT_ENDPOINT")

    @property
    def aiproject_api_key(self) -> Optional[str]:
        return self._get("azure", "AZURE_AIPROJECT_API_KEY")


# Single instance to import everywhere
settings = Settings()
