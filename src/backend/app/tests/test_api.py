import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_health_endpoint():
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint():
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_startup_validation_endpoint():
    from app.main import app
    from app.schemas.startup import StartupValidationResponse
    mock_response = StartupValidationResponse(
        idea="Test idea",
        industry="Tech",
        target_market="US",
        market_research="Good market",
        competitor_analysis="Few competitors",
        overall_score=75.0,
        market_score=80.0,
        competition_score=70.0,
        risk_score=65.0,
        verdict="GO",
        key_strengths=[],
        key_risks=[],
        recommendations=[],
        executive_summary="Viable.",
        error=None,
    )
    with patch(
        "app.api.routes.startup_validation.run_startup_validation",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/startup/validate",
                json={"idea": "Test startup idea for testing", "industry": "Tech"},
            )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_forecast_requires_min_data_points():
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/forecasting/forecast",
            json={
                "metric": "Revenue",
                "historical_data": [{"period": "Q1", "value": 100}],  # Only 1 point — should fail
                "forecast_periods": 4,
            },
        )
    assert response.status_code == 422
