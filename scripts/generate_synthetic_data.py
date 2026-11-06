#!/usr/bin/env python3
"""Generate a small deterministic dataset for software demonstration only."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260717
LITHOLOGY_OFFSETS = {
    "sand": 0.00,
    "silt": -0.08,
    "clayey_soil": 0.08,
    "clay": -0.14,
}


def build_synthetic_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows: list[dict[str, object]] = []
    observation_number = 0
    for lithology, offset in LITHOLOGY_OFFSETS.items():
        for material_number in range(1, 21):
            material_shift = float(rng.normal(0.0, 0.035))
            for _state_number in range(1, 3):
                observation_number += 1
                water = float(rng.uniform(1.0, 29.0))
                wet_density = float(rng.uniform(1.25, 2.15))
                interaction = 0.10 * np.sin(water / 4.5) * (wet_density - 1.70)
                conductivity = (
                    0.25
                    + 1.35 * (1.0 - np.exp(-water / 7.5))
                    + 0.90 * (wet_density - 1.25)
                    + interaction
                    + offset
                    + material_shift
                    + float(rng.normal(0.0, 0.12 + 0.002 * water))
                )
                conductivity = float(np.clip(conductivity, 0.08, 3.6))
                dry_density = wet_density / (1.0 + water / 100.0)
                rows.append(
                    {
                        "observation_id": f"SYN-FII-OBS-{observation_number:04d}",
                        "material_id": (
                            f"SYN-FII-{lithology}-MAT-{material_number:03d}"
                        ),
                        "lithology": lithology,
                        "water_content_pct": round(water, 6),
                        "bulk_density_mg_m3": round(wet_density, 6),
                        "dry_density_mg_m3": round(dry_density, 6),
                        "particle_density_mg_m3": 2.65,
                        "thermal_conductivity_w_mk": round(conductivity, 6),
                    }
                )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="data/synthetic_example/fii_synthetic_example.csv",
        help="Destination CSV path.",
    )
    arguments = parser.parse_args()
    target = Path(arguments.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    table = build_synthetic_dataset()
    table.to_csv(target, index=False)
    print(f"Saved {len(table)} fictional observations to {target}")


if __name__ == "__main__":
    main()
