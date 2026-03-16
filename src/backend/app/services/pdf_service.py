from __future__ import annotations

import io
from typing import Tuple

import fitz  # PyMuPDF

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_text_from_pdf(content: bytes) -> tuple[str, int]:
    """Parse PDF bytes and return (text, page_count)."""
    return _extract(content)


def _extract(content: bytes) -> Tuple[str, int]:
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
        return combined[:15000], page_count

    except Exception as exc:
        logger.error(f"PDF extraction error: {exc}")
        raise
