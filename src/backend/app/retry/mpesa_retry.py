"""
M-Pesa Retry Logic

Comprehensive retry mechanism for M-Pesa API calls with exponential backoff,
circuit breaker pattern, and graceful failure handling.
"""

from __future__ import annotations

import asyncio
import time
from typing import Callable, Any, Optional, Dict, List, Union
from dataclasses import dataclass
from enum import Enum
import random

from app.exceptions.mpesa_exceptions import MpesaException, MpesaRetryableError, MpesaErrorCode
from app.logging.mpesa_logger import get_mpesa_logger


class RetryStrategy(Enum):
    """Retry strategies for different scenarios."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_DELAY = "fixed_delay"
    LINEAR_BACKOFF = "linear_backoff"
    NO_RETRY = "no_retry"


@dataclass
class RetryConfig:
    """Configuration for retry logic."""
    max_retries: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    backoff_multiplier: float = 2.0
    jitter: bool = True
    retryable_exceptions: List[type] = None
    retryable_error_codes: List[MpesaErrorCode] = None
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    
    def __post_init__(self):
        if self.retryable_exceptions is None:
            self.retryable_exceptions = [
                MpesaRetryableError,
                ConnectionError,
                TimeoutError,
            ]
        
        if self.retryable_error_codes is None:
            self.retryable_error_codes = [
                MpesaErrorCode.API_TIMEOUT,
                MpesaErrorCode.API_CONNECTION_FAILED,
                MpesaErrorCode.API_RATE_LIMIT,
            ]


@dataclass
class RetryResult:
    """Result of a retry attempt."""
    success: bool
    result: Any = None
    exception: Optional[Exception] = None
    attempts: int = 0
    total_time: float = 0.0
    retry_delays: List[float] = None
    
    def __post_init__(self):
        if self.retry_delays is None:
            self.retry_delays = []


class CircuitBreaker:
    """Circuit breaker pattern for preventing cascade failures."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        
        self.logger = get_mpesa_logger()
    
    def __call__(self, func):
        """Decorator for circuit breaker."""
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if self._should_attempt_reset():
                    self.state = "HALF_OPEN"
                    self.logger.info("Circuit breaker transitioning to HALF_OPEN")
                else:
                    raise MpesaException(
                        message="Circuit breaker is OPEN",
                        error_code=MpesaErrorCode.API_SERVER_ERROR,
                        details={
                            "failure_count": self.failure_count,
                            "recovery_timeout": self.recovery_timeout,
                            "time_until_reset": self._time_until_reset()
                        }
                    )
            
            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except self.expected_exception as e:
                self._on_failure()
                raise e
        
        return wrapper
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset."""
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )
    
    def _time_until_reset(self) -> float:
        """Calculate time until circuit breaker resets."""
        if not self.last_failure_time:
            return 0.0
        return max(0.0, self.recovery_timeout - (time.time() - self.last_failure_time))
    
    def _on_success(self):
        """Handle successful call."""
        if self.state == "HALF_OPEN":
            self.logger.info("Circuit breaker transitioning to CLOSED")
            self.state = "CLOSED"
        
        self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.logger.warning(
                f"Circuit breaker transitioning to OPEN",
                failure_count=self.failure_count,
                threshold=self.failure_threshold
            )


class MpesaRetryHandler:
    """Handler for M-Pesa API retry logic."""
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self.logger = get_mpesa_logger()
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        retry_config: Optional[RetryConfig] = None,
        **kwargs
    ) -> RetryResult:
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Function arguments
            retry_config: Override retry config
            **kwargs: Function keyword arguments
            
        Returns:
            RetryResult with execution details
        """
        config = retry_config or self.config
        start_time = time.time()
        retry_delays = []
        last_exception = None
        
        for attempt in range(config.max_retries + 1):
            try:
                # Execute function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                # Success on first attempt
                if attempt == 0:
                    return RetryResult(
                        success=True,
                        result=result,
                        attempts=1,
                        total_time=time.time() - start_time,
                        retry_delays=[]
                    )
                
                # Success after retry
                total_time = time.time() - start_time
                self.logger.info(
                    f"Operation succeeded after {attempt} retries",
                    operation=func.__name__,
                    attempts=attempt + 1,
                    total_time=total_time,
                    retry_delays=retry_delays
                )
                
                return RetryResult(
                    success=True,
                    result=result,
                    attempts=attempt + 1,
                    total_time=total_time,
                    retry_delays=retry_delays
                )
                
            except Exception as e:
                last_exception = e
                
                # Check if exception is retryable
                if not self._is_retryable_exception(e, config):
                    self.logger.error(
                        f"Non-retryable exception in {func.__name__}",
                        operation=func.__name__,
                        attempt=attempt + 1,
                        exception_type=e.__class__.__name__,
                        exception_message=str(e)
                    )
                    break
                
                # Log retry attempt
                if attempt < config.max_retries:
                    delay = self._calculate_delay(attempt, config)
                    retry_delays.append(delay)
                    
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay:.2f}s",
                        operation=func.__name__,
                        attempt=attempt + 1,
                        max_retries=config.max_retries,
                        delay=delay,
                        exception_type=e.__class__.__name__,
                        exception_message=str(e)
                    )
                    
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(
                        f"All {config.max_retries + 1} attempts failed for {func.__name__}",
                        operation=func.__name__,
                        total_attempts=config.max_retries + 1,
                        final_exception_type=e.__class__.__name__,
                        final_exception_message=str(e)
                    )
        
        # All attempts failed
        total_time = time.time() - start_time
        return RetryResult(
            success=False,
            exception=last_exception,
            attempts=config.max_retries + 1,
            total_time=total_time,
            retry_delays=retry_delays
        )
    
    def _is_retryable_exception(self, exception: Exception, config: RetryConfig) -> bool:
        """Check if exception should be retried."""
        # Check exception types
        for retryable_type in config.retryable_exceptions:
            if isinstance(exception, retryable_type):
                return True
        
        # Check M-Pesa error codes
        if isinstance(exception, MpesaException):
            return exception.error_code in config.retryable_error_codes
        
        return False
    
    def _calculate_delay(self, attempt: int, config: RetryConfig) -> float:
        """Calculate delay for retry attempt."""
        if config.strategy == RetryStrategy.NO_RETRY:
            return 0.0
        
        elif config.strategy == RetryStrategy.FIXED_DELAY:
            delay = config.base_delay
        
        elif config.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = config.base_delay * (attempt + 1)
        
        elif config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = config.base_delay * (config.backoff_multiplier ** attempt)
        
        else:
            delay = config.base_delay
        
        # Apply jitter if enabled
        if config.jitter:
            jitter_range = delay * 0.1
            delay += random.uniform(-jitter_range, jitter_range)
        
        # Ensure delay is within bounds
        return max(0.0, min(delay, config.max_delay))


