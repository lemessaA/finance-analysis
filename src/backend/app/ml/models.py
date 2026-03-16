from __future__ import annotations

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator


class TimeSeriesModels:
    """Registry of available forecasting models."""

    @staticmethod
    def linear() -> LinearRegression:
        return LinearRegression()

    @staticmethod
    def polynomial(degree: int = 2) -> Pipeline:
        return Pipeline([
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("reg", LinearRegression()),
        ])

    @staticmethod
    def get(model_type: str) -> BaseEstimator:
        if model_type == "polynomial":
            return TimeSeriesModels.polynomial()
        return TimeSeriesModels.linear()
