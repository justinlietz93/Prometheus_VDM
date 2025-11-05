# PROPOSALS Directory

This directory contains formal whitepaper-grade proposal documents extracted from Daily-Pulse notes and designed to support the T0 Unification Program formalization process.

## Purpose

Proposals in this directory represent structured, machine-actionable experimental and theoretical programs that:
1. Address specific targets (M1-M6) in the T0 Unification Program
2. Follow the canonical PROPOSAL_PAPER_TEMPLATE.md structure
3. Include pre-registration, schemas, specs, and provenance requirements
4. Define explicit pass/fail gates and falsifiable predictions

## Proposal Listing

### T2 (Instrument) Proposals

| Proposal | Target | Description |
|----------|--------|-------------|
| [T2_PROPOSAL_CEG_Metric_Definition_v1.md](./T2_PROPOSAL_CEG_Metric_Definition_v1.md) | M2, M6 | Corrective Echo Gain (CEG) metric: dimensionless measure of model-aware correction efficacy in echo/rewind protocols |

### T3 (Smoke Test) Proposals

| Proposal | Target | Description |
|----------|--------|-------------|
| [T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md](./T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md) | M6, M6.9 | Agency as entropy-echo measurement via void-walker self-information flux: dimensionless agency index $\mathcal{A} = E_{\text{echo}} / R_{\text{VW}}$ |
| [T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md](./T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md) | M4, M5 | CMB hemispherical power asymmetry as VDM causal genesis witness: rotation-robustness R-metric and off-diagonal covariance $C_{\ell,\ell+1}$ |

### T4 (Preregistered) Proposals

| Proposal | Target | Description |
|----------|--------|-------------|
| [T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md](./T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md) | M1 | Cold-atom test of VDM causal cone in metriplectic optical lattice: front velocity $v_{\text{VDM}}$ and width broadening β measurements |

## T0 Unification Program Target Mapping

### M1 — Local causality and finite propagation
- **Proposals**: [T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md](./T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md)
- **Gates**: KG J-only dispersion fit $R^2 \geq 0.999$; light-cone speed $v \leq c(1+0.02)$

### M2 — Metriplectic Lyapunov monotonicity
- **Proposals**: [T2_PROPOSAL_CEG_Metric_Definition_v1.md](./T2_PROPOSAL_CEG_Metric_Definition_v1.md)
- **Gates**: $\Delta L_h \leq 0$ per step; identity residuals $\leq 1\text{e-}12$; two-grid slope $\geq 2.90$

### M4 — Cosmology continuity
- **Proposals**: [T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md](./T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md)
- **Gates**: FRW continuity RMS $\leq 1\text{e-}6$

### M5 — Emergent gravity (weak field consistency)
- **Proposals**: [T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md](./T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md)
- **Gates**: Model selection (AIC/BIC) meets or exceeds baseline without LIV

### M6 — Measurement as epistemic projection
- **Proposals**: [T2_PROPOSAL_CEG_Metric_Definition_v1.md](./T2_PROPOSAL_CEG_Metric_Definition_v1.md), [T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md](./T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md)
- **Gates**: KL divergence $\leq 1\text{e-}3$ for Born-rule meters; reversibility $\leq 1\text{e-}10$; Noether drifts $\leq 1\text{e-}12$

### M6.9 — Agency Field witness reproducibility
- **Proposals**: [T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md](./T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md)
- **Gates**: Dispersion and reversibility gates hold in J-only meters

## Source Material

All proposals in this directory were derived from insights and experimental designs documented in the [Daily-Pulse](../Daily-Pulse/) directory, specifically:

