from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .constants import (
    BULK_DENSITY,
    FEATURES,
    PREDICTED_THERMAL_CONDUCTIVITY,
    TARGET,
    WATER_CONTENT,
)
from .fii import compute_fii
from .metrics import regression_metrics
from .models import build_model
from .surfaces import predict_surface, regular_grid


def run_fixed_configurations(
    data: pd.DataFrame,
    model_entries: Iterable[dict],
    analysis_cfg: dict,
    output_dir: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    X = data.loc[:, list(FEATURES)].to_numpy(float)
    y = data[TARGET].to_numpy(float)
    split_cfg = analysis_cfg["main_split"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=float(split_cfg["test_size"]),
        random_state=int(split_cfg["random_state"]),
    )

    grid, water_values, density_values, shape = regular_grid(
        X, int(analysis_cfg["surface"]["grid_resolution"])
    )
    fii_cfg = analysis_cfg["fii"]
    rough_ref = float(fii_cfg["roughness_reference_value"])
    weights = {key: float(value) for key, value in fii_cfg["weights"].items()}
    bounds = tuple(float(value) for value in fii_cfg["output_bounds"])

    rows: list[dict] = []
    surface_rows: list[pd.DataFrame] = []

    for entry in model_entries:
        model = build_model(entry["family"], entry["params"])
        model.fit(X_train, y_train)

        overall = regression_metrics(y, model.predict(X))
        heldout = regression_metrics(y_test, model.predict(X_test))
        Z = predict_surface(model, grid, shape)
        comp = compute_fii(Z, water_values, density_values, rough_ref, weights, bounds)

        row = {
            "model_id": entry["id"],
            "family": entry["family"],
            "configuration": entry["label"],
            **{f"overall_{k}": v for k, v in overall.items()},
            **{f"heldout_{k}": v for k, v in heldout.items()},
            **comp.to_dict(),
        }
        rows.append(row)

        surface_rows.append(pd.DataFrame({
            "model_id": entry["id"],
            WATER_CONTENT: grid[:, 0],
            BULK_DENSITY: grid[:, 1],
            PREDICTED_THERMAL_CONDUCTIVITY: Z.ravel(),
        }))

    results = pd.DataFrame(rows)
    surfaces = pd.concat(surface_rows, ignore_index=True)
    results.to_csv(output_dir / "model_results.csv", index=False)
    surfaces.to_csv(output_dir / "surface_predictions.csv", index=False)
    return results, surfaces
