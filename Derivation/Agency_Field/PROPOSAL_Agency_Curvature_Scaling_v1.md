# PROPOSAL_Agency_Curvature_Scaling_v1.md

## 1. Proposal Title and date

**Agency Curvature Scaling: Steering Law Validation** - October 8, 2025

## 2. List of proposers and associated institutions/companies

Justin K. Lietz - VDM Project

## 3. Abstract

We propose to validate the steering component of the agency field by measuring path curvature of test pulses moving in a memory field (m(x)). The theory predicts curvature (\kappa_{\text{path}}) scales linearly with the transverse gradient magnitude (X=\Theta,|\nabla_\perp m|), independent of pulse details. We will generate smooth (m), launch narrow pulses, and fit (\kappa)–vs–(X) across (\Theta) to demonstrate a scaling collapse and quantify residuals. Primary KPI: linear fit slope stability within (\pm 10%) and (R^2 \ge 0.99).

## 4. Background & Scientific Rationale

The agency/steering law posits a slow bias field that deflects trajectories:
[
\mathbf r''(t)=\Theta,\nabla_\perp m(\mathbf r(t)) \quad\Rightarrow\quad \kappa_{\text{path}}\propto \Theta,|\nabla_\perp m|.
]
This provides an operational measure of goal-directedness: stronger, consistent bias yields reproducible curvature irrespective of carrier dynamics. Demonstrating a dimensionless collapse validates that agency is a physical field with predictable transport.

**Novelty.** Prior work established RD/metriplectic correctness; this isolates **steering** as a macroscopic observable.
**Necessity.** Without a curvature law, “agency” remains qualitative.
**Targets.** Slope equality across (\Theta) and gradient bands; budget consistency in follow-ups.
**Impact.** Enables portable measurement of agency without runtime internals.
**Critiques.** Grid artifacts can pollute curvature; we mitigate with smoothing and sub-step reconstruction.

## 5. Intellectual Merit and Procedure

(1) The question is central to agency as physics; (2) success enables cross-substrate comparison; (3) approach is simple, falsifiable; (4) rigor via two-grid convergence and goodness-of-fit gates.

## 5.1 Experimental Setup and Diagnostics

## Pre‑flight A4 hygiene (agency field) — **must pass before any main run**

**0) Abort policy (always on).**
If any gate fails: stop run, write `CONTRADICTION_REPORT.json` with seed, grid, dt, hash of spec, failing metric, and nearest checkpoints for replay.

**1) J‑only limb (steering on, dissipation off).**
Toggle the agency PDE to the conservative branch (or the J‑coupled parent it actuates).

* **Time‑reversal:** advance (+Δt) then (−Δt). Require
  `||q_back − q0||_∞ ≤ c_eps * sqrt(N) * eps_mach` (e.g., `c_eps = 20`).
* **Noether drift:** pick the discrete invariant tied to the J‑coupled part; require
  `median_rel_drift ≤ 1e−8`, 99th percentile ≤ `5e−8`.
* **Dispersion / linearization sanity (optional but recommended):** measured ω(k) within a 2% band on well‑resolved modes.

**2) M‑only limb (steering off, dissipation on).**

* **H‑theorem (per‑step):** `ΔSigma ≤ 0` with identity residuals from the discrete‑gradient step at or below `1e−12`.
* **Lyapunov budget:** cumulative `Sigma(t)` monotone to within machine jitter; flag any up‑spike beyond `5e−13` as fail.

**3) A4 structural orthogonality (degeneracies).**

* **Skew / PSD:** random‑vector tests:
  `median |vᵀ(J+Jᵀ)v| / ||v||² ≤ 1e−12`; count of negative eigenvalues of M = 0 (within numerical tolerance; allow ≥ −1e−14 for round‑off).
* **Functional degeneracies:** finite‑difference probes of state‑local gradients:
  `||J · ∇Sigma||_∞ ≤ 1e−10`, `||M · ∇I||_∞ ≤ 1e−10` (same stencil used in the step).
  *(These are the metriplectic “wires don’t cross” checks.)*

