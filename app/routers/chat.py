"""Chat endpoint with streaming responses."""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.config import limiter, settings
from app.schemas.chat import ChatRequest
from app.services.local_service import LocalService
from app.services.openai_service import OpenAIService

router = APIRouter()

SERVICES = {
    "openai": OpenAIService,
    "local": LocalService,
}


@router.get("/health")
async def health() -> dict:
    """Health check endpoint for Docker and Nginx."""
    return {"status": "ok"}


@router.post("/chat")
@limiter.limit(settings.rate_limit)
async def chat(request: Request, body: ChatRequest) -> StreamingResponse:
    """Stream a chat response using the selected LLM provider.

    The system prompt is loaded at startup and injected automatically.
    The frontend sends the full conversation history in each request.
    """
    system_prompt: str = request.app.state.system_prompt
    service = SERVICES[body.provider]()

    messages = [msg.model_dump() for msg in body.messages]

    return StreamingResponse(
        service.stream(system_prompt, messages),
        media_type="text/event-stream",
    )
