# 1. T2 (Instrument) — Corrective Echo Gain (CEG) Metric Definition and Validation

> Created Date: 2025-11-05  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> **Short summary (one sentence TL;DR):** Proposed in this document is a T2 instrument defining the Corrective Echo Gain (CEG) metric, a dimensionless measure quantifying how much a model-aware rewind reduces echo error compared to a blind rewind, with explicit validation gates linking to metriplectic monotonicity (M2) and measurement projection (M6) targets in the T0 Unification Program.

## Practical Provenance Pattern

- Compute salted hashes with a random salt; store base_sha256, salt_hex, salted_sha256 in the prereg.
- Commit prereg.
- Create an annotated, signed tag like `prereg.ceg_metric.v1.YYYMMDDThhmmZ` whose message includes:
  - commit SHA
  - the prereg file path
  - the salted_provenance items (or a single manifest hash)
- Push the tag before running. Have the run record that tag in artifacts.
- The proposal document must include the matching hashes in section 5.1.1
- Once the proposal document is fully complete and matches the created artifacts, a hash can be created for the proposal file itself. Then all items can be pushed up before the run. The authorization / approval system will fail a run if this isn't done.
- Optional: timestamp the tag externally (OpenTimestamps/RFC3161) for independent dating.

***Avoid circularity***

## Tier Grade Context

This proposal is graded **T2 (Instrument)**. It defines a measurement apparatus (the CEG metric) that will be used in higher-tier experiments. Supporting prior work:

- **T0 (Concept)**: Metriplectic structure and J→M projection framework documented in [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md)
- **T1 (Proto-model)**: Echo experiments and rewind protocols referenced in Daily-Pulse notes on entropy echoes and self-model efficacy

The CEG metric directly supports:
- **M2 (Metriplectic Lyapunov monotonicity)**: By quantifying correction efficacy while respecting degeneracy constraints
- **M6 (Measurement as epistemic projection)**: By measuring how M-limb corrections improve reversibility when projecting from J-limb

## 2. List of Proposers and Associated Institutions/Companies

- **Justin K. Lietz** — Prometheus_VDM (PI, implementer, approver)

## 3. Abstract

Proposed in this document is the Corrective Echo Gain (CEG), a dimensionless T2 instrument that quantifies the efficacy of model-aware corrections during echo/rewind protocols. CEG is defined as the fractional reduction in echo error achieved by an assisted rewind compared to a baseline blind rewind: CEG = (E_baseline − E_assisted) / E_baseline. This metric is bounded in (-∞, 1], where 1.0 represents perfect correction, 0.0 indicates no improvement, and negative values signal degradation. The CEG instrument will be validated across multiple regimes (reaction-diffusion, Klein-Gordon J-only, metriplectic assisted echo) with explicit pass/fail gates tied to Noether drift (≤1e-12), monotone entropy sum (ΔΣ ≥ 0), and reproducibility across seeds. Artifacts include PNG figures, CSV tables, and JSON provenance logs routed via the io_paths.py helper, consistent with VDM canon and T0 validation metrics.

## 4. Background & Scientific Rationale

**Context and motivation:**

The VDM framework posits that measurement and irreversibility arise from an epistemic projection (M-limb) of an underlying reversible dynamics (J-limb). When rewinding or correcting trajectories, a "blind" rewind that ignores the M-limb structure will accumulate errors from uncompensated dissipation and coarse-graining. A "model-aware" or "assisted" rewind that uses learned or analytical corrections (e.g., via self-model memory, metriplectic splitting, or walker-mediated control) should reduce this error by respecting the J/M degeneracy conditions and entropy monotonicity.

**Why this experiment is necessary:**

The T0 Unification Program requires quantitative gates for:
- **M2**: Metriplectic integrators must satisfy ΔL_h ≤ 0, identity residuals ≤ 1e-12, and two-grid slope ≥ 2.90.
- **M6**: Born-rule meters must converge with KL divergence ≤ 1e-3, demonstrating that M-limb statistics emerge reproducibly from J-limb reversibility.

Without a standardized metric for "correction efficacy," claims that self-models or assisted protocols "help" remain qualitative. The CEG instrument provides a falsifiable, unit-consistent measure of improvement that can be compared across domains, integrators, and hardware.

