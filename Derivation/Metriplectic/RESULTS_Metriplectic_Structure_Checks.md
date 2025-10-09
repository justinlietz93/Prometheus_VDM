# Metriplectic Structure Checks - J Skew and M PSD

> Author: Justin K. Lietz  
> Date: 2025-10-08
>
> TL;DR - This RESULTS page documents the algebraic structure tests for a metriplectic system: (i) skew-symmetry of the canonical J operator and (ii) positive semidefiniteness (PSD) of the metric operator M on the RD channel. Gates: median |⟨v, J v⟩| ≤ 1e−12 over random draws; count of negative ⟨u, M u⟩ equals 0 across draws. Artifacts to be attached from the policy-aware runner.

## Research question

Do the discrete operators used in our metriplectic integrators satisfy the defining degeneracy properties numerically on the working grid?

- J skew: ⟨v, J v⟩ = 0 for all v (in exact arithmetic); gate uses median absolute value over random v.
- M PSD: ⟨u, M u⟩ ≥ 0 for all u; gate uses zero negative counts over random u.

## Methods

- Runner: `derivation/code/physics/metriplectic/metriplectic_structure_checks.py`
- IO: `derivation/code/common/io_paths.py` (policy-aware; quarantines unapproved runs under failed_runs/)
- Spec: grid (N, Δx), params (D, c, m, m_lap_operator), draws (default 100), optional tag.
- Metrics logged: J_skew.median_abs_vJv; M_psd.neg_count, M_psd.min; pass/fail per gate.

## Gates

- J skew gate: median |⟨v, J v⟩| ≤ 1e−12.
- M PSD gate: neg_count = 0 with tolerance 1e−12.

## Artifacts (struct-v1)

- JSON log: `Derivation/code/outputs/logs/metriplectic/20251008_181035_metriplectic_structure_checks__struct-v1.json`
- CSV summary: `Derivation/code/outputs/logs/metriplectic/20251008_181035_metriplectic_structure_checks_summary__struct-v1.csv`
- Figures:
  - `Derivation/code/outputs/figures/metriplectic/20251008_181035_metriplectic_structure_checks_J_skew_hist__struct-v1.png`
  - `Derivation/code/outputs/figures/metriplectic/20251008_181036_metriplectic_structure_checks_M_psd_hist__struct-v1.png`
- Plot metadata logs:
  - `Derivation/code/outputs/logs/metriplectic/20251008_181036_metriplectic_structure_checks_J_skew_hist__struct-v1.json`
  - `Derivation/code/outputs/logs/metriplectic/20251008_181036_metriplectic_structure_checks_M_psd_hist__struct-v1.json`

### Approval details

- Spec path: `derivation/code/physics/metriplectic/specs/struct_checks.v1.json`
- Proposed tag: `struct-v1`
- Runner invocation (policy-aware): use the `--spec` argument pointing to the file above; artifacts will be routed under `code/outputs/logs/metriplectic/` with the tag suffix.

## Status

- struct-v1: PASS.
  - $\mathrm{median}\,|\langle v, J v\rangle| \approx 1.53\times 10^{-15}$ (gate $\le 10^{-12}$)
  - $\min\langle u, M u\rangle \approx 6.33\times 10^{2}$; $\mathrm{neg\_count}=0$ over draws

## Notes

- The M operator here acts on the RD scalar channel; for coupled KG⊕RD states, the check can be extended blockwise to confirm block-PSD.
- Spectral vs stencil Laplacian options are parameterized via `m_lap_operator`.

## References

- Morrison, P. J. (1986). A paradigm for joined Hamiltonian and dissipative systems. Physica D.
- Grmela, M., & Öttinger, H. C. (1997). Dynamics and thermodynamics of complex fluids. I. Development of a general formalism. Phys. Rev. E.
