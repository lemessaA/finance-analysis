"""
Database query optimization utilities and strategies.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union, Tuple
from sqlalchemy import text, Index, Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import logging
import time
from dataclasses import dataclass
from enum import Enum

from app.utils.performance import performance_timer, cached
from app.utils.cache import redis_cache

logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Types of database queries for optimization strategies."""
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    JOIN = "JOIN"
    AGGREGATE = "AGGREGATE"


@dataclass
class QueryMetrics:
    """Metrics for database query performance."""
    query: str
    execution_time: float
    rows_affected: int
    index_used: Optional[str]
    table_scanned: Optional[str]
    timestamp: float


class QueryOptimizer:
    """Advanced database query optimization."""
    
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.query_history: List[QueryMetrics] = []
        self.index_recommendations: Dict[str, List[str]] = {}
    
    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Get database session with connection pooling."""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    @performance_timer("optimized_query")
    async def execute_query(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """Execute optimized database query with caching."""
        
        # Check cache first for SELECT queries
        if use_cache and query.strip().upper().startswith('SELECT'):
            cache_key = f"query:{hash(query + str(params))}"
            cached_result = await self._get_cached_result(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for query: {query[:50]}...")
                return cached_result
        
        # Execute query with performance monitoring
        start_time = time.time()
        
        async with self.get_session() as session:
            try:
                result = await session.execute(text(query), params or {})
                rows = result.fetchall()
                execution_time = time.time() - start_time
                
                # Convert to list of dictionaries
                data = [dict(row._mapping) for row in rows]
                
                # Cache SELECT query results
                if use_cache and query.strip().upper().startswith('SELECT'):
                    await self._cache_result(cache_key, data, ttl=300)  # 5 minutes
                
                # Record metrics
                await self._record_query_metrics(query, execution_time, len(data))
                
                logger.debug(f"Query executed in {execution_time:.3f}s, returned {len(data)} rows")
                return data
                
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                raise
    
    async def _get_cached_result(self, cache_key: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached query result."""
        try:
            from app.utils.cache import cache_manager
            return await cache_manager.get(cache_key)
        except Exception as e:
            logger.debug(f"Cache retrieval failed: {e}")
            return None
    
    async def _cache_result(self, cache_key: str, data: List[Dict[str, Any]], ttl: int):
        """Cache query result."""
        try:
            from app.utils.cache import cache_manager
            await cache_manager.set(cache_key, data, ttl)
        except Exception as e:
            logger.debug(f"Cache storage failed: {e}")
    
    async def _record_query_metrics(self, query: str, execution_time: float, rows_affected: int):
        """Record query performance metrics."""
        metrics = QueryMetrics(
            query=query,
            execution_time=execution_time,
            rows_affected=rows_affected,
            index_used=None,  # Would need EXPLAIN ANALYZE to get this
            table_scanned=None,  # Would need EXPLAIN ANALYZE to get this
            timestamp=time.time()
        )
        
        self.query_history.append(metrics)
        
        # Keep only last 1000 queries
        if len(self.query_history) > 1000:
            self.query_history = self.query_history[-1000:]
        
        # Log slow queries
        if execution_time > 1.0:  # Queries taking more than 1 second
            logger.warning(f"Slow query detected: {execution_time:.3f}s - {query[:100]}...")
    
    @cached(ttl=3600, key_prefix="schema")
    async def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get table schema information for optimization."""
        query = """
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default,
            character_maximum_length
        FROM information_schema.columns 
        WHERE table_name = :table_name
        ORDER BY ordinal_position
        """
        
        async with self.get_session() as session:
            result = await session.execute(text(query), {"table_name": table_name})
            columns = result.fetchall()
            
            return {
                "table_name": table_name,
                "columns": [dict(row._mapping) for row in columns],
                "column_count": len(columns)
            }
    
    async def analyze_query_performance(self, query: str) -> Dict[str, Any]:
        """Analyze query performance using EXPLAIN ANALYZE."""
        explain_query = f"EXPLAIN ANALYZE {query}"
        
        async with self.get_session() as session:
            try:
                result = await session.execute(text(explain_query))
                explain_plan = result.fetchall()
                
                # Parse explain plan for insights
                plan_text = "\n".join([str(row[0]) for row in explain_plan])
                
                return {
                    "query": query,
                    "explain_plan": plan_text,
                    "recommendations": self._generate_recommendations(plan_text)
                }
                
            except Exception as e:
                logger.error(f"Query analysis failed: {e}")
                return {"error": str(e)}
    
    def _generate_recommendations(self, plan_text: str) -> List[str]:
        """Generate optimization recommendations from explain plan."""
        recommendations = []
        
        # Check for sequential scans
        if "Seq Scan" in plan_text:
            recommendations.append("Consider adding indexes for frequently queried columns")
        
        # Check for missing indexes
        if "Bitmap Heap Scan" in plan_text and "Bitmap Index Scan" not in plan_text:
            recommendations.append("Consider creating bitmap indexes for better performance")
        
        # Check for slow operations
        if "Nested Loop" in plan_text and "cost=" in plan_text:
            recommendations.append("Consider optimizing JOIN conditions or adding foreign key indexes")
        
        # Check for sort operations
        if "Sort" in plan_text and "using" not in plan_text.lower():
            recommendations.append("Consider adding indexes to support ORDER BY clauses")
        
        return recommendations
    
    async def get_slow_queries(self, threshold: float = 1.0) -> List[QueryMetrics]:
        """Get list of slow queries above threshold."""
        return [q for q in self.query_history if q.execution_time > threshold]
    
    async def suggest_indexes(self, table_name: str) -> List[str]:
        """Suggest indexes for a table based on query patterns."""
        suggestions = []
        
        # Analyze query history for this table
        table_queries = [
            q for q in self.query_history 
            if table_name.lower() in q.query.lower()
        ]
        
        if not table_queries:
            return suggestions
        
        # Common patterns to suggest indexes for
        where_columns = set()
        join_columns = set()
        order_by_columns = set()
        
        for query_metric in table_queries:
            query = query_metric.query.upper()
            
            # Extract WHERE conditions (simplified)
            if "WHERE" in query:
                where_part = query.split("WHERE")[1].split("ORDER BY")[0].split("GROUP BY")[0]
                # Simple pattern matching for column names
                import re
                columns = re.findall(r'(\w+)\s*=', where_part)
                where_columns.update(columns)
            
            # Extract JOIN conditions
            if "JOIN" in query:
                join_part = query.split("JOIN")[1].split("ON")[1]
                import re
                columns = re.findall(r'(\w+)\s*=', join_part)
                join_columns.update(columns)
            
            # Extract ORDER BY columns
            if "ORDER BY" in query:
                order_part = query.split("ORDER BY")[1].split("LIMIT")[0]
                columns = [col.strip() for col in order_part.split(",")]
                order_by_columns.update([col.split(" ")[0] for col in columns])
        
        # Generate suggestions
        for column in where_columns:
            suggestions.append(f"CREATE INDEX idx_{table_name}_{column} ON {table_name}({column});")
        
        for column in join_columns:
            if column != table_name:  # Skip self-references
                suggestions.append(f"CREATE INDEX idx_{table_name}_{column} ON {table_name}({column});")
        
        for column in order_by_columns:
            suggestions.append(f"CREATE INDEX idx_{table_name}_{column}_order ON {table_name}({column});")
        
        return list(set(suggestions))  # Remove duplicates
    
    @redis_cache(ttl=1800, prefix="query_stats")
    async def get_query_statistics(self) -> Dict[str, Any]:
        """Get comprehensive query statistics."""
        if not self.query_history:
            return {"message": "No query history available"}
        
        execution_times = [q.execution_time for q in self.query_history]
        total_queries = len(self.query_history)
        
        return {
            "total_queries": total_queries,
            "avg_execution_time": sum(execution_times) / total_queries,
            "min_execution_time": min(execution_times),
            "max_execution_time": max(execution_times),
            "slow_queries": len([q for q in self.query_history if q.execution_time > 1.0]),
            "queries_per_minute": total_queries / max(1, (time.time() - self.query_history[0].timestamp) / 60),
            "total_rows_returned": sum(q.rows_affected for q in self.query_history),
        }


class ConnectionPoolManager:
    """Advanced connection pool management."""
    
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.active_connections = 0
        self.max_connections = 20
        self.connection_timeout = 30
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection with timeout and pooling."""
        start_time = time.time()
        
        while self.active_connections >= self.max_connections:
            if time.time() - start_time > self.connection_timeout:
                raise TimeoutError("Database connection timeout")
            await asyncio.sleep(0.1)
        
        self.active_connections += 1
        
        try:
            async with self.session_factory() as session:
                yield session
        finally:
            self.active_connections -= 1
    
    async def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool status."""
        return {
            "active_connections": self.active_connections,
            "max_connections": self.max_connections,
            "available_connections": self.max_connections - self.active_connections,
            "utilization_percent": (self.active_connections / self.max_connections) * 100
        }


# Global query optimizer instance
query_optimizer: Optional[QueryOptimizer] = None
pool_manager: Optional[ConnectionPoolManager] = None


def initialize_optimization(session_factory: sessionmaker):
    """Initialize database optimization components."""
    global query_optimizer, pool_manager
    query_optimizer = QueryOptimizer(session_factory)
    pool_manager = ConnectionPoolManager(session_factory)
    logger.info("Database optimization initialized")


async def get_query_optimizer() -> QueryOptimizer:
    """Get global query optimizer instance."""
    if query_optimizer is None:
        raise RuntimeError("Query optimizer not initialized")
    return query_optimizer


async def get_pool_manager() -> ConnectionPoolManager:
    """Get global connection pool manager."""
    if pool_manager is None:
        raise RuntimeError("Connection pool manager not initialized")
    return pool_manager