def retry_on_failure(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
    jitter: bool = True
):
    """
    Decorator for automatic retry on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries
        max_delay: Maximum delay between retries
        strategy: Retry strategy to use
        jitter: Whether to add jitter to delay
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retry_handler = MpesaRetryHandler(RetryConfig(
                max_retries=max_retries,
                base_delay=base_delay,
                max_delay=max_delay,
                strategy=strategy,
                jitter=jitter
            ))
            
            result = await retry_handler.execute_with_retry(func, *args, **kwargs)
            
            if result.success:
                return result.result
            else:
                raise result.exception
        
        return wrapper
    return decorator


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    expected_exception: type = Exception
):
    """
    Decorator for circuit breaker pattern.
    
    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Time to wait before attempting recovery
        expected_exception: Exception type to track
    """
    def decorator(func):
        breaker = CircuitBreaker(failure_threshold, recovery_timeout, expected_exception)
        return breaker(func)
    return decorator


# Global retry handler instance
mpesa_retry_handler = MpesaRetryHandler()


async def execute_mpesa_with_retry(
    func: Callable,
    *args,
    retry_config: Optional[RetryConfig] = None,
    **kwargs
) -> Any:
    """
    Execute M-Pesa function with retry logic.
    
    Args:
        func: Function to execute
        *args: Function arguments
        retry_config: Retry configuration
        **kwargs: Function keyword arguments
        
    Returns:
        Function result
        
    Raises:
        Exception: Last exception if all retries failed
    """
    result = await mpesa_retry_handler.execute_with_retry(
        func, *args, retry_config=retry_config, **kwargs
    )
    
    if result.success:
        return result.result
    else:
        raise result.exception