**Novel aspects:**

- **Dimensionless and portable**: CEG is independent of system size, units, or specific error functional, making it applicable to RD systems, KG fields, cosmology codes, and agency experiments.
- **Falsifiable gates**: CEG must co-pass with Noether and monotone-sum gates; failure of either invalidates the correction.
- **Reproducible and pre-registered**: All seeds, commits, and artifact paths are logged, enabling exact reproduction.

**Target findings requisite for future work:**

Establishing CEG as a validated T2 instrument enables T3 smoke tests (e.g., assisted echo vs. baseline across noise levels), T4 pre-registered experiments (e.g., CEG vs. assistance budget λ), and T5 pilot studies (e.g., CEG in adaptive controllers or Nexus walkers).

**Criticisms and mitigation:**

- **Criticism**: CEG could be gamed by tuning the baseline to be artificially bad.
  - **Mitigation**: Baseline must use standard integrators (e.g., leapfrog, Strang split) with documented CFL and step size; any deviation requires justification and re-preregistration.
- **Criticism**: Negative CEG (degradation) could be hidden by selective reporting.
  - **Mitigation**: All runs (pass and fail) are logged with full provenance; contradiction policy enforces reporting of failures with JSON contradiction reports.
- **Criticism**: Echo error E is system-dependent and could be chosen post-hoc.
  - **Mitigation**: E must be pre-specified in PRE-REGISTRATION.json (e.g., L2 state error, overlap infidelity, or task loss); changing E invalidates the run.

**Potential gaps:**

- **Integrator sensitivity**: CEG may vary with integrator choice (RK4 vs. leapfrog vs. spectral). Addressed by requiring explicit documentation of steppers in PRE-REGISTRATION.json.
- **Finite-size effects**: Small domains may not exhibit clear separation between baseline and assisted. Addressed by specifying minimum grid sizes (N ≥ 256) in validation runs.

## 5. Intellectual Merit and Procedure

**Intellectual Merit:**

1. **Importance of scientific questions**: Quantifying correction efficacy directly addresses the J→M projection mechanism and the role of self-models in metriplectic systems, central to VDM's epistemic interpretation of irreversibility.
2. **Potential broader impacts**: A standardized CEG metric enables cross-domain comparison of correction strategies in thermodynamics, cosmology, AI substrates, and control theory.
3. **Clarity and reasonableness**: The metric is simple (one formula), unit-consistent, and requires only two echo runs (baseline and assisted) per condition.
4. **Planned level of rigor**: Pass/fail gates tied to Noether drift, monotone-sum, reproducibility, and seed control ensure scientific discipline.

### 5.1 Experimental Setup and Diagnostics

**Domains for validation:**

1. **Reaction-Diffusion (RD)**: 2D Fisher-KPP or Gray-Scott system with zero-flux boundaries.
2. **Klein-Gordon J-only**: 2D hyperbolic field with leapfrog integrator.
3. **Metriplectic Assisted Echo**: 1D telegraph-Fisher with Strang-split J/M composition and walker-mediated assistance.

**Parameters and defaults:**

- **Grid**: N ∈ {256, 512, 1024}, dx = 1.0 (canonical units)
- **Time step**: Δt tied to CFL multiples {0.5, 1.0, 2.0} × CFL_max
- **Forward duration**: T ∈ {100, 200, 500} steps
- **Seeds**: 12 per condition (seed ∈ {1..12})
- **Assistance budget** (when applicable): λ ∈ {0.0, 0.1, 0.2, 0.3, 0.5}

**Diagnostics required (per run):**

1. **Echo error (E)**: Pre-specified in PRE-REGISTRATION.json. Examples:
   - L2 state error: $E = \frac{\|u(2T) - u(0)\|_2}{\|u(0)\|_2}$
   - Overlap infidelity: $E = 1 - \frac{\langle u(0) | u(2T) \rangle}{|\langle u(0) | u(0) \rangle|}$
   - Task loss delta (for control experiments)
