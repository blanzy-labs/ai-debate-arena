from typing import Any

from app.config import Settings
from app.llm.errors import MissingProviderKeyError, ProviderCallError


class OpenAIProvider:
    provider_name = "openai"

    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        api_key = settings.openai_api_key.strip()
        if not api_key:
            raise MissingProviderKeyError("OpenAI API key is not configured.")

        self.model_name = settings.openai_model
        self._client = client or self._build_client(api_key)

    async def generate(self, prompt: str) -> str:
        try:
            response = await self._client.responses.create(
                model=self.model_name,
                input=prompt,
            )
        except Exception as error:
            raise ProviderCallError("OpenAI provider call failed.") from error

        text = self._extract_text(response)
        if not text:
            raise ProviderCallError("OpenAI provider returned no usable text.")

        return text

    def _build_client(self, api_key: str) -> Any:
        from openai import AsyncOpenAI

        return AsyncOpenAI(api_key=api_key)

    def _extract_text(self, response: Any) -> str:
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        return ""
