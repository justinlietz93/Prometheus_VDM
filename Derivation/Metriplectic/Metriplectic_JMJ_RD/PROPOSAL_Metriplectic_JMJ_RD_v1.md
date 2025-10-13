# 1. **Metriplectic Integrator for Mixed Conservative-Dissipative Dynamics: Symplectic J-step ⊕ Discrete-Gradient M-step**

**Date:** 2025-10-06 12:55:11Z

## 2. List of proposers and associated institutions/companies

**Justin K. Lietz** - VDM Project (Independent Researcher)

## 3. Abstract

We propose to implement and certify a **metriplectic time integrator** that composes a **symplectic step** for the conservative (J) sector with a **discrete-gradient (DG) step** for the dissipative (M) sector:
$J(\Delta t/2) \to M(\Delta t) \to J(\Delta t/2)$ (Strang composition).
The J-step preserves Noether invariants (to machine precision) and is time-reversible/volume-preserving; the M-step enforces an exact discrete H-theorem via the DG chain rule for the reaction-diffusion (RD) Lyapunov functional. Diagnostics reuse the RD harness just completed (two-grid order, fixed-$\Delta t$ $|\Delta S|$, Lyapunov monitors) **without modifying any prior scripts or outputs** to preserve reproducibility; new code paths are additive (new module/CLI only) and write to separate output folders. Success yields a scheme that mirrors A4/A5 at the discrete level: conserved quantities for J and monotone entropy for M, with global second-order accuracy for the composition.

## 4. Background & Scientific Rationale

**Context.** The RD study established: (i) scheme-dependent near-conservation (Euler$\approx2$, Strang$\approx3$ two-grid slopes), (ii) no exact global invariant for Euler RD within tested $Q'$/$H$ classes (contradiction report), and (iii) a DG RD step that certifiably obeys a per-step H-theorem with identity residuals at machine precision. This motivates metriplectic composition: keep conservative structure in a **symplectic** update and dissipative structure in a **DG** update, then compose.

**Scientific aim.** Produce a **single-step update** that: (1) preserves Noether invariants (energy/momentum or action) in the J substep, (2) provably decreases the RD Lyapunov in the M substep via a discrete chain rule, and (3) achieves global order $\approx2$ under Strang composition. This aligns the runtime with the axioms: symplectic $+$ metric generators, entropy non-decrease, locality, and measurable acceptance gates.

**Reproducibility constraint.** To avoid perturbing prior results, we will not change existing RD scripts or logs. We will add **new** files and CLI endpoints, and write to **new output directories**. The existing RESULTS document remains reproducible byte-for-byte.

## 5.1 Experimental Setup and Diagnostics

**State & domains.** 1D periodic lattice with spacing $\Delta x$ and size $N$. Primary field $W$ (or $(\phi,\pi)$ for an optional two-field J-test).

**Functionals.**

- **J Hamiltonian (example choices):**
  - linear wave/transport surrogate for $W$ with
    $$ H_J \;=\; \tfrac{c^2}{2}\,\|\nabla_h W\|^2. $$
  - two-field KG toy
    $$ H_J \;=\; \tfrac12\|\pi\|^2 + \tfrac12 c^2\|\nabla_h \phi\|^2 + \tfrac12 m^2\|\phi\|^2. $$
- **M Lyapunov (RD):**
  $$ L_h[W] \;=\; \sum_i \Big( \tfrac{D}{2}\,|\nabla_h W_i|^2 + \hat V(W_i) \Big)\,\Delta x, \quad
     \hat V'(W) \;=\; -f(W) \;=\; -(r W - u W^2). $$

**Schemes.**

- **J-step (symplectic):** leapfrog/Verlet (J-only certification also checks time-reversibility: step $\Delta t$ then $-\Delta t$ $\to$ original state).
- **M-step (DG RD):** midpoint Laplacian (quadratic exact), AVF discrete gradient for $\hat V(W)$:
  $$ \hat V'_{\mathrm{DG}}(W^n, W^{n+1}) \;=\; -\,r\,\tfrac{W^{n+1}+W^n}{2} + u\,\tfrac{(W^{n+1})^2 + W^{n+1}W^n + (W^n)^2}{3}. $$
  Newton solve with line-search/backtracking; stats recorded (iterations, residuals).
