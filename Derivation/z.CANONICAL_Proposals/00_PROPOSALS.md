# PROPOSALS: Overview of Research Proposals

This document provides a comprehensive overview of all research proposals in the Void Dynamics Model (VDM) repository. Each proposal follows the whitepaper-grade template standards and includes explicit gates, MathJax-rendered equations, and full provenance. Proposals are organized by domain and follow the T0-T9 maturity ladder.

**Total Proposals: 86**

> Last Updated: 2025-11-19  
> Template: `Templates/PROPOSAL_PAPER_TEMPLATE.md`  
> Standards: All proposals must be approved before experiments can run  
> Authorization: See `code/common/authorization/README.md`

---

## Agency Field (5 proposals)

- **PROPOSAL_ADC_Response_Slope_v1.md**  
  Path: `Agency_Field/PROPOSAL_ADC_Response_Slope_v1.md`
  *PROPOSAL_ADC_Response_Slope_v1.md*
  - **Diagnostics**: ** logistic regression of outcomes vs (\Delta m); slope (\hat\Theta) with CI; KS test for model adequacy....
  - **Gate(s)**: fails: stop run, write `CONTRADICTION_REPORT.json` with seed, grid, dt, hash of spec, failing metric, and nearest checkpoints for replay....

- **PROPOSAL_Agency_Curvature_Scaling_v1.md**  
  Path: `Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`
  *PROPOSAL_Agency_Curvature_Scaling_v1.md*
  - **Diagnostics**: ** centerline extraction; discrete curvature; linear regression (\kappa) vs (X); collapse across (\Theta). One PNG + CSV + JSON per run....
  - **Gate(s)**: fails: stop run, write `CONTRADICTION_REPORT.json` with seed, grid, dt, hash of spec, failing metric, and nearest checkpoints for replay....

- **PROPOSAL_Agency_Stability_Band_v1.md**  
  Path: `Agency_Field/PROPOSAL_Agency_Stability_Band_v1.md`
  *PROPOSAL_Agency_Stability_Band_v1.md*
  - **Diagnostics**: ** retention metric (peak/plateau ratio), half-life, spatial SNR. Heatmap over a grid of ((\gamma,\delta,\kappa))....
  - **Gate(s)**: fails: stop run, write `CONTRADICTION_REPORT.json` with seed, grid, dt, hash of spec, failing metric, and nearest checkpoints for replay....

### Coordination Depth/

- **PROPOSAL_Multipartite_Coordinaton_Depth_v1.md**  
  Path: `Agency_Field/Coordination_Depth/PROPOSAL_Multipartite_Coordinaton_Depth_v1.md`
  *PROPOSAL_Multipartite_Coordination_Depth_v1.1.md*
  - **Gate(s)**: emits `CONTRADICTION_REPORT__{tag}.json` with per-(S) histograms, adjusted vs unadjusted CIs, local-match diagnostics, and discretization ablations....

### Witness/

- **PROPOSAL_Agency_Witness_v1.md**  
  Path: `Agency_Field/Witness/PROPOSAL_Agency_Witness_v1.md`
  *PROPOSAL_Agency_Witness_v1.1.md*
  - **Gate(s)**: ** $m_2$ that preserves **local statistics** at the agent position (value, gradient, curvature). Define...

---

## Axioms (7 proposals)

- **T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md**  
  Path: `Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md`
  *T8 - A8 (Axiom Candidate) — Lietz Infinity Resolution Conjecture*
  - **Tier**: T8
  - **Gate(s)**: for predictive curvature of observables; under smooth reparameterizations of $(u)$ it shifts by $(O(|\nabla u|^2))$ only....

### A8 Hierarchy Gates/

- **T3_PROPOSAL_A8_Hierarchy_Gates_v1.md**  
  Path: `Axioms/A8_Hierarchy_Gates/T3_PROPOSAL_A8_Hierarchy_Gates_v1.md`
  *T3 (Smoke) - A8 Two‑Gate Hierarchy Test (N(L)~log L & E_exc~L^{d-1})*
  - **Tier**: T3
  - **Diagnostics**: - **Detectors:** interface counters and energy aggregators with threshold sweeps; report detector‑sensitivity scans. - **Fits:** (i) depth vs log L (slope near 1), (ii) log E_exc vs log L (slope α ≈ d−1). - **Acceptance (joint):** slope_N within [0.9, 1.1] **and** |α − (d−1)| ≤ 0.1 with R² ≥ 0.98; AIC/BIC prefer boundary‑law over volume‑law nulls....


### A8 Protein-Packing Boundary-Law/

- **T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md**  
  Path: `Axioms/A8_Protein-Packing_Boundary-Law/T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md`
  *T2_A8_PROPOSAL_Protein‑Packing‑Meters_for_Hierarchical_Boundary‑Law_v1.md*
  - **Tier**: T2
  - **Diagnostics**: **Meters (and methods).** 1. **(R_g(n))** — average subchain (R_g) over all windows of length (n) (as defined in the papers). Report two‑slope fit ((\nu_1,\nu_2)) and kink (n^*) with CIs. 2. **(S(q))** — backbone structure factor; overlay vs backbone diameter scale (\sigma_{bb}). 3. **Core fraction (f_{\text{core}})** — **rSASA thresholding** (Lee–Richards probe, rSASA (<10^{-3})) to tag core resi...


### A8 Scaling 1D/

- **T1_A8_PROPOSAL_1D_Scaling_v1.md**  
  Path: `Axioms/A8_Scaling_1D/T1_A8_PROPOSAL_1D_Scaling_v1.md`
  *T1 (Proto-model) - A8 1D Scaling Instrument: Interface Hierarchy and Area-Law Energy*
  - **Tier**: T1
  - **Diagnostics**: Normalization and parameters (per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)): - Domain length $L$, grid $N$, spacing $\Delta x=L/N$; temporal window $T$ and $\Delta t$ for dynamic relaxation when needed; seeds $S$. - Potential and regime: choose a smooth double‑well tachyonic potential with $V''(0)<0$ (e.g., $V(\phi)=\tfrac{1}{4}(\phi^2-1)^2 - \tfrac{\mu}{2}\phi^2$ with $\mu>0$);...
  - **Gate(s)**: - Count law: Fit $N(L)$ vs $\log L$ using robust regression; slope $\hat s$ within tolerance of a positive constant and $R^2\ge 0.98$; report CI and detector sensitivity bands. - Area law (1D): Fit $E_{\mathrm{exc}}(L)$ vs $L^{\,0}$ (constant w.r.t. $L$) with $R^2\ge 0.98$; equivalently, linear fit of $\log E_{\mathrm{exc}}$ vs $\log L$ with slope $|\hat\alpha|\le 0.1$ (tunable in prereg). - Tachyonic check: Validate $V''(0)<0$ numerically from supplied potential; runs failing this check are invalid. New tools/scripts (commit before runs): - Detector implementations: Derivation/code/physics/ax...


- **T1_PROPOSAL_A8_1D_Scaling_v1.md**  
  Path: `Axioms/A8_Scaling_1D/T1_PROPOSAL_A8_1D_Scaling_v1.md`
  *T1 (Proto-model) - A8 1D Scaling Instrument: Interface Hierarchy and Area-Law Energy*
  - **Diagnostics**: Normalization and parameters (per UNITS_NORMALIZATION.md): - Domain length $L$, grid $N$, spacing $\Delta x=L/N$; temporal window $T$ and $\Delta t$ for dynamic relaxation when needed; seeds $S$. - Potential and regime: choose a smooth double‑well tachyonic potential with $V''(0)<0$ (e.g., $V(\phi)=\tfrac{1}{4}(\phi^2-1)^2 - \tfrac{\mu}{2}\phi^2$ with $\mu>0$); or a canonical tachyonic quadratic...
  - **Gate(s)**: pre-registered for experiments. Assumptions and limitations: - 1D baseline isolates interface counting and energy aggregation; higher‑D generalization is outside scope. - Detector definitions (thresholds and morphological choices) affect $N(L)$; the instrument reports detector sensitivity scans to...
### A8 Scaling 2D3D/

