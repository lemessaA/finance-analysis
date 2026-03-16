from __future__ import annotations

from typing import Optional, List
from typing_extensions import TypedDict


class StartupValidatorState(TypedDict):
    """LangGraph state flowing through the startup validation pipeline."""

    # Input
    idea: str
    industry: str
    target_market: str
    additional_context: Optional[str]

    # Agent outputs (populated sequentially)
    market_research: Optional[str]
    competitor_analysis: Optional[str]

    # Final decision output
    overall_score: Optional[float]
    market_score: Optional[float]
    competition_score: Optional[float]
    risk_score: Optional[float]
    verdict: Optional[str]
    key_strengths: Optional[List[str]]
    key_risks: Optional[List[str]]
    recommendations: Optional[List[str]]
    executive_summary: Optional[str]

    # Execution metadata
    error: Optional[str]
