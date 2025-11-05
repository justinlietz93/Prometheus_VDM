# 1. T3 (Smoke) — CMB Hemispherical Power Asymmetry as VDM Causal Genesis Witness

> Created Date: 2025-11-05  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> **Short summary (one sentence TL;DR):** Proposed in this document is a T3 smoke test measuring the hemispherical power asymmetry in Planck PR4 CMB maps to assess whether the observed ~3% directional modulation is consistent with VDM's diffusive-expansion causal genesis prediction, using rotation-robustness metric R and off-diagonal covariance $C_{\ell,\ell+1}$ with explicit pass/fail gates tied to cosmology continuity (M4) and emergent gravity (M5) targets.

## Practical Provenance Pattern

- Compute salted hashes with a random salt; store base_sha256, salt_hex, salted_sha256 in the prereg.
- Commit prereg.
- Create an annotated, signed tag like `prereg.cmb_hemi_asym.v1.YYYMMDDThhmmZ` whose message includes:
  - commit SHA
  - the prereg file path
  - the salted_provenance items (or a single manifest hash)
- Push the tag before running. Have the run record that tag in artifacts.
- The proposal document must include the matching hashes in section 5.1.1
- Once the proposal document is fully complete and matches the created artifacts, a hash can be created for the proposal file itself. Then all items can be pushed up before the run. The authorization / approval system will fail a run if this isn't done.
- Optional: timestamp the tag externally (OpenTimestamps/RFC3161) for independent dating.

***Avoid circularity***

## Tier Grade Context

This proposal is graded **T3 (Smoke)**. It performs exploratory validation of VDM cosmology predictions against observational data. Supporting prior work:

- **T0 (Concept)**: Cosmology pipeline and causal genesis framework documented in [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md), Appendix D.8 (L7 — Cosmology pipeline)
- **T1 (Proto-model)**: Telegraph-Fisher causality and finite propagation in [Derivation/Metriplectic/](../Derivation/Metriplectic/)
- **T2 (Instrument)**: (Future) FRW continuity meter and CMB meter (referenced in T0 Section 3.4)

This experiment directly supports:
- **M4 (Cosmology continuity)**: Testing whether VDM's diffusive-expansion model produces hemispherical signatures consistent with observations
- **M5 (Emergent gravity weak field)**: Assessing whether VDM-gravity predictions align with large-scale CMB anisotropy without ad-hoc components

## 2. List of Proposers and Associated Institutions/Companies

- **Justin K. Lietz** — Prometheus_VDM (PI, implementer, approver)

## 3. Abstract

Proposed in this document is a T3 smoke test analyzing the hemispherical power asymmetry in Planck PR4 CMB temperature and polarization maps to assess consistency with VDM's causal genesis predictions. The experiment measures two observables: (1) rotation-robustness metric R, quantifying the probability that the observed ~3% hemispherical power difference persists under random sky rotations; and (2) off-diagonal covariance $C_{\ell,\ell+1}$ at low multipoles (ℓ < 100), testing for scale-dependent anisotropy signatures predicted by VDM's diffusive-expansion and hierarchical boundary concentration. Pass gates require R ≥ 3σ above isotropic null, significant $\Delta\ell=1$ couplings after multiple-testing control, and consistency across component-separation methods (SMICA, Commander) and masks. Artifacts include rotation-stability plots, covariance matrices, and cross-method comparison tables, with full provenance locked to Planck PR4 data release manifests.

## 4. Background & Scientific Rationale

**Context and motivation:**

The standard ΛCDM cosmology assumes statistical isotropy of primordial fluctuations, predicting no preferred directions in the CMB. However, Planck PR4 analyses confirm a persistent hemispherical power asymmetry: one half of the sky exhibits ~3% higher temperature fluctuation amplitude than the opposite hemisphere, with a dipole direction near (ℓ, b) ≈ (234°, –14°) in galactic coordinates. This anomaly persists in polarization (though at lower significance) and across component-separation methods, challenging the isotropy assumption.

