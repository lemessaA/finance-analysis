from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from langchain_groq import ChatGroq

from app.config import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_llm(settings: SettingsDep) -> ChatGroq:
    """Provide a ChatGroq instance as a FastAPI dependency."""
    return ChatGroq(
        model=settings.GROQ_MODEL,
        temperature=settings.GROQ_TEMPERATURE,
        api_key=settings.GROQ_API_KEY,
    )


LLMDep = Annotated[ChatGroq, Depends(get_llm)]
