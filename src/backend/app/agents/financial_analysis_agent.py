from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.agents.base_agent import BaseAgent
from app.config import settings
from app.schemas.financial import FinancialReportResponse


FINANCIAL_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a CFA-level financial analyst. From the provided financial document text, "
            "extract and analyze all key financial metrics, highlights and risks. Provide:\n"
            "1. Core metrics: Revenue, Net Profit, Operating Income, Total Assets, Total Liabilities, Cash Flow\n"
            "2. Additional metrics: Revenue Growth (YoY), Margins, EPS, Liquidity, Debt metrics\n"
            "3. Key risks and highlights from the report (max 5 each)\n"
            "4. A comprehensive narrative analysis of the financial state.\n\n"
            "IMPORTANT: If a metric cannot be found, set it to 'Not disclosed'. Extract numbers accurately. "
            "Your output must be structured as the defined JSON schema.",
        ),
        (
            "human",
            "Financial Document: {filename}\n\n"
            "Extracted Text:\n{text}\n\n"
            "Analyze and extract all financial metrics as requested.",
        ),
    ]
)


class FinancialAnalysisAgent(BaseAgent):
    """Extracts and analyzes financial metrics from document text."""

    def __init__(self):
        super().__init__(name="FinancialAnalysisAgent", temperature=0.0)
        # Use a model that supports structured output
        llm = ChatGroq(
            temperature=0.0,
            model="openai/gpt-oss-20b",  # This model supports structured output
            api_key=settings.GROQ_API_KEY,
        )
        self.chain = FINANCIAL_ANALYSIS_PROMPT | llm.with_structured_output(FinancialReportResponse)

    async def run(self, text: str, filename: str) -> FinancialReportResponse:
        self._log_start(f"financial analysis of {filename}")

        # Truncate to avoid token limits (keep first 15K chars of financial data)
        truncated = text[:50000]

        try:
            result: FinancialReportResponse = await self.chain.ainvoke({"text": truncated, "filename": filename})
            # Overwrite internal bookkeeping fields
            result.filename = filename
            result.raw_text_length = len(text)
            
            self._log_done("financial analysis")
            return result
        except Exception as e:
            # Fallback response if structured output fails
            self._log_error(f"structured output failed: {e}")
            # Create a basic response with the text analysis
            return FinancialReportResponse(
                filename=filename,
                page_count=1,
                metrics={
                    "revenue": "Not disclosed",
                    "net_profit": "Not disclosed",
                    "operating_income": "Not disclosed",
                    "total_assets": "Not disclosed",
                    "total_liabilities": "Not disclosed",
                    "cash_flow": "Not disclosed",
                    "revenue_growth_yoy": "Not disclosed",
                    "gross_margin": "Not disclosed",
                    "ebitda": "Not disclosed",
                    "ebitda_margin": "Not disclosed",
                    "net_margin": "Not disclosed",
                    "eps": "Not disclosed",
                    "current_ratio": "Not disclosed",
                    "debt_to_equity": "Not disclosed"
                },
                analysis=f"Unable to extract structured financial data from the document. Extracted text preview: {truncated[:500]}...",
                key_highlights=["Document processed but structured extraction failed"],
                key_risks=["Unable to extract financial metrics due to processing error"],
                raw_text_length=len(text)
            )
