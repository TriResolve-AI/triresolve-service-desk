from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Central configuration for the backend.

    Values are pulled from environment variables and optionally a .env file
    in the repo root.
    """

    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_model: str = "gpt-4o-mini"  # or your AOAI deployment name

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
