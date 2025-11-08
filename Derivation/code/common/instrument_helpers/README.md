# VDM Instrument Helpers

## NOTE: These must not be used alone as instruments

Instead they should be used within gate validated instruments before publishing results derived from the instrument

## VDM LIT Helpers

Files:

- Derivation/code/common/instrument_helpers/lit_tools.py

Quick usage (pseudo-grid of 10 cells with random forces):

```python
import numpy as np
from instrument_helpers.lit_tools import (
    IsotropicFluidCoeffs, build_L_isotropic_fluid, curie_mask,
    gate_report, parity_even
)

coeffs = IsotropicFluidCoeffs(kappa=0.6, eta=1.0, zeta=0.2)
L, r_forces, r_fluxes = build_L_isotropic_fluid(coeffs)
mask = curie_mask(r_forces, r_fluxes)

X = np.random.randn(10, 5) * 0.1  # small gradients/noise near equilibrium
report = gate_report(L, X, dV=1.0, parity=parity_even(5), mask=mask)
print(report)
```
