from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── App ────────────────────────────────────────────────────
    APP_NAME: str = "AI Business Intelligence Platform"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ── LLM ───────────────────────────────────────────────────
    GROQ_API_KEY: str = "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"
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GROQ_TEMPERATURE: float = 0.0

    # ── Search ────────────────────────────────────────────────
    TAVILY_API_KEY: str = ""

    # ── Database ──────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_biz.db"

    # ── CORS ──────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # ── Logging ───────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    model_config = {"env_file": ".env", "case_sensitive": True, "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
