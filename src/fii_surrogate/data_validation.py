from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .constants import (
    BULK_DENSITY,
    DRY_DENSITY,
    FEATURES,
    LITHOLOGIES,
    LITHOLOGY,
    MATERIAL_ID,
    OBSERVATION_ID,
    OPTIONAL_PHYSICAL_COLUMNS,
    PARTICLE_DENSITY,
    REQUIRED_COLUMNS,
    TARGET,
    WATER_CONTENT,
)


class InputValidationError(ValueError):
    """Actionable error raised when canonical input is not valid."""


@dataclass(frozen=True)
class ValidationReport:
    n_input_observations: int
    n_valid_observations: int
    counts_by_lithology: dict[str, int]
    optional_columns_present: tuple[str, ...]


def _row_examples(mask: pd.Series, limit: int = 5) -> list[int]:
    """Return one-based CSV-like row numbers, including the header offset."""
    return (np.flatnonzero(mask.to_numpy())[:limit] + 2).astype(int).tolist()


def _require_numeric(table: pd.DataFrame, columns: list[str]) -> None:
    for column in columns:
        supplied = table[column]
        numeric = pd.to_numeric(supplied, errors="coerce")
        invalid = supplied.notna() & numeric.isna()
        if invalid.any():
            raise InputValidationError(
                f"Column '{column}' contains non-numeric values at input rows "
                f"{_row_examples(invalid)}. Use the unit documented in DATA_SCHEMA.md."
            )
        infinite = numeric.notna() & ~np.isfinite(numeric)
        if infinite.any():
            raise InputValidationError(
                f"Column '{column}' contains infinite values at input rows "
                f"{_row_examples(infinite)}."
            )
        table[column] = numeric


