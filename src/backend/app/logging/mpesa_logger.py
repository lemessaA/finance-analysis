"""
M-Pesa Logging System

Comprehensive logging system for M-Pesa payment processing with structured logging,
multiple output destinations, and log levels.
"""

from __future__ import annotations

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum
import traceback

from app.exceptions.mpesa_exceptions import MpesaException, MpesaErrorCode


class MpesaLogLevel(Enum):
    """M-Pesa specific log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MpesaLogCategory(Enum):
    """M-Pesa log categories for better organization."""
    AUTHENTICATION = "AUTH"
    VALIDATION = "VALIDATION"
    API_CALL = "API"
    TRANSACTION = "TRANSACTION"
    CALLBACK = "CALLBACK"
    ERROR = "ERROR"
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"


class MpesaLogger:
    """Enhanced logger for M-Pesa payment processing."""
    
    def __init__(
        self,
        name: str = "mpesa",
        log_file: Optional[str] = None,
        console_output: bool = True,
        json_format: bool = True
    ):
        self.name = name
        self.log_file = log_file
        self.console_output = console_output
        self.json_format = json_format
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup formatters
        self.json_formatter = self._create_json_formatter()
        self.text_formatter = self._create_text_formatter()
        
        # Add handlers
        self._setup_handlers()
    
    def _create_json_formatter(self) -> logging.Formatter:
        """Create JSON formatter for structured logging."""
        return logging.Formatter(
            '%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _create_text_formatter(self) -> logging.Formatter:
        """Create text formatter for human-readable logs."""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(category)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _setup_handlers(self):
        """Setup console and file handlers."""
        # Console handler
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(
                self.json_formatter if self.json_format else self.text_formatter
            )
            self.logger.addHandler(console_handler)
        
        # File handler
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                self.json_formatter if self.json_format else self.text_formatter
            )
            self.logger.addHandler(file_handler)
    
    def _format_log_entry(
        self,
        message: str,
        category: MpesaLogCategory,
        level: MpesaLogLevel,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format log entry for structured logging."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "mpesa",
            "level": level.value,
            "category": category.value,
            "message": message,
            **(extra_data or {})
        }
        
        if self.json_format:
            return json.dumps(log_entry, default=str)
        else:
            # Text format with extra data
            extra_info = ""
            if extra_data:
                extra_info = f" | {json.dumps(extra_data, default=str)}"
            return f"{message}{extra_info}"
    
    def debug(
        self,
        message: str,
        category: MpesaLogCategory = MpesaLogCategory.SYSTEM,
        **extra_data
    ):
        """Log debug message."""
        formatted_message = self._format_log_entry(message, category, MpesaLogLevel.DEBUG, extra_data)
        self.logger.debug(formatted_message, extra={"category": category.value})
    
    def info(
        self,
        message: str,
        category: MpesaLogCategory = MpesaLogCategory.SYSTEM,
        **extra_data
    ):
        """Log info message."""
        formatted_message = self._format_log_entry(message, category, MpesaLogLevel.INFO, extra_data)
        self.logger.info(formatted_message, extra={"category": category.value})
    
    def warning(
        self,
        message: str,
        category: MpesaLogCategory = MpesaLogCategory.SYSTEM,
        **extra_data
    ):
        """Log warning message."""
        formatted_message = self._format_log_entry(message, category, MpesaLogLevel.WARNING, extra_data)
        self.logger.warning(formatted_message, extra={"category": category.value})
    
    def error(
        self,
        message: str,
        category: MpesaLogCategory = MpesaLogCategory.ERROR,
        exception: Optional[Exception] = None,
        **extra_data
    ):
        """Log error message."""
        error_data = extra_data.copy()
        
        if exception:
            error_data.update({
                "exception_type": exception.__class__.__name__,
                "exception_message": str(exception),
                "traceback": traceback.format_exc()
            })
            
            # Add M-Pesa specific error details
            if isinstance(exception, MpesaException):
                error_data.update({
                    "mpesa_error_code": exception.error_code.value,
                    "mpesa_details": exception.details
                })
        
        formatted_message = self._format_log_entry(message, category, MpesaLogLevel.ERROR, error_data)
        self.logger.error(formatted_message, extra={"category": category.value})
    
    def critical(
        self,
        message: str,
        category: MpesaLogCategory = MpesaLogCategory.ERROR,
        exception: Optional[Exception] = None,
        **extra_data
    ):
        """Log critical message."""
        error_data = extra_data.copy()
        
        if exception:
            error_data.update({
                "exception_type": exception.__class__.__name__,
                "exception_message": str(exception),
                "traceback": traceback.format_exc()
            })
            
            if isinstance(exception, MpesaException):
                error_data.update({
                    "mpesa_error_code": exception.error_code.value,
                    "mpesa_details": exception.details
                })
        
        formatted_message = self._format_log_entry(message, category, MpesaLogLevel.CRITICAL, error_data)
        self.logger.critical(formatted_message, extra={"category": category.value})
    
    def log_authentication(
        self,
        action: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log authentication events."""
        message = f"Authentication {action}: {'Success' if success else 'Failed'}"
        self.info(
            message,
            category=MpesaLogCategory.AUTHENTICATION,
            action=action,
            success=success,
            **(details or {})
        )
    
    def log_validation(
        self,
        field_name: str,
        field_value: Any,
        success: bool,
        error_message: Optional[str] = None
    ):
        """Log validation events."""
        message = f"Validation {'Success' if success else 'Failed'} for {field_name}"
        data = {
            "field_name": field_name,
            "field_value": str(field_value),
            "success": success
        }
        
        if not success and error_message:
            data["error_message"] = error_message
        
        if success:
            self.debug(message, category=MpesaLogCategory.VALIDATION, **data)
        else:
            self.warning(message, category=MpesaLogCategory.VALIDATION, **data)
    
    def log_api_call(
        self,
        method: str,
        url: str,
        status_code: Optional[int] = None,
        response_time_ms: Optional[float] = None,
        success: Optional[bool] = None,
        error_message: Optional[str] = None
    ):
        """Log API calls."""
        message = f"API Call: {method} {url}"
        data = {
            "method": method,
            "url": url
        }
        
        if status_code is not None:
            data["status_code"] = status_code
            success = 200 <= status_code < 400
        
        if response_time_ms is not None:
            data["response_time_ms"] = response_time_ms
        
        if success is not None:
            data["success"] = success
        
        if error_message:
            data["error_message"] = error_message
        
        if success:
            self.info(message, category=MpesaLogCategory.API_CALL, **data)
        else:
            self.error(message, category=MpesaLogCategory.API_CALL, **data)
    
    def log_transaction(
        self,
        transaction_type: str,
        transaction_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        amount: Optional[float] = None,
        status: Optional[str] = None,
        success: Optional[bool] = None,
        error_message: Optional[str] = None
    ):
        """Log transaction events."""
        message = f"Transaction {transaction_type}"
        data = {"transaction_type": transaction_type}
        
        if transaction_id:
            data["transaction_id"] = transaction_id
        
        if phone_number:
            # Mask phone number for privacy
            masked_phone = phone_number[:6] + "XXX" + phone_number[-2:]
            data["phone_number"] = masked_phone
        
        if amount:
            data["amount"] = amount
        
        if status:
            data["status"] = status
        
        if success is not None:
            data["success"] = success
        
        if error_message:
            data["error_message"] = error_message
        
        if success:
            self.info(message, category=MpesaLogCategory.TRANSACTION, **data)
        else:
            self.error(message, category=MpesaLogCategory.TRANSACTION, **data)
    
    def log_callback(
        self,
        callback_type: str,
        transaction_id: Optional[str] = None,
        success: bool = True,
        data: Optional[Dict[str, Any]] = None
    ):
        """Log callback events."""
        message = f"Callback {callback_type}: {'Success' if success else 'Failed'}"
        log_data = {
            "callback_type": callback_type,
            "success": success
        }
        
        if transaction_id:
            log_data["transaction_id"] = transaction_id
        
        if data:
            log_data["callback_data"] = data
        
        self.info(message, category=MpesaLogCategory.CALLBACK, **log_data)
    
    def log_security_event(
        self,
        event_type: str,
        severity: str = "medium",
        details: Optional[Dict[str, Any]] = None
    ):
        """Log security events."""
        message = f"Security Event: {event_type}"
        self.warning(
            message,
            category=MpesaLogCategory.SECURITY,
            event_type=event_type,
            severity=severity,
            **(details or {})
        )


# Global logger instance
mpesa_logger = MpesaLogger(
    name="mpesa",
    log_file="logs/mpesa.log",
    console_output=True,
    json_format=True
)


def get_mpesa_logger() -> MpesaLogger:
    """Get the global M-Pesa logger instance."""
    return mpesa_logger
