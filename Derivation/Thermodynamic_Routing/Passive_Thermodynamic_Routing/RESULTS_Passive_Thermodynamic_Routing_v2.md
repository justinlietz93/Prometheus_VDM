# RESULTS: Passive Thermodynamic Routing v2 — Symmetric Smoke (gate_set = smoke_symm)

Author: Justin K. Lietz  
Date: 2025-10-13  
Commit: 65df9c0  
Tag: thermo-routing-v2

## Purpose

This is the smoke validation for the Passive Thermodynamic Routing v2 preregistration. The smoke gate set only enforces: (i) H-theorem monotonicity for the metric step and (ii) no-switch identity. RJ spectral thermodynamics, flux bias, and energy-floor are recorded as diagnostics but are not gates for the smoke profile.

## Environment receipts

- BLAS: openblas  
- FFT: numpy.pocketfft (deterministic plans)  
- Threads: 32  
- Determinism receipts: 40 checkpoint hashes recorded; no-switch clause = “bitwise”

(Source: summary JSON env and receipts fields.)

## Artifacts (bundle: 20251013_04553x)

Figures:

- Lyapunov + ΔL overlay: Derivation/code/outputs/figures/thermo_routing/20251013_045538_lyapunov_h_theorem_thermo-routing-v2.png
- KPI dashboard: Derivation/code/outputs/figures/thermo_routing/20251013_045538_kpi_dashboard_thermo-routing-v2.png
- Geometry & masks: Derivation/code/outputs/figures/thermo_routing/20251013_045539_geometry_masks_thermo-routing-v2.png

Logs:

- Lyapunov series CSV: Derivation/code/outputs/logs/thermo_routing/20251013_045539_tr_v2_smoke_symm__lyapunov_series_thermo-routing-v2.csv
- Summary JSON: Derivation/code/outputs/logs/thermo_routing/20251013_045539_tr_v2_smoke_symm_thermo-routing-v2.json

Policy: approved=true, quarantined=false; gate_set=smoke_symm; passed_smoke=true.  
(Source: JSON policy, gate_set, and passed_smoke.)

## Gate matrix (smoke)

- H-theorem: PASS  
- No-switch: PASS  
- RJ fit: DIAGNOSTIC (not gated in smoke)  
- Bias: DIAGNOSTIC  
- Energy-floor: DIAGNOSTIC

## Methods (abbrev.)

- Equation: reaction–diffusion metric descent step $\displaystyle \partial_t\,\phi = D\,\nabla^2 \phi + f(\phi)$ with discrete gradient (DG) integrator to ensure $\Delta L_h \le 0$.
- Geometry: symmetric two-outlet control; outflux-only convention at the right boundary.
- RJ diagnostic: spectral fit of modal power to $S_k \approx T/(\lambda_k - \mu)$ over a tail window; recorded but not gated for smoke.
- No-switch: controller-disabled identity; bitwise comparison at checkpoints; SHA-256 of field buffers.

## Results (quoted from JSON)

- H-theorem: violations = 0, max positive $\Delta L_h = 0.0$ (PASS).  
  JSON: kpi.h_theorem.violations = 0; kpi.h_theorem.max_positive_dL = 0.0.
- No-switch identity: checkpoints = 40, ok = true (PASS).  
  JSON: kpi.no_switch.checkpoints = 40; kpi.no_switch.ok = true.
- RJ diagnostic: $R^2 = 0.7326$ with $k\_\min = 3$, $k\_\max = 32$; not gated in smoke.  
  JSON: kpi.rj_fit.R2 = 0.7326; kpi.rj_fit.k_min = 3; kpi.rj_fit.k_max = 32; kpi.rj_fit.not_gated_in_smoke = true.
- Flux bias (outflux-only): $B = -3.11\times10^{-3}$ and $\varrho = 0.3128$ (diagnostic).  
  JSON: kpi.bias.B = -0.0031126; kpi.bias.rho = 0.3128.  
  Note: symmetric geometry control expects $B\approx 0$; observed magnitude is negligible at this horizon.
- Energy-floor witness (diagnostic): $L_h(t_\text{final}) = 2.98\times 10^{-5}$.  
  JSON: kpi.energy_floor.L_last = 2.9789e-05.

## Figures and captions

1) Lyapunov H-theorem plot  
  File: 20251013_045538_lyapunov_h_theorem_thermo-routing-v2.png  
  Caption: $\Delta L_h \le 0$ at every step (violations = 0; max positive $\Delta L_h = 0.0$), with the RJ analysis window shaded and checkpoint ticks annotated.

2) KPI dashboard  
  File: 20251013_045538_kpi_dashboard_thermo-routing-v2.png  
  Caption: RJ spectrum panel shows $R^2 = 0.7326$ (diagnostic, not gated in smoke) over $k\in[3,32]$; flux panel reports outflux-only metrics $(B=-3.11\times10^{-3},\;\varrho=0.3128)$; timeline panel confirms no-switch identity across 40 checkpoints; receipts panel lists BLAS=openblas, FFT=numpy.pocketfft, threads=32.

3) Geometry & masks  
  File: 20251013_045539_geometry_masks_thermo-routing-v2.png  
  Caption: Symmetric two-outlet geometry schematic with snapshot of $\phi(x,y)$; right-boundary outflux arrows indicated. Slim inset shows normalized edge-flux density $F_x(y)$.

## Determinism receipts

Bitwise no-switch identity (40/40 checkpoints identical) and recorded checkpoint hashes confirm deterministic execution under the documented environment (threads, BLAS, FFT plan mode).  
(Source: receipts.checkpoint_hashes, receipts.no_switch.)

## Interpretation and limitations

- The smoke profile validates plumbing: strict H-theorem and no-switch identity both pass, and artifacts route via policy-compliant paths.  
- Symmetric geometry yields near-constant fields at late times, producing weak spectral content and an RJ $R^2$ below the prereg gate value; this is by design not enforced in smoke.  
- Flux bias remains near zero as expected under symmetry.

Contradiction policy: Any future gate failure emits a CONTRADICTION_REPORT with gate, threshold, seed, and artifact IDs.

## Next steps (per preregistration)

1) Implement prereg geometry with no-flux walls and open outlets (biased widths), then reinstate RJ gate with $R^2 \ge 0.99$ in an earlier, power-rich window.  
2) Add robustness gates: injection-site sweep trend and two-source split invariance; report CIs and whiteness diagnostics.  
3) Produce full prereg RESULTS with contradiction handling if any gate fails; update canonical registries after acceptance.

## Provenance

- Proposal: Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md  
- Runner: Derivation/code/physics/thermo_routing/run_thermo_routing.py  
- Summary JSON: Derivation/code/outputs/logs/thermo_routing/20251013_045539_tr_v2_smoke_symm_thermo-routing-v2.json  
- Approval: policy.approved = true; quarantined = false.

---

## License and citation

Copyright (c) 2025 Justin K. Lietz.

This RESULTS document and associated figures/logs are distributed under the repository’s LICENSE. If you use these results, please cite:

Justin K. Lietz, “Passive Thermodynamic Routing v2 — Symmetric Smoke,” Prometheus_VDM (2025), commit 65df9c0.

