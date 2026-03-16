from __future__ import annotations

from fastapi import APIRouter, HTTPException, UploadFile, File, status

from app.schemas.financial import FinancialReportResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction_service import extract_financial_metrics
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


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
        raw_text = extract_text_from_pdf(content)
        result = await extract_financial_metrics(raw_text, filename=file.filename or "report.pdf")
        return result
    except Exception as exc:
        logger.error(f"PDF analysis failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis error: {str(exc)}",
        )
