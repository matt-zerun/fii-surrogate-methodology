# Data and reproducibility boundaries

The institutional laboratory dataset is not distributed. This GitHub repository supports an **executable methodological demonstration** using fictional synthetic data and independent analysis of new, authorised canonical input tables.

Exact published metrics, response surfaces, fitted estimators, FII values and model rankings **cannot** be regenerated using the synthetic dataset. Neither the publication-derived repeated-partition tables nor the manuscript-specific figure reconstruction scripts from the complete Zenodo archive are included in this code-only GitHub distribution.

The public workflow begins with the validated schema in [`DATA_SCHEMA.md`](../DATA_SCHEMA.md). Source-specific extraction, provenance joins and harmonisation remain outside the software boundary. Input validation does not silently translate legacy source fields, convert units, impute measurements or discard malformed rows.

The main model runner **does** generate its own diagnostic scatterplot (`rmse_fii.png`) and auxiliary repeated-partition graphics from the data being analysed. Those operational plotting functions are retained. Results are written locally under `outputs/` and ignored by Git.

Fixed random seeds support repeatable execution in the recorded environment. Floating-point results may differ slightly by platform and dependency version, particularly for tree ensembles and boosting. For a comprehensive provenance description, see [`CODE_ONLY_SCOPE.md`](../CODE_ONLY_SCOPE.md).
