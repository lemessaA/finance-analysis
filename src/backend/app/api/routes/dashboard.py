from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.database.models import (
    Competitor, MarketAnalysis, FinancialMetric, 
    MarketSegment, RevenueForecast, StartupValidation
)
from app.services.scoring_service import score_startup
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

async def ensure_database_populated(db: AsyncSession):
    """Ensure database has data, populate with sample data if empty."""
    
    # Check if we have any data
    result = await db.execute(select(Competitor).limit(1))
    competitors_count = result.scalar_one_or_none()
    
    if not competitors_count:
        logger.info("Database is empty, populating with sample data...")
        
        # Add market analysis
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
        db.add(market_analysis)

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
            db.add(competitor)

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
            db.add(metric)

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
            db.add(segment)

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
            db.add(forecast)

        await db.commit()
        logger.info("Database populated with sample data")

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_data(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Get comprehensive dashboard data including:
    - Startup validation score
    - Market analysis summary
    - Competitor list
    - Revenue forecast data
    - Financial comparison data
    """
    try:
        # Ensure database has data
        await ensure_database_populated(db)
        
        # Get latest startup validation score
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        if latest_validation:
            score_result = await score_startup(
                overall_score=latest_validation.overall_score or 75.0,
                market_score=82.0,
                competition_score=68.0,
                risk_score=71.0,
                verdict=latest_validation.verdict or "Go"
            )
            score = score_result["composite_score"]
        else:
            # Fallback if no validation data exists
            score_result = await score_startup(
                overall_score=75.0,
                market_score=82.0,
                competition_score=68.0,
                risk_score=71.0,
                verdict="Go"
            )
            score = score_result["composite_score"]

        # Get market analysis data
        result = await db.execute(
            select(MarketAnalysis)
            .where(MarketAnalysis.is_current == True)
            .order_by(MarketAnalysis.updated_at.desc())
            .limit(1)
        )
        market_analysis_db = result.scalar_one_or_none()

        market_analysis = {
            "marketSize": market_analysis_db.market_size if market_analysis_db else "$2.4B",
            "growthRate": market_analysis_db.growth_rate if market_analysis_db else "18.5%",
            "competitionLevel": market_analysis_db.competition_level if market_analysis_db else "Medium",
            "opportunityScore": market_analysis_db.opportunity_score if market_analysis_db else 82
        }

        # Get competitors data
        result = await db.execute(
            select(Competitor)
            .where(Competitor.is_active == True)
            .order_by(Competitor.market_share.desc())
        )
        competitors_db = result.scalars().all()

        competitors = []
        for comp in competitors_db:
            competitors.append({
                "name": comp.name,
                "marketShare": comp.market_share,
                "revenue": comp.revenue,
                "strengths": comp.strengths or [],
                "weaknesses": comp.weaknesses or []
            })

        # Get revenue forecast data
        result = await db.execute(
            select(RevenueForecast)
            .order_by(RevenueForecast.month)
        )
        revenue_forecasts_db = result.scalars().all()

        revenue_forecast = []
        for rf in revenue_forecasts_db:
            revenue_forecast.append({
                "month": rf.month,
                "actual": rf.actual,
                "forecast": rf.forecast
            })

        # Get financial comparison data
        result = await db.execute(
            select(FinancialMetric)
            .where(FinancialMetric.is_current == True)
            .order_by(FinancialMetric.category)
        )
        financial_metrics_db = result.scalars().all()

        financial_comparison = []
        for fm in financial_metrics_db:
            financial_comparison.append({
                "category": fm.category,
                "yourCompany": fm.your_company,
                "industryAvg": fm.industry_avg,
                "topPerformer": fm.top_performer
            })

        # Get market segments data
        result = await db.execute(
            select(MarketSegment)
            .where(MarketSegment.is_current == True)
            .order_by(MarketSegment.value.desc())
        )
        market_segments_db = result.scalars().all()

        market_segments = []
        for ms in market_segments_db:
            market_segments.append({
                "name": ms.name,
                "value": ms.value,
                "color": ms.color
            })

        return {
            "score": score,
            "marketAnalysis": market_analysis,
            "competitors": competitors,
            "revenueForecast": revenue_forecast,
            "financialComparison": financial_comparison,
            "marketSegments": market_segments
        }
        
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard data: {str(e)}")

@router.get("/dashboard/score", response_model=Dict[str, Any])
async def get_startup_score(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get just the startup validation score"""
    try:
        await ensure_database_populated(db)
        
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        if latest_validation:
            score_result = await score_startup(
                overall_score=latest_validation.overall_score or 75.0,
                market_score=82.0,
                competition_score=68.0,
                risk_score=71.0,
                verdict=latest_validation.verdict or "Go"
            )
        else:
            score_result = await score_startup(
                overall_score=75.0,
                market_score=82.0,
                competition_score=68.0,
                risk_score=71.0,
                verdict="Go"
            )
        
        return {
            "score": score_result["composite_score"],
            "breakdown": score_result["breakdown"],
            "recommendation": score_result["verdict"]
        }
    except Exception as e:
        logger.error(f"Error fetching startup score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch startup score: {str(e)}")

@router.get("/dashboard/market-analysis", response_model=Dict[str, Any])
async def get_market_analysis(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get market analysis summary"""
    try:
        await ensure_database_populated(db)
        
        result = await db.execute(
            select(MarketAnalysis)
            .where(MarketAnalysis.is_current == True)
            .order_by(MarketAnalysis.updated_at.desc())
            .limit(1)
        )
        market_analysis_db = result.scalar_one_or_none()

        if market_analysis_db:
            return {
                "marketSize": market_analysis_db.market_size,
                "growthRate": market_analysis_db.growth_rate,
                "competitionLevel": market_analysis_db.competition_level,
                "opportunityScore": market_analysis_db.opportunity_score,
                "details": {
                    "total_addressable_market": market_analysis_db.total_addressable_market,
                    "serviceable_addressable_market": market_analysis_db.serviceable_addressable_market,
                    "market_trends": market_analysis_db.market_trends or []
                }
            }
        else:
            # Fallback data
            return {
                "marketSize": "$2.4B",
                "growthRate": "18.5%",
                "competitionLevel": "Medium",
                "opportunityScore": 82,
                "details": {
                    "total_addressable_market": "$8.2B",
                    "serviceable_addressable_market": "$3.1B",
                    "market_trends": ["Digital transformation", "AI adoption", "Remote work"]
                }
            }
    except Exception as e:
        logger.error(f"Error fetching market analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch market analysis: {str(e)}")

@router.get("/dashboard/competitors", response_model=List[Dict[str, Any]])
async def get_competitors(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get competitor analysis"""
    try:
        await ensure_database_populated(db)
        
        result = await db.execute(
            select(Competitor)
            .where(Competitor.is_active == True)
            .order_by(Competitor.market_share.desc())
        )
        competitors_db = result.scalars().all()

        competitors = []
        for comp in competitors_db:
            competitors.append({
                "name": comp.name,
                "marketShare": comp.market_share,
                "revenue": comp.revenue,
                "strengths": comp.strengths or [],
                "weaknesses": comp.weaknesses or [],
                "description": comp.description or ""
            })
        return competitors
    except Exception as e:
        logger.error(f"Error fetching competitors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch competitors: {str(e)}")

@router.get("/dashboard/revenue-forecast", response_model=Dict[str, Any])
async def get_revenue_forecast(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get revenue forecast data"""
    try:
        await ensure_database_populated(db)
        
        result = await db.execute(
            select(RevenueForecast)
            .order_by(RevenueForecast.month)
        )
        revenue_forecasts_db = result.scalars().all()

        forecast = []
        model_used = None
        confidence = 0.87
        next_month_forecast = 0

        for rf in revenue_forecasts_db:
            forecast.append({
                "month": rf.month,
                "actual": rf.actual,
                "forecast": rf.forecast
            })
            if rf.is_forecast and not model_used:
                model_used = rf.forecast_model
                next_month_forecast = rf.forecast

        return {
            "forecast": forecast,
            "model_used": model_used or "Linear Regression",
            "confidence": confidence,
            "next_month_forecast": next_month_forecast
        }
    except Exception as e:
        logger.error(f"Error fetching revenue forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch revenue forecast: {str(e)}")

@router.get("/dashboard/financial-comparison", response_model=Dict[str, Any])
async def get_financial_comparison(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get financial comparison data"""
    try:
        await ensure_database_populated(db)
        
        result = await db.execute(
            select(FinancialMetric)
            .where(FinancialMetric.is_current == True)
            .order_by(FinancialMetric.category)
        )
        financial_metrics_db = result.scalars().all()

        metrics = []
        for fm in financial_metrics_db:
            metrics.append({
                "category": fm.category,
                "yourCompany": fm.your_company,
                "industryAvg": fm.industry_avg,
                "topPerformer": fm.top_performer,
                "percentile": fm.percentile
            })

        return {
            "metrics": metrics,
            "overall_ranking": "Good",
            "key_insights": [
                "Revenue growth above industry average",
                "Strong profit margins indicate good operational efficiency",
                "Customer acquisition cost is competitive",
                "Market share position shows room for growth"
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching financial comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch financial comparison: {str(e)}")
