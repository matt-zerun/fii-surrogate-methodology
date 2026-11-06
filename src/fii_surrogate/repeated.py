from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from .auxiliary import compute_auxiliary_score
from .constants import FEATURES, TARGET
from .metrics import regression_metrics
from .models import build_model
from .surfaces import convex_hull_grid


def run_repeated_partitions(
    data: pd.DataFrame,
    repeated_cfg: dict,
    output_dir: str | Path,
    max_splits: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    X = data.loc[:, list(FEATURES)].to_numpy(float)
    y = data[TARGET].to_numpy(float)
    seeds = list(repeated_cfg["seeds"])
    if max_splits is not None:
        seeds = seeds[: int(max_splits)]

    rows: list[dict] = []
    for split_index, seed in enumerate(seeds):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=float(repeated_cfg["test_size"]), random_state=int(seed)
        )
        grid = convex_hull_grid(X_train, int(repeated_cfg["grid_resolution"]))

        for entry in repeated_cfg["models"]:
            model = build_model(entry["family"], entry["params"])
            model.fit(X_train, y_train)
            heldout = regression_metrics(y_test, model.predict(X_test))
            predictions = model.predict(grid)
            aux = compute_auxiliary_score(grid, predictions, repeated_cfg["output_bounds"])
            rows.append({
                "split": split_index,
                "seed": int(seed),
                "model": "kNN" if entry["family"] == "KNN" else entry["family"],
                "heldout_rmse": heldout["rmse"],
                **aux.to_dict(),
            })

    results = pd.DataFrame(rows)
    summary = summarise_repeated(results)
    results.to_csv(output_dir / "repeated_partition_results.csv", index=False)
    summary.to_csv(output_dir / "repeated_partition_summary.csv", index=False)
    return results, summary


def summarise_repeated(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model, group in results.groupby("model", sort=False):
        rmse_mean = float(group["heldout_rmse"].mean())
        aux_mean = float(group["auxiliary_score"].mean())
        rows.append({
            "model": model,
            "rmse_mean": rmse_mean,
            "rmse_sd": float(group["heldout_rmse"].std(ddof=1)),
            "rmse_cv": float(group["heldout_rmse"].std(ddof=1) / rmse_mean),
            "auxiliary_score_mean": aux_mean,
            "auxiliary_score_sd": float(group["auxiliary_score"].std(ddof=1)),
            "auxiliary_score_cv": float(group["auxiliary_score"].std(ddof=1) / aux_mean),
        })
    return pd.DataFrame(rows)