- **T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md**  
  Path: `Axioms/A8_Scaling_2D3D/T1_A8_PROPOSAL_AreaLaw_2D3D_v1.md`
  *T1 (Proto-model) — A8 Area-Law Instrument in 2D/3D Domains*
  - **Tier**: T1
  - **Gate(s)**: Primary area-law gate (per dimension $d=2$ or $d=3$): - Fit $\log E_{\mathrm{exc}}(L)$ vs $\log L$; expected slope $\hat\alpha \approx d-1$. - Acceptance band: $|\hat\alpha - (d-1)| \le 0.1$ with $R^2 \ge 0.98$. - Report CI for $\hat\alpha$ via bootstrap across seeds; report detector/threshold sensitivity bands. Secondary gates (quality controls): - Detector robustness: for the accepted $\epsilon$-neighborhood, detector kind, and threshold, area-law slope must stay within ±0.1 across at least two detector families (e.g., threshold and TV). - Resolution robustness: two-resolution check (refined...
  - **Methods/Protocol**: 5.1 Domain and BCs - $d=2$: square domains; $d=3$: cubic domains. Periodic or no-flux BC; record choice in JSON. - $N\in\{256,512\}$ typical for 2D; $N\in\{64,96,128\}$ for 3D baseline (CPU-friendly), with an explicit plan to re-run a subset at finer resolution. 5.2 Detector specifics - Threshold detector: count/locate interface voxels where $|\phi|\ge \theta$ (tunable $\theta$), then construct bo...


- **T1_PROPOSAL_A8_AreaLaw_2D3D_v1.md**  
  Path: `Axioms/A8_Scaling_2D3D/T1_PROPOSAL_A8_AreaLaw_2D3D_v1.md`
  *T1 (Proto-model) — A8 Area-Law Instrument in 2D/3D Domains*
  - **Diagnostics**: (informational); the primary fit uses the total $E_{\mathrm{exc}}(L)$. 5.4 Regression and reporting - For each $d$ and each detector, regress $\log E_{\mathrm{exc}}$ vs $\log L$ across $L$; report slope, intercept, $R^2$, CIs. - Aggregate across seeds by medians; report interquartile ranges and bootstrap CIs. ---
  - **Gate(s)**: Primary area-law gate (per dimension $d=2$ or $d=3$): - Fit $\log E_{\mathrm{exc}}(L)$ vs $\log L$; expected slope $\hat\alpha \approx d-1$. - Acceptance band: $|\hat\alpha - (d-1)| \le 0.1$ with $R^2 \ge 0.98$. - Report CI for $\hat\alpha$ via bootstrap across seeds; report detector/threshold...
---

## Causality (4 proposals)

- **PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md**  
  Path: `Causality/PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md`
  *Causal DAG Audits for the Void Dynamics Model (VDM)*
  - **Diagnostics**: derived from event precedence. The experiment constructs an event directed acyclic graph (DAG) from timestamped events and: (i) verifies acyclicity (modulo jitter tolerance), (ii) computes a transitive reduction (TR) to expose the minimal causal skeleton, (iii) samples Alexandrov intervals I(p, q) t...
  - **Gate(s)**: (light-cone locality and dispersion) with background-free diagnostics derived from event precedence. The experiment constructs an event directed acyclic graph (DAG) from timestamped events and: (i) verifies acyclicity (modulo jitter tolerance), (ii) computes a transitive reduction (TR) to expose the...

- **PROPOSAL_Metriplectic_Causal_Dominance_v1.md**  
  Path: `Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md`
  *Why I think this is a strong proposal (and not a foundation error)*
  - **Gate(s)**: is not an artifact of hyperbolizing M. Keep it off by default to preserve A4 semantics. (You already have a telegraph/KG variant noted in equations.)...

- **T1_PROPOSAL_G-TF-1_Telegraph-Fisher_Causality_v1.md**  
  Path: `Causality/T1_PROPOSAL_G-TF-1_Telegraph-Fisher_Causality_v1.md`
  *4) G‑TF‑1 — **Telegraph–Fisher Causality Bridge (finite‑speed)** (T1, paper‑only)*
  - **Tier**: T1
### Causal DAG Audits/

- **T1_PROPOSAL_Causal_DAG_Audits_v1.md**  
  Path: `Causality/Causal_DAG_Audits/T1_PROPOSAL_Causal_DAG_Audits_v1.md`
  *T1 (Proto-model) - Causal DAG Audits via Transfer Entropy (TE/MTE) for Locality-Constrained Transport*
  - **Diagnostics**: Known parameters (unit normalization per UNITS_NORMALIZATION.md): - Spatial grid: $N$, $\Delta x$; temporal: $T$, $\Delta t$; seeds $S$. - Transport regime knobs for context (when using TF calibration runs): $(D,\tau)$ or equivalent cone-calibration references; alternatively $(c,m)$ for J-baseline. - TE parameters: embedding $(k,l)$, delay sweep $\Delta\ell \in [0,\Delta\ell_{\max}]$, estimator...
  - **Gate(s)**: require: (i) adjacency recovery matching the grid’s local stencil, (ii) delay structure consistent with the transport cone from Telegraph–Fisher calibration (VDM-E-105), and (iii) near-zero TE outside the cone (acausal pairs). The instrument produces machine-auditable PNG/CSV/JSON artifacts routed...
---

## Closure (1 proposal)

- **T1_PROPOSAL_G-CL-1_Closure-NoHiddenIntegrals_v1.md**  
  Path: `Closure/T1_PROPOSAL_G-CL-1_Closure-NoHiddenIntegrals_v1.md`
  *G‑CL‑1 — **Closure/Integrability Test (no hidden invariants)** (T1, paper‑only)*
  - **Tier**: T1
---

## Collapse (1 proposal)

- **PROPOSAL_A6_Collapse_v1.md**  
  Path: `Collapse/PROPOSAL_A6_Collapse_v1.md`
  *A6 Scaling Collapse - Proposal (v1)*
  - **Diagnostics**: - Protocol: sample P(A) at a junction for several Θ and Δm sweeps; compute the envelope on a shared X grid....

---

## Conservation Law (1 proposal)

- **PROPOSAL_RD_Discrete_Conservation_vs_Balance.md**  
  Path: `Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md`
  *PROPOSAL - Discrete Conservation vs. Balance in a Reaction-Diffusion Update (Void Dynamics Model)*

---

## Cosmology (8 proposals)

- **PROPOSAL_FRW_Balance_v1.md**  
  Path: `Cosmology/PROPOSAL_FRW_Balance_v1.md`
  *FRW Continuity Balance - Proposal (v1)*
  - **Diagnostics**: computes the residual of d/dt(ρ a³) + w ρ d/dt(a³) (default dust w=0) and gates PASS when the RMS residual ≤ tolerance. This provides a low-cost sanity check for background bookkeeping prior to full cosmological embeddings....
  - **Gate(s)**: PASS when the RMS residual ≤ tolerance. This provides a low-cost sanity check for background bookkeeping prior to full cosmological embeddings....

- **PROPOSAL_FRW_Continuity_Predictive_v2.md**  
  Path: `Cosmology/PROPOSAL_FRW_Continuity_Predictive_v2.md`

- **T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md**  
  Path: `Cosmology/T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md`
  *1. T4 (Preregistered) — Testing a Single‑Axis VDM Portal Modulation Against CMB Low‑ℓ Power‑Tensor Anomalies*
  - **Tier**: T4
  - **Diagnostics**: ** Reproduce the meter behavior (entropy curves, anomalous ℓ list, Kuiper tests) under Patel et al.’s unified mask ((f_{\rm sky}\approx0.929)), **Nside=512**, **1° Gaussian** beam, and **ISAP** inpainting before any model fitting; this is the **T2 instrument** gate. See their **Fig. 1 (p. 3)** for t...
  - **Gate(s)**: **. Methods follow standard data‑analysis rules (masking, simulations, specification tests) and preregistration norms....

### CMB/

- **T2_PROPOSAL_EBN_CMB_Pipeline_v1.md**  
  Path: `Cosmology/CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md`
  *T2 (Instrument) - EBN‑CMB‑ISW+Lens Pipeline (A8→Boltzmann→CMB/LSS)*
  - **Tier**: T2
  - **Diagnostics**: - **Inputs:** A8 generator parameters (interface scale λ, hierarchy depth control, tilt parameters); cosmological background (Ω_b, Ω_c, H0, τ, etc.). - **Diagnostics:** FRW balance (dust) RMS ≤ 1e−6; internal consistency checks; CMB peak positions and heights within preregistered envelopes; lensing amplitude; ISW cross‑checks. - **Acceptance (gates):** (G1) FRW balance gate passes; (G2) fit qualit...


