from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agents.base_agent import BaseAgent
from app.tools.web_search import tavily_search


COMPETITOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a competitive intelligence expert specializing in Ethiopian markets. Analyze the competitive landscape "
            "for the given startup idea and produce a structured report covering:\n"
            "1. Top 5 direct Ethiopian competitors (name, funding, market share, strengths/weaknesses in Ethiopia)\n"
            "2. Top 3 indirect/adjacent Ethiopian competitors\n"
            "3. Competitive moats and differentiation opportunities in Ethiopian context\n"
            "4. Competitive positioning matrix for Ethiopian market\n"
            "5. Blue ocean strategy opportunities specific to Ethiopia\n"
            "6. Ethiopian competitive landscape analysis\n"
            "7. Consider Ethiopian business environment, regulations, and market conditions\n"
            "8. Focus on companies operating in or targeting Ethiopian market\n"
            "Use the search results to ground your analysis in real companies operating in Ethiopia.",
        ),
        (
            "human",
            "Startup Idea: {idea}\n"
            "Industry: {industry}\n"
            "Target Market: {target_market}\n\n"
            "Search Results:\n{search_results}\n\n"
            "Provide a thorough Ethiopian competitor analysis.",
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
            f"top competitors {industry} Ethiopia Ethiopian companies startups {target_market}"
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
