# PROPOSAL_SIE_Invariant_and_Novelty_v1.md

## 1. Proposal Title and date

**SIE Invariant and Novelty Pulse: Controlled Information Energy** - October 8, 2025

## 2. List of proposers and associated institutions/companies

Justin K. Lietz - VDM Project

## 3. Abstract

We certify a clean first integral (Q) for the local information engine (SIE) in the reaction-only limit and quantify controlled deviations under novelty. For logistic-like kinetics
[
\dot W=rW-uW^2,\qquad Q(W,t)=\ln!\frac{r-uW}{W}-rt,
]
(Q) is constant. With a brief parameter kick, (Q) drifts and returns. KPIs: (i) two-grid slope matches integrator order; (ii) (Q)-drift is bounded and reversible when the perturbation ends.

## 4. Background & Scientific Rationale

This converts “novelty/surprise” into a falsifiable, low-dimensional physics statement without any runtime. A clean invariant anchors the information-processing story to A5 (entropy/H-theorem analogs) and standard convergence theory.

## 5. Intellectual Merit and Procedure

Shows learning takes lawful steps locally; provides a meter for “surprise” as controlled deviation from an invariant.

## 5.1 Experimental Setup and Diagnostics

* **Domain:** `Derivation/code/physics/information/`
* **ODE:** as above; integrators: Euler and RK4.
* **Diagnostics:** two-grid error (E(\Delta t)), log–log slope; (Q)-drift time series with/without kick; recovery time.

## 5.2 Experimental runplan

* **Control:** run reaction-only, sweep (\Delta t). Gate: slope (\ge p+1-0.1), (R^2\ge 0.999); max (|Q(t)-Q(0)|\le 10^{-8}) (RK4) / (10^{-5}) (Euler).
* **Novelty:** apply a brief change (r\to r+\delta r(t)); measure peak drift and recovery to baseline. Gate: bounded peak; 95% recovery within predicted relaxation time (1/r).
* **Failure plan:** reduce (\Delta t) or tighten tolerances; log CONTRADICTION_REPORT.
* **Publication:** RESULTS with invariant plots and drift overlays.

## 6. Personnel

Justin K. Lietz.

## 7. References

logarithmic_constant_of_motion.md; EQUATIONS.md; Axiomatic_theory_development.md.

---
