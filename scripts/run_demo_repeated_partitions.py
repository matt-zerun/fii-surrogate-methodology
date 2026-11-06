from __future__ import annotations

import argparse
from pathlib import Path

from fii_surrogate.config import load_json
from fii_surrogate.constants import WATER_CONTENT
from fii_surrogate.data_validation import validate_canonical_input
from fii_surrogate.io import load_table
from fii_surrogate.plots import plot_repeated_boxplots, plot_supplement_repeated
from fii_surrogate.repeated import run_repeated_partitions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/synthetic_example/fii_synthetic_example.csv")
    parser.add_argument("--analysis-config", default="config/demo_analysis_config.json")
    parser.add_argument("--repeated-config", default="config/repeated_partition_config.json")
    parser.add_argument("--output", default="outputs/demo/repeated")
    parser.add_argument("--max-splits", type=int, default=3, help="Use 30 for the complete experiment.")
    args = parser.parse_args()

    analysis_cfg = load_json(args.analysis_config)
    repeated_cfg = load_json(args.repeated_config)
    data, _ = validate_canonical_input(load_table(args.data))
    minimum_water = analysis_cfg.get("filtering", {}).get("minimum_water_content_pct")
    if minimum_water is not None:
        data = data.loc[data[WATER_CONTENT] >= float(minimum_water)].reset_index(drop=True)
    results, summary = run_repeated_partitions(data, repeated_cfg, args.output, args.max_splits)
    plot_repeated_boxplots(results, Path(args.output) / "demo_repeated_partition_boxplots.png")
    plot_supplement_repeated(results, Path(args.output) / "supplement_style")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
