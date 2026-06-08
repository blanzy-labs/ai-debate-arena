from typing import Protocol


class LLMProvider(Protocol):
    provider_name: str
    model_name: str

    async def generate(self, prompt: str) -> str:
        ...
