from __future__ import annotations

import argparse
import json
from pathlib import Path

from sklearn.model_selection import train_test_split

from fii_surrogate.config import load_json
from fii_surrogate.constants import FEATURES, TARGET, WATER_CONTENT
from fii_surrogate.data_validation import validate_canonical_input
from fii_surrogate.io import load_table
from fii_surrogate.tuning import build_search


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=["SVR", "DT", "RF", "XGB", "KNN"], required=True)
    parser.add_argument("--data", default="data/synthetic_example/fii_synthetic_example.csv")
    parser.add_argument("--analysis-config", default="config/demo_analysis_config.json")
    parser.add_argument("--tuning-config", default="config/tuning_spaces.json")
    parser.add_argument("--output", default="outputs/demo/tuning")
    args = parser.parse_args()

    analysis_cfg = load_json(args.analysis_config)
    tuning_cfg = load_json(args.tuning_config)
    data, _ = validate_canonical_input(load_table(args.data))
    minimum_water = analysis_cfg.get("filtering", {}).get("minimum_water_content_pct")
    if minimum_water is not None:
        data = data.loc[data[WATER_CONTENT] >= float(minimum_water)].reset_index(drop=True)
    X = data.loc[:, list(FEATURES)].to_numpy(float)
    y = data[TARGET].to_numpy(float)
    X_train, _, y_train, _ = train_test_split(
        X, y,
        test_size=float(analysis_cfg["main_split"]["test_size"]),
        random_state=int(analysis_cfg["main_split"]["random_state"]),
    )
    search = build_search(args.family, tuning_cfg)
    search.fit(X_train, y_train)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    payload = {"family": args.family, "best_score": float(search.best_score_), "best_params": search.best_params_}
    (output / f"{args.family}_best_params.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
