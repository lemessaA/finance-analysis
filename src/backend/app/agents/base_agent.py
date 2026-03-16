from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from langchain_groq import ChatGroq

from app.config import settings
from app.utils.logger import setup_logger


class BaseAgent(ABC):
    """Abstract base class for all AI agents in the platform."""

    def __init__(self, name: str, temperature: float = 0.0):
        self.name = name
        self.logger = setup_logger(f"agent.{name}")
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            temperature=temperature,
            api_key=settings.GROQ_API_KEY,
        )

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the agent's main logic."""
        ...

    def _log_start(self, task: str) -> None:
        self.logger.info(f"[{self.name}] Starting: {task}")

    def _log_done(self, task: str) -> None:
        self.logger.info(f"[{self.name}] Completed: {task}")
