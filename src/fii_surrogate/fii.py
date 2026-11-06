from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class FIIComponents:
    mvr_water: float
    mvr_density: float
    mvr: float
    roughness_raw: float
    roughness_reference: float
    roughness_normalised: float
    orv: float
    fii: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def directional_gradients(Z: np.ndarray, water_values: np.ndarray, density_values: np.ndarray):
    Z = np.asarray(Z, dtype=float)
    water_values = np.asarray(water_values, dtype=float)
    density_values = np.asarray(density_values, dtype=float)
    expected = (len(water_values), len(density_values))
    if Z.shape != expected:
        raise ValueError(f"Z shape {Z.shape} does not match grid shape {expected}")
    dw = np.diff(water_values)
    dr = np.diff(density_values)
    if np.any(dw <= 0) or np.any(dr <= 0):
        raise ValueError("Predictor grid coordinates must be strictly increasing")
    grad_w = np.diff(Z, axis=0) / dw[:, None]
    grad_r = np.diff(Z, axis=1) / dr[None, :]
    return grad_w, grad_r


def monotonicity_violation_rate(grad_w: np.ndarray, grad_r: np.ndarray):
    mvr_w = float(np.mean(np.asarray(grad_w) < 0.0))
    mvr_r = float(np.mean(np.asarray(grad_r) < 0.0))
    return mvr_w, mvr_r, 0.5 * (mvr_w + mvr_r)


def raw_roughness(grad_w: np.ndarray, grad_r: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.asarray(grad_w) ** 2) + np.mean(np.asarray(grad_r) ** 2)))


def output_range_violation(Z: np.ndarray, lower: float, upper: float) -> float:
    Z = np.asarray(Z, dtype=float)
    return float(np.mean((Z < float(lower)) | (Z > float(upper))))


def compute_fii(
    Z: np.ndarray,
    water_values: np.ndarray,
    density_values: np.ndarray,
    roughness_reference: float,
    weights: dict[str, float],
    bounds: tuple[float, float],
) -> FIIComponents:
    if not np.isfinite(roughness_reference) or roughness_reference <= 0:
        raise ValueError("roughness_reference must be finite and positive")
    total_weight = sum(float(weights[k]) for k in ("mvr", "roughness", "orv"))
    if not np.isclose(total_weight, 1.0):
        raise ValueError("FII weights must sum to 1")
    grad_w, grad_r = directional_gradients(Z, water_values, density_values)
    mvr_w, mvr_r, mvr = monotonicity_violation_rate(grad_w, grad_r)
    rough = raw_roughness(grad_w, grad_r)
    rough_norm = rough / float(roughness_reference)
    orv = output_range_violation(Z, *bounds)
    fii = float(weights["mvr"] * mvr + weights["roughness"] * rough_norm + weights["orv"] * orv)
    return FIIComponents(mvr_w, mvr_r, mvr, rough, float(roughness_reference), rough_norm, orv, fii)
