from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class StartupValidationRequest(BaseModel):
    idea: str = Field(..., min_length=10, description="The startup idea to validate")
    industry: str = Field(..., min_length=2, description="Industry or sector")
    target_market: str = Field(default="Global", description="Target market or geography")
    additional_context: Optional[str] = Field(
        default=None, description="Optional background, constraints, or notes"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "idea": "An AI-powered meal planning app personalized for diabetic patients",
                "industry": "HealthTech",
                "target_market": "United States",
                "additional_context": "B2C SaaS model, targeting Type 2 diabetics aged 40-65",
            }
        }
    }


class StartupValidationResponse(BaseModel):
    idea: str
    industry: str
    target_market: str

    # Research outputs
    market_research: str = ""
    competitor_analysis: str = ""

    # Scores (0–100)
    overall_score: float = 0.0
    market_score: float = 0.0
    competition_score: float = 0.0
    risk_score: float = 0.0

    # Decision
    verdict: str = "NO GO"
    key_strengths: List[str] = []
    key_risks: List[str] = []
    recommendations: List[str] = []
    executive_summary: str = ""

    # Error capture
    error: Optional[str] = None