**4) Composition sanity (if you JMJ inside any agency loop).**

* **Strang‑defect slope:** tiny Δt sweep, fit log(error) vs log(Δt): slope p in `[2.8, 3.2]` and `R² ≥ 0.999`.
  *(This is the same “instrument discipline” you used to certify JMJ previously.)*

**5) Locality / causality bound (A2).**

* **Light‑cone growth:** support radius must obey
  `R(t) ≤ R(0) + c_max * t + κ * Δt` with `c_max` from the linearized J‑branch and κ a small numerical cushion (e.g., 2 grid cells per 1000 steps). Any superluminal spill is a fail.

**6) Scale program smoke (A6).**

* **Scaling collapse:** pick one dimensionless group (e.g., Δt·λ_J or loss_depth/step_size) and show curves collapse to within `MAD ≤ 5%` after rescaling. If not, abort—your plots aren’t in the right variables yet.

**7) CEG‑specific fairness & safety (only when you enable assistance).**

* **Energy budget match:** the assisted rewind must spend the same integrated “effort” as baseline within `≤ 0.5%`. (Define the budget once—e.g., integral of control norm or equivalent.)
* **Referee check:** conservation drift stays within the J‑only envelope; M‑monotonicity stays non‑positive per step (no borrowed entropy).
* **Ablations ready:** a) assistance off (baseline), b) assistance with shuffled model (scramble J or M), c) random micro‑sequence with same budget. If (b,c) give similar gains, halt: the “intent” evidence is contaminated.
* **Time‑reversal line:** spell the norm fully and include a numeric constant so reviewers can rerun and agree on the exact threshold.
* **Noether drift:** specify median *and* tail (99th percentile) to avoid a one‑frame outlier slipping through.
* **Degeneracies:** test both algebra (J skew / M PSD) and functionals (J·∇Sigma = 0, M·∇I = 0). The second one is the one people forget.
* **Composition slope:** put a narrow p‑band and an R² floor; it reads as a real gate, not a vibe.
* **Locality + scaling:** these are A2/A6 and complete the axiom set for “meters are honest” before we measure CEG.

### One‑screen “CEG fairness pre‑flight”

* Budget equalized (±0.5%).
* Conservation drift inside J‑only envelope.
* Σ never increases per M‑step (machine‑jitter wiggle allowed).
* Assistance ablations queued (scramble‑J, scramble‑M, random but budget‑matched).
* If any ablation ≈ assisted, **stop** and post a contradiction report.

* **Domain:** `Derivation/code/physics/agency/`
* **Fields:** static (m(x,y)) (Gaussian ridge, band-limited noise, and linear ramp variants).
* **Carriers:** narrow scalar pulses (\phi) propagated with a stable, second-order scheme (unspecified kinetics; we only log centerline).
* **Parameters:** (\Theta\in{0.5,1.0,2.0}), gradient bins (X).
* **Diagnostics:** centerline extraction; discrete curvature; linear regression (\kappa) vs (X); collapse across (\Theta). One PNG + CSV + JSON per run.

## 5.2 Experimental runplan

* Generate (m); compute (|\nabla m|).
* Emit pulses; extract trajectories (\mathbf r(t)); compute (\kappa(t)).
* Bin by (X); fit (\kappa=\alpha X + \beta).
* **Gates:** (|\beta|\le 0.05,\alpha,\bar X); slope CV (\le 10%) across (\Theta); (R^2\ge 0.99).
* **Failure plan:** if gates fail, increase resolution, reduce pulse width, or smooth (m) until grid error falls; record CONTRADICTION_REPORT.
* **Publication:** RESULTS page with MathJax, pinned artifacts, and regression tables (see `PAPER_STANDARDS.md`).

## 6. Personnel

Justin K. Lietz: design, implementation, analysis, and write-up.

## 7. References

Agency_Field.md; EQUATIONS.md (steering/agency sections); Axiomatic_theory_development.md (A0–A7).

---
