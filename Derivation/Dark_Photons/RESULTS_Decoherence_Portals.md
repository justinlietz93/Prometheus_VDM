# Decoherence Portals  Results (v1)

> Author: Justin K. Lietz  
> Date: 2025-10-08  
> License: Dual-license; see LICENSE.

## TL;DR

- Gates: Fisher consistency (relative error $\le 10\%$) and noise budget residuals within spec.  
- Outcome: awaiting approved run; this scaffold records gates, instruments, and artifact locations.

## Research question

Do the simple Fisher estimate of $\epsilon$ and the noise budget sanity checks agree with injected/expected values within the registered tolerances on synthetic or benchmarked inputs?

## Background (focused)

- Fisher information for small signal $S$ over background $B$ in bins: $\mathcal I(\epsilon)=\sum_i \frac{1}{B_i}\left(\frac{\partial S_i}{\partial \epsilon}\right)^2$ (simplified).  
- Expected $\epsilon$ uncertainty: $\sigma_\epsilon \approx 1/\sqrt{\mathcal I(\epsilon)}$.

## Variables

- Inputs: binned expectations $(S_i,B_i)$, exposures, efficiencies.  
- Dependent: $\hat\epsilon$ and Fisher-derived $\sigma_\epsilon$; noise residuals.  
- Instruments: `run_dp_fisher_check.py`, `run_dp_noise_budget.py`.

## Methods / Procedure

1. Load or generate a small benchmark with 1 4 bins (CSV).
2. Compute Fisher information and $\sigma_\epsilon$ from the benchmark.  
3. Fit $\hat\epsilon$ via a simple likelihood or linearized estimator.  
4. Compare $|\hat\epsilon-\epsilon_\text{true}|/\epsilon_\text{true}$ to the 10% gate.  
5. For noise budget, compute residuals against modeled noise components and check they lie within spec.

## Artifacts (to be pinned)

- Figures: `derivation/code/outputs/figures/dark_photons/<tag>_*.png`
- Logs (CSV/JSON): `derivation/code/outputs/logs/dark_photons/<tag>_*.{csv,json}`

## Results / Data

Awaiting an approved run; artifacts will be pinned here with numeric gate summaries.

## Reproducibility

- Runners: `derivation/code/physics/dark_photons/run_dp_fisher_check.py`, `run_dp_noise_budget.py`
- IO discipline: PNG + CSV + JSON sidecars via `common/io_paths.py` with approvals/quarantine policy.

## References

- Standard Fisher information treatments; dark photon phenomenology primers.
