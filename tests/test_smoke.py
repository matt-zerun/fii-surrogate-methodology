from pathlib import Path

from fii_surrogate.analysis import run_fixed_configurations
from fii_surrogate.config import load_json
from fii_surrogate.data_validation import validate_canonical_input
from fii_surrogate.io import load_table


def test_small_fixed_configuration_smoke(tmp_path):
    cfg = load_json(Path("config/demo_analysis_config.json"))
    manifest = load_json(Path("config/model_manifest.json"))
    data, _ = validate_canonical_input(
        load_table("data/synthetic_example/fii_synthetic_example.csv")
    )
    results, surfaces = run_fixed_configurations(data, manifest["models"][:2], cfg, tmp_path)
    assert len(results) == 2
    assert not surfaces.empty
    assert {"overall_rmse", "heldout_rmse", "fii"}.issubset(results.columns)
    assert {
        "water_content_pct",
        "bulk_density_mg_m3",
        "predicted_thermal_conductivity_w_mk",
    }.issubset(surfaces.columns)
