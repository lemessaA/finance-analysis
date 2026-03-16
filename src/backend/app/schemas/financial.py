from __future__ import annotations

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class FinancialMetrics(BaseModel):
    revenue: Optional[str] = None
    revenue_growth_yoy: Optional[str] = None
    gross_margin: Optional[str] = None
    ebitda: Optional[str] = None
    ebitda_margin: Optional[str] = None
    net_income: Optional[str] = None
    net_margin: Optional[str] = None
    operating_cash_flow: Optional[str] = None
    free_cash_flow: Optional[str] = None
    eps: Optional[str] = None
    current_ratio: Optional[str] = None
    debt_to_equity: Optional[str] = None


class FinancialReportResponse(BaseModel):
    filename: str
    page_count: int
    metrics: FinancialMetrics
    analysis: str = Field(description="Full LLM-generated financial analysis narrative")
    key_highlights: List[str] = []
    key_risks: List[str] = []
    raw_text_length: int = 0
