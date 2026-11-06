from __future__ import annotations

import numpy as np
from scipy.spatial import Delaunay


def regular_grid(X: np.ndarray, resolution: int = 40):
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[1] != 2:
        raise ValueError("X must have shape (n_samples, 2)")
    w = np.linspace(float(X[:, 0].min()), float(X[:, 0].max()), int(resolution))
    rho = np.linspace(float(X[:, 1].min()), float(X[:, 1].max()), int(resolution))
    W, R = np.meshgrid(w, rho, indexing="ij")
    grid = np.column_stack([W.ravel(), R.ravel()])
    return grid, w, rho, W.shape


def convex_hull_grid(X: np.ndarray, resolution: int = 150) -> np.ndarray:
    grid, _, _, _ = regular_grid(X, resolution)
    hull = Delaunay(np.asarray(X, dtype=float))
    return grid[hull.find_simplex(grid) >= 0]


def predict_surface(model, grid: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    return np.asarray(model.predict(grid), dtype=float).reshape(shape)
