# PROPOSALS: Overview of Research Proposals

This document provides a comprehensive overview of all research proposals in the Void Dynamics Model (VDM) repository. Each proposal follows the whitepaper-grade template standards and includes explicit gates, MathJax-rendered equations, and full provenance. Proposals are organized by domain and follow the T0-T9 maturity ladder.

**Total Proposals: 84**

> Last Updated: 2025-11-19  
> Template: `Templates/PROPOSAL_PAPER_TEMPLATE.md`  
> Standards: All proposals must be approved before experiments can run  
> Authorization: See `code/common/authorization/README.md`

---

## Agency Field (5 proposals)

- **PROPOSAL_ADC_Response_Slope_v1.md**  
  Path: `Agency_Field/PROPOSAL_ADC_Response_Slope_v1.md`
  - **Gate(s)**: Gates:** (|\hat\Theta/\Theta-1|\le 0.05); (R^2\ge 0.99); KS (p>0.1)....

- **PROPOSAL_Agency_Curvature_Scaling_v1.md**  
  Path: `Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`
  - **Gate(s)**: Gates:** (|\beta|\le 0.05,\alpha,\bar X); slope CV (\le 10%) across (\Theta); (R^2\ge 0.99)....

- **PROPOSAL_Agency_Stability_Band_v1.md**  
  Path: `Agency_Field/PROPOSAL_Agency_Stability_Band_v1.md`
  - **Gate(s)**: Gates:** contiguous band where retention (>0.8), half-life within target window, and cross-slice reproducibility (Jaccard index (\ge 0.7))....

### Coordination Depth/

- **PROPOSAL_Multipartite_Coordinaton_Depth_v1.md**  
  Path: `Agency_Field/Coordination_Depth/PROPOSAL_Multipartite_Coordinaton_Depth_v1.md`
  *PROPOSAL_Multipartite_Coordination_Depth_v1.1.md*
  - **Gate(s)**: gated) for stronger nonlocal transport (report both profiles)....

### Witness/

- **PROPOSAL_Agency_Witness_v1.md**  
  Path: `Agency_Field/Witness/PROPOSAL_Agency_Witness_v1.md`
  *PROPOSAL_Agency_Witness_v1.1.md*
  - **Gate(s)**: gated)....

---

## Axioms (5 proposals)

- **T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md**  
  Path: `Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md`
  *T8 - A8 (Axiom Candidate) — Lietz Infinity Resolution Conjecture*
  - **Tier**: T8
  - **Diagnostics**: - Require $(c/c\_\star \le 1+\epsilon\_c)$ and a good exponential‑tail fit $(adj.(R^2\ge 0.98))$; a steepness sweep shows $(c)$ approaches $(c\_\star)$ from above but does not exceed gate. **PASS** if...

### A8 Hierarchy Gates/

- **T3_PROPOSAL_A8_Hierarchy_Gates_v1.md**  
  Path: `Axioms/A8_Hierarchy_Gates/T3_PROPOSAL_A8_Hierarchy_Gates_v1.md`
  *T3 (Smoke) - A8 Two‑Gate Hierarchy Test (N(L)~log L & E_exc~L^{d-1})*
  - **Tier**: T3
  - **Diagnostics**: - **Detectors:** interface counters and energy aggregators with threshold sweeps; report detector‑sensitivity scans. - **Fits:** (i) depth vs log L (slope near 1), (ii) log E_exc vs log L (slope α ≈...
  - **Gate(s)**: Gate Hierarchy Test",; gate.v1.json"],...

### A8 Protein-Packing Boundary-Law/

- **T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md**  
  Path: `Axioms/A8_Protein-Packing_Boundary-Law/T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md`
  *T2_A8_PROPOSAL_Protein‑Packing‑Meters_for_Hierarchical_Boundary‑Law_v1.md*
  - **Tier**: T2
  - **Diagnostics**: **Meters (and methods).** 1. **(R_g(n))** — average subchain (R_g) over all windows of length (n) (as defined in the papers). Report two‑slope fit ((\nu_1,\nu_2)) and kink (n^*) with CIs. 2. **(S(q))...
  - **Gate(s)**: gate** for later A8 claims at T4–T8....

### A8 Scaling 1D/

- **T1_A8_PROPOSAL_1D_Scaling_v1.md**  
  Path: `Axioms/A8_Scaling_1D/T1_A8_PROPOSAL_1D_Scaling_v1.md`
  *T1 (Proto-model) - A8 1D Scaling Instrument: Interface Hierarchy and Area-Law Energy*
  - **Tier**: T1
  - **Diagnostics**: Normalization and parameters (per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)): - Domain length $L$, grid $N$, spacing $\Delta x=L/N$; temporal window $T$ and $\Delta t$ for dynamic r...

### A8 Scaling 2D3D/

- **T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md**  
  Path: `Axioms/A8_Scaling_2D3D/T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md`
  *T1 (Proto-model) — A8 Area-Law Instrument in 2D/3D Domains*
  - **Tier**: T1
  - **Diagnostics**: 5.4 Regression and reporting - For each $d$ and each detector, regress $\log E_{\mathrm{exc}}$ vs $\log L$ across $L$; report slope, intercept, $R^2$, CIs. - Aggregate across seeds by medians; re...
  - **Gate(s)**: - Tachyonic regime validation ($V''(0)<0$) is a pre-check for input configurations (instrument logs the check)....

---

## Causality (4 proposals)

- **PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md**  
  Path: `Causality/PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md`
  *Causal DAG Audits for the Void Dynamics Model (VDM)*

