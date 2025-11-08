<!-- ATTENTION! The results documents you create MUST BE whitepaper-grade documents with full structure, FULL NARRATIVE, MathJax-rendered equations (Meaning use Github MathJax syntax, $ ... $ and $$ ... $$ instead of other syntax), numeric figure captions tied to actual artifacts if using any for background, explicit thresholds with pass/fail gates, and provenance. You need to imagine if the document will be getting submitted for proposal at the most highly respected and quality Physics journals on Earth. These templates are engineering-grade and intended to be machine-actionable.

This template is the canonical authoring scaffold for VDM results (T0–T9 ladder). It is MANDATORY and IMPORTANT to include the substance of the outlined topics. The
length of the proposal should be at a MINIMUM of FIVE U.S. letter-sized pages (including figures and references). Language and phrasing in this document should be objective and third perspective, placing the VDM as the subject. When describing methods the focus should be on what is predicted, planned, and what will be done rather than using perspective based verbiage (example: "We/I/They propose a metriplectic..." would be wrong. Instead, do this "This document shows a metriplectic..." or even "VDM validated a metriplectic...")

# Tier Grades

This MUST included the grade of proposal this is. The grade of the proposal should be the same as the grade of the RESULTS_* if the runs pass.

Shown in a table below is the T0–T9 maturity ladder. This ladder distinguishes between:

- **Meters/instruments** (T2): Proven testing measurement apparatus
- **Phenomena** (T3+): Making physics claims with those proven meters
- **Preregistered claims** (T4-T6): Formal hypothesis testing
- **Robustness & validation** (T7-T8): Out-of-sample prediction
- **Reproduction** (T9): External verification

