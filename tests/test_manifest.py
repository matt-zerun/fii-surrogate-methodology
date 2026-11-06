from pathlib import Path

from fii_surrogate.config import load_json


def test_manifest_contains_25_configurations():
    manifest = load_json(Path("config/model_manifest.json"))
    assert len(manifest["models"]) == 25
    assert len({entry["id"] for entry in manifest["models"]}) == 25


def test_known_duplicate_parameterisations_are_preserved():
    manifest = load_json(Path("config/model_manifest.json"))
    by_id = {entry["id"]: entry for entry in manifest["models"]}
    assert by_id["DT__baseline"]["params"] == by_id["DT__variant_1"]["params"]
    assert by_id["KNN__tuned"]["params"] == by_id["KNN__variant_3"]["params"]


def test_corrected_variant_parameters():
    manifest = load_json(Path("config/model_manifest.json"))
    by_id = {entry["id"]: entry for entry in manifest["models"]}
    assert by_id["RF__variant_2"]["params"]["max_features"] == "sqrt"
    assert by_id["RF__variant_3"]["params"]["max_features"] == 0.5
    assert by_id["KNN__variant_1"]["params"]["p"] == 1
    assert by_id["XGB__tuned"]["params"]["subsample"] == 0.6
    assert by_id["XGB__tuned"]["params"]["reg_lambda"] == 2.0
