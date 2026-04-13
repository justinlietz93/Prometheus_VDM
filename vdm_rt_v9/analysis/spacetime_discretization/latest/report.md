# Spacetime Discretization Comparison

## Change log

- Measurement only: expanded the comparison runner to use field-departure transport metrics, condensed-bond component summaries, and morphology notes.
- Measurement only: added a structured markdown report and machine-readable comparison output for side-by-side lattice/boundary cases.

## What changed in measurement/reporting

- Primary transport metric is now field-front speed measured from `|phi - 0.5| >= 0.05`, rather than `last_visit`.
- `last_visit` remains available only as the clearly secondary `observation_front_speed_secondary` diagnostic.
- Reporting now includes first walker tick, first meaningful `phi_var` rise tick, first large condensation jump tick, final `phi_var`, final condensed bond count, condensed-component structure, and morphology notes.

## Comparison table

| case | first walker | phi_var rise | condensation jump | final phi_var | final condensed | field front speed | morphology notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| periodic6 | 1 | 6 | 21 | 0.2221 | 2440 | 0.2114 | strong axis bias (0.625); 1 condensed component(s), largest=495 nodes |
| open6 | 1 | 6 | 26 | 0.2436 | 1115 | 0.2098 | strong axis bias (0.500); 2 condensed component(s), largest=286 nodes |
| open26_raw | 1 | 3 | 15 | 0.2190 | 7136 | 0.1366 | moderate axis bias (0.375); 1 condensed component(s), largest=502 nodes |
| open26_calibrated | 1 | 3 | 14 | 0.2396 | 6306 | 0.1321 | moderate axis bias (0.250); 1 condensed component(s), largest=499 nodes |

## Robust effects vs likely artifacts

- Robust: walker ignition occurs immediately after the pulse in every measured case
- Robust: field variance rise precedes the first large condensation jump in every measured case
- Likely artifact-like or discretization-sensitive: periodic vs open boundary did not strongly separate final phi_var on this small pulse test
- Likely artifact-like or discretization-sensitive: the weighted-26 experiment reduces axis anisotropy relative to open-6 in the final positive phase extent

## Calibration residual

- Raw weighted-26 renormalization: 1.000000; calibrated weighted-26 renormalization: 0.230769.
- Field-front speed shifts from 0.1366 to 0.1321; target `C_SIGNAL` is 0.1581; residual mismatch after calibration is 0.0260.

## What did NOT change in runtime physics semantics

- Governing equations were not edited.
- Superposition IC semantics were not edited.
- Dynamic bond admissibility and dynamic bond creation semantics were not edited.
- Active runtime defaults were not edited in this task.
- No new normalization, clipping, gating, or heuristic smoothing was inserted into the runtime physics path.

## Potential physics-semantic changes that were intentionally NOT implemented

- No retuning of theory constants to chase front-speed agreement.
- No change to dynamic walker-instantiated bond geometry semantics.
- No change to runtime defaults to force one discretization into production.
- No additional bond-admissibility filters or transport heuristics.

## Recommendation

- promising but not canon-ready

## Final checklist

- Governing equations changed? no
- IC semantics changed? no
- Dynamic bond semantics changed? no
- Transport semantics in active runtime path changed? no
- Defaults changed? no
- New optional experimental modes added? no
- Any heuristic/proxy inserted into physics path? no
