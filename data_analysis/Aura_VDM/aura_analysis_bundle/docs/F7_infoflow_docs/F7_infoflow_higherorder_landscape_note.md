# F7 — Information-flow hierarchy, higher-order dynamics, and landscape reshaping

## Scope
This package resolves three previously underpowered high-value distinctions from Family 7:
- D7.1 macrostate directed-influence hierarchy
- D7.6 window-level TC/DTC/O-information dynamics
- D7.8 baseline projection grid / state-space landscape reshaping

## D7.1
Using `macrostate_directed_influence_deltaR2.csv`, directed incremental predictive power is selective rather than flat.
- strongest predictor channel overall: **connectome_entropy** (mean outgoing ΔR² = **0.0795**)
- strongest target channel overall: **vt_coverage** (mean incoming ΔR² = **0.0735**)

## D7.6
O-information stays negative across every epoch, but its depth shifts sharply:
- E1 mean O = **-32.667**
- E2 mean O = **-40.146**
- E3 mean O = **-29.662**

Boundary-local variance changes are severe:
- E1→E2 variance: **1.387 → 48.189**
- E2→E3 variance: **95.609 → 9.118**

## D7.7
LZ complexity shows a small but highly significant upward trend:
- Spearman ρ = **0.0694**
- p = **1.371e-09**

## D7.8
Consecutive state-space landscape JSD declines overall:
- 17160→17220 = **0.323**
- 17220→17280 = **0.224**
- 17280→17340 = **0.174**
- 17340→17400 = **0.187**

This is a settling-but-not-frozen late landscape.
