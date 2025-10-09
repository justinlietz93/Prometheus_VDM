# PROPOSAL_Agency_Stability_Band_v1.md

## 1. Proposal Title and date

**Agency Stability Band: ((D_a,\Lambda,\Gamma)) Map** - October 8, 2025

## 2. List of proposers and associated institutions/companies

Justin K. Lietz - VDM Project

## 3. Abstract

We will map the stability/retention regime of the memory/agency substrate predicted by the dimensionless groups (D_a) (advective/steering), (\Lambda) (loss/decay), and (\Gamma) (diffusion/spread). The memory field (m) obeys
[
\partial_t m=\gamma R - \delta m + \kappa\nabla^2 m,
]
with (R) as localized writes. We predict stable, high-SNR retention when (D_a\gtrsim \Lambda) at intermediate (\Gamma). KPI: a distinct band in the ((D_a,\Lambda)) plane with retention (>0.8) and boundary reproducibility under parameter sweeps.

## 4. Background & Scientific Rationale

Memory steering requires a persistent field (m) that is neither washed out (too diffusive) nor sticky (too slow to adapt). Casting the PDE in dimensionless form yields a stability band. Establishing this band experimentally ties “memory” to measurable physics.

## 5. Intellectual Merit and Procedure

Clarifies controllable levers for agency retention; falsifiable via heat-map boundaries and cross-checks.

## 5.1 Experimental Setup and Diagnostics

* **Domain:** `Derivation/code/physics/agency/`
* **PDE:** as above; sources (R) are Gaussian writes at fixed intervals.
* **Dimensionless groups:** compute (D_a,\Lambda,\Gamma) from ((\Theta,\gamma,\delta,\kappa)).
* **Diagnostics:** retention metric (peak/plateau ratio), half-life, spatial SNR. Heatmap over a grid of ((\gamma,\delta,\kappa)).

## 5.2 Experimental runplan

* Sweep (\gamma,\delta,\kappa) over log-spaced grids.
* Compute ((D_a,\Lambda,\Gamma)), retention metrics.
* **Gates:** contiguous band where retention (>0.8), half-life within target window, and cross-slice reproducibility (Jaccard index (\ge 0.7)).
* **Failure plan:** adjust write cadence or amplitude to decouple confounds; record CONTRADICTION_REPORT.
* **Publication:** RESULTS with band plot, slices, and table of boundary thresholds.

## 6. Personnel

Justin K. Lietz.

## 7. References

Agency_Field.md; EQUATIONS.md (memory law).

---
