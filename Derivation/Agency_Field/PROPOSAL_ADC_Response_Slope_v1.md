# PROPOSAL_ADC_Response_Slope_v1.md

## 1. Proposal Title and date

**ADC Response Function: Logistic Slope Equals (\Theta)** - October 8, 2025

## 2. List of proposers and associated institutions/companies

Justin K. Lietz - VDM Project

## 3. Abstract

We test the decision coupling law at forks: the probability of choosing branch (A) is
[
P(A)=\sigma!\big(\Theta,\Delta m\big),\quad \Delta m=m_A-m_B.
]
We will generate controlled junctions with prescribed (\Delta m), record choices, and verify that the **fitted logistic slope equals the programmed (\Theta)** within (\pm5%). This upgrades prior A6 collapse (shape) to a parameter-identification test (slope).

## 4. Background & Scientific Rationale

The A6 logistic universality is established; tying slope to (\Theta) connects meso-scale agency to micro-level steering gain. This is a necessary calibration for coupling agency to tasks and environments.

## 5. Intellectual Merit and Procedure

Identifies a physical constant in the decision law; rigorous via CI bounds and replication.

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
* **Geometry:** 1D/2D Y-junctions; static (m) fields defining (\Delta m).
* **Trials:** fixed number per (\Delta m) bin; seeds for stochasticity.
* **Diagnostics:** logistic regression of outcomes vs (\Delta m); slope (\hat\Theta) with CI; KS test for model adequacy.

## 5.2 Experimental runplan

* For (\Theta\in{0.5,1.0,2.0}), run trials across (\Delta m\in[-\Delta,\Delta]).
* Fit (P=\sigma(\hat\Theta,\Delta m)).
* **Gates:** (|\hat\Theta/\Theta-1|\le 0.05); (R^2\ge 0.99); KS (p>0.1).
* **Failure plan:** increase sample sizes or reduce noise; document deviations.
* **Publication:** RESULTS with ROC overlays, slope table, artifact paths.

## 6. Personnel

Justin K. Lietz.

## 7. References

RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md; Agency_Field.md; EQUATIONS.md (A6).

---
