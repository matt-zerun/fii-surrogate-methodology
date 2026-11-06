# Methodology implemented in this repository

## Canonical FII workflow

For a fitted model evaluated on a common regular two-dimensional grid:

1. First-order finite-difference gradients are calculated along water content and bulk density using the corresponding predictor increments.
2. The Monotonicity Violation Rate (MVR) is the arithmetic mean of the two directional fractions of negative gradients.
3. Raw roughness is the square root of the sum of the mean squared directional gradients.
4. Normalised roughness is raw roughness divided by one fixed positive reference used unchanged for all compared configurations.
5. The Output-Range Violation rate (ORV) is the fraction of predictions outside 0.2–5.0 W m−1 K−1.
6. FII = 0.4 MVR + 0.4 Rough_norm + 0.2 ORV.

FII is heuristic, relative and context-dependent. It does not measure physical validity or predictive uncertainty. The demo configuration uses a synthetic-only roughness reference value of 1.0; users must supply the fixed reference appropriate to their own analysis.

## Accuracy metrics

The fixed-configuration workflow records two distinct sets of metrics:

- `overall_*`: reconstruction metrics for all retained observations after fitting on the predefined training subset;
- `heldout_*`: metrics for the independent test subset.

They are not interchangeable.

## Auxiliary repeated-partition score

The repeated-partition experiment is implemented separately and does not calculate FII. It reproduces the documented auxiliary procedure:

- 30 seeds from 100 to 129;
- one fixed experiment-specific configuration per family;
- a 150×150 candidate grid restricted to the convex hull of the training observations;
- a sequence-based decrease rate after ordering grid points by water content;
- flattened-sequence roughness `std(gradient(predictions))`;
- output-range violation rate;
- equal-weight mean of the three quantities.

The resulting `auxiliary_score` must never be relabelled as FII.