- **PROPOSAL_Metriplectic_Causal_Dominance_v1.md**  
  Path: `Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md`
  *Why I think this is a strong proposal (and not a foundation error)*
  - **Diagnostics**: And to keep the zeitgeist thread visible for folks outside VDM: Google’s posts make the echo/OTOC mechanism and its verifiability explicit; if you echo‑test on lattice and show the same phenomenology...
  - **Gate(s)**: gate.**...

- **T1_PROPOSAL_G-TF-1_Telegraph-Fisher_Causality_v1.md**  
  Path: `Causality/T1_PROPOSAL_G-TF-1_Telegraph-Fisher_Causality_v1.md`
  *4) G‑TF‑1 — Telegraph–Fisher Causality Bridge (finite‑speed) (T1, paper‑only)*
  - **Tier**: T1
  - **Gate(s)**: * **G‑TF‑1.1:** Closed‑form derivation of (c=\sqrt{D/\tau}). **PASS**.; * **G‑TF‑1.2:** Cone‑slack inequality stated and proved. **PASS**.; * **G‑TF‑1.3:** Discrete admissibility conditions enumerated...

### Causal DAG Audits/

- **T1_PROPOSAL_Causal_DAG_Audits_v1.md**  
  Path: `Causality/Causal_DAG_Audits/T1_PROPOSAL_Causal_DAG_Audits_v1.md`
  *T1 (Proto-model) - Causal DAG Audits via Transfer Entropy (TE/MTE) for Locality-Constrained Transport*
  - **Tier**: T1
  - **Diagnostics**: - Causality collection justification and gate sketch: [PRIVATE causality note](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/causality.md). Scientific need: - Beyond visual front-arrival timing,...

---

## Closure (1 proposal)

- **T1_PROPOSAL_G-CL-1_Closure-NoHiddenIntegrals_v1.md**  
  Path: `Closure/T1_PROPOSAL_G-CL-1_Closure-NoHiddenIntegrals_v1.md`
  *G‑CL‑1 — Closure/Integrability Test (no hidden invariants) (T1, paper‑only)*
  - **Tier**: T1
  - **Gate(s)**: * **G‑CL‑1.1:** Theorem statement (restricted class + assumptions). **PASS**.; * **G‑CL‑1.2:** Criterion applied, concluding “no extra first integrals” beyond A4 Casimirs. **PASS** = derivation writte...

---

## Collapse (1 proposal)

- **PROPOSAL_A6_Collapse_v1.md**  
  Path: `Collapse/PROPOSAL_A6_Collapse_v1.md`
  *A6 Scaling Collapse - Proposal (v1)*
  - **Diagnostics**: Questions addressed: - Does the junction selection indeed collapse to σ(X) across Θ? - Is the residual envelope ≤ 2% across the shared domain? - Are there systematic deviations (e.g., at large |X|) t...
  - **Gate(s)**: - Is the residual envelope ≤ 2% across the shared domain?...

---

## Conservation Law (1 proposal)

- **PROPOSAL_RD_Discrete_Conservation_vs_Balance.md**  
  Path: `Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md`
  *PROPOSAL - Discrete Conservation vs. Balance in a Reaction-Diffusion Update (Void Dynamics Model)*
  - **Diagnostics**: - **Scheme order p:** start with Euler (p=1), then Strang (p=2) using exact logistic substep (see reaction_exact.py). - **Neumann BCs** are reserved only for the front‑speed control runs....

---

## Cosmology (8 proposals)

- **PROPOSAL_FRW_Balance_v1.md**  
  Path: `Cosmology/PROPOSAL_FRW_Balance_v1.md`
  *FRW Continuity Balance - Proposal (v1)*
  - **Gate(s)**: Gate: RMS residual ≤ tol (default 1e-6); emit CONTRADICTION_REPORT on fail....

- **PROPOSAL_FRW_Continuity_Predictive_v2.md**  
  Path: `Cosmology/PROPOSAL_FRW_Continuity_Predictive_v2.md`

