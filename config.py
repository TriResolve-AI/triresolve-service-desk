# config.py
import os

def _load_streamlit_secrets():
    """
    Safely attempt to load Streamlit secrets.

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
    """
    Unified configuration loader for TriResolve / TriNexa.

    Priority for each value:
    1. Streamlit secrets (when running in Streamlit)
    2. Environment variables
    3. Hard-coded default (when provided)
    """

    def __init__(self) -> None:
        self._secrets = _load_streamlit_secrets()

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------
    def _get(self, section: str, key: str, default=None):
        """
        Resolve a value from Streamlit secrets → env vars → default.

        Section maps to a TOML section (e.g. [azure]) and is also used as a
        prefix for environment variables when not running under Streamlit.
        """
        # 1) Streamlit secrets (TOML-like mapping)
        if self._secrets is not None and section in self._secrets:
            section_map = self._secrets[section]
            if key in section_map:
                return section_map[key]

        # 2) Environment variables (e.g. AZURE_OPENAI_ENDPOINT)
        env_key = key.upper()
        if env_key in os.environ:
            return os.environ[env_key]

        # 3) Default
        return default

    # ------------------------------------------------------------------
    # Dev mode toggle
    # ------------------------------------------------------------------
    @property
    def DEV_MODE(self) -> bool:
        """
        If true, the application should use local canned responses instead
        of calling Azure. Respects TRIRESOLVE_DEV_MODE from env or secrets.
        """
        # Env var wins
        val = os.getenv("TRIRESOLVE_DEV_MODE")
        if val is None:
            # Also allow reading from Streamlit secrets if present
            if self._secrets is not None and "TRIRESOLVE_DEV_MODE" in self._secrets:
                val = str(self._secrets["TRIRESOLVE_DEV_MODE"])
            else:
                val = "false"
        return str(val).lower() in ("1", "true", "yes")

    # ------------------------------------------------------------------
    # Azure OpenAI (Deployments)
    # ------------------------------------------------------------------
    @property
    def openai_endpoint(self) -> str:
        return self._get("azure", "AZURE_OPENAI_ENDPOINT", "")

    @property
    def openai_api_key(self) -> str:
        return self._get("azure", "AZURE_OPENAI_API_KEY", "")

    @property
    def openai_api_version(self) -> str:
        return self._get("azure", "AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Deployment names (MUST match deployment names in Azure)
    @property
    def d_orchestrator(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR", "")

    @property
    def d_classifier(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER", "")

    @property
    def d_it(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_IT", "")

    @property
    def d_hr(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_HR", "")

    @property
    def d_finance(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_FINANCE", "")

    @property
    def d_architect(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ARCHITECT", "")

    @property
    def d_security(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_SECURITY", "")

    @property
    def d_ops(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_OPS", "")

    # ------------------------------------------------------------------
    # Azure AI Foundry (Project)
    # ------------------------------------------------------------------
    @property
    def aiproject_endpoint(self) -> str:
        return self._get("azure", "AZURE_AIPROJECT_ENDPOINT", "")

    @property
    def aiproject_api_key(self) -> str:
        # This must be the Project API key from Foundry → Project → Management → Keys
        return self._get("azure", "AZURE_AIPROJECT_API_KEY", "")

    @property
    def aiproject_resource_id(self) -> str:
        # ARM-style resource ID (used only for docs or tooling, not as a key)
        return self._get("azure", "AZURE_AIPROJECT_RESOURCE_ID", "")


# Single shared settings instance
settings = Settings()
