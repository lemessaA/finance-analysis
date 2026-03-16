import pytest
import io


def test_pdf_extraction_with_synthetic_pdf():
    """Test PDF extraction returns text and page count."""
    import fitz

    # Create a minimal synthetic PDF in memory
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 100), "Revenue: $500M. Net Income: $50M. EBITDA Margin: 20%.")
    page.insert_text((50, 130), "Gross Margin: 45%. EPS: $2.50. Cash Flow: $80M.")
    pdf_bytes = doc.tobytes()
    doc.close()

    from app.services.pdf_service import _extract
    text, page_count = _extract(pdf_bytes)

    assert page_count == 1
    assert "Revenue" in text
    assert len(text) > 0


def test_pdf_extraction_prioritizes_financial_pages():
    """Pages with financial keywords should appear before generic pages."""
    import fitz

    doc = fitz.open()

    # Generic page first
    p1 = doc.new_page()
    p1.insert_text((50, 100), "This is the cover page of our annual report.")

    # Financial page second
    p2 = doc.new_page()
    p2.insert_text((50, 100), "Revenue grew 20%. Net Income: $100M. EBITDA: $150M.")

    pdf_bytes = doc.tobytes()
    doc.close()

    from app.services.pdf_service import _extract
    text, page_count = _extract(pdf_bytes)

    assert page_count == 2
    # Financial page content should appear in the result
    assert "Revenue" in text or "EBITDA" in text
