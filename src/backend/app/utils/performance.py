"""
Performance optimization utilities for the AI Database Chat Interface.
"""

import asyncio
import time
import psutil
import functools
from typing import Any, Callable, Dict, Optional, TypeVar
from contextlib import asynccontextmanager
import logging
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

T = TypeVar('T')

# Performance metrics storage
performance_metrics = defaultdict(list)


class PerformanceMonitor:
    """Monitor and track application performance metrics."""
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Get current memory usage statistics."""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "percent": process.memory_percent()
        }
    
    @staticmethod
    def get_cpu_usage() -> float:
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def log_performance_metrics(operation: str, duration: float, **kwargs):
        """Log performance metrics for an operation."""
        metrics = {
            "operation": operation,
            "duration_ms": duration * 1000,
            "timestamp": time.time(),
            "memory": PerformanceMonitor.get_memory_usage(),
            "cpu": PerformanceMonitor.get_cpu_usage(),
            **kwargs
        }
        performance_metrics[operation].append(metrics)
        
        # Keep only last 100 metrics per operation
        if len(performance_metrics[operation]) > 100:
            performance_metrics[operation] = performance_metrics[operation][-100:]
        
        logger.info(f"Performance: {operation} took {duration:.3f}s")


def performance_timer(operation_name: Optional[str] = None):
    """Decorator to measure and log function execution time."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            start_time = time.time()
            name = operation_name or f"{func.__module__}.{func.__name__}"
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                PerformanceMonitor.log_performance_metrics(name, duration)
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            start_time = time.time()
            name = operation_name or f"{func.__module__}.{func.__name__}"
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                PerformanceMonitor.log_performance_metrics(name, duration)
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


class SimpleCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def _is_expired(self, key: str) -> bool:
        """Check if a cache entry is expired."""
        if key not in self.cache:
            return True
        return time.time() > self.cache[key]["expires_at"]
    
    def _evict_if_needed(self):
        """Evict oldest entries if cache is full."""
        if len(self.cache) >= self.max_size:
            # Sort by expiration time and remove oldest 25%
            sorted_items = sorted(
                self.cache.items(), 
                key=lambda x: x[1]["expires_at"]
            )
            items_to_remove = len(sorted_items) // 4
            for key, _ in sorted_items[:items_to_remove]:
                del self.cache[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if self._is_expired(key):
            if key in self.cache:
                del self.cache[key]
            return None
        return self.cache[key]["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with optional TTL."""
        self._evict_if_needed()
        ttl = ttl or self.default_ttl
        self.cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)


# Global cache instance
cache = SimpleCache()


def cached(ttl: int = 300, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            # Create cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            # Create cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


@asynccontextmanager
async def database_connection_pool():
    """Context manager for database connection pooling."""
    # This would be implemented with actual database connection pooling
    # For now, it's a placeholder for the concept
    logger.info("Acquiring database connection from pool")
    try:
        yield
    finally:
        logger.info("Releasing database connection to pool")


class RateLimiter:
    """Simple rate limiter to prevent abuse."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for given identifier."""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False


# Global rate limiter
rate_limiter = RateLimiter()


def get_performance_summary() -> Dict[str, Any]:
    """Get summary of performance metrics."""
    summary = {}
    for operation, metrics in performance_metrics.items():
        if metrics:
            durations = [m["duration_ms"] for m in metrics]
            summary[operation] = {
                "count": len(metrics),
                "avg_duration_ms": sum(durations) / len(durations),
                "min_duration_ms": min(durations),
                "max_duration_ms": max(durations),
                "last_execution": metrics[-1]["timestamp"]
            }
    return summary


def clear_performance_metrics():
    """Clear all performance metrics."""
    performance_metrics.clear()
