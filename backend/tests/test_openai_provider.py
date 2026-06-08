import pytest

from app.config import Settings
from app.llm.errors import ProviderCallError
from app.llm.openai_provider import OpenAIProvider


FAKE_KEY = "sk-fake-openai-secret"


class FakeOpenAIResponse:
    def __init__(self, output_text: str | None) -> None:
        self.output_text = output_text


class FakeOpenAIResponses:
    def __init__(self, response: FakeOpenAIResponse | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error

    async def create(self, model: str, input: str) -> FakeOpenAIResponse:
        if self.error:
            raise self.error
        return self.response or FakeOpenAIResponse(None)


class FakeOpenAIClient:
    def __init__(self, response: FakeOpenAIResponse | None = None, error: Exception | None = None) -> None:
        self.responses = FakeOpenAIResponses(response=response, error=error)


@pytest.mark.asyncio
async def test_openai_provider_returns_mocked_text() -> None:
    settings = Settings(openai_api_key=FAKE_KEY, openai_model="test-openai-model")
    client = FakeOpenAIClient(response=FakeOpenAIResponse(" mocked text "))
    provider = OpenAIProvider(settings=settings, client=client)

    result = await provider.generate("Prompt")

    assert result == "mocked text"
    assert provider.model_name == "test-openai-model"


@pytest.mark.asyncio
async def test_openai_provider_empty_response_raises_safe_error() -> None:
    settings = Settings(openai_api_key=FAKE_KEY)
    provider = OpenAIProvider(
        settings=settings,
        client=FakeOpenAIClient(response=FakeOpenAIResponse("")),
    )

    with pytest.raises(ProviderCallError) as raised:
        await provider.generate("Prompt")

    assert "no usable text" in str(raised.value)
    assert FAKE_KEY not in str(raised.value)


@pytest.mark.asyncio
async def test_openai_provider_client_exception_raises_safe_error() -> None:
    settings = Settings(openai_api_key=FAKE_KEY)
    provider = OpenAIProvider(
        settings=settings,
        client=FakeOpenAIClient(error=RuntimeError(f"boom {FAKE_KEY}")),
    )

    with pytest.raises(ProviderCallError) as raised:
        await provider.generate("Prompt")

    assert str(raised.value) == "OpenAI provider call failed."
    assert FAKE_KEY not in str(raised.value)
