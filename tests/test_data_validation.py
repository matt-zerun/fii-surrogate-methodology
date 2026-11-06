import pandas as pd
import pytest

from fii_surrogate.data_validation import InputValidationError, validate_canonical_input


def valid_table(n=20):
    water = pd.Series(range(n), dtype=float) + 1.0
    dry = pd.Series([1.6] * n)
    return pd.DataFrame(
        {
            "observation_id": [f"obs-{index}" for index in range(n)],
            "material_id": [f"material-{index // 2}" for index in range(n)],
            "lithology": ["sand"] * n,
            "water_content_pct": water,
            "bulk_density_mg_m3": dry * (1 + water / 100),
            "dry_density_mg_m3": dry,
            "particle_density_mg_m3": [2.65] * n,
            "thermal_conductivity_w_mk": [1.5] * n,
        }
    )


def test_valid_canonical_table_is_preserved():
    prepared, report = validate_canonical_input(valid_table())
    assert len(prepared) == 20
    assert report.n_valid_observations == 20
    assert report.optional_columns_present == (
        "dry_density_mg_m3",
        "particle_density_mg_m3",
    )


def test_duplicate_observation_ids_are_rejected():
    table = valid_table()
    table.loc[1, "observation_id"] = table.loc[0, "observation_id"]
    with pytest.raises(InputValidationError, match="Duplicate observation_id"):
        validate_canonical_input(table)


def test_non_numeric_required_value_is_not_silently_dropped():
    table = valid_table()
    table["water_content_pct"] = table["water_content_pct"].astype(object)
    table.loc[4, "water_content_pct"] = "not-a-number"
    with pytest.raises(InputValidationError, match="non-numeric"):
        validate_canonical_input(table)


def test_density_identity_disagreement_is_rejected():
    table = valid_table()
    table.loc[3, "dry_density_mg_m3"] = 1.0
    with pytest.raises(InputValidationError, match="density identity"):
        validate_canonical_input(table)


def test_unknown_lithology_is_rejected():
    table = valid_table()
    table.loc[0, "lithology"] = "unknown"
    with pytest.raises(InputValidationError, match="Unknown lithology"):
        validate_canonical_input(table)
