import asyncio
from typing import Any

from app.config import Settings
from app.llm.errors import MissingProviderKeyError, ProviderCallError


class GeminiProvider:
    provider_name = "gemini"

    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        api_key = settings.gemini_api_key.strip()
        if not api_key:
            raise MissingProviderKeyError("Gemini API key is not configured.")

        self.model_name = settings.gemini_model
        self._client = client or self._build_client(api_key)

    async def generate(self, prompt: str) -> str:
        try:
            response = await asyncio.to_thread(
                self._client.models.generate_content,
                model=self.model_name,
                contents=prompt,
            )
        except Exception as error:
            raise ProviderCallError("Gemini provider call failed.") from error

        text = self._extract_text(response)
        if not text:
            raise ProviderCallError("Gemini provider returned no usable text.")

        return text

    def _build_client(self, api_key: str) -> Any:
        from google import genai

        return genai.Client(api_key=api_key)

    def _extract_text(self, response: Any) -> str:
        text = getattr(response, "text", None)
        if isinstance(text, str) and text.strip():
            return text.strip()

        return ""
