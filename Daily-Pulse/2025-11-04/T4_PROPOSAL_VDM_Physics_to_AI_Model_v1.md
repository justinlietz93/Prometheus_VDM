# 1. T4 (Prereg) — VDM Physics → AI Model Roadmap and Proposal
<!-- Whitepaper-grade; follow VDM template discipline. -->

> Created Date: 2025-11-04  
> Provenance commit: {git rev-parse HEAD}  
> Salted provenance (example): SHA256(commit || "VDM-Physics-to-AI-Model-2025-11-04")  
> Proposer contact(s): <justin@neuroca.ai>  
> License: see [LICENSE](/LICENSE)

**Short summary (one sentence TL;DR):**
Proposed in this document is a physics-native AI roadmap that elevates validated VDM meters and substrates (KG J-only, metriplectic structure, thermodynamic routing) into a preregistered T4 program for intelligence without training: certify conservative substrates (T2), then route, probe-only, and assist (T3–T5), with machine-actionable gates, schemas, and provenance-locked artifacts.

## **Practical Provenance pattern**

- Compute salted hashes with a random salt; store base_sha256, salt_hex, salted_sha256 in the prereg.
- Commit prereg.
- Create an annotated, signed tag like prereg.vdm_ai_model.v1.YYYMMDDThhmmZ whose message includes:
  - commit SHA
  - the prereg file path
  - the salted_provenance items (or a single manifest hash)
- Push the tag before running. Have the run record that tag in artifacts.
- The proposal document must include the matching hashes in section 5.1.1
- Once the proposal document is fully complete and matches the created artifacts, a hash can be created for the proposal file itself. Then all items can be pushed up before the run. The authorization / approval system will fail a run if this isn't done.
- Optional: timestamp the tag externally (OpenTimestamps/RFC3161) for independent dating.

Avoid circularity

## Tier Grades

This proposal is graded T4 (Prereg). Supporting prior work across the T-ladder is referenced:

- T0 (Concept): framing of physics-native intelligence and shared scores in [Derivation/Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md](Derivation/Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md)
- T1 (Proto-model): KG J-only meters and dispersion/locality instrumentation in [Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md)
- T2 (Instrument): RD instrumentation and conservation/balance QA, see [Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md](Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md), with artifacts in the same directory
- T3 (Smoke): Thermodynamic Routing meter pipelines and prereg series, e.g. [Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/RESULTS_Passive_Thermodynamic_Routing_v2.md](Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/RESULTS_Passive_Thermodynamic_Routing_v2.md)
- Additional canon and gates: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md), [Derivation/UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Prometheus_VDM (PI, implementer, approver)

## 3. Abstract

Proposed in this document is a preregistered T4 roadmap that unifies validated VDM physical meters (KG J-only invariants, metriplectic gates, thermodynamic routing receipts) into an AI substrate program that: (i) certifies a conservative, reversible field substrate (T2), (ii) layers probe-only sensing and routing (T3–T4), and (iii) introduces assistance and walker-mediated echo control under metriplectic constraints (T4–T5). Each phase is governed by explicit, machine-actionable gates aligned with canon, with artifacts routed, schema-validated, and provenance-locked. Target outcomes are physics-native intelligence primitives operating in real time without training, with reproducible scores defined by dimensionless knobs, and cross-domain portability enforced by gates and Strang-composition discipline.

## 4. Background & Scientific Rationale

Analogy: As a carefully graded riverbed shapes currents without expending energy, a conservative field substrate can shape and stabilize information flow without training. First certify the bed, then release tracers and routing.

Context and prior work:

- KG limb meters: locality and dispersion fidelity already validated under J-only structure; see figures and CSVs in [Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/KG_Jonly_Dispersion.png) and (../Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/KG_Jonly_Locality.png:1).
- RD QA: discrete conservation and balance instruments documented in [Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md](Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md) with KPI gates.
- Thermodynamic routing meters: wave flux instrumentation and prereg series in [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md) and results in [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md).
- Metriplectic structure: degeneracy conditions and entropy monotonicity gates summarized in [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md).

Why this is next: Prior instruments isolate meters and invariants. The roadmap formalizes how those meters become an AI substrate and routing stack, committing to prereg gates and artifact policies so that claims about “intelligence without training” are falsifiable and reproducible.

Questions considered

- Novelty: The aim is not novelty in physics, but disciplined, falsifiable integration of meters into an AI substrate with no training loop.
- Necessity: A substrate-first approach prevents overfitting and post-hoc optimization; it enforces receipts for determinism and conservation.
- Targets: Cross-domain portability of meters and shared scores; probe-only sensing stability; assistance efficiency under metriplectic gates.
- Impacted areas: Classical field simulation, non-equilibrium thermodynamics, and AI systems engineering.
- Criticisms: “No training” may underperform on benchmarks; addressed by focusing on meters and receipts as the claim, not task-specific accuracy.
- Gaps: Assistance composability under Strang splitting; addressed with explicit gates (ΔL_h ≤ 0, identity residuals, two-grid slope).

## 5. Intellectual Merit and Procedure

Importance: Establishes a physics-native basis for agency/AI by certifying the substrate and meters first.  
Broader impacts: Reproducible, training-free primitives; clarity on what is measured and why; cross-domain generalization governed by KPIs.  
Approach: Phase-gated progression: T2-substrate → T3 routing/probe-only → T4 prereg assistance (walker echoes) → T5 pilot controllers; each phase requires gate PASS before proceeding.  
Rigor: Approvals-first policy; schema validation; artifact minimum (PNG+CSV+JSON); contradiction quarantine.

### 5.1 Experimental Setup and Diagnostics

- Domains: Metriplectic (assisted echo), KG J-only (substrate), Thermodynamic Routing (wave flux meters).
- Substrate (Phase 1/T2): 2D KG J-only, leapfrog time-stepper, reflective or periodic BCs.
- Assistance (Phase 2/T4): 1D assisted-echo under metriplectic structure; Strang composition; assistance budgets and CEG metric.
- Grid/time: N ∈ {256, 512, 1024}, dx = 1.0 (canonical units), Δt tied to CFL multiples {0.5, 1.0, 2.0} × CFL.
- Diagnostics/meters:
  - Energy conservation drift (ΔE_RMS) scaling as O(Δt²).
  - Power balance R²(∂_t e, -∇·s).
  - Determinism receipts: bitwise or ulp-bounded repeatability.
  - Metriplectic gates: ΔL_h ≤ 0 per step; identity residuals ≤ 1e-12; two-grid slope ≥ 2.90; R² ≥ 0.999.
  - Assisted Echo CEG (composite echo gain) vs assistance λ and seeds.
- Artifacts: for each run, route via io helper with tag-based directories; produce exactly 1 PNG + 1 CSV + 1 JSON minimum.

Required parameters and defaults (domain-specific):

- KG J-only: c, m; grid (N_x, N_y), spacings (a_x, a_y), Δt, steps, seeds
- Assisted Echo: c, m, D, r, u; λ ∈ [0, 0.5]; walker_amp/width/channel when present; dt, steps, seeds; operator choice (spectral/FD)

#### 5.1.1 Pre-Run Config Requirements

- Required config and metadata:
  - [Derivation/code/physics/intelligence_model/APPROVAL.json](Derivation/code/physics/intelligence_model/APPROVAL.json)
  - [Derivation/code/physics/intelligence_model/schemas](Derivation/code/physics/intelligence_model/schemas)
    - vdm_ai_model.schema.json
  - [Derivation/code/physics/intelligence_model/specs](Derivation/code/physics/intelligence_model/specs)
    - vdm_ai_model.v1.json

APPROVALS.json

```json
{
  "preflight_name": "im_preflight",
  "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at Derivation/{domain}/ explicit review."
},
{
  "pre_registered": true,
  "proposal": "Derivation/Intelligence_Model/T4_PROPOSAL_VDM_Physics_to_AI_Model_v1.md",
  "allowed_tags": [
    "vdm_ai_model-v1"
  ],
  "schema_dir": "Derivation/code/physics/intelligence_model/schemas",
  "approvals": {
    "vdm_ai_model-v1": {
      "schema": "Derivation/code/physics/intelligence_model/schemas/vdm_ai_model.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto generated timestamp",
      "approval_key": "auto generated hashed key"
    }
  }
}
```

PRE-REGISTRATION.json

```json
{
  "proposal_title": "VDM Physics → AI Model Roadmap (v1)",
  "tier_grade": "T4",
  "commit": "{git rev-parse HEAD}",
  "salted_provenance": "SHA256(commit || salt_hex)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Discrete energy drift scales O(dt^2) and remains below threshold epsilon_E in KG substrate", "direction": "decrease" },
    { "id": "H2", "statement": "Power balance achieves R^2 >= 0.9995 and imbalance <= 0.5%", "direction": "increase" },
    { "id": "H3", "statement": "Determinism receipts are bitwise or <= 1 ulp across repeats", "direction": "no-change" },
    { "id": "H4", "statement": "Metriplectic gates hold for assisted-echo across lambda ∈ [0,0.5]", "direction": "no-change" },
    { "id": "H5", "statement": "CEG median at lambda=0.5 >= 0.05 under MJM control sweeps", "direction": "increase" }
  ],
  "variables": {
    "independent": ["N", "dt", "lambda", "assist_order", "walker_on"],
    "dependent": ["CEG", "ΔE_RMS", "R^2_balance", "identity_residual", "two_grid_slope"],
    "controls": ["seed", "boundary_mode", "operator_type"]
  },
  "pass_fail": [
    { "metric": "ΔE_RMS", "operator": "<=", "threshold": 0.0, "unit": "scaled by (dt/a)^2" },
    { "metric": "R^2_balance", "operator": ">=", "threshold": 0.9995, "unit": "-" },
    { "metric": "identity_residual", "operator": "<=", "threshold": 1e-12, "unit": "-" },
    { "metric": "two_grid_slope", "operator": ">=", "threshold": 2.90, "unit": "-" },
    { "metric": "CEG_median_lambda_0p5", "operator": ">=", "threshold": 0.05, "unit": "-" }
  ],
  "spec_refs": [
    "Derivation/code/physics/intelligence_model/specs/vdm_ai_model.v1.json"
  ],
  "registration_timestamp": "2025-11-04T00:00:00Z"
}
```

Specs

```json
{
  "run_name": "vdm_ai_model",
  "version": "1.0.0",
  "tag": "vdm_ai_model-v1",
  "schema_ref": "Derivation/code/physics/intelligence_model/schemas/vdm_ai_model.schema.json",
  "parameters": {
    "domain": ["kg_substrate", "assisted_echo", "wave_flux_meter"],
    "grid": {"N": [256, 512, 1024], "dx": 1.0},
    "dt_multiples": [0.5, 1.0, 2.0],
    "assist": {"lambda": [0.0, 0.1, 0.2, 0.3, 0.5], "order": ["JMJ", "MJM"]},
    "walker": {"enabled": [false, true], "amp": 0.2, "width": 8, "channel": "phi"},
    "steps": 200,
    "budget": 1e-2
  },
  "seeds": [1,2,3,4,5,6,7,8,9,10,11,12]
}
```

Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm_ai_model.schema.json",
  "title": "VDM Physics → AI Model v1",
  "type": "object",
  "properties": {
    "run_name": { "type": "string" },
    "version": { "type": "string" },
    "tag": { "type": "string" },
    "schema_ref": { "type": "string" },
    "parameters": { "type": "object" },
    "seeds": {
      "type": "array",
      "items": { "type": "integer", "minimum": 0 }
    }
  },
  "required": ["run_name", "version", "tag", "schema_ref", "parameters", "seeds"]
}
```

### 5.2 Experimental runplan

- Cartesian grid:
  - N ∈ {256, 512, 1024}; Δt ∈ {0.5, 1.0, 2.0} × CFL; assist_order ∈ {JMJ, MJM}; λ ∈ {0.0, 0.1, 0.2, 0.3, 0.5}; walker_on ∈ {false, true}; seeds ∈ {1..12}.
- Estimated runtime:
  - KG substrate certification: 1–5 minutes per profile (CPU 1 thread).
  - Assisted-echo sweeps (per condition): 1–3 minutes per seed.
  - Total: bounded by 12 seeds × 3 dt × 3 N × (controls) with early-stop on gate FAIL.
- Success actions:
  - Publish RESULTS_* with gate matrix PASS; figures + CSV + JSON; numeric captions; provenance receipts.
- Failure actions:
  - Route to failed_runs; emit contradiction report JSON; maintain exact tag; adjust dt/BC/operator; re-run under same prereg with new revision.

## 6. Personnel

- Proposer: Justin K. Lietz — design, preregistration, approvals, execution, and RESULTS authoring.  
- Roles: enforce artifact policy; schema maintenance; code reviews for J/M degeneracy and meter integrity.

## 7. References

- Canon and gates: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md), [Derivation/UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)
- Substrate and meters: [Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md)
- RD QA: [Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md](Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md)
- Thermodynamic routing: [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md), [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md)
- Policy: [Derivation/code/common/authorization/README.md](Derivation/code/common/authorization/README.md)

---
> End of proposal draft. Upon approval, generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at the listed paths and create a signed prereg tag before execution.
