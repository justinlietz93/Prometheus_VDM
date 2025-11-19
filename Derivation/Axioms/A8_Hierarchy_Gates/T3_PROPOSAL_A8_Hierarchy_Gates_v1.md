# 1. T3 (Smoke) — A8 Two‑Gate Hierarchy Test ($N(L)\sim\log(L/\lambda)$ & $E_{\mathrm{exc}}(L)\propto L^{d-1}$)

> Created Date:  2025-11-18
> Commit: 29e314eb8ca662eea3f171631252e05c449cef4b
> Salted provenance (pre‑reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}
> Proposer contact(s):  <justin@neuroca.ai>
> License: See LICENSE
> Short summary (one sentence TL;DR):  T3 smoke test of the joint A8 hierarchy gates, checking $N(L)\sim\log(L/\lambda)$ and boundary‑law excess energy $E_{\mathrm{exc}}(L)\propto L^{d-1}$ using preregistered detectors, fits, and null models.

---

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI).

## 3. Abstract

Proposed in this document is a preregistered **Two‑Gate Test** of the A8 hierarchy claim: (P1) logarithmic interface depth $N(L)\sim \log(L/\lambda)$ and (P2) boundary‑law excess energy $E_{\mathrm{exc}}(L)\propto L^{d-1}$. Both must pass jointly. The instrument defines detectors, regressions, and null‑model comparisons (AIC/BIC) and publishes artifacts per gate discipline.

## 4. Background & Scientific Rationale

A8’s geometric necessity links tachyonic genesis to hierarchy. Testing both $N(L)$ and the boundary‑energy law together distinguishes VDM from scale‑free fractal nulls that can mimic one metric alone.

## Some questions to consider

- How novel is a **joint** two‑gate hierarchy test relative to single‑metric probes?
- Why is it necessary to test $N(L)$ and $E_{\mathrm{exc}}(L)$ with shared detectors and meters rather than independently?
- What specific downstream experiments (EBN‑CMB, analog horizons, gravity regression) rely on these gates being validated?
- What criticisms might arise (e.g., detector bias, finite‑size artifacts, choice of null models) and how are they mitigated in this preregistration?

## 5. Intellectual Merit and Procedure

(1) Importance: decisive geometry signature; (2) Impacts: constrains ΛCDM‑style descriptive models; (3) Approach: predeclared detectors, bootstrap CIs, and null comparisons.

## 5.1 Experimental Setup and Diagnostics

- **Detectors:** interface counters and energy aggregators with threshold sweeps; report detector‑sensitivity scans, reusing implementations from the STIV A8 meters and area‑law instruments where applicable.
- **Fits:** (i) depth vs $\log L$ (slope $b_N$ near $1$), (ii) $\log E_{\mathrm{exc}}(L)$ vs $\log L$ (slope $\alpha_E \approx d-1$); use preregistered fitting windows and bootstrap CIs.
- **Acceptance (joint):** $b_N$ within $[0.9, 1.1]$ **and** $\lvert\alpha_E - (d-1)\rvert \le 0.1$ with $R^2 \ge 0.98$; AIC/BIC must prefer the boundary‑law model over volume‑law nulls; failures route to a CONTRADICTION_REPORT with detector‑sensitivity scans.

### 5.1.1 Pre-Run Config Requirements

- **Approvals (hierarchy domain):**
  - `Derivation/code/physics/hierarchy/APPROVAL.json` — approval manifest for hierarchy runs (STIV meters and this A8 hierarchy‑gates test), mapping allowed tags to schemas and this proposal path; must be present and approved before artifact‑writing runs.
- **Pre-registration manifest:**
  - `Derivation/code/physics/hierarchy/PRE-REGISTRATION.json` — preregistration manifest including proposal title, tier grade, commit, salted provenance, hypotheses, variables, pass/fail metrics, and spec references for A8 hierarchy‑gates runs.
- **Schemas:**
  - `Derivation/code/physics/hierarchy/schemas/a8-two-gate.v1.schema.json` — JSON Schema for `a8-two-gate.v1` run specs and summary logs (includes fields for N(L), E_exc(L), fit slopes, R², ΔAIC/ΔBIC, and detector diagnostics).
- **Specs:**
  - `Derivation/code/physics/hierarchy/specs/a8-two-gate.v1.json` — run-spec files referenced in `spec_refs` below; define the L ladder, detector thresholds, dimensionality d, finite‑size corrections, and seeds.
