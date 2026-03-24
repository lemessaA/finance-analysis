from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── App ────────────────────────────────────────────────────
    APP_NAME: str = "Business Insights"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ── LLM ───────────────────────────────────────────────────
    GROQ_API_KEY: str = "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"
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.0

    # ── Search ────────────────────────────────────────────────
    TAVILY_API_KEY: str = ""

    # ── Database ──────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_biz.db"

    # ── CORS ──────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:8000"]

    # ── Logging ───────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    # ── M-Pesa ──────────────────────────────────────────────
    MPESA_CONSUMER_KEY: str = ""
    MPESA_CONSUMER_SECRET: str = ""
    MPESA_PASSKEY: str = ""
    MPESA_SHORTCODE: str = ""
    MPESA_INITIATOR_NAME: str = ""
    MPESA_ENVIRONMENT: str = "sandbox"  # sandbox or production
    MPESA_CALLBACK_URL: str = "http://localhost:8000/api/v1/mpesa/callback"
    MPESA_CONFIRMATION_URL: str = "http://localhost:8000/api/v1/mpesa/confirmation"
    MPESA_VALIDATION_URL: str = "http://localhost:8000/api/v1/mpesa/validation"

    model_config = {"env_file": ".env", "case_sensitive": True, "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
