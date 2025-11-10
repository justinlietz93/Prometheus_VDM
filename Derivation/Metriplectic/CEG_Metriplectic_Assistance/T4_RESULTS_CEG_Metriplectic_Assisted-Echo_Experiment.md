<!-- ATTENTION! Whitepaper-grade results: full narrative, MathJax, numeric captions tied to artifacts, explicit thresholds with pass/fail gates, and provenance. -->

# T4 — Counterfactual Echo Gain (CEG): Metriplectic Assisted‑Echo (Prereg v1c) — RESULTS

> Author: Justin K. Lietz  
> Date: 2025‑11‑04  
> Commit: c63d13f3de38483f867219b1d2ef10330fca7156 (short: c63d13f)  
> License: See [LICENSE](../../LICENSE)  
> Proposal: [T4_PROPOSAL_CEG_Metriplectic_Assisted‑Echo_Experiment.md](../T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md)

TL;DR — Running the preregistered assisted‑echo (tag: assisted‑echo‑t4‑prereg‑v1c) with N=256, Δt=0.02, seeds=12, and λ∈{0,0.1,0.2,0.3,0.5}, all instrument gates passed at 100% pass‑rate (G1–G4). The preregistered outcome gate (G5, “positive CEG”) passed with median_max CEG = 0.054552 ≥ 0.05 at λ=0.5. Core artifacts:

- Run JSON: [assisted_echo run log](../../code/outputs/logs/metriplectic/20251104_123411_assisted_echo__assisted-echo-t4-prereg-v1c.json)
- CEG CSV: [median/mean CEG per λ](../../code/outputs/logs/metriplectic/20251104_123412_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c.csv)
- Figures (pack): e.g., CEG vs λ — [A3_ceg_vs_lambda](../../code/outputs/figures/metriplectic/20251104_123413_20251104_123412_assisted_echo_ceg_vs_lambda__assisted-echo-t4-prereg-v1c.png)

---

## 1. Scope and claim boundaries

This document reports the preregistered CEG outcome and gate statuses for the metriplectic assisted‑echo experiment. It makes no novelty claims about echo mechanisms; the claim is strictly that a model‑aware assistance micro‑sequence yields a statistically positive echo gain under instrument gates and an energy‑match constraint. Numerical scheme is treated as the measuring instrument per VDM canon.

- Canon sources (anchors; see Derivation):  
  - Equations registry: [EQUATIONS.md](../../EQUATIONS.md)  
  - Validation metrics/gates: [VALIDATION_METRICS.md](../../VALIDATION_METRICS.md)  
  - Units/normalization: [UNITS_NORMALIZATION.md](../../UNITS_NORMALIZATION.md)

## 2. Research question (preregistered)

Does a metriplectic, model‑aware assisted echo improve the echo recovery error relative to an energy‑matched, model‑blind baseline, without violating instrument gates?

- Independent variables: grid N=256, spacing dx=1, time‑step Δt=0.02, seeds=12, assistance λ∈{0,0.1,0.2,0.3,0.5}.  
- Dependent observable (dimensionless):  
  $$ \mathrm{CEG} \equiv \frac{E_{\mathrm{baseline}} - E_{\mathrm{assisted}}}{E_{\mathrm{baseline}}} \in [0,1] $$
  computed on the echo overlap per [assisted_echo.py](../../code/physics/metriplectic/assisted_echo.py:325) via the H‑norm metric routine.

- Falsifiable threshold (G5): median\_max CEG ≥ 0.05 at some λ>0, provided G1–G4 gates pass at the instrument pass‑rate.

## 3. Methods (instrument and runner)

- Runner: [assisted_echo.py](../../code/physics/metriplectic/assisted_echo.py:855)  
- Spec (v1c): [assisted_echo.v1c.json](../../code/physics/metriplectic/specs/assisted_echo.v1c.json)  
- Schema tag: [assisted-echo-t4-prereg-v1c.schema.json](../../code/physics/metriplectic/schemas/assisted-echo-t4-prereg-v1c.schema.json:1)

Execution steps per prereg plan:

1) Forward JMJ integration with diagnostics (collect ΔΣ for M‑only segment).  
2) RP‑1 gates measured on the seed’s IC (J‑only reversibility drift; Strang two‑grid slope/R²).  
3) Walker perturbation injection (preregistered amplitude/width/channel) between forward and reverse.  
4) Reverse phase baseline (random equal‑budget correction) and assisted (model‑aware equal‑budget correction) per λ, enforcing energy‑match.  
5) Aggregate CEG per seed and over seeds; compute gate pass‑rates; route artifacts via [io_paths.py](../../code/common/io_paths.py:86).

Approval and provenance were enforced by [check_tag_approval()](../../code/common/authorization/approval.py:426) using manifest [APPROVAL.CEG.json](../../code/physics/metriplectic/APPROVAL.CEG.json:1) with require_provenance=true; proposal header was stamped via [stamp_proposal.py](../../code/common/provenance/stamp_proposal.py:105).

## 4. Results

### 4.1 Gate outcomes (instrument aggregation; pass‑rate threshold ≥ 10/12 = 0.8333)

From the run JSON ledger: [gate ledger summary](../../code/outputs/logs/metriplectic/20251104_123411_assisted_echo__assisted-echo-t4-prereg-v1c.json:392)

