from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Tuple


def prepare_time_series(
    periods: list[str], values: list[float]
) -> Tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Convert raw period strings and values into numeric feature matrix.
    Returns (X, y, cleaned_periods).
    """
    df = pd.DataFrame({"period": periods, "value": values})
    df = df.dropna()
    df["t"] = np.arange(len(df))

    # Lag features
    df["lag1"] = df["value"].shift(1).fillna(method="bfill")
    df["lag2"] = df["value"].shift(2).fillna(method="bfill")

    # Rolling mean
    df["rolling_mean_2"] = df["value"].rolling(2, min_periods=1).mean()

    X = df[["t", "lag1", "lag2", "rolling_mean_2"]].values
    y = df["value"].values

    return X, y, df["period"].tolist()


def compute_growth_rates(values: list[float]) -> list[float]:
    """Compute period-over-period growth rates as percentages."""
    rates = []
    for i in range(1, len(values)):
        if values[i - 1] != 0:
            rates.append((values[i] - values[i - 1]) / abs(values[i - 1]) * 100)
        else:
            rates.append(0.0)
    return rates


def detect_trend(values: list[float]) -> str:
    """Classify trend direction based on linear slope."""
    if len(values) < 2:
        return "neutral"
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    rel_slope = slope / (abs(np.mean(values)) + 1e-9)
    if rel_slope > 0.02:
        return "upward"
    elif rel_slope < -0.02:
        return "downward"
    return "stable"
