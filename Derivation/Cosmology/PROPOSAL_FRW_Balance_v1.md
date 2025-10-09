# FRW Continuity Balance - Proposal (v1)

Author: Justin K. Lietz
Date: 2025-10-06

## 1. Proposal Title and date

FRW Continuity Residual Quality Check (v1) - 2025-10-06

## 2. Proposers and institutions

Justin K. Lietz - Neuroca, Inc.

## 3. Abstract

We will implement a simple, dimensionless continuity-law residual for FRW cosmology, testing discrete consistency of input (ρ(t), a(t)). The diagnostic computes the residual of d/dt(ρ a³) + w ρ d/dt(a³) (default dust w=0) and gates PASS when the RMS residual ≤ tolerance. This provides a low-cost sanity check for background bookkeeping prior to full cosmological embeddings.

## 4. Background & Scientific Rationale

Energy conservation in FRW for a perfect fluid obeys \( \frac{d}{dt}(\rho a^3) + p \frac{d}{dt}(a^3) = 0 \). For an effective equation-of-state parameter w with p = w ρ, this becomes \( \frac{d}{dt}(\rho a^3) + w\rho \frac{d}{dt}(a^3) = 0 \). Our diagnostic computes a finite-difference residual of the LHS and reports RMS; a reference dust case (ρ ∝ a⁻³) should yield residuals near machine precision.

## 5.1 Experimental Setup and Diagnostics

- Input: arrays ρ(t), a(t), t covering a monotone time span.
- Default test: dust (ρ ∝ a⁻³).
- Output: figure of residual vs t, CSV with (t, ρ, a, residual), JSON summary and PASS/FAIL vs tol.
- Gate: RMS residual ≤ tol (default 1e-6); emit CONTRADICTION_REPORT on fail.

Artifacts (tag FRW-balance-v1):

- Figure: derivation/code/outputs/figures/metriplectic/.../frw_continuity_residual__FRW-balance-v1.png
- CSV: derivation/code/outputs/logs/metriplectic/.../frw_continuity_residual__FRW-balance-v1.csv
- JSON: derivation/code/outputs/logs/metriplectic/.../frw_balance__FRW-balance-v1.json

## 5.2 Experimental runplan

- Implement the residual calculator using numpy.gradient; validate against dust.
- Evaluate supplied time series as needed; summarize RMS and decide PASS/FAIL.
- Publication: include residual plot and a small table of RMS vs tol.

## 6. Personnel

Justin K. Lietz - implementation, execution, and documentation; integrate with broader FRW bookkeeping checks.

## 7. References

- Standard FRW continuity equation; internal notes on background bookkeeping and transfer currents in this repository.
