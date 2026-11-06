from __future__ import annotations

from copy import deepcopy
from typing import Any

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


def build_model(family: str, params: dict[str, Any]):
    p = deepcopy(params)
    if family == "SVR":
        return Pipeline([("scaler", StandardScaler()), ("model", SVR(**p))])
    if family == "KNN":
        return Pipeline([("scaler", StandardScaler()), ("model", KNeighborsRegressor(**p))])
    if family == "DT":
        return DecisionTreeRegressor(**p)
    if family == "RF":
        return RandomForestRegressor(**p)
    if family == "XGB":
        return XGBRegressor(**p)
    raise ValueError(f"Unknown model family: {family}")
