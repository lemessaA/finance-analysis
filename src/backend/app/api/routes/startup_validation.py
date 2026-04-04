from __future__ import annotations

from fastapi import APIRouter, HTTPException, status, Request

from app.schemas.startup import StartupValidationRequest, StartupValidationResponse
from app.workflows.startup_validator_graph import run_startup_validation
from app.services.scoring_service import score_startup
from app.utils.logger import setup_logger
from app.middleware.language import get_language_from_request, get_localized_prompt

logger = setup_logger(__name__)
router = APIRouter()


@router.post(
    "/validate",
    response_model=StartupValidationResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate a startup idea using multi-agent analysis",
    description=(
        "Runs a multi-agent LangGraph pipeline: Market Research → Competitor Analysis "
        "→ Risk Assessment → Decision Synthesis. Returns a full validation report with score."
    ),
)
async def validate_startup(request: Request, payload: StartupValidationRequest):
    language = get_language_from_request(request)
    logger.info(f"Validating startup idea in {language}: {payload.idea[:60]}...")
    try:
        # Create localized prompt context
        context = {
            'industry': payload.industry,
            'target_market': payload.target_market
        }
        
        result = await run_startup_validation(
            idea=payload.idea,
            industry=payload.industry,
            target_market=payload.target_market,
            additional_context=get_localized_prompt(payload.additional_context or "", language, context),
        )
        # Enrich the result with composite scoring
        scoring = await score_startup(
            overall_score=result.overall_score,
            market_score=result.market_score,
            competition_score=result.competition_score,
            risk_score=result.risk_score,
            verdict=result.verdict,
        )
        logger.info(
            f"Startup scored: {scoring['grade']} "
            f"(composite={scoring['composite_score']}, verdict={result.verdict})"
        )
        return result
    except Exception as exc:
        logger.error(f"Startup validation failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation pipeline error: {str(exc)}",
        )
