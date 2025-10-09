# KG⊕RD Metriplectic QC - Spectral‑DG Primary Profile

> Author: Justin K. Lietz
> Date: 2025-10-06
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.
> Commercial use requires citation and written permission from Justin K. Lietz.
> See LICENSE file for full terms.

TL;DR - Gate-driven QC of a metriplectic KG⊕RD scheme (spectral-DG for M, Störmer-Verlet for KG J, Strang JMJ). Pinned spec snapshot: derivation/code/outputs/logs/metriplectic/20251006_142434_step_spec_snapshot__kgRD-v1.json

## Introduction

This note evaluates a metriplectic time integrator that couples a conservative Klein-Gordon (KG) field with a dissipative reaction-diffusion (RD) flow via operator splitting. The objective is quality control (QC): verify discrete invariants (time-reversal for J; Lyapunov monotonicity for M), confirm expected error scalings under Strang composition, and document pass/fail against explicit gates with pinned artifacts.

This coupling is representative of multi-physics models where a Hamiltonian subsystem (wave-like KG) interacts with dissipative kinetics (RD). The metriplectic framework separates skew (Poisson) and metric (dissipative) brackets; here, alignment of spectral operators across J and M is used to reduce splitting constants without sacrificing the H-theorem.

Scope: QC only, for a fixed grid and Δt sweep; no novelty claims. All claims are paired with equations and/or gates and artifacts.

## Research question

To what extent does the time step Δt (s, normalized) control the observed log-log two‑grid error slope p (unitless) for the KG⊕RD Strang JMJ composition when using a spectral discrete‑gradient (DG) M‑step? Secondary: does the KG J‑only integrator meet strict per‑step energy and reversibility gates under our normalization?

Dependent measurements and instruments:

- Two‑grid residual E(Δt) (L2 of state difference; instrument: Python harness performing linear regression on log E vs. log Δt).
- KG energy drift per step ΔH (dimensionless energy) and reversibility error in max‑norm.

## Background Information

Minimal framework and definitions:

- Metriplectic dynamics split conservative and dissipative evolution via a Poisson bracket {·,·} and a metric bracket (·,·), with Hamiltonian H and Lyapunov L such that dH/dt = 0 and dL/dt ≤ 0 in the continuum (Onsager; JKO).
- Discrete‑gradient (DG) schemes (Gonzalez; Quispel-McLaren) enforce a discrete identity preserving the sign of the entropy/Lyapunov production.
- Strang splitting (JMJ) is second‑order; its leading local defect scales O(Δt³), so a defect diagnostic exhibits slope near 3 on log-log axes.
- Symplectic Störmer-Verlet preserves a modified Hamiltonian; exact per‑step H conservation is not expected, but time‑reversal symmetry and bounded energy oscillations are (Hairer-Lubich-Wanner).

Core equations (variables dimensionless under our normalization):

1. KG Hamiltonian (spectral gradient ∇ₕ)

$$
H(\phi,\pi) = \tfrac12\,\|\pi\|_2^2 + \tfrac12 c^2\,\|\nabla_h\phi\|_2^2 + \tfrac12 m^2\,\|\phi\|_2^2.
$$

1. DG monotonicity for M (RD)

$$
L(u^{n+1})-L(u^n) = -\Delta t\, \langle \nabla_d L,\, M\, \nabla_d L \rangle \le 0.
$$

1. Strang composition operator

$$
\Phi_{\Delta t}^{\text{JMJ}} = \Phi_{\Delta t/2}^J \circ \Phi_{\Delta t}^M \circ \Phi_{\Delta t/2}^J.
$$

1. Two‑grid error model and slope p

$$
E(\Delta t) \approx C\, \Delta t^{\,p},\qquad p = \frac{\mathrm{d}\,\log E}{\mathrm{d}\,\log \Delta t}.
$$

Mapping to gates:

- DG identity ⇒ enforce ΔL ≤ 0 and identity residuals ≤ 1e-12 for M and JMJ.
- Strang ⇒ target two‑grid slope ≥ 2.90 with R² ≥ 0.999 in the asymptotic range; defect slope near 3.
- Symplectic J ⇒ reversibility ≤ 1e-12; energy drift gate set at ≤ 1e-12 (strict) with discussion of modified energy behavior.

Citations: Strang (1968); Hairer-Lubich-Wanner (2006); Gonzalez (1996); Quispel-McLaren (2008); Onsager (1931); Jordan-Kinderlehrer-Otto (1998).

## Variables

- Independent variable: time step Δt ∈ {0.04, 0.02, 0.01, 0.005} (s, normalized). Small‑Δt set used in diagnostics: {0.02, 0.01, 0.005, 0.0025}.
- Dependent variables:
  - Two‑grid residual E (state L2 norm on ϕ in v1) and fitted slope p (unitless) with R².
  - KG J‑only per‑step energy drift ΔH (dimensionless) and reversibility error (max‑norm).
- Controls:

| Control variable | Value | How controlled | Why controlled |
| --- | --- | --- | --- |
| Grid | N = 256, Δx = 1 | Fixed discretization | Comparable CFL, resolution |
| Seeds | 10, seed_scale = 0.05 | Fixed RNG seeds | Median across seeds, robustness |
| Params | (c, m, D, r, u) = (1.0, 0.5, 1.0, 0.2, 0.25) | Fixed physical coefficients | Reproducible dynamics |
| M‑Laplacian | spectral | Step spec `"m_lap_operator":"spectral"` | Align J and M operators |
| DG tolerance | 1e-12 | Newton/backtracking tolerances | Tight identity enforcement |
| Composition | JMJ; MJM (diag) | Fixed | Compare Strang vs. swapped defect |

## Equipment / Hardware

- Software: Python 3.13.5; NumPy 2.2.6; Matplotlib 3.10.6; float64 machine epsilon ε ≈ 2.22×10⁻¹⁶.
- Platform: Linux (x86_64). Single‑process runs; seeds logged in artifacts.
- IO discipline: every figure has CSV/JSON sidecars under outputs/{figures,logs}/metriplectic tagged `kgRD‑v1`.

## Methods / Procedure

Materials and setup:

- J (KG): spectral gradient; Störmer-Verlet on (ϕ, π) with periodic BCs.
- M (RD): discrete‑gradient (AVF) with spectral Laplacian.
- Composition: JMJ (primary), MJM (defect diagnostic).

Steps:

1. Generate periodic ICs for (ϕ, π) using seeded noise (seed_scale = 0.05). Fix grid, params, tolerances.
2. J‑only diagnostic: advance by Δt and reverse; record max‑norm reversibility and per‑step ΔH; log JSON.
3. M‑only two‑grid: sweep Δt; compute residual E from coarse/fine pairing; fit p, R²; emit CSV/JSON/PNG.
4. JMJ two‑grid: sweep Δt; compute E on ϕ (v1); fit p, R²; emit artifacts.
5. Strang defect: compare JMJ vs. MJM; fit slope; emit artifacts.
6. Enforce gates: ΔL ≤ 0; identity residuals ≤ 1e-12; slope ≥ 2.90 with R² ≥ 0.999; reversibility ≤ 1e-12; route failures under failed_runs/.

Risk assessment (computational): potential under‑resolved asymptotics at coarse Δt (mitigated by planned smaller Δt); strict energy gate for symplectic J may fail despite correct reversibility (addressed in Discussion).

## Results / Data

Pinned spec snapshot: derivation/code/outputs/logs/metriplectic/20251006_142434_step_spec_snapshot__kgRD-v1.json

Table 1 - Summary of gates and outcomes (median over seeds; v1 two‑grid on ϕ)

