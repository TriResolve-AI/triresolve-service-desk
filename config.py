import os
from functools import lru_cache

# We only import Streamlit when running inside Streamlit.
# This prevents backend crashes when Streamlit isn't installed.
def _load_streamlit_secrets():
    try:
        import streamlit as st
        return st.secrets
    except Exception:
        return None


class Settings:
    """
    Unified configuration loader for:
    - Local backend (.env)
    - Streamlit (.streamlit/secrets.toml)
    - GitHub Actions (env vars)
    """

    def __init__(self):
        self._secrets = _load_streamlit_secrets()

    # ------------------------------
    # Helper: read value from secrets > env > default
    # ------------------------------
    def _get(self, section, key, default=None):
        # Streamlit secrets
        if self._secrets and section in self._secrets:
            if key in self._secrets[section]:
                return self._secrets[section][key]

        # Environment variable (backend / GitHub Actions)
        env_key = f"{section.upper()}_{key.upper()}"
        return os.getenv(env_key, default)

    # ------------------------------
    # Azure Core
    # ------------------------------
    @property
    def subscription_id(self):
        return self._get("azure", "AZURE_SUBSCRIPTION_ID")

    @property
    def tenant_id(self):
        return self._get("azure", "AZURE_TENANT_ID")

    @property
    def resource_group(self):
        return self._get("azure", "AZURE_RESOURCE_GROUP", "trinexa-rg")

    @property
    def location(self):
        return self._get("azure", "AZURE_LOCATION", "eastus")

    # ------------------------------
    # Azure OpenAI
    # ------------------------------
    @property
    def openai_endpoint(self):
        return self._get("azure", "AZURE_OPENAI_ENDPOINT")

    @property
    def openai_api_key(self):
        return self._get("azure", "AZURE_OPENAI_API_KEY")

    @property
    def openai_api_version(self):
        return self._get("azure", "AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # ------------------------------
    # Model Deployments
    # ------------------------------
    @property
    def d_orchestrator(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR")

    @property
    def d_classifier(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER")

    @property
    def d_hr(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_HR")

    @property
    def d_it(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_IT")

    @property
    def d_finance(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_FINANCE")

    @property
    def d_architect(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ARCHITECT")

    @property
    def d_security(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_SECURITY")

    @property
    def d_ops(self):
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_OPS")

    # ------------------------------
    # Azure AI Project (Foundry)
    # ------------------------------
    @property
    def aiproject_endpoint(self):
        return self._get("azure", "AZURE_AIPROJECT_ENDPOINT")

    @property
    def aiproject_resource_id(self):
        return self._get("azure", "AZURE_AIPROJECT_RESOURCE_ID")

    @property
    def existing_agent_id(self):
        return self._get("azure", "AZURE_EXISTING_AGENT_ID")

    # ------------------------------
    # Backend URL (Streamlit → FastAPI)
    # ------------------------------
    @property
    def backend_url(self):
        return self._get("backend", "BACKEND_URL", "http://localhost:8000")

    # ------------------------------
    # Logging
    # ------------------------------
    @property
    def log_level(self):
        return self._get("debug", "LOG_LEVEL", "INFO")


@lru_cache
def get_settings():
    """Cached settings so they’re only loaded once."""
    return Settings()


# Shortcut import
settings = get_settings()