- **T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md**  
  Path: `Cosmology/T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md`
  *1. T4 (Preregistered) — Testing a Single‑Axis VDM Portal Modulation Against CMB Low‑ℓ Power‑Tensor Anomalies*
  - **Tier**: T4
  - **Diagnostics**: **Model under test (VDM prior):** For each ℓ, [ A_{ij}^{\text{model}}(\ell)=\frac{C_\ell}{3}\Bigl[\delta_{ij}+\epsilon,g_\ell,\bigl(3,\hat f_i\hat f_j-\delta_{ij}\bigr)\Bigr],\qquad |\epsilon|\ll1, ]...
  - **Gate(s)**: gate. See their **Fig. 1 (p. 3)** for the mask and (f_{\rm sky}).; Gates wiring:** Bind pass/fail evaluation to the three preregistered metrics in `PRE-REGISTRATION.json`. Emit a machine‑readable `pas...

### CMB/

- **T2_PROPOSAL_EBN_CMB_Pipeline_v1.md**  
  Path: `Cosmology/CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md`
  *T2 (Instrument) - EBN‑CMB‑ISW+Lens Pipeline (A8→Boltzmann→CMB/LSS)*
  - **Tier**: T2
  - **Diagnostics**: - **Inputs:** A8 generator parameters (interface scale λ, hierarchy depth control, tilt parameters); cosmological background (Ω_b, Ω_c, H0, τ, etc.). - **Diagnostics:** FRW balance (dust) RMS ≤ 1e−6...

- **T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md**  
  Path: `Cosmology/CMB/T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md`
  *1. T3 (Smoke) — CMB Hemispherical Power Asymmetry as VDM Causal Genesis Witness*
  - **Tier**: T3
  - **Diagnostics**: **Data:** - **Planck PR4 FULLSKY** component-separated maps (SMICA, Commander) - **Masks**: Galactic plane + point source masks from PR4 release - **Lensing products**: PR4/NPIPE lensing for null che...

### Ringdown Meter/

- **T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md**  
  Path: `Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md`
  *T2 — Discrete‑Scale Invariance Ringdown Meter (DSI‑RDM)*
  - **Tier**: T2
  - **Diagnostics**: **Created:** 2025‑11‑15 • **Commit:** *(pin at run time)* • **Salted provenance:** *(pin at run time)* **Proposer:** Justin K. Lietz (PI, implementer, approver) • <[justin@neuroca.ai](mailto:justin@ne...
  - **Gate(s)**: gate summary `{G1:true/false, G2:true/false, G3:true/false}`, seeds, commit, timings, environment. (Same basename discipline as the RESULTS standard.)...

- **T2_PROPOSAL_Ringdown_Meter_v1.md**  
  Path: `Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md`
  *T2 (Instrument) — VDM Ringdown Meter: Damped Normal Modes on a Metriplectic Scalar Field (First‑Principles, No‑GR)*
  - **Tier**: T2
  - **Diagnostics**: **Governing equations (canon, linearized):** J‑limb: $ \partial_{tt}\phi - c^2 \nabla^2 \phi + m_{\rm eff}^2 \phi = 0 $. M‑limb (DG update): decreases $ \mathcal{L}[\phi] $ monotonically; composition...

- **T3_PROPOSAL_Topological_Ringdown_Attempt_v1.md**  
  Path: `Cosmology/Ringdown_Meter/T3_PROPOSAL_Topological_Ringdown_Attempt_v1.md`
  *T3 PROPOSAL — Topological Ringdown Attempt (Topo‑RDM add‑on to DSI‑RDM) v1*
  - **Tier**: T3

---

## Dark Matter (1 proposal)

- **T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md**  
  Path: `Dark_Matter/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md`
  *1. T5 (Pilot) — First‑Principles Skyrme‑SIDM × VDM Micro‑to‑Macro Bridge*
  - **Tier**: T5
  - **Diagnostics**: **Parameters (inputs).** * Dwarf anchors: $(m)$ $[GeV]$, $((\sigma_T/m)_0)$ $[cm(^2)/g]$. * ERE choice: $(\xi)$ for $(r\_e=\xi R\_\ast)$ (single global in ($\[0.5,1.0]$\)). * Numerics: ODE tolerances...
  - **Gate(s)**: gates to test consistency with codimension‑1 energy concentration and pulled fronts. The proposal registers **unitarity/analyticity** hygiene, **refinement** gates on the solved profile, and **optical...

---

## Dark Photons (1 proposal)

- **PROPOSAL_Decoherence_Portals.md**  
  Path: `Dark_Photons/PROPOSAL_Decoherence_Portals.md`
  *Proposal: Decoherence Portals via Dark-Photon Mixing: Noise-Spectrum and Fisher-Budget Tests of Kinetic Mixing in Shielded Cavities (DP-Portal-v1)*
  - **Diagnostics**: Instrumentation (baseline): - Shielded resonant RF cavity (Q characterized), tunable center frequency covering $f\in[\,10^3,10^6\,]$ Hz (example band; exact band to be set by available hardware). - C...

---

## Entropy (1 proposal)

### Self-Information/

- **T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md**  
  Path: `Entropy/Self-Information/T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md`
  *1. T3 (Smoke) — Agency as Entropy-Echo Measurement via Void-Walker Self-Information Flow*
  - **Tier**: T3
  - **Diagnostics**: **Domain:** - **2D metriplectic field** with void-walkers (particles that interact with the field via local coupling and export state tokens/marks) - **Field**: Telegraph-Fisher substrate with J/M sp...

---

## Fluid Dynamics (1 proposal)

### Fluids Corner Regularization/

- **T2_PROPOSAL_OQ-021_VDM-Fluids_Corner_Regularization_v1.md**  
  Path: `Fluid_Dynamics/Fluids_Corner_Regularization/T2_PROPOSAL_OQ-021_VDM-Fluids_Corner_Regularization_v1.md`
  *T2 — PROPOSAL_OQ‑021_VDM‑Fluids_Corner_Regularization_v1*
  - **Tier**: T2

---

## Gravity (3 proposals)

### B1938+666 Pinch Visibility-Plane Lensing/

- **T4_PROPOSAL_NFW_for_the_B1938+666_Pinch_v1.md**  
  Path: `Gravity/B1938+666_Pinch_Visibility-Plane_Lensing/T4_PROPOSAL_NFW_for_the_B1938+666_Pinch_v1.md`
  *1. T4 (Prereg) — VDM vs. NFW for the B1938+666 “Pinch”: a preregistered visibility‑plane lensing test*
  - **Tier**: T4
  - **Diagnostics**: **Question.** *Does a compact VDM Σ‑profile explain the B1938+666 pinch more convincingly than a truncated‑NFW subhalo on the same meter?* **Instrument (T2).** Visibility‑plane forward model ( \mathc...

### Emergent Gravity for Strong-Lensing/

- **T3_PROPOSAL_Emergent_Gravity_for_Strong-Lensing_Substructure_v1.md**  
  Path: `Gravity/Emergent_Gravity_for_Strong-Lensing/T3_PROPOSAL_Emergent_Gravity_for_Strong-Lensing_Substructure_v1.md`
  *T3→T4 — VDM Emergent Gravity for Strong‑Lensing Substructure (B1938+666‑class)*
  - **Tier**: T3
  - **Diagnostics**: * **T3 (Smoke):** Show that a compact VDM excitation (tachyonic KG branch) produces the qualitative “ring‑pinch” seen in B1938+666‑class systems. * **T4 (Prereg):** Register hypotheses, parameter pr...
  - **Gate(s)**: Gate (T4):**; Gate:** KS $p>0.1$ and posterior overlap ≥0.5 with the nearest KG‑tube family.; Gate:** $g_1,g_2\le 10^{-10}$ (refined), $\Delta S\ge0$ in M‑step; locality cone slope matches $c=\sqrt{2J...

### Gravity Regression/

- **T5_PROPOSAL_Gravity_Regression_v1.md**  
  Path: `Gravity/Gravity_Regression/T5_PROPOSAL_Gravity_Regression_v1.md`
  *T5 (Pilot) - Gravity Regression — Weak‑Field VDM vs SPARC/Lensing Suites*
  - **Tier**: T5
  - **Diagnostics**: - **Inputs:** curated SPARC subset; preregistered lensing targets; priors on nuisance parameters. - **Diagnostics:** hold‑out predictive performance; residual structure; ΔAIC/ΔBIC; ΔlnZ; null predic...

---

## Hierarchy (2 proposals)

- **T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md**  
  Path: `Hierarchy/T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md`
  *G‑A8‑1 — A8 Scaling Theorem (1D Existence) (T1, paper‑only)*
  - **Tier**: T1
  - **Gate(s)**: * **G‑A8‑1.1:** Theorem statement with all assumptions and constants declared. **PASS** = formal statement present.; * **G‑A8‑1.2:** Lemmas (tail, interface energy, spacing) proved or rigorously cited...

### STIV/

- **T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md**  
  Path: `Hierarchy/STIV/T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md`
  *1. T2 (Instrument) — STIV Macrostate & Gradient‑Flow Meters for A8 Boundary Hierarchies*
  - **Tier**: T2
  - **Diagnostics**: ---...
  - **Gate(s)**: gate metrics**, while validating meters on analytic shapes and controlled RD/KG fields.; Gate G‑H:** $\Delta \Sigma\ge -10^{-12}$ (or $\Delta F\le +10^{-12}$) per step....

---

## Information (1 proposal)

- **PROPOSAL_SIE_Invariant_and_Novelty_v1.md**  
  Path: `Information/PROPOSAL_SIE_Invariant_and_Novelty_v1.md`
  - **Diagnostics**: * **Domain:** `Derivation/code/physics/information/` * **ODE:** as above; integrators: Euler and RK4. * **Diagnostics:** two-grid error (E(\Delta t)), log–log slope; (Q)-drift time series with/without...

---

## Intelligence Model (2 proposals)

- **PROPOSAL_Physics_Native_Intelligence_v1.md**  
  Path: `Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md`
  *Physics-Native Intelligence (VDM) — Substrate v1 Proposal*
  - **Diagnostics**: - Substrate: 2D KG J-only conservative dynamics with leapfrog time-stepping. - Grid/time: $(N_x, N_y)$, spacings $a_x,a_y$, $\Delta t$ with CFL guard. - Boundaries: reflective walls or periodic; cho...
  - **Gate(s)**: Gate G1: RMS energy drift $\le \epsilon_E$ with scaling $\epsilon_E = K_E (\Delta t / a)^2$.; Gate G2: coefficient of determination $R^2 \ge 0.9995$ for $\partial_t e$ vs $-\nabla\cdot s$.; Gate G3: r...

- **T4_PROPOSAL_VDM_Physics_to_AI_Model_v1.md**  
  Path: `Intelligence_Model/T4_PROPOSAL_VDM_Physics_to_AI_Model_v1.md`
  *1. T4 (Prereg) — VDM Physics → AI Model Roadmap v1*
  - **Tier**: T4
  - **Diagnostics**: Domains covered - KG J-only substrate (T2/T3 instrumentation) - Metriplectic assisted-echo controllers (T4 prereg) - Thermodynamic routing meters (wave flux) - CMB-meter and T_CMB(z) check (cosmology...
  - **Gate(s)**: gated progression with external calibration: T2 substrate → T3 routing/probe-only → T4 prereg assistance (echo) → new T4 cross-benchmarks and pulled-front tests.; Gate per expert; if PASS, either deep...

---

## Metriplectic (16 proposals)

- **PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md`

