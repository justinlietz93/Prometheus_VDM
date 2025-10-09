# Progress (Updated: 2025-10-09)

## Done

- Re-ran spectrum scans at various resolutions; coverage improved from ~0.22 to ~0.66

## Doing

- Implemented adaptive θ-parameter bracketing with multi-resolution refinement in cylinder_modes._find_roots_for_ell
- Added stabilized logarithmic derivatives via scaled Bessel functions (ive/kve)
- Introduced complementary scans (Chebyshev θ, u=k_in R) and secant refinement around |f| minima

## Next

- Consider expanding R_sweep or adjusting ell_max/params in spec to reach ≥0.95 coverage
- Optionally add derivative sign checks to avoid false positives; profile performance impact
