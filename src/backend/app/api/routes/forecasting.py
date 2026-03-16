from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.forecast import ForecastRequest, ForecastResponse
from app.services.forecasting_service import generate_forecast
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post(
    "/forecast",
    response_model=ForecastResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a financial forecast",
    description=(
        "Accepts historical financial data points and produces a forecast using "
        "scikit-learn regression models, then interprets the trend with an LLM narrative."
    ),
)
async def forecast(payload: ForecastRequest):
    if len(payload.historical_data) < 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least 3 historical data points are required for forecasting.",
        )

    logger.info(
        f"Forecasting {payload.metric} — {len(payload.historical_data)} historical "
        f"points → {payload.forecast_periods} periods ahead"
    )
    try:
        result = await generate_forecast(payload)
        return result
    except Exception as exc:
        logger.error(f"Forecasting failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Forecasting error: {str(exc)}",
        )