- **PROPOSAL_Metriplectic_Lindblad_T4.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_Lindblad_T4.md`
  - **Tier**: T0
  - **Diagnostics**: 3. **Clarify symmetry assumptions in the two T4s** * **PROPOSAL_SIE_Invariant_and_Novelty_v1**: add a one‑line lemma defining (Q) and the exact discrete symmetry/closure assumptions; place the drift...
  - **Gate(s)**: Gate:** saturation slope (\partial n/\partial N\to 0) beyond (n\simeq 1) (units set by your normalization) across (>90%) of modes tested.; Gate:** an explicit algebra showing ({\hat\psi_i,\hat\psi_j}=...

- **PROPOSAL_Metriplectic_SymplecticPlusDG.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md`
  *Proposal: Metriplectic - Symplectic (KG) + Discrete-Gradient (RD)*
  - **Gate(s)**: gated policy with tag-scoped schemas to support canon promotion and downstream integration.; Gates and Success Criteria:...

- **T1_PROPOSAL_QGT_to_Metriplectic_Instrument.md**  
  Path: `Metriplectic/T1_PROPOSAL_QGT_to_Metriplectic_Instrument.md`
  *T1 (Proto-model) — QGT → Metriplectic Instrument*
  - **Tier**: T1
  - **Gate(s)**: Outputs: PNG+CSV+JSON artifacts logged to canon paths; pass/fail by pre-registered gates....

- **T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md**  
  Path: `Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md`
  *1. T4 — Counterfactual Echo Gain (CEG): A Metriplectic Assisted‑Echo Experiment in VDM*
  - **Tier**: T4

### Analog Horizon/

