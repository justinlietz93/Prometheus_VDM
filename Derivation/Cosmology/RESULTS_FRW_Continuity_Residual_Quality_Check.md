<!-- DOC-GUARD: REFERENCE -->
# FRW Continuity Residual - Quality Check (v1)

> Author: Justin K. Lietz  
> Date: 2025-10-06  
> Commit: a54d638e2b097cd6bf5606d669fc9984650e2307  
> License: Dual-license; see LICENSE. Commercial use requires citation and written permission.

## TL;DR

- Gate tested: FRW dust continuity residual $\mathrm{RMS}_{\mathrm{FRW}}\le 10^{-6}$.  
- Outcome: PASS with $\mathrm{RMS}_{\mathrm{FRW}}\approx 9.04\times 10^{-16}$.  
- Artifact (one-click): `derivation/code/outputs/figures/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.png`

## Introduction

This note quality-controls the Friedman-Robertson-Walker (FRW) continuity bookkeeping for the dust control ($w=0$). For pressureless matter, $\rho(a) \propto a^{-3}$, implying exact conservation of $\rho a^3$. We validate that the discretized residual is at machine precision on a synthetic series, establishing a baseline before adding sources or curvature.

Scope: This is a QC-only experiment. No cosmological inference is attempted; we strictly test a bookkeeping identity under controlled conditions.

## Research question

To what extent does the FRW dust control satisfy the continuity identity, quantified by the RMS residual $\mathrm{RMS}_{\mathrm{FRW}}$ with units of energy density times volume per unit time [e.g., J·m$^{0}$·s$^{-1}$ in SI], and does it pass the gate $\mathrm{RMS}_{\mathrm{FRW}} \le 10^{-6}$ (dimensionless after normalization)? Measurement uses a synthetic analytic series sampled uniformly in time.

## Background information (focused)

- Continuity identity (dust): $\frac{d}{dt}(\rho a^3)=0$ when $p=w\,\rho$ with $w=0$.  
  Core residual used for QC: $r(t)=\frac{d}{dt}(\rho a^3)+w\,\rho\,\frac{d}{dt}(a^3)$, evaluated with $w=0$.
- Minimal equations:  
  1) $\rho(a)=\rho_0\,a^{-3}$ (definition of dust scaling).  
  2) $\mathrm{RMS}_{\mathrm{FRW}}=\sqrt{\langle r(t)^2\rangle_t}$.  
  Map-to-gate: Identity $\Rightarrow r(t)=0\ \forall t \Rightarrow \mathrm{RMS}_{\mathrm{FRW}}=0$; discretely, expect machine-precision residual.

References: Standard cosmology texts (e.g., Weinberg, Cosmology, 2008), and FRW conservation identities.

## Variables

- Independent: time index $t_k$ (s), sampling cadence $\Delta t$ (s).  
- Dependent: residual $r(t_k)$ (normalized units).  
- Controls: equation-of-state parameter $w{=}0$ (dust), analytic $\rho\propto a^{-3}$ series, consistent $a(t)$ evaluation.  
- Instrument model: numerical differentiation of $\rho a^3$ by central differences; uncertainty dominated by floating-point roundoff and discretization error $\mathcal{O}(\Delta t^2)$.

Control variables table:

| Variable | How controlled | Rationale |
|---|---|---|
| Equation of state $w$ | Fixed to 0 (dust) | Tests the identity $\frac{d}{dt}(\rho a^3)=0$ |
| Scaling law $\rho(a)$ | $\rho_0 a^{-3}$ analytically | Removes modeling ambiguity; sets exact target |
| Time grid | Uniform $\Delta t$ | Ensures consistent finite-difference truncation |
| Differentiation | Central differences | Second-order accurate; symmetric error |

## Equipment / Software

- Software runner: `derivation/code/physics/cosmology/run_frw_balance.py`  
- Environment: Python scientific stack; double precision floats; Git commit a54d638.

## Methods / Procedure

1. Generate synthetic series with $a(t)$ and $\rho(t){=}\rho_0 a(t)^{-3}$; fix $w{=}0$.  
2. Compute $r(t){=}\tfrac{d}{dt}(\rho a^3)+w\,\rho\,\tfrac{d}{dt}(a^3)$ via finite differences.  
3. Compute $\mathrm{RMS}_{\mathrm{FRW}}=\sqrt{\langle r^2\rangle}$.  
4. Compare to gate threshold $10^{-6}$.  
5. Emit artifacts: PNG plot of $r(t)$, CSV of time series, JSON log with params and gate outcome.

Risk assessment (safety/ethics/environment): Software-only QC with synthetic data. Risks limited to methodological errors; mitigations include gate with contradiction report routing on failure and pinned artifacts for audit.

Risk and integrity: If gate fails, artifacts route to `failed_runs/` and a contradiction report is emitted by the runner; no claims are made.

## Data and artifacts (pinned)

- Figure: `derivation/code/outputs/figures/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.png`
- CSV: `derivation/code/outputs/logs/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.csv`
- Log (JSON): `derivation/code/outputs/logs/cosmology/20251006_175329_frw_balance__FRW-balance-v1.json`

Each figure is paired with CSV/JSON; the log includes parameters, RMS value, and pass/fail.

## Results / Data

- Measured: $\mathrm{RMS}_{\mathrm{FRW}}=9.04\times 10^{-16}$ (dimensionless in normalized units).  
- Gate: PASS since $9.04\times 10^{-16} \le 10^{-6}$.

Summary table:

| Metric | Value |
|---|---|
| $\mathrm{RMS}_{\mathrm{FRW}}$ | $9.04\times 10^{-16}$ |
| Gate threshold | $10^{-6}$ |
| Pass/Fail | PASS |

Figure 1 caption: Continuity residual $r(t)$ over the synthetic series; machine-precision fluctuations consistent with roundoff. RMS and threshold are annotated in the JSON log.

Sample calculation: Given a residual vector $\{r_k\}_{k=1}^{N}$,  
$$
\mathrm{RMS}_{\mathrm{FRW}}=\sqrt{\frac{1}{N}\sum_{k=1}^{N} r_k^2}.
$$

## Uncertainties and limitations

- Numerical: dominated by double-precision roundoff and finite-difference truncation; consistent with machine precision.  
- Modeling: synthetic analytic dust control only; no curvature, radiation, or sources.  
- Scope: this QC does not constrain cosmological parameters; it only validates bookkeeping.

## Discussion / Analysis

The machine-scale residual confirms correct implementation of the dust continuity identity. This passes the pre-registered gate and supports extending the check to sourced continuity (e.g., retarded sources) and to other $w$ values. Any future deviation at similar resolution would indicate a discretization or implementation defect.

## Conclusions

The FRW dust control QC passes with $\mathrm{RMS}_{\mathrm{FRW}}\sim10^{-15}$, establishing a solid baseline. Next: introduce source terms and verify residuals remain within a tightened tolerance derived from analytic expectations or manufactured solutions.

## Reproducibility

- Runner: `derivation/code/physics/cosmology/run_frw_balance.py`  
- Commit: a54d638e2b097cd6bf5606d669fc9984650e2307  
- Floating-point: IEEE-754 double precision  
- RNG: Not used (deterministic synthetic control)  
- Artifacts: figure/CSV/log pinned above; CSV provides full time series of residuals.

## References

- S. Weinberg, Cosmology, Oxford University Press (2008).  
- Standard FRW continuity identities in cosmology reviews.
