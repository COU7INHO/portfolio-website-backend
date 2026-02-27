"""Abstract base class for LLM services."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class LLMService(ABC):
    """Interface that all LLM providers must implement."""

    @abstractmethod
    async def stream(
        self, system_prompt: str, messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        """Stream response tokens for the given conversation.

        Args:
            system_prompt: The system prompt to use.
            messages: List of message dicts with 'role' and 'content' keys.

        Yields:
            Response text chunks as they become available.
        """
