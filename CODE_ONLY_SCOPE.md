# GitHub code-only distribution: scope and provenance

- **Scientific software release:** `fii-surrogate-methodology` version `2.0.0`.
- **Source of scientific code/configuration:** audited Zenodo release package `fii-surrogate-methodology-2.0.0.zip`.
- **Archival identifier:** https://doi.org/10.5281/zenodo.21414810 (concept DOI).
- **Related application:** https://doi.org/10.1038/s41598-026-65202-3.

## What is identical to the Zenodo archive?

Every file under `src/fii_surrogate/` and every file under `config/` is preserved byte-for-byte. The canonical synthetic data and canonical input template are likewise unchanged. There were **no changes to model families, hyperparameters, train/test fractions, seeds, response grids, FII weights, diagnostic definitions or repeated-partition procedures**.

## What was intentionally removed?

- `reference_outputs/derived/` (two non-observational **publication-specific** derived reference tables);
- `scripts/make_manuscript_repeated_partition_figures.py` and `scripts/make_figure_10_manuscript.py` (two publication-specific figure-generation scripts);
- Zenodo deposit metadata `.zenodo.json`, the old file checksum manifest and release packaging/checklist materials;
- the original release metadata test that depended on removed Zenodo deposit metadata (replaced with a GitHub code-only metadata/scope test).

## What was edited or added?

- Adapted `README.md`, `docs/DATA_AND_REPRODUCIBILITY.md`, and `METHODS_MAPPING.md` to the smaller public GitHub scope.
- Changed `CITATION.cff` `repository-code` to the GitHub source URL, retaining the software concept DOI and publication reference.
- Removed `Pillow` from dependency declarations, because its use was confined to a removed manuscript figure script. All other scientific dependencies and configurations remain intact.
- Added `.github/workflows/tests.yml` for CI and `tests/test_repository_metadata.py` for metadata/scope consistency.
- Added this `CODE_ONLY_SCOPE.md` and strengthened `.gitignore` to protect generated outputs and private data.

The historical `MIGRATION_NOTES.md` reflects the **full archival version 2.0.0**, not every GitHub-only exclusion.

## Not an exact recreation of the article

The real laboratory dataset is restricted, and the retained synthetic example is fictional. No claim is made that generated metrics, fitted models, surfaces or figures reproduce the published results. The code-only subset is designed for transparent inspection, learning, independent application and methodological audit.
