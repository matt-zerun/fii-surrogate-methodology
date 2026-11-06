# Changelog

## 2.0.0 — 2026-09-16

- Introduced the shared canonical vocabulary and identifier model.
- Replaced source-column mapping with a documented canonical input contract.
- Added strict, actionable input validation and optional density-consistency checks.
- Added a single configuration-driven `run_analysis.py` entry point.
- Replaced committed demo outputs with an empty generated-output directory.
- Added a compact deterministic synthetic example, an input template,
  `DATA_SCHEMA.md`, `METHODS_MAPPING.md`, and `MIGRATION_NOTES.md`.
- Preserved all model configurations, random seeds, split settings, metrics,
  surface definitions, FII settings, and auxiliary repeated-partition logic.

## 1.0.0 — 2026-07-17

- Added the five model families and 25 fixed configurations reported in Supplementary Tables S2a–S2e.
- Added the documented hyperparameter search spaces and search procedures.
- Added a configurable implementation of MVR, normalised roughness, ORV and FII.
- Separated the canonical FII workflow from the auxiliary repeated-partition score.
- Added a fictional synthetic demonstration dataset.
- Added derived repeated-partition results used to regenerate the revised supplementary figures without releasing the restricted laboratory data.
- Added tests, dependency files and reproducibility documentation.
