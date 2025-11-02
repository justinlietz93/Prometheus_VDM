# Prometheus_VDM — Asset Index (Proposals, RESULTS, Runners, Instruments, Runtime)

Purpose
- A living, single-page index of major assets in this repository:
  - PROPOSALS (with commit-pinned permalinks)
  - RESULTS (artifacted, with PASS/FAIL summaries)
  - RUNNERS (scripts/CLIs)
  - INSTRUMENTS (meters/diagnostics)
  - Runtime boundary stack (fum_rt)
- Update this file whenever you add a PROPOSAL_*, RESULTS_*, or new runner/meter.

Status keys
- [Present] in repo now
- [Planned] stub or pending implementation
- [Add link] add exact path and, if appropriate, a commit-pinned permalink

Last updated: 2025‑11‑02 (UTC) — Comprehensive repository audit completed

---

## 0) Canon & Core References

- Axioms (A0–A7) — [Present]  
  [AXIOMS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/AXIOMS.md)
- Equations & Instruments — [Present]  
  [EQUATIONS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/EQUATIONS.md)
- Validation Metrics — [Present]  
  [VALIDATION_METRICS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/VALIDATION_METRICS.md)
- Units/Normalization — [Present]  
  [UNITS_NORMALIZATION.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/UNITS_NORMALIZATION.md)
- Schemas (Observation etc.) — [Present]  
  [SCHEMAS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/SCHEMAS.md)
- Algorithms — [Present]  
  [ALGORITHMS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/ALGORITHMS.md)
- Canon Map — [Present]  
  [CANON_MAP.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/CANON_MAP.md)
- Data Products — [Present]  
  [DATA_PRODUCTS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/DATA_PRODUCTS.md)
- Constants — [Present]  
  [CONSTANTS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/CONSTANTS.md)
- Symbols — [Present]  
  [SYMBOLS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/SYMBOLS.md)
- Naming Conventions — [Present]  
  [NAMING_CONVENTIONS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/NAMING_CONVENTIONS.md)
- BC/IC Geometry — [Present]  
  [BC_IC_GEOMETRY.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/BC_IC_GEOMETRY.md)
- Roadmap — [Present]  
  [ROADMAP.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/ROADMAP.md)
- Open Questions — [Present]  
  [OPEN_QUESTIONS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/OPEN_QUESTIONS.md)

---

## 1) PROPOSALS (commit‑pinned where available)

### A8 (Axiom Candidate)
- T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md

### Echo / Causality (Quantum Echos)
- T0_PROPOSAL_SIE_Willow-Convergence_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Echos/T0_PROPOSAL_SIE_Willow-Convergence_v1.md
- T1_PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Echos/T1_PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md
- T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md
- T4_PROPOSAL_SMAE_CEG_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_SMAE_CEG_v1.md
- T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md

### Foundations / Measurement / Quantum Engines
- T0_PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/T0_PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md
- T1_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence__ProtoModel_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/T1_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence__ProtoModel_v1.md
- T2_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence_Instrument_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/T2_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence_Instrument_v1.md
- T4_PROPOSAL_J-to_Dirac_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/T4_PROPOSAL_J-to_Dirac_v1.md
- T4_PROPOSAL_Quantum-Resource-Engine_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Engine/T4_PROPOSAL_Quantum-Resource-Engine_v1.md

### Metriplectic / Structure
- PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md
- PROPOSAL_Metriplectic_Lindblad_T4.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/PROPOSAL_Metriplectic_Lindblad_T4.md
- PROPOSAL_Metriplectic_SymplecticPlusDG.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md
- PROPOSAL_KG_plus_RD_Metriplectic.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_KG_plus_RD_Metriplectic.md
- PROPOSAL_Metriplectic_JMJ_RD_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_Metriplectic_JMJ_RD_v1.md
- T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md

### Dark Matter / GR Spine
- T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Dark_Matter/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md

