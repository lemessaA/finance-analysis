"""
Advanced caching utilities with Redis support for the AI Database Chat Interface.
"""

import json
import pickle
import asyncio
from typing import Any, Optional, Union, Dict, List
import logging
from functools import wraps
import hashlib
import time

try:
    import aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("Redis not available, falling back to memory cache")

from app.utils.performance import SimpleCache, performance_timer

logger = logging.getLogger(__name__)


class CacheManager:
    """Advanced cache manager with Redis fallback to memory cache."""
    
    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url
        self.redis_client = None
        self.memory_cache = SimpleCache(max_size=500, default_ttl=300)
        self.use_redis = False
        
    async def initialize(self):
        """Initialize Redis connection if available."""
        if REDIS_AVAILABLE and self.redis_url:
            try:
                self.redis_client = await aioredis.from_url(self.redis_url)
                # Test connection
                await self.redis_client.ping()
                self.use_redis = True
                logger.info("Redis cache initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Using memory cache.")
                self.use_redis = False
        else:
            logger.info("Using memory cache (Redis not configured)")
    
    def _make_key(self, prefix: str, key_parts: List[str]) -> str:
        """Create a consistent cache key."""
        key_str = ":".join(str(part) for part in key_parts)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if self.use_redis and self.redis_client:
            try:
                data = await self.redis_client.get(key)
                if data:
                    return pickle.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                # Fallback to memory cache
                return self.memory_cache.get(key)
        
        return self.memory_cache.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache."""
        if self.use_redis and self.redis_client:
            try:
                serialized = pickle.dumps(value)
                await self.redis_client.setex(key, ttl, serialized)
                return True
            except Exception as e:
                logger.error(f"Redis set error: {e}")
                # Fallback to memory cache
                self.memory_cache.set(key, value, ttl)
                return False
        
        self.memory_cache.set(key, value, ttl)
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if self.use_redis and self.redis_client:
            try:
                await self.redis_client.delete(key)
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
        
        # Always try to delete from memory cache
        if key in self.memory_cache.cache:
            del self.memory_cache.cache[key]
        return True
    
    async def clear(self, pattern: Optional[str] = None) -> bool:
        """Clear cache entries."""
        if self.use_redis and self.redis_client:
            try:
                if pattern:
                    keys = await self.redis_client.keys(pattern)
                    if keys:
                        await self.redis_client.delete(*keys)
                else:
                    await self.redis_client.flushdb()
            except Exception as e:
                logger.error(f"Redis clear error: {e}")
        
        # Always clear memory cache
        self.memory_cache.clear()
        return True
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            "memory_cache_size": self.memory_cache.size(),
            "using_redis": self.use_redis
        }
        
        if self.use_redis and self.redis_client:
            try:
                info = await self.redis_client.info()
                stats.update({
                    "redis_used_memory": info.get("used_memory_human"),
                    "redis_connected_clients": info.get("connected_clients"),
                    "redis_keyspace_hits": info.get("keyspace_hits", 0),
                    "redis_keyspace_misses": info.get("keyspace_misses", 0),
                })
            except Exception as e:
                logger.error(f"Redis stats error: {e}")
        
        return stats


# Global cache manager instance
cache_manager = CacheManager()


def redis_cache(
    ttl: int = 300, 
    prefix: str = "app", 
    key_parts: Optional[List[str]] = None,
    use_memory_fallback: bool = True
):
    """Decorator for caching function results with Redis."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key_parts = [func.__name__]
            
            if key_parts:
                # Use specified key parts
                for part in key_parts:
                    if isinstance(part, str) and part in kwargs:
                        cache_key_parts.append(str(kwargs[part]))
                    elif callable(part):
                        cache_key_parts.append(str(part(args, kwargs)))
            else:
                # Use all args and kwargs
                cache_key_parts.extend(str(arg) for arg in args)
                cache_key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            
            cache_key = cache_manager._make_key(prefix, cache_key_parts)
            
            # Try to get from cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache the result
            await cache_manager.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator


class QueryCache:
    """Specialized cache for database query results."""
    
    def __init__(self, default_ttl: int = 600):  # 10 minutes default
        self.default_ttl = default_ttl
    
    @redis_cache(ttl=600, prefix="query", key_parts=["query", "params"])
    async def get_query_result(self, query: str, params: Dict[str, Any]) -> Any:
        """Cache database query results."""
        # This would be implemented with actual query execution
        pass
    
    @redis_cache(ttl=3600, prefix="schema", key_parts=["database_name"])
    async def get_database_schema(self, database_name: str) -> Dict[str, Any]:
        """Cache database schema information."""
        # This would be implemented with actual schema retrieval
        pass
    
    @redis_cache(ttl=1800, prefix="table_info", key_parts=["database_name", "table_name"])
    async def get_table_info(self, database_name: str, table_name: str) -> Dict[str, Any]:
        """Cache table information."""
        # This would be implemented with actual table info retrieval
        pass


class ChatCache:
    """Specialized cache for chat-related data."""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self.default_ttl = default_ttl
    
    @redis_cache(ttl=300, prefix="chat_response", key_parts=["session_id", "query_hash"])
    async def get_chat_response(self, session_id: str, query_hash: str) -> Dict[str, Any]:
        """Cache chat responses."""
        pass
    
    @redis_cache(ttl=600, prefix="suggestions", key_parts=["database_schema"])
    async def get_query_suggestions(self, database_schema: str) -> List[str]:
        """Cache query suggestions."""
        pass
    
    @redis_cache(ttl=1800, prefix="visualization", key_parts=["query_hash", "viz_type"])
    async def get_visualization_data(self, query_hash: str, viz_type: str) -> Dict[str, Any]:
        """Cache visualization data."""
        pass


# Global cache instances
query_cache = QueryCache()
chat_cache = ChatCache()


async def initialize_cache():
    """Initialize the cache system."""
    await cache_manager.initialize()


@performance_timer("cache_warmup")
async def warm_up_cache():
    """Warm up cache with frequently accessed data."""
    logger.info("Starting cache warm-up...")
    
    # This would be implemented with actual warm-up logic
    # For example, pre-loading common queries, schemas, etc.
    
    logger.info("Cache warm-up completed")
