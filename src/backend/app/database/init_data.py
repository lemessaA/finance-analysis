"""
Database initialization script for dashboard data.
Run this script to populate the database with real data.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import AsyncSessionLocal, engine
from app.database.models import (
    Competitor, MarketAnalysis, FinancialMetric, 
    MarketSegment, RevenueForecast, Base
)
from app.services.scoring_service import score_startup
import logging

logger = logging.getLogger(__name__)

async def init_database():
    """Initialize database tables and populate with sample data."""
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        try:
            # Add market analysis data
            market_analysis = MarketAnalysis(
                industry="Technology",
                market_size="$2.4B",
                growth_rate="18.5%",
                competition_level="Medium",
                opportunity_score=82,
                total_addressable_market="$8.2B",
                serviceable_addressable_market="$3.1B",
                market_trends=["Digital transformation", "AI adoption", "Remote work"]
            )
            session.add(market_analysis)

            # Add competitors
            competitors = [
                Competitor(
                    name="TechCorp Inc.",
                    market_share="32%",
                    revenue="$450M",
                    strengths=["Brand recognition", "Large customer base"],
                    weaknesses=["Slow innovation", "High pricing"],
                    description="Leading enterprise software company with established market presence",
                    industry="Technology"
                ),
                Competitor(
                    name="StartupX",
                    market_share="18%",
                    revenue="$180M",
                    strengths=["Agile", "Lower pricing"],
                    weaknesses=["Limited scale", "Newer brand"],
                    description="Fast-growing startup focusing on SMB market",
                    industry="Technology"
                ),
                Competitor(
                    name="DataFlow",
                    market_share="15%",
                    revenue="$150M",
                    strengths=["Tech leadership", "Strong R&D"],
                    weaknesses=["Small team", "Funding concerns"],
                    description="Technology-focused company with innovative solutions",
                    industry="Technology"
                ),
                Competitor(
                    name="CloudBase",
                    market_share="12%",
                    revenue="$120M",
                    strengths=["Enterprise focus", "Stable revenue"],
                    weaknesses=["Legacy tech", "Slow growth"],
                    description="Traditional enterprise software provider",
                    industry="Technology"
                )
            ]
            for competitor in competitors:
                session.add(competitor)

            # Add financial metrics
            financial_metrics = [
                FinancialMetric(
                    category="Revenue",
                    your_company=189000,
                    industry_avg=165000,
                    top_performer=245000,
                    percentile=75,
                    metric_type="financial"
                ),
                FinancialMetric(
                    category="Growth Rate",
                    your_company=18.5,
                    industry_avg=12.3,
                    top_performer=25.8,
                    percentile=80,
                    metric_type="growth"
                ),
                FinancialMetric(
                    category="Profit Margin",
                    your_company=22.4,
                    industry_avg=18.7,
                    top_performer=28.9,
                    percentile=70,
                    metric_type="financial"
                ),
                FinancialMetric(
                    category="Customer Acquisition",
                    your_company=450,
                    industry_avg=320,
                    top_performer=680,
                    percentile=65,
                    metric_type="operational"
                ),
                FinancialMetric(
                    category="Market Share",
                    your_company=8.5,
                    industry_avg=6.2,
                    top_performer=15.3,
                    percentile=72,
                    metric_type="growth"
                )
            ]
            for metric in financial_metrics:
                session.add(metric)

            # Add market segments
            market_segments = [
                MarketSegment(
                    name="Enterprise",
                    value=45,
                    color="#4f62ff",
                    industry="Technology"
                ),
                MarketSegment(
                    name="Mid-Market",
                    value=30,
                    color="#7c3aed",
                    industry="Technology"
                ),
                MarketSegment(
                    name="Small Business",
                    value=20,
                    color="#06b6d4",
                    industry="Technology"
                ),
                MarketSegment(
                    name="Startup",
                    value=5,
                    color="#10b981",
                    industry="Technology"
                )
            ]
            for segment in market_segments:
                session.add(segment)

            # Add revenue forecast data
            revenue_forecasts = [
                RevenueForecast(month="Jan", actual=120000, forecast=120000, is_forecast=False),
                RevenueForecast(month="Feb", actual=135000, forecast=138000, is_forecast=False),
                RevenueForecast(month="Mar", actual=142000, forecast=145000, is_forecast=False),
                RevenueForecast(month="Apr", actual=158000, forecast=162000, is_forecast=False),
                RevenueForecast(month="May", actual=175000, forecast=178000, is_forecast=False),
                RevenueForecast(month="Jun", actual=189000, forecast=195000, is_forecast=False),
                RevenueForecast(month="Jul", forecast=208000, is_forecast=True, forecast_model="Linear Regression"),
                RevenueForecast(month="Aug", forecast=222000, is_forecast=True, forecast_model="Linear Regression"),
                RevenueForecast(month="Sep", forecast=238000, is_forecast=True, forecast_model="Linear Regression"),
                RevenueForecast(month="Oct", forecast=255000, is_forecast=True, forecast_model="Linear Regression"),
                RevenueForecast(month="Nov", forecast=273000, is_forecast=True, forecast_model="Linear Regression"),
                RevenueForecast(month="Dec", forecast=292000, is_forecast=True, forecast_model="Linear Regression")
            ]
            for forecast in revenue_forecasts:
                session.add(forecast)

            await session.commit()
            logger.info("Database initialized with real dashboard data")
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Error initializing database: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(init_database())
