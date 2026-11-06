import numpy as np

from fii_surrogate.auxiliary import compute_auxiliary_score


def test_auxiliary_score_is_separate_equal_weight_mean():
    grid = np.array([[1.0, 1.0], [2.0, 1.0], [3.0, 1.0], [4.0, 1.0]])
    predictions = np.array([1.0, 0.5, 1.5, 1.7])
    comp = compute_auxiliary_score(grid, predictions, bounds=(0.2, 5.0))
    assert np.isclose(comp.decrease_rate, 1/3)
    assert np.isclose(comp.auxiliary_score, np.mean([
        comp.decrease_rate, comp.flattened_roughness, comp.output_range_violation
    ]))
