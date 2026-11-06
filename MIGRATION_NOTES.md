# Migration from fii-surrogate-methodology 1.0.0

> Historical document for the complete Zenodo 2.0.0 archive. The GitHub code-only
> distribution excludes the publication-specific derived tables and manuscript
> figure-generation scripts mentioned below; see `CODE_ONLY_SCOPE.md`.

Version 2.0.0 changes the public architecture and schema, not the scientific
experiment.

## Paths and entry points

| Old path / command | New path / command | Reason |
|---|---|---|
| `scripts/run_demo_analysis.py` plus separate repeated command | `python run_analysis.py --config config/example_config.yml` | one complete public entry point |
| `data/synthetic_demo.csv` | `data/synthetic_example/fii_synthetic_example.csv` | common repository layout and smaller demonstration |
| no input template | `data/templates/fii_canonical_input_template.csv` | user-preparable canonical input |
| `data/derived/` | `reference_outputs/derived/` | distinguish non-observational reference results from input data |
| committed `outputs/demo/` and `outputs/manuscript_derived/` | empty `outputs/` with `.gitkeep` | generated artefacts are reproducible and should not inflate source releases |
| `docs/MANUSCRIPT_ALIGNMENT.md` | `METHODS_MAPPING.md` | content-based methods-to-code documentation |

The focused scripts remain available for users who need a single analysis
stage. Their default input paths now target the canonical synthetic file.

## Column names

| Version 1.0.0 | Canonical 2.0 name | Note |
|---|---|---|
| `sample_id` | `observation_id` plus `material_id` | old demo ID did not distinguish a record from its material |
| `water_content_pct` (input), `water_content` (internal/output) | `water_content_pct` | one public name |
| `bulk_density_g_cm3` (input), `bulk_density` (internal/output) | `bulk_density_mg_m3` | numerical values are unchanged because the units are equivalent |
| `thermal_conductivity_w_mk` (input), `thermal_conductivity` (internal) | `thermal_conductivity_w_mk` | one public name |
| `prediction` | `predicted_thermal_conductivity_w_mk` | explicit predicted quantity and unit |
| absent | `lithology` | shared controlled vocabulary and audit field; not an FII-workflow predictor |

Source-specific aliases are intentionally not converted inside the public
workflow. Convert authorised legacy tables before calling the canonical
runner.

## Removed from the public release

- generated demo output tables and figures;
- generated related-publication figure files (stable scripts and small derived inputs remain);
- the obsolete checksum manifest from the unmodified 1.0.0 archive.

The original uploaded archive is retained separately and its history is
described in the external public-release refactor report.

## Frozen scientific content

Unchanged: all 25 fixed model configurations, tuning spaces, random seeds,
train/test fraction, predictive metrics, response-grid construction, FII
definition and weights, output bounds, and auxiliary repeated-partition
procedure. Numerical regression is evaluated after a one-to-one semantic
rename of the original valid synthetic input.
