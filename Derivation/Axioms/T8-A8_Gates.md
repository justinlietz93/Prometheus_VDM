# Technical Summary Report

**Generated on:** November 3, 2025 at 12:53 AM CST

---

## Canon pointers (authoritative sources)

- Primary gates: [T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md](Axiom-8/Status/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md)
- Single-file outline: [T8-A8_Derivation_hierarchy_A8_SINGLE_FILE_OUTLINE_Version2.md](Axiom-8/Status/T8-A8_Derivation_hierarchy_A8_SINGLE_FILE_OUTLINE_Version2.md)
- This file compiles the gates for convenience; if any discrepancy exists, the Proposal/Outline govern as single sources of truth.

## Generated Summary

Here are the extracted constraints and requirements from the provided document segment, categorized as requested:

### Must-have (non-negotiable)

- **T0 — Concept Seed Requirements:**
  - A concept seed must include a statement and motivation.
  - A concept seed must declare target branch tag(s).
  - A concept seed must sketch one falsifiable consequence.
  - For promotion to T1, one must identify state, controls, and observables.
  - For promotion to T1, one must cite relevant axioms/equations anchors.
- **T1 — Toy Formalization Requirements:**
  - Formalization must use minimal math/simulation.
  - Formalization must link to AX-001..004 and EQUATIONS used.
  - Formalization must include a risks/assumptions list.
  - For promotion to T2, one must choose meter(s), KPIs, and QC checks.
  - For promotion to T2, one must specify branch‑specific gates.
- **T2 — Meter (Instrument) Calibrated Requirements:**
  - One must calibrate instruments before claiming phenomena.
  - Metriplectic split degeneracy diagnostics (g₁,g₂) must be ≲ 10⁻¹⁰ at grid‑refined tolerance when applicable (cross‑branch invariant).
- **T3 — Smoke Test Requirements:**
  - One must perform a small demo with the T2 meter.
  - One must predeclare no novelty if the test is QC‑only.
  - Pass/fail results must be logged with margins.
- **T4 — Preregistered Hypothesis Requirements:**
  - Hypotheses, nulls, effect sizes, CI thresholds, analysis windows, and contradiction routing must be locked.
- **T5 — Pilot Execution Requirements:**
  - Execution must use a narrow grid/time.
  - One must verify power & CI handling.
- **T6 — Main Execution Requirements:**
  - Execution must be a full preregistered run.
  - KPIs, CIs, and ablations must be reported.
- **T7 — Robustness Requirements:**
  - One must perform parameter sweeps, stepper variants, and resolution scaling.
  - One must track degradation versus meters.
- **T8 — Out-of-Sample Prediction Requirements:**
  - One must report hit‑rate or quantitative error on previously unseen systems/datasets.
  - For Agency, one must include cross‑substrate tests.
- **T9 — External Reproduction Requirements:**
  - An independent team must reproduce T6–T8 results.
  - Artifacts and preregistration must be open.
- **Global Tier Invariants (Tiers ≥T2):**
  - A0–A7 compliance must be cited.
  - Measurable observables (A7) must be present.
  - Scope banners (“meter testing, not phenomenon”, “no novelty claim”) must be used.
  - Transparent gates must be provided.
- **VDT Axioms & Design Constraints:**
  - The VDM framework must be formally closed (A0).
  - A field $\Psi(x,t)$ must be the fundamental carrier (A1).
  - Dynamics must be built from local functionals; influence must propagate finitely (A2).
  - Finite domain-of-dependence (cone) must be asserted and tested only for the hyperbolic (J-only KG) limb or for an explicitly flagged hyperbolic RD regularization (A2).
  - Noether currents derived from symmetries must be conserved (A3).
  - Noether currents must be checked numerically in the KG runner; totals drift must be $\le 10^{-8}$/period (A3).
  - Metriplectic split must use dual generators $J(q)$ (antisymmetric) and $M(q)$ (symmetric positive semidefinite), with degeneracies $J\,\frac{\delta\Sigma}{\delta q}=0$ and $M\,\frac{\delta\mathcal I}{\delta q}=0$ (A4).
  - Metriplectic degeneracy diagnostics ($g_1, g_2$) must be $\le 10^{-10}$ (grid-refined) every K steps (A4).
  - The entropy functional $\Sigma[q]$ must be non-decreasing along trajectories (A5).
  - Predictions must be formulated in dimensionless groups; units themselves must carry no physical claims (A6).
  - Every nontrivial statement must map to concrete observables with a test protocol (falsifiable) (A7).
