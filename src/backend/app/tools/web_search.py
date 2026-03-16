from __future__ import annotations

from tavily import AsyncTavilyClient

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def tavily_search(query: str, max_results: int = 5) -> str:
    """Perform a Tavily web search and return formatted results string."""
    if not settings.TAVILY_API_KEY:
        logger.warning("TAVILY_API_KEY not set — returning empty search results")
        return "No search results available (TAVILY_API_KEY not configured)."

    try:
        client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
        response = await client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True,
        )

        parts: list[str] = []
        if response.get("answer"):
            parts.append(f"Summary: {response['answer']}\n")

        for i, result in enumerate(response.get("results", []), 1):
            parts.append(
                f"[{i}] {result.get('title', 'No title')}\n"
                f"    URL: {result.get('url', '')}\n"
                f"    {result.get('content', '')[:300]}\n"
            )

        return "\n".join(parts) if parts else "No results found."

    except Exception as exc:
        logger.error(f"Tavily search error: {exc}")
        return f"Search failed: {exc}"