- **CEG Metric**: [Daily-Pulse/2025-10-30/define-the-CEG.md](../Daily-Pulse/2025-10-30/define-the-CEG.md)
- **Agency Entropy-Echo**: [Daily-Pulse/2025-11-04/Quantifying-Agency-as-Entropy-Echo.md](../Daily-Pulse/2025-11-04/Quantifying-Agency-as-Entropy-Echo.md), [Daily-Pulse/2025-10-31/measuring-agency-through-entropy-echoes.md](../Daily-Pulse/2025-10-31/measuring-agency-through-entropy-echoes.md)
- **CMB Hemispherical Asymmetry**: [Daily-Pulse/2025-11-04/CMB-Asymmetry-as-a-Causal-Anchor.md](../Daily-Pulse/2025-11-04/CMB-Asymmetry-as-a-Causal-Anchor.md), [Daily-Pulse/2025-11-04/T3_T4_Off-Diagonal-CMB-Test.md](../Daily-Pulse/2025-11-04/T3_T4_Off-Diagonal-CMB-Test.md), [Daily-Pulse/2025-10-31/testing-vdm-diffusive-cosmology.md](../Daily-Pulse/2025-10-31/testing-vdm-diffusive-cosmology.md)
- **Cold-Atom Causal Cone**: [Daily-Pulse/2025-10-31/cold-atom-test-of-the-vdm-causal-cone.md](../Daily-Pulse/2025-10-31/cold-atom-test-of-the-vdm-causal-cone.md)

## Canon and Template References

All proposals follow:
- **Template**: [Derivation/Templates/PROPOSAL_PAPER_TEMPLATE.md](../Derivation/Templates/PROPOSAL_PAPER_TEMPLATE.md)
- **T0 Unification Program**: [Derivation/Unification/T0_Unification_Program_Spec_v1.md](../Derivation/Unification/T0_Unification_Program_Spec_v1.md)
- **Canon registries**: [Derivation/SYMBOLS.md](../Derivation/SYMBOLS.md), [Derivation/EQUATIONS.md](../Derivation/EQUATIONS.md), [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md), [Derivation/UNITS_NORMALIZATION.md](../Derivation/UNITS_NORMALIZATION.md), [Derivation/ALGORITHMS.md](../Derivation/ALGORITHMS.md)

## Approval and Authorization

Before executing any proposed experiment:
1. Generate APPROVAL.json, PRE-REGISTRATION.json, schema, and spec files at paths specified in each proposal
2. Create signed, dated provenance tag per proposal Section 5.1.1
3. Review and approve per [Derivation/code/common/authorization/README.md](../Derivation/code/common/authorization/README.md)
4. Commit all config files and push tag before artifact-writing runs

## Result Standards

Upon completion, results must follow:
- **Standards**: [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
- **Artifact routing**: Via [Derivation/code/common/io_paths.py](../Derivation/code/common/io_paths.py)
- **Minimum artifacts**: 1 PNG figure + 1 CSV log + 1 JSON provenance per run
- **Provenance**: Full commit, tag, seed, and gate pass/fail documentation

## Additional Proposal Ideas from Daily-Pulse

The following Daily-Pulse notes contain additional experimental ideas that could be formalized into future proposals:

1. **Rayleigh-Bénard as Quantitative Gate** ([Daily-Pulse/2025-10-29/rayleigh-benard-as-a-quantitative-gate.md](../Daily-Pulse/2025-10-29/rayleigh-benard-as-a-quantitative-gate.md)) - Maps to M3 (RD phenomenology)
2. **Quantum Echo to VDM Agency Field Mapping** ([Daily-Pulse/2025-11-04/Quantum-Echoes-Meet-Causal-Cones.md](../Daily-Pulse/2025-11-04/Quantum-Echoes-Meet-Causal-Cones.md)) - Maps to M6 (Born-rule frequencies)
3. **Self-Model Efficacy Index (SMEI)** ([Daily-Pulse/2025-10-30/self-model-efficacy-index.md](../Daily-Pulse/2025-10-30/self-model-efficacy-index.md)) - Energy-normalized performance metric
4. **VDM vs. Classical RD Benchmark** ([Daily-Pulse/2025-10-30/benchmark-vdm-against-classical-systems.md](../Daily-Pulse/2025-10-30/benchmark-vdm-against-classical-systems.md)) - Falsifiable differentiator tests
5. **Multi-Tier Falsifier for Causal Coherence** ([Daily-Pulse/2025-10-31/multi-tier-falsifier-for-causal-coherence.md](../Daily-Pulse/2025-10-31/multi-tier-falsifier-for-causal-coherence.md)) - Causal constraint validator toolkit

These may be formalized into additional proposals as the T0 Unification Program progresses through the maturity ladder (T0→T9).

---

**Created**: 2025-11-05  
**Maintainer**: Justin K. Lietz  
**License**: See [LICENSE](../LICENSE)