- **T5_PROPOSAL_Analog_Horizon_v1.md**  
  Path: `Metriplectic/Analog_Horizon/T5_PROPOSAL_Analog_Horizon_v1.md`
  *T5 (Pilot) - Analog Horizon — Telegraph‑Fisher Causality & Causal Dominance Meter*
  - **Tier**: T5
  - **Diagnostics**: - **Platform:** any medium realizing TF dynamics (electrical/acoustic meta‑lattice, BEC phononics). - **Knobs:** D via coupling; τ via relaxation network; J‑limb c from wave branch. - **Diagnostic...

### CEG Metric Definition/

- **T2_PROPOSAL_CEG_Metric_Definition_v1.md**  
  Path: `Metriplectic/CEG_Metric_Definition/T2_PROPOSAL_CEG_Metric_Definition_v1.md`
  *1. T2 (Instrument) — Corrective Echo Gain (CEG) Metric Definition and Validation*
  - **Tier**: T2
  - **Diagnostics**: **Domains for validation:** 1. **Reaction-Diffusion (RD)**: 2D Fisher-KPP or Gray-Scott system with zero-flux boundaries. 2. **Klein-Gordon J-only**: 2D hyperbolic field with leapfrog integrator. 3....

### CEG Metriplectic Assistance/

- **T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md**  
  Path: `Metriplectic/CEG_Metriplectic_Assistance/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md`
  *1. T4 — Counterfactual Echo Gain (CEG): A Metriplectic Assisted‑Echo Experiment in VDM*
  - **Tier**: T4
  - **Diagnostics**: **Maturity ladder (T0–T9) in brief.** Tiers track evidence maturity and scope: T0 (Concept) articulates ideas and falsifiers; T1 (Proto‑model) implements the first working toy; T2 (Instrument) certifi...
  - **Gate(s)**: gate‑bounded, metriplectic assisted‑echo** and its preregistered metric (CEG). Target findings: (i) statistically robust $(\mathrm{CEG}>0)$ under energy‑matched controls; (ii) zero violations of J‑Noe...

### Constructive QGT to Metriplectic/

- **T1_PROPOSAL_G-QGT-1_QGT-to-Metriplectic_Mapping_v1.md**  
  Path: `Metriplectic/Constructive_QGT_to_Metriplectic/T1_PROPOSAL_G-QGT-1_QGT-to-Metriplectic_Mapping_v1.md`
  *G‑QGT‑1 — Constructive QGT → Metriplectic Mapping (T1, paper‑only)*
  - **Tier**: T1
  - **Diagnostics**: * **Objects:** (H(\lambda)), eigenframe (|u_n(\lambda)\rangle), (Q_{\mu\nu}), pushforward to observables, functionals (\mathcal I,\Sigma). * **Diagnostics (paper‑only):** algebraic checks for antisymm...

### Contact Geometry Projection/

- **T1_PROPOSAL_G-CG-1_Contact-to-Metriplectic_v1.md**  
  Path: `Metriplectic/Contact_Geometry_Projection/T1_PROPOSAL_G-CG-1_Contact-to-Metriplectic_v1.md`
  *G‑CG‑1 — Contact Geometry Projection → Metriplectic Split (T1, paper‑only)*
  - **Tier**: T1
  - **Diagnostics**: * **Objects:** ((\mathcal M,\eta,R,H_c)), projections (P_{\perp}, P_{\parallel}), brackets ({\cdot,\cdot}_J), ((\cdot,\cdot)_M). * **Diagnostics:** verify (J^\top=-J), (M^\top=M\ge0), and the two dege...
  - **Gate(s)**: * **G‑CG‑1.1:** Reeb construction fully specified; **PASS** = ( \eta(R)=1,, d\eta(R,\cdot)=0) shown.; * **G‑CG‑1.2:** Projection formulas yield explicit (J,M); **PASS** = closed forms given.; * **G‑CG...

### Metriplectic Instruments/

- **T2_PROPOSAL_Metriplectic_Instruments_v1.md**  
  Path: `Metriplectic/Metriplectic_Instruments/T2_PROPOSAL_Metriplectic_Instruments_v1.md`
  *T2 (Instrument) - Metriplectic Instruments: Identity, KG, RD, and FRW Meters (EBN series)*
  - **Tier**: T2
  - **Diagnostics**: **KG J‑only meter.** Inputs: grid N, Δt, c, m, seeds. Diagnostics: dispersion fit (ω² vs k²), cone slope v. **Gates:** v ≤ c·(1+0.02); dispersion fit R² ≥ 0.999; Noether drifts ≤ 1e−12. **RD meter.*...
  - **Gate(s)**: Gates:** v ≤ c·(1+0.02); dispersion fit R² ≥ 0.999; Noether drifts ≤ 1e−12.; Gates:** |c_obs/(2√(Dr))−1| ≤ 0.05 with R² ≥ 0.98; dispersion median rel‑err ≤ 1e−2....

### Schrodingerization KvN/

- **T1_PROPOSAL_Schrodingerization_KvN_v1.md**  
  Path: `Metriplectic/Schrodingerization_KvN/T1_PROPOSAL_Schrodingerization_KvN_v1.md`
  *T1 (Proto-model) - Schrödingerization (Koopman–von Neumann) Lifting of Metriplectic J ⊕ M to a Unified Hamiltonian Instrument*
  - **Tier**: T1
  - **Diagnostics**: ---...

### Strang Defect vs dt kg RD/

- **PROPOSAL_KG_plus_RD_Metriplectic.md**  
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_KG_plus_RD_Metriplectic.md`
  *Proposal: KG ⊕ RD Metriplectic Experiment (Two-Field)*
  - **Diagnostics**: 3. Run a minimal sweep - N=256, seeds=10, dt = [0.02, 0.01, 0.005, 0.0025]. - Record gates and artifacts; update a new RESULTS file `Derivation/kg_metriplectic/RESULTS_KG_plus_RD.md`....

- **PROPOSAL_Metriplectic_JMJ_RD_v1.md**  
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_Metriplectic_JMJ_RD_v1.md`
  *1. Metriplectic Integrator for Mixed Conservative-Dissipative Dynamics: Symplectic J-step ⊕ Discrete-Gradient M-step*