2. **Noether drift**: $|\Delta H| / |H(0)|$ (for J-only) or $|\Delta E| / |E(0)|$ (for full system) ≤ 1e-12 (scaled by step size if needed)
3. **Monotone sum**: $\Delta \Sigma = \Sigma(2T) - \Sigma(0) \geq 0$ (entropy-like Casimir)
4. **CEG**: $\text{CEG} = (E_{\text{baseline}} - E_{\text{assisted}}) / E_{\text{baseline}}$
5. **Reproducibility check**: Bitwise or ulp-bounded repeatability across identical seeds

**Minimum artifacts per run:**

- 1 PNG figure: CEG vs. regime (or CEG vs. λ if assistance is varied)
- 1 CSV log: columns `run_id, regime, seed, T, E_baseline, E_assisted, CEG, noether_drift, delta_sigma, pass_fail`
- 1 JSON log: full provenance (commit, tag, schema, seeds, parameters, gates)

**Equipment/tools required:**

- Standard Python numerical stack (NumPy, SciPy, Matplotlib)
- io_paths.py helper for artifact routing
- Integrators: leapfrog (KG), Strang split (metriplectic), RK4 or implicit (RD)
- No new fabrication required; uses existing codebase

### 5.1.1 Pre-Run Config Requirements

**Required config and metadata:**

- **Derivation/code/physics/metriplectic/APPROVAL.json** (or domain-specific)
- **Derivation/code/physics/metriplectic/schemas/ceg_metric.schema.json**
- **Derivation/code/physics/metriplectic/specs/ceg_metric.v1.json**

#### APPROVALS.json

```json
{
  "preflight_name": "ceg_preflight",
  "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at PROPOSALS/ with explicit review."
},
{
  "pre_registered": true,
  "proposal": "PROPOSALS/T2_PROPOSAL_CEG_Metric_Definition_v1.md",
  "allowed_tags": [
    "ceg_metric-v1"
  ],
  "schema_dir": "Derivation/code/physics/metriplectic/schemas",
  "approvals": {
    "ceg_metric-v1": {
      "schema": "Derivation/code/physics/metriplectic/schemas/ceg_metric.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto generated timestamp",
      "approval_key": "auto generated hashed key"
    }
  }
}
```

#### PRE-REGISTRATION.json

```json
{
  "proposal_title": "Corrective Echo Gain (CEG) Metric Definition and Validation",
  "tier_grade": "T2",
  "commit": "{git rev-parse HEAD}",
  "salted_provenance": "SHA256(commit || salt_hex)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "CEG for assisted rewind > 0 across at least 2 regimes with SNR >= 3", "direction": "increase" },
    { "id": "H2", "statement": "Noether drift <= 1e-12 for all J-only or J-limb components", "direction": "no-change" },
    { "id": "H3", "statement": "Monotone sum delta_sigma >= 0 for all M-limb components", "direction": "no-change" },
    { "id": "H4", "statement": "CEG reproducibility across seeds: CV <= 0.2", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["regime", "N", "dt", "T", "lambda", "seed"],
    "dependent": ["E_baseline", "E_assisted", "CEG", "noether_drift", "delta_sigma"],
    "controls": ["integrator_type", "boundary_mode", "error_functional"]
  },
  "pass_fail": [
    { "metric": "CEG_median", "operator": ">=", "threshold": 0.05, "unit": "-" },
    { "metric": "noether_drift", "operator": "<=", "threshold": 1e-12, "unit": "-" },
    { "metric": "delta_sigma", "operator": ">=", "threshold": 0.0, "unit": "-" },
    { "metric": "CEG_CV", "operator": "<=", "threshold": 0.2, "unit": "-" }
  ],
  "spec_refs": [
    "Derivation/code/physics/metriplectic/specs/ceg_metric.v1.json"
  ],
  "registration_timestamp": "2025-11-05T00:00:00Z"
}
```

#### Specs

```json
{
  "run_name": "ceg_metric",
  "version": "1.0.0",
  "tag": "ceg_metric-v1",
  "schema_ref": "Derivation/code/physics/metriplectic/schemas/ceg_metric.schema.json",
  "parameters": {
    "regimes": ["RD_fisher_kpp", "KG_jonly", "metriplectic_assisted_echo"],
    "grid": {"N": [256, 512, 1024], "dx": 1.0},
    "dt_multiples": [0.5, 1.0, 2.0],
    "T_forward": [100, 200, 500],
    "assistance": {"lambda": [0.0, 0.1, 0.2, 0.3, 0.5]},
    "error_functional": "L2_state_error"
  },
  "seeds": [1,2,3,4,5,6,7,8,9,10,11,12]
}
```

#### Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "ceg_metric.schema.json",
  "title": "CEG Metric Definition and Validation v1",
  "type": "object",
  "properties": {
    "run_name": { "type": "string" },
    "version": { "type": "string" },
    "tag": { "type": "string" },
    "schema_ref": { "type": "string" },
    "parameters": {
      "type": "object",
      "properties": {
        "regimes": { "type": "array", "items": { "type": "string" } },
        "grid": { "type": "object" },
        "dt_multiples": { "type": "array", "items": { "type": "number" } },
        "T_forward": { "type": "array", "items": { "type": "integer" } },
        "assistance": { "type": "object" },
        "error_functional": { "type": "string" }
      },
      "required": ["regimes", "grid", "error_functional"]
    },
    "seeds": {
      "type": "array",
      "items": { "type": "integer", "minimum": 0 }
    }
  },
  "required": ["run_name", "version", "tag", "schema_ref", "parameters", "seeds"]
}
```

### 5.2 Experimental Runplan

**Cartesian product of independent variables:**

- Regimes: {RD_fisher_kpp, KG_jonly, metriplectic_assisted_echo}
- N: {256, 512, 1024}
- Δt: {0.5, 1.0, 2.0} × CFL
- T: {100, 200, 500}
- λ (assistance): {0.0, 0.1, 0.2, 0.3, 0.5} (for metriplectic regime only)
- Seeds: {1..12}

**Estimated runtime:**

- Per condition (single regime, N, Δt, T, seed): 1-5 minutes (CPU single thread)
- Total conditions (excluding full Cartesian): ~100-200 runs (selective sampling)
- Total compute budget: ~10-20 hours (parallelizable across seeds/regimes)

**Success actions:**

1. Publish RESULTS_CEG_Metric_v1.md with gate matrix (all pass)
2. Archive figures (CEG vs. regime, CEG vs. λ), CSV tables, JSON logs
3. Update [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md) with CEG definition and thresholds
4. Tag commit with signed, dated provenance

**Failure actions:**

1. Route failed runs to `Derivation/code/outputs/failed_runs/ceg_metric_YYYYMMDD/`
2. Emit contradiction report JSON with exact gate failures
3. Maintain exact tag and commit; adjust integrator/BC/parameters as needed
4. Re-run under same prereg with new revision number (v1.1, v1.2, etc.)
5. Document failure modes in RESULTS_CEG_Metric_v1.md under "Contradiction Policy" section

**Result publication plan:**

- **Format**: Follow [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
- **Sections**: Abstract, Background, Methods, Results (tables + figures), Discussion, Provenance
- **Numeric captions**: All figures include exact gate thresholds and pass/fail status
- **CSV/JSON sidecars**: Deposited alongside figures in `Derivation/code/outputs/logs/metriplectic/ceg_metric/`

## 6. Personnel

**Proposer: Justin K. Lietz**

- **Role**: PI, implementer, approver
- **Responsibilities**:
  - Design and implement CEG metric in Python
  - Pre-register hypotheses and gates in PRE-REGISTRATION.json
  - Execute validation runs across regimes
  - Analyze results and publish RESULTS_CEG_Metric_v1.md
  - Enforce artifact policy and provenance discipline
  - Review and approve schema/spec files before execution

## 7. References

**Canon and gates:**

- [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md)
- [Derivation/EQUATIONS.md](../Derivation/EQUATIONS.md)
- [Derivation/UNITS_NORMALIZATION.md](../Derivation/UNITS_NORMALIZATION.md)
- [Derivation/ALGORITHMS.md](../Derivation/ALGORITHMS.md)

**T0 Unification Program:**

- [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md)

**Daily-Pulse source notes:**

- [Daily-Pulse/2025-10-30/define-the-CEG.md](../Daily-Pulse/2025-10-30/define-the-CEG.md)

**Policy:**

- [Derivation/code/common/authorization/README.md](../Derivation/code/common/authorization/README.md)

**Result standards:**

- [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---

> End of proposal. Upon approval, generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at the listed paths and create a signed prereg tag before execution.