VDM proposes a causal genesis mechanism via telegraph-Fisher propagation with hierarchical boundary concentration (A8), predicting:
1. **Directional modulation** from finite-speed diffusive expansion at early times
2. **Scale-dependent signatures** strongest at low ℓ (large angular scales) where causal horizon effects dominate
3. **Off-diagonal couplings** $C_{\ell,\ell+1}$ from inhomogeneous transport throttling via void-debt $D_{\text{void}}$

**Why this experiment is necessary:**

The T0 Unification Program requires:
- **M4**: FRW continuity RMS ≤ 1e-6 as a precondition for cosmology claims
- **M5**: Emergent gravity predictions must meet or exceed ΛCDM across CMB/LSS metrics while respecting locality gates, with Hubble tension addressed without ad-hoc components

Without testing VDM predictions against observational data, cosmology claims remain theoretical. This experiment provides:
1. A quantitative benchmark: does VDM's predicted asymmetry amplitude match the observed ~3%?
2. A falsification path: if R collapses under rotations or $C_{\ell,\ell+1}$ couplings are absent, VDM's large-scale causal structure is excluded
3. A systematic check: does the signal persist across component methods and masks, or is it a residual systematic?

**Novel aspects:**

- **Rotation-robustness metric R**: Directly tests whether asymmetry is a fixed sky feature or a statistical fluctuation by computing power asymmetry under N=2000 random rotations
- **Off-diagonal covariance**: Measures adjacent-multipole couplings that standard ΛCDM does not predict but VDM's inhomogeneous transport does
- **Cross-method validation**: Tests SMICA vs. Commander vs. (optionally) SEVEM/NILC to rule out method-specific artifacts

**Target findings requisite for future work:**

Establishing the hemispherical asymmetry as a VDM-consistent feature (or ruling it out) enables:
- **T4 pre-registered experiments**: Full CMB power spectrum fits with VDM corrections
- **T5 pilot studies**: ISW effect and weak lensing under VDM-gravity
- **T6 main results**: Cosmology continuity with anomaly handling and Hubble tension posture

**Criticisms and mitigation:**

- **Criticism**: The asymmetry could be a residual systematic (beam, foreground) rather than cosmological.
  - **Mitigation**: Test across multiple component-separation methods and masks. Require consistency to pass. Null if any method shows no signal.
- **Criticism**: VDM might post-hoc fit the observed amplitude without predictive power.
  - **Mitigation**: VDM's predicted amplitude comes from pre-existing parameters (c, τ, D, β) in the telegraph-Fisher framework. No free parameters are introduced to match the 3% value.
- **Criticism**: Off-diagonal covariance could arise from known systematics (e.g., scanning strategy).
  - **Mitigation**: Compare to PR4-like MC simulations (noise, beams, mask). Require significance after multiple-testing control and calibrate against lensing/birefringence null tests.

**Potential gaps:**

- **Low-ℓ cosmic variance**: Large-scale modes have high variance. Addressed by using PR4's improved τ (reionization) prior and reporting τ-locked and τ-free results.
- **Mask sensitivity**: Galactic plane masks affect low-ℓ modes. Addressed by testing a ladder of masks (conservative to aggressive) and requiring stability.
- **Polarization systematic floor**: EB systematics from beam or birefringence. Addressed by referencing PR4 birefringence analysis and reporting separate TT and EE results.

## 5. Intellectual Merit and Procedure

**Intellectual Merit:**

1. **Importance of scientific questions**: Testing whether the hemispherical asymmetry is a signature of causal genesis addresses a major cosmological anomaly and VDM's predictive power.
2. **Potential broader impacts**: If VDM explains the asymmetry without ad-hoc modifications, it provides a unified framework for CMB anomalies, Hubble tension, and large-scale structure.
3. **Clarity and reasonableness**: The experiment uses publicly available Planck PR4 data, standard tools (healpy, libsharp), and well-defined observables (R-metric, $C_{\ell,\ell+1}$).
4. **Planned level of rigor**: Pre-registered pass/fail gates, cross-method validation, multiple-testing control, and full provenance ensure reproducibility.

