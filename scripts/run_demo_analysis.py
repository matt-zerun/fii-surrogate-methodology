from __future__ import annotations

import argparse
from pathlib import Path

from fii_surrogate.analysis import run_fixed_configurations
from fii_surrogate.config import load_json
from fii_surrogate.constants import WATER_CONTENT
from fii_surrogate.data_validation import validate_canonical_input
from fii_surrogate.io import load_table
from fii_surrogate.plots import plot_rmse_fii


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/synthetic_example/fii_synthetic_example.csv")
    parser.add_argument("--config", default="config/demo_analysis_config.json")
    parser.add_argument("--manifest", default="config/model_manifest.json")
    parser.add_argument("--output", default="outputs/demo/main")
    args = parser.parse_args()

    cfg = load_json(args.config)
    manifest = load_json(args.manifest)
    data, _ = validate_canonical_input(load_table(args.data))
    minimum_water = cfg.get("filtering", {}).get("minimum_water_content_pct")
    if minimum_water is not None:
        data = data.loc[data[WATER_CONTENT] >= float(minimum_water)].reset_index(drop=True)
    results, _ = run_fixed_configurations(data, manifest["models"], cfg, args.output)
    plot_rmse_fii(results, Path(args.output) / "demo_rmse_fii.png")
    print(results[["model_id", "overall_rmse", "heldout_rmse", "fii"]].to_string(index=False))


if __name__ == "__main__":
    main()
