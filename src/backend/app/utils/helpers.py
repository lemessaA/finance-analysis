from __future__ import annotations

import re
from datetime import datetime
from typing import Any


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text)


def truncate_text(text: str, max_chars: int = 10000) -> str:
    """Truncate text to max_chars, appending ellipsis if truncated."""
    return text[:max_chars] + "..." if len(text) > max_chars else text


def format_currency(value: float, currency: str = "USD") -> str:
    """Format a float as a currency string."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B {currency}"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M {currency}"
    elif value >= 1_000:
        return f"${value / 1_000:.2f}K {currency}"
    return f"${value:.2f} {currency}"


def utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Division that returns default instead of raising ZeroDivisionError."""
    return numerator / denominator if denominator != 0 else default