### Cosmology
- PROPOSAL_FRW_Balance_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/PROPOSAL_FRW_Balance_v1.md
- PROPOSAL_FRW_Continuity_Predictive_v2.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/PROPOSAL_FRW_Continuity_Predictive_v2.md
- T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md

### Dark Photons
- PROPOSAL_Decoherence_Portals.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Dark_Photons/PROPOSAL_Decoherence_Portals.md

### Agency Field
- PROPOSAL_ADC_Response_Slope_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Agency_Field/PROPOSAL_ADC_Response_Slope_v1.md
- PROPOSAL_Agency_Curvature_Scaling_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md
- PROPOSAL_Agency_Stability_Band_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Agency_Field/PROPOSAL_Agency_Stability_Band_v1.md
- PROPOSAL_Multipartite_Coordinaton_Depth_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Agency_Field/Coordination_Depth/PROPOSAL_Multipartite_Coordinaton_Depth_v1.md
- PROPOSAL_Agency_Witness_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Agency_Field/Witness/PROPOSAL_Agency_Witness_v1.md

### Causality
- PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Causality/PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md
- PROPOSAL_Metriplectic_Causal_Dominance_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md

### Collapse
- PROPOSAL_A6_Collapse_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Collapse/PROPOSAL_A6_Collapse_v1.md

### Conservation Law
- PROPOSAL_RD_Discrete_Conservation_vs_Balance.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md

### Information
- PROPOSAL_SIE_Invariant_and_Novelty_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Information/PROPOSAL_SIE_Invariant_and_Novelty_v1.md

### Intelligence Model
- PROPOSAL_Physics_Native_Intelligence_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md

### Qualia
- PROPOSAL_T3_Calibration_of_Psychophysical_Observables_to_C_Field.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Qualia/PROPOSAL_T3_Calibration_of_Psychophysical_Observables_to_C_Field.md
- PROPOSAL_vdm_qualia_program.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Qualia/PROPOSAL_vdm_qualia_program.md

### Quantum Gravity
- PROPOSAL_Dark_Photon_Bridge.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum_Gravity/PROPOSAL_Dark_Photon_Bridge.md
- PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum_Gravity/PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md
- T2_PROPOSAL_QG_Regge_CDT_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum_Gravity/T2_PROPOSAL_QG_Regge_CDT_v1.md

### Tachyon Condensation
- PROPOSAL_Tachyonic_Tube_Condensation.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Tachyon_Condensation/PROPOSAL_Tachyonic_Tube_Condensation.md

### Thermodynamic Routing
- PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md
- PROPOSAL_Flux_Through_Memory_Channels_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Flux_Through_Memory_Channels_v1.md
- PROPOSAL_Passive_Thermodynamic_Routing_v2.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md
- PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Prereg_Biased_Main/PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md
- PROPOSAL_Wave_Flux_Meter_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md
- PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md
- PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md

### Topology
- PROPOSAL_Loop_Quench_Test_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Topology/PROPOSAL_Loop_Quench_Test_v1.md
- PROPOSAL_Loop_Quench_Test_Robustness_v2.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Topology/PROPOSAL_Loop_Quench_Test_Robustness_v2.md

---

## 2) RESULTS (artifacted instruments and studies)

### Metriplectic / KG Structure
- RESULTS_KG_Noether_Invariants_v1.md — [Present] | PASS — Energy drift ≈8.33×10⁻¹⁷, Momentum drift ≈2.60×10⁻¹⁷ | Artifacts: 20251008_184547_kg_noether_energy_momentum__KG-noether-v1.{png,csv,json}  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md

- RESULTS_KG_Energy_Oscillation_v1.md — [Present] | KG energy oscillation validation | Artifacts in metriplectic/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/KG_Energy_Oscillation/RESULTS_KG_Energy_Oscillation_v1.md

- RESULTS_KG_Jonly_Locality_and_Dispersion.md — [Present] | J-only KG dispersion relation validation | Artifacts in metriplectic/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md

- RESULTS_KG_RD_Metriplectic.md — [Present] | KG⊕RD composition via metriplectic framework | Artifacts in metriplectic/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/KG_RD_Metriplectic/RESULTS_KG_RD_Metriplectic.md