### 5.1 Experimental Setup and Diagnostics

**Data:**

- **Planck PR4 FULLSKY** component-separated maps (SMICA, Commander)
- **Masks**: Galactic plane + point source masks from PR4 release
- **Lensing products**: PR4/NPIPE lensing for null checks (optional)
- **Reionization prior**: PR4 τ constraint (April 2025 analysis) for low-ℓ calibration

**Tools:**

- **healpy**: SHT via `map2alm`, `anafast`, `alm2map`, `rotator`
- **libsharp**: Fast C99 SHT with MPI (for large-scale transforms)
- **Python**: NumPy, SciPy, Matplotlib for analysis and plotting

**Parameters and defaults:**

- **Multipole range**: ℓ_max ∈ {100, 200, 600} (focus on ℓ < 100 for asymmetry, ℓ < 600 for $C_{\ell,\ell+1}$)
- **Rotations**: N_rot = 2000 random SO(3) rotations for R-metric
- **Masks**: Test conservative (Galactic latitude |b| > 30°) and aggressive (|b| > 10°) cuts
- **Component methods**: SMICA (primary), Commander (secondary), SEVEM/NILC (optional)
- **ε tolerance**: ε = 0.1 (for R-metric; probability |A_i - A_0| ≤ ε A_0)

**Diagnostics required (per run):**

1. **Baseline asymmetry amplitude $A_0$**: Local-variance dipole or power-split $C_\ell$ estimator on masked map
2. **Rotation-robustness R**: $R = \Pr(|A_i - A_0| \leq \epsilon A_0)$ over N_rot random rotations
3. **Off-diagonal covariance**: $K_{\ell}^{(\Delta\ell=1)} = \sum_m a_{\ell m} a^*_{\ell+1,m}$ (and EB/TE variants if desired)
4. **Significance**: Calibrate R and $K_{\ell}$ against PR4-like MC simulations (isotropic null)
5. **Cross-method consistency**: Require R ≥ 3σ and significant $K_{\ell}$ in both SMICA and Commander
6. **Mask stability**: Require signal persistence across mask ladder

**Minimum artifacts per run:**