- **Composition:** **Strang** $J(\Delta t/2) \to M(\Delta t) \to J(\Delta t/2)$.

**Diagnostics (each with PNG $+$ CSV/JSON artifacts).**

- **Obj-B (order):** two-grid error
  $$ E(\Delta t) \;=\; \big\| \Phi_{\Delta t}(W_0) - \Phi_{\Delta t/2}\!\big(\Phi_{\Delta t/2}(W_0)\big) \big\|_\infty $$
  for J-only, M-only, and $J\oplus M$ (expect slopes $\approx2$ for Strang; J-only slope depends on the chosen J stepper but is symplectic and typically second order; M-only DG behaves as order $\approx2$ in practice).
- **Noether (J-only):** invariants and reversibility: max per-step drift $\le 10^{-12}$; forward-then-reverse error $\le 10^{-12}$.
- **H-theorem (M, and $J\oplus M$):** per-step
  $$ L_h(W^{n+1}) - L_h(W^n) \;=\; -\,\Delta t\,\|\bar\nabla L_h\|^2 \;\le\; 0, $$
  and **DG identity residuals** (energy and dot-product forms) $\le 10^{-12}$.
- **Mass/flux control:** diffusion-only mass conservation at machine epsilon (antisymmetric edge flux).
- **Provenance:** commit hash, environment, seeds, BC, stencil, scheme; `step_spec_snapshot` saved.

**I/O layout (additive; preserves prior work).**

```plaintext
Derivation/code/physics/metriplectic/
      configs/step_spec.metriplectic.example.json
Derivation/code/outputs/figures/metriplectic/
      two_grid_error_vs_dt_{scheme}.png
      lyapunov_delta_per_step_{scheme}.png
      fixed_dt_deltaS_compare.png
Derivation/code/outputs/logs/metriplectic/
      step_spec_snapshot.json
      sweep_dt_{scheme}.json            # two-grid slopes + R²
      lyapunov_series_{scheme}.json     # with DG identity residuals (if scheme includes DG)
      *.json
      *.csv
```

No existing RD files are touched; paths are new and names are scheme-suffixed.

## 5.2 Experimental runplan

1) Implement J-step in a new module (e.g., `metriplectic/j_step.py`) and a composer (e.g., `metriplectic/compose.py`). Do **not** edit existing RD runners; add a new script `run_metriplectic.py` (CLI flags mirror RD harness).
2) **Controls & certifications.**
   - J-only: Noether invariants ($\le 10^{-12}$), time-reversibility ($\le 10^{-12}$).
   - M-only: DG Lyapunov identities ($\le 10^{-12}$), $\Delta L_h \le 0$ per step, diffusion mass.
3) **Obj-B (order) sweeps:** two-grid $E(\Delta t)$ for J-only, M-only, $J\oplus M$; fit slope and $R^2$ using the established fitter (median over seeds).
4) **Fixed-$\Delta t$ $|\Delta S|$ compare:** Euler vs Strang vs DG vs $J\oplus M$ at common $\Delta t$ to visualize scheme-dependence of near-conservation (for $S$ built from $Q$ and $H$ if desired).
5) **Parameter mini-grid:** run $\ge 3$ tuples of $(r,u,D,N)$, $N\in\{64,128\}$; periodic BC only.
6) **Outputs & write-up:** PNGs with numeric captions; CSV/JSON pairs; one pinned artifact path per subsection; follow PAPER_STANDARDS.

**Estimated runtime.** Comparable to RD sweeps; DG/Newton costs are modest for 1D $N\le 128$.

## 6. Personnel

**Justin K. Lietz** - design, implementation (new modules only), CAS/analysis, and write-up. No changes to prior RD scripts; reproducibility preserved.

## 7. References

- Prior RD results document (canonical reference for harness, gates, and artifact style).
- Symplectic (Verlet/leapfrog) and discrete-gradient/AVF methods (to be cited in the paper).
- PAPER_STANDARDS.md for figure/CSV pairing, numeric captions, provenance, and acceptance gate reporting.
