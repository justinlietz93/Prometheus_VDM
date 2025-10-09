# Tachyonic Tube v1: Spectrum completeness and condensation curvature (QC)

> Author: Justin K. Lietz
> Date: 2025-10-09
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.
> Commercial use requires citation and written permission from Justin K. Lietz.
> See LICENSE file for full terms.

## TL;DR

This note documents two quality-control gates for the tachyonic tube model: (1) spectrum completeness over the physically-admissible set and (2) condensation energy exhibiting an interior minimum with positive curvature. Both gates pass with artifacts generated via io_paths.

Pinned artifact (spectrum overview): Derivation/code/outputs/figures/tachyonic_condensation/20251009_084702_tube_spectrum_overview__tube-spectrum-v1.png

## Scope & boundaries

This document verifies numerical completeness/consistency; it does not claim new physics beyond the EFT and boundary conditions stated. Off-diagonal quartic couplings and nonzero axial momentum are out of scope for v1.

## Research question

- Independent variables: radius R ∈ [0.5, 6.0], integer azimuthal index ℓ ≤ 8; parameters (μ=1, c=1). For condensation: λ=0.5, σ=0.6, α=12.0.
- Dependent variables: roots κ_ℓ(R) at k=0; coverage metrics; condensation energy E(R) with background E_bg(R)=2πσR + α/R; curvature near the minimum.
- Estimators: physically-admissible coverage cov_phys = successes / attempts_phys where attempts_phys is the count of (R,ℓ) pairs with sign-change potential; raw coverage cov_raw = successes / attempts_raw for transparency. Curvature from quadratic fit around the detected minimum with Δ² fallback.
- Thresholds: spectrum gate requires cov_phys ≥ 0.95; condensation gate requires finite_fraction ≥ 0.80 and curvature_ok = true.

## Background (core equations)

At k=0 the secular equation is

f_ℓ(κ; R, μ, c) = (κ_in/κ_out) (I′_ℓ/I_ℓ)(κ_in R) + (K′_ℓ/K_ℓ)(κ_out R) = 0,

with κ_in^2 = μ^2/c^2 − κ^2 and κ_out^2 = κ^2 + 2μ^2/c^2. The condensation baseline uses diagonal λ with N4_ℓ = (2π) λ ∫ r u_ℓ^4 dr and m_ℓ^2 = − c^2 κ_ℓ^2.

## Methods (measurement instrument)

- Spectrum: θ-parameterization κ=(μ/c) sin θ, multi-resolution scans, Chebyshev and u=k_in R complements, midpoint probes, and secant/Newton refinement. Scaled modified Bessels stabilize log-derivatives for I′/I and K′/K. Root potential is flagged by sign-change heuristics over admissible κ.
- Condensation: adaptive inside/outside split for N4 integrals with geometric tail shells and stopping on diminishing contribution; energy scan includes local refinement near the minimum to avoid boundary artifacts.
- IO discipline: io_paths used for all artifacts; approval gates route failed runs into quarantine.

## Results

### Spectrum gate (tag: tube-spectrum-v1)

- Summary JSON: Derivation/code/outputs/logs/tachyonic_condensation/20251009_084703_tube_spectrum_summary__tube-spectrum-v1.json
- Roots CSV: Derivation/code/outputs/logs/tachyonic_condensation/20251009_084702_tube_spectrum_roots__tube-spectrum-v1.csv
- Figures:
  - Overview: Derivation/code/outputs/figures/tachyonic_condensation/20251009_084702_tube_spectrum_overview__tube-spectrum-v1.png
  - Heatmap: Derivation/code/outputs/figures/tachyonic_condensation/20251009_084703_tube_spectrum_heatmap__tube-spectrum-v1.png

Metrics (v2-phys-aware): cov_phys = 1.000; cov_raw ≈ 0.548; attempts_phys = 74; attempts_raw = 135; successes = 74; max_residual ≈ 0.709. Verdict: PASS.

Note: Heatmap shows no possible-but-missed bins. Residual is informational for v1; propose adding a residual tolerance in v2.

### Condensation gate (tag: tube-condensation-v1)

- Summary JSON: Derivation/code/outputs/logs/tachyonic_condensation/20251009_062600_tube_condensation_summary__tube-condensation-v1.json
- Energy CSV: Derivation/code/outputs/logs/tachyonic_condensation/20251009_062600_tube_energy_scan__tube-condensation-v1.csv
- Figure: Derivation/code/outputs/figures/tachyonic_condensation/20251009_062600_tube_energy_scan__tube-condensation-v1.png

Metrics: finite_fraction = 1.0; min_R ≈ 1.35; curvature_ok = true (quadratic-fit a>0). Verdict: PASS.

Parameters: (μ, c, λ) = (1.0, 1.0, 0.5), ℓ_max=8, E_bg with σ=0.6, α=12.0.

## Discussion

- Coverage denominator matters: counting only physically-admissible (R,ℓ) pairs avoids false negatives when no secular root can exist; raw coverage is kept for transparency and sweep design comparisons.
- Stability fixes (scaled Bessels) and complementary scans eliminate the earlier "drop around R≈3" artifact by improving bracketing and avoiding overflow/underflow in I′/I and K′/K.
- Refinement near the energy minimum is necessary to avoid boundary minima and secure positive curvature.

## Conclusion

Both gates pass with artifact discipline. The spectrum is complete over the admissible set, and condensation exhibits an interior minimum with positive curvature for the documented parameters. Next steps: codify cov_phys as the primary KPI in the schema and optionally gate on residual; explore robustness across parameter ranges and extend beyond diagonal λ as needed.
