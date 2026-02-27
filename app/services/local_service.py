"""Local model LLM service — placeholder for future implementation."""

from collections.abc import AsyncGenerator

from app.services.base import LLMService


class LocalService(LLMService):
    """LLM service using a locally hosted model with RAG.

    Not yet implemented. Will use a 1B-3B parameter model
    running on a Raspberry Pi 5 with retrieval-augmented generation.
    """

    async def stream(
        self, system_prompt: str, messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        """Stream response tokens from the local model."""
        raise NotImplementedError("Local model is not yet available.")
        yield  # noqa: RET503 — required to make this an async generator