- **Dependencies (meters/instruments):**
  - STIV macrostate and gradient‑flow meters in [`T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md`](Derivation/Hierarchy/STIV/T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md) must be in PASS state.
  - A8 area‑law instrument in [`T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md`](Derivation/Axioms/A8_Scaling_2D3D/T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md) provides prior calibration for E_exc scaling; runs in this T3 test must respect its units/normalization and detector definitions.

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "A8 Two-Gate Hierarchy Test",
  "tier_grade": "T3",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_N", "statement": "N(L) grows logarithmically with L.", "direction": "increase" },
    { "id": "H_E", "statement": "E_exc scales as L^{d-1}.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["L", "detector thresholds", "dimension d", "seeds"],
    "dependent": ["slope_N", "α_energy", "R2", "ΔAIC", "ΔBIC"],
    "controls": ["masking", "binning", "finite-size correction"]
  },
  "pass_fail": [
    { "metric": "slope_N", "operator": "between", "threshold": [0.9, 1.1], "unit": "" },
    { "metric": "α_energy", "operator": "between", "threshold": ["d-1-0.1", "d-1+0.1"], "unit": "" },
    { "metric": "R2", "operator": ">=", "threshold": 0.98, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/physics/hierarchy/specs/a8-two-gate.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

### Minimal spec example (a8-two-gate.v1)

The file `Derivation/code/physics/hierarchy/specs/a8-two-gate.v1.json` must contain at least one spec entry of the following shape (keys aligned with §5.1.1 and the PRE‑REG `variables` block):

```json
{
  "run_name": "a8-two-gate-baseline",
  "version": "1.0.0",
  "tag": "a8-two-gate.v1",
  "schema_ref": "Derivation/code/physics/hierarchy/schemas/a8-two-gate.v1.schema.json",
  "parameters": {
    "L_list": [32, 64, 128, 256],
    "detector_thresholds": {
      "interface": 0.5,
      "energy_cut": 0.1
    },
    "dimension": 3,
    "masking": "none",
    "binning": "logL",
    "finite_size_correction": "surface-to-volume"
  },
  "seeds": [0, 1, 2]
}
```

This is a **minimal illustrative spec**. Actual production specs:

- Must set `L_list`, detector thresholds, and `dimension` consistent with the STIV and area‑law instruments and the A8 program.
- May include additional parameters (e.g., detector variants, alternative binning strategies) as long as `a8-two-gate.v1.schema.json` validates.
- Must be validated by `a8-two-gate.v1.schema.json` and the hierarchy `APPROVAL.json` manifest before any artifact‑writing runs.

## 5.2 Experimental runplan

1. **Design $L$ ladder and detectors.** Choose a log‑spaced set of domain sizes $L$ and detector thresholds consistent with STIV/A8 instruments; document dimensionality $d$ and finite‑size correction strategy in the spec.
2. **Run STIV/A8 calibration meters.** For each $L$, run the STIV and area‑law meters to verify detector behavior and units/normalization; record preliminary $N(L)$, $\alpha_E$, and hierarchy diagnostics for context (not gated here).
3. **Execute A8 two‑gate runs.** For each spec in `a8-two-gate.v1.json`, generate interface configurations and energy fields, apply detectors, and compute $N(L)$ and $E_{\mathrm{exc}}(L)$ across seeds.
4. **Fit and model comparison.** Fit $N(L)$ vs $\log L$ and $\log E_{\mathrm{exc}}(L)$ vs $\log L$ according to preregistered windows; compute slopes, $R^2$, and ΔAIC/ΔBIC against volume‑law and alternative nulls; bootstrap CIs and log all metrics in JSON/CSV.
5. **Gate evaluation and routing.** Apply PRE‑REG pass/fail rules on $b_N$, $\alpha_E$, $R^2$, and model‑selection metrics. On PASS, publish RESULTS_* with numbered figures and artifacts (PNG+CSV+JSON via `io_paths`); on FAIL, route all artifacts to `failed_runs/` with a CONTRADICTION_REPORT summarizing detector behavior, fit diagnostics, and which metrics violated the gates.

## 6. Personnel

Justin K. Lietz will design the hierarchy‑gates experiment, select detectors and null models, and interpret regression and model‑selection diagnostics under the A8 program. Collaborators (to be named) will implement and maintain the hierarchy‑measurement runners, manage datasets and specs, and assist with fit and CI calculations under this preregistered protocol.

## 7. References

- A8 milestones and gaps:
  - [`T8-A8_Milestones.md`](Derivation/Axioms/T8-A8_Milestones.md) — includes EBN‑CMB and EBN‑Analog‑Horizon milestones that depend on validated hierarchy meters.
  - [`T8-A8_Gaps.md`](Derivation/Axioms/T8-A8_Gaps.md) — gap analysis guiding hierarchy‑measurement design.
- Hierarchy and area‑law meters:
  - [`T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md`](Derivation/Hierarchy/STIV/T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md) — STIV macrostate and gradient‑flow meters for A8.
  - [`T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md`](Derivation/Axioms/A8_Scaling_2D3D/T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md) — A8 area‑law instrument providing prior calibration for boundary‑energy scaling.
- Program context and standards:
  - [`Derivation/Unification/T0_Unification_Program_Spec_v1.md`](Derivation/Unification/T0_Unification_Program_Spec_v1.md) — A8 and hierarchy program threads, including meters and gates.
  - [`Derivation/TIER_STANDARDS.md`](Derivation/TIER_STANDARDS.md) — tier ladder and invariants for T3 smoke tests.
  - [`Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md`](Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) — global KPIs and meter gates reused by hierarchy instruments.