- RESULTS_Metriplectic_JMJ_RD_v1.md — [Present] | JMJ Strang composition for RD | Artifacts in metriplectic/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md

- RESULTS_Metriplectic_Structure_Checks.md — [Present] | Degeneracy residuals g₁,g₂ structure validation | Artifacts in metriplectic/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md

### Reaction-Diffusion
- RESULTS_RD_Discrete_Conservation_vs_Balance.md — [Present] | PASS — Euler β≈2, Strang/DG β≈3, DG satisfies H-theorem | Artifacts: 20251006_072251_fixed_dt_deltaS_compare.{png,csv,json} in rd_conservation/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Conservation_Law/RESULTS_RD_Discrete_Conservation_vs_Balance.md

### Cosmology / FRW
- RESULTS_FRW_Continuity_Residual_Quality_Check.md — [Present] | PASS — RMS_FRW ≈9.04×10⁻¹⁶ ≪ 10⁻⁶ gate | Artifacts: 20251006_175329_frw_continuity_residual__FRW-balance-v1.{png,csv,json}  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md

### Tachyon Condensation
- RESULTS_Tachyonic_Tube_v1.md — [Present] | Tachyonic tube spectrum analysis | Artifacts in tachyonic_condensation/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md

### Collapse / A6
- RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md — [Present] | A6 collapse scaling and junction behavior | Artifacts in collapse/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Collapse/RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md

### Dark Photons
- RESULTS_Decoherence_Portals.md — [Present] | Dark photon decoherence portal analysis | Artifacts: 20251006_180711_fisher_check__DP-fisher-smoke.{csv,json} in dark_photons/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Dark_Photons/RESULTS_Decoherence_Portals.md

### Intelligence Model
- RESULTS_Physics_Native_Intelligence_Substrate_v1.md — [Present] | Physics-native intelligence substrate validation | Artifacts in intelligence_model/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Intelligence_Model/RESULTS_Physics_Native_Intelligence_Substrate_v1.md

### Thermodynamic Routing
- RESULTS_Passive_Thermodynamic_Routing_v2.md — [Present] | Passive routing flux validation | Artifacts in thermo_routing/passive_thermo_routing/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/RESULTS_Passive_Thermodynamic_Routing_v2.md

- RESULTS_Wave_Flux_Meter_A_Phase_v1.md — [Present] | Wave flux meter Phase A results | Artifacts in thermo_routing/wave_flux_meter/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md

- RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md — [Present] | Wave flux meter Phase B (open ports) | Artifacts in thermo_routing/wave_flux_meter/  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md

---

## 3) RUNNERS (scripts/CLIs)

### Metriplectic
- run_metriplectic.py — [Present]  
  Purpose: Main metriplectic composition runner (KG⊕RD, echo experiments)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/run_metriplectic.py

- run_kg_rd_metriplectic.py — [Present]  
  Purpose: KG+RD metriplectic composition experiments  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/run_kg_rd_metriplectic.py

- run_kg_dispersion.py — [Present]  
  Purpose: Klein-Gordon dispersion relation validation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/run_kg_dispersion.py

- run_kg_energy_oscillation.py — [Present]  
  Purpose: KG energy oscillation tests  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/run_kg_energy_oscillation.py

- run_kg_light_cone.py — [Present]  
  Purpose: KG light cone structure validation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/run_kg_light_cone.py

### Reaction-Diffusion / Conservation
- run_rd_conservation.py — [Present]  
  Purpose: RD discrete conservation vs balance tests  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/rd_conservation/run_rd_conservation.py

### Cosmology
- run_frw_balance.py — [Present]  
  Purpose: FRW continuity residual quality check  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/cosmology/run_frw_balance.py

### Tachyon Condensation
- run_tachyon_tube.py — [Present]  
  Purpose: Tachyonic tube condensation experiments  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py

### Collapse / A6
- run_a6_collapse.py — [Present]  
  Purpose: A6 collapse scaling experiments  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/collapse/run_a6_collapse.py

### Dark Photons
- run_dp_fisher_check.py — [Present]  
  Purpose: Dark photon Fisher information check  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/dark_photons/run_dp_fisher_check.py

- run_dp_noise_budget.py — [Present]  
  Purpose: Dark photon noise budget analysis  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/dark_photons/run_dp_noise_budget.py

### Quantum
- run_vdm_triad_prereg.py — [Present]  
  Purpose: VDM triad pre-registration experiments  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/quantum/run_vdm_triad_prereg.py

### Causality
- run_causality_dag_audit.py — [Present]  
  Purpose: Causal DAG audit validation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/causality/run_causality_dag_audit.py

### Thermodynamic Routing
- run_thermo_routing.py — [Present]  
  Purpose: Main thermodynamic routing experiments  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/run_thermo_routing.py

- run_tr_v2_prereg_biased.py — [Present]  
  Purpose: Thermodynamic routing v2 pre-registered biased  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/run_tr_v2_prereg_biased.py

- run_tr_v2_prereg_biased_main.py — [Present]  
  Purpose: TR v2 pre-registered biased main  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/run_tr_v2_prereg_biased_main.py

- run_tr_v2_prereg_biased_main_full.py — [Present]  
  Purpose: TR v2 pre-registered biased main (full sweep)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/run_tr_v2_prereg_biased_main_full.py

- run_tr_v2_prereg_biased_main_aggregate.py — [Present]  
  Purpose: TR v2 pre-registered biased main (aggregation)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/run_tr_v2_prereg_biased_main_aggregate.py

- run_ftmc_v1.py — [Present]  
  Purpose: Flux Through Memory Channels v1  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/passive_thermo_routing/run_ftmc_v1.py

- run_wave_flux_meter_v1.py — [Present]  
  Purpose: Wave flux meter Phase A  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/wave_flux_meter/run_wave_flux_meter_v1.py

- run_wave_flux_meter_openports_v1.py — [Present]  
  Purpose: Wave flux meter open ports version  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/thermo_routing/wave_flux_meter/run_wave_flux_meter_openports_v1.py

---

## 4) INSTRUMENTS / METERS (code modules or notebooks)

### Core Metriplectic Instruments
- kg_noether.py — [Present]  
  Purpose: KG Noether invariants (energy & momentum conservation meters)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/kg_noether.py

- metriplectic_structure_checks.py — [Present]  
  Purpose: Metriplectic degeneracy residuals (g₁,g₂) validation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/metriplectic_structure_checks.py

- kg_ops.py — [Present]  
  Purpose: Klein-Gordon operators (Hamiltonian, evolution)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/kg_ops.py

- j_step.py — [Present]  
  Purpose: J-branch (symplectic) stepping for metriplectic composition  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/j_step.py

- compose.py — [Present]  
  Purpose: Metriplectic composition operators (JMJ Strang)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/compose.py

- echo_metrics.py — [Present]  
  Purpose: Echo quality metrics for CEG experiments  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/echo_metrics.py

- echo_gates.py — [Present]  
  Purpose: Echo gate validation functions  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/echo_gates.py

- assisted_echo.py — [Present]  
  Purpose: Self-model-assisted echo (SMAE) instrumentation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/metriplectic/assisted_echo.py

### Reaction-Diffusion Meters
- rd_dispersion_experiment.py — [Present]  
  Purpose: RD dispersion relation meter (σ(k)=r−Dk²)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py

- rd_front_speed_experiment.py — [Present]  
  Purpose: RD front speed meter (2√Dr validation)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py

- rd_front_speed_sweep.py — [Present]  
  Purpose: RD front speed parameter sweep  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/rd_front_speed_sweep.py

- discrete_gradient.py — [Present]  
  Purpose: Discrete gradient (H-theorem) meter for RD  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/discrete_gradient.py

- flux_core.py — [Present]  
  Purpose: Flux computation core for RD systems  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/flux_core.py

