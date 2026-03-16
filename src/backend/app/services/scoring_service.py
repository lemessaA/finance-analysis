from __future__ import annotations

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def score_startup(
    overall_score: float,
    market_score: float,
    competition_score: float,
    risk_score: float,
    verdict: str,
) -> dict:
    """
    Compute a composite business viability score and grade.
    Weights: market=35%, competition=30%, risk=20%, overall=15%
    """
    composite = (
        market_score * 0.35
        + competition_score * 0.30
        + risk_score * 0.20
        + overall_score * 0.15
    )

    if composite >= 80:
        grade, color = "A", "green"
    elif composite >= 65:
        grade, color = "B", "blue"
    elif composite >= 50:
        grade, color = "C", "yellow"
    elif composite >= 35:
        grade, color = "D", "orange"
    else:
        grade, color = "F", "red"

    return {
        "composite_score": round(composite, 1),
        "grade": grade,
        "color": color,
        "verdict": verdict,
        "breakdown": {
            "market": round(market_score, 1),
            "competition": round(competition_score, 1),
            "risk": round(risk_score, 1),
            "overall": round(overall_score, 1),
        },
    }