- **A8 Axiom Candidate Promotion Rule:**
  - On PROPOSAL T8 PASS (G1–G8), the statement must be copied verbatim into `Canon/AXIOMS.md` as **A8**.
  - The status in the proposal document must be updated to **ACCEPTED**.
  - Artifacts must be archived under `Derivation/code/outputs/axioms/a8_infinity_resolution/`.

### Bench isolation and metriplectic hygiene (A8 updates 2025-11-03)

- Bench isolation (no runtime coupling): A8 benches must be physics‑bench native; do not import from `fum_rt/`. Place A8 tools under `Derivation/code/physics/hierarchy/...` with meters under `.../meters/`. Any runtime data may be ingested only via read‑only ETL after bench‑native meters exist and must not be a dependency for A8 validation.

- Two‑grid order QC (composition meters): Where an instrument claims an order, require two‑grid slope ≥ 2.90 with R² ≥ 0.999 (Strang‑defect gate) and report the fit in artifacts.

- Anisotropy/morphometry control (boundary metrics): Use Minkowski functionals or structure‑tensor analysis and, where applicable, deconvolution to rule out grid‑aligned artifacts in boundary orientation distributions; document masks and procedures.

- CI/FDR accounting (bundle gates): Bootstrap CIs for α, α_I, β_E, and N(L) slopes; when evaluating gate bundles, apply FDR control and include q‑values in PASS/FAIL tables.

- Cone clause reinforcement (A2 scope): Finite‑speed cone assertions are permitted only on KG (J‑only) or explicitly hyperbolic RD (Telegraph–Fisher) benches. RD‑only runs may claim front‑speed/dispersion, not cones.
- ε‑tube selection policy (A8 boundary metrics): preregister the rule to choose ε (e.g., half‑max of |∇φ| peak width or a spectral roll‑off method), sweep ε and report plateau regions with CIs; grade α, α_I only on a preregistered plateau window.
- Area‑law model selection (β_E): fit both E_exc(L) ∝ L^{d−1} and E_exc(L) ∝ L^{d}; report ΔAIC/ΔBIC; require R² ≥ 0.98 and |β_E − (d−1)| &lt; 0.10 with CI not straddling d.
- A5 sign convention (global): enforce a unified sign across docs/meters. Prefer ΔΣ ≥ −tol per M‑update; if reporting a Lyapunov free‑energy F instead, enforce ΔF ≤ +tol. Keep the choice consistent in prereg, meters, and captions.
- Universality separation (Model A only for A8): use non‑conserved Model A (RD / Telegraph–Fisher) for A8 benches; reserve conserved Model B (Cahn–Hilliard) for later phases. Do not mix channels within a bench.

- **VDT Project Management & Reproducibility:**
  - Artifacts must be pinned (commit+seed in captions).
  - CSV/JSON/PNG sidecar manifests must be used.
  - Provenance tracking (`PROVENANCE_manifest.json`) must be implemented.
  - The Asset Index (`Derivation_ASSET_INDEX_Version.md`) must be updated whenever a `PROPOSAL_*`, `RESULTS_*`, or new runner/meter is added.
  - The Asset Index must include exact script paths for runners and module paths for instruments.
  - Maintainers must keep the "Quick Status" in the Asset Index honest.