- 1 PNG: Rotation-robustness curve (x-axis = ε, y-axis = R, with isotropic null band)
- 1 PNG: Off-diagonal covariance matrix (heatmap of $C_{\ell,\ell'}$ for ℓ, ℓ' < 100)
- 1 PNG: Cross-method comparison (barplot of R and $K_{\ell}$ significance for SMICA vs. Commander)
- 1 CSV: columns `method, mask, ell_max, A0, R_epsilon_0p1, K_ell_avg, significance_R, significance_K, pass_fail`
- 1 JSON: full provenance (commit, tag, data manifests, seeds, parameters, gates)

**Equipment/tools required:**

- Planck PR4 data files (downloaded and checksummed)
- Python environment with healpy, libsharp (via healpy or direct C interface), NumPy, SciPy, Matplotlib
- io_paths.py helper for artifact routing
- MC simulation suite (isotropic, matched to PR4 noise/beam/mask)

### 5.1.1 Pre-Run Config Requirements

**Required config and metadata:**

- **Derivation/code/physics/cosmology/APPROVAL.json**
- **Derivation/code/physics/cosmology/schemas/cmb_hemi_asym.schema.json**
- **Derivation/code/physics/cosmology/specs/cmb_hemi_asym.v1.json**

#### APPROVALS.json

```json
{
  "preflight_name": "cmb_hemi_asym_preflight",
  "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at PROPOSALS/ with explicit review."
},
{
  "pre_registered": true,
  "proposal": "PROPOSALS/T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md",
  "allowed_tags": [
    "cmb_hemi_asym-v1"
  ],
  "schema_dir": "Derivation/code/physics/cosmology/schemas",
  "approvals": {
    "cmb_hemi_asym-v1": {
      "schema": "Derivation/code/physics/cosmology/schemas/cmb_hemi_asym.schema.json",
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
  "proposal_title": "CMB Hemispherical Power Asymmetry as VDM Causal Genesis Witness",
  "tier_grade": "T3",
  "commit": "{git rev-parse HEAD}",
  "salted_provenance": "SHA256(commit || salt_hex)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Rotation-robustness R at epsilon=0.1 >= 3 sigma above isotropic null", "direction": "increase" },
    { "id": "H2", "statement": "Significant off-diagonal covariance K_ell at ell < 100 after multiple-testing control", "direction": "increase" },
    { "id": "H3", "statement": "Cross-method consistency: R and K_ell significance in both SMICA and Commander", "direction": "no-change" },
    { "id": "H4", "statement": "Mask stability: signal persists across conservative and aggressive masks", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["component_method", "mask_type", "ell_max", "epsilon", "N_rot"],
    "dependent": ["A0", "R", "K_ell", "significance_R", "significance_K"],
    "controls": ["tau_prior", "MC_simulations"]
  },
  "pass_fail": [
    { "metric": "R_epsilon_0p1_sigma", "operator": ">=", "threshold": 3.0, "unit": "sigma" },
    { "metric": "K_ell_significance", "operator": ">=", "threshold": 3.0, "unit": "sigma" },
    { "metric": "cross_method_consistency", "operator": "==", "threshold": 1, "unit": "bool" },
    { "metric": "mask_stability", "operator": "==", "threshold": 1, "unit": "bool" }
  ],
  "spec_refs": [
    "Derivation/code/physics/cosmology/specs/cmb_hemi_asym.v1.json"
  ],
  "registration_timestamp": "2025-11-05T00:00:00Z"
}
```

#### Specs

```json
{
  "run_name": "cmb_hemi_asym",
  "version": "1.0.0",
  "tag": "cmb_hemi_asym-v1",
  "schema_ref": "Derivation/code/physics/cosmology/schemas/cmb_hemi_asym.schema.json",
  "parameters": {
    "data_release": "Planck_PR4_FULLSKY",
    "component_methods": ["SMICA", "Commander"],
    "ell_max": [100, 200, 600],
    "N_rot": 2000,
    "epsilon": 0.1,
    "masks": ["conservative_b30", "aggressive_b10"],
    "tau_prior": "PR4_reionization_Apr2025",
    "MC_sims": 1000
  },
  "data_manifests": [
    "Planck_PR4_SMICA_temperature_Nside2048.fits",
    "Planck_PR4_Commander_temperature_Nside2048.fits",
    "Planck_PR4_mask_conservative.fits",
    "Planck_PR4_mask_aggressive.fits"
  ]
}
```

#### Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "cmb_hemi_asym.schema.json",
  "title": "CMB Hemispherical Asymmetry Test v1",
  "type": "object",
  "properties": {
    "run_name": { "type": "string" },
    "version": { "type": "string" },
    "tag": { "type": "string" },
    "schema_ref": { "type": "string" },
    "parameters": {
      "type": "object",
      "properties": {
        "data_release": { "type": "string" },
        "component_methods": { "type": "array", "items": { "type": "string" } },
        "ell_max": { "type": "array", "items": { "type": "integer" } },
        "N_rot": { "type": "integer" },
        "epsilon": { "type": "number" },
        "masks": { "type": "array", "items": { "type": "string" } },
        "tau_prior": { "type": "string" },
        "MC_sims": { "type": "integer" }
      },
      "required": ["data_release", "component_methods", "ell_max", "N_rot"]
    },
    "data_manifests": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["run_name", "version", "tag", "schema_ref", "parameters", "data_manifests"]
}
```

### 5.2 Experimental Runplan

**Cartesian product of independent variables:**

- Component method: {SMICA, Commander}
- Mask: {conservative (|b| > 30°), aggressive (|b| > 10°)}
- ℓ_max: {100, 200, 600}
- Observables: {R-metric at ε=0.1, $K_{\ell}^{(\Delta\ell=1)}$ for ℓ < 100}

Total conditions: ~12 runs (2 methods × 2 masks × 3 ℓ_max, not all combinations necessary)

**Estimated runtime:**

- Per method/mask/ℓ_max: 10-30 minutes (SHT + rotations + MC comparison)
- Total compute budget: ~4-8 hours (serial), ~1-2 hours (parallel)

**Success actions:**

1. Publish RESULTS_CMB_Hemispherical_Asymmetry_v1.md with gate matrix (all pass)
2. Archive figures (rotation-robustness, covariance matrix, cross-method comparison), CSV tables, JSON logs
3. Update [Derivation/Cosmology/](../Derivation/Cosmology/) with validated VDM signature
4. Tag commit with signed, dated provenance

**Failure actions:**

1. Route failed runs to `Derivation/code/outputs/failed_runs/cmb_hemi_asym_YYYYMMDD/`
2. Emit contradiction report JSON with exact gate failures
3. Document which gates failed (R < 3σ, no $K_{\ell}$ significance, method inconsistency, mask instability)
4. Assess whether VDM predictions need revision or observational systematics dominate
5. Re-run with refined masks/priors if systematic floor is suspected

**Result publication plan:**

- **Format**: Follow [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
- **Sections**: Abstract, Background, Methods (data + analysis), Results (R-metric, $C_{\ell,\ell+1}$, cross-method), Discussion, Provenance
- **Numeric captions**: All figures include exact gate thresholds, significance levels, pass/fail status
- **CSV/JSON sidecars**: Deposited alongside figures in `Derivation/code/outputs/logs/cosmology/cmb_hemi_asym/`

## 6. Personnel

**Proposer: Justin K. Lietz**

- **Role**: PI, implementer, approver
- **Responsibilities**:
  - Download and checksum Planck PR4 data
  - Implement R-metric and $C_{\ell,\ell+1}$ analysis pipeline
  - Pre-register hypotheses and gates in PRE-REGISTRATION.json
  - Execute validation runs across methods, masks, and ℓ_max
  - Analyze results and publish RESULTS_CMB_Hemispherical_Asymmetry_v1.md
  - Enforce artifact policy and provenance discipline
  - Review and approve schema/spec files before execution

## 7. References

**Canon and gates:**

- [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md)
- [Derivation/EQUATIONS.md](../Derivation/EQUATIONS.md)
- [Derivation/UNITS_NORMALIZATION.md](../Derivation/UNITS_NORMALIZATION.md)

**T0 Unification Program:**

- [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md)

**Cosmology:**

- [Derivation/Cosmology/](../Derivation/Cosmology/)

**Daily-Pulse source notes:**

- [Daily-Pulse/2025-11-04/CMB-Asymmetry-as-a-Causal-Anchor.md](../Daily-Pulse/2025-11-04/CMB-Asymmetry-as-a-Causal-Anchor.md)
- [Daily-Pulse/2025-11-04/T3_T4_Off-Diagonal-CMB-Test.md](../Daily-Pulse/2025-11-04/T3_T4_Off-Diagonal-CMB-Test.md)
- [Daily-Pulse/2025-10-31/testing-vdm-diffusive-cosmology.md](../Daily-Pulse/2025-10-31/testing-vdm-diffusive-cosmology.md)

**External data and tools:**

- Planck PR4 FULLSKY: https://data.cmb-s4.org/planck_pr4-fullsky.html
- healpy documentation: https://healpy.readthedocs.io/
- libsharp: arXiv:1303.4945

**Policy:**

- [Derivation/code/common/authorization/README.md](../Derivation/code/common/authorization/README.md)

**Result standards:**

- [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---

> End of proposal. Upon approval, generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at the listed paths and create a signed prereg tag before execution.
