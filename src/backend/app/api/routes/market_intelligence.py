import asyncio
from fastapi import APIRouter, HTTPException

from app.schemas.market import MarketIntelligenceRequest, MarketIntelligenceResponse
from app.agents.market_research_agent import MarketResearchAgent
from app.agents.competitor_agent import CompetitorAgent
# Re-using the decision agent just for its LLM synthesis capability 
# if we needed a final sweep, but we can also just compile results here.
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=MarketIntelligenceResponse)
async def analyze_market(payload: MarketIntelligenceRequest):
    """
    Run a comprehensive market intelligence analysis.
    Uses MarketResearchAgent and CompetitorAgent in parallel to gather data,
    then synthesizes a structured MarketIntelligenceResponse.
    """
    logger.info(f"Starting market intelligence for: {payload.industry} in {payload.target_market}")
    try:
        # Initialize sub-agents
        market_agent = MarketResearchAgent()
        competitor_agent = CompetitorAgent()

        # Gather raw research data in parallel
        market_future = market_agent.run(
            idea=f"General {payload.industry} market analysis", 
            industry=payload.industry, 
            target_market=payload.target_market
        )
        competitor_future = competitor_agent.run(
            idea=f"General {payload.industry} market analysis", 
            industry=payload.industry, 
            target_market=payload.target_market
        )
        
        market_research_text, competitor_analysis_text = await asyncio.gather(
            market_future, competitor_future
        )

        # Synthesize into the final JSON structured response
        llm = ChatGroq(
            temperature=0.1,
            model_name=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a top-tier Market Intelligence Analyst specializing in Ethiopian markets.
You have been provided with raw market research and competitor data focused on Ethiopia.
Your task is to synthesize this information into a structured JSON report with Ethiopian market focus.
Be extremely concise, factual, and analytical. Ensure all analysis considers Ethiopian context."""),
            ("user", """
Industry: {industry}
Target Market: {target_market}

--- MARKET RESEARCH ---
{market_research}

--- COMPETITOR DATA ---
{competitor_data}
""")
        ])

        chain = prompt | llm.with_structured_output(MarketIntelligenceResponse)
        
        result = await chain.ainvoke({
            "industry": payload.industry,
            "target_market": payload.target_market,
            "market_research": market_research_text,
            "competitor_data": competitor_analysis_text
        })
        
        logger.info("Market intelligence synthesis complete.")
        return result

    except Exception as exc:
        logger.error(f"Market intelligence failed: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