- census_clocks.py — [Present]  
  Purpose: Census clock tracking for RD fronts  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/census_clocks.py

- reaction_exact.py — [Present]  
  Purpose: Exact reaction solver (logistic, Fisher-KPP)  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/reaction_diffusion/reaction_exact.py

### Tachyon Condensation Instruments
- condense_tube.py — [Present]  
  Purpose: Tachyonic tube condensation core  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/tachyonic_condensation/condense_tube.py

- cylinder_modes.py — [Present]  
  Purpose: Cylindrical mode decomposition for tachyon tubes  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/tachyonic_condensation/cylinder_modes.py

### Memory Steering Instruments
- memory_steering.py — [Present]  
  Purpose: Memory steering core implementation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/memory_steering/memory_steering.py

- memory_steering_experiments.py — [Present]  
  Purpose: Memory steering experimental suite  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/memory_steering/memory_steering_experiments.py

- memory_steering_acceptance.py — [Present]  
  Purpose: Memory steering acceptance gates  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/memory_steering/memory_steering_acceptance.py

### Fluid Dynamics (Benchmarks)
- taylor_green_benchmark.py — [Present]  
  Purpose: Taylor-Green vortex benchmark  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py

- lid_cavity_benchmark.py — [Present]  
  Purpose: Lid-driven cavity benchmark  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py

- lbm2d.py — [Present]  
  Purpose: 2D Lattice Boltzmann method implementation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py

### Conservation Law Validators
- qfum_validate.py — [Present]  
  Purpose: QFUM (quantum flux unit measure) validation  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/conservation_law/qfum_validate.py

### Axiom Verification
- verify_discrete_EL.py — [Present]  
  Purpose: Discrete Euler-Lagrange equation verification  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/axioms/verify_discrete_EL.py

### Agency Field Instruments
- simulate_options_probe.py — [Present]  
  Purpose: Options probe simulation for agency field  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/agency/simulate_options_probe.py

### Planned / Conceptual (not yet implemented)
- κ‑collapse validator — [Planned]
- Cone‑slack meter (telegraph/causality) — [Planned]
- A8 hierarchy meters: boundary detector (physics bench), depth N(L), α, α_I, β_E — [Planned]
- Minkowski morphometry & deconvolution — [Planned]

---

## 5) A8 Program (Hierarchy, Area‑law, Information)

- Proposal: T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md
- DOI: https://doi.org/10.5281/zenodo.17503344
- Physics‑bench meters (boundary → Γ, N(L), α, α_I, β_E) — [Planned]
- Cross‑grid/ε invariance and morphometry/deconvolution — [Planned]
- RESULTS_A8_* (G1–G12) — [Missing] — No gate runs executed yet
- Status: 0/12 gates executed

---

## 6) Causality Program (Telegraph–Fisher)

### Proposals
- Echo-Limited Causality (T4) — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md
- PROPOSAL_Metriplectic_Causal_Dominance_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md
- PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Causality/PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md

### Instruments & Runners
- run_causality_dag_audit.py — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/causality/run_causality_dag_audit.py
- Stepper + meters (cone‑slack, κ‑collapse) — [Planned]
- RESULTS_Telegraph_Fisher_* — [Missing]

---

## 7) Cosmology Spine

### Canon References
- Units/FRW QC — [Present]  
  [UNITS_NORMALIZATION.md](https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/UNITS_NORMALIZATION.md)

### Proposals
- PROPOSAL_FRW_Balance_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/PROPOSAL_FRW_Balance_v1.md
- PROPOSAL_FRW_Continuity_Predictive_v2.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/PROPOSAL_FRW_Continuity_Predictive_v2.md
- T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md

### Results & Runners
- RESULTS_FRW_Continuity_Residual_Quality_Check.md — [Present] | PASS  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md
- run_frw_balance.py — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/Derivation/code/physics/cosmology/run_frw_balance.py

### Planned Components
- Primordial P(k) generator — [Planned]
- Evolution interface (CLASS/CAMB style) — [Planned]
- Additional RESULTS_Cosmology_* — [Planned]

