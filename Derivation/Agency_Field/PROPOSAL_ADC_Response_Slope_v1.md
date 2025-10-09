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
