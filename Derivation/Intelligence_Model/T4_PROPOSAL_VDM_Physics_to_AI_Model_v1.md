<!-- White Paper Proposal Template compliance: whitepaper-grade, MathJax, explicit gates, provenance, and machine-actionable artifacts. -->

# 1. T4 (Prereg) — VDM Physics → AI Model Roadmap v1

> Created Date: 2025-11-04  
> Provenance commit: {git rev-parse HEAD}  
> Salted provenance: SHA256(commit || "VDM-Physics-to-AI-Model-2025-11-04")  
> Proposer contact(s): <justin@neuroca.ai>  
> License: see [LICENSE](LICENSE)

**Short summary (one-sentence TL;DR):**  
Proposed in this document is a preregistered T4 roadmap that elevates validated VDM meters and substrates (KG J-only, metriplectic gates, thermodynamic routing) into physics-native AI experiments without training, integrating external benchmarks (Quantum Echoes OTOC, Planck map robustness, ALMA T_CMB(z)) and new pulled-front complexity tests into a machine-actionable program with explicit pass/fail gates, schemas, and provenance.

## Practical Provenance pattern

- Compute salted hashes with a random salt; store base_sha256, salt_hex, salted_sha256 in the prereg.
- Commit prereg.
- Create an annotated, signed tag like prereg.vdm_ai_model.v1.YYYYMMDDThhmmZ whose message includes:
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

- T0 (Concept): physics-native intelligence substrate concept, [Derivation/Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md](Derivation/Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md)
- T1 (Proto-model): KG J-only meters and invariants, [Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md)
- T2 (Instrument): RD conservation and balance QA, [Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md](Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md)
- T3 (Smoke): Thermodynamic routing meters and results, [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md)
- Canon/gates registry: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md), [Derivation/UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Prometheus_VDM (PI, implementer, approver)

## 3. Abstract

A physics-native AI program is preregistered that (i) certifies conservative, reversible substrates and meters, (ii) integrates external empirical benchmarks to calibrate VDM meters (Google’s Quantum Echoes OTOC advantage; Planck likelihood robustness; ALMA T_CMB at z=0.89), and (iii) tests metriplectic pulled-front predictions that dissipation can increase boundary complexity with logarithmic and discrete-scale-invariant signatures. Success yields reproducible, training-free primitives operating in real-time with claims limited strictly to meter fidelity under explicit gates and provenance discipline.

## 4. Background & Scientific Rationale

Analogy: As a carefully graded riverbed shapes currents without consuming energy, a conservative field substrate can shape and stabilize information flow without training. First certify the bed (meters), then release tracers (probes), then test assistance under metriplectic composition.

Context and prior VDM instruments:

- KG limb: locality/dispersion fidelity and Noether receipts (see images and CSVs in [Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/KG_Jonly_Dispersion.png](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/KG_Jonly_Dispersion.png) and [Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/KG_Jonly_Locality.png](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/KG_Jonly_Locality.png)).
- RD QA: discrete conservation and balance meters, [Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md](Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md).
- Thermodynamic routing: wave-flux meters and phased results, [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md).

New external calibration drivers (from Daily-Pulse brainstorming)

- Quantum Echoes OTOC(2) on Google Willow reports ~13,000× classical speedup and verifiable outputs; this provides an empirical “echo→agency” calibration target.  
- Planck likelihood/map robustness (Oct 2025 preprint): cosmology inferences are stable across products once combined with ground-based data; use as a strong null for “CMB-meter” device gates.  
- ALMA measurement of T_CMB at z = 0.89 (5.13 ± 0.06 K): a high-precision target for the redshift–temperature law.

Why this is the next step: Prior meters are validated locally; now we bind them to external empirical curves for calibration and add pulled-front complexity tests aligned with metriplectic structure, all under prereg gates that constrain claims strictly to instrument fidelity.

Some questions to consider

- Novelty: The contribution is not new physics but rigorous integration of meters and calibration against external benchmarks; claims are limited to meter fidelity under gates.
- Necessity: Empirical calibration and prereg gating prevent post-hoc tuning; receipts and quarantines maintain integrity.
- Targets: Echo-decay vs OTOC envelope, CMB-meter robustness, T_CMB(z) consistency, and metriplectic pulled-front complexity signatures.
- Criticisms: Training-free substrate may underperform on benchmarks; claims are scoped to meter fidelity, not benchmark supremacy.
- Gaps: Assistance under Strang splitting; addressed with metriplectic gates (ΔL_h ≤ 0, identity residuals ≤ 1e-12, two-grid slope ≥ 2.90).

## 5. Intellectual Merit and Procedure

Importance: Establishes a physics-first AI substrate with empirical calibration.  
Broader impacts: Reproducible, training-free primitives; transparent scoring via dimensionless knobs; cross-domain portability enforced by gates.  
Approach: Phase-gated progression with external calibration: T2 substrate → T3 routing/probe-only → T4 prereg assistance (echo) → new T4 cross-benchmarks and pulled-front tests.  
Rigor: Approvals-first; schema validation; artifact minimum; contradiction quarantine.

### 5.1 Experimental Setup and Diagnostics

Domains covered

- KG J-only substrate (T2/T3 instrumentation)
- Metriplectic assisted-echo controllers (T4 prereg)
- Thermodynamic routing meters (wave flux)
- CMB-meter and T_CMB(z) check (cosmology instrument)
- RD pulled-front complexity (new T4 instrument)

Common grid/time

- N ∈ {256, 512, 1024}, dx = 1.0 (canonical units)
- Δt tied to CFL multiples {0.5, 1.0, 2.0} × CFL guard
- Steps: 200 (sweeps use early-stop on gate fail)
- Seeds: {1..12}

Meters and gates used across domains (canon: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md))

