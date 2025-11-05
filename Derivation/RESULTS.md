# RESULTS: Overview of Experimental Results

This document provides a comprehensive overview of all experimental results in the Void Dynamics Model (VDM) repository. Each results document follows whitepaper-grade standards with full narrative, MathJax-rendered equations, numeric figure captions tied to actual artifacts, explicit thresholds with pass/fail gates, and provenance. Results are organized by domain.

**Total Results Documents: 17**

> Last Updated: 2025-11-05  
> Template: `Templates/RESULTS_PAPER_STANDARDS.md`  
> Standards: All results must follow comprehensive documentation standards  
> Authorization: All experiments require approved PROPOSAL_ documents

---

## Collapse (1 result)

- **RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md**  
  Path: `Collapse/RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md`  
  *A6 Scaling Collapse - Junction Logistic Universality (v1)*
  - **Gate**: env_max ≤ 0.02 for logistic-router scaling collapse  
  - **Outcome**: PASS with env_max ≈ 0.0166  
  - **Artifact**: `code/outputs/figures/collapse/20251006_175337_a6_collapse_overlay__A6-collapse-v1.png`  
  - **Summary**: Quality-controls the A6 universality: when routing selection follows a logistic in memory contrast Δm with slope Θ, plotting P(A) vs X=ΘΔm collapses curves across Θ. This dimensionless universality statement validates the chosen router class.

---

## Conservation Law (1 result)

- **RESULTS_RD_Discrete_Conservation_vs_Balance.md**  
  Path: `Conservation_Law/RESULTS_RD_Discrete_Conservation_vs_Balance.md`  
  *Discrete Conservation vs Balance in Reaction-Diffusion (RD) Steppers*
  - **Summary**: Near-conservation scales with method order; Euler shows β≈2, Strang and discrete-gradient (DG) RD show β≈3 on two-grid error, and DG RD satisfies a per-step H-theorem.  
  - **Artifact**: `code/outputs/figures/rd_conservation/20251006_*`

---

## Cosmology (1 result)

- **RESULTS_FRW_Continuity_Residual_Quality_Check.md**  
  Path: `Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md`  
  *FRW Continuity Residual - Quality Check (v1)*
  - **Gate**: FRW dust continuity residual RMS_FRW ≤ 10⁻⁶  
  - **Outcome**: PASS with RMS_FRW ≈ 9.04×10⁻¹⁶  
  - **Artifact**: `code/outputs/figures/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.png`  
  - **Summary**: Validates FRW cosmology continuity equation implementation to machine precision, far beneath acceptance threshold.

---

## Dark Photons (1 result)

- **RESULTS_Decoherence_Portals.md**  
  Path: `Dark_Photons/RESULTS_Decoherence_Portals.md`  
  *Decoherence Portals Results (v1)*
  - **Gates**: Fisher consistency (relative error ≤ 10%) and noise budget residuals within spec  
  - **Status**: Awaiting approved run; scaffold records gates, instruments, and artifact locations

---

## Intelligence Model (1 result)

- **RESULTS_Physics_Native_Intelligence_Substrate_v1.md**  
  Path: `Intelligence_Model/RESULTS_Physics_Native_Intelligence_Substrate_v1.md`  
  *RESULTS: Physics-Native Intelligence — Substrate-Only v1*
  - **Summary**: Documents substrate certification for physics-native intelligence program, establishing conservative 2D Klein–Gordon substrate with validated energy conservation and void-faithfulness receipts.

---

## Metriplectic (9 results)

### KG_Energy_Oscillation/
- **RESULTS_KG_Energy_Oscillation_v1.md**  
  Path: `Metriplectic/KG_Energy_Oscillation/RESULTS_KG_Energy_Oscillation_v1.md`  
  *KG J-only Energy Oscillation Scaling and Time-Reversal (QC)*
  - **Summary**: Validates conservative limb of linear Klein–Gordon (KG) discretization under symplectic (Störmer–Verlet) time integrator on periodic lattice. Measures discrete energy oscillation amplitude scaling with time step and checks strict time-reversal.

### KG_Jonly_Locality_and_Dispersion/
- **RESULTS_KG_Jonly_Locality_and_Dispersion.md**  
  Path: `Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md`  
  *KG J-only Validations - Dispersion and Locality (Metriplectic Upstream)*
  - **Gates**: Two decisive Hamiltonian (J-only) gates for Klein–Gordon sector  
  - **Outcome**: Light cone speed v ≈ 0.998 (R² ≈ 0.99985), dispersion fit ω² ≈ (1.0002)·k² + 0.9978 (R² ≈ 0.999999997)  
  - **Summary**: Approved runs with pinned artifacts demonstrate excellent agreement with expected dispersion and locality properties.

