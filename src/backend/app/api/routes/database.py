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
