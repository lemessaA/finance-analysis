from __future__ import annotations

import io
from typing import Tuple

try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError as e:
    print(f"Warning: PyMuPDF not available: {e}")
    PDF_AVAILABLE = False
    fitz = None

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_text_from_pdf(content: bytes) -> tuple[str, int]:
    """Parse PDF bytes and return (text, page_count)."""
    if not PDF_AVAILABLE:
        logger.warning("PDF processing not available - returning empty content")
        return ("PDF processing not available. Please install PyMuPDF.", 0)
    return _extract(content)


def _extract(content: bytes) -> Tuple[str, int]:
    if not PDF_AVAILABLE:
        return ("PDF processing not available. Please install PyMuPDF.", 0)
        
    try:
        doc = fitz.open(stream=io.BytesIO(content), filetype="pdf")
        page_count = len(doc)

        financial_keywords = {
            "revenue", "income", "earnings", "cash flow", "ebitda",
            "profit", "loss", "margin", "assets", "liabilities", "equity",
        }
        priority_pages: list[str] = []
        other_pages: list[str] = []

        for i in range(page_count):
            text = doc[i].get_text("text")
            (priority_pages if any(k in text.lower() for k in financial_keywords) else other_pages).append(text)

        combined = "\n\n".join(priority_pages + other_pages)
        return combined[:50000], page_count

    except Exception as exc:
        logger.error(f"PDF extraction error: {exc}")
        raise
