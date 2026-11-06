"""Canonical public vocabulary for the FII surrogate-model workflow."""

OBSERVATION_ID = "observation_id"
MATERIAL_ID = "material_id"
LITHOLOGY = "lithology"
WATER_CONTENT = "water_content_pct"
BULK_DENSITY = "bulk_density_mg_m3"
DRY_DENSITY = "dry_density_mg_m3"
PARTICLE_DENSITY = "particle_density_mg_m3"
THERMAL_CONDUCTIVITY = "thermal_conductivity_w_mk"
PREDICTED_THERMAL_CONDUCTIVITY = "predicted_thermal_conductivity_w_mk"

FEATURES = (WATER_CONTENT, BULK_DENSITY)
TARGET = THERMAL_CONDUCTIVITY
REQUIRED_COLUMNS = (
    OBSERVATION_ID,
    MATERIAL_ID,
    LITHOLOGY,
    WATER_CONTENT,
    BULK_DENSITY,
    THERMAL_CONDUCTIVITY,
)
OPTIONAL_PHYSICAL_COLUMNS = (DRY_DENSITY, PARTICLE_DENSITY)
LITHOLOGIES = ("sand", "silt", "clayey_soil", "clay")
