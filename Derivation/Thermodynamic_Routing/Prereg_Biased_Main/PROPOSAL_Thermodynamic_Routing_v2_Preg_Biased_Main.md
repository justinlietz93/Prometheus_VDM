# PROPOSAL: Thermodynamic Routing v2 — Prereg Biased Main

Author: Justin K. Lietz  
Date: 2025-10-13  
Commit: 9c27e65  
Provenance hash (commit:salt→sha256): 9c27e65a34a87eae875ed49b419ad4e2030c7e89 : 1760354544 → 3095e2fda4af934cd9d1755592d764ebf30470301e4a87d1ee502d39b81a6af5

## 1. Proposal Title and date

Thermodynamic Routing v2 — Prereg Biased Main (full gates)

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz (Prometheus VDM)

## 3. Abstract

We will execute the preregistered biased-geometry run of Thermodynamic Routing v2 with full gates enforced. The metric (DG) step must satisfy the H-theorem (ΔL_h ≤ 0), no-switch identity must hold bitwise or within ∞-norm ≤ 1e−12, the RJ spectral fit must achieve R² ≥ 0.99 on a predeclared band and time window with residual whiteness diagnostics (Durbin–Watson, Ljung–Box(5), ρ₁), routing bias must exhibit nonzero B and ρ with 95% CI excluding 0 meeting a preregistered margin δ, the energy-floor witness must beat a local baseline by ≥ 5σ, and robustness checks (injection-site slope CI≠0, two-source |Δη_route| ≤ 5%) must pass. Artifacts and JSON/CSV logs will be routed via policy-aware helpers with deterministic receipts.

## 4. Background & Scientific Rationale

A metriplectic RD system with passive descent provides a testbed for thermodynamic routing without explicit control. The discrete Lyapunov functional

$$
L_h[\phi] = \sum_i \Big( \tfrac{D}{2} |\nabla_h \phi_i|^2 + \hat V(\phi_i) \Big) \, \Delta x^2, \quad \hat V'(\phi) \equiv -f(\phi),\ f(\phi)= r\phi - u\phi^2 
$$

is monotonically non-increasing under the DG metric step. In a geometry with biased outlet widths $(w_A > w_B)$ and outflux-only boundary accounting, we hypothesize a positive routing bias toward A. Post-collapse modal occupancies on the discrete Laplacian eigenbasis should follow a Rayleigh–Jeans form $\langle |c_k|^2 \rangle = T/(\lambda_k-\mu)$ in a predeclared window.

## 5. Intellectual Merit and Procedure

- Importance: tests rigorous thermodynamic routing claims with metriplectic structure and reproducible gates.
- Impact: establishes baseline routing capability without actuation, enabling comparisons to active controllers.
- Rigor: approvals, deterministic receipts, predeclared windows/bands and CI-based gates.

## 5.1 Experimental Setup and Diagnostics

- Grid: 96×48, Lx=6.0, Ly=3.0; stencil=FD-3pt; periodic interior, outflux on right boundary.
- Geometry: outlet widths (w_A=0.55, w_B=0.35) on right boundary; injection packet near x0=0.25, y0 ∈ {0.9,1.5,2.1} (robustness sweep).
- RD params: D=1.0, r=0.2, u=0.25, λ=0.0.
- Time: T=1.5, dt=0.01 (adjustable down if overflow risk), checkpoints K=25.
- RJ: k-band [3,24]; window t ∈ [0.8, 1.5].
- Seeds: 5 (band-limited, fixed list).
- Diagnostics: Lyapunov series (CSV), RJ regression JSON, flux bias JSON (B, ρ, CI, width), receipts (threads, BLAS, FFT, hashes).

## 5.2 Experimental runplan

- Enforce approvals; run 5 seeds and aggregate by median for KPIs with 95% CIs (bootstrap or t-interval where applicable).
- Perform injection-site sweep and two-source split ratios {0.3,0.5,0.7}; compute slope CI and Δη_route CI.
- RJ fit in [0.8,1.5] over k ∈ [3,24] with residual diagnostics (DW, Ljung–Box(5), ρ₁). Gate R² ≥ 0.99.
- Outflux-only bias at right boundary; CI excludes 0 and meets δ margin (δ to be set at 0.02 in spec).
- Energy-floor witness vs matched baseline ≥ 5σ; CI excludes 0.

## KPI Gates (must pass)

1. H-theorem: violations = 0.
2. No-switch: bitwise or ∞-norm ≤ 1e−12 (or max-ULP ≤ 1); log clause.
3. RJ fit: R² ≥ 0.99 on [k_min,k_max]=[3,24], window [0.8,1.5]; include DW/LB/ρ₁.
4. Bias: 95% CI excluding 0; δ ≥ 0.02; report CI width.
5. Energy-floor: ≥ 5σ vs baseline; CI excludes 0.
6. Robustness: injection-site slope CI≠0; two-source |Δη_route| ≤ 5% (CI).
7. Determinism: receipts present (threads/BLAS/FFT/plan), checkpoint hashes present; no-switch clause logged.

## 6. Personnel

- Justin K. Lietz — design, execution, analysis, and documentation.

## 7. References

- Metriplectic integrators and discrete gradient methods (e.g., Gonzalez 1996; Quispel & Turner 1996).
- Rayleigh–Jeans spectral statistics in discretized systems; standard econometrics tests for residual whiteness (DW, Ljung–Box).