- Energy conservation drift: $\Delta E_\mathrm{RMS} = \mathcal{O}(\Delta t^2)$
- Power balance: $R^2(\partial_t e, -\nabla\cdot s)$; relative imbalance
- Determinism receipts: bitwise or ulp-bounded repetition
- Metriplectic: per-step $\Delta L_h \le 0$; identity residuals ≤ 1e-12; two-grid slope ≥ 2.90; $R^2 \ge 0.999$
- Assisted Echo CEG vs assistance $\lambda$
- CMB-meter robustness score R_metric across map/likelihoods
- T_CMB(z) residual vs $T_0(1+z)$ at z=0.89
- RD pulled-front: front position/logarithmic delay and log-periodic (DSI) signatures

#### Artifacts per run

- Exactly 1 PNG + 1 CSV + 1 JSON minimum per condition, routed via io helper with tag-based directories.

Equation exemplars and expectations

- KG equation of motion:  
  $$ \partial_t^2\,\phi - c^2\,\nabla^2\phi + \mu^2\,\phi = 0 $$
- Continuity residual scaling:  
  $$ r = \partial_t e + \nabla\cdot s,\quad \lVert r \rVert_2 = \mathcal{O}(\Delta t^2) $$
- Cosmology redshift-temperature law:  
  $$ T_\mathrm{CMB}(z) = T_0\,(1+z) $$
- Pulled-front position (logarithmic delay + DSI option):  
  $$ X(t) = v^* t - \eta\log t + b + \sum_j a_j \cos(\omega_j \log t + \varphi_j) $$

#### 5.1.1 Pre-Run Config Requirements

Required config and metadata

- [Derivation/code/physics/intelligence_model/APPROVAL.json](Derivation/code/physics/intelligence_model/APPROVAL.json)
- [Derivation/code/physics/intelligence_model/schemas](Derivation/code/physics/intelligence_model/schemas)  
  - vdm_ai_model.schema.json
- [Derivation/code/physics/intelligence_model/specs](Derivation/code/physics/intelligence_model/specs)  
  - vdm_ai_model.v1.json

##### APPROVALS.json (example)

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
  "proposal": "Derivation/Intelligence_Model/T4_PROPOSAL_VDM_Physics_to_A_I_Model_v1.md",
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

##### PRE-REGISTRATION.json (minimum keys)

