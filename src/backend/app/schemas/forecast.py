from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    period: str = Field(..., description="e.g. 'Q1 2023', '2022', 'Jan 2024'")
    value: float = Field(..., description="Numeric value of the metric")


class ForecastRequest(BaseModel):
    metric: str = Field(..., description="Metric name e.g. 'Revenue', 'Net Income'")
    historical_data: List[DataPoint] = Field(..., min_length=3)
    forecast_periods: int = Field(default=4, ge=1, le=20)
    model_type: Optional[str] = Field(
        default="auto",
        description="'linear', 'polynomial', 'auto'",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "metric": "Revenue",
                "historical_data": [
                    {"period": "Q1 2023", "value": 100000},
                    {"period": "Q2 2023", "value": 118000},
                    {"period": "Q3 2023", "value": 134000},
                    {"period": "Q4 2023", "value": 152000},
                ],
                "forecast_periods": 4,
                "model_type": "auto",
            }
        }
    }


class ForecastDataPoint(BaseModel):
    period: str
    value: float
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    is_forecast: bool = False


class ForecastResponse(BaseModel):
    metric: str
    model_used: str
    r_squared: float = Field(description="Model R² score (goodness of fit)")
    avg_growth_rate: float = Field(description="Average period-over-period growth %")
    data_points: List[ForecastDataPoint]
    interpretation: str = Field(description="LLM-generated narrative interpretation")
    confidence: str = Field(description="High / Medium / Low")
