# PROPOSAL: Passive Thermodynamic Routing v2 (Pre-Registration)

> Supersedes earlier No-Switch draft.

Author: Justin K. Lietz  
Date: 2025-10-13  
Commit: 2bb143a  
Tag: thermo-routing-v2

## Hypothesis and Scope

Passive thermodynamic routing improves energy/entropy allocation under a passive controller (no explicit actuation), reducing Lyapunov-like functional L_h while respecting metriplectic structure. This v2 preregistration follows the certified J-only KG instrument and introduces KPI-gated diagnostics for the J⊕M coupling limb. No parameter tuning post hoc; windowing and masks are predeclared.

Assumptions and exclusions:

- Discrete operator stability respected (Δt ≤ 0.8/ω_max from discrete spectral operator)
- Single-thread numerics, deterministic FFT/plan where applicable
- Seeds: fixed band-limited set; seed-band aggregation via median
- Geometry masks: preregistered; any changes trigger re-run under new tag

Axiom gates (trace to A0–A7): Noether/H-invariants enforced by design; J-only Noether is N/A for purely linear checks; M-step H-theorem applies. Locality smoke retained for J component.

## Background & Scientific Rationale

We consider passive thermodynamic routing in a metriplectic reaction–diffusion medium, where the field $\phi(\mathbf x,t)$ evolves under a metric (DG) step that monotonically decreases a discrete Lyapunov functional $L_h[\phi]$ while preserving the metriplectic split. In a 2-channel geometry with a mild funnel bias, thermodynamic descent alone should steer flux toward the favored outlet without any explicit switching. Beyond routing, we evaluate post-collapse spectral equilibria via Rayleigh–Jeans (RJ) fits over Laplacian modes to assess thermodynamic consistency.

Model baseline (RD form):

$$
\partial_t \, \phi \;=\; D \, \nabla^2 \phi + f(\phi),\qquad
L_h[\phi] \;=\; \sum_i \Big( \tfrac{D}{2} \, |\nabla_h \phi_i|^2 + \hat V(\phi_i) \Big)\,\Delta x^d,\quad \hat V'(\phi) \equiv -f(\phi).
$$

RJ diagnostic in a post-collapse window uses modal occupancies $\langle |c_k|^2\rangle$ over Laplacian eigenpairs $-\Delta \psi_k = \lambda_k\,\psi_k$ with the fit

$$
\langle |c_k|^2 \rangle \;\approx\; \frac{T}{\lambda_k - \mu}.
$$

## Objectives & Hypotheses

- H1 (H-theorem): For the DG M-only step, $\Delta L_h \le 0$ at every time step (violations $=0$).
- H2 (Energy-floor witness): At matched horizon $T$ and identical ICs, the passive DG run achieves strictly lower $L_h$ than a matched local baseline by $\ge 5\sigma$ (bootstrap CI excludes $0$).
- H3 (Routing bias): Outlet flux to $\mathcal O_\mathrm{A}$ exceeds $\mathcal O_\mathrm{B}$ by a pre-registered margin; report $B \equiv F_\mathrm{A} - F_\mathrm{B}$ and $\varrho \equiv \tfrac{F_\mathrm{A}}{F_\mathrm{A}+F_\mathrm{B}}$ with 95% CI.
- H4 (No-switch invariance): A controller-disabled flag yields trajectories and metrics identical (bitwise or within machine epsilon) to the default path; logs include `no_switch:true`, stepper SHA, and code-path identity.
- H5 (Thermalization fit): In a pre-registered post-collapse window, the modal spectrum admits an RJ fit with $R^2 \ge 0.99$; report $(T,\mu)$ stability across sub-windows.

## Variables (Pre-Registered)

Independent

