import os

def _load_streamlit_secrets():
    try:
        import streamlit as st  # type: ignore
        return st.secrets
    except Exception:
        return None


class Settings:
    def __init__(self) -> None:
        self._secrets = _load_streamlit_secrets()

    def _get(self, section: str, key: str, default=None):
        if self._secrets is not None and section in self._secrets:
            section_map = self._secrets[section]
            if key in section_map:
                return section_map[key]

        env_key = key.upper()
        if env_key in os.environ:
            return os.environ[env_key]

        return default

    @property
    def DEV_MODE(self) -> bool:
        val = os.getenv("TRIRESOLVE_DEV_MODE")
        if val is None and self._secrets is not None and "TRIRESOLVE_DEV_MODE" in self._secrets:
            val = str(self._secrets["TRIRESOLVE_DEV_MODE"])
        if val is None:
            val = "false"
        return str(val).lower() in ("1", "true", "yes")

    # Azure OpenAI core
    @property
    def openai_endpoint(self) -> str:
        return self._get("azure", "AZURE_OPENAI_ENDPOINT", "")

    @property
    def openai_api_key(self) -> str:
        return self._get("azure", "AZURE_OPENAI_API_KEY", "")

    @property
    def openai_api_version(self) -> str:
        return self._get("azure", "AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Deployment names
    @property
    def d_orchestrator(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR", "")

    @property
    def d_classifier(self) -> str:
        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER", "")

    @property
    def d_it(self) -> str:        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_IT", "")
    @property
    def d_hr(self) -> str:        return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_HR", "")
    @property
    def d_finance(self) -> str:   return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_FINANCE", "")
    @property
    def d_architect(self) -> str: return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_ARCHITECT", "")
    @property
    def d_security(self) -> str:  return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_SECURITY", "")
    @property
    def d_ops(self) -> str:       return self._get("azure", "AZURE_OPENAI_DEPLOYMENT_OPS", "")

    # Foundry bits can stay here but won’t be used by Assistant now
    @property
    def aiproject_endpoint(self) -> str:
        return self._get("azure", "AZURE_AIPROJECT_ENDPOINT", "")

    @property
    def aiproject_api_key(self) -> str:
        return self._get("azure", "AZURE_AIPROJECT_API_KEY", "")

    @property
    def aiproject_resource_id(self) -> str:
        return self._get("azure", "AZURE_AIPROJECT_RESOURCE_ID", "")


settings = Settings()
