import pytest

from app.config import Settings
from app.llm.errors import MissingProviderKeyError, ProviderCallError, UnsupportedProviderError
from app.llm.factory import get_provider
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider


def test_unsupported_provider_error_is_safe() -> None:
    with pytest.raises(UnsupportedProviderError) as raised:
        get_provider("bad-provider", Settings())

    assert str(raised.value) == "Unsupported provider: bad-provider."


def test_missing_keys_are_safe() -> None:
    with pytest.raises(MissingProviderKeyError) as openai_error:
        OpenAIProvider(Settings(openai_api_key=""))

    with pytest.raises(MissingProviderKeyError) as gemini_error:
        GeminiProvider(Settings(gemini_api_key=""))

    assert str(openai_error.value) == "OpenAI API key is not configured."
    assert str(gemini_error.value) == "Gemini API key is not configured."


def test_provider_call_error_does_not_expose_cause_in_message() -> None:
    secret = "secret-value"
    error = ProviderCallError("OpenAI provider call failed.")
    error.__cause__ = RuntimeError(secret)

    assert str(error) == "OpenAI provider call failed."
    assert secret not in str(error)