- **T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md**  
  Path: `Cosmology/CMB/T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md`
  *1. T3 (Smoke) — CMB Hemispherical Power Asymmetry as VDM Causal Genesis Witness*
  - **Experimental Setup**: Data: - Planck PR4 FULLSKY component-separated maps (SMICA, Commander) - Masks: Galactic plane + point source masks from PR4 release - Lensing products: PR4/NPIPE lensing for null checks (optional) - Reionization prior: PR4 τ constraint (April 2025 analysis) for low-ℓ calibration Tools: - healpy: SHT via `map2alm`, `anafast`, `alm2map`, `rotator` - libsharp: Fast C99 SHT with MPI (for large-scale transforms) - Python: NumPy, SciPy, Matplotlib for analysis and plotting Parameters and defaults: - Multipole range: ℓ_max ∈ {100, 200, 600} (focus on ℓ < 100 for asymmetry, ℓ < 600 for...
  - **Diagnostics**: Data: - Planck PR4 FULLSKY component-separated maps (SMICA, Commander) - Masks: Galactic plane + point source masks from PR4 release - Lensing products: PR4/NPIPE lensing for null checks (optional) - Reionization prior: PR4 τ constraint (April 2025 analysis) for low-ℓ calibration
  - **Methods/Protocol**: Cartesian product of independent variables: - Component method: {SMICA, Commander} - Mask: {conservative (|b| > 30°), aggressive (|b| > 10°)} - ℓ_max: {100, 200, 600} - Observables: {R-metric at ε=0.1, $K_{\ell}^{(\Delta\ell=1)}$ for ℓ < 100} Total conditions: ~12 runs (2 methods × 2 masks × 3 ℓ_max, not all combinations necessary) Estimated runtime: - Per method/mask/ℓ_max: 10-30 minutes (SHT + rotations + MC comparison) - Total compute budget: ~4-8 hours (serial), ~1-2 hours (parallel)...
### Ringdown Meter/

- **T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md**  
  Path: `Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md`
  *T2 — Discrete‑Scale Invariance Ringdown Meter (DSI‑RDM)*
  - **Tier**: T2

- **T2_PROPOSAL_Ringdown_Meter_v1.md**  
  Path: `Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md`
  *T2 (Instrument) — VDM Ringdown Meter: Damped Normal Modes on a Metriplectic Scalar Field (First‑Principles, No‑GR)*
  - **Tier**: T2
  - **Diagnostics**: **Governing equations (canon, linearized):** J‑limb: $ \partial_{tt}\phi - c^2 \nabla^2 \phi + m_{\rm eff}^2 \phi = 0 $. M‑limb (DG update): decreases $ \mathcal{L}[\phi] $ monotonically; composition J–M–J (Strang) yields an effective damping of modal amplitudes (small‑dissipation regime). Metrics and flux are computed via $ \mathcal{H}, \mathbf{S} $. **Geometry & BCs:** 2‑D disk or 3‑D ball of ra...

- **T3_PROPOSAL_Topological_Ringdown_Attempt_v1.md**  
  Path: `Cosmology/Ringdown_Meter/T3_PROPOSAL_Topological_Ringdown_Attempt_v1.md`
  *T3 PROPOSAL — Topological Ringdown Attempt (Topo‑RDM add‑on to DSI‑RDM) v1*
  - **Tier**: T3


---

## Dark Matter (1 proposal)

- **T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md**  
  Path: `Dark_Matter/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md`
  *1. T5 (Pilot) — First‑Principles Skyrme‑SIDM × VDM Micro‑to‑Macro Bridge*
  - **Diagnostics**: Parameters (inputs). *Dwarf anchors: $(m)$ $[GeV]$, $((\sigma_T/m)_0)$ $[cm(^2)/g]$.* ERE choice: $(\xi)$ for $(r\_e=\xi R\_\ast)$ (single global in ($\[0.5,1.0]$\)). * Numerics: ODE tolerances; quadrature tolerances for $(F\_{\rm prof}(q))$; $(k)$ grid.
  - **References**: *J. K. Lietz. 2025. The Lietz Infinity Resolution Conjecture: Hierarchical Scale-Breaking in Tachyonic Metriplectic Systems (v0.1). Zenodo. <https://doi.org/10.5281/zenodo.17503344>;* J. K. Lietz. 2025. Agency field evolution in metriplectic systems. VDM Canonical Documentation, <https://github.com/justinlietz93/Prometheus_VDM/Derivation/AGENCY_FIELD.md>.; *J. K. Lietz. 2025. Causality-enhanced guidance in the Void Dynamics Model. VDM Internal Report, <https://github.com/justinlietz93/Prometheus_VDM/Derivation/>.;* Voxtrium. 2025. Voxtrium/GR-DM-Interaction-Theory: SU2-Skyrme-SIDM-Microphysics (v1.0). Zenodo. <https://doi.org/10.5281/zenodo.16857209>
---

## Dark Photons (1 proposal)

- **PROPOSAL_Decoherence_Portals.md**  
  Path: `Dark_Photons/PROPOSAL_Decoherence_Portals.md`
  *Proposal: Decoherence Portals via Dark-Photon Mixing: Noise-Spectrum and Fisher-Budget Tests of Kinetic Mixing in Shielded Cavities (DP-Portal-v1)*
  - **Gate(s)**: fails triggers a CONTRADICTION_REPORT with raw artifacts and root-cause analysis; no claims about DP signals are made....

---

## Entropy (1 proposal)

### Self-Information/

- **T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md**  
  Path: `Entropy/Self-Information/T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md`
  *1. T3 (Smoke) — Agency as Entropy-Echo Measurement via Void-Walker Self-Information Flow*
  - **Experimental Setup**: Domain: - 2D metriplectic field with void-walkers (particles that interact with the field via local coupling and export state tokens/marks) - Field: Telegraph-Fisher substrate with J/M split (Strang composition) - Walkers: Four policy types: thermal (no memory), random (memoryless), scripted (fixed sequence), adaptive (goal-directed with self-model) Parameters and defaults: - Grid: N = 512 (2D), dx = 1.0 - Time step: Δt = 0.5 × CFL - Forward duration: T ∈ {100, 500, 1000} steps - Perturbation: δ ∈ {1e-6, 1e-5, 1e-4} (local kick magnitude) - Walker count: n_walkers = 32 per cluster - Energy...
  - **Diagnostics**: Domain: - 2D metriplectic field with void-walkers (particles that interact with the field via local coupling and export state tokens/marks) - Field: Telegraph-Fisher substrate with J/M split (Strang composition) - Walkers: Four policy types: thermal (no memory), random (memoryless), scripted (fixed sequence), adaptive (goal-directed with self-model)
  - **Methods/Protocol**: Cartesian product of independent variables: - Policy: {thermal, random, scripted, adaptive} - T: {100, 500, 1000} - δ: {1e-6, 1e-5, 1e-4} - K: {16, 32, 64} - Seeds: {1..32} Total conditions (selective sampling): ~100-200 runs (not full Cartesian; prioritize adaptive vs. random at multiple δ and T) Estimated runtime: - Per condition (single policy, T, δ, seed): 5-15 minutes (CPU + GPU for walker simulation) - Total compute budget: ~20-50 hours (parallelizable across seeds) Success actions: 1....
---

## Fluid Dynamics (1 proposal)

### Fluids Corner Regularization/

- **T2_PROPOSAL_OQ-021_VDM-Fluids_Corner_Regularization_v1.md**  
  Path: `Fluid_Dynamics/Fluids_Corner_Regularization/T2_PROPOSAL_OQ-021_VDM-Fluids_Corner_Regularization_v1.md`
  *T2 — PROPOSAL_OQ‑021_VDM‑Fluids_Corner_Regularization_v1*
  - **Tier**: T2
  - **Gate(s)**: .  Readiness is bolstered by existing results: KG J‑only light‑cone and dispersion pass with tight fits and $(v\approx 0.998)$, showing the locality meters work....

---

## Gravity (3 proposals)

### B1938+666 Pinch Visibility-Plane Lensing/

- **T4_PROPOSAL_NFW_for_the_B1938+666_Pinch_v1.md**  
  Path: `Gravity/B1938+666_Pinch_Visibility-Plane_Lensing/T4_PROPOSAL_NFW_for_the_B1938+666_Pinch_v1.md`
  *1. **T4 (Prereg)** — *VDM vs. NFW for the B1938+666 “Pinch”: a preregistered visibility‑plane lensing test**
  - **Experimental Setup**: Question. *Does a compact VDM Σ‑profile explain the B1938+666 pinch more convincingly than a truncated‑NFW subhalo on the same meter?* Instrument (T2). Visibility‑plane forward model ( \mathcal{M}(\Theta) ): macro lens + localized perturber + source brightness model → sky → Fourier sample on VLBI ((u,v)) points → complex vis residuals. This is treated as the measuring apparatus, with calibration tests and nulls. (Image‑plane versions are used only for quick smoke checks.) Parameters (required). * Cosmological distances (D_d,D_s,D_{ds}) (fixed to catalog values); critical density (\Sigma_{\rm...
  - **Diagnostics**: Question. *Does a compact VDM Σ‑profile explain the B1938+666 pinch more convincingly than a truncated‑NFW subhalo on the same meter?*
  - **Methods/Protocol**: Dimensionless set‑up. Rescale to ( \hat R !=! R/R_E), (\hat \Sigma !=! \Sigma/\Sigma_{\rm crit}), (\hat \alpha !=! \alpha/\theta_E). Predictions and gates are thus unit‑free (A6). Hypothesis tests and gates. *G1 (mass): Fit VDM & NFW classes independently with (m_{80}) soft‑prior; require (|\hat m_{80}-1|\le 0.05).* G2 (meter power): In a preregistered ROI around the pinch, require [ \frac{{\rm RMS}*{\rm ROI}(\text{VDM})}{{\rm RMS}*{\rm ROI}(\text{NFW})};\le;0.80 , ] computed over complex...
### Emergent Gravity for Strong-Lensing/

- **T3_PROPOSAL_Emergent_Gravity_for_Strong-Lensing_Substructure_v1.md**  
  Path: `Gravity/Emergent_Gravity_for_Strong-Lensing/T3_PROPOSAL_Emergent_Gravity_for_Strong-Lensing_Substructure_v1.md`
  ***T3→T4 — VDM Emergent Gravity for Strong‑Lensing Substructure (B1938+666‑class)***
  - **Experimental Setup**: State & equations (canon): Discrete action → KG branch (J‑only): [ \partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0,\quad c^{2}=2Ja^{2}. ] Overdamped RD (M‑limb): ( \partial_t \phi = D\nabla^{2}\phi + f(\phi) ). (Used for relaxation/seeding only—no external forces added.) **Effective lensing mapping (derived‑limit, *runtime only*):** We adopt the *thin‑lens, geometric‑optics* approximation as a *test meter*, not a new axiom. Light rays follow null geodesics of an effective metric functionally dependent on $\phi$; in the weak‑field/eikonal limit this reduces to a 2‑D potential $\psi$ on...
  - **Diagnostics**: (T2 instrument)
  - **Gate(s)**: KS $p>0.1$ and posterior overlap ≥0.5 with the nearest KG‑tube family.; $g_1,g_2\le 10^{-10}$ (refined), $\Delta S\ge0$ in M‑step; locality cone slope matches $c=\sqrt{2Ja^2}$ within 1%.; ΔlnZ ≥ +5 (decisive) or, minimally, ΔlnZ ≥ +3 (strong). ---
### Gravity Regression/

- **T5_PROPOSAL_Gravity_Regression_v1.md**  
  Path: `Gravity/Gravity_Regression/T5_PROPOSAL_Gravity_Regression_v1.md`
  *T5 (Pilot) - Gravity Regression — Weak‑Field VDM vs SPARC/Lensing Suites*
  - **Tier**: T5
  - **Diagnostics**: - **Inputs:** curated SPARC subset; preregistered lensing targets; priors on nuisance parameters. - **Diagnostics:** hold‑out predictive performance; residual structure; ΔAIC/ΔBIC; ΔlnZ; null predictions respected. - **Acceptance (gates):** (G1) ΔAIC ≤ 0 vs ΛCDM on prereg sets (tie/beat); (G2) decisive evidence on at least one lensing case (ΔlnZ ≥ +5); (G3) no locality/LIV gate violations from cor...


---

## Hierarchy (2 proposals)

- **T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md**  
  Path: `Hierarchy/T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md`
  *Formulate and prove (in 1D) that finite‑energy configurations under a tachyonic potential $(V''(0)<0)$ on large domains with stated BCs/regularity yield logarithmic hierarchy depth (N(L)=\Theta(\log(L/\lambda))) and boundary‑law excess energy $(E_{\mathrm{exc}}(L)=\Theta(L^{d-1}))$ (constant in 1D).*
  - **Tier**: T1
### STIV/

- **T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md**  
  Path: `Hierarchy/STIV/T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md`
  *1. **T2 (Instrument)** — **STIV Macrostate & Gradient‑Flow Meters for A8 Boundary Hierarchies***
  - **Diagnostics**: (g₁,g₂), grid invariance, model selection, and bootstrap CIs** are enforced. ---
  - **Methods/Protocol**: Scope banner: *T2 instrument calibration only; no phenomenon claim.* All A8 claims (G1–G12) remain governed by the separate T8 PROPOSAL. Datasets / testbeds. S1 Analytic shapes (2D/3D): disks, annuli, lattices of holes (Swiss‑cheese), extruded surfaces. Truth for area vs perimeter known → β_E oracle; α, α_{\mathcal I} computable from synthetic $I$ fields. S2 Static segmentations: synthetic hierarchical partitions with prereg $N(L)$ ground truth. S3 Dynamic fields (bench): small RD/KG clips from...
---

## Information (1 proposal)

- **PROPOSAL_SIE_Invariant_and_Novelty_v1.md**  
  Path: `Information/PROPOSAL_SIE_Invariant_and_Novelty_v1.md`
  *PROPOSAL_SIE_Invariant_and_Novelty_v1.md*
  - **Diagnostics**: ** two-grid error (E(\Delta t)), log–log slope; (Q)-drift time series with/without kick; recovery time....

---

## Intelligence Model (2 proposals)

- **PROPOSAL_Physics_Native_Intelligence_v1.md**  
  Path: `Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md`
  *Physics-Native Intelligence (VDM) — Substrate v1 Proposal*
  - **Diagnostics**: , adjust $\Delta t$, stencils, or boundary model; re-run under same tag with explicit FAILURE in gate matrix....
  - **Gate(s)**: . Success provides a stable base for subsequent routing, probe-only, and actuation phases, using shared scores and dimensionless knobs to test generality across domains....

- **T4_PROPOSAL_VDM_Physics_to_AI_Model_v1.md**  
  Path: `Intelligence_Model/T4_PROPOSAL_VDM_Physics_to_AI_Model_v1.md`
  *1. T4 (Prereg) — VDM Physics → AI Model Roadmap v1*
  - **Experimental Setup**: Domains covered - KG J-only substrate (T2/T3 instrumentation) - Metriplectic assisted-echo controllers (T4 prereg) - Thermodynamic routing meters (wave flux) - CMB-meter and T_CMB(z) check (cosmology instrument) - RD pulled-front complexity (new T4 instrument) Common grid/time - N ∈ {256, 512, 1024}, dx = 1.0 (canonical units) - Δt tied to CFL multiples {0.5, 1.0, 2.0} × CFL guard - Steps: 200 (sweeps use early-stop on gate fail) - Seeds: {1..12} Meters and gates used across domains (canon: Derivation/VALIDATION_METRICS.md) - Energy conservation drift: $\Delta E_\mathrm{RMS} =...
  - **Diagnostics**: Domains covered - KG J-only substrate (T2/T3 instrumentation) - Metriplectic assisted-echo controllers (T4 prereg) - Thermodynamic routing meters (wave flux) - CMB-meter and T_CMB(z) check (cosmology instrument) - RD pulled-front complexity (new T4 instrument) Common grid/time - N ∈ {256, 512, 1024}, dx = 1.0 (canonical units) - Δt tied to CFL multiples {0.5, 1.0, 2.0} × CFL guard - Steps: 200...
---

## Metriplectic (16 proposals)

- **PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md`

- **PROPOSAL_Metriplectic_Lindblad_T4.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_Lindblad_T4.md`
  - **Gate(s)**: ** saturation slope (\partial n/\partial N\to 0) beyond (n\simeq 1) (units set by your normalization) across (>90%) of modes tested....

- **PROPOSAL_Metriplectic_SymplecticPlusDG.md**  
  Path: `Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md`
  *Proposal: Metriplectic - Symplectic (KG) + Discrete-Gradient (RD)*
  - **Diagnostics**: . This program supplies rigorous, reproducible artifacts (JSON, CSV, PNG) under an approval-gated policy with tag-scoped schemas to support canon promotion and downstream integration....
  - **Gate(s)**: fails, route logs/figures under `failed_runs/`, emit a CONTRADICTION_REPORT with spec snapshot and control outcomes, and halt promotion to canon; iterate with controlled parameter adjustments (documented in decision log) before re-approval if the tag changes....

- **T1_PROPOSAL_QGT_to_Metriplectic_Instrument.md**  
  Path: `Metriplectic/T1_PROPOSAL_QGT_to_Metriplectic_Instrument.md`
  *T1 (Proto-model) — QGT → Metriplectic Instrument*
  - **Tier**: T1
  - **Gate(s)**: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md), [Derivation/code/common/io_paths.py](Derivation/code/common/io_paths.py:1)...

- **T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md**  
  Path: `Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md`
  *1. T4 — Counterfactual Echo Gain (CEG): A Metriplectic Assisted‑Echo Experiment in VDM*
  - **Tier**: T4

### Analog Horizon/

- **T5_PROPOSAL_Analog_Horizon_v1.md**  
  Path: `Metriplectic/Analog_Horizon/T5_PROPOSAL_Analog_Horizon_v1.md`
  *T5 (Pilot) - Analog Horizon — Telegraph‑Fisher Causality & Causal Dominance Meter*
  - **Tier**: T5
  - **Diagnostics**: - **Platform:** any medium realizing TF dynamics (electrical/acoustic meta‑lattice, BEC phononics). - **Knobs:** D via coupling; τ via relaxation network; J‑limb c from wave branch. - **Diagnostics:** cone slope (front arrival) and slack; TF dispersion; reproducibility across pulses. - **Acceptance (gates):** (G1) |c_TF/c_J − 1| ≤ 0.02; (G2) cone‑slack ≤ 2%; (G3) reproducibility across runs (Jacca...


### CEG Metric Definition/

- **T2_PROPOSAL_CEG_Metric_Definition_v1.md**  
  Path: `Metriplectic/CEG_Metric_Definition/T2_PROPOSAL_CEG_Metric_Definition_v1.md`
  *1. T2 (Instrument) — Corrective Echo Gain (CEG) Metric Definition and Validation*
  - **Experimental Setup**: Domains for validation: 1. Reaction-Diffusion (RD): 2D Fisher-KPP or Gray-Scott system with zero-flux boundaries. 2. Klein-Gordon J-only: 2D hyperbolic field with leapfrog integrator. 3. Metriplectic Assisted Echo: 1D telegraph-Fisher with Strang-split J/M composition and walker-mediated assistance. Parameters and defaults: - Grid: N ∈ {256, 512, 1024}, dx = 1.0 (canonical units) - Time step: Δt tied to CFL multiples {0.5, 1.0, 2.0} × CFL_max - Forward duration: T ∈ {100, 200, 500} steps - Seeds: 12 per condition (seed ∈ {1..12}) - Assistance budget (when applicable): λ ∈ {0.0, 0.1, 0.2, 0.3,...
  - **Diagnostics**: Domains for validation: 1. Reaction-Diffusion (RD): 2D Fisher-KPP or Gray-Scott system with zero-flux boundaries. 2. Klein-Gordon J-only: 2D hyperbolic field with leapfrog integrator. 3. Metriplectic Assisted Echo: 1D telegraph-Fisher with Strang-split J/M composition and walker-mediated assistance.
  - **Methods/Protocol**: Cartesian product of independent variables: - Regimes: {RD_fisher_kpp, KG_jonly, metriplectic_assisted_echo} - N: {256, 512, 1024} - Δt: {0.5, 1.0, 2.0} × CFL - T: {100, 200, 500} - λ (assistance): {0.0, 0.1, 0.2, 0.3, 0.5} (for metriplectic regime only) - Seeds: {1..12} Estimated runtime: - Per condition (single regime, N, Δt, T, seed): 1-5 minutes (CPU single thread) - Total conditions (excluding full Cartesian): ~100-200 runs (selective sampling) - Total compute budget: ~10-20 hours...
### CEG Metriplectic Assistance/

- **T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md**  
  Path: `Metriplectic/CEG_Metriplectic_Assistance/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md`
  *1. T4 — Counterfactual Echo Gain (CEG): A Metriplectic Assisted‑Echo Experiment in VDM*
  - **Experimental Setup**: State and splits. Domain $\Omega\subset\mathbb{R}^d$ (1D/2D) with field $W$ (KG for $J$; RD/gradient‑flow for $M$). Discrete action and updates from EQUATIONS registry; canonical constants from CONSTANTS registry. Integrator. Strang JMJ (or MJM as control): symplectic step for $J$; discrete‑gradient step for $M$. Diagnostics on each limb are enabled during both forward and reverse phases. Primary observable. Echo error $E \equiv \|q_{\text{final}}-q_0\|_{\mathcal{H}}$ in a declared discrete energy norm $\|\cdot\|_{\mathcal{H}}$ (per VDM discrete Hamiltonian density). CEG as above. Gates...
  - **Diagnostics**: provide the measurement substrate for the echo tests; e.g., the discrete action and Lagrangian/Euler–Lagrange structure (for $J$), and gradient‑flow RD updates (for $M$). These appear in the EQUATIONS registry used as the computational “instrument manual.”
  - **Methods/Protocol**: RP‑1 Baseline calibration (meters). Run J‑only reversibility, M‑only monotonicity, and Strang defect slope across the grid; must pass G1–G2–G4 before any assisted runs. (Artifacts posted with same‑basename CSV/JSON and figure captions that include slope/$R^2$ and seed/commit.) RP‑2 Assisted‑echo implementation. Insert a micro‑sequence during the reverse M‑segment using the internal $M$ estimator, with assistance parameter $\lambda$ and energy‑match clamp. Log assistance work, ensure G3. RP‑3...
### Constructive QGT to Metriplectic/

- **T1_PROPOSAL_G-QGT-1_QGT-to-Metriplectic_Mapping_v1.md**  
  Path: `Metriplectic/Constructive_QGT_to_Metriplectic/T1_PROPOSAL_G-QGT-1_QGT-to-Metriplectic_Mapping_v1.md`
  *G‑QGT‑1 — **Constructive QGT → Metriplectic Mapping** (T1, paper‑only)*
  - **Tier**: T1
  - **Diagnostics**: *Objects: (H(\lambda)), eigenframe (|u_n(\lambda)\rangle), (Q_{\mu\nu}), pushforward to observables, functionals (\mathcal I,\Sigma).* Diagnostics (paper‑only): algebraic checks for antisymmetry/PSD; explicit null‑space verifications for degeneracies; coordinate/gauge invariance notes.
  - **Gate(s)**: align to RESULTS standards.
### Contact Geometry Projection/

- **T1_PROPOSAL_G-CG-1_Contact-to-Metriplectic_v1.md**  
  Path: `Metriplectic/Contact_Geometry_Projection/T1_PROPOSAL_G-CG-1_Contact-to-Metriplectic_v1.md`
  *G‑CG‑1 — **Contact Geometry Projection → Metriplectic Split** (T1, paper‑only)*
  - **Tier**: T1
  - **Diagnostics**: verify (J^\top=-J), (M^\top=M\ge0), and the two degeneracies on chosen functionals (\Sigma,\mathcal I).
### Metriplectic Instruments/

- **T2_PROPOSAL_Metriplectic_Instruments_v1.md**  
  Path: `Metriplectic/Metriplectic_Instruments/T2_PROPOSAL_Metriplectic_Instruments_v1.md`
  *T2 (Instrument) - Metriplectic Instruments: Identity, KG, RD, and FRW Meters (EBN series)*
  - **Tier**: T2
  - **Diagnostics**: **KG J‑only meter.** Inputs: grid N, Δt, c, m, seeds. Diagnostics: dispersion fit (ω² vs k²), cone slope v. **Gates:** v ≤ c·(1+0.02); dispersion fit R² ≥ 0.999; Noether drifts ≤ 1e−12. **RD meter.** Inputs: D, r, λ (optional); measure c_front and σ(k). **Gates:** |c_obs/(2√(Dr))−1| ≤ 0.05 with R² ≥ 0.98; dispersion median rel‑err ≤ 1e−2. **Identity (metriplectic) meter.** Diagnostics: ΔL_h ≤ 0 pe...


### Schrodingerization KvN/

- **T1_PROPOSAL_Schrodingerization_KvN_v1.md**  
  Path: `Metriplectic/Schrodingerization_KvN/T1_PROPOSAL_Schrodingerization_KvN_v1.md`
  *T1 (Proto-model) - Schrödingerization (Koopman–von Neumann) Lifting of Metriplectic J ⊕ M to a Unified Hamiltonian Instrument*
  - **Diagnostics**: Known parameters (dimensionless normalization consistent with UNITS_NORMALIZATION.md): - Temporal step and horizon: $\Delta t$, $T$; grid sizes $N$, $\Delta x$. - Model knobs for baselines: $(c,m)$ for KG limb; RD coefficients $(D,r,u)$ for $M$-limb comparators. - KvN construction parameters: choice of basis/functions for $\lvert\psi\rangle$, truncation level $K$, projection operator family...
### Strang Defect vs dt kg RD/

- **PROPOSAL_KG_plus_RD_Metriplectic.md**  
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_KG_plus_RD_Metriplectic.md`
  *Proposal: KG ⊕ RD Metriplectic Experiment (Two-Field)*

- **PROPOSAL_Metriplectic_JMJ_RD_v1.md**  
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_Metriplectic_JMJ_RD_v1.md`
  *1. Metriplectic Integrator for Mixed Conservative-Dissipative Dynamics: Symplectic J-step ⊕ Discrete-Gradient M-step*
  - **Diagnostics**: reuse the RD harness just completed (two-grid order, fixed-$\Delta t$ $|\Delta S|$, Lyapunov monitors) **without modifying any prior scripts or outputs** to preserve reproducibility; new code paths are additive (new module/CLI only) and write to separate output folders. Success yields a scheme that ...

### TF Causality/

- **T1_PROPOSAL_TF_Causality_v1.md**  
  Path: `Metriplectic/TF_Causality/T1_PROPOSAL_TF_Causality_v1.md`
  *T1 (Proto-model) - Telegraph–Fisher (TF) Causality Instrument: Finite-Speed Transport and Cone Gates*
  - **Diagnostics**: Known parameters and normalization (per UNITS_NORMALIZATION.md): - Grid: $N$, $\Delta x$; time: $T$, $\Delta t$; seeds. - TF parameters: $\{D,\tau\}$; optional reaction term $f(u)$ for TF–Fisher variants (kept smooth, bounded). - Boundary/IC: periodic or reflecting; localized IC for front measurements; broadband small-amplitude IC for dispersion. Diagnostics (minimum set per run): - $c$ from...
  - **Gate(s)**: (i) dispersion fits with $R^2\ge 0.999$ matching predicted slope/intercept; (ii) locality cone with measured $v\le c(1+0.02)$; (iii) CFL/stability envelope checks. The design is compatible with metriplectic compositions (J⊕M), but this proposal limits scope to TF causality meters and cones....
### Void Debt Transport Throttle/

- **T1_PROPOSAL_Void_Debt_Transport_Throttle_v1.md**  
  Path: `Metriplectic/Void_Debt_Transport_Throttle/T1_PROPOSAL_Void_Debt_Transport_Throttle_v1.md`
  *T1 (Proto-model) - Void-Debt Transport Throttling Instrument: $c_{\mathrm{eff}}=c_0 \exp(-\tfrac{1}{2}\beta D)$ Gates*
  - **Diagnostics**: Normalization and parameters (per UNITS_NORMALIZATION.md): - Spatial grid: $N$, $\Delta x$; temporal: $\Delta t$, $T$; seeds $S$. - Transport regime: select either J‑only baselines (for $c_0$) or TF (for $c_0=\sqrt{D/\tau}$); optionally metriplectic compositions for stress‑tests. - Boundary detector settings: threshold $\theta$, scale pyramid levels $L_s$, morphological kernel sizes. Diagnostics...
---

## Nonequilibrium (2 proposals)

### GB Oscillating Load/

- **T2_PROPOSAL_GB_Oscillating_Load_v1.md**  
  Path: `Nonequilibrium/GB_Oscillating_Load/T2_PROPOSAL_GB_Oscillating_Load_v1.md`
  *1. T2 — GB Relaxation Meter under Oscillating Load (v1)*
  - **Tier**: T2
  - **Diagnostics**: into anchor‑referenced, gate‑enforced, and artifact‑audited routines. It advances sampling exactness and error accounting norms from lattice practice into materials‑like GB contexts within VDM....
  - **Gate(s)**: . Canonical equations are referenced by anchors only (VDM‑E‑160..164). Acceptance gates and thresholds are specified in the canonical metrics registry. All artifacts (PNG/CSV/JSON) are written via the IO helper with deterministic seeds and commit hashes recorded, enabling reproducible T2 instrument ...

### Self Organization/

- **T2_PROPOSAL_Self_Organization_Meters_v1.md**  
  Path: `Nonequilibrium/Self_Organization/T2_PROPOSAL_Self_Organization_Meters_v1.md`
  *T2 (Instrument) — Self-Organization Onset Meters (Nicolis–Prigogine)*
  - **Tier**: T2
  - **Diagnostics**: . It validates Excess-Entropy-Production (EEP) trend, leading-eigenvalue bifurcation cards with branch classification, localized-structure detection, and branch-stability overlays against canonical gates. Artifacts are emitted with PNG+CSV+JSON sidecars and contradiction routing on failure....
  - **Gate(s)**: diagnostics, and statistically sound error bars with autocorrelation awareness. VDM’s nonequilibrium meters adopt the same discipline: (i) EEP trend conformity near steady state, (ii) linear stability via leading eigenvalues with explicit sign changes in $\Re(\lambda_1)$ across control ladders, (iii...

---

## Qualia (2 proposals)

- **PROPOSAL_vdm_qualia_program.md**  
  Path: `Qualia/PROPOSAL_vdm_qualia_program.md`
  *VDM–Qualia Program: Coupled‑Field Explanations of Psychedelic Phenomenology (Sober Proxies)*
  - **Gate(s)**: gate:** $S$ vs gain shows sigmoid; defect density $\rho(t)$ fits $\rho_0 e^{-\kappa t}$ with $R^2>0.9$; $\kappa$ increases under stronger entrainment....

- **T3_PROPOSAL_Calibration_of_Psychophysical_Observables_to_C_Field.md**  
  Path: `Qualia/T3_PROPOSAL_Calibration_of_Psychophysical_Observables_to_C_Field.md`
  *1. **T3 — Calibration of Psychophysical Observables to the VDM (C)-Field***
  - **Experimental Setup**: Known parameters & defaults *Tasks (2–3): TOJ bias (ms), Cross‑modal projection (psychometric slope / ITPC), Dynamic texture spectrum ((1/f) exponent).* Sampling: within‑subject, (n \ge 20), two sessions ≥24 h apart (test–retest). *Hardware: calibrated display (60–144 Hz), headphones or vibrotactile motor, optional EEG (32ch).* Derived observables (\mathcal{O}*k): (\Delta t*{\mathrm{TOJ}}) bias, projection gain (\hat g), PSD exponent (\hat\beta); optional ITPC at drive frequency. * Forward model family: RD‑limit (C)-PDE or its 0‑D reduction, plus minimal readout maps...
  - **Diagnostics**: Known parameters & defaults *Tasks (2–3): TOJ bias (ms), Cross‑modal projection (psychometric slope / ITPC), Dynamic texture spectrum ((1/f) exponent).* Sampling: within‑subject, (n \ge 20), two sessions ≥24 h apart (test–retest). *Hardware: calibrated display (60–144 Hz), headphones or vibrotactile motor, optional EEG (32ch).* Derived observables (\mathcal{O}*k): (\Delta t*{\mathrm{TOJ}})...
  - **Gate(s)**: ≤500 LOC/file; no outer→inner deps; interfaces for cross‑layer calls; tests mirror source paths; domain/business logic framework‑free. ---; (Pass/Fail) *Reliability: (\mathrm{ICC}(\text{C‑features; day1 vs day2}) \ge 0.8).* Predictive validity: held‑out RMSE ≤ 5% (block design). *Identifiability: Hessian condition number (\kappa \le 10^3); (\mathrm{CI}_{A,\tau}<30%).* Convergent/discriminant: tasks designed to correlate must show...
---

## Quantum (11 proposals)

- **T0_PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md**  
  Path: `Quantum/T0_PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md`
  ***PROPOSAL — VDM J‑branch QFT Bootstrap & Metriplectic Decoherence (v1)***
  - **Tier**: T0
  - **Experimental Setup**: Domain routing. Figures → `Derivation/doce/physics/outputs/figures/quantum/` Logs (CSV/JSON) → `Derivation/doce/physics/outputs/logs/quantum/` Minimum artifact set per run (code‑enforced): 1. PNG dashboard, 2) metrics CSV, 3) summary JSON (with commit, salted self‑hash, code‑hash list, proposal name, gate verdicts, overall verdict). Planned file names (example tag `qft-metro-v1`) *`Derivation/doce/physics/outputs/figures/quantum/2025_qft-metro-v1_dashboard.png`* `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-v1_metrics.csv` *...
  - **Diagnostics**: (for T1→T2)
  - **Methods/Protocol**: T1 (Proto‑model) — Scalar‑only instrument shakedown *Simulate free scalar on 1D/2D periodic lattice.* Estimate ( \omega(k) ) from timeseries; fit to analytic dispersion. *Serialize artifacts to the paths listed above. T2 (Instrument) — Scalar → Dirac + metriplectic coupling* Add staggered or Wilson fermion discretization; verify massless/massive dispersion and control of doublers. *Add metriplectic/Lindblad term with coupling ( \gamma ); measure purity decay vs ( \gamma ).* Perform 2× and...
- **T1_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence__ProtoModel_v1.md**  
  Path: `Quantum/T1_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence__ProtoModel_v1.md`
  *1. Tier Grade, Proposal Title and Date*
  - **Diagnostics**: Domain routing (enforced by `io_paths.py`): *Figures (PNG): `Derivation/doce/physics/outputs/figures/quantum/`* Logs (CSV/JSON): `Derivation/doce/physics/outputs/logs/quantum/`
- **T2_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence_Instrument_v1.md**  
  Path: `Quantum/T2_PROPOSAL_VDM_J-branch_Metriplectic_Decoherence_Instrument_v1.md`  
  *(File is empty or could not be parsed)*
- **T4_PROPOSAL_J-to_Dirac_v1.md**  
  Path: `Quantum/T4_PROPOSAL_J-to_Dirac_v1.md`
  *1. T4 (Prereg) - T4 — J→Dirac‑Aligned False‑Vacuum Metastability & Void‑Debt Asymmetry (Preregistration v1)*
  - **Experimental Setup**: Fields & functionals (minimal working form). β‑field with tilted double‑well potential \( V_\beta(\beta)=\tfrac{\lambda}{4}(\beta^2-v^2)^2+\epsilon\,\beta \) with small tilt \(\epsilon\); announcer fields \(\mathcal A\) mediate currents; an optional conserved B‑charge current \(J_B^\mu\). Two asymmetry routes are preregistered: (i) add \(\mu_B J_B^0\) (grand‑canonical bias); (ii) couple \(\beta\) to announcer curvature via a Chern–Simons–type term with coefficient \(\kappa_{CP}\). Action/entropy are schematic: \[\mathcal I[q]=\int (|\nabla\beta|^2 + V_\beta + \mathcal L_\mathcal A + \mathcal...
  - **Diagnostics**: Fields & functionals (minimal working form). β‑field with tilted double‑well potential \( V_\beta(\beta)=\tfrac{\lambda}{4}(\beta^2-v^2)^2+\epsilon\,\beta \) with small tilt \(\epsilon\); announcer fields \(\mathcal A\) mediate currents; an optional conserved B‑charge current \(J_B^\mu\). Two asymmetry routes are preregistered: (i) add \(\mu_B J_B^0\) (grand‑canonical bias); (ii) couple \(\beta\)...
  - **Gate(s)**: fit \(R_c=K\,\sigma/\Delta V\) with \(R^2\ge 0.99\) and \(|K/\kappa_d-1|\le 0.15\). *Work/energy check: \(W(R)\) shows extremum at \(R_c\); derivative zero within tol; curvature sign correct. fileciteturn1file18; exponential fit \(R^2\ge 0.99\); KS p\(>0.1\) on tail; CI for \(\Gamma\).* Resolution robustness: doubling spatial resolution changes \(\Gamma\) by \(<10\%\); CI excludes \(\ge 10\%\) change. fileciteturn1file10; \(\langle\Delta Q_B\rangle_{\mu_B>0}-\langle\Delta Q_B\rangle_{0}\ge\delta_Q\) with 95% CI excluding 0 (\(\delta_Q\) set by pilot). * CP‑pumping route: with \(\kappa_{CP}\neq 0\), moving walls pump \(Q_B\). Gate: slope \(d\langle\Delta Q_B\rangle/d\kappa_{CP}>0\) with 95% CI; sign flips under...
  - **Methods/Protocol**: 1) Meters first (tiny grids). Reversibility ≤ \(10^{-12}\); operator/BC match; determinism receipts; (if M) H‑theorem micro‑tol. 2) Thin‑wall pilot. Measure \(\sigma\), \(\Delta V\); seed bubbles to bracket \(R_c\); size \(\Delta t\) ladder. 3) Lifetime pilot. 50–100 seeds; validate exponential tail and set floors. 4) Asymmetry pilot. Small \(\mu_B\) or \(\kappa_{CP}\) sweep; estimate \(\delta_Q\) and slope; finalize gates. 5) Full prereg execution. Run prereg seeds/horizons; compute...
