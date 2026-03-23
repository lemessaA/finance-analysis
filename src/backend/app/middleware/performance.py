"""
Performance monitoring middleware for FastAPI.
"""

import time
import asyncio
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
import logging
from app.utils.performance import PerformanceMonitor, performance_timer, get_performance_summary
from app.utils.cache import cache_manager

logger = logging.getLogger(__name__)


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware to monitor and log request performance."""
    
    def __init__(self, app, enable_cache_headers: bool = True):
        super().__init__(app)
        self.enable_cache_headers = enable_cache_headers
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Start timing
        start_time = time.time()
        
        # Get initial memory usage
        initial_memory = PerformanceMonitor.get_memory_usage()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Get final memory usage
        final_memory = PerformanceMonitor.get_memory_usage()
        memory_delta = final_memory["rss_mb"] - initial_memory["rss_mb"]
        
        # Log performance metrics
        PerformanceMonitor.log_performance_metrics(
            operation=f"http_request_{request.method}_{request.url.path}",
            duration=duration,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            memory_delta_mb=memory_delta,
            user_agent=request.headers.get("user-agent"),
            content_length=response.headers.get("content-length")
        )
        
        # Add performance headers
        if self.enable_cache_headers:
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            response.headers["X-Memory-Usage"] = f"{final_memory['rss_mb']:.1f}MB"
            response.headers["X-Memory-Delta"] = f"{memory_delta:+.1f}MB"
        
        # Log slow requests
        if duration > 2.0:  # Log requests taking more than 2 seconds
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {duration:.3f}s (status: {response.status_code})"
            )
        
        return response


class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware to handle HTTP caching."""
    
    def __init__(self, app, cache_ttl: int = 300):
        super().__init__(app)
        self.cache_ttl = cache_ttl
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)
        
        # Generate cache key
        cache_key = f"http_cache:{request.url}:{hash(str(request.query_params))}"
        
        # Try to get from cache
        cached_response = await cache_manager.get(cache_key)
        if cached_response:
            logger.debug(f"Cache hit for {request.url}")
            return Response(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers=cached_response["headers"],
                media_type=cached_response["media_type"]
            )
        
        # Process request
        response = await call_next(request)
        
        # Cache successful responses
        if response.status_code == 200:
            # Read response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            # Create new response with the body
            response_data = {
                "content": response_body,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "media_type": response.media_type
            }
            await cache_manager.set(cache_key, response_data, self.cache_ttl)
            logger.debug(f"Cached response for {request.url}")
            
            # Return new response with the body
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting."""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        from app.utils.performance import rate_limiter
        self.rate_limiter = rate_limiter
        self.requests_per_minute = requests_per_minute
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Get client identifier (IP address or user ID)
        client_id = request.client.host
        user_id = request.headers.get("X-User-ID")
        if user_id:
            client_id = f"user:{user_id}"
        
        # Check rate limit
        if not self.rate_limiter.is_allowed(client_id):
            logger.warning(f"Rate limit exceeded for {client_id}")
            return Response(
                content={"error": "Rate limit exceeded"},
                status_code=429,
                headers={"Retry-After": "60"}
            )
        
        return await call_next(request)


class CompressionMiddleware(BaseHTTPMiddleware):
    """Middleware to compress responses."""
    
    def __init__(self, app, min_size: int = 1024):
        super().__init__(app)
        self.min_size = min_size
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # Check if response should be compressed
        if (
            response.headers.get("content-type", "").startswith("application/json") or
            response.headers.get("content-type", "").startswith("text/")
        ):
            content_length = len(response.body) if response.body else 0
            if content_length > self.min_size:
                # Add compression header (actual compression would be handled by server)
                response.headers["Content-Encoding"] = "gzip"
        
        return response


async def get_performance_stats() -> dict:
    """Get comprehensive performance statistics."""
    return {
        "performance_metrics": get_performance_summary(),
        "cache_stats": await cache_manager.get_stats(),
        "system_stats": {
            "memory": PerformanceMonitor.get_memory_usage(),
            "cpu": PerformanceMonitor.get_cpu_usage()
        }
    }
