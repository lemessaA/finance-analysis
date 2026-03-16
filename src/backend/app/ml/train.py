from __future__ import annotations

import numpy as np
from sklearn.metrics import r2_score

from app.ml.models import TimeSeriesModels
from app.ml.evaluation import evaluate_model
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def train_forecasting_model(
    X: np.ndarray, y: np.ndarray, model_type: str = "auto"
) -> tuple:
    """
    Train a model, returns (fitted_model, model_name, r2_score).
    When model_type='auto', selects the best between linear and polynomial.
    """
    if model_type == "auto":
        lin = TimeSeriesModels.linear()
        lin.fit(X, y)
        lin_r2 = r2_score(y, lin.predict(X))

        poly = TimeSeriesModels.polynomial()
        poly.fit(X, y)
        poly_r2 = r2_score(y, poly.predict(X))

        if poly_r2 > lin_r2 + 0.05:
            logger.info(f"Auto-selected: Polynomial (R²={poly_r2:.3f} vs Linear R²={lin_r2:.3f})")
            return poly, "Polynomial Regression", poly_r2

        logger.info(f"Auto-selected: Linear (R²={lin_r2:.3f})")
        return lin, "Linear Regression", lin_r2

    model = TimeSeriesModels.get(model_type)
    model.fit(X, y)
    r2 = r2_score(y, model.predict(X))
    name = "Polynomial Regression" if model_type == "polynomial" else "Linear Regression"
    return model, name, r2
