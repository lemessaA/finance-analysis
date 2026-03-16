import pytest
import numpy as np
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_generate_forecast_basic():
    """Forecast service should return ForecastResponse with correct periods."""
    from app.schemas.forecast import ForecastRequest, DataPoint
    from app.services.forecasting_service import generate_forecast

    payload = ForecastRequest(
        metric="Revenue",
        historical_data=[
            DataPoint(period="Q1 2023", value=100000),
            DataPoint(period="Q2 2023", value=115000),
            DataPoint(period="Q3 2023", value=130000),
            DataPoint(period="Q4 2023", value=148000),
        ],
        forecast_periods=4,
        model_type="linear",
    )

    with pytest.MonkeyPatch.context() as mp:
        from app.agents import forecasting_agent
        mp.setattr(
            "app.services.forecasting_service._forecast_agent.run",
            AsyncMock(return_value="Mock forecast interpretation"),
        )
        result = await generate_forecast(payload)

    assert result.metric == "Revenue"
    assert len(result.data_points) == 8  # 4 historical + 4 forecast
    assert any(dp.is_forecast for dp in result.data_points)
    assert result.r_squared >= 0.0


def test_model_auto_select_linear():
    """Auto-select should prefer linear for clean linear data."""
    from app.ml.train import train_forecasting_model

    X = np.arange(10).reshape(-1, 1)
    y = np.array([i * 2 + 1 for i in range(10)], dtype=float)

    model, name, r2 = train_forecasting_model(X, y, model_type="auto")
    assert r2 > 0.99
    assert "Linear" in name or "Polynomial" in name


def test_growth_rates_computation():
    """Growth rates should be computed correctly."""
    from app.ml.feature_engineering import compute_growth_rates

    values = [100.0, 110.0, 121.0, 133.1]
    rates = compute_growth_rates(values)
    assert len(rates) == 3
    assert abs(rates[0] - 10.0) < 0.1