### Analog Quantum/

- **T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md**  
  Path: `Quantum/Analog_Quantum/T4_PROPOSAL_Cold_Atom_Causal_Cone_Test_v1.md`
  *1. T4 (Prereg) — Cold-Atom Test of VDM Causal Cone in Metriplectic Optical Lattice*
  - **Experimental Setup**: System: - 2D optical lattice (square geometry preferred for symmetry) - Ultracold Bose gas (e.g., $^{87}$Rb or $^{39}$K) in Mott insulator or superfluid regime - Quantum-gas microscope with site-resolved imaging (spatial resolution ≤ 1 lattice spacing) - Engineered dissipation: Local atom loss (via resonant light), local dephasing (via AC Stark shift noise), or measurement back-action Parameters and defaults: - Lattice depth: $V_0 \sim 10-20 E_R$ (tunable to control tunneling $J$ and on-site interaction $U$) - Filling: $n \sim 1$ atom/site (Mott regime) or $n < 1$ (superfluid regime) - Quench...
  - **Diagnostics**: System: - 2D optical lattice (square geometry preferred for symmetry) - Ultracold Bose gas (e.g., $^{87}$Rb or $^{39}$K) in Mott insulator or superfluid regime - Quantum-gas microscope with site-resolved imaging (spatial resolution ≤ 1 lattice spacing) - Engineered dissipation: Local atom loss (via resonant light), local dephasing (via AC Stark shift noise), or measurement back-action
  - **Methods/Protocol**: Conditions: - Dissipation: {OFF (baseline), ON (Γ = 0.1J, 0.5J, 1.0J)} - Lattice depth: {10, 15, 20} $E_R$ (testing robustness across $J$ values) - Time points: {0, 5, 10, 20, 50, 100} × $J^{-1}$ - Repetitions: $N_{\text{rep}} = 50$ per condition Total runs: ~20 conditions (4 dissipation × 3 depths, with some prioritization) Estimated runtime: - Per time point per condition: 10-30 minutes (including equilibration, quench, imaging, readout) - Total: ~40-80 hours (experiment-dependent; can be...
### Quantum Echos/

- **T0_PROPOSAL_SIE_Willow-Convergence_v1.md**  
  Path: `Quantum/Quantum_Echos/T0_PROPOSAL_SIE_Willow-Convergence_v1.md`
  *T0 PROPOSAL_SIE_Willow-Convergence_v1.md*
  - **Experimental Setup**: Domain string (for routing): `quantum` Runner (suggested path; you may rename): `Derivation/doce/physics/code/runners/quantum/sie_willow_convergence_v1.py` I/O routing (via `io_paths.py`): *Figure (PNG): `Derivation/doce/physics/outputs/figures/quantum/sie_willow_convergence_v1_timeseries.png`* Metrics (CSV): `Derivation/doce/physics/outputs/logs/quantum/sie_willow_convergence_v1_metrics.csv` * Summary (JSON): `Derivation/doce/physics/outputs/logs/quantum/sie_willow_convergence_v1_summary.json` Mandatory JSON fields (enforced by runner): ```json { "proposal_name":...
  - **Diagnostics**: Domain string (for routing): `quantum`
  - **Methods/Protocol**: 1. Initial approval request. Create an approval record for this run tag: *Domain: `quantum`* Tag: `sie_willow_convergence_v1` * Approval record path (text/JSON, committed with this PROPOSAL): `Derivation/doce/physics/approvals/requests/sie_willow_convergence_v1.request.json` Minimal content: ```json { "proposal": "PROPOSAL_SIE_Willow-Convergence_v1.md", "domain": "quantum", "tag": "sie_willow_convergence_v1", "requested_by": "Justin K. Lietz", "requested_at_utc": "<ISO-8601>", "status":...
- **T1_PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md**  
  Path: `Quantum/Quantum_Echos/T1_PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md`
  *PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md*
  - **Experimental Setup**: Domain: `qis` (quantum‑information‑style echo testbed) Outputs (managed by `io_paths.py`): *Figures dir (canonical): `Derivation/code/physics/outputs/figures/qis/`* Logs dir (canonical): `Derivation/code/physics/outputs/logs/qis/` Required output artifacts (minimum): 1. PNG figure — timeseries & gate summaries `Derivation/code/physics/outputs/figures/qis/{RUN_ID}_echo_timeseries_{TAG}.png` 2. CSV metrics — per‑step metrics for all gates `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_metrics_{TAG}.csv` 3. JSON summary — provenance + PASS/FAIL per gate and overall...
  - **Diagnostics**: Domain: `qis` (quantum‑information‑style echo testbed)
  - **Gate(s)**: (PASS/FAIL; all must pass):** *G0: Initial Approval Gate — summary JSON includes `approval: {status:"APPROVED", approver, timestamp_utc}`*(Your `approval.py` step writes this to the same logs dir as the run: `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_approval_{TAG}.json` and the runner...
  - **Methods/Protocol**: Forward–Echo protocol (single trial): 1. Forward‑1: Integrate for (T_f) with full metriplectic flow. Record `baseline_err_pre`. 2. Echo: Apply echo sequence for (T_e): reverse conservative generator ( J \mapsto -J ) (or scripted time‑reversal), maintain/adjust (M) per config. 3. Forward‑2: Resume nominal flow for (T_f). Record `baseline_err_post`. 4. Metrics: *Echo Fidelity on an overlap window ([t_0, t_0+\Delta]): [ F_{\mathrm{echo}} ;=; 1 - \frac{|u_{\mathrm{pre}}(t)-u_{\mathrm{post}}(t)|*2}...
- **T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md**  
  Path: `Quantum/Quantum_Echos/T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md`
  *1. Tier Grade, Proposal Title and Date*
  - **Experimental Setup**: Governing fields. *$J$ limb (reversible): $\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0$, $c^2=2Ja^2$.* $M$ limb (agency): $\partial_t C = D\nabla^2 C - \gamma C + S(\phi,\dot\phi,\nabla\phi)$; canonical source structure follows VDM agency definitions. Metriplectic split (A4). $\partial_t q = J(q),\delta \mathcal I/\delta q + M(q),\delta \Sigma/\delta q$ with degeneracies; diagnostic invariants $g_1,g_2$ are computed to verify $J,\delta\Sigma=0$, $M,\delta\mathcal I=0$ to tolerance. Dimensionless program (A6). Use $\tilde t=\gamma t$, $\tilde x=x/\ell_D$, $\ell_D=\sqrt{D/\gamma}$...
  - **Diagnostics**: for KG (cone slope $\approx c$), Noether/H‑theorem monitors, dimensionless scaling program (A6). This proposal (T4) preregisters a falsifiable causality claim using those meters.
  - **Methods/Protocol**: Plan to employ resources. 1. Calibrate meters (RD dispersion/front; KG locality; agency update stability). 2. Run $J$‑only echo window sanity to pin $c$ and Noether drift. 3. Activate $J\oplus M$ coupling with preregistered $S(\cdot)$; execute impulse and collect $C$ fields. 4. Compute arrival and front metrics; produce cone plots in $(r/(ct),C)$ space. 5. Sweep grid/time resolutions and seeds; repeat with altered $D,\gamma$ to test dimensionless collapse. Runtime estimate & datasets....
- **T4_PROPOSAL_SMAE_CEG_v1.md**  
  Path: `Quantum/Quantum_Echos/T4_PROPOSAL_SMAE_CEG_v1.md`
  *1. Tier Grade, Proposal Title and Date*
  - **Tier**: T4
  - **Experimental Setup**: System. 1D/2D lattice; JMJ Strang composition with established RD/KG meters (front speed, dispersion, Noether). No body forces, local operators only. AMD stack (VDM rule). Forward pass. J(Δt/2) → M(Δt) → J(Δt/2) for horizon T, with a localized “walker” perturbation mid‑run. Reverse pass (baseline). Same scheme, −Δt, no assistance. Reverse pass (assisted). Insert a tiny corrective micro‑sequence informed by the internal J/M model to pre‑compensate dissipation/commutator defects. Budget: ∑(assist work) = ∑(baseline work). Observables. * Echo errors: E_baseline, E_assisted in a VDM‑standard norm...
  - **Diagnostics**: System. 1D/2D lattice; JMJ Strang composition with established RD/KG meters (front speed, dispersion, Noether). No body forces, local operators only. AMD stack (VDM rule).
  - **Gate(s)**: (G1) J‑Noether drift ≤ pre‑registered envelope; (G2) M‑step entropy non‑increase (discrete H‑theorem) holds; (G3) assistance is energy‑matched to baseline. *Causality checks: Ablate self‑model (scramble J, scramble M); CEG → 0 under ablation.* Generalization: modest sweep over loss depth and step...; (i) Noether drift (J‑only runs and in JMJ segments), (ii) Lyapunov/entropy monotonicity per M‑step (discrete gradient gate), (iii) energy budget equality (assist vs baseline). *Ablations: scramble J (e.g., permuted couplings), scramble M (e.g., perturbed metric), recompute CEG.* Artifacts:...; (i) conservation drift within preset J‑drift envelope, (ii) non‑increase of entropy in each M step, (iii) equal energy budgets. PASS requires CEG>0 across seeds and ablations that destroy the self‑model eliminate the gain (causal). If successful, SMAE upgrades the VDM “echo with intent” from...
  - **Methods/Protocol**: High‑level plan. 1. Meter certification reuse. Confirm RD front speed/dispersion and J‑only Noether/dispersion remain PASS on the exact grid/Δt to be used (spot checks only). 2. Baseline echo. Acquire E_baseline and gate metrics on N_seeds (e.g., 25). 3. Assisted echo. Insert the micro‑sequence (same budget); acquire E_assisted and gates on identical seeds. 4. Primary decision. Compute CEG per seed; report median, CI; perform ablations (J‑scramble, M‑scramble) and recompute. 5. Sweep. Small...
- **T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md**  
  Path: `Quantum/Quantum_Echos/T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md`
  *Convergence Note (motivation-first)*
  - **Experimental Setup**: State & flow. Discretize $z\in\mathbb{R}^d$ on a cubic lattice (periodic), Strang‑split the flow into $J$ and $M$ steps. Echo cycle length: $T_e$. Core equations (discrete): - Reversible (symplectic) step: $z^{n+\frac12} = \Phi_J^{\Delta t}(z^n)$ (symplectic integrator). - Dissipative step (gradient flow): $z^{n+1} = z^{n+\frac12} - \Delta t\, M(z^{n+\frac12})\,\nabla S(z^{n+\frac12})$. - Echo map: $\mathcal{E} = \Phi_J^{\Delta t}\circ \Phi_M^{\Delta t}\circ \Phi_J^{-\Delta t}$. Diagnostics (all recorded to CSV & JSON): - Fidelity gain per cycle: $\Delta F_k := F_{k}-F_{k-1}$, with $F_k =...
  - **Diagnostics**: State & flow. Discretize $z\in\mathbb{R}^d$ on a cubic lattice (periodic), Strang‑split the flow into $J$ and $M$ steps. Echo cycle length: $T_e$.
  - **Methods/Protocol**: Plan. For each seed and noise level, run $K$ echo cycles (e.g., $K=256$), record $(F_k,\Delta H_k,S_k)$, compute gates, emit artifacts with hashes. Runtime. CPU; ~{N} minutes per seed × {S} seeds × {levels} noise settings. Success path. All gates pass; publish artifacts & JSON; promote to T5 pilot. Failure path. Post CONTRA_REPORT.md with the failing gate, measured values, and a minimal counterexample seed; file a remediation issue. Publication / display. PNG shows $F_k$ trajectories and drift...
### Quantum Engine/

- **T4_PROPOSAL_Quantum-Resource-Engine_v1.md**  
  Path: `Quantum/Quantum_Engine/T4_PROPOSAL_Quantum-Resource-Engine_v1.md`
  ***T4 — Quantum‑Resource Engine: A Metriplectic Ledger to Test “Beyond‑Carnot” Efficiencies***
  - **Diagnostics**: State & symbols (VDM canon). We use the canonical notation sheet for fields, fluxes, and ledger variables; Noether energy/flux diagnostics anchor the J‑leg.
  - **Gate(s)**: PASS/FAIL is mechanical. *Entropy lemma (M‑only): Discrete gradient update yields ( \mathcal L^{n+1}-\mathcal L^n = -\Delta t\lVert(\phi^{n+1}-\phi^n)/\Delta t\rVert_2^2\le 0) in RD‑like tests, validating our dissipative monitor (background QC instrument).* Noether lemma (J‑only): Energy/flux...
---

## Quantum Gravity (3 proposals)

- **PROPOSAL_Dark_Photon_Bridge.md**  
  Path: `Quantum_Gravity/PROPOSAL_Dark_Photon_Bridge.md`
  *Quantum Gravity Bridge - Proposal (v1)*
  - **Gate(s)**: -first discipline. The immediate aim is to construct reproducible pipelines that (i) propagate VDM-consistent FRW backgrounds and perturbations into linear observables, and (ii) scope dark-photon kinetic-mixing constraints via detector noise budgets and quick Fisher estimates with finite-difference ...

- **PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md**  
  Path: `Quantum_Gravity/PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md`
  *VDM ↔ Quantum-Gravity Bridge: Causal Geometry and Holonomy Tests*
  - **Diagnostics**: ) as **gates**. Passing these gates would establish that VDM realizes a micro-causal, hyperbolic geometry consistent with a causal-set-like substrate while supporting gauge-like loop transport—an essential bridge to research-grade quantum-gravity programs without importing them as axioms....
  - **Gate(s)**: **. Passing these gates would establish that VDM realizes a micro-causal, hyperbolic geometry consistent with a causal-set-like substrate while supporting gauge-like loop transport—an essential bridge to research-grade quantum-gravity programs without importing them as axioms....

- **T2_PROPOSAL_QG_Regge_CDT_v1.md**  
  Path: `Quantum_Gravity/T2_PROPOSAL_QG_Regge_CDT_v1.md`
  *) Where VDM already overlaps “string‑like” physics*
  - **Diagnostics**: just as you do now. * A7 Measurability: every claim maps to an observable (balance residuals, spectral proxies, scaling exponents) with thresholds in RESULTS docs. ---
---

## Spinor (1 proposal)

- **T1_PROPOSAL_Spinor_Emergence_v1.md**  
  Path: `Spinor/T1_PROPOSAL_Spinor_Emergence_v1.md`
  *T1 (Proto-model) - Spinor Emergence from the VDM J‑Limb (Dirac Sector from a Scalar Void Lattice)*
  - **Tier**: T1
  - **Gate(s)**: ** Linearization of the discrete Euler–Lagrange equation around an interface produces a first‑order Dirac operator for the bound mode manifold up to controlled remainders; dispersion linear near k=0....

---

## Tachyon Condensation (1 proposal)

- **PROPOSAL_Tachyonic_Tube_Condensation.md**  
  Path: `Tachyon_Condensation/PROPOSAL_Tachyonic_Tube_Condensation.md`
  *Tachyonic Tube Condensation and Spectrum (Proposal)*
  - **Diagnostics**: Parameters: $\mu$, $\lambda$, $c$, $\ell_{\max}$. Diagnostics: (a) root-finding convergence counts, (b) per-mode $\kappa_\ell$, $N4_\ell$, $v_\ell$, $M_\ell^2$, (c) energy scan $E(R)$ and minima statistics. Artifacts: spectrum CSV per tag, condensation summary JSON, energy scan figure + CSV. Scripts...
  - **Gate(s)**: root solver success fraction $>95\%$ (finite rows present for $\ell=0..\ell_{\max}$ except tolerable misses at high $\ell$ when $R$ small)....

---

## Thermodynamic Routing (7 proposals)

- **PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md**  
  Path: `Thermodynamic_Routing/PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md`
  *PROPOSAL_Thermodynamic_Routing_NoSwitch_v2.md*
  - **Gate(s)**: emits `CONTRADICTION_REPORT__{tag}.json` with per-seed distributions, geometry masks, collapse logs, and RJ residuals....

### Passive Thermodynamic Routing/

- **PROPOSAL_Flux_Through_Memory_Channels_v1.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Flux_Through_Memory_Channels_v1.md`
  *Flux Through Memory Channels (Frozen Landscape) — Passive Thermodynamic Routing v2 (Pre‑Registration)*
  - **Diagnostics**: - Domain & BCs: 2‑outlet geometry; reflecting sidewalls; open right boundary with two outlet segments A/B. Port closure ablation yields zero outflux by construction....
  - **Gate(s)**: $\eta_{\rm ch} \ge \theta$ and 95% CI excludes the geometry‑only null. ($\theta$ to be set from pilot; target $\ge 0.60$ for strong maps.)...

- **PROPOSAL_Passive_Thermodynamic_Routing_v2.md**  
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md`
  *PROPOSAL: Passive Thermodynamic Routing v2 (Pre-Registration)*
  - **Diagnostics**: in a post-collapse window uses modal occupancies $\langle |c_k|^2\rangle$ over Laplacian eigenpairs $-\Delta \psi_k = \lambda_k\,\psi_k$ with the fit...
  - **Gate(s)**: d diagnostics for the J⊕M coupling limb. No parameter tuning post hoc; windowing and masks are predeclared....

### Prereg Biased Main/

- **PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md**  
  Path: `Thermodynamic_Routing/Prereg_Biased_Main/PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md`
  *PROPOSAL: Thermodynamic Routing v2 — Prereg Biased Main*
  - **Diagnostics**: (Durbin–Watson, Ljung–Box(5), ρ₁), routing bias must exhibit nonzero B and ρ with 95% CI excluding 0 meeting a preregistered margin δ, the energy-floor witness must beat a local baseline by ≥ 5σ, and robustness checks (injection-site slope CI≠0, two-source |Δη_route| ≤ 5%) must pass. Artifacts and J...
  - **Gate(s)**: enforced. The metric (DG) step must satisfy the H-theorem (ΔL_h ≤ 0), no-switch identity must hold bitwise or within ∞-norm ≤ 1e−12, the RJ spectral fit must achieve R² ≥ 0.99 on a predeclared band and time window with residual whiteness diagnostics (Durbin–Watson, Ljung–Box(5), ρ₁), routing bias mu...

### Wave Flux Meter/

- **PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md`
  - **Diagnostics**: ), A6 (dimensionless/scale program), A7 (measurability). Use their built‑in QC gates (Noether drift, Strang‑defect order checks, Lyapunov/H‑theorem) as acceptance tests....
  - **Gate(s)**: , and gives you ready‑to‑fill proposal stubs that align with your repository’s Tier ladder and writing standards....

- **PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`
  *Proposal: Wave Flux Meter — Phase B (Open-Ports with Absorber) v1*

- **PROPOSAL_Wave_Flux_Meter_v1.md**  
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md`
  *Proposal: Wave Poynting-Meter Instrument v1 (Thermodynamic Routing — Photonic Track)*
  - **Gate(s)**: $$\max_t \frac{|E(t)-E(0)|}{E(0)} \le 10^{-6}$$ over ≥100 periods; time-reversal error ≤ $10^{-12}$....

---

## Thermodynamics (1 proposal)

### Convection/

- **T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md**  
  Path: `Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md`
  *T2 — A Rayleigh–Bénard Onset Gate (“RB‑Gate”) for Deep‑M Limb Convection Solvers*
  - **Tier**: T2
  - **Gate(s)**: ** that detects the onset of Rayleigh–Bénard convection (RBC) in Deep‑M limb solvers by comparing the **measured** dynamics against **theoretical** onset thresholds for $\mathrm{Ra}$ and $k_c$, with machine‑actionable preregistration, artifacts, and validation metrics....

---

## Topology (2 proposals)

- **PROPOSAL_Loop_Quench_Test_Robustness_v2.md**  
  Path: `Topology/PROPOSAL_Loop_Quench_Test_Robustness_v2.md`

- **PROPOSAL_Loop_Quench_Test_v1.md**  
  Path: `Topology/PROPOSAL_Loop_Quench_Test_v1.md`
  *PROPOSAL_Loop_Quench_Test_v1.md*
  - **Diagnostics**: ** Kendall (\tau) between loop count and (-\Delta L_h); loop lifetime histogram; budget residual sanity....

---

## Transport (1 proposal)

### Telegraph From Relaxation/

- **T1_PROPOSAL_Telegraph_From_Relaxation_v1.md**  
  Path: `Transport/Telegraph_From_Relaxation/T1_PROPOSAL_Telegraph_From_Relaxation_v1.md`
  *T1 (Proto-model) - Telegraph From Relaxation Instrument*
  - **Gate(s)**: Let runs sweep $(D,\tau)$ over a grid and compute $(\hat c, D, \tau)$ tuples. Primary gate (speed law): - Fit $\log \hat c$ vs $\tfrac12(\log D - \log \tau)$: - Slope $\hat s$ within $[0.95, 1.05]$ - $R^2 \ge 0.98$ Secondary gates (stability and repeatability): - Across seeds, coefficient of...
---

