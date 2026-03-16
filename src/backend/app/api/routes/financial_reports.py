from __future__ import annotations

import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException, UploadFile, File, status

from app.schemas.financial import FinancialReportResponse, ComparisonRequest, ComparisonResponse
from app.services.extraction_service import extract_financial_metrics
from app.services.comparison_service import compare_metrics
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

# Simple in-memory store for demonstration. In production, use a Database.
_REPORT_STORE: Dict[str, FinancialReportResponse] = {}

@router.post(
    "/analyze",
    response_model=FinancialReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze a financial report PDF",
    description=(
        "Upload a financial PDF (annual report, 10-K, etc.). The system parses the "
        "document with PyMuPDF, then extracts key metrics via LLM structured output."
    ),
)
async def analyze_financial_report(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are supported.",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds 20 MB limit.",
        )

    logger.info(f"Processing PDF: {file.filename} ({len(content) / 1024:.1f} KB)")
    try:
        result = await extract_financial_metrics(content, filename=file.filename or "report.pdf")
        
        # Store for comparison
        report_id = str(uuid.uuid4())
        _REPORT_STORE[report_id] = result
        
        # Return the report ID in the filename field so the frontend can reference it
        result.filename = report_id
        
        return result
    except Exception as exc:
        logger.error(f"PDF analysis failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis error: {str(exc)}",
        )


@router.post(
    "/compare",
    response_model=ComparisonResponse,
    status_code=status.HTTP_200_OK,
    summary="Compare two analyzed financial reports",
    description="Compare two previously uploaded reports using their report IDs.",
)
async def compare_reports(request: ComparisonRequest):
    baseline_report = _REPORT_STORE.get(request.baseline_report_id)
    current_report = _REPORT_STORE.get(request.current_report_id)

    if not baseline_report:
        raise HTTPException(status_code=404, detail="Baseline report not found")
    if not current_report:
        raise HTTPException(status_code=404, detail="Current report not found")

    comparison_results = compare_metrics(baseline_report.metrics, current_report.metrics)

    return ComparisonResponse(
        baseline_id=request.baseline_report_id,
        current_id=request.current_report_id,
        comparison_results=comparison_results,
    )
