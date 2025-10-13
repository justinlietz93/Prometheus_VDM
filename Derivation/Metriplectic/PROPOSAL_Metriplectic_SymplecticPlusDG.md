# Proposal: Metriplectic - Symplectic (KG) + Discrete-Gradient (RD)

Date: 2025-10-08
Commit: fa2d126b8ebbc4d6f7929410c1a1dda9ae0f1524

## Proposer

- Justin K. Lietz (Independent Research; Prometheus VDM)

## Abstract

We propose a pre-registered suite of metriplectic validations coupling a symplectic (J-only) Klein–Gordon discretization to a metriplectic RD (M-only) operator, with the goal of establishing: (i) exact discrete Noether invariants for linear KG under Störmer–Verlet on periodic BCs; (ii) dispersion fidelity (ω² = c²k² + m²) at high R²; (iii) locality-cone consistency for the KG limit; and (iv) algebraic structure checks (skew J, PSD M) via randomized diagnostics. This program supplies rigorous, reproducible artifacts (JSON, CSV, PNG) under an approval-gated policy with tag-scoped schemas to support canon promotion and downstream integration.

## Background & Scientific Rationale

Metriplectic systems augment Hamiltonian (J) dynamics with metric (M) dissipation to enforce H-theorems while preserving invariants. For linear KG on a periodic lattice, symplectic integrators (e.g., Störmer–Verlet) are known to conserve a discrete energy exactly and maintain time-reversibility; translation symmetry yields a discrete momentum invariant. Validating these properties at machine precision provides a clean baseline for subsequent J+M coupling. Complementary dispersion and locality-cone tests ensure the discrete model reproduces continuum predictions. Independent algebraic structure checks of J (skew-symmetry) and M (positive semidefiniteness) are essential to certify metriplectic compatibility.

Novelty: The proposal ties together exact KG invariants, dispersion/causality baselines, and metriplectic structure checks in a single, approval-governed framework with standardized outputs and domain-tagged schemas, supporting canonization and regression over time.

## Intellectual Merit and Procedure

1) Importance. Discrete conservation and correct dispersion underlie trustworthy hybrid J+M simulations; metriplectic algebra provides thermodynamic consistency.  
2) Impact. Establishes a reproducible, auditable foundation for future nonlinear couplings and control problems within VDM.  
3) Approach. Use spectral spatial operators for KG, Störmer–Verlet time stepping, and IO/plotting helpers for uniform artifacts; for structure, use randomized quadratic-form diagnostics with documented gates.  
4) Rigor. Pre-registration with tag-specific JSON Schemas; DB-backed approvals; pass/fail gates; quarantining of unapproved runs.

## 5.1 Experimental Setup and Diagnostics

- Discretization: periodic 1D lattice, N ∈ {256}, dx = 1.0; spectral ∇, Δ for KG.  
- Parameters: c = 1.0, m = 0.5.  
- Time stepping: Störmer–Verlet with dt = min(dt_sweep) = 0.005, steps = 512 (baseline).  
- Diagnostics (KG-noether-v1):
  - Discrete energy E_d(t) and momentum P_d(t) time series; reversibility by forward/backward integration.  
  - Artifacts: PNG (E_d, P_d vs t), CSV (t, E_d, P_d), JSON summary (max per-step drift, pass flags).  
- Diagnostics (KG-dispersion-v1): ω² vs k² regression (R² ≥ 0.999) with CSV and PNG.  
- Diagnostics (KG-cone-v1): wavefront fit v_front within 2% of c under refinement.  
- Structure (struct-v1): randomized checks for median |<v, J v>| ≤ 1e−12 and neg_count(<u, M u>) = 0; figures: histograms; logs: JSON/CSV.
- Diagnostics (KG-energy-osc-v1): certify symplectic energy oscillation scaling and time-reversal for the conservative limb.  
  - Define discrete energy $H_d(t) = \tfrac12\|\pi\|_2^2 + \tfrac12 c^2\|\nabla_h\phi\|_2^2 + \tfrac12 m^2\|\phi\|_2^2$.  
  - For each $\Delta t$, measure oscillation amplitude $A_H(\Delta t) = \tfrac12(\max_t H_d - \min_t H_d)$ and relative amplitude $A_H/\bar H$.  
  - Time-reversal check: advance $+\Delta t$ then $-\Delta t$ and record $e_{\mathrm{rev}} = \max\{\|\phi_\text{back}-\phi_0\|_\infty,\,\|\pi_\text{back}-\pi_0\|_\infty\}$.  
  - Stability ladder: compute the discrete $\omega_\max$ from the actual spatial operator via $\omega_k^2 = m^2 + c^2\,\lambda_k$ (with $\lambda_k$ the operator eigenvalues), set $\Delta t_\max = 0.8/\omega_\max$, and sample a geometric grid $\{\Delta t_\max/2^j\}_{j=0..4}$.  
  - Seeds: pre-register band-limited initial conditions (low/mid/high $k$ bands), draw multiple seeds per band, aggregate medians to avoid resonance bias.  
  - Determinism: single-thread numerics, deterministic FFT plans, fixed seeds, and raw-buffer hashing at fixed checkpoints.

