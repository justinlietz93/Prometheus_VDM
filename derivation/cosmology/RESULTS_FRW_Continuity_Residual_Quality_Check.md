<!-- DOC-GUARD: REFERENCE -->
# FRW Continuity Residual — Quality Check (v1)

> Author: Justin K. Lietz  
> Date: 2025-10-06

## Introduction

Goal: validate background bookkeeping by measuring the RMS residual of the FRW continuity equation for the dust control ($w=0$). We use a synthetic sanity series with $\rho \propto a^{-3}$ so the residual should be at machine precision.

## Methods

- Runner: `derivation/code/physics/cosmology/run_frw_balance.py`
- Residual: $r(t) = \tfrac{d}{dt}(\rho a^3) + w\,\rho\, \tfrac{d}{dt}(a^3)$ with $w=0$ (dust)
- Metric: RMS residual `RMS_FRW = sqrt(mean(r^2))`
- Gate: `RMS_FRW ≤ tol_rms` (default `1e−6`)

## Artifacts (pinned)

- Figure: `derivation/code/outputs/figures/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.png`
- CSV: `derivation/code/outputs/logs/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.csv`
- Log: `derivation/code/outputs/logs/cosmology/20251006_175329_frw_balance__FRW-balance-v1.json`

## Results

- Measured RMS: $9.04\times 10^{-16}$ (double precision scale)
- Gate: PASS (≤ 1e−6)

## Conclusions

The dust control passes with machine-precision residuals, establishing a clean baseline for extending the continuity check to sourced cases. Future work: add retarded-source channel(s) and extend the residual accordingly.
