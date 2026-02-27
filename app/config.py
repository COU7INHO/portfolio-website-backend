"""Application settings and shared instances."""

from pydantic_settings import BaseSettings
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.5
    openai_max_tokens: int = 500
    rate_limit: str = "5/minute"
    allowed_origins: list[str] = ["https://tiago-coutinho.com"]

    model_config = {"env_file": ".env"}


settings = Settings()

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
