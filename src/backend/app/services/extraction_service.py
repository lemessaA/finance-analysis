from __future__ import annotations

from app.agents.financial_analysis_agent import FinancialAnalysisAgent
from app.schemas.financial import FinancialReportResponse
from app.services.pdf_service import _extract
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

_financial_agent = FinancialAnalysisAgent()


async def extract_financial_metrics(
    content: bytes, filename: str
) -> FinancialReportResponse:
    """Full pipeline: PDF bytes → text → LLM analysis → structured response."""
    text, page_count = _extract(content)

    # The agent now returns a FinancialReportResponse directly via structured output
    result: FinancialReportResponse = await _financial_agent.run(text=text, filename=filename)
    
    # Ensure page count is set correctly from the PDF extraction
    result.page_count = page_count

    return result
