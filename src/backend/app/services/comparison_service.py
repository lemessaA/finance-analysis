from __future__ import annotations

from typing import Any


def compare_metrics(baseline: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    """
    Compare two sets of financial metrics and return delta analysis.
    Handles numeric values; marks non-numeric as 'N/A'.
    """
    results: dict[str, Any] = {}

    all_keys = set(baseline.keys()) | set(current.keys())
    for key in all_keys:
        b_val = baseline.get(key)
        c_val = current.get(key)

        try:
            b_num = float(str(b_val).replace("%", "").replace(",", "").strip())
            c_num = float(str(c_val).replace("%", "").replace(",", "").strip())
            delta = c_num - b_num
            pct_change = (delta / abs(b_num) * 100) if b_num != 0 else 0.0
            results[key] = {
                "baseline": b_val,
                "current": c_val,
                "delta": round(delta, 4),
                "pct_change": round(pct_change, 2),
                "direction": "up" if delta > 0 else ("down" if delta < 0 else "flat"),
            }
        except (TypeError, ValueError):
            results[key] = {"baseline": b_val, "current": c_val, "delta": "N/A"}

    return results
