from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_json(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML or JSON configuration file."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    suffix = path.suffix.lower()
    with path.open("r", encoding="utf-8") as handle:
        if suffix in {".yml", ".yaml"}:
            payload = yaml.safe_load(handle)
        elif suffix == ".json":
            payload = json.load(handle)
        else:
            raise ValueError(
                f"Unsupported configuration format: {suffix}. Use YAML or JSON."
            )
    if not isinstance(payload, dict):
        raise ValueError("The configuration root must be a mapping/object.")
    return payload
