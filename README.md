# Functional Inconsistency Index (FII)

**Surrogate-model diagnostic workflow · Python · v2.0.0 (GitHub code-only distribution)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21414810.svg)](https://doi.org/10.5281/zenodo.21414810)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

FII is an open-source Python workflow for post hoc comparison of **predictive accuracy** and **functional behaviour** in two-input machine-learning surrogate models. It evaluates model response surfaces using a common prediction grid, alongside reconstruction and held-out prediction metrics.

The software was used in the related [*Scientific Reports* study](https://doi.org/10.1038/s41598-026-65202-3). The publication is **related context**, not a replacement for the software documentation.

## Method at a glance

```text
canonical thermal-conductivity observations
    → validation and predefined filtering
    → 25 fixed configurations in five regression families
    → reconstruction and held-out predictive metrics
    → common-grid response surfaces
    → monotonicity, roughness and output-range diagnostics
    → Functional Inconsistency Index (FII)
```

The five families are decision trees (DT), random forests (RF), support vector regression (SVR), extreme gradient boosting (XGB) and k-nearest neighbours (kNN). Hyperparameter configurations, main split, random seeds, grid definition and diagnostic settings are retained from the archived scientific release.

The index combines three case-dependent diagnostics:

\[ \mathrm{FII} = 0.4\,\mathrm{MVR} + 0.4\,\mathrm{Rough}_{norm} + 0.2\,\mathrm{ORV} \]

FII is **not** a physical-validity test, an uncertainty estimator, or a general guarantee of suitability. Its interpretation requires fixed and explicit domain, units, constraints, output bounds, roughness reference and weights. The separate *auxiliary repeated-partition score* is **not the FII**.

## Install

Requires **Python 3.10 or newer**. From the repository root:

```bash
python -m pip install -e ".[test]"
```

A tested reference set of package versions is recorded in `requirements-lock.txt`. `environment.yml` documents the archived Conda environment; it specifies Python 3.13. The software also supports installation in a suitable independent environment (including Python 3.11 if compatible dependencies are available).

## Run the synthetic demonstration

```bash
python run_analysis.py --config config/example_config.yml
```

Or use the installed console entry point:

```bash
fii-surrogate-run --config config/example_config.yml
```

The default configuration runs **25 fixed model configurations** and **3 auxiliary repeated train/test partitions** using a deterministic, entirely fictional dataset. Results are generated under `outputs/synthetic_example/` (ignored by Git). To run 30 repeated partitions, change `repeated_partitions.max_splits` in the YAML configuration from `3` to `30`.

For authorised analytical data, prepare a table in the canonical format described in [`DATA_SCHEMA.md`](DATA_SCHEMA.md), then copy and adapt `config/example_config.yml`. No implicit unit conversion, column renaming, imputation or silent row removal occurs during canonical validation.

## Outputs

Typical outputs include `validation_report.json`, `main/model_results.csv`, `main/surface_predictions.csv`, `main/rmse_fii.png` and the optional repeated-partition tables and figures. These are **generated locally** and are not committed to the repository.

Selected focused commands:

```bash
python scripts/run_demo_analysis.py
python scripts/run_demo_repeated_partitions.py --max-splits 30
python scripts/run_tuning.py --family SVR
python -m pytest -q
python scripts/verify_release_boundary.py
```

Full hyperparameter searches can take considerably longer than the demonstration.

## Repository contents

| Path | Purpose |
| --- | --- |
| `src/fii_surrogate/` | Scientific implementation, validation, metrics, plotting and CLI |
| `config/` | Frozen model definitions, tuning spaces and run settings |
| `data/synthetic_example/` | Fictional deterministic demonstration dataset |
| `data/templates/` | Blank canonical-input template |
| `scripts/` | Data generator, demonstration, tuning and release-boundary validation |
| `tests/` | Unit, smoke, integration and metadata tests |
| `docs/` | Methodology and reproducibility guidance |
| `METHODS_MAPPING.md` | Correspondence between methodology, functions and outputs |
| `CODE_ONLY_SCOPE.md` | Scope, exclusions and comparison with Zenodo archive |

## Reproducibility and data boundary

No real laboratory observations, source-specific identifier mappings, fitted reference models or publication-specific figure datasets are included. The synthetic dataset **cannot reproduce the published numerical results**. This is an executable methodological demonstration, not a complete replay of the original restricted-data experiment.

This GitHub **code-only subset** intentionally excludes the two derived reference tables and the two manuscript-specific figure scripts distributed in the archival Zenodo version. The plotting code used by the **scientific CLI remains included** because it is an operational dependency. The underlying scientific Python modules and the five files in `config/` are unchanged from the Zenodo 2.0.0 archive. See [`CODE_ONLY_SCOPE.md`](CODE_ONLY_SCOPE.md).

## Citation and rights

Software: **Mateusz Żeruń**, [Functional Inconsistency Index: surrogate-model diagnostic workflow](https://doi.org/10.5281/zenodo.21414810), Zenodo concept DOI **10.5281/zenodo.21414810**. Citation metadata are in [`CITATION.cff`](CITATION.cff).

Related article: Żeruń, M. (2026), [*Separating predictive accuracy from functional behaviour in machine-learning surrogate models for geoengineering applications*](https://doi.org/10.1038/s41598-026-65202-3), *Scientific Reports*.

MIT License, copyright © 2026 Mateusz Żeruń. Institutional affiliation: Polish Geological Institute – National Research Institute (PGI-NRI).
