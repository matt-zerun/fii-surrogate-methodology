# FII workflow methods-to-code mapping

| Method or analysis stage | Module, function, or script | Main output |
|---|---|---|
| Canonical analytical input and quality control | `fii_surrogate.data_validation.validate_canonical_input` | `validation_report.json` and validated in-memory table |
| Historical water-content exclusion | `fii_surrogate.cli.run_from_config` using `filtering.minimum_water_content_pct` | retained observation set and filter counts |
| Fixed model definitions | `fii_surrogate.models.build_model`; `config/model_manifest.json` | 25 fitted candidate configurations |
| Main train/test partition | `fii_surrogate.analysis.run_fixed_configurations` | deterministic training and held-out subsets |
| Overall reconstruction and held-out prediction metrics | `fii_surrogate.metrics.regression_metrics`; `run_fixed_configurations` | `main/model_results.csv` |
| Common-grid response-surface reconstruction | `fii_surrogate.surfaces.regular_grid`; `predict_surface` | `main/surface_predictions.csv` |
| MVR, roughness, ORV, and FII | `fii_surrogate.fii.compute_fii` | component columns in `main/model_results.csv` |
| Accuracy-versus-behaviour display | `fii_surrogate.plots.plot_rmse_fii` | `main/rmse_fii.png` |
| Auxiliary repeated-partition analysis | `fii_surrogate.repeated.run_repeated_partitions`; `fii_surrogate.auxiliary.compute_auxiliary_score` | `repeated_partition_results.csv`, summary, and plots |
| Documented hyperparameter search | `fii_surrogate.tuning.build_search`; `scripts/run_tuning.py` | `<family>_best_params.json` |

The synthetic workflow demonstrates the implementation. Exact model metrics,
surfaces, and FII values from the archived reference analysis require the
restricted laboratory dataset and are outside the public data boundary. The
legacy `manuscript` script and data names are retained as stable interfaces for
rebuilding the related publication figures.
