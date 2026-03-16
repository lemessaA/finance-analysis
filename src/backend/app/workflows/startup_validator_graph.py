from __future__ import annotations

from langgraph.graph import StateGraph, END, START

from app.agents.market_research_agent import MarketResearchAgent
from app.agents.competitor_agent import CompetitorAgent
from app.agents.decision_agent import DecisionAgent
from app.workflows.state_schema import StartupValidatorState
from app.schemas.startup import StartupValidationResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# ── Instantiate agents ────────────────────────────────────────────────────────
_market_agent = MarketResearchAgent()
_competitor_agent = CompetitorAgent()
_decision_agent = DecisionAgent()


# ── Node functions ────────────────────────────────────────────────────────────

async def market_research_node(state: StartupValidatorState) -> StartupValidatorState:
    """Node 1: Conduct market research."""
    logger.info("Graph node: market_research_node")
    try:
        result = await _market_agent.run(
            idea=state["idea"],
            industry=state["industry"],
            target_market=state["target_market"],
        )
        return {**state, "market_research": result}
    except Exception as exc:
        logger.error(f"market_research_node failed: {exc}")
        return {**state, "error": str(exc), "market_research": "Research unavailable."}


async def competitor_analysis_node(state: StartupValidatorState) -> StartupValidatorState:
    """Node 2: Analyze competitors."""
    logger.info("Graph node: competitor_analysis_node")
    try:
        result = await _competitor_agent.run(
            idea=state["idea"],
            industry=state["industry"],
            target_market=state["target_market"],
        )
        return {**state, "competitor_analysis": result}
    except Exception as exc:
        logger.error(f"competitor_analysis_node failed: {exc}")
        return {**state, "error": str(exc), "competitor_analysis": "Analysis unavailable."}


async def decision_node(state: StartupValidatorState) -> StartupValidatorState:
    """Node 3: Synthesize final decision."""
    logger.info("Graph node: decision_node")
    try:
        result = await _decision_agent.run(
            idea=state["idea"],
            industry=state["industry"],
            market_research=state.get("market_research", ""),
            competitor_analysis=state.get("competitor_analysis", ""),
            additional_context=state.get("additional_context") or "",
        )
        return {**state, **result}
    except Exception as exc:
        logger.error(f"decision_node failed: {exc}")
        return {**state, "error": str(exc)}


# ── Build graph ───────────────────────────────────────────────────────────────

def _build_graph() -> StateGraph:
    graph = StateGraph(StartupValidatorState)

    graph.add_node("market_research", market_research_node)
    graph.add_node("competitor_analysis", competitor_analysis_node)
    graph.add_node("decision", decision_node)

    graph.add_edge(START, "market_research")
    graph.add_edge("market_research", "competitor_analysis")
    graph.add_edge("competitor_analysis", "decision")
    graph.add_edge("decision", END)

    return graph.compile()


_compiled_graph = _build_graph()


# ── Public interface ──────────────────────────────────────────────────────────

async def run_startup_validation(
    idea: str,
    industry: str,
    target_market: str,
    additional_context: str | None = None,
) -> StartupValidationResponse:
    """Run the full startup validation multi-agent pipeline."""

    initial_state: StartupValidatorState = {
        "idea": idea,
        "industry": industry,
        "target_market": target_market,
        "additional_context": additional_context,
        "market_research": None,
        "competitor_analysis": None,
        "overall_score": None,
        "market_score": None,
        "competition_score": None,
        "risk_score": None,
        "verdict": None,
        "key_strengths": None,
        "key_risks": None,
        "recommendations": None,
        "executive_summary": None,
        "error": None,
    }

    final_state = await _compiled_graph.ainvoke(initial_state)

    return StartupValidationResponse(
        idea=idea,
        industry=industry,
        target_market=target_market,
        market_research=final_state.get("market_research", ""),
        competitor_analysis=final_state.get("competitor_analysis", ""),
        overall_score=final_state.get("overall_score", 0.0),
        market_score=final_state.get("market_score", 0.0),
        competition_score=final_state.get("competition_score", 0.0),
        risk_score=final_state.get("risk_score", 0.0),
        verdict=final_state.get("verdict", "NO GO"),
        key_strengths=final_state.get("key_strengths", []),
        key_risks=final_state.get("key_risks", []),
        recommendations=final_state.get("recommendations", []),
        executive_summary=final_state.get("executive_summary", ""),
        error=final_state.get("error"),
    )
