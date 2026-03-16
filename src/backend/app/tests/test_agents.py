import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_market_research_agent_returns_string():
    """Market Research Agent should return non-empty string."""
    with patch("app.tools.web_search.tavily_search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = "Mock search results about HealthTech market."
        from app.agents.market_research_agent import MarketResearchAgent
        agent = MarketResearchAgent()
        agent.chain = AsyncMock(return_value="Mock market research output")
        result = await agent.run("AI meal planner for diabetics", "HealthTech", "US")
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.asyncio
async def test_competitor_agent_returns_string():
    """Competitor Agent should return a non-empty analysis string."""
    with patch("app.tools.web_search.tavily_search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = "Mock competitor data."
        from app.agents.competitor_agent import CompetitorAgent
        agent = CompetitorAgent()
        agent.chain = AsyncMock(return_value="Mock competitor analysis output")
        result = await agent.run("AI meal planner", "HealthTech", "US")
        assert isinstance(result, str)


@pytest.mark.asyncio
async def test_decision_agent_returns_dict():
    """Decision Agent should return a dict with required keys."""
    from app.agents.decision_agent import DecisionAgent
    agent = DecisionAgent()
    agent.chain = AsyncMock(return_value={
        "overall_score": 75.0,
        "market_score": 80.0,
        "competition_score": 70.0,
        "risk_score": 65.0,
        "verdict": "GO",
        "key_strengths": ["Strong market", "Low competition"],
        "key_risks": ["Regulatory risk"],
        "recommendations": ["Focus on B2B"],
        "executive_summary": "Strong opportunity in HealthTech.",
    })
    result = await agent.run("AI meal planner", "HealthTech", "Research", "Analysis")
    assert isinstance(result, dict)
    assert "verdict" in result
