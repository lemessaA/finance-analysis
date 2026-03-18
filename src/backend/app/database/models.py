from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Float, Text, DateTime, Integer, JSON, Boolean
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


class Competitor(Base):
    """Stores competitor analysis data."""

    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    market_share: Mapped[str] = mapped_column(String(50))
    revenue: Mapped[str] = mapped_column(String(50))
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    weaknesses: Mapped[list] = mapped_column(JSON, default=list)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class MarketAnalysis(Base):
    """Stores market analysis data."""

    __tablename__ = "market_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    industry: Mapped[str] = mapped_column(String(100))
    market_size: Mapped[str] = mapped_column(String(50))
    growth_rate: Mapped[str] = mapped_column(String(20))
    competition_level: Mapped[str] = mapped_column(String(50))
    opportunity_score: Mapped[int] = mapped_column(Integer)
    total_addressable_market: Mapped[str] = mapped_column(String(50), nullable=True)
    serviceable_addressable_market: Mapped[str] = mapped_column(String(50), nullable=True)
    market_trends: Mapped[list] = mapped_column(JSON, default=list)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class FinancialMetric(Base):
    """Stores financial comparison metrics."""

    __tablename__ = "financial_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String(100))
    your_company: Mapped[float] = mapped_column(Float)
    industry_avg: Mapped[float] = mapped_column(Float)
    top_performer: Mapped[float] = mapped_column(Float)
    percentile: Mapped[int] = mapped_column(Integer, nullable=True)
    metric_type: Mapped[str] = mapped_column(String(50), default="financial")  # financial, growth, operational
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class MarketSegment(Base):
    """Stores market segment data."""

    __tablename__ = "market_segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int] = mapped_column(Integer)  # percentage
    color: Mapped[str] = mapped_column(String(20), default="#4f62ff")
    industry: Mapped[str] = mapped_column(String(100), nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class RevenueForecast(Base):
    """Stores revenue forecast data points."""

    __tablename__ = "revenue_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    month: Mapped[str] = mapped_column(String(20))
    actual: Mapped[float] = mapped_column(Float, nullable=True)
    forecast: Mapped[float] = mapped_column(Float)
    forecast_model: Mapped[str] = mapped_column(String(100), nullable=True)
    confidence_interval: Mapped[float] = mapped_column(Float, nullable=True)
    is_forecast: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
