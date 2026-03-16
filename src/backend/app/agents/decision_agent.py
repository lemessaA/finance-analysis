from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

from app.agents.base_agent import BaseAgent


class ValidationScore(BaseModel):
    overall_score: float = Field(description="Overall viability score from 0-100")
    market_score: float = Field(description="Market opportunity score 0-100")
    competition_score: float = Field(description="Competitive positioning score 0-100")
    risk_score: float = Field(description="Risk-adjusted score 0-100 (higher = lower risk)")
    verdict: str = Field(description="STRONG GO / GO / CONDITIONAL GO / NO GO")
    key_strengths: List[str] = Field(description="Top 3-5 key strengths")
    key_risks: List[str] = Field(description="Top 3-5 key risks")
    recommendations: List[str] = Field(description="Top 3-5 actionable recommendations")
    executive_summary: str = Field(description="2-3 sentence executive summary")


DECISION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a venture capital partner making an investment decision. "
            "Synthesize all research and analysis to produce a final validation report. "
            "Return ONLY valid JSON matching the requested schema — no extra text.",
        ),
        (
            "human",
            "Startup Idea: {idea}\n"
            "Industry: {industry}\n\n"
            "MARKET RESEARCH:\n{market_research}\n\n"
            "COMPETITOR ANALYSIS:\n{competitor_analysis}\n\n"
            "ADDITIONAL CONTEXT:\n{additional_context}\n\n"
            "Synthesize the above and return a JSON validation report.",
        ),
    ]
)


class DecisionAgent(BaseAgent):
    """Synthesizes research from all agents into a final validation report."""

    def __init__(self):
        super().__init__(name="DecisionAgent", temperature=0.0)
        self.parser = JsonOutputParser(pydantic_object=ValidationScore)
        self.chain = DECISION_PROMPT | self.llm | self.parser

    async def run(
        self,
        idea: str,
        industry: str,
        market_research: str,
        competitor_analysis: str,
        additional_context: str = "",
    ) -> dict:
        self._log_start("final decision synthesis")

        result = await self.chain.ainvoke(
            {
                "idea": idea,
                "industry": industry,
                "market_research": market_research,
                "competitor_analysis": competitor_analysis,
                "additional_context": additional_context or "None provided.",
            }
        )
        self._log_done("final decision synthesis")
        return result
