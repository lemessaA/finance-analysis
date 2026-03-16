from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Float, Text, DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.session import Base


class StartupValidation(Base):
    """Persists startup validation results."""

    __tablename__ = "startup_validations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    idea: Mapped[str] = mapped_column(String(500))
    industry: Mapped[str] = mapped_column(String(200))
    target_market: Mapped[str] = mapped_column(String(200))
    overall_score: Mapped[float] = mapped_column(Float, nullable=True)
    verdict: Mapped[str] = mapped_column(String(50), nullable=True)
    executive_summary: Mapped[str] = mapped_column(Text, nullable=True)
    raw_response: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class FinancialReport(Base):
    """Persists analyzed financial report metadata."""

    __tablename__ = "financial_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    page_count: Mapped[int] = mapped_column(Integer)
    raw_text_length: Mapped[int] = mapped_column(Integer)
    metrics: Mapped[dict] = mapped_column(JSON, nullable=True)
    analysis: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ForecastRecord(Base):
    """Persists forecasting run records."""

    __tablename__ = "forecast_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    metric: Mapped[str] = mapped_column(String(200))
    model_used: Mapped[str] = mapped_column(String(100))
    r_squared: Mapped[float] = mapped_column(Float)
    avg_growth_rate: Mapped[float] = mapped_column(Float)
    confidence: Mapped[str] = mapped_column(String(20))
    data_points: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
