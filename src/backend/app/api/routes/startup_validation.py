from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.startup import StartupValidationRequest, StartupValidationResponse
from app.workflows.startup_validator_graph import run_startup_validation
from app.utils.logger import setup_logger

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
async def validate_startup(payload: StartupValidationRequest):
    logger.info(f"Validating startup idea: {payload.idea[:60]}...")
    try:
        result = await run_startup_validation(
            idea=payload.idea,
            industry=payload.industry,
            target_market=payload.target_market,
            additional_context=payload.additional_context,
        )
        return result
    except Exception as exc:
        logger.error(f"Startup validation failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation pipeline error: {str(exc)}",
        )
