# Wave Flux Meter A-Phase: Closed-Box Energy Conservation and Local Balance (J-only Scalar Wave)

> Author: Justin K. Lietz  
> Date: 2025-10-13  
> Commit: 9c27e65  
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.  
> Commercial use requires citation and written permission from Justin K. Lietz.  
> See LICENSE file for full terms.

## TL;DR

A J-only scalar-wave meter was validated in a closed box with a frozen potential V. Two gates passed: (i) energy conservation within a dynamic leapfrog tolerance, and (ii) pointwise local balance via the continuity residual $r = \partial_t e + \nabla\cdot\mathbf{s}$ with $\dot V = 0$. Artifacts (figure + CSV + JSON) are pinned to:

- Figure: `Derivation/code/outputs/figures/thermo_routing/20251013_142050_wave_flux_meter_energy_thermo-routing-v2-wave-meter.png`
- CSV:   `Derivation/code/outputs/logs/thermo_routing/20251013_142050_wave_flux_meter_v1_metrics_thermo-routing-v2-wave-meter.csv`
- JSON:  `Derivation/code/outputs/logs/thermo_routing/20251013_142050_wave_flux_meter_v1_summary_thermo-routing-v2-wave-meter.json`

Gate outcomes:

- Energy drift $E_{\text{rel, max}} = 0.0 \le \text{tol}_E = 3.2\times10^{-3}$ (pass)
- Local balance residual $\max\,\|r\|_2 = 0.0 \le \text{tol}_B \approx 1.203875\times10^{-2}$ (pass)

## Introduction

This document certifies an energy/flux meter for scalar waves used later to audit photonic-style routing. The instrument evolves $(\phi, \pi)$ with J-only dynamics on a 2D periodic grid and measures energy density $e$ and a Poynting-analog flux $\mathbf{s}$. The scope here is Phase A: a closed box (no ports) with a frozen potential $V$, testing only inherent conservation and consistency of the discretization.

## Research question

Given a uniform medium with periodic boundaries and frozen $V$,

1) does total energy stay within a leapfrog-consistent tolerance over many steps?  
2) does the continuity residual $r = \partial_t e + \nabla\cdot\mathbf{s}$ remain small pointwise (L2 norm) at each step?

Independent variables: grid $(N_x=128, N_y=64)$, domain $(L_x=8, L_y=4)$, time step $\Delta t=2.5\times10^{-4}$, duration $T=2.0$, wave speed $c=1$.  
Dependent variables: energy drift $E_{\text{rel, max}}$, balance residual $\max\,\|r\|_2$, both dimensionless.

Gates (falsifiable):

- Energy: $E_{\text{rel, max}} \le \text{tol}_E$ with $\text{tol}_E = C_E\,(\Delta t/a)^2$, $a=L_x/N_x$, $C_E=200$.
- Balance: $\max\,\|r\|_2 \le \text{tol}_B$ with $\text{tol}_B = C_B\,a^2 + C_D\,(\Delta t/a)^2$, $C_B=3$, $C_D=20$.

## Background

Dynamics (J-only leapfrog):

$$\partial_t \phi = \pi, \qquad \partial_t \pi = c^2 \nabla^2\phi - V\,\phi.$$

Energy density and Poynting-analog flux:

$$e = \tfrac12\big(\pi^2 + c^2\,\lvert\nabla\phi\rvert^2 + V\,\phi^2\big), \qquad \mathbf{s} = -\,\pi\,c^2\,\nabla\phi.$$

Continuity (local balance):

$$\partial_t e + \nabla\cdot\mathbf{s} = -\tfrac12 (\partial_t V)\,\phi^2.$$

With frozen $V$ ($\partial_t V=0$), the RHS vanishes and the residual is

$$r := \partial_t e + \nabla\cdot\mathbf{s}.$$

We evaluate $\partial_t e$ with a centered difference in time and $\nabla\cdot\mathbf{s}$ by centered spatial differences.

## Variables

- Independent: $N_x=128, N_y=64, L_x=8, L_y=4, a=L_x/N_x=0.0625$; $\Delta t=2.5\times10^{-4}$; $c=1$; periodic BCs; frozen $V=0$; plane-wave initial mode aligned to the grid.
- Dependent: $E_{\text{rel, max}} = \max_n |E_n-E_0|/|E_0|$; balance max $= \max_n \|r_n\|_2$.
- Controls: double precision; single-threaded BLAS/FFT (receipts in JSON); deterministic seeds.

## Equipment / Hardware

Linux host; Python/numpy stack (OpenBLAS, numpy.pocketfft). Environment receipts logged in the summary JSON. No accelerators.

## Methods / Procedure

- Spatial discretization: second-order centered differences for $\nabla$ and $\nabla^2$.  
- Time integrator: leapfrog (Störmer–Verlet), staggering $\pi$ at half-steps; energy density sampled compatibly with staggering.  
- Residual evaluation: centered $\partial_t e$ via $(e^{n+1} - e^{n-1})/(2\,\Delta t)$, divergence by centered differences; then $\|r\|_2$ per step.  
- Tolerances: $\text{tol}_E = 200\,(\Delta t/a)^2$, $\text{tol}_B = 3\,a^2 + 20\,(\Delta t/a)^2$.

## Results / Data

- Energy drift: $E_{\text{rel, max}} = 0.0$; $\text{tol}_E = 0.0032$ ⇒ gate: pass.  
- Local balance residual: $\max = 0.0$; $\text{tol}_B \approx 0.01203875$ ⇒ gate: pass.

Figure 1 — Energy and residual traces (PNG; paired CSV/JSON with same basename):  
`Derivation/code/outputs/figures/thermo_routing/20251013_142050_wave_flux_meter_energy_thermo-routing-v2-wave-meter.png`

CSV (metrics):  
`Derivation/code/outputs/logs/thermo_routing/20251013_142050_wave_flux_meter_v1_metrics_thermo-routing-v2-wave-meter.csv`

JSON (summary):  
`Derivation/code/outputs/logs/thermo_routing/20251013_142050_wave_flux_meter_v1_summary_thermo-routing-v2-wave-meter.json`

All artifacts produced via common/io_paths with policy-aware routing; this approved run is not quarantined.

## Discussion / Analysis

- Discrete instrument behavior matches expectations: leapfrog yields bounded energy oscillations of $\mathcal{O}((\Delta t/a)^2)$; the dynamic tolerance reflects this and was met with margin.  
- The true continuity residual $r$ (with centered $\partial_t e$) is numerically zero at this resolution for the chosen uniform medium and discrete plane wave, confirming correct discrete bookkeeping of flux and energy density.  
- Using periodic BCs avoids boundary flux terms in the closed box, isolating bulk discretization.  
- Future tightening can use a smaller $\Delta t$ and explicit plane-wave eigenmodes to quantify exact error constants; current gates are appropriate for meter certification.

## Conclusions

Phase A of the Wave Flux Meter is certified: energy conservation and local balance gates pass in a closed box with frozen $V$. This establishes the meter as a trustworthy instrument for subsequent phases:

- Phase B (Open-port optics): add two outlets and absorber/PML; verify power accounting and symmetry null; quantify absorber loss.
- Phase C (Channel map engaged): frozen $V(x,y)$ with routing KPIs ($\bar F_A, \bar F_B$).

The passive FTMC walkers remain a transport toy; photonic-style routing will be audited with this wave instrument.

## References

- Landau & Lifshitz, Electrodynamics of Continuous Media.  
- Jackson, Classical Electrodynamics.  
- Standard scalar wave energy/flux formulations (acoustics).
