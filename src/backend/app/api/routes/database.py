"""
Database initialization endpoint for creating tables and populating data.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database.session import get_db, engine
from app.database.models import Base
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/init-database")
async def init_database(db: AsyncSession = Depends(get_db)):
    """Initialize database tables and populate with sample data."""
    try:
        logger.info("Creating database tables...")
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully!")
        
        # Test by checking if tables exist
        result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        
        logger.info(f"Created tables: {tables}")
        
        return {
            "message": "Database initialized successfully",
            "tables_created": tables,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")

@router.get("/database-status")
async def get_database_status(db: AsyncSession = Depends(get_db)):
    """Check database status and list tables."""
    try:
        result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        
        return {
            "status": "connected",
            "tables": tables,
            "table_count": len(tables)
        }
        
    except Exception as e:
        logger.error(f"Database status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database status check failed: {str(e)}")

@router.get("/stats")
async def get_platform_stats(db: AsyncSession = Depends(get_db)):
    """Get platform statistics for dashboard."""
    try:
        # For now, return mock stats that will be updated when real data is available
        # In a real implementation, these would be calculated from actual database tables
        
        # Check if we have any tables to determine if we should return real or mock data
        result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        
        # Mock stats for demonstration - replace with real queries when tables are populated
        stats = {
            "total_analyses": 24,
            "success_rate": 87,
            "api_calls": 1284,
            "avg_score": 72.5,
            "recent_activity": [
                {
                    "type": "startup",
                    "title": "AI Meal Planning App",
                    "score": 85,
                    "time": "2 hours ago",
                    "status": "success"
                },
                {
                    "type": "market",
                    "title": "SaaS Market Analysis",
                    "score": None,
                    "time": "4 hours ago",
                    "status": "completed"
                },
                {
                    "type": "forecasting",
                    "title": "Revenue Forecast Q1",
                    "score": 92,
                    "time": "1 day ago",
                    "status": "success"
                },
                {
                    "type": "startup",
                    "title": "HealthTech Platform",
                    "score": 78,
                    "time": "2 days ago",
                    "status": "success"
                },
                {
                    "type": "analyzer",
                    "title": "Q4 Financial Report Analysis",
                    "score": 88,
                    "time": "3 days ago",
                    "status": "success"
                }
            ],
            "breakdown": {
                "startup_validations": 8,
                "market_intelligence": 6,
                "financial_forecasts": 5,
                "financial_analyses": 5
            }
        }
        
        return {
            "status": "success",
            "data": stats,
            "last_updated": "2024-03-21T15:30:00Z"
        }
        
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")
