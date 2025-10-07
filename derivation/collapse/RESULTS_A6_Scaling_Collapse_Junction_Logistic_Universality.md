<!-- DOC-GUARD: REFERENCE -->
# A6 Scaling Collapse — Junction Logistic Universality (v1)

> Author: Justin K. Lietz  
> Date: 2025-10-06

## Introduction

Goal: validate the A6 dimensionless universality claim for junction routing. When selection follows a logistic in a memory contrast $\Delta m$ with slope parameter $\Theta$, plotting $P(A)$ against $X=\Theta\Delta m$ should collapse curves across $\Theta$.

## Methods

- Runner: `derivation/code/physics/collapse/run_a6_collapse.py`
- Curves: $\{(X_i, P_i)\}$ for multiple $\Theta$ values; interpolate onto shared $X$ grid
- Envelope: $E(X)=Y_{\max}(X)-Y_{\min}(X)$; metric `env_max = max_X E(X)`
- Gate: `env_max ≤ 0.02` (≤ 2%)

## Artifacts (pinned)

- Figure: `derivation/code/outputs/figures/collapse/20251006_175337_a6_collapse_overlay__A6-collapse-v1.png`
- CSV: `derivation/code/outputs/logs/collapse/20251006_175337_a6_collapse_envelope__A6-collapse-v1.csv`
- Log: `derivation/code/outputs/logs/collapse/20251006_175337_a6_collapse__A6-collapse-v1.json`

## Results

- Measured envelope maximum: $E_{\max} \approx 1.657\%$
- Gate: PASS (≤ 2%)

## Conclusions

The overlay and envelope band confirm a tight scaling collapse under the specified router and parameterization, meeting the A6 universality gate. If router mechanics change, re-run this envelope to maintain the guarantee.
