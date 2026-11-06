from __future__ import annotations

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from .models import build_model


def build_search(family: str, tuning_cfg: dict):
    family_cfg = tuning_cfg["families"][family]
    estimator = build_model(family, _baseline_params(family))
    common = {
        "estimator": estimator,
        "param_grid" if family_cfg["search"] == "grid" else "param_distributions": family_cfg["parameters"],
        "scoring": tuning_cfg["scoring"],
        "cv": int(tuning_cfg["cv"]),
        "n_jobs": 1,
        "return_train_score": True,
    }
    if family_cfg["search"] == "grid":
        return GridSearchCV(**common)
    return RandomizedSearchCV(
        **common,
        n_iter=int(tuning_cfg["randomized_n_iter"]),
        random_state=int(tuning_cfg["random_state"]),
    )


def _baseline_params(family: str) -> dict:
    if family == "SVR":
        return {"kernel":"rbf", "C":1.0, "gamma":"scale", "epsilon":0.1}
    if family == "KNN":
        return {"n_neighbors":5, "weights":"uniform", "p":2}
    if family == "DT":
        return {"random_state":42}
    if family == "RF":
        return {"random_state":42, "n_jobs":-1}
    if family == "XGB":
        return {"objective":"reg:squarederror", "random_state":42, "verbosity":0, "n_jobs":1}
    raise ValueError(f"Unknown family: {family}")
