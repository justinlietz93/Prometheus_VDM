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
