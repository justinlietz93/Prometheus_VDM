# 1. T4 (Prereg) — Cold-Atom Test of VDM Causal Cone in Metriplectic Optical Lattice

> Created Date: 2025-11-05  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> **Short summary (one sentence TL;DR):** Proposed in this document is a T4 preregistered experimental program to measure the causal cone front velocity $v_{\text{VDM}}$ and width broadening factor β in a 2D optical lattice Bose gas with engineered dissipation, testing the prediction that $v_H \leq v_{\text{VDM}} \leq v_{\text{LR}}$ (Hamiltonian ≤ VDM ≤ Lieb-Robinson bound) with β shifts of 10-30% relative to dissipation-off baselines, using site-resolved quantum-gas microscopy and correlation function spreading post-quench.

## Practical Provenance Pattern

- Compute salted hashes with a random salt; store base_sha256, salt_hex, salted_sha256 in the prereg.
- Commit prereg.
- Create an annotated, signed tag like `prereg.cold_atom_causal_cone.v1.YYYMMDDThhmmZ` whose message includes:
  - commit SHA
  - the prereg file path
  - the salted_provenance items (or a single manifest hash)
- Push the tag before running. Have the run record that tag in artifacts.
- The proposal document must include the matching hashes in section 5.1.1
- Once the proposal document is fully complete and matches the created artifacts, a hash can be created for the proposal file itself. Then all items can be pushed up before the run. The authorization / approval system will fail a run if this isn't done.
- Optional: timestamp the tag externally (OpenTimestamps/RFC3161) for independent dating.

***Avoid circularity***

## Tier Grade Context

This proposal is graded **T4 (Prereg)**. It is a preregistered experimental test with falsifiable predictions. Supporting prior work:

- **T0 (Concept)**: Finite propagation and telegraph-Fisher causality documented in [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md), Target M1 (Local causality and finite propagation)
- **T1 (Proto-model)**: Telegraph-Fisher emergence and metriplectic structure in [Derivation/Metriplectic/](../Derivation/Metriplectic/)
- **T2 (Instrument)**: KG J-only dispersion meter and cone verification (referenced in T0 Section 3.1)
- **T3 (Smoke)**: Preliminary numerical simulations of correlation spreading in Bose-Hubbard + dissipation (if available)

This experiment directly supports:
- **M1 (Local causality and finite propagation)**: KG J-only dispersion fit slope/intercept match $c^2$ and $m^2$ with $R^2 \geq 0.999$; light-cone speed $v \leq c(1+0.02)$

## 2. List of Proposers and Associated Institutions/Companies

- **Justin K. Lietz** — Prometheus_VDM (PI, implementer, approver)
- **(Optional) Collaborating experimental group with quantum-gas microscope capabilities**

## 3. Abstract

Proposed in this document is a T4 preregistered experimental program to measure the causal cone front velocity and width broadening in a 2D optical lattice Bose gas with engineered local dissipation, testing VDM's metriplectic (Hamiltonian + dissipative) dynamics against Hamiltonian-only and Lieb-Robinson bounds. The experiment uses site-resolved quantum-gas microscopy to track first-order coherence $g^{(1)}(x,t)$ post-quench across lattice sites. Falsifiable predictions: (1) dissipation-modified velocity $v_{\text{VDM}}$ falls between purely Hamiltonian velocity $v_H$ and open-system bound $v_{\text{LR}}$, with SNR ≥ 6 on slope extraction; (2) front width FWHM exhibits β broadening of 10-30% relative to dissipation-off baseline, with SNR ≥ 4. Pass gates exclude pure Hamiltonian propagation (no dissipation effect) and pure diffusion ($\sim \sqrt{t}$) behavior. Artifacts include correlation-front tracking, velocity fits, width evolution plots, and full experimental provenance (lattice parameters, imaging latency, dissipation calibration).

## 4. Background & Scientific Rationale

**Context and motivation:**

The Lieb-Robinson bound establishes finite-speed propagation of correlations in local Hamiltonian lattice systems: $|[A_x(t), B_y]| \lesssim C \exp(-(d - v_{\text{LR}} t))$ for observables separated by distance $d$. Cold-atom experiments have observed light-cone-like spreading in closed systems. VDM extends this to metriplectic (Hamiltonian + dissipative) dynamics, predicting:
1. **Dissipation modifies velocity**: $v_H \leq v_{\text{VDM}} \leq v_{\text{LR}}$ (dissipation slows propagation but respects causal bounds)
2. **Front broadening**: Dissipation induces width increase (β shift) without converting to pure diffusion

**Why this experiment is necessary:**

The T0 Unification Program requires:
- **M1**: KG J-only dispersion and cone verification with $R^2 \geq 0.999$ and $v \leq c(1+0.02)$

While numerical meters validate M1 in simulations, experimental verification in a physical many-body quantum system provides:
1. Direct evidence that VDM's metriplectic structure applies to real quantum gases
2. Falsification: if $v_{\text{VDM}}$ violates the bounds or β is absent, VDM's dissipation model is excluded
3. Bridge to analog quantum simulation: establishes cold atoms as a VDM testbed

**Novel aspects:**

- **Metriplectic quantum gas**: First experimental test of metriplectic dynamics (Hamiltonian + engineered dissipation) in optical lattice
- **Site-resolved front tracking**: Quantum-gas microscope enables direct measurement of correlation front position and width vs. time
- **Quantitative bounds**: Pre-registered velocity and width predictions with explicit SNR thresholds

**Target findings requisite for future work:**

Establishing cold-atom causal cone measurements enables:
- **T5 pilot studies**: Extended tests with varying dissipation strength, lattice geometry, dimensionality
- **T6 main results**: Born-rule meter convergence in quantum measurement analogs
- **T7 out-of-sample**: Predictions for other analog systems (BEC phonons, polariton condensates)

**Criticisms and mitigation:**

- **Criticism**: Bosonic operators are unbounded; rigorous Lieb-Robinson bounds are unclear.
  - **Mitigation**: Benchmark against theoretical velocities from effective models (mean-field, tensor-network simulations) rather than claiming strict bounds. Report $v_{\text{VDM}}$ relative to simulated $v_H$ and $v_{\text{LR}}$.
- **Criticism**: Dissipation may blur the front or induce diffusion, making front extraction ambiguous.
  - **Mitigation**: Define front as 50% of peak correlation amplitude; require sharp front (not diffusive tail) by fitting to error-function profile and checking residuals.
- **Criticism**: Finite size and boundary reflections complicate timing.
  - **Mitigation**: Use lattice size > 10 × front propagation distance at longest time point; discard data near boundaries; report finite-size correction estimates.
- **Criticism**: Imaging latency/resolution may blur temporal dynamics.
  - **Mitigation**: Temporal resolution << front-crossing time; spatial resolution ≤ 1 lattice site; document camera specs and jitter in provenance.

**Potential gaps:**

- **Dissipation control**: Engineered dissipation (local loss, dephasing) must be stable and calibrated. Addressed by measuring dissipation rate via independent atom-loss and coherence-decay assays.
- **Heating**: Stray heating may mask dissipation effects. Addressed by monitoring temperature via time-of-flight imaging; requiring stable T throughout run.
- **Long-range interactions**: Next-nearest neighbor (NNN) hopping or dipolar interactions may distort cone. Addressed by verifying short-range model via spectroscopy; reporting NNN coupling upper bounds.

## 5. Intellectual Merit and Procedure

**Intellectual Merit:**

1. **Importance of scientific questions**: Testing VDM's metriplectic causal cone in a quantum many-body system addresses the fundamental question of how dissipation modifies information spreading in local quantum dynamics.
2. **Potential broader impacts**: Validates VDM in a physical (not just numerical) setting; establishes cold atoms as analog quantum simulators for VDM; enables cross-domain tests (cosmology, thermodynamics, agency) via shared metriplectic framework.
3. **Clarity and reasonableness**: Experiment uses established quantum-gas microscopy techniques, pre-registered analysis protocols, and explicit falsification criteria.
4. **Planned level of rigor**: Pre-registered velocity and width predictions, SNR thresholds, cross-check against simulations, full experimental provenance.

### 5.1 Experimental Setup and Diagnostics

**System:**

- **2D optical lattice** (square geometry preferred for symmetry)
- **Ultracold Bose gas** (e.g., $^{87}$Rb or $^{39}$K) in Mott insulator or superfluid regime
- **Quantum-gas microscope** with site-resolved imaging (spatial resolution ≤ 1 lattice spacing)
- **Engineered dissipation**: Local atom loss (via resonant light), local dephasing (via AC Stark shift noise), or measurement back-action

**Parameters and defaults:**

- **Lattice depth**: $V_0 \sim 10-20 E_R$ (tunable to control tunneling $J$ and on-site interaction $U$)
- **Filling**: $n \sim 1$ atom/site (Mott regime) or $n < 1$ (superfluid regime)
- **Quench protocol**: Start in ground state or low-entropy state; apply local perturbation (e.g., single-site removal or phase twist) at $t=0$
- **Dissipation strength**: $\Gamma \sim 0.1-1 J$ (engineered loss/dephasing rate)
- **Time points**: $t \in \{0, 5, 10, 20, 50, 100\} \times J^{-1}$ (adaptable based on $v$ estimates)
- **Repetitions**: $N_{\text{rep}} \geq 50$ per time point per condition (for shot noise averaging)

**Observables:**

1. **First-order coherence**: $g^{(1)}(x,t) = \langle \hat{\psi}^\dagger(x,t) \hat{\psi}(0,t) \rangle / \sqrt{n(x,t) n(0,t)}$, measured via matter-wave interference or Ramsey sequence
2. **Correlation envelope**: Radial profile $C(r,t) = \langle g^{(1)}(r,t) \rangle_{\text{angular average}}$
3. **Front position**: $r_{\text{front}}(t)$ defined as radius where $C(r,t) = 0.5 C_{\text{max}}$
4. **Front width**: FWHM of $C(r,t)$ profile
5. **Velocity**: $v = d r_{\text{front}} / dt$ (linear fit over multiple time points)

**Diagnostics required (per run):**

1. **Velocity $v_{\text{VDM}}$**: Slope of $r_{\text{front}}$ vs. $t$ with SNR ≥ 6
2. **Width FWHM$(t)$**: Track evolution vs. $t$; fit to $\text{FWHM}(t) = \text{FWHM}_0 + \beta t$
3. **Baseline $v_H$**: Measure with dissipation OFF (purely Hamiltonian)
4. **Bound $v_{\text{LR}}$**: Estimate from tensor-network simulation or mean-field calculation
5. **Velocity bounds check**: $v_H \leq v_{\text{VDM}} \leq v_{\text{LR}}$
6. **Width shift**: $\beta_{\text{dissipation}} / \beta_{\text{baseline}} \in [1.1, 1.3]$ (10-30% increase)
7. **Diffusion exclusion**: Fit $r_{\text{front}} \sim t^\alpha$; require $\alpha > 0.8$ (exclude $\alpha = 0.5$ diffusion)

**Minimum artifacts per run:**

- 1 PNG: Correlation envelope $C(r,t)$ vs. $r$ at multiple time slices, with front position markers
- 1 PNG: Front position $r_{\text{front}}$ vs. $t$, with linear fit and velocity extraction (baseline vs. dissipation)
- 1 PNG: Width FWHM vs. $t$, with β slope comparison (baseline vs. dissipation)
- 1 PNG: Velocity comparison (barplot: $v_H$, $v_{\text{VDM}}$, $v_{\text{LR}}$ with error bars and bounds check)
- 1 CSV: columns `condition, t, r_front, FWHM, C_max, v_fit, beta_fit, SNR_v, SNR_beta, bounds_check, pass_fail`
- 1 JSON: full experimental provenance (lattice depth $V_0$, tunneling $J$, interaction $U$, dissipation $\Gamma$, imaging specs, time points, $N_{\text{rep}}$, commit, tag)

**Equipment/tools required:**

- Quantum-gas microscope with site-resolved imaging (existing apparatus or collaborator access)
- Optical lattice setup (tunable depth, 2D geometry)
- Engineered dissipation: resonant laser for loss or AC Stark shift for dephasing
- Ramsey/interferometric sequence for coherence measurement (if not using direct imaging)
- Data analysis pipeline: Python (NumPy, SciPy, Matplotlib) + custom correlation extraction scripts
- io_paths.py helper for artifact routing

### 5.1.1 Pre-Run Config Requirements

**Required config and metadata:**

- **Derivation/code/physics/analog_quantum/APPROVAL.json**
- **Derivation/code/physics/analog_quantum/schemas/cold_atom_causal_cone.schema.json**
- **Derivation/code/physics/analog_quantum/specs/cold_atom_causal_cone.v1.json**

#### APPROVALS.json

```json
{
  "preflight_name": "cold_atom_causal_cone_preflight",
  "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at PROPOSALS/ with explicit review."
},
{
  "pre_registered": true,
  "proposal": "PROPOSALS/T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md",
  "allowed_tags": [
    "cold_atom_causal_cone-v1"
  ],
  "schema_dir": "Derivation/code/physics/analog_quantum/schemas",
  "approvals": {
    "cold_atom_causal_cone-v1": {
      "schema": "Derivation/code/physics/analog_quantum/schemas/cold_atom_causal_cone.schema.json",
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
  "proposal_title": "Cold-Atom Test of VDM Causal Cone in Metriplectic Optical Lattice",
  "tier_grade": "T4",
  "commit": "{git rev-parse HEAD}",
  "salted_provenance": "SHA256(commit || salt_hex)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Velocity v_VDM satisfies v_H <= v_VDM <= v_LR with SNR >= 6 on slope", "direction": "no-change" },
    { "id": "H2", "statement": "Width broadening beta_dissipation / beta_baseline in [1.1, 1.3] with SNR >= 4", "direction": "increase" },
    { "id": "H3", "statement": "Front scaling exponent alpha > 0.8 (exclude diffusion alpha=0.5)", "direction": "increase" },
    { "id": "H4", "statement": "Temperature stable throughout run (delta_T / T < 0.1)", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["dissipation_on", "lattice_depth_V0", "time_t", "dissipation_Gamma"],
    "dependent": ["r_front", "FWHM", "v_fit", "beta_fit", "alpha_scaling"],
    "controls": ["N_rep", "imaging_latency", "quench_protocol"]
  },
  "pass_fail": [
    { "metric": "v_bounds_check", "operator": "==", "threshold": 1, "unit": "bool (v_H <= v_VDM <= v_LR)" },
    { "metric": "SNR_v", "operator": ">=", "threshold": 6.0, "unit": "-" },
    { "metric": "beta_ratio", "operator": ">=", "threshold": 1.1, "unit": "-" },
    { "metric": "beta_ratio", "operator": "<=", "threshold": 1.3, "unit": "-" },
    { "metric": "SNR_beta", "operator": ">=", "threshold": 4.0, "unit": "-" },
    { "metric": "alpha_scaling", "operator": ">", "threshold": 0.8, "unit": "-" },
    { "metric": "temperature_stability", "operator": "<=", "threshold": 0.1, "unit": "-" }
  ],
  "spec_refs": [
    "Derivation/code/physics/analog_quantum/specs/cold_atom_causal_cone.v1.json"
  ],
  "registration_timestamp": "2025-11-05T00:00:00Z"
}
```

#### Specs

```json
{
  "run_name": "cold_atom_causal_cone",
  "version": "1.0.0",
  "tag": "cold_atom_causal_cone-v1",
  "schema_ref": "Derivation/code/physics/analog_quantum/schemas/cold_atom_causal_cone.schema.json",
  "parameters": {
    "lattice": {
      "geometry": "square_2D",
      "depth_V0": [10, 15, 20],
      "spacing_a": 532,
      "tunneling_J_estimate": "computed from V0"
    },
    "gas": {
      "species": "Rb87",
      "filling_n": 1.0,
      "regime": "Mott_insulator"
    },
    "dissipation": {
      "type": "local_loss",
      "strength_Gamma": [0.1, 0.5, 1.0],
      "calibration_method": "atom_loss_rate"
    },
    "quench": {
      "protocol": "single_site_removal",
      "location": "center"
    },
    "imaging": {
      "method": "fluorescence",
      "spatial_resolution_sites": 1.0,
      "temporal_resolution_us": 10
    },
    "time_points": [0, 5, 10, 20, 50, 100],
    "N_rep": 50
  }
}
```

#### Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "cold_atom_causal_cone.schema.json",
  "title": "Cold-Atom Causal Cone Test v1",
  "type": "object",
  "properties": {
    "run_name": { "type": "string" },
    "version": { "type": "string" },
    "tag": { "type": "string" },
    "schema_ref": { "type": "string" },
    "parameters": {
      "type": "object",
      "properties": {
        "lattice": { "type": "object" },
        "gas": { "type": "object" },
        "dissipation": { "type": "object" },
        "quench": { "type": "object" },
        "imaging": { "type": "object" },
        "time_points": { "type": "array", "items": { "type": "number" } },
        "N_rep": { "type": "integer" }
      },
      "required": ["lattice", "gas", "dissipation", "quench", "imaging", "time_points", "N_rep"]
    }
  },
  "required": ["run_name", "version", "tag", "schema_ref", "parameters"]
}
```

### 5.2 Experimental Runplan

**Conditions:**

- Dissipation: {OFF (baseline), ON (Γ = 0.1J, 0.5J, 1.0J)}
- Lattice depth: {10, 15, 20} $E_R$ (testing robustness across $J$ values)
- Time points: {0, 5, 10, 20, 50, 100} × $J^{-1}$
- Repetitions: $N_{\text{rep}} = 50$ per condition

Total runs: ~20 conditions (4 dissipation × 3 depths, with some prioritization)

**Estimated runtime:**

- Per time point per condition: 10-30 minutes (including equilibration, quench, imaging, readout)
- Total: ~40-80 hours (experiment-dependent; can be spread across multiple days)

**Success actions:**

1. Publish RESULTS_Cold_Atom_Causal_Cone_v1.md with gate matrix (all pass)
2. Archive figures (correlation envelopes, front tracking, velocity/width fits), CSV tables, JSON logs
3. Update [Derivation/Causality/](../Derivation/Causality/) with experimental validation
4. Tag commit with signed, dated provenance
5. Submit to experimental physics journal (Nature Physics, PRL, or PRA)

**Failure actions:**

1. Route failed runs to `Derivation/code/outputs/failed_runs/cold_atom_causal_cone_YYYYMMDD/`
2. Emit contradiction report JSON with exact gate failures (velocity bounds violated, β shift absent, diffusive behavior)
3. Assess whether VDM metriplectic model needs revision or experimental systematics dominate
4. Re-run with refined dissipation calibration, lattice parameters, or imaging protocols
5. Document failure modes in RESULTS_Cold_Atom_Causal_Cone_v1.md under "Contradiction Policy" section

**Result publication plan:**

- **Format**: Follow [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md) + experimental physics standards
- **Sections**: Abstract, Background, Experimental Setup, Methods, Results (velocity, width, bounds checks), Discussion, Supplementary (provenance, calibration curves, systematic checks)
- **Numeric captions**: All figures include exact gate thresholds, SNR values, pass/fail status
- **CSV/JSON sidecars**: Deposited alongside figures in `Derivation/code/outputs/logs/analog_quantum/cold_atom_causal_cone/`

## 6. Personnel

**Proposer: Justin K. Lietz**

- **Role**: PI, theoretical framework, pre-registration, data analysis, publication
- **Responsibilities**:
  - Define theoretical predictions ($v_H$, $v_{\text{LR}}$, β shifts)
  - Pre-register hypotheses and gates in PRE-REGISTRATION.json
  - Collaborate with experimental team on protocol design
  - Analyze data (front tracking, velocity/width fits) and publish RESULTS
  - Enforce artifact policy and provenance discipline

**(Optional) Experimental Collaborators:**

- **Role**: Quantum-gas microscope operation, dissipation engineering, imaging, data acquisition
- **Responsibilities**:
  - Execute cold-atom experiments per pre-registered protocol
  - Calibrate dissipation strength and monitor systematics
  - Deliver raw correlation data with full experimental provenance
  - Co-author RESULTS publication

## 7. References

**Canon and gates:**

- [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md)
- [Derivation/EQUATIONS.md](../Derivation/EQUATIONS.md)
- [Derivation/UNITS_NORMALIZATION.md](../Derivation/UNITS_NORMALIZATION.md)

**T0 Unification Program:**

- [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md)

**Causality:**

- [Derivation/Causality/](../Derivation/Causality/)

**Daily-Pulse source notes:**

- [Daily-Pulse/2025-10-31/cold-atom-test-of-the-vdm-causal-cone.md](../Daily-Pulse/2025-10-31/cold-atom-test-of-the-vdm-causal-cone.md)

**External references:**

- Lieb-Robinson bounds: Scholarpedia (https://www.scholarpedia.org/article/Lieb-Robinson_bounds)
- Maximal speed in open quantum systems: EMS Press (https://ems.press/content/book-chapter-files/24223)
- Quantum-gas microscopy: Greiner Lab thesis (https://greiner.physics.harvard.edu/assets/theses/peng_thesis.pdf)
- Tensor-network correlation spreading: Nature Comms (https://www.nature.com/articles/s42005-022-00848-9)

**Policy:**

- [Derivation/code/common/authorization/README.md](../Derivation/code/common/authorization/README.md)

**Result standards:**

- [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---

> End of proposal. Upon approval, generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at the listed paths and create a signed prereg tag before execution.