### KG_RD_Metriplectic/
- **RESULTS_KG_RD_Metriplectic.md**  
  Path: `Metriplectic/KG_RD_Metriplectic/RESULTS_KG_RD_Metriplectic.md`  
  *KG⊕RD Metriplectic QC - Spectral‑DG Primary Profile*
  - **Summary**: Gate-driven QC of metriplectic KG⊕RD scheme (spectral-DG for M, Störmer-Verlet for KG J, Strang JMJ composition).  
  - **Artifact**: `code/outputs/logs/metriplectic/20251006_142434_step_spec_snapshot__kgRD-v1.json`

### Metriplectic_JMJ_RD/
- **RESULTS_Metriplectic_JMJ_RD_v1.md**  
  Path: `Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md`  
  *Metriplectic Integrator: Symplectic J-Step Composed with Discrete-Gradient M-Step*
  - **Configuration**: N=256, seeds=10, seed_scale=0.05, dg_tol=1e-12; Δt∈[0.02,0.01,0.005,0.0025,0.00125]  
  - **M-only**: PASS (slope 2.9803, R²=0.999986), Lyapunov violations = 0  
  - **JMJ (Strang)**: FAIL on slope gate (slope 2.7287, R²=0.999379), Lyapunov violations = 0  
  - **Summary**: Documents Strang defect behavior in composed metriplectic integrator.

### Core Metriplectic
- **RESULTS_KG_Noether_Invariants_v1.md**  
  Path: `Metriplectic/RESULTS_KG_Noether_Invariants_v1.md`  
  *KG Noether Invariants - Discrete Energy & Momentum Conservation (Periodic BCs)*
  - **Summary**: Documents conservation of Klein–Gordon discrete Noether invariants (energy and spatial translation momentum) under Störmer–Verlet integrator on 1D periodic lattice. Both invariants conserved to machine precision; per-step drifts O(1e-17), far beneath acceptance gate (≤ 1e-12 or 10ε√N). Reversibility test shows exact round-trip recovery within numerical noise.  
  - **Domain**: Metriplectic (J-only linear KG sector)  
  - **Tag**: KG-noether-v1

- **RESULTS_Metriplectic_Structure_Checks.md**  
  Path: `Metriplectic/RESULTS_Metriplectic_Structure_Checks.md`  
  *Metriplectic Structure Checks - J Skew and M PSD*
  - **Gates**: (i) median |⟨v, J v⟩| ≤ 1e-12 over random draws; (ii) count of negative ⟨u, M u⟩ equal to zero  
  - **Summary**: Documents algebraic structure tests for metriplectic system: skew-symmetry of canonical J operator and positive semidefiniteness (PSD) of metric operator M on RD channel.

---

## Tachyon Condensation (1 result)

- **RESULTS_Tachyonic_Tube_v1.md**  
  Path: `Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md`  
  *Tachyonic Tube v1 - Spectrum completeness and condensation curvature (QC)*
  - **Gates**: (i) completeness of discrete spectrum over physically admissible set; (ii) existence of interior minimum in condensation energy with positive curvature  
  - **Summary**: Quality-control gates for finite-radius tachyonic tube within simple scalar EFT baseline.

---

## Thermodynamic Routing (2 results)

### Passive_Thermodynamic_Routing/
- **RESULTS_Passive_Thermodynamic_Routing_v2.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/RESULTS_Passive_Thermodynamic_Routing_v2.md`  
  *RESULTS: Passive Thermodynamic Routing v2 — Symmetric Smoke (gate_set = smoke_symm)*
  - **Summary**: Documents symmetric smoke tests for passive thermodynamic routing without active switching mechanisms.

### Wave_Flux_Meter/
- **RESULTS_Wave_Flux_Meter_A_Phase_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md`  
  *Wave Flux Meter A-Phase: Closed-Box Energy Conservation and Local Balance (J-only Scalar Wave)*
  - **Gates**: (i) energy conservation within dynamic leapfrog tolerance; (ii) pointwise local balance via continuity residual r = ∂ₜe + ∇·s with V̇ = 0  
  - **Outcome**: Both gates PASSED  
  - **Summary**: J-only scalar-wave meter validated in closed box with frozen potential V. Artifacts pinned for reproducibility.

- **RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`  
  *Wave Flux Meter — Phase B (Open Ports) Results v1*

---

## Summary Statistics by Domain

| Domain | Results Count | Key Focus |
|--------|--------------|-----------|
| Collapse | 1 | Scaling universality |
| Conservation Law | 1 | Discrete conservation properties |
| Cosmology | 1 | FRW continuity validation |
| Dark Photons | 1 | Decoherence portals |
| Intelligence Model | 1 | Physics-native substrate |
| Metriplectic | 9 | Conservative-dissipative dynamics |
| Tachyon Condensation | 1 | Spectrum and condensation |
| Thermodynamic Routing | 2 | Wave flux and passive routing |

---

## Notes

- All results follow the standards at `Templates/RESULTS_PAPER_STANDARDS.md`
- Every result includes: TL;DR with artifact path, explicit gates, pass/fail outcomes, and full provenance
- Results must cite corresponding PROPOSAL_ document
- All artifacts (figures, CSVs, JSONs) are pinned with timestamps and tags for reproducibility
- Failed gates trigger contradiction reports and artifact quarantine
