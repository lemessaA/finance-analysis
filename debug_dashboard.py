"""
Debug script to identify the null error in dashboard
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append('/home/lemessa-ahmed/Startup-to-Business/src/backend')

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import AsyncSessionLocal, engine
from app.database.models import StartupValidation

async def debug_dashboard():
    """Debug the dashboard data fetching"""
    try:
        print("🔍 Debugging dashboard data...")
        
        async with AsyncSessionLocal() as db:
            # Get latest startup validation
            result = await db.execute(
                select(StartupValidation)
                .order_by(StartupValidation.created_at.desc())
                .limit(1)
            )
            latest_validation = result.scalar_one_or_none()
            
            if latest_validation:
                print(f"✅ Found validation: {latest_validation.idea}")
                print(f"   Industry: {latest_validation.industry}")
                print(f"   Overall Score: {latest_validation.overall_score}")
                print(f"   Market Score: {latest_validation.market_score}")
                print(f"   Competition Score: {latest_validation.competition_score}")
                print(f"   Risk Score: {latest_validation.risk_score}")
                print(f"   Verdict: {latest_validation.verdict}")
                
                # Test scoring service
                from app.services.scoring_service import score_startup
                score_result = await score_startup(
                    overall_score=latest_validation.overall_score or 0,
                    market_score=latest_validation.market_score or 0,
                    competition_score=latest_validation.competition_score or 0,
                    risk_score=latest_validation.risk_score or 0,
                    verdict=latest_validation.verdict or "Pending"
                )
                print(f"✅ Score result: {score_result}")
                
            else:
                print("❌ No validation found")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_dashboard())