- Geometry: 2-channel mask with outlet widths $(w_\mathrm{A} \ge w_\mathrm{B})$, channel length $L_c$, obstacles; no-flux walls; outlet segments on the right boundary.
- RD parameters: $(D, r, u)$ for $f(\phi)=r\phi - u\phi^2$ (or alternative $f$ with $\hat V'=-f$).
- Grid/discretization: $(N_x,N_y) \in \{(256,128),(512,256)\}$, $\Delta x$; stencil $\in\{\text{FD-3pt}, \text{spectral}\}$ (param-gated).
- Stepper: primary DG M-only; optional JMJ (symplectic half-steps around DG) as a tagged diagnostic.
- Time: $\Delta t$, horizon $T$; checkpoint cadence $K$.
- Seeds: number of random initializations; injection position(s) and optional two-source split ratios.
- Tag: string for artifact suffixing.

Dependent

- Lyapunov series: $L_h(t)$, per-step $\Delta L_h$.
- Outlet fluxes: $(F_\mathrm{A}, F_\mathrm{B})$; efficiencies $\eta_\text{route} \equiv \tfrac{F_\mathrm{A}}{F_\mathrm{A}+F_\mathrm{B}}$, $\eta_\text{shed} \equiv 1-\eta_\text{route}$.
- Modal thermodynamics: $\{\lambda_k, \langle |c_k|^2\rangle\}$ and RJ fit $(T,\mu,R^2)$ in the post-collapse window.
- Optional numerics: JMJ two-grid slope and Strang-defect scaling.

Controls

- Symmetric geometry: $w_\mathrm{A}=w_\mathrm{B} \Rightarrow B\approx 0$.
- Local baseline: explicit local descent on $-\nabla L_h$ (same stencil and $\Delta t$), no DG correction.
- Injection robustness: (i) injection-site sweep (distance to funnel apex), (ii) two-source superposition test (split ratio invariance).

## Methods & Procedure

1. Geometry, BCs, and initial state

2. Steppers

3. Flux & efficiency accounting

4. Collapse detector & RJ fit

5. No-switch invariance

6. Injection robustness controls

## KPI Gates (must pass)

1. H-theorem monotonicity (metric step):  

- Gate: zero violations of $\Delta L_h \le 0$  
- Reporting: log violation count (must be 0) and max negative magnitude (should be 0); attach per-step CSV

1. No-switch identity (passive vs controller-disabled):  

- Gate: arrays identical at checkpoints (bitwise) or $\lVert\cdot\rVert_\infty \le 10^{-12}$  
- Provenance: hash raw buffers at checkpoints; store SHA-256; log any mismatches  
- Cadence: checkpoints every K steps (declare K in spec; default K=50)

1. RJ fit (spectral equilibrium diagnostic):  

- Gate: $S_k \propto \tfrac{T}{\lambda_k - \mu}$ with array-level $R^2 \ge 0.99$  
- Reporting: [k_min, k_max] used, residual lag-1 autocorrelation, short window-sensitivity sweep (3 windows) with R^2 spread  
- Notes: window sizes predeclared; no post hoc tuning; log all regression details

1. Routing bias (directional preference):  

- Gate: preregister scalar bias $B$ and fraction $\varrho$ with 95% CI excluding $0$ and margin $\delta$; report $(B,\varrho, \text{CI}, \delta)$  
- Controls: symmetric-geometry control must return ~0 bias within CI  

1. Energy-floor witness (efficiency):  

- Gate: final $L_h$ strictly below matched baseline; $\ge 5\sigma$; CI excludes $0$  
- Reporting: baseline pairing method, σ estimate method, CI details

1. Robustness battery:  

- Gates: symmetric-geometry control (~0 bias); injection-site monotone trend; two-source split (≤ 5% change)  
- Reporting: per-test CSV/JSON and a summary table with pass/fail

1. Determinism receipts:  

- Gate: single-thread numerics; deterministic FFT plans; environment audit line (threads, BLAS, FFTW/NumPy plan mode); checkpoint cadence + buffer hashes present in JSON  
- Reporting: include receipts in summary JSON and RESULTS; attach SHA-256 of artifacts

## Discrete Stability and Determinism

- Δt ladder: geometric ladder predeclared (e.g., [dt0, dt0/2, dt0/4, dt0/8]) with dt0 < 0.8/ω_max (discrete)
- Seeds: band-limited ensemble, preregistered; aggregation via median
- RNG: explicit seeding; record seed band in JSON
- Plans: enforce deterministic FFT/rFFT where used; disable multithreading in BLAS/FFT libs

## Artifacts and Routing

- Figures → `Derivation/code/outputs/figures/thermo_routing/<tag>/*.png`
- Logs (CSV/JSON) → `Derivation/code/outputs/logs/thermo_routing/<tag>/*.{csv,json}`
- Use `Derivation/code/common/io_paths.py` for all outputs; attach SHA-256 in JSON

## Approval and Governance

- Requires pre-approval in `Derivation/code/physics/thermo_routing/APPROVAL.json` (script-scoped HMAC)  
- Unapproved runs are quarantined and must not update canon  
- RESULTS must follow `Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md`

## Kill Plan (if a gate fails)

Order of triage:  

1. Verify determinism receipts (threads, FFT plans, buffer hashes, seeds)  
1. Re-check RJ windowing (no post hoc tuning; only predeclared windows)  
1. Inspect geometry masks and symmetric-control  
1. Check $\Delta t$ ladder vs discrete $\omega_\text{max}$; reduce $dt_0$ if needed  
1. Re-run with same seeds and updated spec; document changes in RESULTS

## Spec Outline (to create in `Derivation/code/physics/thermo_routing/specs/`)

- Grid/params: domain size, boundary conditions, λ_k operator, dt ladder, steps, checkpoints K  
- Seeds: band specification and seed list  
- Windows: RJ fit windows (3) and [k_min,k_max]  
- Bias definitions: B scalar and ρ fraction; symmetric-control config  
- Robustness tests: injection sites and two-source configuration  
- Tag: `thermo-routing-v2`

Example spec (path: `Derivation/code/physics/thermo_routing/specs/tr_v2.json`):


  Note: $\lambda_k$ are the discrete eigenvalues of the same Laplacian operator used in the run (FD-3pt vs spectral) under the run’s boundary conditions; RJ fits use exactly these $\lambda_k$ to avoid operator–spectrum mismatch.

  This is an optics-inspired thermodynamic routing analogue in a metriplectic RD medium; we borrow RJ-style diagnostics, not Maxwell’s equations.
  
```json
{
  "grid": {"Nx": 256, "Ny": 128, "Lx": 8.0, "Ly": 4.0, "stencil": "fd3"},
  "geometry": {"w_A": 0.6, "w_B": 0.3, "wall_gap": 0.1},
  "rd": {"D": 1.0, "r": 0.2, "u": 0.25},
  "ic": {"type": "packet", "x0": 0.5, "y0": 2.0, "sigma": 0.3, "amplitude": 1.0},
  "time": {"T": 10.0, "dt": 0.01, "checkpoints": 50},
  "analysis": {
    "collapse": {"zeta": 0.6, "dt_after": 0.5, "rj_window": 2.0},
    "rj_fit": {"kmin": 3, "kmax": 64, "r2_gate": 0.99, "windows": [1.0, 1.5, 2.0]}
  },
  "controls": {
    "symmetric_geometry": true,
    "injection_sweep": {"y_list": [1.0, 1.5, 2.0, 2.5, 3.0]},
    "two_source_split": {"ratios": [0.5, 0.6, 0.7, 0.8]}
  },
  "baseline": {"type": "local_descent"},
  "no_switch": true,
  "seeds": 40,
  "gates": {"delta_bias": 0.1, "eta_fraction": 0.1},
  "tag": "thermo-routing-v2"
}
```

## Expected Outputs (schemas to define)

- Summary JSON schema: includes all KPI fields above with pass/fail, receipts, env audit, artifact paths  
- Per-test CSVs: RJ regression details, ΔL_h per step, bias estimates with CIs, robustness summaries

## Appendix A: Optional JMJ/Strang-defect diagnostic (carried forward from earlier No-Switch draft)

Purpose: optional numerical diagnostic to sanity-check composition accuracy relative to the primary DG M-only step. This is diagnostic only and does not affect KPI gates above.

- Stepper: JMJ (Strang) composition — half-J, DG M, half-J; identical geometry/params; enable via a param-gated flag in the runner/spec.
- Measurements:
  - Two-grid residual slope versus Δt for JMJ, expecting ≈ 3 with R² ≥ 0.999.
  - Strang-defect slope comparing JMJ and MJM compositions, logged with fit diagnostics.
- Suggested artifacts (with standard CSV/JSON sidecars):
  - figures: `residual_vs_dt__jmj__{tag}.png`, `strang_defect_vs_dt__{tag}.png`
  - logs: slopes and regression details per step size with windowing noted
- Policy: keep optional; use same IO helper and tag routing; note in SUMMARY JSON if recorded.

---

By approving this pre-registration, we commit to these KPI gates and receipts; any deviation requires a new tag and spec.
