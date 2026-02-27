"""FastAPI application for the portfolio chatbot."""

from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import limiter, settings
from app.routers import chat

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent.parent / "about-me.md"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the system prompt once at startup."""
    app.state.system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    yield


app = FastAPI(title="Portfolio Chatbot", lifespan=lifespan)

def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Return a 429 with the exact time the user can retry."""
    default_response = _rate_limit_exceeded_handler(request, exc)
    retry_after = int(default_response.headers.get("Retry-After", 60))
    retry_at = datetime.now(timezone.utc) + timedelta(seconds=retry_after)
    return JSONResponse(
        status_code=429,
        content={"detail": f"Too many requests. Try again at {retry_at.strftime('%H:%M:%S')} UTC."},
        headers={"Retry-After": str(retry_after)},
    )


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(chat.router)