| Test | Gate | Outcome | Artifact (one pinned) |
| --- | --- | --- | --- |
| J‑only (KG) | reversibility ≤ 1e-12; ΔH per‑step ≤ 1e-12 | rev ≈ 6.94×10⁻¹⁸ (PASS); ΔH ≈ 2.16×10⁻⁷ (FAIL) | logs/metriplectic/failed_runs/20251006_142434_j_reversibility_kg__kgRD-v1.json |
| M‑only (RD, spectral‑DG) | ΔL ≤ 0; ids ≤ 1e-12; slope ≥ 2.90; R² ≥ 0.999 | slope 2.8715; R² 0.999843 (slope FAIL) | figures/metriplectic/failed_runs/20251006_142435_residual_vs_dt_m_only__kgRD-v1.png |
| JMJ (Strang, spectral‑DG) | ΔL ≤ 0; ids ≤ 1e-12; slope ≥ 2.90; R² ≥ 0.999 | slope 2.1087; R² 0.999922 (slope FAIL) | figures/metriplectic/failed_runs/20251006_142436_residual_vs_dt_jmj__kgRD-v1.png |
| Strang defect (diag) | slope near 3; R² ≥ 0.999 | slope 2.945; R² 0.999971 (OK) | figures/metriplectic/20251006_142436_strang_defect_vs_dt__kgRD-v1.png |

Figures (each has CSV/JSON sidecars):

- M‑only residual vs Δt: derivation/code/outputs/figures/metriplectic/failed_runs/20251006_142435_residual_vs_dt_m_only__kgRD-v1.png
  - Sidecars: derivation/code/outputs/logs/metriplectic/failed_runs/20251006_142435_residual_vs_dt_m_only__kgRD-v1.csv, .../20251006_142435_sweep_dt_m_only__kgRD-v1.json
- JMJ residual vs Δt: derivation/code/outputs/figures/metriplectic/failed_runs/20251006_142436_residual_vs_dt_jmj__kgRD-v1.png
  - Sidecars: derivation/code/outputs/logs/metriplectic/failed_runs/20251006_142436_residual_vs_dt_jmj__kgRD-v1.csv, .../20251006_142436_sweep_dt_jmj__kgRD-v1.json
- Strang defect vs Δt: derivation/code/outputs/figures/metriplectic/20251006_142436_strang_defect_vs_dt__kgRD-v1.png
  - Sidecars: derivation/code/outputs/logs/metriplectic/20251006_142436_strang_defect_vs_dt__kgRD-v1.{csv,json}

Sample calculation (slope fit): let x_i = log Δt_i, y_i = log E_i. The least‑squares slope is

$$
\hat p = \frac{\sum_i (x_i-\bar x)(y_i-\bar y)}{\sum_i (x_i-\bar x)^2},\qquad R^2 = 1 - \frac{\sum_i (y_i - (\hat p x_i + \hat b))^2}{\sum_i (y_i-\bar y)^2}.
$$

Uncertainty treatment: medians across seeds reduce outlier influence; regression scatter enters the R² gate. Additional CI on p can be obtained via standard linear‑fit formulas but is not required by current gates.

## Discussion / Analysis

Key findings:

1. KG J‑only is time‑reversible to machine precision (PASS), but the strict per‑step energy drift gate fails (~2.16×10⁻⁷). This aligns with symplectic Verlet preserving a modified Hamiltonian; energy oscillations around a shadow energy are typical rather than exact per‑step conservation.
2. Two‑grid slopes for M‑only (2.87) and JMJ (2.11) miss the ≥2.90 gate for the current Δt set and a ϕ‑only residual. The Strang defect slope (~2.95) confirms the expected near‑cubic defect behavior, indicating that coupling/measurement-not algorithmic breakdown-likely explains the low primary slope.

Explanations and next checks:

- Norm choice: using an energy‑weighted composite norm over (ϕ, π) should better reflect the KG⊕RD state error than ϕ‑only.
- Asymptotics: extending to smaller Δt (e.g., 0.0025, 0.00125) should access the asymptotic slope regime for JMJ.
- J energy gate: complement the strict reversibility gate with an oscillation‑based energy gate (fit amplitude ∝ Δt² with high R²) consistent with symplectic theory.

## Conclusions

Aim: QC of a metriplectic KG⊕RD integrator (spectral‑DG M, Störmer-Verlet J, Strang JMJ) against explicit gates.

