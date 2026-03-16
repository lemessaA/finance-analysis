from __future__ import annotations

import json
from pathlib import Path

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def load_json_file(path: str) -> dict:
    """Load and parse a JSON file from disk."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text_file(path: str, max_chars: int = 20000) -> str:
    """Load a plain text file, capped at max_chars."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = p.read_text(encoding="utf-8")
    return text[:max_chars]


def list_directory(path: str, pattern: str = "*") -> list[str]:
    """List files matching a glob pattern inside a directory."""
    p = Path(path)
    return [str(f) for f in p.glob(pattern) if f.is_file()]
