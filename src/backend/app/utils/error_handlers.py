"""
Global exception handlers for FastAPI application.
Provides centralized error handling and consistent error responses.
"""

from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Dict, Any

from app.utils.exceptions import AIBizException
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ErrorResponse:
    """Standardized error response format."""
    def __init__(
        self,
        message: str,
        error_code: str = None,
        details: Dict[str, Any] = None,
        status_code: int = 500
    ):
        self.message = message
        self.error_code = error_code or "INTERNAL_ERROR"
        self.details = details or {}
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "message": self.message,
                "code": self.error_code,
                "details": self.details,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }

def setup_global_exception_handlers(app: FastAPI):
    """Register global exception handlers for the FastAPI app."""
    
    @app.exception_handler(AIBizException)
    async def ai_biz_exception_handler(request: Request, exc: AIBizException):
        """Handle custom business logic exceptions."""
        logger.error(f"Business exception: {exc.message} - {exc.details}")
        
        error_response = ErrorResponse(
            message=exc.message,
            error_code="BUSINESS_ERROR",
            details={"additional_info": exc.details} if exc.details else {},
            status_code=400
        )
        
        return JSONResponse(
            status_code=400,
            content=error_response.to_dict()
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
        
        error_response = ErrorResponse(
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
            status_code=exc.status_code
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.to_dict()
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        logger.warning(f"Validation error: {exc.errors()}")
        
        error_details = []
        for error in exc.errors():
            error_details.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        error_response = ErrorResponse(
            message="Invalid request data",
            error_code="VALIDATION_ERROR",
            details={"validation_errors": error_details},
            status_code=422
        )
        
        return JSONResponse(
            status_code=422,
            content=error_response.to_dict()
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle Starlette HTTP exceptions."""
        logger.warning(f"Starlette HTTP exception: {exc.status_code} - {exc.detail}")
        
        error_response = ErrorResponse(
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
            status_code=exc.status_code
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.to_dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other unexpected exceptions."""
        logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
        
        # Don't expose internal error details in production
        error_response = ErrorResponse(
            message="An unexpected error occurred. Please try again later.",
            error_code="INTERNAL_ERROR",
            status_code=500
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response.to_dict()
        )

def create_error_response(
    message: str,
    error_code: str = None,
    details: Dict[str, Any] = None,
    status_code: int = 500
) -> JSONResponse:
    """Helper function to create standardized error responses."""
    error_response = ErrorResponse(
        message=message,
        error_code=error_code,
        details=details,
        status_code=status_code
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.to_dict()
    )