### TF Causality/

- **T1_PROPOSAL_TF_Causality_v1.md**  
  Path: `Metriplectic/TF_Causality/T1_PROPOSAL_TF_Causality_v1.md`
  *T1 (Proto-model) - Telegraph–Fisher (TF) Causality Instrument: Finite-Speed Transport and Cone Gates*
  - **Tier**: T1
  - **Diagnostics**: Known parameters and normalization (per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)): - Grid: $N$, $\Delta x$; time: $T$, $\Delta t$; seeds. - TF parameters: $\{D,\tau\}$; optional...

### Void Debt Transport Throttle/

- **T1_PROPOSAL_Void_Debt_Transport_Throttle_v1.md**  
  Path: `Metriplectic/Void_Debt_Transport_Throttle/T1_PROPOSAL_Void_Debt_Transport_Throttle_v1.md`
  *T1 (Proto-model) - Void-Debt Transport Throttling Instrument: $c_{\mathrm{eff}}=c_0 \exp(-\tfrac{1}{2}\beta D)$ Gates*
  - **Tier**: T1
  - **Diagnostics**: - Approach: Construct $\widehat{D}$ from simulation fields; estimate $c_{\mathrm{eff}}$ by cones/dispersion; fit $c_{\mathrm{eff}}/c_0$ vs $D$ to $\exp(-\tfrac{1}{2}\beta D)$; test attenuation gates a...
  - **Gate(s)**: Gate metrics: relative error bands on predicted vs measured $c_{\mathrm{eff}}$, monotonicity of attenuation with increasing $D$....

---

## Nonequilibrium (2 proposals)

### GB Oscillating Load/

- **T2_PROPOSAL_GB_Oscillating_Load_v1.md**  
  Path: `Nonequilibrium/GB_Oscillating_Load/T2_PROPOSAL_GB_Oscillating_Load_v1.md`
  *1. T2 — GB Relaxation Meter under Oscillating Load (v1)*
  - **Tier**: T2
  - **Diagnostics**: Planned rigor: - IEEE‑754 float64, deterministic seeds, commit‑hash provenance. - IO policy via [`io_paths.py`](../code/common/io_paths.py). - Canon discipline: anchors only; no equation/number d...

### Self Organization/

- **T2_PROPOSAL_Self_Organization_Meters_v1.md**  
  Path: `Nonequilibrium/Self_Organization/T2_PROPOSAL_Self_Organization_Meters_v1.md`
  *T2 (Instrument) — Self-Organization Onset Meters (Nicolis–Prigogine)*
  - **Tier**: T2
  - **Gate(s)**: Gate: rolling worst positive slope over tail window $\le \text{tol}$ (default $10^{-12}$).; Gate: detect sign-change in $\Re(\lambda_1)$ across the $\beta$ ladder; $\min |\Re(\lambda_1)| \le 10^{-6}$ ...

---

## Qualia (2 proposals)

- **PROPOSAL_vdm_qualia_program.md**  
  Path: `Qualia/PROPOSAL_vdm_qualia_program.md`
  *VDM–Qualia Program: Coupled‑Field Explanations of Psychedelic Phenomenology (Sober Proxies)*
  - **Gate(s)**: Gate:** ≥2 significant spectral peaks (z>3 over baseline) at eigenmodes predicted by simulated $K_{vv}$; color/opponent alternation rate matches band spacing.; Gate:** Condition A: $\Delta S>0$, primi...