- **A8 Infinity Resolution Conjecture (CT-3) & Validation (M-1) - High Priority:**
  - The theory must formalize tachyonic condensation as the primordial cosmogenetic event.
  - The theory must demonstrate that N(L) = Θ(log(L/λ)) for logarithmic depth.
  - The theory must demonstrate that E_exc(L) = Θ(L^(d-1)) (boundary-law energy).
  - The theory must demonstrate that α_I > 0 at boundaries (information concentration).
  - G1: A 1D theoretical proof of log-depth lower bound must be provided.
  - G2: A Γ-convergence or perimeter-law reduction for interface energy must be shown.
  - G3: Numerical scaling in 2D/3D (slope d-1±0.1) must be measured.
  - G4: Boundary energy fraction (α) and information fraction (α_I) must be ≥ 0.6.
  - G5: An ablation test (penalize hierarchy → energy blowup) must be performed.
  - G8: All preregistration, code, and artifacts must pass VDM reproducibility checks.
  - A hierarchical boundary detector must be implemented.
  - Operational information density metrics must be implemented in the codebase.
  - Multi-scale partition analysis tools must be implemented.
  - A log-depth vs L measurement apparatus must be implemented.
  - Boundary energy tracking infrastructure must be implemented.
  - Area-law vs volume-law measurement tools must be implemented.
  - Information proxy implementations (log(1+|∇φ|²/σ²)) must be created.
  - For A8 validation, all runs must adhere to the Pulled-regime criterion.
    - Measured front speed $c$ must be $\le c_\star(1+\epsilon_c)$ ($\epsilon_c$ preregistered, e.g., 0.02).
    - The leading edge must fit an exponential tail with decay $\lambda$ consistent with linear theory (±10%).
    - The "steepness test" must show that varying initial front steepness does not increase $c$ beyond $c_\star$ within tolerance.
    - Runs violating these criteria must be flagged as "pushed" and excluded from A8 admission.
  - "Information-concentration" claims must hold for both preregistered information proxies ($\mathcal{I}_1$ and $\mathcal{I}_2$) within preregistered tolerances (Gate G-PX).
  - All scaling claims are graded in $d=1,2$; boundary-law exponents must match $(d-1)$ within ±0.1, and $N(L)$ must remain logarithmic with stable base $\rho$ (±10%) after finite-size correction.
  - **Gate G-PLD (Pulledness diagnostic):** Must require $c/c_\star \le 1+\epsilon_c$, a good exponential-tail fit ($adj.R^2 \ge 0.98$), and that a steepness sweep shows $c$ approaches $c_\star$ from above but does not exceed it within gate. All three conditions must hold for PASS.
  - **Gate G-PX (Proxy concordance):** Boundary fractions from $\mathcal{I}_1$ and $\mathcal{I}_2$ must agree within ±10% across masks/seeds and both must exceed the $\alpha_\mathcal{I}$ threshold. It must PASS if both exceed the threshold and differ by ≤10%.
  - **Gate G-ABL-Compute:** If assisted energy/time budget is identical, replacing metriplectic guidance with random kicks must not meet the original CEG PASS criteria.
  - **Gate G-ABL-J:** With a scrambled J-map (same compute and assist budget), CEG improvement must drop below a specified threshold (e.g., 0.01 or 20% of baseline CEG, p<0.01).
  - **Gate G-ABL-M:** With a scrambled M-map (same budget), CEG improvement must likewise collapse below a specified threshold.
  - To PASS A8 validation, all G1–G5 must be met, AND at least one of G6–G7 must be met, AND G8 must be met.
  - In addition, the following always‑on bench hygiene gates must PASS for every A8 run:
    - **G‑DEP (Degeneracy certificate):** g₁ = ⟨J·δΣ, δΣ⟩ ≤ 1e−10 and g₂ = ⟨M·δI, δI⟩ ≤ 1e−10 with refinement tightening (A4).
    - **G‑GI (Grid‑invariance):** Under resolution doubling, drift of β_E, α, α_I, and N(L) slope ≤ 0.05 with CI overlap; document masks and procedures (anisotropy/morphometry controls).
    - **G‑H (H‑theorem sign):** Enforce ΔΣ ≥ −tol per M‑update; if reporting a Lyapunov free‑energy F instead, enforce ΔF ≤ +tol. Keep the choice consistent across prereg, meters, and captions (A5).
    - **G‑AL‑ModelSel (Area‑law model selection):** Dual fit E_exc(L) ∝ L^{d−1} vs E_exc(L) ∝ L^{d}; require ΔAIC/ΔBIC favoring area‑law, R² ≥ 0.98, and CI for β_E not straddling d.
    - **G‑FDR (Bundle FDR control):** Familywise q ≤ 0.10 across gate bundles; report q‑values in PASS/FAIL tables (A7).
  - To FAIL A8 validation, any of G1–G5 must fail, OR any always‑on hygiene gate must fail, OR G8 must fail.
  - A theory note (PDF) proving G1 lower bound in 1D + Γ-style perimeter reduction sketch, with repository anchors, must be delivered.
  - A preregistered experiment suite (scripts + manifests) producing scaling curves ($E_{\text{exc}}(L)$, $N(L)$, $\rho$, $\alpha$, $\alpha_\mathcal{I}$, $c/c_\star$) must be delivered.
  - A PASS/FAIL report with FDR table and ablation outcomes must be delivered.
  - If A8 passes, a `Canon/AXIOMS.md` patch and `Canon/Candidates/A8_*` moving to Accepted must be delivered.
- **Telegraph-Fisher Causality (CT-9) & Validation (M-2) - High Priority:**
  - The Telegraph-Fisher stepper must be coded.
  - A causal cone slack metric must be implemented.
  - A κ=rτ parameter sweep must be run.
  - Dimensionless collapse ĉ=(1+4κ)^(-1/2) must be validated.
  - A continuity test with RD baseline for overdamped limit τ→0 recovery must be created.
  - A `Derivation/causality/RESULTS_Telegraph_Fisher_v1.md` must be delivered.
  - H1-H5 hypothesis tests with cone plots must be delivered.
  - Overdamped limit τ→0 continuity with RD baseline must be delivered.
- **Critical Gaps - High Priority (from Roadmap Analysis):**
  - **OQ-002 Blocker:** Scale separation analysis and fast transient characterization must be developed for EFT branch necessity criteria.
  - **OQ-014 Blocker:** A variational limit from lattice action must be developed to recast the discrete model into a discrete action.
  - **OQ-015 Blocker:** Exact coefficient extraction from ∑J(Wⱼ-Wᵢ)² must be performed to derive kinetic normalization c² = 2Ja².
  - **OQ-027 Blocker:** A first-principles connection to the Planck scale must be established for lattice scale parameter determination.
- **Milestone EBN-A8-Def:** Must establish single-source, repository-canonical definitions of E_exc, α, α_I, β_E, N(L), tubular neighborhoods, and diameter/gap conditions, with unit tests on analytic shapes and synthetic segmentations.
  - Dependencies BN-1.1..1.5 basic implementations must be complete.
- **Milestone EBN-A8-Bridge-AI-Physics:** Must define a translation layer from `fum_rt` boundary artifacts to the physics-side tubular integrals and hierarchy depth N(L).
  - `fum_rt` metrics must be available.
- **Milestone EBN-A8-UQ:** Must add bootstrap CIs and power analysis for α, α_I, β_E, N(L) slopes; preregister ε-tube and segmentation parameter ladders; and publish sensitivity envelopes.
- **Milestone EBN-A8-Replicate:** Must replicate A8 metrics across distinct integrators (where applicable) and CPU/GPU + precisions; must record drift bounds as prereg gates.
- **Milestone EBN-Energy-Cal:** Must harmonize discrete energy density and tubular procedure; validate against analytic perimeters/areas; and eliminate definition drift.
  - EBN-A8-Def must be complete.
