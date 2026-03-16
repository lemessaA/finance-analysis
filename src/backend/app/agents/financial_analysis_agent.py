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
        # Use an LLM instance capable of structured output
        llm = ChatGroq(
            temperature=0.0,
            model="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY,
        )
        self.chain = FINANCIAL_ANALYSIS_PROMPT | llm.with_structured_output(FinancialReportResponse)

    async def run(self, text: str, filename: str) -> FinancialReportResponse:
        self._log_start(f"financial analysis of {filename}")

        # Truncate to avoid token limits (keep first 15K chars of financial data)
        truncated = text[:15000]

        result: FinancialReportResponse = await self.chain.ainvoke({"text": truncated, "filename": filename})
        # Overwrite internal bookkeeping fields
        result.filename = filename
        result.raw_text_length = len(text)
        
        self._log_done("financial analysis")
        return result