- **T3_PROPOSAL_Calibration_of_Psychophysical_Observables_to_C_Field.md**  
  Path: `Qualia/T3_PROPOSAL_Calibration_of_Psychophysical_Observables_to_C_Field.md`
  *1. T3 — Calibration of Psychophysical Observables to the VDM (C)-Field*
  - **Tier**: T3
  - **Diagnostics**: **Known parameters & defaults** * **Tasks (2–3):** TOJ bias (ms), Cross‑modal projection (psychometric slope / ITPC), Dynamic texture spectrum ((1/f) exponent). * **Sampling:** within‑subject, (n \ge...
  - **Gate(s)**: Gate evaluation & logs:** emit JSON + CSV with pass/fail and salted provenance; publish figures per RESULTS standard.; Gates:** ≤500 LOC/file; no outer→inner deps; interfaces for cross‑layer calls; te...

---

## Quantum (11 proposals)

- **T0_PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md**  
  Path: `Quantum/T0_PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md`
  *PROPOSAL — VDM J‑branch QFT Bootstrap & Metriplectic Decoherence (v1)*
  - **Tier**: T0
  - **Diagnostics**: **Domain routing.** Figures → `Derivation/doce/physics/outputs/figures/quantum/` Logs (CSV/JSON) → `Derivation/doce/physics/outputs/logs/quantum/` **Minimum artifact set per run (code‑enforced):** 1...

- **T1_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence__ProtoModel_v1.md**  
  Path: `Quantum/T1_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence__ProtoModel_v1.md`
  *1. Tier Grade, Proposal Title and Date*
  - **Tier**: T1

- **T2_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence_Instrument_v1.md**  
  Path: `Quantum/T2_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence_Instrument_v1.md`
  *Instrument for this proposal*
  - **Tier**: T2

- **T4_PROPOSAL_J-to_Dirac_v1.md**  
  Path: `Quantum/T4_PROPOSAL_J-to_Dirac_v1.md`
  *1. T4 (Prereg) - T4 — J→Dirac‑Aligned False‑Vacuum Metastability & Void‑Debt Asymmetry (Preregistration v1)*
  - **Tier**: T4
  - **Diagnostics**: **Fields & functionals (minimal working form).** β‑field with tilted double‑well potential \( V_\beta(\beta)=\tfrac{\lambda}{4}(\beta^2-v^2)^2+\epsilon\,\beta \) with small tilt \(\epsilon\); announ...
  - **Gate(s)**: Gate:** fit \(R_c=K\,\sigma/\Delta V\) with \(R^2\ge 0.99\) and \(|K/\kappa_d-1|\le 0.15\).; Gate:** exponential fit \(R^2\ge 0.99\); KS p\(>0.1\) on tail; CI for \(\Gamma\).; Gate:** \(\langle\Delta ...

### Analog Quantum/

- **T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md**  
  Path: `Quantum/Analog_Quantum/T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md`
  *1. T4 (Prereg) — Cold-Atom Test of VDM Causal Cone in Metriplectic Optical Lattice*
  - **Tier**: T4
  - **Diagnostics**: **System:** - **2D optical lattice** (square geometry preferred for symmetry) - **Ultracold Bose gas** (e.g., $^{87}$Rb or $^{39}$K) in Mott insulator or superfluid regime - **Quantum-gas microscope*...

### Quantum Echos/

- **T0_PROPOSAL_SIE_Willow-Convergence_v1.md**  
  Path: `Quantum/Quantum_Echos/T0_PROPOSAL_SIE_Willow-Convergence_v1.md`
  *T0 PROPOSAL_SIE_Willow-Convergence_v1.md*
  - **Tier**: T0
  - **Diagnostics**: **Domain string (for routing):** `quantum` **Runner (suggested path; you may rename):** `Derivation/doce/physics/code/runners/quantum/sie_willow_convergence_v1.py` **I/O routing (via `io_paths.py`):*...
  - **Gate(s)**: gates pass....

- **T1_PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md**  
  Path: `Quantum/Quantum_Echos/T1_PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md`
  *PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md*
  - **Tier**: T1
  - **Diagnostics**: **Domain:** `qis` (quantum‑information‑style echo testbed) **Outputs (managed by `io_paths.py`):** * **Figures dir (canonical):** `Derivation/code/physics/outputs/figures/qis/` * **Logs dir (canon...

- **T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md**  
  Path: `Quantum/Quantum_Echos/T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md`
  *1. Tier Grade, Proposal Title and Date*
  - **Tier**: T4
  - **Diagnostics**: This proposal (T4) preregisters a falsifiable causality claim using those meters. **Novelty & impact.** Demonstrating a cone‑limited $M$ limb under $J\oplus M$ would provide a unifying causal constra...

- **T4_PROPOSAL_SMAE_CEG_v1.md**  
  Path: `Quantum/Quantum_Echos/T4_PROPOSAL_SMAE_CEG_v1.md`
  *1. Tier Grade, Proposal Title and Date*
  - **Tier**: T4
  - **Diagnostics**: **System.** 1D/2D lattice; **JMJ Strang** composition with established RD/KG meters (front speed, dispersion, Noether). **No body forces**, local operators only. AMD stack (VDM rule). **Forward pass.*...
  - **Gate(s)**: gated, falsifiable observables** (A0–A7). Prior validated slices include **RD front‑speed and dispersion** (PASS) and a **logarithmic on‑site invariant** used as a QA guard, with explicit drift/fit ga...

- **T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md**  
  Path: `Quantum/Quantum_Echos/T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md`
  *Convergence Note (motivation-first)*
  - **Tier**: T4
  - **Diagnostics**: and we publish all artifacts with hashes and PASS/FAIL JSON....
  - **Gate(s)**: gates** with explicit thresholds and require **mandatory artifacts**:; gates**,; Gate G1 — Monotone fidelity recovery.**...

### Quantum Engine/

- **T4_PROPOSAL_Quantum-Resource-Engine_v1.md**  
  Path: `Quantum/Quantum_Engine/T4_PROPOSAL_Quantum-Resource-Engine_v1.md`
  *T4 — Quantum‑Resource Engine: A Metriplectic Ledger to Test “Beyond‑Carnot” Efficiencies*
  - **Tier**: T4
  - **Diagnostics**: **State & symbols (VDM canon).** We use the canonical notation sheet for fields, fluxes, and ledger variables; Noether energy/flux diagnostics anchor the J‑leg. **System under test (SUT).** * Work...
  - **Gate(s)**: Gate:** PASS/FAIL is mechanical.; Gate G‑1**.; Gate G‑2** (≥1.05 with CI)....

---

## Quantum Gravity (3 proposals)

- **PROPOSAL_Dark_Photon_Bridge.md**  
  Path: `Quantum_Gravity/PROPOSAL_Dark_Photon_Bridge.md`
  *Quantum Gravity Bridge - Proposal (v1)*
  - **Diagnostics**: - Tooling: - Cosmology: CLASS or CAMB CLI bindings; results marshalled into JSON/CSV with provenance. - Portals: Python analyses for noise budgets and Fisher quick estimates. - Diagnostics & accep...

- **PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md**  
  Path: `Quantum_Gravity/PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md`
  *VDM ↔ Quantum-Gravity Bridge: Causal Geometry and Holonomy Tests*
  - **Diagnostics**: Date: YYYY-MM-DD...
  - **Gate(s)**: gates**. Passing these gates would establish that VDM realizes a micro-causal, hyperbolic geometry consistent with a causal-set-like substrate while supporting gauge-like loop transport—an essential b...

- **T2_PROPOSAL_QG_Regge_CDT_v1.md**  
  Path: `Quantum_Gravity/T2_PROPOSAL_QG_Regge_CDT_v1.md`
  - **Tier**: T2
  - **Diagnostics**: * **A7 Measurability:** every claim maps to an observable (balance residuals, spectral proxies, scaling exponents) with thresholds in RESULTS docs. ---...
  - **Gate(s)**: Gates (T2 Instrument):**; Gates (T3 Smoke → T4 Prereg):**; Gates (T4 Prereg → T5 Pilot):** preregister a narrow set of observables and acceptance thresholds; pilot on small lattices to confirm stable ...

---

## Spinor (1 proposal)

- **T1_PROPOSAL_Spinor_Emergence_v1.md**  
  Path: `Spinor/T1_PROPOSAL_Spinor_Emergence_v1.md`
  *T1 (Proto-model) - Spinor Emergence from the VDM J‑Limb (Dirac Sector from a Scalar Void Lattice)*
  - **Tier**: T1
  - **Diagnostics**: - **C1 — Clifford algebra gate:** Construct local γ^μ on coarse cells with `{γ^μ, γ^ν}=2η^{μν}` to O(a^2). - **C2 — Dirac reduction gate:** Linearization of the discrete Euler–Lagrange equation arou...

---

## Tachyon Condensation (1 proposal)

- **PROPOSAL_Tachyonic_Tube_Condensation.md**  
  Path: `Tachyon_Condensation/PROPOSAL_Tachyonic_Tube_Condensation.md`
  *Tachyonic Tube Condensation and Spectrum (Proposal)*
  - **Diagnostics**: Parameters: $\mu$, $\lambda$, $c$, $\ell_{\max}$. Diagnostics: (a) root-finding convergence counts, (b) per-mode $\kappa_\ell$, $N4_\ell$, $v_\ell$, $M_\ell^2$, (c) energy scan $E(R)$ and minima stati...

---

## Thermodynamic Routing (7 proposals)

- **PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md**  
  Path: `Thermodynamic_Routing/PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md`
  *PROPOSAL_Thermodynamic_Routing_NoSwitch_v2.md*
  - **Gate(s)**: gated).; gated).; gates produce a `CONTRADICTION_REPORT` with ablations. No post-hoc tuning beyond the pre-registered grids....

### Passive Thermodynamic Routing/

- **PROPOSAL_Flux_Through_Memory_Channels_v1.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Flux_Through_Memory_Channels_v1.md`
  *Flux Through Memory Channels (Frozen Landscape) — Passive Thermodynamic Routing v2 (Pre‑Registration)*

- **PROPOSAL_Passive_Thermodynamic_Routing_v2.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md`
  *PROPOSAL: Passive Thermodynamic Routing v2 (Pre-Registration)*
  - **Diagnostics**: Assumptions and exclusions: - Discrete operator stability respected (Δt ≤ 0.8/ω_max from discrete spectral operator) - Single-thread numerics, deterministic FFT/plan where applicable - Seeds: fixed b...
  - **Gate(s)**: gated diagnostics for the J⊕M coupling limb. No parameter tuning post hoc; windowing and masks are predeclared.; gated).; Gate: zero violations of $\Delta L_h \le 0$...

### Prereg Biased Main/

- **PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md**  
  Path: `Thermodynamic_Routing/Prereg_Biased_Main/PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md`
  *PROPOSAL: Thermodynamic Routing v2 — Prereg Biased Main*

### Wave Flux Meter/

- **PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md`
  - **Tier**: T2
  - **Diagnostics**: * **Dimensionless KPIs.** Report and gate on the dimensionless groups in your symbols sheet (e.g., (M_v,\ \Sigma,\ \Lambda,\ \Pi_{Dr},\ c^*)). Scale‑collapse and regime classification live here. * *...

- **PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`
  *Proposal: Wave Flux Meter — Phase B (Open-Ports with Absorber) v1*

- **PROPOSAL_Wave_Flux_Meter_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md`
  *Proposal: Wave Poynting-Meter Instrument v1 (Thermodynamic Routing — Photonic Track)*

---

## Thermodynamics (1 proposal)

### Convection/

- **T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md**  
  Path: `Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md`
  *T2 — A Rayleigh–Bénard Onset Gate (“RB‑Gate”) for Deep‑M Limb Convection Solvers*
  - **Tier**: T2
  - **Diagnostics**: * **Parameterized BCs** to detect boundary‑condition mis‑specifications automatically. ---...
  - **Gate(s)**: gate-preflight",; Gate instrument runs that write artifacts.",; Gate.md",...

---

## Topology (2 proposals)

- **PROPOSAL_Loop_Quench_Test_Robustness_v2.md**  
  Path: `Topology/PROPOSAL_Loop_Quench_Test_Robustness_v2.md`

- **PROPOSAL_Loop_Quench_Test_v1.md**  
  Path: `Topology/PROPOSAL_Loop_Quench_Test_v1.md`
  - **Diagnostics**: * **Domain:** `Derivation/code/physics/topology/` * **Dynamics:** 2D RD with stable explicit scheme; no-flux boundaries. * **Observables:** binary mask of (\phi>\tau); simple cycle count via cycle bas...
  - **Gate(s)**: Gates:** Kendall (\tau \le -0.7) with (p<10^{-6}); lifetime tail fit slope (>2) (fast decay)....

---

## Transport (1 proposal)

### Telegraph From Relaxation/

- **T1_PROPOSAL_Telegraph_From_Relaxation_v1.md**  
  Path: `Transport/Telegraph_From_Relaxation/T1_PROPOSAL_Telegraph_From_Relaxation_v1.md`
  *T1 (Proto-model) - Telegraph From Relaxation Instrument*
  - **Tier**: T1

---

