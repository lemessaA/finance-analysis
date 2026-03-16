from __future__ import annotations

from fastapi import HTTPException, status


class AIBizException(Exception):
    """Base exception for the platform."""
    def __init__(self, message: str, details: str | None = None):
        super().__init__(message)
        self.message = message
        self.details = details


class AgentExecutionError(AIBizException):
    """Raised when an agent fails to complete its task."""


class PDFExtractionError(AIBizException):
    """Raised when PDF parsing fails."""


class ForecastingError(AIBizException):
    """Raised when the forecasting pipeline fails."""


class InsufficientDataError(AIBizException):
    """Raised when not enough data points are provided."""


def raise_not_found(resource: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found.",
    )


def raise_bad_request(detail: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )
