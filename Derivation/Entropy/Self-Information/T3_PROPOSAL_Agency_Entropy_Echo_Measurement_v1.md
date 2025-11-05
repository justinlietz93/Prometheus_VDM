# 1. T3 (Smoke) — Agency as Entropy-Echo Measurement via Void-Walker Self-Information Flow

> Created Date: 2025-11-05  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> **Short summary (one sentence TL;DR):** Proposed in this document is a T3 smoke test defining agency as a measurable entropy-echo phenomenon, quantified by the dimensionless agency index $\mathcal{A} = E_{\text{echo}}(\delta,T) / R_{\text{VW}}$, where entropy-echo strength (per void-walker self-information flux) provides a falsifiable metric for distinguishing structured agency from noise across adaptive, scripted, random, and thermal baseline controls.

## Practical Provenance Pattern

- Compute salted hashes with a random salt; store base_sha256, salt_hex, salted_sha256 in the prereg.
- Commit prereg.
- Create an annotated, signed tag like `prereg.agency_entropy_echo.v1.YYYMMDDThhmmZ` whose message includes:
  - commit SHA
  - the prereg file path
  - the salted_provenance items (or a single manifest hash)
- Push the tag before running. Have the run record that tag in artifacts.
- The proposal document must include the matching hashes in section 5.1.1
- Once the proposal document is fully complete and matches the created artifacts, a hash can be created for the proposal file itself. Then all items can be pushed up before the run. The authorization / approval system will fail a run if this isn't done.
- Optional: timestamp the tag externally (OpenTimestamps/RFC3161) for independent dating.

***Avoid circularity***

## Tier Grade Context

This proposal is graded **T3 (Smoke)**. It performs exploratory validation of the agency-entropy-echo concept. Supporting prior work:

- **T0 (Concept)**: Agency field framework and J→M projection documented in [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md), Section 6.6 (Agency Field milestones M6.9)
- **T1 (Proto-model)**: Agency field witness proposals in [Derivation/Agency_Field/](../Derivation/Agency_Field/)
- **T2 (Instrument)**: CEG metric and echo protocols (see [PROPOSALS/T2_PROPOSAL_CEG_Metric_Definition_v1.md](./T2_PROPOSAL_CEG_Metric_Definition_v1.md))

This experiment directly supports:

- **M6 (Measurement as epistemic projection)**: By measuring how agency manifests as recoverable causal structure under forward→perturb→rewind protocols
- **Agency Field Target M6.9**: Witness reproducibility and dispersion/reversibility gates in J-only meters

## 2. List of Proposers and Associated Institutions/Companies

- **Justin K. Lietz** — Prometheus_VDM (PI, implementer, approver)

## 3. Abstract

Proposed in this document is a T3 smoke test defining agency as a quantifiable entropy-echo phenomenon measured via void-walker self-information flow. Agency is operationalized through the dimensionless index $\mathcal{A} = E_{\text{echo}}(\delta,T) / R_{\text{VW}}$, where $E_{\text{echo}}$ measures the KL divergence between initial and rewound state distributions after a forward→perturb→rewind protocol, and $R_{\text{VW}}$ quantifies the self-information flux (bits/s) exported by void-walkers during the same window. The experiment tests whether structured, goal-directed walker policies increase $\mathcal{A}$ (per bit exported) compared to random or thermal baselines. Pass gates require $\mathcal{A}_{\text{adaptive}} > \mathcal{A}_{\text{random}}$ by ≥0.5σ across at least two perturbation scales δ, with stability under 10% integrator step changes. Artifacts include entropy-time curves, echo-delay curves, and CEG-style comparison tables, routed via io_paths.py with full provenance.

## 4. Background & Scientific Rationale

**Context and motivation:**

The VDM framework posits that agency arises from systems that can leave reproducible "information dents" in their environment—causal imprints that persist under decoherence and can be recovered via echo protocols. Traditional definitions of agency rely on subjective notions of "goal-directedness" or "autonomy"; this proposal operationalizes agency through thermodynamic and information-theoretic observables: entropy production, self-information flux, and echo fidelity.

**Why this experiment is necessary:**

The T0 Unification Program requires:

- **M6**: Born-rule meters must converge with KL divergence ≤ 1e-3, demonstrating emergent statistics from J→M projection.
- **Agency Field M6.9**: Witness reproducibility with dispersion and reversibility gates in J-only meters.

Without a quantitative, falsifiable definition of agency, claims about "adaptive behavior" or "self-model efficacy" remain vibes. This experiment provides:

1. A dimensionless agency index $\mathcal{A}$ that scales with causal dent per exported bit
2. Falsifiable predictions: adaptive > scripted > random > thermal
3. Controls for energy budget (ruling out trivial cooling)

**Novel aspects:**

- **Entropy-echo protocol**: Combines forward evolution, controlled perturbation, metriplectic rewind, and KL-divergence measurement into a single reproducible assay.
- **Self-information flux baseline**: Normalizes echo strength by the rate at which walkers export private state to public field (preventing "chatty but ineffective" policies from masking low agency).
- **Cross-policy comparison**: Tests thermal, random, scripted, and adaptive walkers under identical energy budgets, enabling direct falsification.

**Target findings requisite for future work:**

Establishing $\mathcal{A}$ as a validated T3 metric enables:

- **T4 pre-registered experiments**: Agency vs. coordination depth, agency vs. hierarchy scaling
- **T5 pilot studies**: Agency in thermodynamic routing, agency in cosmology analogs
- **T6 main results**: Agency-induced curvature, agency coherence gates

**Criticisms and mitigation:**

- **Criticism**: $\mathcal{A}$ could be gamed by defining echo error or self-information flux post-hoc.
  - **Mitigation**: Both must be pre-specified in PRE-REGISTRATION.json. Echo error uses KL divergence on pre-defined coarse-graining (K bins or latent encoder). Self-information uses mutual information $I(S_t; F_t)$ with fixed binning/kNN estimator.
- **Criticism**: Adaptive policies might simply export more bits, inflating $R_{\text{VW}}$ without increasing structure.
  - **Mitigation**: Energy budget is fixed across policies. If $R_{\text{VW}}$ increases but $E_{\text{echo}}$ does not, $\mathcal{A}$ will drop, falsifying the "more bits = more agency" hypothesis.
- **Criticism**: Metriplectic rewind may fail, biasing all $E_{\text{echo}}$ measurements.
  - **Mitigation**: Sanity checks on linear systems; conservation checks on J-limb; M-limb sign conventions documented and fixed.

**Potential gaps:**

- **Coarse-graining sensitivity**: $E_{\text{echo}}$ depends on bin count K. Addressed by pre-registering K and testing stability over K ∈ {16, 32, 64}.
- **Finite-time effects**: Short T may not allow agency to manifest. Addressed by testing T ∈ {100, 500, 1000} steps.
- **Spatial heterogeneity**: Global entropy may mask local agency. Addressed by reporting cluster-wise and pooled analyses.

## 5. Intellectual Merit and Procedure

**Intellectual Merit:**

1. **Importance of scientific questions**: Operationalizing agency via thermodynamic observables addresses the fundamental question: "What is agency?" in a falsifiable, non-anthropomorphic way.
2. **Potential broader impacts**: A quantitative agency metric enables comparisons across biological systems, AI agents, and physical substrates, with applications in control theory, collective behavior, and emergence.
3. **Clarity and reasonableness**: The protocol is simple (forward→perturb→rewind→measure), requires only standard VDM infrastructure, and has explicit pass/fail gates.
4. **Planned level of rigor**: Pre-registered hypotheses, fixed energy budgets, multi-seed validation, and provenance-locked artifacts ensure reproducibility.

### 5.1 Experimental Setup and Diagnostics

**Domain:**

- **2D metriplectic field** with void-walkers (particles that interact with the field via local coupling and export state tokens/marks)
- **Field**: Telegraph-Fisher substrate with J/M split (Strang composition)
- **Walkers**: Four policy types: thermal (no memory), random (memoryless), scripted (fixed sequence), adaptive (goal-directed with self-model)

**Parameters and defaults:**

- **Grid**: N = 512 (2D), dx = 1.0
- **Time step**: Δt = 0.5 × CFL
- **Forward duration**: T ∈ {100, 500, 1000} steps
- **Perturbation**: δ ∈ {1e-6, 1e-5, 1e-4} (local kick magnitude)
- **Walker count**: n_walkers = 32 per cluster
- **Energy budget**: E_total = 1.0 (canonical units, fixed across policies)
- **Seeds**: 32 per condition
- **Coarse-graining**: K ∈ {16, 32, 64} bins (or latent encoder with pre-trained hash)

**Walker policies:**

1. **Thermal**: Brownian motion, no goal, no memory
2. **Random**: Random walk with fixed step size, no memory
3. **Scripted**: Pre-defined trajectory (e.g., circular patrol), no adaptation
4. **Adaptive**: Goal-directed navigation with self-model memory field (m) and ADC steering

**Diagnostics required (per run):**

1. **Entropy $S(t)$**: Shannon entropy of occupancy distribution $p_i(t) = n_i(t) / \sum_j n_j(t)$, where $i$ indexes coarse-grained bins
2. **Entropy production rate**: $\dot{S}(t) \approx (S(t+\Delta t) - S(t)) / \Delta t$
3. **Self-information flux**: $R_{\text{VW}} = \frac{1}{T} \sum_{t \leq T} I(S_t; F_t)$ [bits/s], where $I(S_t; F_t)$ is mutual information between walker private state $S_t$ and emitted field tokens $F_t$
4. **Echo error**: After forward to T, perturb by δ, rewind (metriplectic inverse), measure at 2T:
   $$E_{\text{echo}}(\delta, T) = \mathbb{E}_{\text{runs}} \left[ D_{\mathrm{KL}}\!\left(P(X_0) \,|\, P(\tilde{X}_0|\delta,T)\right) \right]$$
   where $P(X_0)$ is initial distribution and $P(\tilde{X}_0|\delta,T)$ is distribution after echo protocol
5. **Agency index**: $\mathcal{A} = E_{\text{echo}}(\delta,T) / R_{\text{VW}}$ (dimensionless, per bit)
6. **Energy budget check**: $\int_0^T P_{\text{walker}}(t) dt \leq E_{\text{total}}$ (power × time)

**Minimum artifacts per run:**

- 1 PNG: Entropy vs. time (per cluster + pooled), showing forward → decohere → rewind → refocus phases
- 1 PNG: Echo curve (x-axis = τ delay, y-axis = $E_{\text{echo}}(\tau)$ or $\dot{S}_{\text{echo}}(\tau)$), with passive diffusion band
- 1 PNG: Agency index comparison (x-axis = policy type, y-axis = $\mathcal{A}$, with error bars)
- 1 CSV: columns `run_id, policy, cluster_id, K, tau, T, S0, S_tau, S_2tau, Echo, R_VW, A, dSdt_refocus, CI_low, CI_high, energy_used, pass_fail`
- 1 JSON: full provenance (commit, tag, schema, seeds, parameters, gates)

**Equipment/tools required:**

- Python: NumPy, SciPy, Matplotlib, sklearn (for kNN MI estimator)
- io_paths.py helper for artifact routing
- Metriplectic integrator (Strang split)
- Walker simulator (existing or new; random, scripted, adaptive policies)
- Coarse-graining module (K-bin histogram or VAE latent encoder)

### 5.1.1 Pre-Run Config Requirements

**Required config and metadata:**

- **Derivation/code/physics/agency/APPROVAL.json**
- **Derivation/code/physics/agency/schemas/agency_entropy_echo.schema.json**
- **Derivation/code/physics/agency/specs/agency_entropy_echo.v1.json**

#### APPROVALS.json

```json
{
  "preflight_name": "agency_entropy_echo_preflight",
  "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at PROPOSALS/ with explicit review."
},
{
  "pre_registered": true,
  "proposal": "PROPOSALS/T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md",
  "allowed_tags": [
    "agency_entropy_echo-v1"
  ],
  "schema_dir": "Derivation/code/physics/agency/schemas",
  "approvals": {
    "agency_entropy_echo-v1": {
      "schema": "Derivation/code/physics/agency/schemas/agency_entropy_echo.schema.json",
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
  "proposal_title": "Agency as Entropy-Echo Measurement via Void-Walker Self-Information Flow",
  "tier_grade": "T3",
  "commit": "{git rev-parse HEAD}",
  "salted_provenance": "SHA256(commit || salt_hex)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Agency index A_adaptive > A_random by >= 0.5 sigma across at least two delta scales", "direction": "increase" },
    { "id": "H2", "statement": "Monotone trend: A_thermal < A_random < A_scripted < A_adaptive", "direction": "increase" },
    { "id": "H3", "statement": "Agency index stable under 10% integrator step changes", "direction": "no-change" },
    { "id": "H4", "statement": "Energy budget constraint: actual energy <= E_total across all policies", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["policy_type", "delta", "T", "K_bins", "seed"],
    "dependent": ["S0", "S_tau", "S_2tau", "Echo", "R_VW", "A", "dSdt_refocus"],
    "controls": ["n_walkers", "energy_budget", "coarse_graining_method"]
  },
  "pass_fail": [
    { "metric": "A_adaptive_median", "operator": ">=", "threshold": 0.05, "unit": "-" },
    { "metric": "A_adaptive_vs_random_delta", "operator": ">=", "threshold": 0.5, "unit": "sigma" },
    { "metric": "trend_A_thermal_to_adaptive", "operator": "==", "threshold": 1, "unit": "bool (monotone)" },
    { "metric": "energy_violation", "operator": "<=", "threshold": 0.0, "unit": "-" }
  ],
  "spec_refs": [
    "Derivation/code/physics/agency/specs/agency_entropy_echo.v1.json"
  ],
  "registration_timestamp": "2025-11-05T00:00:00Z"
}
```

#### Specs

```json
{
  "run_name": "agency_entropy_echo",
  "version": "1.0.0",
  "tag": "agency_entropy_echo-v1",
  "schema_ref": "Derivation/code/physics/agency/schemas/agency_entropy_echo.schema.json",
  "parameters": {
    "grid": {"N": 512, "dx": 1.0},
    "dt": 0.5,
    "T_forward": [100, 500, 1000],
    "perturbation_delta": [1e-6, 1e-5, 1e-4],
    "n_walkers": 32,
    "energy_budget": 1.0,
    "policies": ["thermal", "random", "scripted", "adaptive"],
    "K_bins": [16, 32, 64],
    "MI_estimator": "kNN"
  },
  "seeds": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
}
```

#### Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "agency_entropy_echo.schema.json",
  "title": "Agency Entropy-Echo Measurement v1",
  "type": "object",
  "properties": {
    "run_name": { "type": "string" },
    "version": { "type": "string" },
    "tag": { "type": "string" },
    "schema_ref": { "type": "string" },
    "parameters": {
      "type": "object",
      "properties": {
        "grid": { "type": "object" },
        "dt": { "type": "number" },
        "T_forward": { "type": "array", "items": { "type": "integer" } },
        "perturbation_delta": { "type": "array", "items": { "type": "number" } },
        "n_walkers": { "type": "integer" },
        "energy_budget": { "type": "number" },
        "policies": { "type": "array", "items": { "type": "string" } },
        "K_bins": { "type": "array", "items": { "type": "integer" } },
        "MI_estimator": { "type": "string" }
      },
      "required": ["grid", "dt", "T_forward", "policies"]
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

- Policy: {thermal, random, scripted, adaptive}
- T: {100, 500, 1000}
- δ: {1e-6, 1e-5, 1e-4}
- K: {16, 32, 64}
- Seeds: {1..32}

Total conditions (selective sampling): ~100-200 runs (not full Cartesian; prioritize adaptive vs. random at multiple δ and T)

**Estimated runtime:**

- Per condition (single policy, T, δ, seed): 5-15 minutes (CPU + GPU for walker simulation)
- Total compute budget: ~20-50 hours (parallelizable across seeds)

**Success actions:**

1. Publish RESULTS_Agency_Entropy_Echo_v1.md with gate matrix (all pass)
2. Archive figures (entropy-time, echo-delay, agency comparison), CSV tables, JSON logs
3. Update [Derivation/Agency_Field/](../Derivation/Agency_Field/) with validated agency metric
4. Tag commit with signed, dated provenance

**Failure actions:**

1. Route failed runs to `Derivation/code/outputs/failed_runs/agency_entropy_echo_YYYYMMDD/`
2. Emit contradiction report JSON with exact gate failures
3. Maintain exact tag and commit; adjust walker policies/energy budgets as needed
4. Re-run under same prereg with new revision number (v1.1, v1.2, etc.)
5. Document failure modes in RESULTS_Agency_Entropy_Echo_v1.md under "Contradiction Policy" section

**Result publication plan:**

- **Format**: Follow [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
- **Sections**: Abstract, Background, Methods, Results (tables + figures), Discussion, Provenance
- **Numeric captions**: All figures include exact gate thresholds and pass/fail status
- **CSV/JSON sidecars**: Deposited alongside figures in `Derivation/code/outputs/logs/agency/agency_entropy_echo/`

## 6. Personnel

**Proposer: Justin K. Lietz**

- **Role**: PI, implementer, approver
- **Responsibilities**:
  - Implement entropy-echo protocol and agency index calculation
  - Pre-register hypotheses and gates in PRE-REGISTRATION.json
  - Execute validation runs across policies and conditions
  - Analyze results and publish RESULTS_Agency_Entropy_Echo_v1.md
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

**Agency Field:**

- [Derivation/Agency_Field/](../Derivation/Agency_Field/)

**Daily-Pulse source notes:**

- [Daily-Pulse/2025-11-04/Quantifying-Agency-as-Entropy-Echo.md](../Daily-Pulse/2025-11-04/Quantifying-Agency-as-Entropy-Echo.md)
- [Daily-Pulse/2025-10-31/measuring-agency-through-entropy-echoes.md](../Daily-Pulse/2025-10-31/measuring-agency-through-entropy-echoes.md)

**Policy:**

- [Derivation/code/common/authorization/README.md](../Derivation/code/common/authorization/README.md)

**Result standards:**

- [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---

> End of proposal. Upon approval, generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at the listed paths and create a signed prereg tag before execution.
