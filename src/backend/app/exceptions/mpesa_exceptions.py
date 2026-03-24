"""
M-Pesa Custom Exceptions

Custom exception classes for M-Pesa payment processing with proper error codes
and user-friendly messages.
"""

from __future__ import annotations

from typing import Optional, Dict, Any
from enum import Enum


class MpesaErrorCode(Enum):
    """M-Pesa error codes for different failure scenarios."""
    
    # Authentication Errors
    INVALID_CREDENTIALS = "AUTH_001"
    TOKEN_EXPIRED = "AUTH_002"
    TOKEN_GENERATION_FAILED = "AUTH_003"
    
    # Validation Errors
    INVALID_PHONE_NUMBER = "VAL_001"
    INVALID_AMOUNT = "VAL_002"
    INVALID_SHORTCODE = "VAL_003"
    MISSING_REQUIRED_FIELD = "VAL_004"
    
    # API Errors
    API_TIMEOUT = "API_001"
    API_CONNECTION_FAILED = "API_002"
    API_RATE_LIMIT = "API_003"
    API_SERVER_ERROR = "API_004"
    
    # Transaction Errors
    TRANSACTION_FAILED = "TXN_001"
    INSUFFICIENT_FUNDS = "TXN_002"
    DUPLICATE_TRANSACTION = "TXN_003"
    TRANSACTION_NOT_FOUND = "TXN_004"
    TRANSACTION_TIMEOUT = "TXN_005"
    
    # System Errors
    CONFIGURATION_ERROR = "SYS_001"
    DATABASE_ERROR = "SYS_002"
    UNKNOWN_ERROR = "SYS_999"


class MpesaException(Exception):
    """Base M-Pesa exception class."""
    
    def __init__(
        self,
        message: str,
        error_code: MpesaErrorCode = MpesaErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.original_error = original_error
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error_code": self.error_code.value,
            "message": self.message,
            "details": self.details,
            "type": self.__class__.__name__
        }


class MpesaAuthenticationError(MpesaException):
    """Authentication-related M-Pesa errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=MpesaErrorCode.INVALID_CREDENTIALS,
            details=details,
            original_error=original_error
        )


class MpesaValidationError(MpesaException):
    """Input validation errors for M-Pesa requests."""
    
    def __init__(self, message: str, field: str, value: Any, details: Optional[Dict[str, Any]] = None):
        enhanced_details = {
            "field": field,
            "value": value,
            **(details or {})
        }
        super().__init__(
            message=message,
            error_code=MpesaErrorCode.INVALID_PHONE_NUMBER,
            details=enhanced_details
        )


class MpesaAPIError(MpesaException):
    """M-Pesa API communication errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        details = {
            "status_code": status_code,
            "response_data": response_data
        }
        
        # Determine error code based on status code
        if status_code == 429:
            error_code = MpesaErrorCode.API_RATE_LIMIT
        elif status_code and status_code >= 500:
            error_code = MpesaErrorCode.API_SERVER_ERROR
        elif status_code and status_code >= 400:
            error_code = MpesaErrorCode.API_CONNECTION_FAILED
        else:
            error_code = MpesaErrorCode.API_CONNECTION_FAILED
            
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            original_error=original_error
        )


class MpesaTransactionError(MpesaException):
    """M-Pesa transaction processing errors."""
    
    def __init__(
        self, 
        message: str, 
        transaction_id: Optional[str] = None,
        response_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        enhanced_details = {
            "transaction_id": transaction_id,
            "response_code": response_code,
            **(details or {})
        }
        
        # Determine error code based on response code
        if response_code == "1":
            error_code = MpesaErrorCode.INSUFFICIENT_FUNDS
        elif response_code == "1037":
            error_code = MpesaErrorCode.DUPLICATE_TRANSACTION
        elif response_code == "1032":
            error_code = MpesaErrorCode.TRANSACTION_TIMEOUT
        else:
            error_code = MpesaErrorCode.TRANSACTION_FAILED
            
        super().__init__(
            message=message,
            error_code=error_code,
            details=enhanced_details
        )


class MpesaConfigurationError(MpesaException):
    """M-Pesa configuration errors."""
    
    def __init__(self, message: str, missing_fields: Optional[list] = None):
        details = {"missing_fields": missing_fields or []}
        super().__init__(
            message=message,
            error_code=MpesaErrorCode.CONFIGURATION_ERROR,
            details=details
        )


class MpesaRetryableError(MpesaException):
    """Errors that can be retried."""
    
    def __init__(
        self, 
        message: str, 
        retry_count: int = 0,
        max_retries: int = 3,
        original_error: Optional[Exception] = None
    ):
        details = {
            "retry_count": retry_count,
            "max_retries": max_retries,
            "can_retry": retry_count < max_retries
        }
        super().__init__(
            message=message,
            error_code=MpesaErrorCode.API_TIMEOUT,
            details=details,
            original_error=original_error
        )


def handle_mpesa_exception(func):
    """Decorator for handling M-Pesa exceptions consistently."""
    
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MpesaException as e:
            # Re-raise M-Pesa exceptions as-is
            raise e
        except Exception as e:
            # Convert unknown exceptions to MpesaException
            raise MpesaException(
                message=f"Unexpected error in {func.__name__}: {str(e)}",
                error_code=MpesaErrorCode.UNKNOWN_ERROR,
                original_error=e
            )
    
    return wrapper
