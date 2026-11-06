from __future__ import annotations

import csv
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRECTORIES = {
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    "outputs",
}
FORBIDDEN_SUFFIXES = {
    ".docx",
    ".env",
    ".joblib",
    ".pkl",
    ".pickle",
    ".whl",
    ".xlsx",
    ".xls",
    ".zip",
}
TEXT_SUFFIXES = {".cff", ".csv", ".json", ".md", ".py", ".toml", ".txt", ".yml", ".yaml"}
ABSOLUTE_PATHS = {
    "workspace path": re.compile("/" + "workspace" + "/"),
    "user home path": re.compile(r"/(?:" + "home" + r"|Users)/[^/\s]+/"),
    "Windows user path": re.compile(r"[A-Za-z]:" + r"\\Users\\"),
}
REQUIRED_TEMPLATE_COLUMNS = [
    "observation_id",
    "material_id",
    "lithology",
    "water_content_pct",
    "bulk_density_mg_m3",
    "thermal_conductivity_w_mk",
]


def verify_release_boundary(root: Path = ROOT) -> dict[str, object]:
    failures: list[str] = []
    checked_files = 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(
            part in IGNORED_DIRECTORIES or part.endswith(".egg-info")
            for part in relative.parts
        ):
            continue
        if not path.is_file():
            continue
        checked_files += 1
        suffix = path.suffix.lower()
        if suffix in FORBIDDEN_SUFFIXES or path.name.lower().endswith(".tar.gz"):
            failures.append(f"forbidden source-release file: {relative}")
        if suffix in TEXT_SUFFIXES and path.name != "MANIFEST.sha256":
            content = path.read_text(encoding="utf-8", errors="ignore")
            for description, pattern in ABSOLUTE_PATHS.items():
                if pattern.search(content):
                    failures.append(f"{description} in public text: {relative}")

    template = root / "data/templates/fii_canonical_input_template.csv"
    synthetic = root / "data/synthetic_example/fii_synthetic_example.csv"
    for path in (template, synthetic):
        if not path.is_file():
            failures.append(f"missing canonical data file: {path.relative_to(root)}")
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            header = next(csv.reader(stream), [])
        missing = [column for column in REQUIRED_TEMPLATE_COLUMNS if column not in header]
        if missing:
            failures.append(
                f"canonical columns missing from {path.relative_to(root)}: {missing}"
            )

    outputs = root / "outputs"
    unexpected_outputs = [
        path.relative_to(root).as_posix()
        for path in outputs.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    if unexpected_outputs:
        failures.append(f"generated outputs included: {unexpected_outputs[:5]}")

    report = {
        "status": "passed" if not failures else "failed",
        "release_root": root.name,
        "checked_files": checked_files,
        "failures": failures,
    }
    return report


def main() -> None:
    report = verify_release_boundary()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
