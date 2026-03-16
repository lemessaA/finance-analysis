from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agents.base_agent import BaseAgent


FINANCIAL_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a CFA-level financial analyst. From the provided financial document text, "
            "extract and analyze all key financial metrics. Provide:\n"
            "1. Revenue & growth rates (YoY, QoQ)\n"
            "2. Profitability ratios (Gross Margin, EBITDA Margin, Net Margin)\n"
            "3. Cash flow analysis (Operating, Free Cash Flow)\n"
            "4. Liquidity metrics (Current Ratio, Quick Ratio)\n"
            "5. Debt metrics (D/E ratio, Interest Coverage)\n"
            "6. Earnings per share (EPS, diluted EPS)\n"
            "7. Key risks and highlights from the report\n\n"
            "If a metric cannot be found, state 'Not disclosed'. Be precise.",
        ),
        (
            "human",
            "Financial Document: {filename}\n\n"
            "Extracted Text:\n{text}\n\n"
            "Analyze and extract all financial metrics.",
        ),
    ]
)


class FinancialAnalysisAgent(BaseAgent):
    """Extracts and analyzes financial metrics from document text."""

    def __init__(self):
        super().__init__(name="FinancialAnalysisAgent", temperature=0.0)
        self.chain = FINANCIAL_ANALYSIS_PROMPT | self.llm | StrOutputParser()

    async def run(self, text: str, filename: str) -> str:
        self._log_start(f"financial analysis of {filename}")

        # Truncate to avoid token limits (keep first 12K chars of financial data)
        truncated = text[:12000]

        result = await self.chain.ainvoke({"text": truncated, "filename": filename})
        self._log_done("financial analysis")
        return result
