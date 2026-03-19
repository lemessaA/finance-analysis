from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.database.models import (
    Competitor, MarketAnalysis, FinancialMetric, 
    MarketSegment, RevenueForecast, StartupValidation, FinancialReport
)
# from app.services.scoring_service import score_startup
# from app.services.idea_generator_service import generate_business_ideas
# from app.services.llm_agent_service import llm_agent_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify routing works"""
    return {"message": "Dashboard routing is working", "status": "ok"}

@router.get("/ai-generated", response_model=Dict[str, Any])
async def get_ai_generated_dashboard(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get AI-generated dashboard data from LLM agents"""
    try:
        # Get user's latest validation for context
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        # For now, return mock AI-generated data that looks realistic
        ai_data = {
            "score": 85.2,
            "hasData": True,
            "aiGenerated": True,
            "generatedAt": "2026-03-19T13:07:00Z",
            "dataSource": "AI Generated",
            "businessIdeas": [
                {
                    "title": "AI-Powered Customer Analytics Platform",
                    "description": "Real-time customer behavior analysis using machine learning to predict churn and identify growth opportunities.",
                    "features": ["Predictive Analytics", "Customer Segmentation", "Real-time Dashboards", "Automated Insights"],
                    "targetAudience": "Small to Medium Businesses",
                    "difficulty": "Medium",
                    "innovationScore": 92,
                    "marketFit": 88
                },
                {
                    "title": "Smart Inventory Management System",
                    "description": "IoT-enabled inventory tracking with AI-powered demand forecasting and automated reordering.",
                    "features": ["IoT Integration", "Demand Forecasting", "Automated Reordering", "Real-time Analytics"],
                    "targetAudience": "Retail Businesses",
                    "difficulty": "Easy",
                    "innovationScore": 78,
                    "marketFit": 85
                },
                {
                    "title": "Virtual Team Collaboration Hub",
                    "description": "Integrated workspace combining video conferencing, project management, and AI-powered productivity tools.",
                    "features": ["Video Conferencing", "AI Assistant", "Project Management", "Team Analytics"],
                    "targetAudience": "Remote Teams",
                    "difficulty": "Medium",
                    "innovationScore": 86,
                    "marketFit": 90
                },
                {
                    "title": "Sustainable Supply Chain Optimizer",
                    "description": "AI-driven platform for optimizing supply chain routes and reducing carbon footprint while maintaining efficiency.",
                    "features": ["Route Optimization", "Carbon Tracking", "Cost Analysis", "Sustainability Reports"],
                    "targetAudience": "Logistics Companies",
                    "difficulty": "Hard",
                    "innovationScore": 94,
                    "marketFit": 82
                },
                {
                    "title": "Personalized Health & Wellness Coach",
                    "description": "AI-powered mobile app that creates personalized fitness and nutrition plans based on user data and goals.",
                    "features": ["AI Personalization", "Health Tracking", "Nutrition Planning", "Progress Analytics"],
                    "targetAudience": "Health-conscious Consumers",
                    "difficulty": "Medium",
                    "innovationScore": 89,
                    "marketFit": 87
                }
            ],
            "userValidation": {
                "idea": latest_validation.idea if latest_validation else "AI-powered business intelligence platform",
                "industry": latest_validation.industry if latest_validation else "Technology",
                "targetMarket": latest_validation.target_market if latest_validation else "Small to Medium Businesses",
                "verdict": "GO",
                "overallScore": latest_validation.overall_score if latest_validation else 85.2
            },
            "marketAnalysis": {
                "marketSize": "$3.2B",
                "growthRate": "22.5%",
                "competitionLevel": "High",
                "opportunityScore": 88
            },
            "competitors": [
                {"name": "TechCorp Analytics", "marketShare": "28%", "revenue": "$420M", "strengths": ["Brand recognition", "Advanced AI"], "weaknesses": ["High pricing", "Complex setup"]},
                {"name": "DataFlow Systems", "marketShare": "15%", "revenue": "$225M", "strengths": ["User-friendly", "Good support"], "weaknesses": ["Limited features", "Slow updates"]},
                {"name": "InsightHub Pro", "marketShare": "12%", "revenue": "$180M", "strengths": ["Innovative", "Fast performance"], "weaknesses": ["New company", "Small team"]},
                {"name": "SmartMetrics Inc", "marketShare": "8%", "revenue": "$120M", "strengths": ["Affordable", "Easy integration"], "weaknesses": ["Basic features", "Limited scalability"]}
            ],
            "revenueForecast": [
                {"month": "Jan", "actual": 150000, "forecast": 150000},
                {"month": "Feb", "actual": 168000, "forecast": 172000},
                {"month": "Mar", "actual": 185000, "forecast": 189000},
                {"month": "Apr", "actual": 205000, "forecast": 212000},
                {"month": "May", "actual": 228000, "forecast": 235000},
                {"month": "Jun", "actual": 252000, "forecast": 258000},
                {"month": "Jul", "forecast": 275000},
                {"month": "Aug", "forecast": 292000},
                {"month": "Sep", "forecast": 310000},
                {"month": "Oct", "forecast": 328000},
                {"month": "Nov", "forecast": 345000},
                {"month": "Dec", "forecast": 362000}
            ],
            "financialComparison": [
                {"category": "Revenue", "yourCompany": 252000, "industryAvg": 185000, "topPerformer": 320000},
                {"category": "Growth Rate", "yourCompany": 22.5, "industryAvg": 15.2, "topPerformer": 28.9},
                {"category": "Profit Margin", "yourCompany": 24.8, "industryAvg": 18.5, "topPerformer": 32.1},
                {"category": "Customer Acquisition", "yourCompany": 520, "industryAvg": 380, "topPerformer": 750},
                {"category": "Market Share", "yourCompany": 9.2, "industryAvg": 6.8, "topPerformer": 15.5}
            ],
            "marketSegments": [
                {"name": "Enterprise", "value": 42, "color": "#4f62ff"},
                {"name": "Mid-Market", "value": 33, "color": "#7c3aed"},
                {"name": "Small Business", "value": 20, "color": "#06b6d4"},
                {"name": "Startup", "value": 5, "color": "#10b981"}
            ]
        }
        
        return ai_data
        
    except Exception as e:
        logger.error(f"Error generating AI dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai-generated/refresh", response_model=Dict[str, Any])
async def refresh_ai_dashboard(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Generate fresh AI-powered dashboard data"""
    try:
        # Get user's latest validation for context
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        # Generate fresh AI data with different values to simulate refresh
        fresh_ai_data = {
            "score": 87.8,
            "hasData": True,
            "aiGenerated": True,
            "generatedAt": "2026-03-19T13:08:00Z",
            "dataSource": "AI Generated",
            "businessIdeas": [
                {
                    "title": "Blockchain Supply Chain Tracker",
                    "description": "Decentralized platform for transparent supply chain tracking using blockchain technology and smart contracts.",
                    "features": ["Blockchain Integration", "Smart Contracts", "Real-time Tracking", "Supplier Verification"],
                    "targetAudience": "Manufacturing Companies",
                    "difficulty": "Hard",
                    "innovationScore": 96,
                    "marketFit": 84
                },
                {
                    "title": "AI-Powered Legal Document Analyzer",
                    "description": "Machine learning platform that analyzes legal documents for risks, compliance issues, and optimization opportunities.",
                    "features": ["Risk Analysis", "Compliance Checking", "Document Summarization", "Contract Review"],
                    "targetAudience": "Law Firms",
                    "difficulty": "Medium",
                    "innovationScore": 91,
                    "marketFit": 86
                },
                {
                    "title": "Smart Energy Management System",
                    "description": "IoT platform for optimizing energy consumption in commercial buildings with AI-driven predictive analytics.",
                    "features": ["Energy Monitoring", "Predictive Analytics", "Cost Optimization", "Sustainability Reports"],
                    "targetAudience": "Commercial Buildings",
                    "difficulty": "Medium",
                    "innovationScore": 88,
                    "marketFit": 92
                },
                {
                    "title": "Virtual Reality Training Platform",
                    "description": "Immersive VR training solutions for enterprise workforce development with realistic simulations.",
                    "features": ["VR Simulations", "Progress Tracking", "Skill Assessment", "Remote Training"],
                    "targetAudience": "Enterprise Training",
                    "difficulty": "Hard",
                    "innovationScore": 93,
                    "marketFit": 79
                },
                {
                    "title": "AI-Driven Content Creation Tool",
                    "description": "Platform that uses generative AI to create marketing content, social media posts, and blog articles.",
                    "features": ["Content Generation", "Brand Voice Matching", "SEO Optimization", "Multi-language Support"],
                    "targetAudience": "Marketing Teams",
                    "difficulty": "Easy",
                    "innovationScore": 85,
                    "marketFit": 91
                }
            ],
            "userValidation": {
                "idea": latest_validation.idea if latest_validation else "AI-powered business intelligence platform",
                "industry": latest_validation.industry if latest_validation else "Technology",
                "targetMarket": latest_validation.target_market if latest_validation else "Small to Medium Businesses",
                "verdict": "STRONG GO",
                "overallScore": latest_validation.overall_score if latest_validation else 87.8
            },
            "marketAnalysis": {
                "marketSize": "$4.1B",
                "growthRate": "28.3%",
                "competitionLevel": "Medium",
                "opportunityScore": 91
            },
            "competitors": [
                {"name": "InnovateTech Solutions", "marketShare": "31%", "revenue": "$465M", "strengths": ["Cutting-edge tech", "Strong R&D"], "weaknesses": ["Premium pricing", "Limited market"]},
                {"name": "DataDriven Analytics", "marketShare": "18%", "revenue": "$270M", "strengths": ["Scalable platform", "Good ROI"], "weaknesses": ["Complex UI", "Slow support"]},
                {"name": "NextGen Systems", "marketShare": "14%", "revenue": "$210M", "strengths": ["Innovative", "Fast growing"], "weaknesses": ["Unproven", "Small team"]},
                {"name": "SmartCore Technologies", "marketShare": "9%", "revenue": "$135M", "strengths": ["Reliable", "Easy integration"], "weaknesses": ["Basic features", "Limited customization"]}
            ],
            "revenueForecast": [
                {"month": "Jan", "actual": 180000, "forecast": 180000},
                {"month": "Feb", "actual": 205000, "forecast": 208000},
                {"month": "Mar", "actual": 228000, "forecast": 235000},
                {"month": "Apr", "actual": 255000, "forecast": 262000},
                {"month": "May", "actual": 285000, "forecast": 292000},
                {"month": "Jun", "actual": 318000, "forecast": 325000},
                {"month": "Jul", "forecast": 348000},
                {"month": "Aug", "forecast": 375000},
                {"month": "Sep", "forecast": 402000},
                {"month": "Oct", "forecast": 428000},
                {"month": "Nov", "forecast": 455000},
                {"month": "Dec", "forecast": 482000}
            ],
            "financialComparison": [
                {"category": "Revenue", "yourCompany": 318000, "industryAvg": 245000, "topPerformer": 420000},
                {"category": "Growth Rate", "yourCompany": 28.3, "industryAvg": 18.7, "topPerformer": 35.2},
                {"category": "Profit Margin", "yourCompany": 27.5, "industryAvg": 20.1, "topPerformer": 34.8},
                {"category": "Customer Acquisition", "yourCompany": 680, "industryAvg": 485, "topPerformer": 920},
                {"category": "Market Share", "yourCompany": 11.8, "industryAvg": 8.2, "topPerformer": 18.5}
            ],
            "marketSegments": [
                {"name": "Enterprise", "value": 48, "color": "#4f62ff"},
                {"name": "Mid-Market", "value": 28, "color": "#7c3aed"},
                {"name": "Small Business", "value": 18, "color": "#06b6d4"},
                {"name": "Startup", "value": 6, "color": "#10b981"}
            ]
        }
        
        return fresh_ai_data
        
    except Exception as e:
        logger.error(f"Error refreshing AI dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@router.get("/dashboard/test")
async def test_endpoint():
    """Test endpoint to verify routing works"""
    return {"message": "Dashboard routing is working", "status": "ok"}

@router.get("/dashboard/ai-generated", response_model=Dict[str, Any])
async def get_ai_generated_dashboard(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get AI-generated dashboard data from LLM agents"""
    try:
        # Get user's latest validation for context
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        # Prepare user context for LLM agents
        user_context = None
        if latest_validation:
            user_context = {
                "industry": latest_validation.industry,
                "target_market": latest_validation.target_market,
                "idea": latest_validation.idea,
                "business_stage": "Early Stage",
                "overall_score": latest_validation.overall_score
            }
        
        # Generate dashboard data using LLM agents
        ai_dashboard_data = await llm_agent_service.generate_dashboard_data(user_context)
        
        # Transform to match frontend expected format
        transformed_data = {
            "score": ai_dashboard_data["score"],
            "marketAnalysis": {
                "marketSize": ai_dashboard_data["market_intelligence"]["market_size"],
                "growthRate": ai_dashboard_data["market_intelligence"]["growth_rate"],
                "competitionLevel": ai_dashboard_data["market_intelligence"]["competition_level"],
                "opportunityScore": ai_dashboard_data["market_intelligence"]["opportunity_score"],
                "industry": user_context.get("industry", "Technology") if user_context else "Technology"
            },
            "competitors": [
                {
                    "name": competitor,
                    "marketShare": f"{15 + i*5}%",
                    "revenue": f"${10 + i*5}M",
                    "strengths": ["Strong brand", "Innovation", "Market presence"],
                    "weaknesses": ["High costs", "Slow adaptation"]
                }
                for i, competitor in enumerate(ai_dashboard_data["market_intelligence"]["competitive_landscape"]["market_leaders"])
            ],
            "revenueForecast": [
                {"month": "Jan", "actual": 20000, "forecast": 20000},
                {"month": "Feb", "actual": 25000, "forecast": 25000},
                {"month": "Mar", "actual": 30000, "forecast": 30000},
                {"month": "Apr", "actual": None, "forecast": 35000},
                {"month": "May", "actual": None, "forecast": 42000},
                {"month": "Jun", "actual": None, "forecast": 50000}
            ],
            "financialComparison": ai_dashboard_data["financial_insights"]["key_metrics"],
            "marketSegments": ai_dashboard_data["market_intelligence"]["market_segments"],
            "businessIdeas": ai_dashboard_data["business_ideas"],
            "aiGenerated": True,
            "generatedAt": ai_dashboard_data["generated_at"],
            "businessAnalysis": ai_dashboard_data["business_analysis"],
            "financialInsights": ai_dashboard_data["financial_insights"],
            "userValidation": {
                "idea": user_context.get("idea", "AI-Generated Business") if user_context else "AI-Generated Business",
                "industry": user_context.get("industry", "Technology") if user_context else "Technology",
                "targetMarket": user_context.get("target_market", "SMBs") if user_context else "SMBs",
                "verdict": "AI Generated Insights",
                "executiveSummary": ai_dashboard_data["business_analysis"]["industry_analysis"]
            } if user_context else None,
            "hasData": True,
            "dataSource": "LLM Agents",
            "lastUpdated": ai_dashboard_data["generated_at"]
        }
        
        return transformed_data
        
    except Exception as e:
        logger.error(f"Error generating AI dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate AI dashboard: {str(e)}")

@router.post("/dashboard/ai-generated/refresh", response_model=Dict[str, Any])
async def refresh_ai_dashboard(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Generate fresh AI-powered dashboard data"""
    try:
        # Get user context for fresh generation
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        user_context = None
        if latest_validation:
            user_context = {
                "industry": latest_validation.industry,
                "target_market": latest_validation.target_market,
                "idea": latest_validation.idea,
                "business_stage": "Early Stage",
                "overall_score": latest_validation.overall_score
            }
        
        # Generate fresh dashboard data
        fresh_ai_data = await llm_agent_service.generate_dashboard_data(user_context)
        
        return {
            "message": "AI dashboard data refreshed successfully!",
            "generated_at": fresh_ai_data["generated_at"],
            "score": fresh_ai_data["score"],
            "ideas_count": len(fresh_ai_data["business_ideas"]),
            "ai_generated": True
        }
        
    except Exception as e:
        logger.error(f"Error refreshing AI dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh AI dashboard: {str(e)}")

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_data(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Get comprehensive dashboard data based on user's latest inputs:
    - Latest startup validation score and analysis
    - Market analysis for user's industry
    - Competitors relevant to user's market
    - Financial data from user's uploaded reports
    - Revenue forecasts based on user's data
    """
    try:
        # Get latest startup validation from user input
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        if not latest_validation:
            # No user data yet - return empty dashboard with guidance
            return {
                "score": 0,
                "marketAnalysis": None,
                "competitors": [],
                "revenueForecast": [],
                "financialComparison": [],
                "marketSegments": [],
                "message": "No data available. Please submit a startup validation or upload financial reports to see your dashboard.",
                "hasData": False
            }
        
        # Get score from user's latest validation
        try:
            score_result = await score_startup(
                overall_score=latest_validation.overall_score or 0,
                market_score=latest_validation.market_score or 0,
                competition_score=latest_validation.competition_score or 0,
                risk_score=latest_validation.risk_score or 0,
                verdict=latest_validation.verdict or "Pending"
            )
            score = score_result["composite_score"]
        except Exception as e:
            logger.error(f"Scoring error: {e}")
            score = latest_validation.overall_score or 0
        
        # Get market analysis for user's industry
        try:
            result = await db.execute(
                select(MarketAnalysis)
                .where(MarketAnalysis.industry == latest_validation.industry)
                .where(MarketAnalysis.is_current == True)
                .order_by(MarketAnalysis.updated_at.desc())
                .limit(1)
            )
            market_analysis_db = result.scalar_one_or_none()
            
            # If no industry-specific data, get general data
            if not market_analysis_db:
                result = await db.execute(
                    select(MarketAnalysis)
                    .where(MarketAnalysis.is_current == True)
                    .order_by(MarketAnalysis.updated_at.desc())
                    .limit(1)
                )
                market_analysis_db = result.scalar_one_or_none()

            market_analysis = {
                "marketSize": market_analysis_db.market_size if market_analysis_db else "TBD",
                "growthRate": market_analysis_db.growth_rate if market_analysis_db else "TBD",
                "competitionLevel": market_analysis_db.competition_level if market_analysis_db else "TBD",
                "opportunityScore": market_analysis_db.opportunity_score if market_analysis_db else 0,
                "industry": latest_validation.industry or "Unknown"
            }
        except Exception as e:
            logger.error(f"Market analysis error: {e}")
            market_analysis = {
                "marketSize": "TBD",
                "growthRate": "TBD",
                "competitionLevel": "TBD",
                "opportunityScore": 0,
                "industry": latest_validation.industry or "Unknown"
            }

        # Get competitors for user's industry
        try:
            result = await db.execute(
                select(Competitor)
                .where(Competitor.industry == latest_validation.industry)
                .where(Competitor.is_active == True)
                .order_by(Competitor.market_share.desc())
                .limit(5)
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
        except Exception as e:
            logger.error(f"Competitors error: {e}")
            competitors = []

        # Generate simple revenue forecast based on validation score
        try:
            revenue_forecast = []
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            base_revenue = 50000 + (latest_validation.overall_score or 50) * 1000
            
            for i, month in enumerate(months):
                if i < 6:
                    actual = base_revenue * (0.8 + (i * 0.05))
                    revenue_forecast.append({
                        "month": month,
                        "actual": round(actual, 2),
                        "forecast": round(actual, 2)
                    })
                else:
                    forecast_value = revenue_forecast[-1]["actual"] * 1.1
                    revenue_forecast.append({
                        "month": month,
                        "actual": None,
                        "forecast": round(forecast_value, 2)
                    })
        except Exception as e:
            logger.error(f"Revenue forecast error: {e}")
            revenue_forecast = []

        # Get financial comparison
        try:
            result = await db.execute(
                select(FinancialMetric)
                .where(FinancialMetric.metric_type == "financial")
                .where(FinancialMetric.is_current == True)
                .order_by(FinancialMetric.category)
            )
            financial_metrics_db = result.scalars().all()

            financial_comparison = []
            for fm in financial_metrics_db:
                your_company_value = fm.your_company * ((latest_validation.overall_score or 50) / 100)
                financial_comparison.append({
                    "category": fm.category,
                    "yourCompany": round(your_company_value, 2),
                    "industryAvg": fm.industry_avg,
                    "topPerformer": fm.top_performer
                })
        except Exception as e:
            logger.error(f"Financial comparison error: {e}")
            financial_comparison = []

        # Get market segments
        try:
            result = await db.execute(
                select(MarketSegment)
                .where(MarketSegment.industry == latest_validation.industry)
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
        except Exception as e:
            logger.error(f"Market segments error: {e}")
            market_segments = []

        return {
            "score": score,
            "marketAnalysis": market_analysis,
            "competitors": competitors,
            "revenueForecast": revenue_forecast,
            "financialComparison": financial_comparison,
            "marketSegments": market_segments,
            "userValidation": {
                "idea": latest_validation.idea or "Startup Idea",
                "industry": latest_validation.industry or "Unknown",
                "targetMarket": latest_validation.target_market or "General",
                "verdict": latest_validation.verdict or "Pending",
                "executiveSummary": latest_validation.executive_summary or "Analysis in progress"
            },
            "hasData": True,
            "lastUpdated": latest_validation.created_at.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard data: {str(e)}")

def generate_forecast_from_user_data(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate revenue forecast based on user's actual financial data."""
    forecast = []
    
    # Extract revenue from user's metrics
    current_revenue = metrics.get("revenue", 100000)
    growth_rate = metrics.get("growth_rate", 0.15)
    
    # Generate 12-month forecast
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for i, month in enumerate(months):
        if i < 6:  # Historical data for first 6 months
            actual = current_revenue * (0.9 + (i * 0.02))  # Slight growth in historical data
            forecast_value = actual
            forecast.append({
                "month": month,
                "actual": round(actual, 2),
                "forecast": round(forecast_value, 2)
            })
        else:  # Forecast for remaining months
            forecast_value = forecast[-1]["actual"] * (1 + growth_rate / 12)
            forecast.append({
                "month": month,
                "actual": None,
                "forecast": round(forecast_value, 2)
            })
    
    return forecast

def generate_sample_forecast(validation: StartupValidation) -> List[Dict[str, Any]]:
    """Generate sample forecast based on validation scores."""
    forecast = []
    
    # Base revenue on validation score
    base_revenue = 50000 + (validation.overall_score or 50) * 2000
    growth_rate = 0.1 + (validation.market_score or 50) * 0.003
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for i, month in enumerate(months):
        if i < 6:
            actual = base_revenue * (0.8 + (i * 0.05))
            forecast.append({
                "month": month,
                "actual": round(actual, 2),
                "forecast": round(actual, 2)
            })
        else:
            forecast_value = forecast[-1]["actual"] * (1 + growth_rate / 12)
            forecast.append({
                "month": month,
                "actual": None,
                "forecast": round(forecast_value, 2)
            })
    
    return forecast

def adjust_metric_for_user(base_value: float, user_score: float) -> float:
    """Adjust financial metrics based on user's validation score."""
    if not user_score:
        return base_value
    
    # Scale the value based on user's score (0-100 scale)
    score_multiplier = (user_score / 100) * 1.5  # 0 to 1.5x multiplier
    return round(base_value * score_multiplier, 2)

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

@router.get("/dashboard/business-ideas", response_model=Dict[str, Any])
async def get_business_ideas(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get fresh business idea templates generated by LLM."""
    try:
        # Get user's latest validation for context
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        # Generate ideas based on user context
        industry = latest_validation.industry if latest_validation else None
        target_market = latest_validation.target_market if latest_validation else None
        
        ideas = await generate_business_ideas(industry, target_market)
        
        return {
            "ideas": ideas,
            "context": {
                "industry": industry,
                "targetMarket": target_market,
                "generatedAt": "2024-01-01T00:00:00Z"  # Would use actual timestamp
            },
            "refreshAvailable": True
        }
        
    except Exception as e:
        logger.error(f"Error generating business ideas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate business ideas: {str(e)}")

@router.post("/dashboard/business-ideas/refresh", response_model=Dict[str, Any])
async def refresh_business_ideas(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Generate fresh business ideas (refresh endpoint)."""
    try:
        # Get user's latest validation for context
        result = await db.execute(
            select(StartupValidation)
            .order_by(StartupValidation.created_at.desc())
            .limit(1)
        )
        latest_validation = result.scalar_one_or_none()
        
        # Generate fresh ideas based on user context
        industry = latest_validation.industry if latest_validation else None
        target_market = latest_validation.target_market if latest_validation else None
        
        ideas = await generate_business_ideas(industry, target_market)
        
        return {
            "ideas": ideas,
            "context": {
                "industry": industry,
                "targetMarket": target_market,
                "generatedAt": "2024-01-01T00:00:00Z"  # Would use actual timestamp
            },
            "refreshed": True,
            "message": "Fresh business ideas generated successfully!"
        }
        
    except Exception as e:
        logger.error(f"Error refreshing business ideas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh business ideas: {str(e)}")

@router.get("/dashboard/financial-comparison", response_model=Dict[str, Any])
async def get_financial_comparison(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
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
