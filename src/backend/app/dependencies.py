from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from langchain_openai import ChatOpenAI

from app.config import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_llm(settings: SettingsDep) -> ChatOpenAI:
    """Provide a ChatOpenAI instance as a FastAPI dependency."""
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
    )


LLMDep = Annotated[ChatOpenAI, Depends(get_llm)]
