from app.config import Settings
from app.llm.base import LLMProvider
from app.llm.errors import MissingProviderKeyError, UnsupportedProviderError
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider


def get_provider(provider_name: str, settings: Settings) -> LLMProvider:
    normalized_name = provider_name.strip().lower()

    if normalized_name == "openai":
        if not settings.openai_api_key.strip():
            raise MissingProviderKeyError("OpenAI API key is not configured.")
        return OpenAIProvider(settings=settings)

    if normalized_name == "gemini":
        if not settings.gemini_api_key.strip():
            raise MissingProviderKeyError("Gemini API key is not configured.")
        return GeminiProvider(settings=settings)

    raise UnsupportedProviderError(f"Unsupported provider: {normalized_name or 'unknown'}.")
