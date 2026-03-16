from __future__ import annotations

import re
from typing import Tuple

from app.agents.financial_analysis_agent import FinancialAnalysisAgent
from app.schemas.financial import FinancialReportResponse, FinancialMetrics
from app.services.pdf_service import _extract
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

_financial_agent = FinancialAnalysisAgent()

# Regex patterns to pull structured metrics from agent response text
_PATTERNS: dict[str, str] = {
    "revenue": r"[Rr]evenue[:\s]+\$?([\d,\.]+\s*(?:billion|million|B|M|K)?)",
    "revenue_growth_yoy": r"[Rr]evenue [Gg]rowth.*?([+-]?\d+\.?\d*\s*%)",
    "gross_margin": r"[Gg]ross [Mm]argin[:\s]+([+-]?\d+\.?\d*\s*%)",
    "ebitda": r"EBITDA[:\s]+\$?([\d,\.]+\s*(?:billion|million|B|M|K)?)",
    "ebitda_margin": r"EBITDA [Mm]argin[:\s]+([+-]?\d+\.?\d*\s*%)",
    "net_income": r"[Nn]et [Ii]ncome[:\s]+\$?([\d,\.]+\s*(?:billion|million|B|M|K)?)",
    "net_margin": r"[Nn]et [Mm]argin[:\s]+([+-]?\d+\.?\d*\s*%)",
    "eps": r"EPS[:\s]+\$?([\d,\.]+)",
    "current_ratio": r"[Cc]urrent [Rr]atio[:\s]+([\d,\.]+)",
    "debt_to_equity": r"[Dd]ebt.to.[Ee]quity[:\s]+([\d,\.]+)",
}


def _extract_pattern(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def _parse_highlights(analysis: str) -> tuple[list[str], list[str]]:
    """Heuristically extract highlights and risks from analysis text."""
    highlights, risks = [], []
    for line in analysis.split("\n"):
        line = line.strip().lstrip("•-123456789. ")
        if not line:
            continue
        lower = line.lower()
        if any(w in lower for w in ["strength", "positive", "grew", "increased", "record"]):
            highlights.append(line)
        elif any(w in lower for w in ["risk", "decline", "loss", "concern", "debt", "decreased"]):
            risks.append(line)
    return highlights[:5], risks[:5]


async def extract_financial_metrics(
    content: bytes, filename: str
) -> FinancialReportResponse:
    """Full pipeline: PDF bytes → text → LLM analysis → structured response."""
    text, page_count = _extract(content)

    analysis_text = await _financial_agent.run(text=text, filename=filename)

    metrics = FinancialMetrics(
        **{k: _extract_pattern(analysis_text, p) for k, p in _PATTERNS.items()}
    )
    highlights, risks = _parse_highlights(analysis_text)

    return FinancialReportResponse(
        filename=filename,
        page_count=page_count,
        metrics=metrics,
        analysis=analysis_text,
        key_highlights=highlights,
        key_risks=risks,
        raw_text_length=len(text),
    )
