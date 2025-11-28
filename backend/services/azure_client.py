# backend/api/services/azure_client.py

from openai import AzureOpenAI

from backend.config import get_settings

settings = get_settings()

# Single shared Azure OpenAI client
client = AzureOpenAI(
    api_key=settings.azure_openai_api_key,
    api_version=settings.azure_openai_api_version,
    azure_endpoint=settings.azure_openai_endpoint,
)


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
    *,
    temperature: float = 0.2,
    max_tokens: int | None = None,
) -> str:
    """
    Helper that wraps Azure OpenAI chat completions.

    Returns the string content of the first choice.
    """
    model_name = model or settings.azure_openai_model

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content or ""
