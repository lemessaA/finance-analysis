from __future__ import annotations

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class FinancialMetrics(BaseModel):
    revenue: Optional[str] = Field(None, description="Total revenue for the period")
    net_profit: Optional[str] = Field(None, description="Net profit or net income")
    operating_income: Optional[str] = Field(None, description="Operating income or EBIT")
    total_assets: Optional[str] = Field(None, description="Total assets")
    total_liabilities: Optional[str] = Field(None, description="Total liabilities")
    cash_flow: Optional[str] = Field(None, description="Operating or Free cash flow")
    revenue_growth_yoy: Optional[str] = None
    gross_margin: Optional[str] = None
    ebitda: Optional[str] = None
    ebitda_margin: Optional[str] = None
    net_margin: Optional[str] = None
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


class ComparisonRequest(BaseModel):
    baseline_report_id: str
    current_report_id: str


class ComparisonResponse(BaseModel):
    baseline_id: str
    current_id: str
    comparison_results: Dict[str, Any]
