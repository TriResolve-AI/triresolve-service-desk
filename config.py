import os
from functools import lru_cache


def _load_streamlit_secrets():
    """Safely attempt to load Streamlit secrets.

    This only works when running inside a Streamlit app. On the backend or in
    plain scripts, `streamlit` may not be installed or `st.secrets` may not be
    available, so we catch all exceptions and fall back to env vars.
    """
    try:
        import streamlit as st  # type: ignore

        return st.secrets
    except Exception:
        return None


class Settings:
    """Unified configuration loader for TriResolve / TriNexa.

    Priority order for each value:
    1. Streamlit secrets (when running in Streamlit)
    2. Environment variables (.env, GitHub Actions, container env)
    3. Hard-coded default (when provided)
    """

    def __init__(self) -> None:
        self._secrets = _load_streamlit_secrets()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get(self, section: str, key: str, default: str | None = None) -> str | None:
        """Resolve a value from Streamlit secrets → env vars → default.

        Section maps to a TOML section (e.g. [azure]) and is also used as a
        prefix for environment variables when not running under Streamlit.
        """

        # 1) Streamlit secrets (TOML-like mapping)
        if self._secrets is not None and section in self._secrets:
            section_map = self._secrets[section]
            if key in section_map:
                return section_map[key]

        # 2) Environment variables (e.g. AZURE_OPENAI_ENDPOINT)
        env_key = key
        if not env_key.isupper():
            env_key = key.upper()

        value = os.getenv(env_key)
        if value is not None:
            return value

        # 3) Default
        return default

    # ------------------------------------------------------------------
    # Azure core
    # ------------------------------------------------------------------
    @property
    def subscription_id(self) -> str | None:
        return self._get("azure", "AZURE_SUBSCRIPTION_ID")

    @property
    def tenant_id(self) -> str | None:
        return self._get("azure", "AZURE_TENANT_ID")

    @property
    def resource_group(self) -> str:
        return self._get("azure", "AZURE_RESOURCE_GROUP", "trinexa-rg") or "trinexa-rg"

    @property
    def location(self) -> str:
        return self._get("azure", "AZURE_LOCATION", "eastus") or "eastus"

    # ------------------------------------------------------------------
    # Azure OpenAI
    # ------------------------------------------------------------------
    @property
    def openai_endpoint(self) -> str:
        value = self._get("azure", "AZURE_OPENAI_ENDPOINT")
        if not value:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT is not configured")
        return value

    @property
    def openai_api_key(self) -> str:
        value = self._get("azure", "AZURE_OPENAI_API_KEY")
        if not value:
            raise RuntimeError("AZURE_OPENAI_API_KEY is not configured")
        return value

    @property
    def openai_api_version(self) -> str:
        return (
            self._get(
                "azure",
                "AZURE_OPENAI_API_VERSION",
                "2024-02-15-preview",
            )
            or "2024-02-15-preview"
        )

    # ------------------------------------------------------------------
    # Model deployments
    # ------------------------------------------------------------------
    @property
    def d_orchestrator(self) -> str:
        return (
            self._get(
                "azure",
                "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR",
                "triresolve-orchestrator",
            )
            or "triresolve-orchestrator"
        )

    @property
    def d_classifier(self) -> str:
        return (
            self._get(
                "azure",
                "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER",
                "triresolve-classifier",
            )
            or "triresolve-classifier"
        )

    @property
    def d_hr(self) -> str:
        return (
            self._get("azure", "AZURE_OPENAI_DEPLOYMENT_HR", "triresolve-hr")
            or "triresolve-hr"
        )

    @property
    def d_it(self) -> str:
        return (
            self._get("azure", "AZURE_OPENAI_DEPLOYMENT_IT", "triresolve-it")
            or "triresolve-it"
        )

    @property
    def d_finance(self) -> str:
        return (
            self._get(
                "azure",
                "AZURE_OPENAI_DEPLOYMENT_FINANCE",
                "triresolve-finance",
            )
            or "triresolve-finance"
        )

    @property
    def d_architect(self) -> str:
        return (
            self._get(
                "azure",
                "AZURE_OPENAI_DEPLOYMENT_ARCHITECT",
                "trinexa-architect-agent",
            )
            or "trinexa-architect-agent"
        )

    @property
    def d_security(self) -> str:
        return (
            self._get(
                "azure",
                "AZURE_OPENAI_DEPLOYMENT_SECURITY",
                "trinexa-security-agent",
            )
            or "trinexa-security-agent"
        )

    @property
    def d_ops(self) -> str:
        return (
            self._get("azure", "AZURE_OPENAI_DEPLOYMENT_OPS", "trinexa-ops-agent")
            or "trinexa-ops-agent"
        )

    # ------------------------------------------------------------------
    # Azure AI Project (Foundry)
    # ------------------------------------------------------------------
    @property
    def aiproject_endpoint(self) -> str | None:
        return self._get("azure", "AZURE_AIPROJECT_ENDPOINT")

    @property
    def aiproject_resource_id(self) -> str | None:
        return self._get("azure", "AZURE_AIPROJECT_RESOURCE_ID")


# Single shared settings instance for easy import (e.g. `from config import settings`).
# Using a plain instance keeps things simple for this sample project.
settings = Settings()