```json
{
  "proposal_title": "VDM Physics → AI Model Roadmap (v1)",
  "tier_grade": "T4",
  "commit": "{git rev-parse HEAD}",
  "salted_provenance": "SHA256(commit || salt_hex)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Discrete energy drift in KG substrate scales O(dt^2) and remains below threshold epsilon_E", "direction": "decrease" },
    { "id": "H2", "statement": "Power balance achieves R^2 >= 0.9995 and imbalance <= 0.5%", "direction": "increase" },
    { "id": "H3", "statement": "Determinism receipts are bitwise or <= 1 ulp across repeats", "direction": "no-change" },
    { "id": "H4", "statement": "Metriplectic gates hold for assisted-echo across λ ∈ [0,0.5]", "direction": "no-change" },
    { "id": "H5", "statement": "CEG median at λ=0.5 >= 0.05 under MJM control sweeps", "direction": "increase" },
    { "id": "H6", "statement": "Echo-decay exponents match OTOC(2) envelope within ±2σ after noise rescaling", "direction": "no-change" },
    { "id": "H7", "statement": "CMB-meter is robust across Planck map/likelihood choices with Δθ within 0.2σ", "direction": "no-change" },
    { "id": "H8", "statement": "|ΔT| at z=0.89 vs 5.13±0.06 K <= 0.1 K unless model term is preregistered", "direction": "no-change" },
    { "id": "H9", "statement": "RD pulled-fronts show η>0 and significant log-periodic terms under increased dissipation", "direction": "increase" }
  ],
  "variables": {
    "independent": ["N", "dt", "lambda", "assist_order", "walker_on", "map_choice", "likelihood_choice", "dissipation_weight"],
    "dependent": ["CEG", "ΔE_RMS", "R^2_balance", "identity_residual", "two_grid_slope", "R_metric", "ΔT_z0p89", "η_log_delay", "DSI_significance"],
    "controls": ["seed", "boundary_mode", "operator_type"]
  },
  "pass_fail": [
    { "metric": "ΔE_RMS", "operator": "<=", "threshold": 0.0, "unit": "scaled by (dt/a)^2" },
    { "metric": "R^2_balance", "operator": ">=", "threshold": 0.9995, "unit": "-" },
    { "metric": "identity_residual", "operator": "<=", "threshold": 1e-12, "unit": "-" },
    { "metric": "two_grid_slope", "operator": ">=", "threshold": 2.90, "unit": "-" },
    { "metric": "CEG_median_lambda_0p5", "operator": ">=", "threshold": 0.05, "unit": "-" },
    { "metric": "OTOC_exponent_match_sigma", "operator": "<=", "threshold": 2.0, "unit": "σ" },
    { "metric": "CMB_R_metric_variation", "operator": "<=", "threshold": 0.2, "unit": "σ" },
    { "metric": "ΔT_z0p89", "operator": "<=", "threshold": 0.10, "unit": "K" },
    { "metric": "η_log_delay", "operator": ">=", "threshold": 0.0, "unit": "-" },
    { "metric": "DSI_AIC_gain", "operator": ">=", "threshold": 10.0, "unit": "AIC points" }
  ],
  "spec_refs": [
    "Derivation/code/physics/intelligence_model/specs/vdm_ai_model.v1.json"
  ],
  "registration_timestamp": "2025-11-04T00:00:00Z"
}
```

##### Specs (skeleton)

```json
{
  "run_name": "vdm_ai_model",
  "version": "1.0.0",
  "tag": "vdm_ai_model-v1",
  "schema_ref": "Derivation/code/physics/intelligence_model/schemas/vdm_ai_model.schema.json",
  "parameters": {
    "domain": ["kg_substrate", "assisted_echo", "wave_flux_meter", "cmb_meter", "rd_pulled_fronts"],
    "grid": {"N": [256, 512, 1024], "dx": 1.0},
    "dt_multiples": [0.5, 1.0, 2.0],
    "assist": {"lambda": [0.0, 0.1, 0.2, 0.3, 0.5], "order": ["JMJ", "MJM"]},
    "walker": {"enabled": [false, true], "amp": 0.2, "width": 8, "channel": "phi"},
    "cmb": {"maps": ["SMICA", "Commander"], "likelihoods": ["plik", "hiLLiPoP"]},
    "rd": {"dissipation_weight": [0.0, 0.2, 0.4, 0.6]},
    "steps": 200,
    "budget": 1e-2
  },
  "seeds": [1,2,3,4,5,6,7,8,9,10,11,12]
}
```

##### Schemas (minimum)

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