---

## 8) Runtime Boundary Detection (fum_rt stack)

- Event schema (boundary_probe; cut_strength) — [Present]  
  fum_rt/core/announce.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/fum_rt/core/announce.py
- Incremental boundary maintenance (EWMA cut_strength, churn) — [Present]  
  fum_rt/core/adc.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/fum_rt/core/adc.py
- Frontier scout (edge/cut/cohesion targeting) — [Present]  
  fum_rt/core/cortex/void_walkers/void_frontier_scout.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/fum_rt/core/cortex/void_walkers/void_frontier_scout.py
- Engine wiring & metrics exposure — [Present]  
  fum_rt/core/engine/core_engine.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/fum_rt/core/engine/core_engine.py
- Runtime execution — [Present]  
  fum_rt/run_nexus.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/c6aedb3bb967c41d7302d4e9250578ceb0b19d4b/fum_rt/run_nexus.py

Note: Detector is implemented and running in the runtime. The physics‑bench A8 meters are separate and currently [Planned].

---

## 9) Quick Status (high‑stakes)

### Program Completion
- **A8 gates executed:** 0/12 — [Missing] — No gate runs executed yet
- **Telegraph–Fisher stepper/meters:** [Partially Present] — Causality DAG audit runner exists; cone-slack & κ-collapse meters [Planned]
- **Runtime boundary detector:** [Present] — fum_rt stack fully implemented
- **Echo/SMAE proposals:** [Present] — 5 quantum echo proposals documented
- **Core instruments (RD/KPP/KG/FRW):** [Present with RESULTS]
  - RD dispersion: ✓ meter + RESULTS
  - RD front speed: ✓ meter + experiments
  - KG Noether: ✓ meter + RESULTS (PASS)
  - FRW continuity: ✓ meter + RESULTS (PASS)
  - Metriplectic structure: ✓ meter + RESULTS
  - Tachyonic tube: ✓ meter + RESULTS

### Assets Summary
- **PROPOSALS:** 48 documented with commit-pinned permalinks
- **RESULTS:** 15 documented with artifacts (PNG/CSV/JSON)
- **RUNNERS:** 21 documented executable scripts
- **INSTRUMENTS:** 30+ meter/diagnostic modules
- **Canon References:** 13 core documentation files

### Domain Coverage
- ✓ Metriplectic (6 proposals, 6 results, 5 runners, 8+ instruments)
- ✓ Reaction-Diffusion (1 proposal, 1 result, 1 runner, 7 instruments)
- ✓ Cosmology (3 proposals, 1 result, 1 runner)
- ✓ Quantum/Echo (10 proposals, 1 runner)
- ✓ Dark Matter (1 proposal)
- ✓ Dark Photons (1 proposal, 1 result, 2 runners)
- ✓ Tachyon Condensation (1 proposal, 1 result, 1 runner, 2 instruments)
- ✓ Thermodynamic Routing (7 proposals, 3 results, 7 runners)
- ✓ Agency Field (5 proposals, 1 instrument)
- ✓ Causality (2 proposals, 1 runner)
- ✓ Collapse/A6 (1 proposal, 1 result, 1 runner)
- ✓ Intelligence Model (1 proposal, 1 result, 3 instruments)
- ✓ Quantum Gravity (3 proposals)
- ✓ Qualia (2 proposals)
- ✓ Topology (2 proposals)
- ✓ Information (1 proposal)

### Outstanding Work
- A8 gate execution suite (0/12 gates)
- Telegraph-Fisher cone-slack & κ-collapse meters
- Primordial P(k) generator
- Additional echo/CEG execution results
- Physics-bench boundary meters for A8

---

## 10) Edit checklist for maintainers

- When you land a new PROPOSAL_*, add it here with a commit‑pinned permalink.
- When you post a RESULTS_*, add the doc path, PASS/FAIL summary, and artifact basenames.
- Record new runners (exact script paths) and instruments (module paths) as they are created.
- Keep the Quick Status honest (A8, TF, etc.).
