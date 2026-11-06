from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MODEL_ORDER = ["DT", "RF", "SVR", "XGB", "kNN"]
MARKERS = {"baseline":"o", "tuned":"s", "variant_1":"^", "variant_2":"D", "variant_3":"P"}


def plot_rmse_fii(results: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    for family, group in results.groupby("family", sort=False):
        ax.scatter(group["overall_rmse"], group["fii"], label=family, s=48)
    ax.set_xlabel("Overall reconstruction RMSE")
    ax.set_ylabel("Functional Inconsistency Index (FII)")
    ax.legend(frameon=True)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_repeated_boxplots(results: pd.DataFrame, path: str | Path) -> None:
    results = results.copy()
    results["model"] = results["model"].replace({"KNN": "kNN"})
    order = [m for m in MODEL_ORDER if m in set(results["model"])]
    rmse = [results.loc[results["model"] == m, "heldout_rmse"].to_numpy() for m in order]
    aux = [results.loc[results["model"] == m, "auxiliary_score"].to_numpy() for m in order]
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.0))
    axes[0].boxplot(rmse, tick_labels=order)
    axes[1].boxplot(aux, tick_labels=order)
    axes[0].set_title("Held-out RMSE across repeated partitions")
    axes[1].set_title("Auxiliary behavioural score across repeated partitions")
    axes[0].set_ylabel(r"RMSE [W m$^{-1}$ K$^{-1}$]")
    axes[1].set_ylabel("Auxiliary behavioural score [–]")
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_supplement_repeated(results: pd.DataFrame, output_dir: str | Path) -> pd.DataFrame:
    results = results.copy()
    results["model"] = results["model"].replace({"KNN": "kNN"})
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    order = [m for m in MODEL_ORDER if m in set(results["model"])]
    summary = _summary_for_plots(results, order)

    x = np.arange(len(order))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.bar(x - width/2, summary["rmse_cv"], width, label="Held-out RMSE")
    ax.bar(x + width/2, summary["auxiliary_score_cv"], width, label="Auxiliary behavioural score")
    ax.set_xticks(x, order)
    ax.set_ylabel("Coefficient of variation across partitions [–]")
    ax.legend(frameon=True)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    _save(fig, output_dir / "Figure_S3.png")

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for model in order:
        subset = results.loc[results["model"] == model].sort_values("split")
        ax.plot(subset["split"], subset["auxiliary_score"], marker="o", markersize=3.5, linewidth=1.1, label=model)
    ax.set_xlabel("Partition index")
    ax.set_ylabel("Auxiliary behavioural score [–]")
    ax.legend(frameon=True)
    ax.grid(alpha=0.25)
    _save(fig, output_dir / "Figure_S4.png")

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for model in order:
        subset = results.loc[results["model"] == model]
        ax.scatter(subset["heldout_rmse"], subset["auxiliary_score"], s=26, alpha=0.75, label=model)
    ax.set_xlabel(r"Held-out test RMSE [W m$^{-1}$ K$^{-1}$]")
    ax.set_ylabel("Auxiliary behavioural score [–]")
    ax.legend(frameon=True)
    ax.grid(alpha=0.25)
    _save(fig, output_dir / "Figure_S5.png")

    summary.to_csv(output_dir / "Table_S4.csv", index=False)
    return summary


def _summary_for_plots(results: pd.DataFrame, order: list[str]) -> pd.DataFrame:
    grouped = results.groupby("model").agg(
        rmse_mean=("heldout_rmse", "mean"),
        rmse_sd=("heldout_rmse", "std"),
        auxiliary_score_mean=("auxiliary_score", "mean"),
        auxiliary_score_sd=("auxiliary_score", "std"),
    ).reindex(order)
    grouped["rmse_cv"] = grouped["rmse_sd"] / grouped["rmse_mean"]
    grouped["auxiliary_score_cv"] = grouped["auxiliary_score_sd"] / grouped["auxiliary_score_mean"]
    return grouped.reset_index()


def _save(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=600, bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)