- G1 Noether (J‑only drift): PASS 12/12; pass‑rate 1.000; typical drift ~3.5×10⁻¹⁷; tol scaled per instrument (≈1.6×10⁻¹¹).
- G2 H‑theorem (ΔΣ≥0 during M): PASS 12/12; pass‑rate 1.000; min ΔΣ per seed ≳ 4.1×10⁻⁴.
- G4 Strang defect (two‑grid slope, R²): PASS 12/12; pass‑rate 1.000; slopes ≈ 2.94–2.95; R² ≈ 0.99997.
- G3 Energy‑match (reverse equal‑work): PASS 12/12; pass‑rate 1.000; rel\_diff ≤ 1.4×10⁻¹⁶.
- G5 CEG positive (outcome metric): median\_max = 0.054552 ≥ 0.05 → PASS.

No instrument gate failed the pass‑rate threshold; no contradiction report was emitted.

### 4.2 Assisted‑echo gain vs λ

- Source CSV: [CEG summary](../../code/outputs/logs/metriplectic/20251104_123412_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c.csv)  
- Figure (numeric caption below): [A3 CEG vs λ](../../code/outputs/figures/metriplectic/20251104_123413_20251104_123412_assisted_echo_ceg_vs_lambda__assisted-echo-t4-prereg-v1c.png)

| λ    | median CEG   | mean CEG      | n  |
|-----:|--------------:|--------------:|---:|
| 0.0  | 0.000000      | 0.000000      | 12 |
| 0.1  | 0.012462      | 0.012113      | 12 |
| 0.2  | 0.023688      | 0.023465      | 12 |
| 0.3  | 0.034664      | 0.034247      | 12 |
| 0.5  | 0.054552      | 0.053785      | 12 |

Numeric caption (A3): “CEG vs λ (median ± mean) for N=256, Δt=0.02, seeds=12. Median\_max = 0.054552 at λ=0.5; all instrument gates passed at 100%.”

### 4.3 Telemetry and diagnostics

Per‑step telemetry (errors, ΔΣ, first‑mode energies, work partitions) is provided in the figure pack (A1–B12) generated by [generate_core_pack()](../../code/common/plotting/assisted_echo_plots.py:1). Representative panels:

- A5 ΔΣ(t): monotone per step (M limb), consistent with G2.  
- B11 overlay: forward vs reverse traces align with energy budgets; no seed‑chord artifacts post fix.  
- A6 Noether drift: within scaled tolerance on all seeds.

## 5. Provenance

- Run JSON: [20251104_123411_assisted_echo__assisted-echo-t4-prereg-v1c.json](../../code/outputs/logs/metriplectic/20251104_123411_assisted_echo__assisted-echo-t4-prereg-v1c.json)  
- CSV: [20251104_123412_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c.csv](../../code/outputs/logs/metriplectic/20251104_123412_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c.csv)  
- Proposal stamping tool: [stamp_proposal.py](../../code/common/provenance/stamp_proposal.py:1) (used to ensure proposal header ⇄ prereg salted hash consistency).  
- Approval policy/gates: [approval.py](../../code/common/authorization/approval.py:426), manifest [APPROVAL.CEG.json](../../code/physics/metriplectic/APPROVAL.CEG.json:1).

## 6. Discussion

- The CEG curve is monotone increasing across the preregistered λ grid, with a clear positive effect at λ=0.5 crossing the prereg threshold. The effect size is modest but robust to seeds (n=12) under strict energy‑match and instrument gates.
- Strang defect slopes (~2.94–2.95) and R² (~0.99997) reaffirm composition accuracy at these settings, supporting that the observed CEG is not a numerical artifact of order degradation.
- Energy‑match G3 eliminates trivial gains from extra injected energy; the assistance work is equalized baseline vs assisted. The positive CEG therefore indicates directional utility of the model‑aware correction in the reverse phase.

Limitations and next steps:

- Explore finer λ grid around 0.3–0.6 to map the CEG ridge; extend to N∈{512,1024} and Δt∈{0.01,0.04} as listed in the proposal roadmap.  
- Harden G4 to the multi‑point Δt fit variant (same thresholds) as a robustness check (see README News, 2025‑11‑04).  
- Run ablations (model‑blind, J‑scramble, M‑scramble, MJM ordering) per proposal RP‑4 to quantify dependence on internal model fidelity.

## 7. Conclusions

Under preregistered conditions and strict gates, the metriplectic assisted‑echo exhibits a statistically positive CEG (median\_max 0.054552 at λ=0.5) while preserving J‑Noether and M‑monotonicity and passing Strang defect QC. This supports the preregistered claim that internal J/M knowledge can be operationally exploited to improve echo recovery without cheating via energy injection.

## 8. References (selected)

- VDM canon: [EQUATIONS.md](../../EQUATIONS.md), [VALIDATION_METRICS.md](../../VALIDATION_METRICS.md), [UNITS_NORMALIZATION.md](../../UNITS_NORMALIZATION.md).  
- Metriplectic dynamics (background) and gradient‑flow formalisms (Onsager/JKO/AGS), as cited in proposal.

---

Appendix: Key source references

- Runner main: [assisted_echo.py:main()](../../code/physics/metriplectic/assisted_echo.py:855)  
- Gate definitions used by runner: [echo_gates.py](../../code/physics/metriplectic/echo_gates.py:1)  
- Plot pack generator: [assisted_echo_plots.py](../../code/common/plotting/assisted_echo_plots.py:1)
