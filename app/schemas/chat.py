"""Request and response schemas for the chat endpoint."""

from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    """A single message in the conversation."""

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Incoming chat request from the frontend."""

    messages: list[Message]
    provider: Literal["openai", "local"] = "openai"
