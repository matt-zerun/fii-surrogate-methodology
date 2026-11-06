from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from .analysis import run_fixed_configurations
from .config import load_config, load_json
from .constants import WATER_CONTENT
from .data_validation import InputValidationError, validate_canonical_input
from .io import load_table
from .plots import plot_repeated_boxplots, plot_rmse_fii, plot_supplement_repeated
from .repeated import run_repeated_partitions


def _repository_path(raw: str, repository_root: Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repository_root / path


def _workflow_root(config_path: Path) -> Path:
    """Resolve relative input/output paths from the active checkout.

    This keeps the source-archive command usable after a normal package
    installation: a config run from a repository checkout should still use
    that checkout's ``data`` and ``outputs`` directories rather than the
    installed package directory.
    """
    current = Path.cwd()
    if (current / "config").is_dir():
        return current
    if config_path.parent.name == "config":
        return config_path.parent.parent
    return current


def run_from_config(config_path: str | Path) -> dict[str, Path]:
    config_path = Path(config_path).resolve()
    repository_root = _workflow_root(config_path)
    cfg = load_config(config_path)

    input_path = _repository_path(str(cfg["input"]["path"]), repository_root)
    output_root = _repository_path(str(cfg["output"]["directory"]), repository_root)
    validation_cfg = cfg.get("validation", {})
    data, report = validate_canonical_input(
        load_table(input_path),
        minimum_observations=int(validation_cfg.get("minimum_observations", 20)),
        density_identity_abs_tolerance_mg_m3=float(
            validation_cfg.get("density_identity_abs_tolerance_mg_m3", 0.02)
        ),
        density_identity_rel_tolerance=float(
            validation_cfg.get("density_identity_rel_tolerance", 0.02)
        ),
    )

    filtering_cfg = cfg.get("filtering", {})
    minimum_water_content = filtering_cfg.get("minimum_water_content_pct")
    n_before_filter = len(data)
    if minimum_water_content is not None:
        data = data.loc[
            data[WATER_CONTENT] >= float(minimum_water_content)
        ].reset_index(drop=True)
    if len(data) < int(validation_cfg.get("minimum_observations", 20)):
        raise InputValidationError(
            "Too few observations remain after the configured water-content filter: "
            f"{len(data)}."
        )

    output_root.mkdir(parents=True, exist_ok=True)
    validation_payload = {
        "canonical_input": asdict(report),
        "publication_filter": {
            "minimum_water_content_pct": minimum_water_content,
            "n_before_filter": n_before_filter,
            "n_after_filter": len(data),
            "removed_observations": n_before_filter - len(data),
        },
    }
    validation_path = output_root / "validation_report.json"
    validation_path.write_text(
        json.dumps(validation_payload, indent=2), encoding="utf-8"
    )

    manifest_path = _repository_path(str(cfg["models"]["manifest"]), repository_root)
    main_cfg = {
        "main_split": cfg["main_split"],
        "surface": cfg["surface"],
        "fii": cfg["fii"],
    }
    main_output = output_root / "main"
    results, _ = run_fixed_configurations(
        data,
        load_json(manifest_path)["models"],
        main_cfg,
        main_output,
    )
    plot_rmse_fii(results, main_output / "rmse_fii.png")

    outputs: dict[str, Path] = {
        "validation": validation_path,
        "main": main_output,
    }
    repeated_cfg = cfg.get("repeated_partitions", {})
    if bool(repeated_cfg.get("enabled", False)):
        repeated_config_path = _repository_path(
            str(repeated_cfg["config"]), repository_root
        )
        repeated_output = output_root / "repeated_partitions"
        repeated_results, _ = run_repeated_partitions(
            data,
            load_json(repeated_config_path),
            repeated_output,
            max_splits=repeated_cfg.get("max_splits"),
        )
        plot_repeated_boxplots(
            repeated_results,
            repeated_output / "repeated_partition_boxplots.png",
        )
        plot_supplement_repeated(
            repeated_results, repeated_output / "supplement_style"
        )
        outputs["repeated_partitions"] = repeated_output
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the FII surrogate-model workflow from canonical input."
        )
    )
    parser.add_argument(
        "--config", default="config/example_config.yml", help="YAML or JSON run configuration."
    )
    arguments = parser.parse_args()
    try:
        outputs = run_from_config(arguments.config)
    except (InputValidationError, FileNotFoundError, KeyError, ValueError) as error:
        raise SystemExit(f"Input/configuration error: {error}") from None
    for name, path in outputs.items():
        print(f"{name}: {path.resolve()}")
