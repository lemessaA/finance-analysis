"""
API routes for performance monitoring and metrics.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import logging

from app.utils.performance import (
    get_performance_summary, 
    PerformanceMonitor,
    clear_performance_metrics
)
from app.utils.cache import cache_manager
from app.database.optimization import get_query_optimizer, get_pool_manager
from app.middleware.performance import get_performance_stats

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/performance/summary")
async def get_performance_overview():
    """Get comprehensive performance overview."""
    try:
        performance_summary = get_performance_summary()
        cache_stats = await cache_manager.get_stats()
        system_stats = {
            "memory": PerformanceMonitor.get_memory_usage(),
            "cpu": PerformanceMonitor.get_cpu_usage()
        }
        
        # Get database stats if available
        db_stats = {}
        try:
            query_optimizer = await get_query_optimizer()
            db_stats = await query_optimizer.get_query_statistics()
            
            pool_manager = await get_pool_manager()
            db_stats["connection_pool"] = await pool_manager.get_pool_status()
        except Exception as e:
            logger.debug(f"Database stats not available: {e}")
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "performance_metrics": performance_summary,
            "cache_statistics": cache_stats,
            "system_resources": system_stats,
            "database_performance": db_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting performance overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance overview")


@router.get("/performance/metrics")
async def get_detailed_metrics(
    operation: Optional[str] = None,
    limit: int = 100
):
    """Get detailed performance metrics for operations."""
    try:
        from app.utils.performance import performance_metrics
        
        if operation:
            # Get metrics for specific operation
            metrics = performance_metrics.get(operation, [])
            return {
                "operation": operation,
                "metrics": metrics[-limit:],  # Return last N metrics
                "total_count": len(metrics)
            }
        else:
            # Get all operations summary
            summary = {}
            for op_name, op_metrics in performance_metrics.items():
                if op_metrics:
                    durations = [m["duration_ms"] for m in op_metrics]
                    summary[op_name] = {
                        "count": len(op_metrics),
                        "avg_duration_ms": sum(durations) / len(durations),
                        "min_duration_ms": min(durations),
                        "max_duration_ms": max(durations),
                        "last_execution": op_metrics[-1]["timestamp"]
                    }
            
            return {
                "operations": summary,
                "total_operations": len(summary)
            }
            
    except Exception as e:
        logger.error(f"Error getting detailed metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get detailed metrics")


@router.get("/performance/health")
async def get_health_check():
    """Get application health status with performance indicators."""
    try:
        memory_usage = PerformanceMonitor.get_memory_usage()
        cpu_usage = PerformanceMonitor.get_cpu_usage()
        
        # Determine health status
        health_status = "healthy"
        issues = []
        
        # Check memory usage
        if memory_usage["percent"] > 80:
            health_status = "degraded"
            issues.append(f"High memory usage: {memory_usage['percent']:.1f}%")
        
        # Check CPU usage
        if cpu_usage > 80:
            health_status = "degraded"
            issues.append(f"High CPU usage: {cpu_usage:.1f}%")
        
        # Check cache performance
        cache_stats = await cache_manager.get_stats()
        if cache_stats.get("memory_cache_size", 0) > 800:  # Near limit
            health_status = "degraded"
            issues.append("Cache memory nearly full")
        
        return {
            "status": health_status,
            "timestamp": datetime.utcnow().isoformat(),
            "system_resources": {
                "memory": memory_usage,
                "cpu": cpu_usage
            },
            "cache_status": cache_stats,
            "issues": issues,
            "uptime": "N/A"  # Would need to track startup time
        }
        
    except Exception as e:
        logger.error(f"Error getting health status: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/performance/slow-queries")
async def get_slow_queries(threshold: float = 1.0, limit: int = 50):
    """Get list of slow database queries."""
    try:
        query_optimizer = await get_query_optimizer()
        slow_queries = await query_optimizer.get_slow_queries(threshold)
        
        # Format for API response
        formatted_queries = []
        for query_metric in slow_queries[-limit:]:
            formatted_queries.append({
                "query": query_metric.query[:200] + "..." if len(query_metric.query) > 200 else query_metric.query,
                "execution_time": query_metric.execution_time,
                "rows_affected": query_metric.rows_affected,
                "timestamp": query_metric.timestamp
            })
        
        return {
            "threshold_seconds": threshold,
            "slow_queries": formatted_queries,
            "total_count": len(slow_queries)
        }
        
    except Exception as e:
        logger.error(f"Error getting slow queries: {e}")
        raise HTTPException(status_code=500, detail="Failed to get slow queries")


@router.get("/performance/cache-analysis")
async def get_cache_analysis():
    """Get detailed cache performance analysis."""
    try:
        cache_stats = await cache_manager.get_stats()
        
        # Analyze cache performance
        analysis = {
            "cache_stats": cache_stats,
            "performance_impact": {},
            "recommendations": []
        }
        
        # Generate recommendations based on cache stats
        if cache_stats.get("memory_cache_size", 0) > 800:
            analysis["recommendations"].append("Consider increasing cache size or reducing TTL")
        
        if cache_stats.get("using_redis", False):
            hit_rate = cache_stats.get("redis_keyspace_hits", 0) / max(1, 
                cache_stats.get("redis_keyspace_hits", 0) + cache_stats.get("redis_keyspace_misses", 0)
            )
            analysis["performance_impact"]["hit_rate"] = hit_rate
            
            if hit_rate < 0.7:
                analysis["recommendations"].append("Cache hit rate is low, consider adjusting cache keys or TTL")
        else:
            analysis["recommendations"].append("Consider using Redis for better cache performance")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze cache")


@router.post("/performance/clear-metrics")
async def clear_metrics():
    """Clear performance metrics and cache."""
    try:
        # Clear performance metrics
        clear_performance_metrics()
        
        # Clear cache
        await cache_manager.clear()
        
        logger.info("Performance metrics and cache cleared")
        
        return {
            "message": "Performance metrics and cache cleared successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error clearing metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear metrics")


@router.get("/performance/trends")
async def get_performance_trends(
    hours: int = 24,
    operation: Optional[str] = None
):
    """Get performance trends over time."""
    try:
        from app.utils.performance import performance_metrics
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        trends = {}
        
        for op_name, op_metrics in performance_metrics.items():
            if operation and op_name != operation:
                continue
            
            # Filter metrics by time
            recent_metrics = [
                m for m in op_metrics 
                if datetime.fromtimestamp(m["timestamp"]) > cutoff_time
            ]
            
            if recent_metrics:
                # Calculate trend data
                timestamps = [datetime.fromtimestamp(m["timestamp"]) for m in recent_metrics]
                durations = [m["duration_ms"] for m in recent_metrics]
                
                trends[op_name] = {
                    "data_points": len(recent_metrics),
                    "avg_duration_ms": sum(durations) / len(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "trend_direction": "stable",  # Would need more complex analysis
                    "timeline": [
                        {
                            "timestamp": ts.isoformat(),
                            "duration_ms": dur
                        }
                        for ts, dur in zip(timestamps, durations)
                    ]
                }
        
        return {
            "time_range_hours": hours,
            "operation_filter": operation,
            "trends": trends
        }
        
    except Exception as e:
        logger.error(f"Error getting performance trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance trends")


@router.get("/performance/alerts")
async def get_performance_alerts():
    """Get performance alerts and warnings."""
    try:
        alerts = []
        
        # Check memory usage
        memory_usage = PerformanceMonitor.get_memory_usage()
        if memory_usage["percent"] > 80:
            alerts.append({
                "type": "warning",
                "message": f"High memory usage: {memory_usage['percent']:.1f}%",
                "timestamp": datetime.utcnow().isoformat(),
                "severity": "high" if memory_usage["percent"] > 90 else "medium"
            })
        
        # Check CPU usage
        cpu_usage = PerformanceMonitor.get_cpu_usage()
        if cpu_usage > 80:
            alerts.append({
                "type": "warning",
                "message": f"High CPU usage: {cpu_usage:.1f}%",
                "timestamp": datetime.utcnow().isoformat(),
                "severity": "high" if cpu_usage > 90 else "medium"
            })
        
        # Check for slow queries
        try:
            query_optimizer = await get_query_optimizer()
            slow_queries = await query_optimizer.get_slow_queries(2.0)  # 2 second threshold
            if len(slow_queries) > 5:
                alerts.append({
                    "type": "performance",
                    "message": f"Multiple slow queries detected: {len(slow_queries)} queries > 2s",
                    "timestamp": datetime.utcnow().isoformat(),
                    "severity": "medium"
                })
        except:
            pass
        
        # Check cache performance
        cache_stats = await cache_manager.get_stats()
        if cache_stats.get("memory_cache_size", 0) > 800:
            alerts.append({
                "type": "cache",
                "message": "Cache memory nearly full",
                "timestamp": datetime.utcnow().isoformat(),
                "severity": "medium"
            })
        
        return {
            "alerts": alerts,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a.get("severity") == "high"])
        }
        
    except Exception as e:
        logger.error(f"Error getting performance alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance alerts")