- **T0 (Concept)**
- **T1 (Proto-model)**
- **T2 (Instrument)**
- **T3 (Smoke)**
- **T4 (Prereg)**
- **T5 (Pilot)**
- **T6 (Main Result)**
- **T7 (Out-of-sample prediction)**
- **T8 (Robustness validation and parameter sweeps**
- **T9 (External verification/reproduction)** 

Additionally, if this RESULTS document is graded above T0, there should be existing supporting work referenced for each tier in sequence. For example, if a T4 experiment is proposed there must be a T0, T1, T2, and T3 that exists within the repository referenced with paths for any existing PROPOSAL and RESULTS documents listed. The figures and logs can also be referenced from each of those prior work items. There should be at a minimum of one for each, but no max limit.-->
# **Title Name Here**

> Author: Justin K. Lietz
> Date: {todays date}
> Commit: {either short or long commit hash}
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.  
> Commercial use requires citation and written permission from Justin K. Lietz.
> See LICENSE file for full terms.

## Authoring Policy (Comprehensiveness)

* Favor comprehensive, evidence-driven documentation over brevity. Include only context that directly supports methods, gates, and results.
* Lead with scope: state what this note **does** and **does not** claim. Use third person throughout.
* Use standard terminology first, then any project-specific label in parentheses. Define key terms once, plainly.
* Pair every conceptual claim with either a **concrete equation**, a **gate/threshold**, or a **reputable citation**.
* Treat the **numerical method as the measuring instrument**. Show the derivation → discretization → implementation path and tie each to validation gates.
* **Claims & novelty discipline:** never imply novelty for classical results; separate architecture (new) from kernels/math (may be standard); make each claim falsifiable with a metric+threshold+pass/fail.
* **Math & invariants discipline:** prefer tiny lemmas (≤3 lines); if dissipative, use gradient-flow/entropy/Onsager language (not least-action); introduce dimensionless groups early and drop tildes cleanly.
* **Naming & jargon:** avoid anthropomorphism; explain metaphors or remove them; clarity beats cleverness.
* **Posting flow (operational habit):** open with TL;DR + one artifact path; include at least one boxed gate or boxed lemma; end with one invitation (“Propose a tighter threshold; it will be run and posted.”)
* **Preflight checklist (before you post):**

  * Title reflects purpose (QC/architecture), not novelty.
  * Plain-language definitions appear before custom names.
  * Any invariant has a ≤3-line lemma/proof.
  * Every figure has CSV/JSON + seed + commit (same basename).
  * Gates have names, thresholds, pass/fail JSON, and contradiction report on failure.
  * Minimal citations at first skeptical touchpoints.
  * Runtime claims report β slope (log–log), P50/95/99, jitter, active-site fraction.
  * Floats anchored; captions include numbers (R²/slope/RMSE/CI).
  * Text leads with the artifact path; replies focus on thresholds.

## **Introduction**

1. Briefly state the computational phenomenon under study (e.g., dispersion relation recovery, front speed in reaction–diffusion, stability of a metriplectic discretization) and where it is used.
2. Explain scientific/practical significance (why this matters in computation; which decisions it informs).
3. Introduce and justify the **computational methodology** (finite volume/difference/FEM/spectral, Monte Carlo, agent-based, PDE-constrained optimization) as the appropriate probe.
4. Close with an explicit **evaluation question** and a **single artifact path** (code+data) that will prove/falsify the claim.
5. **Scope & boundaries:** list what’s out of scope (e.g., “No novelty claim for Fisher–KPP; this is QC only.”). Distinguish adaptation vs training in one line, then move on.

## **Research question**

1. State the question with **independent variables** (e.g., grid spacing (h), time step (\Delta t), Péclet (\mathrm{Pe}), seeds) and **dependent variables** (e.g., error norm (|e|_2), front speed (c), drift (\Delta\mathcal{I})).
2. Include units or declare a dimensionless program; give ranges/levels (e.g., (h\in{2^{-6},\dots,2^{-10}}), (\Delta t\in[10^{-4},10^{-2}])).
3. Specify **estimation/measurement** method for dependents (discrete norms, spectral estimators, bootstrap CI) and justify each choice.
4. Make it falsifiable: attach a **threshold** (e.g., “entropy drift (\le 10^{-5}) per step on (n\ge 8) seeds”).

## **Background Information**

1. Present the physics/mathematics of the core model (state, invariants, entropy/Lyapunov, symmetries).
2. Treat the **numerical scheme** as the measurement method (why Strang splitting/TVD flux/semi-implicit, what it preserves or biases).
3. **Core equations (required):** include only those used later:

   * Governing equation(s) in conservative/metriplectic or gradient-flow form.
   * Temporal/spatial discretization, stability conditions, and orders of accuracy.
   * Error/diagnostic models (modified equation, dispersion relation).
4. **Scope & larger theory (required):** situate within a standard framework (e.g., metriplectic dynamics; gradient flows), define minimal terms, and give 2–4 foundational citations at the first skeptical touchpoints.
5. **Map to gates (required):** connect properties to metrics/thresholds (e.g., “discrete Noether ⇒ (|\Delta \mathcal{I}|\le \varepsilon) over (T)”; “Strang split ⇒ two-grid slope (\ge 2)”).
6. If more context is needed, move it to a short **Theory Primer** or **Appendix**, not at the expense of clarity here.

## **Variables**

1. **Independent variables:** ranges/levels and rationale (grid (N), (h), (\Delta t), Reynolds/Péclet, noise amplitude, agents).
2. **Dependent variables:** units/dimensionless form, estimator definition, uncertainty quantification (bootstrap CI, multi-seed, Richardson extrapolation).
3. **Control variables table:** list each control (e.g., CFL, domain size, BCs, precision), how it’s controlled/normalized, and why.

## **Equipment / Hardware**

1. **Compute environment:** machines, accelerators, OS, compilers/interpreters, math libraries. Capture with:

   ```bash
   systemspecs
   ```

2. **Measurement limits/uncertainties:** fp32 vs fp64 accumulation error, solver tolerance, RNG quality, cross-architecture reproducibility tolerance.
3. **Configuration actually used:** solver tolerances, threading/affinity, ROCm version (AMD), BLAS/LAPACK, FFT library; justify choices.
4. **System metrics to report:** CPU model/cores/clocks; VRAM; RAM cap/peak; % CPU/GPU utilization; max/min temps; number of non-experiment processes; stage-wise wall-clock; storage footprint; whether hardware differences materially change outcomes (and mitigations). You can capture most, if not all, of this from the bash command listed just prior.
5. Optional pipeline schematic (I/O → preprocessing → solver → post-proc) if it clarifies.

## **Methods / Procedure**

1. **Reproducible pipeline (narrative, third person):**

   * Exact equations and discretizations.
   * ICs/BCs, parameters, seeds.
   * Solver details (integrator, tolerances, preconditioners, stopping criteria).
   * Post-processing (filters, diagnostics, regressions).
2. **Materials (software/data):** repo path + commit; environment spec (`environment.yml`/`requirements.txt`); datasets/IC generators with versions and licenses.
3. **Diagram (optional):** operator-splitting graph or data-flow if helpful.
4. **Risk/Ethics table:** data licensing, compute cost/carbon, execution safety (sandboxing/quotas).
5. **Security/Integrity:** always log seeds, commits, environment; disclose assistance roles (“Equations in standard RD form; architecture and tests specified by author.”)

## **Formal Derivation Writeup**
<!-- **ENTIRE Formal Derivation Writeup, with narrative flow for clarity**-->

* Physics and mathematic formalisms must be clearly explained from start to finish.
* Vague math or hand waving is prohibited, and this document will be rejected.

## **Results / Data**

1. Tables of processed results (centered) with clear captions; significant figures and uncertainties respected.
2. Qualitative computational observations (morphology, pattern classes, numerical artifacts) where useful (with images).
3. **Sample calculations:** show how norms, dispersion error, front speed, Richardson extrapolation are computed.
4. Full processed data tables after the sample.
5. **Uncertainty propagation:** analytic when possible; otherwise bootstrap/multi-seed. Provide interpretation (uncertainty vs effect size).
6. **Figures/graphs:** (MANDATORY) one claim per figure; numeric captions (slope, (R^2), RMSE, CI). Anchor floats (`[!htbp]`/`\FloatBarrier`; `[H]` sparingly). Pair every figure with CSV/JSON of the **same basename**; list seed and commit in the caption.
7. **Evidence & reproducibility:** pin one artifact path in text; on any gate failure, emit a **contradiction report** (gate, threshold, seed, commit, artifact pointer).

### Chain sampling diagnostics (if MCMC is used)

* ΔH histograms per stepsize ε with JSON sidecars (mean/var/skew/kurt) and a panel PNG; see [VDM-E-131](Derivation/EQUATIONS.md#vdm-e-131) and KPI [kpi-hmc-deltaH-hist](Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist).
* Acceptance vs stepsize curve: fit 1−α(ε) on log–log axes, report slope p and R²; expected p≈4 for leapfrog. Include the plot + CSV/JSON; see [VDM-E-130](Derivation/EQUATIONS.md#vdm-e-130) and KPI [kpi-hmc-acceptance-vs-stepsize](Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize).
* τ_int and ESS reporting: estimate τ_int per observable with stated window rule; log ESS=N/(2τ_int). Include a τ_int-vs-window figure or table; see [VDM-E-132](Derivation/EQUATIONS.md#vdm-e-132) and KPI [kpi-tau-int](Derivation/VALIDATION_METRICS.md#kpi-tau-int).
* τ‑aware binning: use B ≥ 2·τ_int and demonstrate CI stability under B→2B (≤10% relative change). Include a stability plot and JSON; see [VDM-E-133](Derivation/EQUATIONS.md#vdm-e-133) and KPI [kpi-binning-adequacy](Derivation/VALIDATION_METRICS.md#kpi-binning-adequacy).
* Correlated fits with SVD truncation: when fitting multi‑point observables, use full covariance and include a cutoff‑sweep figure; report χ²/dof and parameter stability past the knee; see [VDM-E-134](Derivation/EQUATIONS.md#vdm-e-134) and KPI [kpi-correlated-chi2-svd](Derivation/VALIDATION_METRICS.md#kpi-correlated-chi2-svd).

## **IX. Discussion / Analysis**

Open with key findings tied to figures/tables and metrics. Explain patterns via the **derivations** and **discretizations** (e.g., sources of instability, aliasing, boundary effects). Compare alternatives you tried (step sizes/fluxes/precisions) and how results change. Debate **thresholds**, not venues. Keep claims bounded by artifacts.

## **Conclusions**

Summarize what was learned, referencing mathematical structures and computational evidence. Discuss **computational error sources** (discretization, tolerance, precision, aliasing, boundary effects); avoid generic “human error.” State whether the research question is fully/partially answered, with numbers. Compare to **analytic/benchmark/literature** and cite inline. Define **next gates** to run. Explain how this supports or detracts from other hypotheses and open proposals, whether it changes things for the theory.

1. Restate the aim.
2. Relate trends back to the question with concrete values.
3. Report (R^2) (if linear), but also residual structure and CI.
4. Note anomalies with plausible computational causes (grid resonance, stiffness, cancellation) and follow-ups.
5. Interpret uncertainties relative to effect sizes (relative CI width, etc.).
6. Determine if the initial proposal provided an accurate prediction of results.
7. Name and list next plans and experiments for work to continue exploring the best path for Void Dynamics Model.

## **References / Works Cited**

* Cite lineage at first use: Logistic → Verhulst; fronts → Fisher–KPP; gradient flow → Onsager/JKO/AGS; RD patterns → Turing/Murray.
* Keep related work minimal but present (four solid bullets beat zero). Don’t bury key citations in an appendix.

---

## GENERIC metriplectic diagnostics (if dissipative/thermodynamic structure is used)

* Declare the GENERIC building blocks with canon anchors:
  * Evolution: [VDM-E-140](Derivation/EQUATIONS.md#vdm-e-140) (ẋ = L∇E + M∇S)
  * Poisson/Jacobi residual: [VDM-E-141](Derivation/EQUATIONS.md#vdm-e-141)
  * Degeneracy conditions: [VDM-E-142](Derivation/EQUATIONS.md#vdm-e-142)
  * Entropy production: [VDM-E-143](Derivation/EQUATIONS.md#vdm-e-143)
  * Structural variable c (if used): [VDM-E-144](Derivation/EQUATIONS.md#vdm-e-144), [VDM-E-145](Derivation/EQUATIONS.md#vdm-e-145)
  * Curie compliance: [VDM-E-146](Derivation/EQUATIONS.md#vdm-e-146)

* Required gates and artifacts:
  1) Degeneracy residuals (Casimirs): report g1 = ||L∇S||∞ and g2 = ||M∇E||∞ with JSON sidecar and pass/fail per KPI [kpi-degeneracy-resid](Derivation/VALIDATION_METRICS.md#kpi-degeneracy-resid). Include commit, seeds, grid/mesh meta.
  2) H‑theorem monitor: plot σ(t) and cumulative ΔΣ; assert non‑negativity to tolerance; provide CSV + JSON as per KPI [kpi-entropy-prod-nonneg](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg). State whether σ was computed via discrete‑gradient or continuous approximation.
  3) Poisson–Jacobi identity check: report e_Jacobi over the basis 𝔅 used, with threshold and histogram QQ‑plot; gate per KPI [kpi-poisson-jacobi-resid](Derivation/VALIDATION_METRICS.md#kpi-poisson-jacobi-resid). Include test functionals definition and BCs.
  4) Curie principle audit: include the linter output (curie_ok boolean and list of flagged couplings if any) per KPI [kpi-curie-compliance](Derivation/VALIDATION_METRICS.md#kpi-curie-compliance).
  5) If RG/scale analysis is performed: provide blocking/collapse overlay and envelope metric E_max per KPI [kpi-rg-collapse](Derivation/VALIDATION_METRICS.md#kpi-rg-collapse) with method tag (kernel, Δφ).

* OQ‑021 Corner Regularization (if applicable):
  * Report three corner KPIs with figures + CSV/JSON:
    • Stress boundedness near apex (no blow‑up vs r→0): [kpi-corner-stress-bound](Derivation/VALIDATION_METRICS.md#kpi-corner-stress-bound)  
    • Velocity cap and scaling collapse vs Λ·De_c with envelope E_max ≤ 0.05: [kpi-corner-velocity-cap](Derivation/VALIDATION_METRICS.md#kpi-corner-velocity-cap)  
    • Entropy non‑divergence (σ components and ΔΣ): [kpi-corner-entropy-nondiv](Derivation/VALIDATION_METRICS.md#kpi-corner-entropy-nondiv)
  * State the dimensionless groups used (Λ, De_c, Pe_c) and provide their definitions/values in the Variables section.
  * Confirm GENERIC conformance via the VDM‑GENERIC adapter QC (see [VDM-A-037](Derivation/ALGORITHMS.md#vdm-a-037)) prior to presenting results.

* Provenance:
  * Pin one artifact path for each KPI figure; filenames must share basenames with CSV/JSON logs (commit hash and seeds included).
  * If any gate fails, emit a contradiction report JSON and route outputs to failed_runs/ as per repository policy.
