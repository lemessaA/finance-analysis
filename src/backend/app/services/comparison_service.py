from __future__ import annotations

from typing import Any, Dict

from app.schemas.financial import FinancialMetrics

def compare_metrics(baseline: FinancialMetrics, current: FinancialMetrics) -> Dict[str, Any]:
    """
    Compare two sets of financial metrics and return delta analysis.
    Handles numeric values; marks non-numeric as 'N/A'.
    """
    results: Dict[str, Any] = {}

    baseline_dict = baseline.model_dump(exclude_none=True)
    current_dict = current.model_dump(exclude_none=True)
    
    all_keys = set(baseline_dict.keys()) | set(current_dict.keys())
    for key in all_keys:
        b_val = baseline_dict.get(key)
        c_val = current_dict.get(key)
        
        # Determine numeric variation
        try:
            b_num = float(str(b_val).replace("%", "").replace(",", "").replace("$", "").replace("B", "000000000").replace("M", "000000").strip()) if b_val else 0.0
            c_num = float(str(c_val).replace("%", "").replace(",", "").replace("$", "").replace("B", "000000000").replace("M", "000000").strip()) if c_val else 0.0
            
            delta = c_num - b_num
            pct_change = (delta / abs(b_num) * 100) if b_num != 0 else 0.0
            results[key] = {
                "baseline": b_val if b_val is not None else "Not disclosed",
                "current": c_val if c_val is not None else "Not disclosed",
                "delta": round(delta, 4) if bool(b_val and c_val) else "N/A",
                "pct_change": round(pct_change, 2) if bool(b_val and c_val) else "N/A",
                "direction": "up" if delta > 0 else ("down" if delta < 0 else "flat"),
            }
        except (TypeError, ValueError):
            results[key] = {
                "baseline": b_val if b_val is not None else "Not disclosed",
                "current": c_val if c_val is not None else "Not disclosed",
                "delta": "N/A",
                "pct_change": "N/A",
                "direction": "flat",
            }
            
    return results