#### **Calibration Matrix (from Brainstorming.md synthesis)**

- Echo→Agency (Echoes→OTOC(2)): fit echo-decay exponent and prefactor; match OTOC envelope within ±1–2σ after rescaling to the substrate noise model; flip Echo→Agency gate to “empirical” if residuals are white.
- Cosmology-Null Consistency (CMB-meter): run ≥2 Planck map/likelihood combos; require Δθ for key parameters to remain within 0.2σ when adding ground-based datasets; treat deviations as pipeline bias.
- Redshift–Temperature Law (ALMA z=0.89): require |ΔT| ≤ 0.1 K vs 5.13 ± 0.06 K unless a preregistered VDM term is specified and gated.

#### New T4 experiments/controls

- T4_Echo-OTOC_Crossbench: Assisted-echo mapping against OTOC(2) target curves (JMJ, MJM, model_blind controls).
- T4_CMB-meter_v0: Robustness of R_metric under Planck map/likelihood swaps (with ground-based augmentation).
- T4_ALMA-Crosscheck: Compare VDM T(z) to $T_0(1+z)$ at z=0.89; enforce |ΔT| bound.
- T4_RD-PulledFronts: Fit $X(t)=v^* t - \eta\log t + b + \sum a_j \cos(\omega_j\log t + \varphi_j)$; PASS if $\eta>0$ and at least one log-periodic term is significant (AIC/BIC) under increased dissipation.

#### Exact Cartesian product (core subsets)

- N ∈ {256, 512, 1024}
- Δt ∈ {0.5, 1.0, 2.0} × CFL
- assist_order ∈ {JMJ, MJM}; λ ∈ {0.0, 0.1, 0.2, 0.3, 0.5}; walker_on ∈ {false, true}
- cmb: maps ∈ {SMICA, Commander}; likelihoods ∈ {plik, hiLLiPoP}
- rd: dissipation_weight ∈ {0.0, 0.2, 0.4, 0.6}
- seeds ∈ {1..12}; steps = 200

#### Estimated runtime

- KG substrate certification: 1–5 min per profile (CPU 1 thread)
- Assisted-echo per condition/seed: 1–3 min
- CMB-meter runs: I/O dominated; CPU-light per combination
- RD pulled-fronts: 1–3 min per condition
- Early-stop on gate FAIL with quarantine

#### Success actions

- Publish RESULTS_* with gate matrix PASS; figures with numeric captions; CSV and JSON logs; prereg tag recorded.

Failure actions

- Route to failed_runs; emit contradiction report JSON; retain tag; adjust dt/BC/operator or dissipation weights; rerun under same prereg with revision.

## 6. Personnel

- Proposer: Justin K. Lietz — design, preregistration, approvals, execution, and RESULTS authoring.  
- Roles include artifact policy enforcement, schema maintenance, J/M degeneracy and meter integrity reviews.

## 7. References

- Canon and gates: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md), [Derivation/UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)
- Substrate and meters: [Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md); [Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md)
- RD QA: [Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md](Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md)
- Thermodynamic routing: [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md), [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md)
- Policy: [Derivation/code/ARCHITECTURE.md](Derivation/code/ARCHITECTURE.md), [Derivation/code/common/authorization/README.md](Derivation/code/common/authorization/README.md)
- External calibration (sources to be attached in RESULTS and supplementary notes):
  - Google Research blog and supporting articles on Quantum Echoes (OTOC(2)) on Willow (Oct 22, 2025)
  - Planck map/likelihood robustness preprint (Oct 10, 2025; arXiv:2510.09430)
  - ALMA T_CMB at z=0.89 = 5.13 ± 0.06 K (ApJ Oct 29, 2025; Keio press Oct 30, 2025)

---
<!-- Appendix set capturing decisions and ideas from Daily-Pulse Brainstorming -->
### Appendix A — SOP: Phase-Transitioned Scaling for VDM/LLMs  

> (from Brainstorming.md, captured for future T5 pilot)

**Core idea:** treat model growth like a pulled front in knowledge space. A single “master” rapidly absorbs primitive facts; when saturation signals are met, freeze Master-k, then branch Sub-k,i experts that learn higher-order primitives bounded by the new transition surface.

#### Signals ( continuously measured )

- Coverage: novelty rate (Zipf tail mass; semantic dedup)
- Surprise: moving-average NLL on unseen shards; $d(\text{Surprise})/dt \to 0$ signals saturation
- Fisher rank / Hessian spectrum: top-K eigenvalues drop; spectrum narrows
- Compressibility: hidden activation compression plateaus
- DSI/log-periodic (optional): under tiny periodic curriculum perturbations, look for log-periodic oscillations in loss/frontier size as hierarchical boundary markers

#### Pulled-front pacing (time-for-scale trade)

- $\eta(t)=\eta_0/(1+\alpha t)$; $T(t)=T_0\log(1+\beta t)$ where $T$ is context window or batch temperature; induces $1/t$-like relaxation and log-time exploration without exploding capacity.

#### Metriplectic optimizer sketch

- Base dissipative optimizer step + conservative transformation (e.g., orthogonalization/symplectic reparam) that preserves loss but increases representational diversity; increase symmetric-bracket weight as saturation approaches to induce structured complexity vs overfitting.

#### Phase-transition trigger (gate over window $W$)

- Novelty rate < $\epsilon_\text{nov}$; $d(\text{NLL}_\text{holdout})/dt \approx 0$ and Fisher rank drop > $\epsilon_F$; compression gain < $\epsilon_\text{zip}$; (optional) clear log-periodic residuals under curriculum ping.

#### Branching & freezing

- Freeze Master-k weights; spawn $M$ experts $\{\text{Sub}_{k,i}\}_{i=1..M}$ with domain-specific priors and narrow curricula; constrain inter-expert metriplectic coupling.

#### Evaluation & progression

- Gate per expert; if PASS, either deepen (Sub-k+1,i) or expand M; if FAIL, prune/merge.

**Note:** SOP is recorded here to capture brainstorming decisions; it is not executed in this T4 prereg but will inform subsequent T5 pilots under separate preregistration.

---

### Appendix B — Decisions captured from brainstorming record

Source: [PRIVATE/Daily-Pulse/2025-11-04/Brainstorming.md](PRIVATE/Daily-Pulse/2025-11-04/Brainstorming.md)

#### B.1 External cross-benchmarks (calibration matrix details)

- Echo→Agency (OTOC(2) crossbench):
  - Target: Google Quantum Echoes (Willow) verified OTOC(2) workload and decay envelope.
  - Action: Fit assisted-echo decay exponent/prefactor and match OTOC envelope within ±2σ after noise-model rescaling. Flip Echo→Agency from “theoretical” to “empirical” when residuals are white.
  - Gate additions (extend PRE-REG): OTOC_exponent_match_sigma ≤ 2.0 (unit: σ).

- Cosmology-Null Consistency (CMB-meter):
  - Target: Planck map/likelihood choice robustness (arXiv:2510.09430).
  - Action: Run ≥2 map/likelihood combinations (e.g., SMICA/Commander × plik/hiLLiPoP) with ground-based augmentation; require parameter deltas Δθ to remain within 0.2σ.
  - Gate additions: CMB_R_metric_variation ≤ 0.2 σ.

- Redshift–Temperature Law (ALMA z=0.89):
  - Target: T_CMB(0.89) = 5.13 ± 0.06 K (ApJ Oct 29, 2025; Keio press Oct 30, 2025).
  - Action: Compare VDM T(z) to T0(1+z); enforce |ΔT| ≤ 0.10 K unless a preregistered model term is specified.
  - Gate additions: ΔT_z0p89 ≤ 0.10 K.

#### B.2 New T4 experiments derived from brainstorming

- T4_Echo-OTOC_Crossbench: Assisted-echo vs OTOC(2) decay alignment under JMJ/MJM/model_blind; report σ-match and residual whiteness.
- T4_CMB-meter_v0: R_metric robustness under map/likelihood swaps with ground-based augmentation.
- T4_ALMA-Crosscheck: T_CMB(z) at z=0.89 consistency check with 0.10 K gate.
- T4_RD-PulledFronts: Pulled-front fits with log delay + optional DSI terms:
  $$ X(t) = v^* t - \eta \log t + b + \sum_j a_j \cos(\omega_j \log t + \varphi_j) $$
  Gates: η_log_delay ≥ 0 and DSI_AIC_gain ≥ 10 (AIC points) under increased dissipation weight.