- **Milestone EBN-TF-IMEX:** Must implement Telegraph-Fisher dynamics with IMEX or Strang-partitioned J⊕M; must verify ⟨J,δΣ⟩=0, ⟨M,δI⟩=0 per step (bounds logged/gated).
  - Dependencies KG J-only runner, RD DG M-step, and structure checks must be complete.
- **Milestone EBN-TF-Stability:** Must document Δt–Δx–τ stability envelopes; dispersion error charting; and provide admissible ladders to avoid cone artifacts.
  - EBN-TF-IMEX must be complete.
- **Milestone EBN-TF-Calibration:** Must calibrate τ by matching TF c=√(D/τ) to J-limb c_J from KG dispersion/locality; must define a reproducible κ=rτ sweep.
  - KG dispersion/locality RESULTS must be available.
- **Milestone EBN-Cones-Arrival:** Must replace naïve thresholds with matched-filter or hysteresis front-tracking; must reduce noise sensitivity in cone slack.
  - BN-2.2 must be complete.
- **Milestone EBN-Units:** Must map (λ, r, D, τ) to comoving units/redshift using FRW baseline; must document re-scaling recipes for VDT↔cosmology.
  - FRW QC results must be available.
- **Milestone EBN-BranchCriteria:** Must define discriminants (e.g., inertia-to-diffusion ratios, local κ=rτ) and a decision flow in the runners; preregister thresholds for when to apply RD vs KG vs TF regularized branches.
  - TF calibration (EBN-TF-Calibration), KG and RD diagnostics must be complete.
- **Milestone EBN-Action-Continuum:** Must recast the discrete model into a variational action; derive ∂t² terms and c² normalization from lattice couplings; unit-tested toy models; and document assumptions.
- **Milestone EBN-c2-Norm:** Must extract c² from lattice couplings and spacing; validate against KG dispersion across grids.
  - EBN-Action-Continuum, KG dispersion results, and EQUATIONS.md must be complete.
- **Milestone EBN-Lattice-Scale:** Must calibrate lattice 'a' via astrophysical anchors (Skyrme T5 R*; cosmological characteristic scales); must provide prior ranges and uncertainty.
  - T5 RESULTS, FRW, and unit re-embedding (EBN-Units) must be complete.
