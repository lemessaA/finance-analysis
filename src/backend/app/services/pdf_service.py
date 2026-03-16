from __future__ import annotations

import io
from typing import Tuple

import fitz  # PyMuPDF

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_text_from_pdf(content: bytes) -> Tuple[str, int]:
    """
    Parse a PDF from raw bytes and return (full_text, page_count).

    Strategy:
    - Extract text from every page
    - Prioritize pages containing financial keywords
    - Return concatenated text (max 15K chars) + page count
    """
    try:
        doc = fitz.open(stream=io.BytesIO(content), filetype="pdf")
        page_count = len(doc)
        logger.info(f"PDF opened: {page_count} pages")

        financial_keywords = {
            "revenue", "income", "earnings", "cash flow", "ebitda",
            "profit", "loss", "margin", "assets", "liabilities",
            "equity", "balance sheet", "financial statements",
        }

        priority_pages: list[str] = []
        other_pages: list[str] = []

        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text("text")  # type: ignore[arg-type]
            lower = text.lower()

            if any(kw in lower for kw in financial_keywords):
                priority_pages.append(text)
            else:
                other_pages.append(text)

        # Combine: financial pages first, then others, cap at 15K chars
        combined = "\n\n".join(priority_pages + other_pages)
        return combined[:15000], page_count

    except Exception as exc:
        logger.error(f"PDF extraction failed: {exc}")
        raise


# Convenience wrapper matching the route's call signature
def extract_text_from_pdf(content: bytes):  # noqa: F811
    text, pages = _extract(content)
    return text, pages


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
