import pytest

from app.config import Settings
from app.llm.errors import ProviderCallError
from app.llm.gemini_provider import GeminiProvider


FAKE_KEY = "fake-gemini-secret"


class FakeGeminiResponse:
    def __init__(self, text: str | None) -> None:
        self.text = text


class FakeGeminiModels:
    def __init__(self, response: FakeGeminiResponse | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error

    def generate_content(self, model: str, contents: str) -> FakeGeminiResponse:
        if self.error:
            raise self.error
        return self.response or FakeGeminiResponse(None)


class FakeGeminiClient:
    def __init__(self, response: FakeGeminiResponse | None = None, error: Exception | None = None) -> None:
        self.models = FakeGeminiModels(response=response, error=error)


@pytest.mark.asyncio
async def test_gemini_provider_returns_mocked_text() -> None:
    settings = Settings(gemini_api_key=FAKE_KEY, gemini_model="test-gemini-model")
    client = FakeGeminiClient(response=FakeGeminiResponse(" mocked text "))
    provider = GeminiProvider(settings=settings, client=client)

    result = await provider.generate("Prompt")

    assert result == "mocked text"
    assert provider.model_name == "test-gemini-model"


@pytest.mark.asyncio
async def test_gemini_provider_empty_response_raises_safe_error() -> None:
    settings = Settings(gemini_api_key=FAKE_KEY)
    provider = GeminiProvider(
        settings=settings,
        client=FakeGeminiClient(response=FakeGeminiResponse("")),
    )

    with pytest.raises(ProviderCallError) as raised:
        await provider.generate("Prompt")

    assert "no usable text" in str(raised.value)
    assert FAKE_KEY not in str(raised.value)


@pytest.mark.asyncio
async def test_gemini_provider_client_exception_raises_safe_error() -> None:
    settings = Settings(gemini_api_key=FAKE_KEY)
    provider = GeminiProvider(
        settings=settings,
        client=FakeGeminiClient(error=RuntimeError(f"boom {FAKE_KEY}")),
    )

    with pytest.raises(ProviderCallError) as raised:
        await provider.generate("Prompt")

    assert str(raised.value) == "Gemini provider call failed."
    assert FAKE_KEY not in str(raised.value)