#### B.3 Event-driven runtime (no prior training) — integration decisions

- Always-on organism pattern (no offline loops):
  - Ephemeral adapters: rank-1/2 LoRA/IA³; online mirror descent updates O(1) ms/token.
  - Fast heads: RLS / online logistic probes for cheap supervised heads.
  - Oja/Hebb updates: streaming PCA-like subspace carving without trunk backprop.

- Tool/actuator routing:
  - Router choices (bandit + Dirichlet-Tree): {generate, retrieve, calculate, ask, abstain}.
  - Uncertainty head: when uncertainty > τ, route to verifiers (retrieval/calculator) or ask backpressure.

- Veracity gates:
  - Phase keys (example): veracity_gate = { min_verified_ratio: 0.6, max_uncal_conf: 0.2 }.
  - Telemetry additions: Brier score, ECE, veracity@k; citation-required mode for factual claims.

- Causal state cache:
  - Maintain session state (entities, claims, time); contradiction penalties; trigger clarifying question / lookup as needed.

#### B.4 Autophase gating and streaming metrics (no dense scans)

- Streaming, windowed metrics (computed every W events):
  - novelty_rate (MinHash/Bloom over token/semantic shingles),
  - dNLL_dt (EMA/Welford regression),
  - compression_gain (online entropy of activations/residuals),
  - fisher_rank (Hutchinson trace + randomized power iteration sketches),
  - ΔMDL = Δ(bits_model) + Δ(bits_residual) (adapter delta + running code-length).
- Autophase trigger (all must hold in a window W):
  - novelty_rate < ε_nov; |dNLL_dt| < ε_dNLL; fisher_rank < τ_F; compression_gain < ε_zip; ΔMDL < 0.
  - Emits BRANCH control event; freeze current path as Master-k; spawn 2 Sub-experts; route 10% canary to children until ΔMDL advantage is sustained, then promote winner.
- Example phase.json knobs to add:
  - auto_phase: true
  - window: 2048
  - epsilon_novelty: 0.02
  - epsilon_dNLL: 1e-4
  - fisher_rank_min: 12
  - epsilon_compress: 0.01
  - mdl_budget_bits: -2000
  - cooldown_events: 10000
  - canary_fraction: 0.1

#### B.5 Efficiency and budgets (bounded per-event cost)

- Per-event FLOPs and latency remain flat:
  - Trunk forward (frozen) + ≤2 rank-r adapters + fast head ⇒ O(d r) + O(d) overhead vs trunk.
  - Router cost O(E_hot) with E_hot ≤ 2.
  - Streaming metric updates O(1) amortized.
- Storage discipline:
  - Cold vs hot storage; lazy loading + eviction (LRU / recent-success).
  - Delta checkpoints, quantization (e.g., int8), engram compaction (dedup/merge).
  - Branch persists only if ΔMDL < 0; otherwise merge/retire.
- Monitors to add:
  - FLOPs/event and latency/event, hot RAM footprint plateau, ΔMDL per added MB.

#### B.6 Primitive admission wall and paradigm-shift protocol

- Admission barrier (deterministic gate):
  - Admit new primitive iff ΔMDL ≤ −τ_primitive and θ_min ≥ θ0 and constraints pass (units, symmetries, conservation).
  - τ_primitive grows with depth d to model rising wall (e.g., τ0·(1+γ d) or τ0 e^{γ d}).
- Orthogonality guards and null-space utilization:
  - Track principal angles between adapter directions; alert when θ_min < 15°.
  - Null-space utilization per layer: U = trace(P_adapters)/d; if U → 1, headroom exhausted.
- Paradigm-shift exam (rare, formal):
  - Fork Master-v2; require strictly shorter two-part code length (MDL), and preserved/improved calibration & invariance tests; backward-compatibility wrapper; version v1 retained for provenance.

#### B.7 Boundaries as orchestration gates (naming from “Physical Boundaries”)

- Causality/Latency gate: per-event FLOPs cap and latency SLOs.
- Measurement/Verification gate: veracity and calibration thresholds (Brier/ECE).
- Horizon/Overflow gate: hot RAM/VRAM caps, cold storage quotas with eviction/merge.
- Boundary promotion occurs only at the frontier when residual power and ΔMDL indicate compressible structure and constraints hold.

---

### Appendix C — Minimal runtime module plan (surgical augmentation; no rewrite)

- New files under fum_rt/ (naming per brainstorming decisions):
  - [fum_rt/runtime/router.py](fum_rt/runtime/router.py): Dirichlet-Tree + bandit router; sparse routing; canary mode.
  - [fum_rt/runtime/online_adapters.py](fum_rt/runtime/online_adapters.py): rank-1/2 LoRA/IA³ updates; Oja/Hebb; RLS/online-logistic head.
  - [fum_rt/runtime/metriplectic.py](fum_rt/runtime/metriplectic.py): conservative (loss-neutral diversity) step; symmetric-bracket ramp near saturation; ties to veracity.
  - [fum_rt/runtime/causal_contract.py](fum_rt/runtime/causal_contract.py): frozen primitives contract (units, symmetries, conservation), support masks, consistency tests.
- Extensions:
  - [fum_rt/runtime/phase.py](fum_rt/runtime/phase.py): autophase gate; cooldown/hysteresis; ΔMDL budgets.
  - [fum_rt/runtime/telemetry.py](fum_rt/runtime/telemetry.py): novelty_rate, dNLL_dt, compression_gain, fisher_rank, ΔMDL, veracity@k, ECE/Brier, residual-whiteness, log-periodic score.
  - [fum_live.py](fum_live.py): hook points — after loss compute: metriplectic.step(); phase gate check; BRANCH emission; router update.

---

### Appendix D — Example config snippets (drop-in)

- Veracity gate (phase.json):
  - { "veracity_gate": { "min_verified_ratio": 0.6, "max_uncal_conf": 0.2 } }
- Primitive gate (rising wall):
  - { "primitive_gate": {
      "enable": true,
      "delta_mdl_bits_threshold_base": 2000,
      "threshold_growth": {"type":"exp","gamma":0.15},
      "min_principal_angle_deg": 15,
      "consistency": ["units","symmetry:SO(3)","conservation:H"],
      "cooldown_events": 50000
    } }
- Adapter gate (easier than primitives):
  - { "adapter_gate": { "delta_mdl_bits_threshold": 200, "regime_gating": true } }
- Storage and router caps:
  - { "per_event_flops_cap": 1.0e9, "max_active_experts": 2,
      "storage": { "hot_ram_mb": 2048, "cold_disk_gb": 64,
                   "quantize": "int8", "checkpoint_delta": true },
      "router": { "sparse": true, "canary_frac": 0.1 } }

### Appendix E — Roadmap PR slices (implementation-ready)

- PR-1: Metrics & gates — extend telemetry with streaming metrics; dashboard surfacing; no behavior change until enabled.
- PR-2: Router (shadow mode) — introduce router.py; route-logging only; execution remains single-path.
- PR-3: Online adapters — add online_adapters.py; default rank=0; enable per-domain via phase.json.
- PR-4: Metriplectic step — add metriplectic.py; post-optimizer hook; default weight=0.
- PR-5: Branching & retention — implement freeze→spawn; canary routing and ΔMDL-based promotion; retention policy for merge/evict.

#### Note on scope and policy

- These runtime decisions are recorded here to capture the brainstorming direction and to inform T4/T5 execution planning. They do not alter the scope of physics claims; all claims remain meter- and gate-scoped. Any new experiments based on these runtime modules will be preregistered separately with their own PROPOSAL_ and APPROVAL.json in domain-specific paths, and executed only under approvals policy per [Derivation/code/common/authorization/README.md](Derivation/code/common/authorization/README.md).

End of appendices capturing brainstorming decisions (see source record: [PRIVATE/Daily-Pulse/2025-11-04/Brainstorming.md](PRIVATE/Daily-Pulse/2025-11-04/Brainstorming.md)).

---

> End of proposal. Upon approval, generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at the listed paths and create a signed prereg tag before execution. The above integrates and captures the decisions and ideas from the brainstorming record into prereg-executable sections (calibration matrix, new T4 experiments, SOP appendix).