def validate_canonical_input(
    df: pd.DataFrame,
    *,
    minimum_observations: int = 20,
    density_identity_abs_tolerance_mg_m3: float = 0.02,
    density_identity_rel_tolerance: float = 0.02,
) -> tuple[pd.DataFrame, ValidationReport]:
    """Validate the canonical FII observation table without silent row removal."""
    missing_columns = [name for name in REQUIRED_COLUMNS if name not in df.columns]
    if missing_columns:
        raise InputValidationError(
            "Missing required columns: " + ", ".join(missing_columns)
        )
    if len(df) < minimum_observations:
        raise InputValidationError(
            f"At least {minimum_observations} observations are required; found {len(df)}."
        )

    retained_columns = list(REQUIRED_COLUMNS) + [
        name for name in OPTIONAL_PHYSICAL_COLUMNS if name in df.columns
    ]
    prepared = df.loc[:, retained_columns].copy()

    missing_required = prepared[list(REQUIRED_COLUMNS)].isna()
    if missing_required.any().any():
        details = []
        for column in REQUIRED_COLUMNS:
            mask = missing_required[column]
            if mask.any():
                details.append(f"{column}: rows {_row_examples(mask)}")
        raise InputValidationError(
            "Required values are missing (CSV row numbers): " + "; ".join(details)
        )

    for column in (OBSERVATION_ID, MATERIAL_ID):
        prepared[column] = prepared[column].astype("string").str.strip()
        empty = prepared[column].eq("")
        if empty.any():
            raise InputValidationError(
                f"Column '{column}' contains empty identifiers at input rows "
                f"{_row_examples(empty)}."
            )

    prepared[LITHOLOGY] = (
        prepared[LITHOLOGY]
        .astype("string")
        .str.lower()
        .str.strip()
        .str.replace(" ", "_", regex=False)
    )
    empty_lithology = prepared[LITHOLOGY].eq("")
    if empty_lithology.any():
        raise InputValidationError(
            f"Column '{LITHOLOGY}' contains empty values at input rows "
            f"{_row_examples(empty_lithology)}."
        )
    unknown = sorted(set(prepared[LITHOLOGY]) - set(LITHOLOGIES))
    if unknown:
        raise InputValidationError(
            f"Unknown lithology values: {unknown}. Allowed values: {list(LITHOLOGIES)}."
        )

    duplicates = prepared[OBSERVATION_ID].duplicated(keep=False)
    if duplicates.any():
        examples = prepared.loc[duplicates, OBSERVATION_ID].astype(str).head(5).tolist()
        raise InputValidationError(
            f"Duplicate observation_id values detected, examples: {examples}."
        )

    numeric_columns = [*FEATURES, TARGET] + [
        name for name in OPTIONAL_PHYSICAL_COLUMNS if name in prepared.columns
    ]
    _require_numeric(prepared, numeric_columns)

    for column in (*FEATURES, TARGET):
        missing = prepared[column].isna()
        if missing.any():
            raise InputValidationError(
                f"Column '{column}' contains missing numeric values at input rows "
                f"{_row_examples(missing)}."
            )

    negative_water = prepared[WATER_CONTENT] < 0
    if negative_water.any():
        raise InputValidationError(
            f"{WATER_CONTENT} cannot be negative; input rows {_row_examples(negative_water)}."
        )
    invalid_bulk = prepared[BULK_DENSITY] <= 0
    if invalid_bulk.any():
        raise InputValidationError(
            f"{BULK_DENSITY} must be positive; input rows {_row_examples(invalid_bulk)}."
        )
    invalid_lambda = prepared[TARGET] <= 0
    if invalid_lambda.any():
        raise InputValidationError(
            f"{TARGET} must be positive; input rows {_row_examples(invalid_lambda)}."
        )

    likely_density_units = prepared[BULK_DENSITY] > 10
    if likely_density_units.any():
        raise InputValidationError(
            f"{BULK_DENSITY} exceeds 10 Mg m^-3 at input rows "
            f"{_row_examples(likely_density_units)}; values may be in kg m^-3."
        )
    likely_lambda_units = prepared[TARGET] > 50
    if likely_lambda_units.any():
        raise InputValidationError(
            f"{TARGET} exceeds 50 W m^-1 K^-1 at input rows "
            f"{_row_examples(likely_lambda_units)}; verify units and material scope."
        )

    for column in OPTIONAL_PHYSICAL_COLUMNS:
        if column not in prepared.columns:
            continue
        invalid = prepared[column].notna() & (prepared[column] <= 0)
        if invalid.any():
            raise InputValidationError(
                f"{column} must be positive when supplied; input rows "
                f"{_row_examples(invalid)}."
            )
        likely_units = prepared[column].notna() & (prepared[column] > 10)
        if likely_units.any():
            raise InputValidationError(
                f"{column} exceeds 10 Mg m^-3 at input rows "
                f"{_row_examples(likely_units)}; values may be in kg m^-3."
            )

    if DRY_DENSITY in prepared.columns:
        comparable = prepared[DRY_DENSITY].notna()
        dry_exceeds_wet = comparable & (
            prepared[DRY_DENSITY] > prepared[BULK_DENSITY]
        )
        if dry_exceeds_wet.any():
            raise InputValidationError(
                f"{DRY_DENSITY} exceeds {BULK_DENSITY} at input rows "
                f"{_row_examples(dry_exceeds_wet)}."
            )
        expected_bulk = prepared[DRY_DENSITY] * (
            1.0 + prepared[WATER_CONTENT] / 100.0
        )
        tolerance = density_identity_abs_tolerance_mg_m3 + (
            density_identity_rel_tolerance * prepared[BULK_DENSITY].abs()
        )
        inconsistent = comparable & (
            (prepared[BULK_DENSITY] - expected_bulk).abs() > tolerance
        )
        if inconsistent.any():
            raise InputValidationError(
                "Wet/dry-density identity is inconsistent at input rows "
                f"{_row_examples(inconsistent)}. Expected {BULK_DENSITY} = "
                f"{DRY_DENSITY} * (1 + {WATER_CONTENT}/100)."
            )

    if PARTICLE_DENSITY in prepared.columns:
        comparable = prepared[PARTICLE_DENSITY].notna()
        bulk_exceeds_particle = comparable & (
            prepared[BULK_DENSITY] > prepared[PARTICLE_DENSITY]
        )
        if bulk_exceeds_particle.any():
            raise InputValidationError(
                f"{BULK_DENSITY} exceeds {PARTICLE_DENSITY} at input rows "
                f"{_row_examples(bulk_exceeds_particle)}."
            )

    counts = prepared[LITHOLOGY].value_counts().reindex(LITHOLOGIES, fill_value=0)
    report = ValidationReport(
        n_input_observations=len(prepared),
        n_valid_observations=len(prepared),
        counts_by_lithology={key: int(value) for key, value in counts.items()},
        optional_columns_present=tuple(
            name for name in OPTIONAL_PHYSICAL_COLUMNS if name in prepared.columns
        ),
    )
    return prepared.reset_index(drop=True), report