- **Milestone EBN-PreReg:** Must implement machine-readable prereg YAML for A8, TF, T4, T5, GR weak-field, analogue horizons; must be locked before first runs; embedded SHA and salted provenance.
- **Milestone EBN-Repro:** Must add CI jobs to run A8/TF smoke tests on multiple hardware/OS stacks; quantify drift; require PASS invariance to platform within CIs.
- **A8 Conjecture Constraints:**
  - The system must operate in $d\in\{1,2,3\}$.
  - The potential $V$ must have $V''(0)<0$ (tachyonic origin).
  - The metriplectic evolution must have $J(\cdot)$ antisymmetric and $M(\cdot)$ symmetric positive semidefinite.
  - The system must exhibit pulled-front regime with speed $c_\star = 2\sqrt{D\,r}$, where $D\propto \kappa$.
  - A family of states $\{\phi_L\}$ on domains $\Omega_L$ must be finite-excess-energy: $\sup_{L} E_{\text{exc}}[\phi_L;\Omega_L] < \infty \quad\text{as } L\to\infty$.
  - Hierarchical partition must satisfy the gap condition: $\text{diam}(\Gamma_{\ell+1}) \in [\rho/C, C\rho]\cdot \text{diam}(\Gamma_{\ell})$.
  - Hierarchical partition must have finite depth $N<\infty$ for any finite $L$, with $N(L)=\mathcal{O}(\log (L/\lambda))$.
  - Boundary energy concentration must be $\liminf_{L\to\infty} \frac{ \int_{\mathcal{N}_\epsilon(\cup_\ell \Gamma_\ell)} \kappa|\nabla \phi_L|^2 \,dx }{ E_{\text{exc}}[\phi_L;\Omega_L] } \ge \alpha$.
  - Information density must show analogous boundary concentration for $\mathcal{I}$: a fraction $\alpha\_\mathcal{I}$ concentrates in $\mathcal{N}\_\epsilon(\cup\_\ell \Gamma\_\ell)$.
  - All “information‑concentration” claims must hold for both preregistered proxies ($\mathcal{I}_1$ and $\mathcal{I}_2$) within preregistered tolerances (Gate G‑PX).
  - M-production near $x_\star$ must scale $\propto \delta^2$.
  - Absence of hierarchical scale breaks must imply either energy blow-up or violation of the pulled-front bound.
  - The system must not exhibit existence of finite-excess-energy, large-$L$ states with no hierarchical partition and fronts still traveling at $2\sqrt{Dr}$ (F1).
  - The system must not exhibit robust demonstrations that $E_{\text{exc}}(L)=o(L^{d-1})$ or remains $O(1)$ without hierarchical boundaries (F2).
  - The system must not exhibit empirical boundary-energy fraction $<0.3$ with stable pulled fronts (F3).
  - Assisted nudges must be zero‑mean, white in phase, and supported only in the tail’s tubular set; a matched‑budget randomized control must be run each time.
  - Cross‑correlation between the final boundary field and the nudge field outside $\mathcal{N}\*\epsilon(x\*\star)$ must be $\le 0.05$ (pre‑reg) at all non‑tail scales.
  - All claims assume **pulled** propagation (i.e., measured speed $c\le c_\star(1+\epsilon_c)$, leading edge fits exponential tail, steepness test does not increase $c$ beyond $c_\star$). Runs violating any of these are excluded from A8 admission.
  - All scaling claims are graded in $d=1,2$; boundary‑law exponents must match $(d-1)$ within ±0.1 and $N(L)$ must remain logarithmic with the same base $(\rho)$ (±10%) after finite‑size correction.

### Should-have (important but flexible)

- **Global Tier Invariants (Tiers ≥T2):** Scaling groups should be used where appropriate (A6).
- **Target CT-2: Tachyonic Genesis:** Connection to cosmological observables needs quantitative models.
- **Target CT-5: Cosmic Web as Hierarchical Partition (M-3) - Medium Priority:**
  - VDT hierarchical partition depth N ~ log(L_universe/λ_planck) should predict observed cosmic web statistics.
  - A cosmological N-body simulation integration should be implemented.
  - Cosmic web topology metrics should be implemented.
  - Comparison with SDSS/DES large-scale structure data should be performed.
  - Hierarchical depth measurement from galaxy surveys should be implemented.
  - **Dependencies:** A8 validation must pass first.
  - `Derivation/cosmology/PROPOSAL_Cosmic_Web_Hierarchy_v1.md`, `Derivation/cosmology/PROPOSAL_CMB_Cold_Spot_v1.md`, and quantitative predictions with falsification criteria should be delivered.
- **Target CT-6: CMB Cold Spot as Origin Signature:**
  - Quantitative predictions should include: Temperature deficit: ~70 μK vs 18 μK typical; Size: ~5-10 degrees on sky; Mechanism: ISW effect from supervoid + primordial cooling signature.
  - CMB anisotropy calculation from VDT first principles should be performed.
  - An ISW effect + VDT origin cooling model should be created.
  - Parameter fitting to Planck/WMAP data should be performed.
  - Prediction of Cold Spot statistical properties should be performed.
- **Recommendations (Near-Term Actions):**
  - Cosmological prediction frameworks must be created.
  - A8 and Causality Results should be published (if gates pass).
  - Community Engagement actions (seminars, workshops, preprints) should be undertaken.
