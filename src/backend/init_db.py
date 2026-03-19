"""
Initialize database tables and populate with sample data.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.database.models import Base
from app.database.session import engine
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def init_database():
    """Initialize database tables."""
    try:
        logger.info("Creating database tables...")
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully!")
        
        # Test the dashboard API to populate data
        logger.info("Testing dashboard API to populate sample data...")
        
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/v1/dashboard/dashboard")
            if response.status_code == 200:
                logger.info("Dashboard API working and data populated!")
            else:
                logger.error(f"Dashboard API error: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())
