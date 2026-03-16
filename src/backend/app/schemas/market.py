from typing import List, Optional
from pydantic import BaseModel, Field


class CompetitorModel(BaseModel):
    name: str
    description: str
    strengths: List[str]
    weaknesses: List[str]
    market_share_estimate: Optional[str] = None


class MarketIntelligenceRequest(BaseModel):
    industry: str = Field(..., description="The industry or sector to analyze")
    target_market: str = Field(default="Global", description="Target market or geography")


class MarketIntelligenceResponse(BaseModel):
    industry: str
    target_market: str
    
    # Overview
    market_size_estimate: str = Field(default="Unknown", description="Estimated TAM or market size")
    cagr_estimate: str = Field(default="Unknown", description="Estimated Compound Annual Growth Rate")
    market_overview: str = Field(..., description="High-level narrative of the market")
    
    # Analysis
    key_trends: List[str] = Field(default_factory=list, description="Current trends driving the market")
    opportunities: List[str] = Field(default_factory=list, description="Strategic areas for entry or growth")
    risks: List[str] = Field(default_factory=list, description="Major threats or regulatory risks")
    
    # Competitors
    top_competitors: List[CompetitorModel] = Field(default_factory=list)

    # Error capture
    error: Optional[str] = None