Outcomes: reversibility PASS; Strang defect consistent; two‑grid gates not met in v1 under ϕ‑only measurement and current Δt set; strict per‑step energy gate FAIL as expected for symplectic schemes without modified‑energy tracking.

Planned bounded follow‑ups:

- Adopt composite (ϕ, π) two‑grid norm and re‑fit slopes.
- Extend small‑Δt sweep to probe asymptotics.
- Add oscillation‑based KG energy gate alongside strict reversibility.

## References / Works Cited

- Strang, G. (1968). On the Construction and Comparison of Difference Schemes. SIAM J. Numer. Anal.
- Hairer, E., Lubich, C., Wanner, G. (2006). Geometric Numerical Integration. Springer.
- Gonzalez, O. (1996). Time integration and discrete Hamiltonian systems. J. Nonlinear Sci.
- Quispel, G. R. W., McLaren, D. I. (2008). A new class of energy‑preserving numerical integration methods. J. Phys. A.
- Onsager, L. (1931). Reciprocal relations in irreversible processes. Phys. Rev.
- Jordan, R., Kinderlehrer, D., Otto, F. (1998). The variational formulation of the Fokker-Planck equation. SIAM J. Math. Anal.

---

### Addendum - kgRD‑v1b (H‑energy norm, spectral‑DG; tagged)

Short note: Switching from ϕ‑only to the KG energy norm |(Δϕ,Δπ)|_H restores near‑cubic two‑grid scaling for JMJ (H‑norm slope ≈ 2.885, R² ≈ 0.99988), consistent with the Strang defect diagnostic.

Obj‑B status: if the JMJ H‑norm slope remains < 2.90 under the extended small‑Δt sweep, we freeze this chapter as EXPLAINED‑BY‑DEFECT and proceed without further tuning.

Pinned artifacts (tag `kgRD‑v1b`):

- Spec snapshot: derivation/code/outputs/logs/metriplectic/20251006_145830_step_spec_snapshot__kgRD-v1b.json
- J‑only energy oscillation vs Δt (slope gate ≈ 2):
  - Figure: derivation/code/outputs/figures/metriplectic/failed_runs/20251006_145830_j_energy_oscillation_vs_dt__kgRD-v1b.png
  - Logs: derivation/code/outputs/logs/metriplectic/failed_runs/20251006_145831_j_energy_oscillation_vs_dt__kgRD-v1b.{json,csv}
- M‑only two‑grid:
  - Figure: derivation/code/outputs/figures/metriplectic/failed_runs/20251006_145831_residual_vs_dt_m_only__kgRD-v1b.png
  - Logs: derivation/code/outputs/logs/metriplectic/failed_runs/20251006_145831_residual_vs_dt_m_only__kgRD-v1b.{json,csv}
- JMJ two‑grid (H‑energy norm):
  - Figure: derivation/code/outputs/figures/metriplectic/failed_runs/20251006_145832_residual_vs_dt_jmj__kgRD-v1b.png
  - Logs: derivation/code/outputs/logs/metriplectic/failed_runs/20251006_145832_sweep_dt_jmj__kgRD-v1b.json and .../20251006_145832_residual_vs_dt_jmj__kgRD-v1b.csv
- Strang defect (JMJ vs MJM):
  - Figure: derivation/code/outputs/figures/metriplectic/20251006_145832_strang_defect_vs_dt__kgRD-v1b.png
  - Logs: derivation/code/outputs/logs/metriplectic/20251006_145833_strang_defect_vs_dt__kgRD-v1b.{json,csv}

Gate outcomes (median across seeds):

- JMJ (H‑energy norm): slope ≈ 2.885; R² ≈ 0.999877 (near‑cubic but below ≥ 2.90 gate).
- Strang defect: slope ≈ 2.957; R² ≈ 0.999969 (as expected, supporting the near‑cubic behavior).
- J‑only energy oscillation slope: ≈ 0.951 (R² ≈ 0.99937), below the ≥ 1.9 gate; reversibility remains PASS.
