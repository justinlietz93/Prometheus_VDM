<!-- White Paper Proposal • Aligns to Templates/PROPOSAL_PAPER_TEMPLATE.md -->

# 1. T2 — GB Relaxation Meter under Oscillating Load (v1)

> **Created Date (UTC):** 2025-11-08  
> **Commit:** <TO_BE_FILLED_BY_PREREG git rev-parse HEAD>  
> **Salted Provenance:** base_sha256=<...>, salt_hex=<...>, salted_sha256=<...>  
> **Proposer contact(s):** Justin K. Lietz <justin@neuroca.ai>  
> **License:** [LICENSE](../../LICENSE)  
> **Short summary (TL;DR):** Establish a reproducible, auditable T2 instrument to quantify GB relaxation under oscillatory load using γ²-law fit, asymmetric emission threshold, cycle-Lyapunov descent, protocol-insensitivity, and A6-style dimensionless collapse, with artifacts routed via io helper and pass/fail gates defined in VALIDATION_METRICS.

Practical provenance pattern (per template):

- Store base_sha256, salt_hex, salted_sha256 in prereg files; commit prereg; create signed prereg tag with commit SHA, file paths, salted provenance; push tag before runs; record tag in artifacts. Include the same hashes in §5.1.1.

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Neuroca (PI, approver)
- VDM Physics (Boundaries) — implementation

---

## 3. Abstract

VDM proposes a Tier‑2 (instrument) procedure to measure nonequilibrium relaxation of grain boundaries (GBs) under oscillatory loading. The meter quantifies: (i) γ²‑law behavior for excess GB energy versus a scalar misfit/strain proxy, (ii) a minimal asymmetric emission threshold p0⋆ at which emissions co‑occur with cycle‑wise relaxation, (iii) Lyapunov‑like monotone descent of excess GB energy over cycles, (iv) protocol‑insensitivity under small‑Δ nuisance changes, and (v) scale‑program compliance via a dimensionless collapse and envelope gate. Canonical equations are referenced by anchors only (VDM‑E‑160..164). Acceptance gates and thresholds are specified in the canonical metrics registry. All artifacts (PNG/CSV/JSON) are written via the IO helper with deterministic seeds and commit hashes recorded, enabling reproducible T2 instrument validation.

---

## 4. Background & Scientific Rationale

Context and prior work:

- Nonequilibrium GB relaxation under cyclic driving surveyed in [Nonequilibrium‑grain‑boundaries.md](../References/Boundaries/Nonequilibrium-grain-boundaries.md).  
- Canon anchors (no duplication of formulas):  
  - γ² law: [VDM‑E‑160](../EQUATIONS.md#vdm-e-160)  
  - Asymmetric emission threshold p0⋆: [VDM‑E‑161](../EQUATIONS.md#vdm-e-161)  
  - Cycle‑Lyapunov descent (excess energy): [VDM‑E‑162](../EQUATIONS.md#vdm-e-162)  
  - Moiré‑contrast observable: [VDM‑E‑163](../EQUATIONS.md#vdm-e-163)  
  - Dimensionless groups for collapse: [VDM‑E‑164](../EQUATIONS.md#vdm-e-164)

Why this instrument:

- Converts qualitative GB relaxation into quantitative, gate‑validated measurements consistent with VDM axioms (measurability; scale by dimensionless groups; entropy trends on metric limb).  
- Supports later T3+ claims by ensuring the meter itself passes KPI gates and produces reproducible artifacts.  
- Embeds rigorous UQ practices (τ_int‑aware binning; correlated χ² with SVD truncation; CI stability), matching standards already adopted elsewhere in VDM.

---

## 5. Intellectual Merit and Procedure

Merit: The instrument formalizes longstanding GB relaxation diagnostics into anchor‑referenced, gate‑enforced, and artifact‑audited routines. It advances sampling exactness and error accounting norms from lattice practice into materials‑like GB contexts within VDM.

Planned rigor:

- IEEE‑754 float64, deterministic seeds, commit‑hash provenance.  
- IO policy via [`io_paths.py`](../code/common/io_paths.py).  
- Canon discipline: anchors only; no equation/number duplication.

---

## 5.1 Experimental Setup and Diagnostics

Required parameters (examples; units per UNITS_NORMALIZATION; domain‑specific specs registered in §5.1.1):

- Geometry/material tag: {system, orientation, temperature}
- Control: amplitude p0, frequency f, optional phase ϕ (small‑Δ variants)
- Cycles: C (e.g., 10–50 cycles per condition)
- Misfit/strain proxy: γ (dimensionless) or protocol‑derived equivalent
- Seeds: integer list (deterministic)

Diagnostics (counts and outputs):

- Excess GB energy E_ex(c) per cycle and/or E_ex(t) segmented by cycles (CSV + PNG)  
- Emission events per cycle (counts; threshold logic) (CSV + JSON)  
- Optional 2D field snapshots for spectral ring detection (Moiré contrast) (CSV + PNG)  
- Summary JSON with KPI gate statuses and metrics; contradiction report on failure

New tools/scripts implemented (single‑responsibility helpers):

- [`python.GBExcessEnergyGamma2Fitter()`](../code/common/instrument_helpers/boundaries/gb_energy_gamma2_fitter.py:1)  
- [`python.GBEmissionThresholdEstimator()`](../code/common/instrument_helpers/boundaries/gb_emission_threshold.py:1)  
- [`python.GBLyapunovCycleMonitor()`](../code/common/instrument_helpers/boundaries/gb_cycle_lyapunov.py:1)  
- [`python.GBMoireContrast()`](../code/common/instrument_helpers/boundaries/gb_moire_contrast.py:1)

---

## 5.1.1 Pre‑Run Config Requirements

Required config and metadata:

- Derivation/code/physics/materials/gb_relax_ust/APPROVAL.json  
- Derivation/code/physics/materials/gb_relax_ust/schemas/{tag}.schema.json  
- Derivation/code/physics/materials/gb_relax_ust/specs/{run_name}.{version}.json  
- Derivation/code/physics/materials/gb_relax_ust/PRE-REGISTRATION.json

APPROVALS.json (pattern per template; content adapted by runner tooling)

```json
{
  "preflight_name": "gb_relax_preflight",
  "description": "Approval manifest: preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight tests permitted; artifact-writing experiments require this proposal and an approval record.",
  "pre_registered": true,
  "proposal": "Derivation/Nonequilibrium/T2_PROPOSAL_GB_Oscillating_Load_v1.md",
  "allowed_tags": ["gb-osc-v1"],
  "schema_dir": "Derivation/code/physics/materials/gb_relax_ust/schemas",
  "approvals": {
    "gb-osc-v1": {
      "schema": "Derivation/code/physics/materials/gb_relax_ust/schemas/gb-osc-v1.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "TO_BE_FILLED_AT_APPROVAL",
      "approval_key": "TO_BE_FILLED_AT_APPROVAL"
    }
  }
}
```

PRE‑REGISTRATION.json (minimum keys; extended in practice)

```json
{
  "proposal_title": "T2 — GB Relaxation Meter under Oscillating Load (v1)",
  "tier_grade": "T2",
  "commit": "TO_BE_FILLED_BY_PREREG",
  "salted_provenance": "TO_BE_FILLED_BY_PREREG",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Excess energy follows γ² fit with R² ≥ 0.98 within registered band", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["p0", "f", "ϕ", "γ"],
    "dependent": ["E_ex", "emission_count", "drop_10", "moire_contrast"],
    "controls": ["geometry", "material", "C", "seed"]
  },
  "pass_fail": [
    { "metric": "kpi-gb-gamma2-law", "operator": ">=", "threshold": 0.98, "unit": "R^2" },
    { "metric": "kpi-gb-lyapunov-cycle", "operator": ">=", "threshold": 0.15, "unit": "fractional_drop_10" }
  ],
  "spec_refs": ["Derivation/code/physics/materials/gb_relax_ust/specs/gb-osc-v1.0.0.json"],
  "registration_timestamp": "TO_BE_FILLED_BY_PREREG"
}
```

Specs (minimum keys; runner‑specific fields added):

```json
{
  "run_name": "gb_oscillating_load",
  "version": "1.0.0",
  "tag": "gb-osc-v1",
  "schema_ref": "Derivation/code/physics/materials/gb_relax_ust/schemas/gb-osc-v1.schema.json",
  "parameters": {
    "p0": [0.05, 0.10, 0.15],
    "f": [0.5],
    "phi": [0.0, 0.1], 
    "C": 20,
    "gamma_levels": [0.0, 0.02, 0.04, 0.06],
    "seeds": [0,1,2]
  },
  "seeds": [0,1,2]
}
```

Schemas (minimum JSON Schema draft; extend for full validation):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "gb-osc-v1.schema.json",
  "title": "GB Oscillating Load v1",
  "type": "object",
  "properties": {
    "p0": { "type": "number", "minimum": 0.0 },
    "f": { "type": "number", "minimum": 0.0 },
    "phi": { "type": "number" },
    "C": { "type": "integer", "minimum": 1 },
    "gamma_levels": { "type": "array", "items": { "type": "number" } },
    "seeds": { "type": "array", "items": { "type": "integer" } }
  },
  "required": ["p0","f","C","gamma_levels","seeds"]
}
```

---

## 5.2 Experimental runplan

Plan:

- Cartesian product over γ levels and cycle budget C; sweep p0 ladder for threshold; fix f with small‑Δ ϕ variants for protocol‑insensitivity.  
- For each condition, collect E_ex(c) and emissions; optionally capture 2D fields for Moiré analysis.

Estimated runtime:

- Per run O(C·NlogN) for spectral steps when enabled; total budget scales with |γ|×|p0|×|ϕ|×|seeds|. Exact figures provided in run specs.

Success/failure actions:

- Success: All mandatory gates pass; RESULTS written per standards with figures/CSV/JSON.  
- Failure: Route to failed_runs and emit contradiction report JSON including seeds, commit hash, and gate diagnostics.

Publishing:

- Follow [RESULTS_PAPER_STANDARDS.md](../Templates/RESULTS_PAPER_STANDARDS.md) with numeric captions and sidecar CSV/JSON.

---

## 6. Personnel

- Justin K. Lietz — approval authority; scientific oversight; merge control.  
- VDM Physics (Boundaries) — implementation, diagnostics, artifact QA, gate enforcement.

---

## 7. References (canon anchors and repo paths)

- Equations and Observables: [VDM‑E‑160](../EQUATIONS.md#vdm-e-160), [VDM‑E‑161](../EQUATIONS.md#vdm-e-161), [VDM‑E‑162](../EQUATIONS.md#vdm-e-162), [VDM‑E‑163](../EQUATIONS.md#vdm-e-163), [VDM‑E‑164](../EQUATIONS.md#vdm-e-164)  
- Metrics and Gates: [VALIDATION_METRICS.md](../VALIDATION_METRICS.md)  
- Algorithms: [ALGORITHMS.md](../ALGORITHMS.md)  
- Standards: [RESULTS_PAPER_STANDARDS.md](../Templates/RESULTS_PAPER_STANDARDS.md)  
- Literature overview (non‑canonical): [Nonequilibrium‑grain‑boundaries.md](../References/Boundaries/Nonequilibrium-grain-boundaries.md)

---

Appendix A — Acceptance Gates (anchor summary; see VALIDATION_METRICS for thresholds):

- γ² law: [kpi-gb-gamma2-law](../VALIDATION_METRICS.md#kpi-gb-gamma2-law)  
- Emission threshold: [kpi-gb-asym-threshold](../VALIDATION_METRICS.md#kpi-gb-asym-threshold)  
- Cycle Lyapunov: [kpi-gb-lyapunov-cycle](../VALIDATION_METRICS.md#kpi-gb-lyapunov-cycle)  
- Protocol‑insensitivity: [kpi-gb-protocol-insensitivity](../VALIDATION_METRICS.md#kpi-gb-protocol-insensitivity)  
- Dimensionless collapse: [kpi-gb-dimless-collapse](../VALIDATION_METRICS.md#kpi-gb-dimless-collapse); envelope [kpi-a6-envelope-max](../VALIDATION_METRICS.md#kpi-a6-envelope-max)

Notes:

- No equations or numeric baselines are duplicated; anchors only.  
- Determinism and environment per [Derivation/code/ARCHITECTURE.md](../code/ARCHITECTURE.md).  
- Artifacts routed via [python.io_paths](../code/common/io_paths.py:1).
