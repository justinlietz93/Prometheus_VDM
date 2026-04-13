# Spacetime Discretization Validation

## Tier 2: Transport sanity

| case | boundary | stencil | renorm | front speed | first walkers | phi_var rise | condensation jump |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| periodic6 | periodic | 6 | 1.000000 | 0.2114 | 1 | 6 | 21 |
| open6 | open | 6 | 1.000000 | 0.2098 | 1 | 6 | 26 |
| open26_raw | open | 26 | 1.000000 | 0.1366 | 1 | 3 | 15 |
| open26_calibrated | open | 26 | 0.230769 | 0.1321 | 1 | 3 | 14 |

## Tier 3: Calibration

Weighted-26 raw uses renormalization 1.000000; calibrated uses 0.230769.
Front speed shifts from 0.1366 to 0.1321; phi_var rise shifts from 3 to 3.
Target C_SIGNAL is 0.1581; calibrated weighted-26 still carries a residual front-speed mismatch of 0.0260 on this small test.

## Tier 4: Morphology and admissibility

- periodic6: wrap_axes_count=0, anisotropy=0.625, phase_before_condensation=True
- open6: wrap_axes_count=0, anisotropy=0.500, phase_before_condensation=True
- open26_raw: wrap_axes_count=0, anisotropy=0.375, phase_before_condensation=True
- open26_calibrated: wrap_axes_count=0, anisotropy=0.250, phase_before_condensation=True
