import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_market_research_agent_returns_string():
    """Market Research Agent should return non-empty string."""
    with patch("app.tools.web_search.tavily_search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = "Mock search results about HealthTech market."
        from app.agents.market_research_agent import MarketResearchAgent
        agent = MarketResearchAgent()
        # Patch ainvoke on the chain so it returns the mocked output directly
        agent.chain.ainvoke = AsyncMock(return_value="Mock market research output")
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
        agent.chain.ainvoke = AsyncMock(return_value="Mock competitor analysis output")
        result = await agent.run("AI meal planner", "HealthTech", "US")
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.asyncio
async def test_decision_agent_returns_dict():
    """Decision Agent should return a dict with required keys."""
    from app.agents.decision_agent import DecisionAgent, ValidationScore
    agent = DecisionAgent()

    mock_score = ValidationScore(
        overall_score=75.0,
        market_score=80.0,
        competition_score=70.0,
        risk_score=65.0,
        verdict="GO",
        key_strengths=["Strong market", "Low competition"],
        key_risks=["Regulatory risk"],
        recommendations=["Focus on B2B"],
        executive_summary="Strong opportunity in HealthTech.",
    )
    # with_structured_output returns a Pydantic object; run() calls .model_dump()
    agent.chain.ainvoke = AsyncMock(return_value=mock_score)
    result = await agent.run("AI meal planner", "HealthTech", "Research", "Analysis")
    assert isinstance(result, dict)
    assert "verdict" in result
    assert result["overall_score"] == 75.0
