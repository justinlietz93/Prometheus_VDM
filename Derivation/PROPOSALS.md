# PROPOSALS: Overview of Research Proposals

This document provides a comprehensive overview of all research proposals in the Void Dynamics Model (VDM) repository. Each proposal follows the whitepaper-grade template standards and includes explicit gates, MathJax-rendered equations, and full provenance. Proposals are organized by domain and follow the T0-T9 maturity ladder.

**Total Proposals: 35**

> Last Updated: 2025-11-05  
> Template: `Templates/PROPOSAL_PAPER_TEMPLATE.md`  
> Standards: All proposals must be approved before experiments can run  
> Authorization: See `code/common/authorization/README.md`

---

## Agency Field (5 proposals)

### Coordination_Depth/
- **PROPOSAL_Multipartite_Coordination_Depth_v1.md**  
  Path: `Agency_Field/Coordination_Depth/PROPOSAL_Multipartite_Coordinaton_Depth_v1.md`

### Core Agency Field
- **PROPOSAL_ADC_Response_Slope_v1.md**  
  Path: `Agency_Field/PROPOSAL_ADC_Response_Slope_v1.md`  
  *Testing the decision coupling law at forks: probability of choosing branch A follows P(A)=σ(Θ,Δm) where Δm=m_A-m_B. Validates fitted logistic slope equals programmed parameters.*

- **PROPOSAL_Agency_Curvature_Scaling_v1.md**  
  Path: `Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`  
  *Validates steering component by measuring path curvature of test pulses in memory field m(x). Theory predicts curvature κ_path scales linearly with transverse gradient magnitude X=Θ|∇_⊥m|.*

- **PROPOSAL_Agency_Stability_Band_v1.md**  
  Path: `Agency_Field/PROPOSAL_Agency_Stability_Band_v1.md`  
  *Maps stability/retention regime of memory/agency substrate using dimensionless groups D_a (advective/steering), Λ (loss/decay), and Γ (diffusion/spread).*

### Witness/
- **PROPOSAL_Agency_Witness_v1.md**  
  Path: `Agency_Field/Witness/PROPOSAL_Agency_Witness_v1.md`

---

## Causality (2 proposals)

- **PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md**  
  Path: `Causality/PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md`  
  *Lightweight, order-only causality audit for VDM complementing existing metric-based gates (light-cone locality and dispersion) with background-free diagnostics derived from event precedence. Constructs event DAG from timestamped events.*

- **PROPOSAL_Metriplectic_Causal_Dominance_v1.md**  
  Path: `Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md`

---

## Collapse (1 proposal)

- **PROPOSAL_A6_Collapse_v1.md**  
  Path: `Collapse/PROPOSAL_A6_Collapse_v1.md`  
  *A6 Scaling Collapse: Tests dimensionless scaling collapse when routing at Y-junction follows softmax in memory field m. Branch probability should collapse to universal curve P(A)=σ(ΘΔm) when plotted vs X=ΘΔm across multiple Θ values.*

---

## Conservation Law (1 proposal)

- **PROPOSAL_RD_Discrete_Conservation_vs_Balance.md**  
  Path: `Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md`  
  *Discrete Conservation vs. Balance in a Reaction-Diffusion Update (Void Dynamics Model)*

---

## Cosmology (2 proposals)

- **PROPOSAL_FRW_Balance_v1.md**  
  Path: `Cosmology/PROPOSAL_FRW_Balance_v1.md`  
  *FRW Continuity Balance: Implements dimensionless continuity-law residual for FRW cosmology, testing discrete consistency of input (ρ(t), a(t)). Computes residual of d/dt(ρa³) + wρd/dt(a³) (default dust w=0) with RMS residual ≤ tolerance.*

- **PROPOSAL_FRW_Continuity_Predictive_v2.md**  
  Path: `Cosmology/PROPOSAL_FRW_Continuity_Predictive_v2.md`

---

## Dark Photons (1 proposal)

- **PROPOSAL_Decoherence_Portals.md**  
  Path: `Dark_Photons/PROPOSAL_Decoherence_Portals.md`  
  *Decoherence Portals via Dark-Photon Mixing: Pre-registered investigation of dark-photon (DP) kinetic mixing as decoherence portal leaving measurable imprints in precision electromagnetic noise spectra and Fisher budgets in shielded resonant cavities.*

---

## Information (1 proposal)

- **PROPOSAL_SIE_Invariant_and_Novelty_v1.md**  
  Path: `Information/PROPOSAL_SIE_Invariant_and_Novelty_v1.md`  
  *Certifies clean first integral Q for local information engine (SIE) in reaction-only limit and quantifies controlled deviations under novelty. For logistic-like kinetics, Q is constant; with parameter kick, Q drifts and recovers.*

---

## Intelligence Model (1 proposal)

- **PROPOSAL_Physics_Native_Intelligence_v1.md**  
  Path: `Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md`  
  *Physics-Native Intelligence (VDM) — Substrate v1: First step of physics-native intelligence program avoiding training and operating in real time. Phase 1 establishes conservative, reversible 2D Klein–Gordon substrate for information structures to persist and interact without external learning loops.*

---

## Metriplectic (8 proposals)

- **PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md`

- **PROPOSAL_Metriplectic_Lindblad_T4.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_Lindblad_T4.md`

