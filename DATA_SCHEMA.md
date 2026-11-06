# FII surrogate-model workflow: canonical input schema

The public workflow accepts CSV, XLSX, XLSM, or XLS tables and starts after all
source-specific extraction and harmonisation are complete. Column names are
case-sensitive. Extra columns are ignored by the analysis engine.

## Columns

| Column | Unit / values | Type | Meaning | Required | Example | Quality control |
|---|---|---|---|---:|---|---|
| `observation_id` | — | string | Unique source observation/measurement | yes | `OBS-0001` | non-empty; unique |
| `material_id` | — | string | Stable physical sample or material-member identifier | yes | `MAT-0042` | non-empty |
| `lithology` | controlled category | string | Harmonised mineral-soil class | yes | `sand` | one of `sand`, `silt`, `clayey_soil`, `clay` |
| `water_content_pct` | % dry mass | numeric | Gravimetric water content, `100*m_w/m_s` | yes | `12.5` | finite; >= 0; frozen >=1% analysis filter is applied afterwards |
| `bulk_density_mg_m3` | Mg m^-3 | numeric | Measured wet bulk density | yes | `1.86` | finite; > 0; values >10 trigger a likely-unit error |
| `thermal_conductivity_w_mk` | W m^-1 K^-1 | numeric | Measured thermal conductivity | yes | `1.74` | finite; > 0; values >50 trigger a likely-unit error |
| `dry_density_mg_m3` | Mg m^-3 | numeric | Dry bulk density | no | `1.65` | positive when present; <= wet density; density identity checked |
| `particle_density_mg_m3` | Mg m^-3 | numeric | Particle density | no | `2.65` | positive when present; >= wet bulk density |

`Mg m^-3` and `g cm^-3` have identical numerical values. Do not supply
`kg m^-3` values without conversion.

## Density identity

When `dry_density_mg_m3` is present, the validator checks:

```text
bulk_density_mg_m3
    = dry_density_mg_m3 * (1 + water_content_pct / 100)
```

The final 2.0.0 tolerance is `0.02 Mg m^-3 + 2% of wet bulk density`. This
tolerance is configurable and accommodates rounded archival values; it is an
input-integrity check rather than an exclusion rule or transformation.

## Behaviour on invalid data

Malformed required records cause an actionable validation error containing the
column and example input row numbers. The validator does not silently coerce
bad strings to missing values, drop rows, translate aliases, convert units, or
impute observations. The historical minimum-water-content filter is applied
only after successful canonical validation and its row count is recorded in
`validation_report.json`.

## Template and demonstration

- Minimal template: `data/templates/fii_canonical_input_template.csv`
- Synthetic demonstration: `data/synthetic_example/fii_synthetic_example.csv`

The demonstration includes optional dry and particle densities to exercise
the shared consistency checks. Only water content and measured wet bulk
density are model predictors.