- **A8 Validation (G6, G7, G9, G10, G11, G1T, G2T, G3T, G-CEG-Integrity, G-DIM, G-NI):**
  - **G6 (Robustness):** Results should hold across different potentials ($V''(0)<0$), boundary conditions, and mesh scales.
  - **G7 (Cross-code):** Independent implementation should reproduce G3–G5 results within specified error bars.
  - **G9 (Refinement collapse):** Simulations at multiple mesh refinements ($\Delta x, \Delta x/2, \Delta x/4$) should be run and small-scale energy and M-production curves should collapse or converge.
  - **G10 ($\delta^2$ law):** With controlled micro-noise, measured M-production near $x_\star$ should scale as $\delta^2\pm 10\%$.
  - **G11 (Bottleneck & FDT):** Energy flux vs. wavenumber for spectral kinks should be analyzed and fluctuation–dissipation ratio matched within ±10%.
  - **G1T (coverage bound):** Measured $N(L,T)$ should satisfy a minimum coverage bound.
  - **G2T (cost optimality):** $E_{\text{exc}}$ for hierarchical runs should be minimized vs. non‑hierarchical baselines by ≥5%.
  - **G3T (δ² locality):** Tail‑localized M‑production near $x_\star$ should obey δ² ±10% across $\Delta x$ refinements.
  - **G-CEG-Integrity:** CEG should improve with $\eta$ while $c$ and perimeter-law scaling remain within pulled bounds.
  - **G-DIM:** In $d=1,2$, the fitted energy exponent should equal $d-1 \pm 0.1$, and $\rho$ should be consistent within ±10% across $d$.
  - **G-NI (No-imprint):** Cross‑correlation threshold should be $\le 0.05$ at non‑tail bands, and hierarchy ratio $\rho$ should be unchanged (±5%) relative to the unassisted run.
- **Milestone EBN-Cosmo-TDA:** Should add Betti curves/persistence and DisPerSE-like skeletonization; classify codimensions; compute N and boundary fingerprints robustly.
  - BN-3.1/3.3 prototypes should be available.
- **Milestone EBN-Cosmo-Obs:** Should incorporate survey masks, completeness, fiber collisions, and Redshift-Space Distortions (RSD) into P(k), ξ(r), void statistics, and boundary metrics; should publish corrections and uncertainties.
  - BN-3.3 must be complete.
- **Milestone EBN-CMB-ISW+Lens:** Should include Integrated Sachs-Wolfe (ISW)/Rees–Sciama (RS) and lensing with priors; produce $\Delta T$ and $\theta$ distributions; compare to Planck with Bayes factors; define falsification windows.
  - EBN-Units must be complete.
- **Milestone EBN-HPC-3D:** Should profile hotspots; implement FFT-based spectral ops and GPU acceleration where suitable; memory tiling for tubular neighborhood operations; plan target grid sizes and wallclock budgets for statistical power for A8/TF/cosmology experiments.

### Nice-to-have (optional, future scope)

- **Target CT-7: It from Metriplectic Bit - Wheeler Realization (M-4) - Low-Medium Priority:**
  - "Observer" should be formalized as system's interaction with its own constraints via M-term.
  - A formal information-theoretic framework should be created.
  - "Observer" as M-production operator should be formalized.
  - Measurement = boundary formation equivalence proof should be provided.
  - A connection to the quantum measurement problem should be established.
  - `Derivation/foundations/PROPOSAL_It_From_Metriplectic_Bit_v1.md`, `Derivation/gravity/PROPOSAL_BH_Information_Encoding_v1.md`, and a formal information-theoretic framework document should be delivered.
- **Target CT-8: Black Hole Information as Boundary Encoding:**
  - A black hole spacetime model in VDM should be created.
  - Horizon boundary formation dynamics should be modeled.
  - Hawking radiation from VDM first principles should be derived.
  - Information transcription should be quantified.
