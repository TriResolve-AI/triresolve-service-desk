"""Central Azure OpenAI client helpers for TriResolve / TriNexa.

This module provides:
- A cached AzureOpenAI client configured from `config.settings`.
- Thin wrapper functions for common chat-completion patterns used by the
  orchestrator and domain agents.

Backends, Streamlit pages, and background jobs can import these helpers to
avoid duplicating connection logic.
"""

from functools import lru_cache
from typing import Iterable, Mapping, Any, List

from openai import AzureOpenAI  # type: ignore

# Re-use the shared settings object from config.py
# (Make sure `config.py` lives on the Python path.)
from config import settings  # type: ignore


def _get_settings():
    # Simple wrapper in case you want to extend later
    return settings


@lru_cache(maxsize=1)
def get_azure_openai_client() -> AzureOpenAI:
    """Return a cached AzureOpenAI client.

    Reads configuration from `config.settings` (Streamlit secrets or env vars).
    """
    s = _get_settings()
    client = AzureOpenAI(
        api_key=s.openai_api_key,
        api_version=s.openai_api_version,
        azure_endpoint=s.openai_endpoint,
    )
    return client


def chat_completion(
    messages: Iterable[Mapping[str, Any]],
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> str:
    """Generic helper for chat-based completions.

    Args:
        messages: Standard OpenAI chat messages list.
        model: Optional deployment name. If omitted, uses the global
            orchestrator deployment from settings.
        temperature: Sampling temperature (defaults to 0.2 for stability).
        max_tokens: Optional max tokens for the response.
        **kwargs: Extra keyword arguments forwarded to the client.

    Returns:
        The response message content as a string.
    """
    s = _get_settings()
    deployment = model or s.d_orchestrator

    client = get_azure_openai_client()
    response = client.chat.completions.create(
        model=deployment,
        messages=list(messages),
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )

    choice = response.choices[0]
    # Newer SDKs use `.message.content`; older ones supported dict-style access.
    content = getattr(choice.message, "content", None)
    if content is None and isinstance(choice.message, Mapping):  # type: ignore[unreachable]
        content = choice.message.get("content")

    return content or ""


def orchestrator_chat(user_message: str, system_prompt: str | None = None) -> str:
    """High-level entry point for the TriResolve orchestrator.

    This can be called from Streamlit or the backend to route a user request
    through the orchestrator agent.
    """
    s = _get_settings()
    messages: List[Mapping[str, str]] = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append(
            {
                "role": "system",
                "content": (
                    "You are the central TriResolve AI orchestrator, coordinating "
                    "IT, HR, Finance, Security, Architect, and Ops agents."
                ),
            }
        )

    messages.append({"role": "user", "content": user_message})

    return chat_completion(messages, model=s.d_orchestrator)


def domain_agent_chat(user_message: str, domain: str) -> str:
    """Route a message to a specific domain agent by logical name.

    Args:
        user_message: Natural-language request.
        domain: One of: "it", "hr", "finance", "architect", "security", "ops".
    """
    s = _get_settings()
    domain = domain.lower().strip()

    deployment_map = {
        "it": s.d_it,
        "hr": s.d_hr,
        "finance": s.d_finance,
        "architect": s.d_architect,
        "security": s.d_security,
        "ops": s.d_ops,
    }

    deployment = deployment_map.get(domain)
    if not deployment:
        raise ValueError(f"Unknown domain agent: {domain!r}")

    messages = [
        {
            "role": "system",
            "content": (
                f"You are the TriResolve {domain.upper()} domain agent. "
                f"Answer only from the perspective of {domain.upper()} and "
                "escalate unclear or cross-domain issues back to the orchestrator."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    return chat_completion(messages, model=deployment)
