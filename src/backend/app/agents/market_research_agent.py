from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agents.base_agent import BaseAgent
from app.tools.web_search import tavily_search


MARKET_RESEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert market research analyst. Analyze the given startup idea "
            "and provide a comprehensive market research report including:\n"
            "1. Total Addressable Market (TAM) size estimate\n"
            "2. Serviceable Addressable Market (SAM)\n"
            "3. Serviceable Obtainable Market (SOM)\n"
            "4. Key market trends and tailwinds\n"
            "5. Customer segments and personas\n"
            "6. Market maturity and growth rate\n\n"
            "Be specific with numbers and cite reasoning. Use the search results provided.",
        ),
        (
            "human",
            "Startup Idea: {idea}\n"
            "Industry: {industry}\n"
            "Target Market: {target_market}\n\n"
            "Search Results:\n{search_results}\n\n"
            "Provide a detailed market research analysis.",
        ),
    ]
)


class MarketResearchAgent(BaseAgent):
    """Researches market size, trends, and customer segmentation."""

    def __init__(self):
        super().__init__(name="MarketResearchAgent", temperature=0.1)
        self.chain = MARKET_RESEARCH_PROMPT | self.llm | StrOutputParser()

    async def run(self, idea: str, industry: str, target_market: str) -> str:
        self._log_start(f"market research for: {idea[:50]}")

        # Use Tavily to get real-time market data
        search_results = await tavily_search(
            f"{industry} market size trends {target_market} 2024 2025"
        )

        result = await self.chain.ainvoke(
            {
                "idea": idea,
                "industry": industry,
                "target_market": target_market,
                "search_results": search_results,
            }
        )
        self._log_done("market research")
        return result
