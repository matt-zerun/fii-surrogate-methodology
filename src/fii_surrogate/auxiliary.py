from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class AuxiliaryComponents:
    decrease_rate: float
    flattened_roughness: float
    output_range_violation: float
    auxiliary_score: float

    def to_dict(self):
        return asdict(self)


def compute_auxiliary_score(grid: np.ndarray, predictions: np.ndarray, bounds=(0.2, 5.0)) -> AuxiliaryComponents:
    grid = np.asarray(grid, dtype=float)
    predictions = np.asarray(predictions, dtype=float)
    if grid.ndim != 2 or grid.shape[1] != 2 or len(grid) != len(predictions):
        raise ValueError("grid and predictions have incompatible shapes")

    order = np.argsort(grid[:, 0], kind="mergesort")
    ordered_predictions = predictions[order]
    decrease_rate = float(np.mean(np.diff(ordered_predictions) < 0.0))
    flattened_roughness = float(np.std(np.gradient(predictions)))
    lower, upper = map(float, bounds)
    orv = float(np.mean((predictions < lower) | (predictions > upper)))
    score = float(np.mean([decrease_rate, flattened_roughness, orv]))
    return AuxiliaryComponents(decrease_rate, flattened_roughness, orv, score)
