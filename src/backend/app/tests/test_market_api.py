import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_market_intelligence_endpoint():
    from app.main import app
    from app.schemas.market import MarketIntelligenceResponse

    mock_response = MarketIntelligenceResponse(
        industry="Tech",
        target_market="US",
        market_size_estimate="$1B",
        cagr_estimate="10%",
        market_overview="A growing market.",
        key_trends=["AI adoption"],
        opportunities=["B2B SaaS"],
        risks=["Regulatory scrutiny"],
        top_competitors=[
            {
                "name": "Competitor A",
                "description": "Leader in the space",
                "strengths": ["Strong brand"],
                "weaknesses": ["Legacy tech"],
                "market_share_estimate": "40%"
            }
        ],
        error=None
    )

    with patch(
        "app.api.routes.market_intelligence.ChatGroq.with_structured_output",
    ) as mock_structured_output:
        # We need to mock the chain pipeline
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value = mock_response
        
        # When with_structured_output is called, it returns a mock that when used in a pipe returns our mock_chain
        # Actually it's easier to patch the market/competitor agents and the LLM chain directly.
        pass

    # Better to patch the whole route function or the agents.
    with patch(
        "app.api.routes.market_intelligence.MarketResearchAgent.run",
        new_callable=AsyncMock,
        return_value="Market Research Data"
    ), patch(
        "app.api.routes.market_intelligence.CompetitorAgent.run",
        new_callable=AsyncMock,
        return_value="Competitor Data"
    ), patch(
        "langchain_core.runnables.base.RunnableSequence.ainvoke",
        new_callable=AsyncMock,
        return_value=mock_response
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/market/analyze",
                json={"industry": "Tech", "target_market": "US"},
            )
            
    assert response.status_code == 200
    data = response.json()
    assert data["industry"] == "Tech"
    assert data["market_size_estimate"] == "$1B"
    assert len(data["top_competitors"]) == 1
    assert data["top_competitors"][0]["name"] == "Competitor A"