- **PROPOSAL_Metriplectic_SymplecticPlusDG.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md`  
  *Metriplectic - Symplectic (KG) + Discrete-Gradient (RD): Composition of symplectic time-stepping for conservative Klein-Gordon dynamics with discrete-gradient methods for dissipative reaction-diffusion.*

### Strang_Defect_vs_dt_kg_RD/
- **PROPOSAL_KG_plus_RD_Metriplectic.md**  
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_KG_plus_RD_Metriplectic.md`  
  *KG ⊕ RD Metriplectic Experiment: Two-field metriplectic dynamics combining Klein-Gordon and reaction-diffusion systems.*

- **PROPOSAL_Metriplectic_JMJ_RD_v1.md**  
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_Metriplectic_JMJ_RD_v1.md`  
  *Metriplectic Integrator for Mixed Conservative-Dissipative Dynamics: Symplectic J-step ⊕ Discrete-Gradient M-step composition scheme.*

### Thermal_Landscape_Quench/
- **PROPOSAL_Thermal_Landscape_Quench_v1.md**  
  Path: `Metriplectic/Thermal_Landscape_Quench/PROPOSAL_Thermal_Landscape_Quench_v1.md`

### PROPOSAL_Echo_vs_Static_Calibration/
- **PROPOSAL_Echo_CEG_Static_PROPOSAL_v1.md**  
  Path: `Metriplectic/PROPOSAL_Echo_vs_Static_Calibration/PROPOSAL_Echo_CEG_Static_PROPOSAL_v1.md`

### Self_Model_Assisted_Echo/
- **PROPOSAL_Self_Model_Assisted_Echo_v1.md**  
  Path: `Metriplectic/Self_Model_Assisted_Echo/PROPOSAL_Self_Model_Assisted_Echo_v1.md`

---

## Qualia (2 proposals)

- **PROPOSAL_T3_Calibration_of_Psychophysical_Observables_to_C_Field.md**  
  Path: `Qualia/PROPOSAL_T3_Calibration_of_Psychophysical_Observables_to_C_Field.md`  
  *T3 — Calibration of Psychophysical Observables to the VDM (C)-Field*

- **PROPOSAL_vdm_qualia_program.md**  
  Path: `Qualia/PROPOSAL_vdm_qualia_program.md`  
  *VDM–Qualia Program: Coupled‑Field Explanations of Psychedelic Phenomenology using sober proxies.*

---

## Quantum Gravity (2 proposals)

- **PROPOSAL_Dark_Photon_Bridge.md**  
  Path: `Quantum_Gravity/PROPOSAL_Dark_Photon_Bridge.md`  
  *Quantum Gravity Bridge v1: Bridging VDM with quantum gravity through dark photon dynamics.*

- **PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md**  
  Path: `Quantum_Gravity/PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md`  
  *VDM ↔ Quantum-Gravity Bridge: Causal Geometry and Holonomy Tests connecting VDM framework to quantum gravity through causal structure.*

---

## Tachyon Condensation (1 proposal)

- **PROPOSAL_Tachyonic_Tube_Condensation.md**  
  Path: `Tachyon_Condensation/PROPOSAL_Tachyonic_Tube_Condensation.md`  
  *Tachyonic Tube Condensation and Spectrum: Studies condensation dynamics and spectral properties of tachyonic field configurations in tube geometry.*

---

## Thermodynamic Routing (6 proposals)

- **PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md**  
  Path: `Thermodynamic_Routing/PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md`

### Passive_Thermodynamic_Routing/
- **PROPOSAL_Flux_Through_Memory_Channels_v1.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Flux_Through_Memory_Channels_v1.md`  
  *Flux Through Memory Channels (Frozen Landscape) — Passive Thermodynamic Routing v2 Pre‑Registration*

- **PROPOSAL_Passive_Thermodynamic_Routing_v2.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md`  
  *Passive Thermodynamic Routing v2 Pre-Registration: Tests passive routing through memory channels without active switching.*

### Prereg_Biased_Main/
- **PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md**  
  Path: `Thermodynamic_Routing/Prereg_Biased_Main/PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md`  
  *Thermodynamic Routing v2 — Prereg Biased Main: Pre-registered main study with biased initial conditions.*

### Wave_Flux_Meter/
- **PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md`

- **PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`  
  *Wave Flux Meter — Phase B (Open-Ports with Absorber) v1*

- **PROPOSAL_Wave_Flux_Meter_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md`  
  *Wave Poynting-Meter Instrument v1 (Thermodynamic Routing — Photonic Track): Establishes wave-based flux measurement instrument.*

---

## Topology (2 proposals)

- **PROPOSAL_Loop_Quench_Test_Robustness_v2.md**  
  Path: `Topology/PROPOSAL_Loop_Quench_Test_Robustness_v2.md`

- **PROPOSAL_Loop_Quench_Test_v1.md**  
  Path: `Topology/PROPOSAL_Loop_Quench_Test_v1.md`

---

## Notes

- All proposals must follow the template at `Templates/PROPOSAL_PAPER_TEMPLATE.md`
- Proposals are graded T0-T9 according to maturity ladder (see TIER_STANDARDS.md)
- Each proposal requires approval before experiments can run
- Proposals must include: explicit gates, provenance, equations, and artifact paths
- Higher-tier proposals (T4+) must reference supporting work from lower tiers
