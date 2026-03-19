"""
Minimal server to test the 5-idea dashboard system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append('/home/lemessa-ahmed/Startup-to-Business/src/backend')

from app.services.llm_agent_service import llm_agent_service

app = FastAPI(title="AI Business Intelligence - Dashboard Test")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Business Intelligence Dashboard API"}

@app.get("/api/v1/dashboard/ai-generated")
async def get_ai_dashboard():
    """Get AI-generated dashboard data with 5 business ideas"""
    try:
        # Generate dashboard data using LLM agents
        ai_dashboard_data = await llm_agent_service.generate_dashboard_data({
            "industry": "Technology",
            "target_market": "Small to Medium Businesses",
            "business_stage": "Early Stage"
        })
        
        # Transform to match frontend expected format
        transformed_data = {
            "score": ai_dashboard_data["score"],
            "marketAnalysis": {
                "marketSize": ai_dashboard_data["market_intelligence"]["market_size"],
                "growthRate": ai_dashboard_data["market_intelligence"]["growth_rate"],
                "competitionLevel": ai_dashboard_data["market_intelligence"]["competition_level"],
                "opportunityScore": ai_dashboard_data["market_intelligence"]["opportunity_score"],
                "industry": "Technology"
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
            "businessIdeas": ai_dashboard_data["business_ideas"],  # This will have 5 ideas
            "aiGenerated": True,
            "generatedAt": ai_dashboard_data["generated_at"],
            "businessAnalysis": ai_dashboard_data["business_analysis"],
            "financialInsights": ai_dashboard_data["financial_insights"],
            "userValidation": {
                "idea": "AI-Generated Business",
                "industry": "Technology",
                "targetMarket": "SMBs",
                "verdict": "AI Generated Insights",
                "executiveSummary": ai_dashboard_data["business_analysis"]["industry_analysis"]
            },
            "hasData": True,
            "dataSource": "LLM Agents",
            "lastUpdated": ai_dashboard_data["generated_at"]
        }
        
        return transformed_data
        
    except Exception as e:
        print(f"Error generating AI dashboard: {str(e)}")
        return {
            "error": f"Failed to generate AI dashboard: {str(e)}",
            "businessIdeas": [],
            "aiGenerated": False
        }

@app.post("/api/v1/dashboard/ai-generated/refresh")
async def refresh_ai_dashboard():
    """Generate fresh AI-powered dashboard data"""
    try:
        # Generate fresh dashboard data
        fresh_ai_data = await llm_agent_service.generate_dashboard_data({
            "industry": "Technology",
            "target_market": "Small to Medium Businesses",
            "business_stage": "Early Stage"
        })
        
        return {
            "message": "AI dashboard data refreshed successfully!",
            "generated_at": fresh_ai_data["generated_at"],
            "score": fresh_ai_data["score"],
            "ideas_count": len(fresh_ai_data["business_ideas"]),
            "ai_generated": True,
            "businessIdeas": fresh_ai_data["business_ideas"]
        }
        
    except Exception as e:
        print(f"Error refreshing AI dashboard: {str(e)}")
        return {
            "error": f"Failed to refresh AI dashboard: {str(e)}",
            "ai_generated": False
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting minimal dashboard server...")
    print("📊 This server provides the 5-idea dashboard functionality")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