- **Recommendations (Long-Term Actions):**
  - The Foundations Framework should be developed.
  - Open Questions (OQ-014, OQ-015, OQ-027) should be resolved.
  - Community & Collaborations should be built.
- **A8 Validation (G12, G-DSI1, G-DSI2, G-DSI3):**
  - **G12 (DSI probe, optional):** Boundary statistics should be examined for log-periodic modulations.
  - **G-DSI1:** Log‑periodic modulation in boundary statistics should be nonzero and stable across sizes/masks.
  - **G-DSI2 (Null):** Log‑periodic modulation should be absent under control conditions (no limit cycle, pushed fronts).
  - **G-DSI3 (Cross-metric):** The same $\rho$ should appear in at least two independent metrics.
- **Milestone BN-4.1:** Should operationalize "Measurement = Boundary Formation" with a metriplectic-consistent information functional and falsifiable gates that tie M-production to information registration under a controlled protocol.
  - Dependencies A8 info/energy metrics, RESULTS harness, EBN-Info-Functional, T4 proposal must be complete.
- **Milestone EBN-Info-Functional:** Should define I_info[φ] aligned with Σ/I and A4 degeneracy; candidate implementations.
  - A8 info/energy metrics and RESULTS harness must be available.
- **Milestone EBN-T4-ΔΣΔI-Gates:** In the T4 CEG protocol, should preregister gates: corr(ΔΣ, ΔI_info) ≥ threshold (with refinement stability), echo-quality sensitivity under M vs J-only, and boundary-proximal info capture (α_I in ε-tubes) during controlled "measurement" windows.
  - EBN-Info-Functional and T4 proposal must be complete.
- **Milestone BN-4.2:** Should operationalize "Horizon as Hierarchical Boundary" with a precise path: weak-field Einstein–Skyrme post-processing from T5, and a near-term analogue-horizon experiment in the Wave Flux Meter.
  - Dependencies T5 RESULTS; units mapping; two independent solvers for replication; EBN-Info-Functional; Wave Flux Meter RESULTS (A/B phases) must be complete.
- **Milestone EBN-GR-Weak:** Should consume T5 ε(x) and f(x) to form Tμν[U], solve weak-field Poisson/linearized GR for Φ(r), compute v_circ(r), Σ_lens(R), and validate with tight replication gates.
  - Dependencies T5 RESULTS; units mapping; two independent solvers for replication must be complete.
- **Milestone EBN-Analog-Horizon:** Should extend Wave Flux Meter geometry to create an effective horizon; measure α/α_I scaling with horizon boundary measure and ΔΣ–ΔI correlation under controlled M injections; enforce energy/flux conservation gates.
  - Info functional (EBN-Info-Functional) and wave meter conservation gates must be complete.
- **Milestone EBN-GR-Covariant-Notes:** Should draft "Covariant Metriplectic Notes"—∂→∇, metric-compatibility of M, degeneracy in curved space, ∇μTμν=0 checks, and a spherical Einstein–Skyrme outline for future phases.
  - GR-Weak results and literature cross-checks must be available.
- **Milestone EBN-SM-Effective:** Should map SM gauge actions to transformations of Ψ that yield emergent Noether charges/currents in the J-limb; identify internal indices/fiber structure in Ψ consistent with A0 and A3; document necessary constraints.
  - SYMBOLS.md/EQUATIONS.md and Noether machinery in KG tests must be complete.
- **Milestone EBN-RG-Bridge:** Should connect lattice-scale VDT parameters to continuum EFT couplings via scaling/renormalization logic; identify dimensionless invariants that survive coarse-graining (A6).
  - UNITS_NORMALIZATION.md and Collapse domain results must be complete.
- **Milestone EBN-SM-Phenomenology:** Should define operational probes for emergent quasi-particles/collective modes in VDT that could correspond to SM-like sectors.
  - KG J-only instruments and metriplectic coupling QC must be complete.

---

*Powered by AI Content Suite & Gemini*
