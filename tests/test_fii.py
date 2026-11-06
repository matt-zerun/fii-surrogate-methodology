import numpy as np

from fii_surrogate.fii import compute_fii, directional_gradients


def test_monotonic_linear_surface_has_zero_mvr():
    w = np.array([1.0, 2.0, 3.0])
    rho = np.array([1.2, 1.5, 1.8])
    W, R = np.meshgrid(w, rho, indexing="ij")
    Z = 0.5 * W + 2.0 * R
    comp = compute_fii(
        Z, w, rho, roughness_reference=1.0,
        weights={"mvr":0.4, "roughness":0.4, "orv":0.2},
        bounds=(0.2, 10.0),
    )
    assert comp.mvr == 0.0
    assert comp.orv == 0.0
    assert comp.roughness_raw > 0.0


def test_negative_water_slope_is_detected():
    w = np.array([1.0, 2.0, 3.0])
    rho = np.array([1.0, 2.0])
    W, R = np.meshgrid(w, rho, indexing="ij")
    Z = -W + R
    comp = compute_fii(
        Z, w, rho, roughness_reference=1.0,
        weights={"mvr":0.4, "roughness":0.4, "orv":0.2},
        bounds=(-10.0, 10.0),
    )
    assert comp.mvr_water == 1.0
    assert comp.mvr_density == 0.0
    assert comp.mvr == 0.5


def test_gradients_use_predictor_spacing():
    w = np.array([0.0, 2.0, 4.0])
    rho = np.array([1.0, 3.0])
    W, R = np.meshgrid(w, rho, indexing="ij")
    Z = 3.0 * W + 4.0 * R
    gw, gr = directional_gradients(Z, w, rho)
    assert np.allclose(gw, 3.0)
    assert np.allclose(gr, 4.0)