## 5.2 Experimental Runplan

- Tags and Schemas:  
  - KG-energy-osc-v1 → `Derivation/code/physics/metriplectic/schemas/KG-energy-osc-v1.schema.json` (planned; fields for {dt_list, A_H, rel_A_H, fit:{p,R2}, e_rev, pass}).  
  - KG-noether-v1 → `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json`  
  - KG-dispersion-v1 → existing schema  
  - KG-cone-v1 → existing schema  
  - struct-v1 → existing schema  

- Runners and Specs:  
  - KG energy-oscillation: `Derivation/code/physics/metriplectic/run_kg_energy_oscillation.py` with spec `.../specs/kg_energy_osc.v1.json` (band-limited seeds, discrete $\omega_\max$ ladder, checkpoints, tag="KG-energy-osc-v1").  
  - KG-noether: `Derivation/code/physics/metriplectic/kg_noether.py` with spec `.../specs/kg_noether.v1.json` (N=256, dx=1.0, c=1.0, m=0.5, steps=512, tag="KG-noether-v1").  
  - Dispersion: `run_kg_dispersion.py` with `step_spec.kg_rd.v1.json` tag `KG-dispersion-v1`.  
  - Cone: `run_kg_light_cone.py` with `step_spec.kg_rd.v1.json` tag `KG-cone-v1`.  
  - Structure: `metriplectic_structure_checks.py` with `specs/struct_checks.v1.json` tag `struct-v1`.

- Gates and Success Criteria:  
  - H0 (KG energy-osc): log–log slope $p\in[1.95,2.05]$ with $R^2\ge 0.999$ for $A_H(\Delta t)$; time-reversal $e_{\mathrm{rev}}\le 1\times 10^{-12}$ (ULP $\le 1$ portability note); relative amplitude gate at smallest $\Delta t$: $(A_H/\bar H)\le 10^{-4}$.  
  - H1 (Noether): max per-step drift E_d, P_d ≤ 1e−12 or ≤ 10 ε √N; reversibility ≤ 1e−10; artifacts present.  
  - H2 (Dispersion): R² ≥ 0.999; slope/intercept within 5% of c², m².  
  - H3 (Cone): v within 2% of c and stable under refinement.  
  - H4 (Structure): median |<v, J v>| ≤ 1e−12 and neg_count = 0; sidecar CSV/JSON + hist PNGs.

- Failure Plan: If any gate fails, route logs/figures under `failed_runs/`, emit a CONTRADICTION_REPORT with spec snapshot and control outcomes, and halt promotion to canon; iterate with controlled parameter adjustments (documented in decision log) before re-approval if the tag changes.
  - Determinism audit: record library versions, thread caps, FFT plan mode; hash raw state arrays at fixed checkpoints (every K steps and final) to support no-switch identity and reversal audits.

- Publication: RESULTS pages per subtopic under `Derivation/Metriplectic/`, pinned artifact paths, and updates to `CANON_PROGRESS.md` upon PROVEN gates.

## Personnel

Proposer: Justin K. Lietz - designs experiments, sets gates and tags, approves proposals, runs pre-registered scripts, and curates RESULTS and canon updates.

## References

- Hairer, Lubich, Wanner. Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations. Springer.
- Morrison, P. J. A paradigm for joined Hamiltonian and dissipative systems. Physica D (1998).
- Leimkuhler, Reich. Simulating Hamiltonian Dynamics. Cambridge.
