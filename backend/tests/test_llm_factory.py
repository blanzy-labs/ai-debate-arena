import pytest

from app.config import Settings
from app.llm.errors import MissingProviderKeyError, UnsupportedProviderError
from app.llm.factory import get_provider
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider


def test_get_openai_provider_when_key_exists() -> None:
    settings = Settings(openai_api_key="fake-openai-key")

    provider = get_provider("openai", settings)

    assert isinstance(provider, OpenAIProvider)
    assert provider.model_name == "gpt-4.1-mini"


def test_get_gemini_provider_when_key_exists() -> None:
    settings = Settings(gemini_api_key="fake-gemini-key")

    provider = get_provider("gemini", settings)

    assert isinstance(provider, GeminiProvider)
    assert provider.model_name == "gemini-2.5-flash"


def test_invalid_provider_raises_safe_error() -> None:
    settings = Settings()

    with pytest.raises(UnsupportedProviderError, match="Unsupported provider"):
        get_provider("anthropic", settings)


def test_missing_openai_key_raises_safe_error() -> None:
    settings = Settings(openai_api_key="")

    with pytest.raises(MissingProviderKeyError, match="OpenAI API key is not configured"):
        get_provider("openai", settings)


def test_missing_gemini_key_raises_safe_error() -> None:
    settings = Settings(gemini_api_key="")

    with pytest.raises(MissingProviderKeyError, match="Gemini API key is not configured"):
        get_provider("gemini", settings)
