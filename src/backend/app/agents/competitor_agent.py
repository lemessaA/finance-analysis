from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agents.base_agent import BaseAgent
from app.tools.web_search import tavily_search


COMPETITOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a competitive intelligence expert. Analyze the competitive landscape "
            "for the given startup idea and produce a structured report covering:\n"
            "1. Top 5 direct competeitors (name, funding, market share, strengths/weaknesses in ethiopia)\n"
            "2. Top 3 indirect/adjacent competitors\n"
            "3. Competitive moats and differentiation opportunities\n"
            "4. Competitive positioning matrix\n"
            "5. Blue ocean strategy opportunities\n\n"
            "Use the search results to ground your analysis in real companies.",
        ),
        (
            "human",
            "Startup Idea: {idea}\n"
            "Industry: {industry}\n"
            "Target Market: {target_market}\n\n"
            "Search Results:\n{search_results}\n\n"
            "Provide a thorough competitor analysis.",
        ),
    ]
)


class CompetitorAgent(BaseAgent):
    """Identifies and analyzes the competitive landscape."""

    def __init__(self):
        super().__init__(name="CompetitorAgent", temperature=0.1)
        self.chain = COMPETITOR_PROMPT | self.llm | StrOutputParser()

    async def run(self, idea: str, industry: str, target_market: str) -> str:
        self._log_start(f"competitor analysis for: {idea[:50]}")

        search_results = await tavily_search(
            f"top competitors {industry} startups companies {target_market}"
        )

        result = await self.chain.ainvoke(
            {
                "idea": idea,
                "industry": industry,
                "target_market": target_market,
                "search_results": search_results,
            }
        )
        self._log_done("competitor analysis")
        return result
