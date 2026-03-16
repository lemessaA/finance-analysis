from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline

from app.agents.forecasting_agent import ForecastingAgent
from app.schemas.forecast import ForecastRequest, ForecastResponse, ForecastDataPoint
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
_forecast_agent = ForecastingAgent()


def _select_model(X: np.ndarray, y: np.ndarray, model_type: str):
    """Select and fit the best model based on type or auto-selection."""
    if model_type == "polynomial":
        model = Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("reg", LinearRegression()),
        ])
    elif model_type == "linear":
        model = LinearRegression()
    else:  # auto
        lin = LinearRegression().fit(X, y)
        lin_r2 = r2_score(y, lin.predict(X))

        poly_pipe = Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("reg", LinearRegression()),
        ])
        poly_pipe.fit(X, y)
        poly_r2 = r2_score(y, poly_pipe.predict(X))

        model = poly_pipe if poly_r2 > lin_r2 + 0.05 else lin
        logger.info(f"Auto-selected model: {'polynomial' if model == poly_pipe else 'linear'} "
                    f"(R²={max(lin_r2, poly_r2):.3f})")
        return model, max(lin_r2, poly_r2)

    model.fit(X, y)
    return model, r2_score(y, model.predict(X))


async def generate_forecast(payload: ForecastRequest) -> ForecastResponse:
    """Run sklearn forecasting and return structured results with LLM narrative."""
    periods = [dp.period for dp in payload.historical_data]
    values = np.array([dp.value for dp in payload.historical_data], dtype=float)
    n = len(values)

    # Feature: integer time index
    X_hist = np.arange(n).reshape(-1, 1)

    model_type = payload.model_type or "auto"
    model, r2 = _select_model(X_hist, values, model_type)
    model_name = "Polynomial Regression" if "poly" in str(type(model)) else "Linear Regression"

    # Forecast future periods
    X_future = np.arange(n, n + payload.forecast_periods).reshape(-1, 1)
    forecasted_values = model.predict(X_future)

    # Confidence intervals (±10% as heuristic band)
    residuals = values - model.predict(X_hist)
    std = float(np.std(residuals))
    band = std * 1.5 if std > 0 else np.abs(forecasted_values) * 0.1

    # Growth rate
    growth_rates = [
        (values[i] - values[i - 1]) / values[i - 1] * 100
        for i in range(1, n)
        if values[i - 1] != 0
    ]
    avg_growth = float(np.mean(growth_rates)) if growth_rates else 0.0

    # Build unified data points list
    data_points: list[ForecastDataPoint] = []
    for p, v in zip(periods, values.tolist()):
        data_points.append(ForecastDataPoint(period=p, value=round(v, 2), is_forecast=False))

    future_labels = [f"F{i + 1}" for i in range(payload.forecast_periods)]
    for label, fv in zip(future_labels, forecasted_values.tolist()):
        data_points.append(
            ForecastDataPoint(
                period=label,
                value=round(fv, 2),
                lower_bound=round(fv - band, 2),
                upper_bound=round(fv + band, 2),
                is_forecast=True,
            )
        )

    # LLM interpretation
    interpretation = await _forecast_agent.run(
        metric=payload.metric,
        historical_data=[{"period": p, "value": float(v)} for p, v in zip(periods, values)],
        forecast_data=[{"period": l, "value": round(float(fv), 2)} for l, fv in zip(future_labels, forecasted_values)],
        model_type=model_name,
        growth_rate=avg_growth,
    )

    confidence = "High" if r2 >= 0.85 else ("Medium" if r2 >= 0.6 else "Low")

    return ForecastResponse(
        metric=payload.metric,
        model_used=model_name,
        r_squared=round(r2, 4),
        avg_growth_rate=round(avg_growth, 2),
        data_points=data_points,
        interpretation=interpretation,
        confidence=confidence,
    )
