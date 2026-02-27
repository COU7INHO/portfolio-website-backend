"""OpenAI LLM service implementation."""

from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from app.config import settings
from app.services.base import LLMService


class OpenAIService(LLMService):
    """LLM service powered by the OpenAI API."""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def stream(
        self, system_prompt: str, messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        """Stream response tokens from OpenAI."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt}, *messages],
            temperature=settings.openai_temperature,
            max_tokens=settings.openai_max_tokens,
            stream=True,
        )
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
