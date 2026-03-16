from __future__ import annotations

import httpx
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def scrape_url(url: str, timeout: int = 10) -> str:
    """Lightweight URL scraper that extracts plain text from HTML."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
            response = await client.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (AI Research Bot)"},
            )
            response.raise_for_status()
            # Strip basic HTML tags
            import re
            text = re.sub(r"<[^>]+>", " ", response.text)
            text = re.sub(r"\s+", " ", text).strip()
            return text[:5000]
    except Exception as exc:
        logger.warning(f"Scrape failed for {url}: {exc}")
        return ""
