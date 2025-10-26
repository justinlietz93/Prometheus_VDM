# VDM Standards Technical Summary Report

**Generated on:** October 26, 2025 at 4:26 AM CDT

---

# Comprehensive Technical Ruleset for Void Dynamics Model (VDM) Development

This document synthesizes the overarching technical rules, syntax requirements, and constraints governing the Void Dynamics Model (VDM) project. These commandments ensure architectural integrity, consistent development practices, rigorous validation, and secure operations across all project segments.

## 1. Foundational Principles & Architecture

*   **Axiomatic Foundations:**
    *   **Closure:** Utilize only objects defined within the framework; external primitives are prohibited as foundational elements.
    *   **Void Primacy:** All physical observables must be expressed as functionals of `Ψ` and its derivatives.
    *   **Local Causality:** Dynamics must be constructed from local functionals of the state; influence must propagate finitely from `Ψ` and its spatial/temporal derivatives. Reaction-Diffusion (RD) models must refer to 'front speed' instead of claiming a causal cone.
    *   **Symmetry (Noether):** Invariants under group `G` must generate conserved currents.
    *   **Entropy Law:** The entropy functional `Σ[q]` must be non-decreasing along trajectories, with equality permitted only at steady states.
    *   **Measurability:** Every non-trivial statement must map to concrete observables with a falsifiable test protocol.
    *   **Scale Program:** Predictions must be formulated in terms of dimensionless groups; units themselves carry no physical claims.
    *   **Lagrangian Metric Signature:** The kinetic Lagrangian density must include a minus sign to reflect the Minkowski metric (`+---`).
    *   **Axiom Anchors:** Provide a stable anchor per axiom in `AXIOMS.md` using the format `VDM-AX-00X`.
    *   **Axiom Compliance:** All Tiers ≥T2 of the project lifecycle must cite `A0–A7` compliance, ensuring measurable observables (`A7`) and appropriate scaling groups (`A6`).

*   **Metriplectic Framework:**
    *   **Dual Generators (J):** The `J` component of the metriplectic split must be skew-symmetric (`J^\top = -J`).
    *   **Dual Generators (M):** The `M` component of the metriplectic split must be symmetric and positive semi-definite (`M^\top = M >= 0`).
    *   **Degeneracy Conditions:** The degeneracy conditions `J * (δΣ/δq) = 0` and `M * (δI/δq) = 0` must hold.

*   **Void Dynamics Model (VDM) Specifics:**
    *   **VDM Continuum Surrogate:** The model must use both a first-order (Reaction-Diffusion-like) equation to reshape the substrate and a hyperbolic/telegraph equation for finite-speed signal transport.
    *   **VDM Scale Separation:** The tension between Reaction-Diffusion and Lorentzian Effective Field Theory (EFT) must be interpreted as scale separation, not a contradiction.
    *   **VDM Void-Debt Gate:** The void-debt gate `$\mathcal{D}$` must couple the Reaction-Diffusion and hyperbolic equations.
    *   **VDM Layer Naming:** The microscopic layer must be "excitation routing" (hyperbolic transport with VDM gating); the mesoscopic layer must be "substrate assimilation/repair" (Reaction-Diffusion with VDM-gated mobility); the macroscopic layer must be "conservation."
    *   **Gating Mask:** The gating mask `$\boldsymbol{\gamma}(\mathbf{x},t)$` must be in the range `[0,1]^C`.
    *   **Effective Wave Speed:** The effective wave speed `c_eff` must be defined as `c_0 e^(-½ β D)`.
    *   **Accumulation of D:** The `D` parameter must accumulate in regions of high curvature/gradients, and this accumulation must throttle transport.
    *   **D Dynamics:** The dynamics of `D` must be implemented as `∂t D = (1/τ_g)(a_1|∇u| + a_2|κ_path| + a_3|∇s|) - D/τ_r`.
    *   **Gating J:** The gating `J` must be implemented as `- D_s M_0 e^(-β D) ∇s`.
    *   **Kinetic Normalization:** The kinetic-term normalization must be unified: keep `$\mathcal L_K = \tfrac12(\partial_t\phi)^2 - J a^2(\nabla\phi)^2$` with no hard constraint between `J` and `a`, and wave speed `c^2=2Ja^2`. Any previous versions forcing `Ja^2=1/2` must be updated.
    *   **No Microscopic J-a Constraint:** There is no microscopic constraint tying `J` to `a`.

*   **Effective Field Theory (EFT) / Fundamental Universal Model (FUM):**
    *   **EFT Contextual Use:** EFT claims must only be used in EFT contexts.
    *   **EFT Objective (Rigor):** Rigorously calculate `V(\phi)` and `Z(\phi)` coefficients directly from the discrete model, and demonstrate that higher-derivative terms are zero or suppressed.
    *   **EFT Symmetry Assumption:** The low-energy theory must respect Lorentz invariance.
    *   **FUM Approach:** The FUM approach must not use external EFT, training, or extra postulates.
    *   **FUM Continuum Task:** Perform a rigorous derivation of coefficients directly from discrete model rules.
    *   **FUM Kinetic Term Derivation:** Formally derive the coefficient `Z(\phi)` and demonstrate it is a constant (`Z(\phi) = 1/2`).
    *   **FUM Temporal Kinetic Term:** The temporal part of the kinetic term arises from the kinetic energy term in the discrete Hamiltonian.
    *   **FUM Spatial Kinetic Term:** The spatial part of the kinetic term arises from the interaction energy between neighboring nodes.
    *   **FUM Spatial Kinetic Term Derivation Method:** Take the continuum limit of the interaction term via Taylor series expansion on `W_j` around node `i`, summing over neighbors, to show leading-order result proportional to `$(\nabla \phi)^2$`.
    *   **FUM Parameter Determination:** A parameter determination method from first principles must be established for the UTOE framework.
    *   **FUM $\partial_t^2$ Term:** The $\partial_t^2$ term must appear from first principles rather than by assumption in the discrete action recast.
    *   **FUM Kinetic Normalization:** Kinetic normalization `c^2 = κ a^2` with `κ = 2J` per-edge must be derived from discrete action via continuum limit.
    *   **FUM Conserved Quantity:** The true conserved quantity of FUM, beyond trivial energy/momentum conservation, must be discovered.

## 2. Documentation & Reporting Standards

*   **General Content & Structure:**
    *   **Whitepaper Grade:** All proposals and results documents must be whitepaper-grade, including full structure, narrative, MathJax-rendered equations, numeric figure captions tied to artifacts, explicit thresholds with pass/fail gates, and full provenance.
    *   **Evidence-Driven:** Favor comprehensive, evidence-driven documentation over brevity; include only context that directly supports methods, gates, and results.
    *   **Scope & Claims:** Results notes must clearly state what the note **does** and **does not** claim. Introduction sections must state exactly what is claimed and not claimed, and present the evaluation question in one sentence.
    *   **Third Person:** Use third person throughout all documentation.
    *   **Terminology:** Use standard terminology first, then any project-specific label in parentheses; define key terms once, plainly. Metaphors must be explained or removed; clarity takes precedence over cleverness.
    *   **Conceptual Backing:** Every conceptual claim must be paired with either a concrete equation, a gate/threshold, or a reputable citation.
    *   **Maturity Ladder Context:** Proposals' "Background & Scientific Rationale" section must address the maturity ladder and provenance.
    *   **Proposal Abstract:** Summarize motivation and anticipated goals in less than 200 words.
    *   **Related Work:** Keep related work sections focused (2–4 citations).
    *   **Core Equations (Results):** List only the equations actually used (invariants, discretizations, error models) with symbol definitions and units.
    *   **Procedure (Results):** Steps must be sufficient for replication; use third-person, past tense.
    *   **Results Reporting (Results):** Report processed data with uncertainties; present one claim per figure.
    *   **Discussion (Results):** Interpret patterns with explicit pointers to figures/tables. Claims must be bounded by artifacts, and limits noted.
    *   **Conclusions (Results):** Provide a concise restatement, list limits, and state the next testable gate(s). It must also determine if the initial proposal provided an accurate prediction of results.
    *   **Taxonomy Consistency:** All new indices must include the "Overarching Lenses" block and the "Genus" section where appropriate.
    *   **Taxonomy Leaf Content:** Each leaf in the taxonomy must have a one-minute explainer covering: what moves, what restores, what resists; what changes the tempo; what damps it.
    *   **Numerical Method Treatment:** The numerical method must be treated as the measuring instrument, showing the derivation → discretization → implementation path tied to validation gates.
    *   **Claims Discipline:** Never imply novelty for classical results. Separate architecture (new) from kernels/math (may be standard). Each claim must be falsifiable with a metric + threshold + pass/fail.
    *   **Math Discipline:** Prefer tiny lemmas (≤3 lines). If dissipative, use gradient-flow/entropy/Onsager language (not least-action). Introduce dimensionless groups early and drop tildes cleanly.
    *   **Naming & Jargon:** Avoid anthropomorphism. Explain metaphors or remove them. Clarity beats cleverness.
    *   **Posting Flow (Results):** Open with a TL;DR and one artifact path. Include at least one boxed gate or boxed lemma. End with an invitation to propose tighter thresholds.

*   **Formatting & Style:**
    *   **MathJax (General):** Use GitHub-safe `$...$` for inline expressions and `$$...$$` for block equations.
    *   **MathJax (Descriptions):** Inline `$...$` is permitted only within descriptions. Block environments or tags are prohibited within `Axioms.md` and `Constants.md`.
    *   **MathJax (Agency_Field.md):** Use the `boxed` keyword for core formulas.
    *   **MathJax (Data_Products.md):** Use `$...$` / `$$...$$` only when quoting existing math.
    *   **Proposal Length:** Proposal documents must not exceed five U.S. letter-sized pages (including figures and references). LaTeX templates will issue a compile-time warning if this is exceeded.
    *   **Figure Captions:** Figure/graph captions must be numeric, include numbers (e.g., $R^2$/slope/RMSE/CI), and list the seed and commit hash.
    *   **Math Style (Papers):** Use `\usepackage{siunitx,amsmath,amssymb,mathtools,amsthm}`. Prove tiny lemmas in one line and box derivatives that equal zero. Keep dissipative language to Onsager/entropy.
    *   **Plots Readable:** All plots must be readable in grayscale and have clearly labeled axes.
    *   **PNG Plots (VDM Fluids):** Render PNG plots with identical color bars and axis labels.
    *   **Figure Captions (VDM Fluids):** Include caption text in plots that references canonical equations from Block 1.
    *   **Markdown Linting:** `DATA_PRODUCTS.md` and `DIMENSIONLESS_CONSTANTS.md` may disable specific markdownlint rules (MD033, MD022, MD032, MD001).
    *   **Sidecar JSON Format:** Sidecar JSON files must be written with `json.dumps(payload, indent=2)`.

*   **Canonical Content & Cross-Referencing:**
    *   **Canonical Ownership:** The following files are the **sole owners** of their respective content: `derivation/SYMBOLS.md`, `derivation/EQUATIONS.md`, `derivation/CONSTANTS.md`, `derivation/UNITS_NORMALIZATION.md`, `derivation/VALIDATION_METRICS.md`, `derivation/BC_IC_GEOMETRY.md`, `derivation/ALGORITHMS.md`, `docs/DATA_PRODUCTS.md`, `docs/SCHEMAS.md`, `derivation/NAMING_CONVENTIONS.md`, `AXIOMS.md`.
    *   **Equations Page:** The one-page document for canonical equations (RD + hyperbolic + VDM) must be included in the repository.
    *   **Referencing Canonical Content:** Other documents must link to canonical content by anchor; content must not be duplicated elsewhere. Reference-only documents must never paste math or numbers; they must link by anchor.
    *   **Link Format:** Agents must insert links using the format `[VDM-E-012](../derivation/EQUATIONS.md#vdm-e-012)`; never copy math.
    *   **`ALGORITHMS.md` Rules:** Pseudocode must include references only; link to math/values elsewhere (EQUATIONS/CONSTANTS/SYMBOLS/UNITS).
    *   **`AXIOMS.md` Rules:** Cite sources from existing repository texts only.
    *   **`BC_IC_GEOMETRY.md`:** Link to equations/constants/symbols by anchor; do not restate them.
    *   **Prohibited Duplication:** Do not redefine symbols, paste equations or variants, restate numbers, re-explain units, reproduce math, embed equations/constants, re-derive formulas, define symbols in schema files, override naming conventions, or store canonical content in `ROADMAP.md` or speculations in `AXIOMS.md`.

## 3. Data & Artifact Management

*   **Output Generation & Routing:**
    *   **Output Discipline:** For each Dark Photon document, produce a minimum of one Python simulation that outputs one figure and one CSV/JSON, and assert acceptance gates before merging.
    *   **Artifacts (General):** All figures must include **numeric captions** and have paired CSV/JSON sidecars with the same basename, containing seed, commit, and metrics.
    *   **Failed Run Artifacts:** Failed runs must route their artifacts (figures, logs, contradiction reports) to a `failed_runs/` subdirectory. Original logs must be preserved under `failed_runs/` for audit.
    *   **Contradiction Reports:** A `CONTRADICTION_REPORT.json` must be emitted on gate failure, including the gate name, spec path, tag, seed, figure/CSV paths, and free text notes.
    *   **Tag Approval:** Any tag used for artifacts must be pre-registered and approved; otherwise, artifacts are quarantined.
    *   **Artifact Path Patterns:** All output paths must conform to specified patterns (e.g., `derivation/outputs/logs/conservation_law/flux_sweep_<timestamp>.json`). Default figure output: `derivation/code/outputs/figures/`. Default log output: `derivation/code/outputs/logs/`.
    *   **Figure Filenames:** Must follow the naming convention `{_ts()}_{slug}.png` (using UTC timestamp).
    *   **Log Filenames:** Must follow the naming convention `{_ts()}_{slug}.{type}` (using UTC timestamp), where `type` is either `'json'` or `'csv'`.
    *   **Output Path Overrides:** Output paths are overridable via CLI flags (`--outdir`, `--figure`, `--log`).
    *   **Image Format:** Figures must be raster images, typically PNG lossless.
    *   **Model Card:** Every benchmark must produce a JSON card with open channels and qualitative signature tags.
    *   **Limits Plotter:** The limits plotter must run, with CSV validated (schema + monotonic units), figure saved, and JSON summary written.
    *   **`io_paths.py` Functions:** `ensure_dir(p: Path)`, `build_slug(name: str, tag: str | None = None) -> str`, `figure_path_by_tag(domain: str, name: str, tag: str | None, failed: bool=False) -> Path`, `log_path_by_tag(domain: str, name: str, tag: str | None, failed: bool=False, type: str="json") -> Path`, `write_log(path: Path, data: dict)` must be implemented as specified.
    *   **JSON Logging Format:** When writing JSON logs, `json.dump` must be used with `indent=2` and `sort_keys=True`.
    *   **CSV Logging Format:** When writing CSV logs, `csv.DictWriter` must be used with `fieldnames=data.keys()` and `writer.writeheader()`.
    *   **Quarantine Policy Enforcement:** If `VDM_POLICY_APPROVED` is `0`, outputs must be quarantined (marked as failed).

*   **Provenance & Metadata:**
    *   **Provenance Recording:** Provenance (e.g., code locations, Git commit hashes, seeds) must be explicitly recorded for all data products.
    *   **Commit Hash (General):** Record the git commit hash (`{git rev-parse HEAD}` or short/long hash) in proposals and results documents for provenance.
    *   **Archiving:** Archive produced JSON/PNG under version control when passing. Keep generated artifacts under version control when passing.
    *   **Log Seeds/Commits:** Logs must record seeds and commit hashes.
    *   **Run Artifacts (Pinned Path):** One artifact path must be pinned in the text (repository commit + data directory).
    *   **Provenance Block:** A provenance block listing commit, env, seeds, hardware must be included where appropriate (e.g., Discrete Conservation).

*   **Data Structure & Schemas:**
    *   **Validation Hook Definition:** Validation hooks/KPIs must be explicitly defined for each data product.
    *   **Retention Policies:** Data product retention policies (e.g., "none," "rolling buffer," "configurable") must be specified.
    *   **Connectome Checkpoint Configuration:** Connectome checkpoint retention must be configurable via `checkpoint_keep`.
    *   **JSON Schema (Benchmarks):** JSON payloads for benchmarks must include `theory` (string), `params` (object), `metrics` (object), `outputs` (object), and `timestamp` (UTC ISO-8601).
    *   **JSON Logging (FRW Continuity):** The `frw_continuity_residual log` JSON must include fields: `tol_rms` (float), `rms` (float), `passed` (bool), `figure` (str), `csv` (str).
    *   **CSV Schema (Noise Budget):** Input `noise_budget.csv` files must contain columns: `freq_Hz`, `integration_time_s`, `shot_noise`, `thermal_noise`, `amplifier_noise`, `total_noise`, `SNR`.
    *   **CSV Schema (Fisher Estimate):** Input `fisher_example.csv` files must contain columns: `bin_label`, `expected_signal`, `background`, `exposure`, `eff_signal`, `eff_background`.
    *   **CSV Schema (FRW Continuity Series):** The `frw_continuity_residual series` CSV must include columns: `t` (float), `rho` (float), `a` (float), `residual` (float).
    *   **Dark Photon Output Formats:** Dark photon noise budget outputs must include JSON and CSV sidecars.
    *   **Python/TypeScript Schemas (Specific Constraints):** A comprehensive set of schemas defines field types, ranges, immutability, and conditional logic (e.g., `schema-run-profile` numeric fields `>=0`, `neurons >0`; `schema-lbmconfig` `tau >0.5`; `schema-routersplitevent` fractions sum to 1.0; `schema-baseevent` must be immutable, etc.). All such schema definitions must be strictly adhered to.
    *   **`qfum_metrics`:** Must include `failed_runs` subdirectory for non-passing experiments.

*   **Logging & Metrics:**
    *   **VDM Fluid Logging:** Log time series data in CSV or Parquet format, including `max(‖u‖)`, `max(|ω|)`, domain averages `⟨D⟩` and `⟨|∇u|⟩`, `E_kin` (kinetic energy), dissipation, and the VDM work term `W_D = ∫ β D |∇u|² dx`. Log VDM-work signals and debt signals.
    *   **C-score Calculation:** `C_score` must be unitless. Calculation requires a `ref` dictionary containing mean and standard deviation of P, U, V from a null/reference distribution for robust z-scoring.
    *   **Status HTTP Endpoint:** A status HTTP endpoint must lack authentication/TLS; keep it localhost by default, with optional token authentication gated.
    *   **Dashboard Data Retention:** Dashboard timeseries state data is in-memory only and not persisted.

## 4. Validation & Testing

*   **General Validation Principles:**
    *   **Reproducibility:** Ensure reproducibility by setting and recording seeds in logs. The pipeline must be deterministic (no RNG; seed N/A). Configuration used (solver tolerances, threading/affinity, ROCm version (AMD), BLAS/LAPACK, FFT library) must be justified.
    *   **Acceptance Gate Conjunction:** `acceptance.passed` (in JSON metrics) must be the conjunction of all sub-gates.
    *   **KPI Compliance:** All Key Performance Indicators (KPIs) defined in `VALIDATION_METRICS.md` must pass.
    *   **CI Failure:** A single failure in an aggregated test suite must fail the entire CI run.
    *   **Trial Validity:** Trials must be marked **invalid** if any tolerance fails (e.g., in local match methods).
    *   **Statistical Adaptation:** Apply Benjamini–Hochberg FDR and report **adjusted** Confidence Intervals (CIs) for statistics. Gates must use adjusted CIs.
    *   **Numerical Differentiation Expectation:** Numerical differentiation is expected to yield machine-precision residual.
    *   **`VDM-A-022` Policy:** `io_paths` policy and approvals must be in effect for `VDM-A-022` (Tube Spectrum and Condensation); unapproved runs must be quarantined.

*   **Core Framework & Axiom Validation:**
    *   **Axiom (A3 Symmetry):** Noether currents must be checked numerically in the KG runner; total drift must be `≤ 10^-8/period`.
    *   **Axiom (A4 Dual Generators):** Compute `g1 = <J, δΣ, δΣ>` and `g2 = <M, δI, δI>` every `K` steps; both must be `≤ 10^-10` (grid-refined).
    *   **Degeneracy (J+M Regimes):** `sum_product(<J*delta_Sigma, delta_Sigma>) approx 0` and `sum_product(<M*delta_I, delta_I>) approx 0` must be `≤ 10^-10 * N` (grid-refined).
    *   **Metriplectic Causal Dominance (Axiom Gates):** Locality (A2) J-only cone slope must be within `1%` across resolutions. Degeneracy (A4) `g1,g2` must be `≤ 10^-10` (refined). Noether (A3) energy/momentum drift must be `<= 10^-8/period` on J-only runs.
    *   **Metriplectic Causal Dominance (Witness Gates):** Cone-dominance tail ratio must be `≤ epsilon_tail` for all `t` and seeds. Echo-amplification reversed-run correlation must be `> baseline` by `>= 5*sigma` and decay *slower* than non-reversed probe.
    *   **Tachyonic Condensation (Axiom Validation):** All eigenvalues of the post-condensation mass matrix `M²` must be `≥ 0` (massless phases only if a complex scalar is used). An $R_\ast$ at which $E(R)$ has a true minimum must be identified.
    *   **Mass Gap Validation:** Validate a mass gap directly in simulation by perturbing a quiescent snapshot, measuring two-point correlation, fitting to $e^{-r/\xi}$, and reporting $m_{\text{eff}}=1/\xi$.
    *   **Propagation Speed Validation:** Measure propagation speed $c$ from a narrow pulse on the graph and back out $c^2 \approx 2Ja^2$.
    *   **Symmetry Breaking Validation:** Document symmetry breaking in order parameters by tracking $\langle W \rangle$ (or its distribution) across transitions, showing bimodal $\to$ unimodal collapse or hysteresis.

*   **Numerical Scheme & Conservation Validation:**
    *   **Discrete Conservation (Mathematical Gates):** Exact identity: `(ΔS === 0)` for the *implemented* one-step map. Local flux form: `(ΔQ_i + sum_j_in_N(i) (H_ij - H_ji) = 0)` per node. Scope declared: BCs, scheme (unsplit/split/RKp), parameter domain. Symbolic certificate: CAS-reduced zero with saved minimal forms.
    *   **Discrete Conservation (Validation Gates CI):** V1 Seed sweep: `>=40` random seeds; require `(max |ΔS| <= 1e-12)`. V2 Parameter grid: `>=6` tuples `((r,u,J,D,N))`; same tolerance. V3 `dt-slope`: slope `>= (p+1-0.1)`, `(R^2 >= 0.999)`. V4 Negative controls: Diffusion-only mass conservation at machine epsilon. Reaction-only `(Q_FUM)` `order-4` convergence with `(R^2 approx 1)`. V5 Out-of-sample: If `(H_ij)` has any fitted parameters, freeze and rerun on fresh seeds; identical tolerances must hold.
    *   **Discrete Conservation (Compliance Checklist):** Every figure must have a *numeric caption*. Each figure must have a paired CSV/JSON. Acceptance gates must be stated and marked PASS/FAIL. Provenance block must list commit, env, seeds, hardware. Boxed **LEMMA/THEOREM** or **CONTRADICTION_REPORT** as appropriate. Units and dimensionless groups stated; BCs and scheme declared. All plots readable in grayscale; axes labeled.
    *   **Flux-form Diffusion:** Must conserve total mass `sum(phi_i)` to machine precision when `f === 0`.
    *   **`Q_FUM` Logistic Invariant Validation:** `Q(W,t) = \ln(W/(r-uW))-rt` defines the logarithmic first integral, which must be constant (drift guard). KPI: `VALIDATION_METRICS.md#kpi-qfum-drift-abs (ΔQ ≤ 10⁻⁸)`. Convergence must be consistent with time-stepper's order. Track `Q_FUM` across tube-condensation numerics as a diagnostic that dynamics are predictable, not chaotic, during the phase transition.
    *   **Discrete Conservation ($\Delta L_h$):** `ΔL_h <= 0` must be reported per step under periodic/no-flux BCs.
    *   **H-theorem (Agency_Field.md):** Discrete Lyapunov must decrease per converged step (`ΔL_h <= 0`).
    *   **Strang Composition (Agency_Field.md):** Primary gate: two-grid slope `>= 2.90`, `R^2 >= 0.999`. If slope `<2.90` but Strang-defect regresses to `≈ 3` with high `R^2`, stamp **EXPLAINED-BY-DEFECT** (contingent on M-Lyapunov).
    *   **Metriplectic Strang Defect:** Strang defect slope near `3`: slope `approx 3`, `R^2 >= 0.999`. Asymptotic two-grid slope: slope `>= 2.90`, `R^2 >= 0.999`.

*   **Fluid Dynamics Benchmarks (LBM/Navier-Stokes):**
    *   **Falsifiable Acceptance:** Define falsifiable acceptance thresholds to certify LBM reduction to Navier-Stokes.
    *   **Taylor-Green Vortex Thresholds:** Baseline grid (≥ 256²): Relative error `|ν_{fit} - ν_{th}| / ν_{th} ≤ 5%`. Refinement (×2 linear res): Error must decrease consistent with scheme order. Viscosity fit must be within 5% tolerance.
    *   **Lid-Driven Cavity Thresholds:** Maximum divergence norm `‖∇·v‖₂ ≤ 1e-6` (double precision). Centerline profiles must converge with grid.
    *   **Void-Walker Non-Interference:** Ensure read-only walker usage does not alter flow fields. Acceptance: max `|Δu| = 0` and `|Δv| = 0` at end of matched runs. Zero field difference must be achieved between runs with/without walkers.
    *   **Fluid Sector Status:** Fluid benchmarks do not change the RD sector’s canonical status; both sectors live side-by-side with separate claims and tests.
    *   **Benchmark Pass Condition:** A benchmark passes when all thresholds are met and `metrics.passed` is true.

*   **Cosmological & Dark Sector Validation:**
    *   **FRW Continuity/Balance:** RMS residual `RMS_FRW` must be `≤ 10^-6`. Differentiation must use Central differences. The QC for FRW balance does not constrain cosmological parameters. Any future deviation at similar resolution would indicate a discretization or implementation defect. If the gate fails, artifacts must route to `failed_runs/` and a contradiction report must be emitted; no claims are made. Must emit a PNG plot of `r(t)`, a CSV of the time series, and a JSON log with parameters and gate outcome.
    *   **Dark Photon Portal Choice:** The primary method for Void Dynamics signatures must utilize the Dark Photon (A') as the anchoring portal.
    *   **Dark Photon Portal Validation:** Validation gates must include annotated regime split (quantum- vs thermal-limited) and finite-difference Fisher cross-check consistency.
    *   **Dark Photon Modeling Tunability:** Dark photon modeling must be tunable to ensure that dark energy drift ($\epsilon_{\rm DE}$) and dark matter injection fraction ($f_{\rm inj}$) remain tiny at low redshift.
    *   **Dark Photon Parameter Discipline:** All derived claims and artifacts must be subjected to acceptance gates, including specified tolerances and $R^2$ values.
    *   **UTOE Framework Validation:** A complete cosmological framework with observational connections must be established. Observational tests must be defined. Renormalization group analysis must be complete; UV/IR behavior must be characterized. Lattice scale must be determined from physical principles; uncertainty must be reduced.

*   **Reaction-Diffusion (RD) Validation:**
    *   **RD Causal Cone:** RD/Fisher–KPP models must not claim a causal cone; refer to 'front speed' instead.
    *   **RD Front Speed Validation:** Front speed agreement: `rel_err = |c_meas - c_th| / |c_th| ≤ 0.05`. Linear fit quality: `R² ≥ 0.98`. Cross-check: gradient-tracker speed within ≈5% of `c_th` and level-tracker speed.
    *   **RD Linear Dispersion Validation:** Median relative error over good modes (`R²_mode ≥ 0.95`): `med_rel_err ≤ 0.10`. `R²_array(measured vs σ_d) ≥ 0.98`.
    *   **RD Discrete Conservation (Results):** The study must restrict to periodic boundary conditions for the Obj‑A/B order and balance tests; Neumann boundaries are out-of-scope.
    *   **RD Derived Baselines (Metriplectic CD):** Front speed `c_front=2*sqrt(Dr)` must be within `2%`. Dispersion `sigma(k)=r-Dk^2` median relative error must be `≤ 1%`.
    *   **KG Dispersion (Agency_Field.md):** Regress `ω^2` on `k^2`; require slope `= c^2 +/- 2%`, intercept `= m^2 +/- 2%`, `R^2 >= 0.999`.
    *   **Locality Cone (Agency_Field.md):** Fit front radius `R(t)` from a narrow pulse; require `v <= c(1+ε)` with `ε=0.02`, `R^2 >= 0.999`.
    *   **CI Lint:** The command `grep -RIn "cone" derivation write_ups docs | grep -Ei "RD|Fisher|diffus"` is prohibited and causes CI failure.

*   **Tachyonic Tube Condensation Validation:**
    *   **Tachyonic Tube RESULTS:** Physically admissible spectrum coverage `cov_phys` is the primary KPI (gate `>= 0.95`); `cov_raw` is for transparency only.
    *   **Tube Spectrum Coverage Gate:** Spectrum coverage `cov_phys >= 0.95` across `(R,ℓ)` attempts. At least one low-$\ell$ mode (e.g., `ℓ≤2`) must be detected for some `R`.
    *   **Condensation Curvature Gate:** `finite_fraction ≥ 0.90` AND an interior minimum certified by either (i) a positive quadratic curvature (`fit a>0`) on a local window around the minimum, or (ii) a discrete second difference `Δ²E(R_i) = E_{i+1}-2E_i+E_{i-1} > 0` at an interior index `i`.
    *   **Tachyonic Mode Tower:** The tachyonic mode tower must show discrete `κ_ℓ(R)` solutions with a finite count $N_{\rm tach}(R)$ that grows with `R`.

*   **Agency & Learning System Validation:**
    *   **Connectome Step (VDM-A-002):** Dense connectome modes (`structural_mode=="dense"`) are a **BROKEN / WRONG** policy violation and are prohibited. Structural rewiring RNG must be plumbed from run seed; wire deterministic RNG.
    *   **Memory Steering Validation:** KPIs for drift `(≤0.02)`, target convergence `(|M_final - 0.6| ≤ 0.02)`, and SNR improvement `(≥3 dB)` must all pass.
    *   **GDSP Runtime Wiring Validation:** Firing path tag $\to$ actuation latency `≤ 2 ticks`. `TagEvent` must be integrated; scoreboard must be operational. GDSP tick must be callable; sparse operations must work under budget constraints. Budgets must be computed from signals; no static knobs.
    *   **GDSP Adaptive Thresholds (VDM-A-007):** Thresholds must stay within `[min, max]` bounds. Histories must be bounded to the last 100 samples. `sie_report` keys must be present. `reward_threshold` must be `0.95*reward_threshold + 0.05*r75` for statistical adaptation.
    *   **Agency Curvature Scaling (KPI/Gates):** Linear fit slope stability within `± 10%` and `R^2 >= 0.99`. Gates: `|β| <= 0.05 * α * X_bar`, slope CV `<= 10%` across `Θ`, `R^2 >= 0.99`.
    *   **Agency Stability Band (KPI/Gates):** Distinct band in `(D_a,Λ)` plane with retention `(>0.8)` and boundary reproducibility. Gates: Contiguous band where retention `(>0.8)`, half-life within target window, and cross-slice reproducibility (Jaccard index `>= 0.7`).
    *   **Agency Witness (Gates):** `exists r_star > 0` with `median W(r_star) >= 5 * sigma_null`, CI excluding `0`, and replication across discretizations. For nonlocal agency, `r_min_hat` must replicate across discretizations within one grid step. Local-feature invariance: `W(r)` must remain above threshold after conditioning on matched local statistics. Monotonic onset: `W(r)` must increase monotonically up to `r_star` (Spearman `ρ >= 0.8`), then saturate. Null/Controls Gates: For `P_local`, `|median W(r)| <= 2 * sigma_null`, adjusted CIs contain `0`. For `r=0` and `r_near`, `|median W(r)| <= 2 * sigma_null` (both policies).
    *   **ADC Response Slope (Gates):** `|hat_Θ/Θ-1| <= 0.05`, `R^2 >= 0.99`, KS `(p>0.1)`.
    *   **Agency Readme (Action Plan Gates):** Curvature scaling (`R^2 >= 0.9`, slope within 10%); Stability band (`D_a >= Λ` at intermediate `Γ`); ADC response (measured slope equals programmed `Θ` within `±5%`); SIE invariant (slope `>= expected-0.1`, `R^2 >= 0.999`, bounded `Q` drift); Loop quench (`ρ <= -0.7` for `ΔL_h < 0`, fast-decay tail).

*   **Other Specific Validation Gates:**
    *   **A6 Collapse (Gates):** Max envelope `env_max <= 0.02`.
    *   **Energy Clamp (draft_sims.md Gate):** Curve should sit near 2.0 before `(t=5)`, relax toward `~1.2` after, and exponential fit should hug the simulated curve.
    *   **Inverted-U Ridge (draft_sims.md Gate):** Heatmap must show a **bright band** (ridge) at **intermediate coupling** and **moderate noise**; dark corners at very low/high coupling/noise.
    *   **Canonical Progress (J-only Regimes):** Locality cone: `v_front` must be within `2%` of `c`; cone stable under refinement. Dispersion: linear fit `R^2 >= 0.999`. Noether: per-step drift `≤ 10^-12` or `10 * epsilon * sqrt(N)`; reversibility `≤ 10^-10`. Energy oscillation: slope `p in [1.95, 2.05]`, `R^2 >= 0.999`, `e_rev <= 10^-12`, `(A_H / H_bar)_min_Delta_t <= 10^-4`.
    *   **Canonical Progress (M-only Regimes):** Front speed: relative error `≤ 5%`, `R^2 >= 0.999`. Dispersion: median relative error `≤ 2 * 10^-3`, `R^2 >= 0.999`. H-theorem: `Delta Sigma >= -tol`.
    *   **Canonical Progress (On-site ODE):** `Q` conservation: drift `≤ 10^-8` at `Δt ~ 10^-3`.
    *   **Canonical Progress (Coupled Lattice):** `Q` conservation: bounded by coupling & timestep tolerance.
    *   **Causal DAG Audits (Gates):** Acyclicity must be true (within `δ` jitter). Slope(`log|I|` vs `log Δt`) `≈ mean d_hat +/- δ_d`. Optional frontier `≤ c(1+ε)`.
    *   **Detector Noise Budget Plotting:** Plot SNR vs. integration time for a fixed frequency (single curve) and identify/annotate quantum-limited vs. thermal-limited regimes. The plot must be saved as PNG.
    *   **Detector Noise Budget Conclusion:** A one-sentence conclusion must specify the dominant noise regime and its underlying cause.
    *   **Fisher Information Estimation:** Compute a simple Fisher estimate for $\varepsilon$ in 1-2 bins, either analytically or via finite differences.
    *   **Fisher Information Output:** Output a tiny JSON summary with the estimated $\sigma(\varepsilon)$.
    *   **Fisher Information Note:** A two-line note must accompany the Fisher estimate, describing the scaling behavior of sensitivity with exposure and background.
    *   **QC Statistics Constraints:** The neuron count must be ≥ 64.
    *   **VDM Fluid Model Acceptance:** Acceptance requires one geometry diagram with labels, one parameter table with run values, and the two main plots.
    *   **VDM Fluid Plot Expectation:** Expect monotone saturation to a finite ceiling for max speed plots with VDM on.

## 5. Numerical Stability & Implementation

*   **General Algorithms & Logic:**
    *   **Main Loop (`VDM-A-001`):** Steps are sequential (single-threaded per tick). `Try-except` wrappers must be used on all subsystem calls. `VOID_STRICT=0` must result in silent no-op on errors. `VOID_STRICT=1` must re-raise exceptions for debugging.
    *   **Connectome Step (`VDM-A-002`):** `N, k, threshold, lambda_omega, candidates` must be configured. Node weights `W` must be initialized in `[0,1]` and stay within `[0,1]`. Adjacency matrix `A` must be symmetric and have approximately `k` neighbors per node. Edge weights `E` must be derived from `W` and `A`.
    *   **Void Scout Runner (`VDM-A-003`):** `max_us` must be `>= 0`. Total wall-clock time must be `<= max_us`. Round-robin fairness must be maintained over ticks. Scouts must have a `.step(...)` method. Connectome must expose neighbors/get_neighbors. `Try-except` must be used on `scout.step` (swallow errors). `Try-except` must be used on `bus.publish_many` (swallow errors).
    *   **Alias Sampling (`VDM-A-005`):** `p` must be normalized to `p / sum(p)`. If `p.sum() <= 0`, a uniform distribution fallback (`p = 1/N`) must be used. `p.size > 0` and `p.sum() > 0` must hold. `prob.size == alias.size == N` must hold. Draws from alias table must reproduce original distribution.
    *   **RE-VGSP Learning Step (`VDM-A-006`):** `W` must be a CSR matrix, operating on `W.data`; `indices/indptr` must remain unchanged; densification is forbidden. `E` (eligibility traces), if present, must be CSR with **identical sparsity pattern** as `W`. `W.indptr`/`W.indices` must be unchanged (no structural rewiring). Value changes must be bounded by chosen clamps. If `domain_modulation` lookup fails, use `dm := 1.0` and log a warning. If `E` pattern mismatches `W`, raise an error (do not silently densify) or resync pattern explicitly.
    *   **Fluid Dynamics Walker (`VDM-A-008`):** Clamp `x_new`, `y_new` to interior band `[0.5, nx-1.5] x [0.5, ny-1.5]`. If `solid[y_new, x_new]`, jitter inward. `sim.ux`, `sim.uy` must be 2D arrays (`ny, nx`). `sim.solid` must be a boolean mask. No writes to `sim` state (read-only).
    *   **Advisory Policy (`VDM-A-009`):** Suggested params must stay within bounds. No writes to `sim` state (advisory only). Default mode is `observe-only`; `advise/act` modes require explicit flags and must *never* inject body forces.
    *   **Memory Steering (Graph Laplacian):** Input adjacency matrix `A` must be symmetric for undirected graphs; self-loops are ignored by setting diagonal to 0 in degree calculation.
    *   **Memory Steering (Transition Probabilities):** If `neighbors` list is empty, an empty array must be returned. Softmax steering probabilities must use numerically stable max-subtraction. If the sum of exponentials `s <= 0.0` or is not finite, fallback to uniform probabilities.
    *   **Memory Steering (Temperatured Transition Probabilities):** Temperature `T` must be a finite float greater than 0, else default to `1.0`. Must use numerically stable max-subtraction and retain backward compatibility with `transition_probs()`.
    *   **Memory Steering (Heading-aware Sampler):** The `heading` vector will be renormalized defensively. `pos` must provide geometric coordinates for all nodes; otherwise, use memory-only softmax.
    *   **Memory Steering (Y-Junction Adjacency):** The returned adjacency matrix `A` must be dense binary.
    *   **Memory Steering (Junction Choices):** If the junction does not have exactly two neighbors, or `neighbors` is not `(a_next, b_next)`, it must fallback to using the two highest-`m_j` neighbors.
    *   **Curvature Scaling (Pearson Correlation):** If the denominator is `0.0` or not `np.isfinite`, `float("nan")` must be returned.
    *   **Curvature Scaling (AUC Binary):** If `n_pos == 0` or `n_neg == 0`, `float("nan")` must be returned.
    *   **Curvature Scaling (Average Precision TopK):** If `n_pos == 0` or `topk <= 0`, `float("nan")` must be returned.
    *   **`run_a6_collapse.py`:** For interpolation, `x` values must be monotone. If `xmin`, `xmax` are not finite or `xmax <= xmin`, empty arrays must be returned.

*   **Numerical Stability & Precision:**
    *   **Precision:** Numerical calculations in fluids benchmarks must use double precision.
    *   **Memory Steering (Memory Update):** Explicit Euler requires `dt` small enough relative to (`delta`, `kappa * lambda_max(L)`) for stability.
    *   **CFL Constraints (Diffusion):** CFL-type bound `Δt <= Δx^2/(2dD)` must be maintained for stability in discrete diffusive update. For explicit diffusion in 1D Euler, ensure `Δt <= Δx^2/(2D)`. Log the boolean `cfl_used` and record the actual `dt` chosen. Maintain a CFL number `≲ 0.5` for VDM Fluid Models. Curvature Scaling `kappa` must be clamped by a CFL condition: `dt * κ * λ_max(L) <= cfl_limit` with `λ_max(L) ≈ 2 * deg_max`. The Explicit Euler step **must obey** `dt ≤ cfl · dx²/(2D)`. Scripts **must compute** a safe `dt`.
    *   **Energy Clamp (`draft_sims.md`):** If `D > 0`, `dt` must be `0.9 * cfl_limit` if it exceeds `0.95 * cfl_limit`.
    *   **Numerical Safety Clamp (VDM Fluids):** `$\nu_{\text{eff}}/\nu \le 5$`.
    *   **BGK Relaxation Time:** The BGK relaxation time `τ` must be `>0.5` for stability.
    *   **Random Noise IC (RD dispersion):** Small amplitude must ensure linearization `partial_t u approx D partial_xx u + r u` is valid.

*   **Computational Environment & Execution:**
    *   **Operating System:** The OS must be Linux.
    *   **Python Environment:** Python environment must conform to `requirements.txt`.
    *   **Environment Activation:** Always activate the Python virtual environment (`.\venv\Scripts\Activate.ps1`) before running fluid dynamics benchmarks and before running commands in general.
    *   **System Metrics Reporting:** CPU model/cores/clocks; VRAM; RAM cap/peak; % CPU/GPU utilization; max/min temps; number of non-experiment processes; stage-wise wall-clock; storage footprint; whether hardware differences materially change outcomes (and mitigations) must be reported.
    *   **`USE_REVGSP_TIME_DYNAMICS`:** Must be `True` for all proofs.
    *   **`USE_GDSP_TIME_DYNAMICS`:** Must be `True` for all proofs.
    *   **`W[0]` Initialization:** `W[0]` is typically initialized at `0.1`.
    *   **`num_steps`:** Fixed at `100` for QM and SM, `1000` for Cosmogenesis, DM, Higgs, Light Speed. Varies (e.g., 100 to 50,000) for multi-scale analyses (e.g., Biology and Consciousness proof).
    *   **Spectrum Phase Execution (Tachyon):** Sweep of radii `R ∈ R_sweep`; compute lowest `κ_ℓ` per `ℓ ≤ ℓ_{\max}`.
    *   **Condensation Phase Execution (Tachyon):** For each `R`, compute diagonal quartic `N4_ℓ`, condensates `v_ℓ`, post-condensation masses `M²_ℓ`, and energy `E(R)`.
    *   **Runtime Estimate (Tachyon Condensation):** Expected runtime is `< 2 minutes` per tag (`ell_max=8`, modest `R` grid) on standard workstation.
    *   **No New External Libraries:** No new external libraries beyond SciPy are allowed for the `cylinder_modes.py` and `condense_tube.py` pipelines.
    *   **GPU-native frameworks:** Heterogeneous computing requires GPU-native frameworks (ROCm/HIP for AMD).
    *   **Type-specific Kernels:** Type-specific GPU kernels must be working; correct device allocation must be achieved.

## 6. Security & Authorization

*   **Global Approval Requirement:** Approvals are **required** for all scripts unless explicitly listed in the `exempt_scripts` database table.
*   **Approval Process Prerequisite:** For any experiment to run or pass, `PROPOSAL_` documents must be created.
*   **Approval Key Derivation:** The approval key must be derived using `HMAC-SHA256(secret, f"{domain}:{script}:{tag}")`. `tag_secret` is prioritized over `domain_key` for derivation.
*   **Approval Conditions:** Approval requires all of the following: `pre_registered=true` in the manifest; the tag is present in `allowed_tags`; a `proposal` file exists; a tag-specific JSON schema exists and contains the same tag; `approved_by` matches the configured approver name (default: "Justin K. Lietz"); `approval_key` in the manifest matches the expected key derived from the database secret.
*   **Runtime Rejection:** The runtime checker **must reject** runs on any mismatch in the approval block compared to database expectations.
*   **Pre-Run Validation:** Integrate approval checks before any artifacts are written.
*   **Unapproved Runs:** Unapproved runs must be quarantined and excluded from canon.
*   **Database Design:** Employ a two-DB design: Public DB (`approval.db`) is freely readable by runtime, with write operations gated by CLI/password; Admin DB (`approval_admin.db`) stores only the PBKDF2-SHA256 admin password record.
*   **Admin Password Handling:** The admin password must always be entered interactively (never via environment variables) and used only to authorize CLI write operations.
*   **DB File Permissions:** Public database file permissions must be set to `0o600` on creation. Place DBs in user-private locations.
*   **DB Path Discovery Order:** Discover database paths in this order: CLI flags, environment variables (`VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`), optional `.env` files.
*   **DB Creation Logging:** When a database path is resolved, the module **must log** its provenance (source of the path) at INFO level.
*   **DB Schema Initialization:** On first creation, the module **must initialize** the schema and enforce `0o600` permissions.
*   **Admin Password Hashing:** PBKDF2-SHA256 must be used for admin password hashing.
*   **Admin Password Verification:** Password verification must return `False` if the scheme is not `pbkdf2_sha256`.
*   **Manifest Path Resolution:** Manifests are located with priority: 1) `Derivation/code/physics/<domain>/APPROVAL.json`, 2) `Derivation/<domain>/APPROVAL.json` (as a writings fallback).
*   **Schema Validation for Approval:** For a schema to be valid for approval, its `tag` field (or `metadata.tag`) must match the requested tag, and it must contain either `"$schema"` or `"type"`.
*   **Hard Block Policy Enforcement:** If `VDM_POLICY_HARD_BLOCK` is `1` and the run is not approved, a runtime error must be raised.
*   **Result Logging Integrity:** Store results in SQLite with per-experiment tables, including a `row_hash` (SHA-256) for the entire row to enable tamper-evident auditing.
*   **Experiment Script Naming for HMAC:** The `VDM_RUN_SCRIPT` environment variable must be set to the stem of the run script to help downstream authorization policy.
*   **Read-only CLI Commands:** Read-only CLI commands (status, check, exempt list) must not require a password.
*   **Public DB Schema:** The Public DB must contain `approvals`, `domain_keys`, `tag_secrets`, and `exempt_scripts` tables.
*   **Admin DB Schema:** The Admin DB must contain an `admin` table.

## 7. Project Management & Workflow

*   **Project Lifecycle & Maturity (Tier Standards T0-T9):**
    *   **T0 Concepts:** Declare target branch tag(s). Identify state, controls, and observables. Cite relevant axioms/equations anchors for T0 promotion to T1.
    *   **T1 Formalization:** Link to **AXIOMS/EQUATIONS** used. List risks/assumptions. Choose meter(s), KPIs, and QC checks. Specify branch-specific gates for T1 promotion to T2.
    *   **T2 Calibration:** Calibrate instruments before claiming phenomena.
    *   **T3 Smoke Tests:** Include a small demo with the T2 meter. Predeclare no novelty if QC-only; log pass/fail with margins.
    *   **T4 Preregistration:** Lock hypotheses, nulls, effect sizes, CI thresholds, analysis windows, and contradiction routing.
    *   **T5 Pilot Execution:** Verify power and CI handling with narrow grid/time.
    *   **T6 Main Execution:** Report full prereg run, KPIs, CIs, and ablations.
    *   **T7 Robustness:** Track degradation vs. meters through parameter sweeps, stepper variants, and resolution scaling.
    *   **T8 Out-of-Sample Prediction:** Report hit-rate or quantitative error on previously unseen systems/datasets.
    *   **T9 External Reproduction:** Achieve independent team reproduction of T6-T8.
    *   **Transparency:** Include scope banners ("meter testing, not phenomenon", "no novelty claim") and transparent gates for all Tiers ≥T2.
    *   **Canonical Progress Status Tags:** Only `[DISPROVEN]`, `[PLAUSIBLE]`, `[PLAUSIBLE→PROVEN]`, `[PROVEN]` are allowed; any other word fails CI.

*   **Development Workflow & Practices:**
    *   **Canonical File Headers:** Canonical files must include `<!-- DOC-GUARD: CANONICAL -->`.
    *   **Reference-Only File Headers:** Reference-only files must include `<!-- DOC-GUARD: REFERENCE -->`.
    *   **Append-Only Blocks:** Agents may update only inside `AUTOSECTION` fences.
    *   **HTML Anchors:** Preserve HTML anchors exactly; if moved, update links, do not modify content.
    *   **File Maintenance:** Rules for maintaining `DATA_PRODUCTS.md` are defined in `/mnt/ironwolf/git/Prometheus_VDM/prompts/data_products_maintenance.md`.
    *   **Copyright & Licensing:** Commercial use of this research requires citation and written permission from Justin K. Lietz. Refer to the `LICENSE` file for full terms.
    *   **Scout Flag Overlap:** Scout flags must be unified or toggles validated if overlapping.
    *   **Software Skeleton (LOC):** Keep files `LOC <= 500/file`.
    *   **Software Skeleton (Business Logic):** Business logic must be framework-free.
    *   **Next Steps (Metriplectic Causal Dominance):** Create proposal document from template; pin git hash and salt hash for provenance. Record seeds/commits/constants from single-source of truth.
    *   **RD Discrete Conservation (Variables):** BC must match code (`periodic` / `no-flux`). Scheme must declare `p` (`Euler` / `Strang p=2` / `RKp`).
    *   **VDM Fluid Model Experimental Design:** Freeze the corner testbed specification.
    *   **VDM Fluid Model Faithfulness:** Do not alter walls or relax no-slip. Do not add arbitrary smoothing; modulation must be state-coupled. Encode a finite information/transport rate.
    *   **Project Context (`VDM-A-002`):** `Env gate: NO_DENSE_CONNECTOME=1` must be asserted in tests/CI.
    *   **EFT Scale Ladder Figure:** A ladder figure depicting different energy scales within the EFT framework must be developed, supported by five bullet points explaining assumptions pertinent to the rungs.
    *   **Dark Photon Fields/Couplings:** Define dark photon A′ (hidden U(1)_D), dark Higgs S (complex scalar), SM fields, and couplings (kinetic mixing $\varepsilon$, dark gauge $g_D$, dark Higgs potential $V(S)$).
    *   **"Tachyonic Tube" De-emphasis:** Move the "tube tachyonic tower / E(R) minimum" work to `archive/method_dev/` and de-emphasize its core role in A' claims, while retaining code and documentation.
    *   **"Void Laws" Translation:** Replace "breaks the laws" with "breaks a symmetry / changes phase / transfers energy through a portal."
    *   **Void Field Type Selection:** Pick a void field type: scalar $\phi$, vector A' (dark photon), or axion-like $a$.
    *   **Symmetry Breaking in Visible Phase:** In the visible-coupled phase, symmetry must be broken, and a mass gap must open.
    *   **Decoherence Explanation:** Once coupled, the void field's excitations leave interference records in our sector; macroscopically, it must behave classically. Three bullet points explaining decoherence must cover record location, practical irreversibility, and why "invisible" does not equate to "anti-photon."
    *   **Energy Accounting:** "Evaporation" must conserve energy-momentum, translated into decay, scattering, or phase change.
    *   **Domain Folders:** All domain folders under `Derivation/code/physics` must contain `schema/`, `specs/`, `APPROVALS.json`, and `README.md`.
    *   **Schema Directory:** Each `schema/` directory must contain required schema files.
    *   **Specs Directory:** Each `specs/` directory must contain required spec files used to configure experiments and other metadata.
    *   **APPROVALS.json:** Each `APPROVALS.json` file must contain required approval information.
    *   **Domain README.md:** Each `README.md` within a domain folder must contain required background, equations, and methods for experiments. Its header must be `# {Domain} Experiments`, with common sections listed with `## {Section name}`.
    *   **Helper Module Usage:** All experiments must use the helpers in `common/` for logs and figures handling. They can also use `common/` for existing equations, constants, and theory-wide resources.
    *   **Authorization Module Isolation:** The `authorization` package must be kept isolated from other common utilities and must not contain experiment code or plotting logic.
    *   **Approval System Enforcement:** The `authorization` module is wired into other helpers to enforce the approval system.
    *   **Plotting Helper Usage:** The `plotting` module is used by other helpers for plotting and creating figures.
    *   **Data Storage:** Admin credentials, approvals, and experiment results data must be stored in `Derivation/code/common/data`.
    *   **`vdm_equations.py` Content:** This file must include all available equations involved in the Void Dynamics Theory.
    *   **`constants.py` Content:** This file must contain all VDM-specific constants for use in experiments.
    *   **`io_paths.py` Purpose:** This helper must correctly route log and figure files to their respective folders.
    *   **`authorization/__init__.py` Design:** This file must be intentionally minimal to enable specific imports (e.g., `from common.authorization.approval import check_tag_approval`) and must not contain runtime logic.
    *   **Causality Module Design:** The `causality` module must be dependency-minimal (pure Python + math/random; numpy optional) and bounded algorithms with caps for large graphs. It must not contain I/O or approvals.

*   **Project Status & Roadmapping (Dependencies):**
    *   **RD Baseline Status:** RD baseline **must be proven** before Memory Steering Mechanism can proceed.
    *   **EFT/KG Branch Status:** EFT/KG branch is marked `[PLAUSIBLE]` until KPI-gated RESULTS pass.
    *   **RD "Canonical Model" Front-Speed:** RD "canonical model" front-speed claim must pass quantitative gates (`≤5% tolerance`).
    *   **Axiomatic Foundation Status:** Axiomatic foundation **must be complete** before EFT/KG Branch Validation and Discrete Action Recast can proceed.
    *   **Discrete Action Recast Status:** Discrete action recast **must be complete** before Kinetic Normalization from Discrete Action and True Conserved Quantity Discovery can proceed.
    *   **VDM-Fluids Equations Status:** Canonical equations for VDM-fluids **must be defined** before VDM-Fluids Corner Testbed can proceed.
    *   **Attention Graph Formalism Status:** Attention graph formalism **must be defined** before Extend Walkers to Attention Graphs can proceed.
    *   **Memory-Steering Harness Status:** Memory-steering acceptance harness **must be completed** before Memory-Steering System Integration can proceed.
    *   **Physics Validation CI Task:** A 'Physics Validation Task' **must be established and continuously run** within the CI pipeline.
    *   **Model Learning Diagnostic Tools:** The model **must learn to apply** diagnostic tools (e.g., tomography) without its core physics understanding being modified by them for Tier 9.

## 8. Physics, Mathematical & Code Constraints

*   **Universal Constants (FUM):**
    *   `$\alpha = 0.25$` (Universal learning rate for RE-VGSP)
    *   `$\beta = 0.1$` (Universal plasticity rate for GDSP)
    *   `$f_{ref} = 0.02$` (Universal reference frequency for time modulation)
    *   `$\phi_{sens} = 0.5$` (Universal phase sensitivity for time modulation)

*   **Physics Definitions & Formulas:**
    *   **Canonical Model:** The canonical model class is Reaction-Diffusion (RD).
    *   **Logarithmic First Integral:** `$Q(W,t) = \ln(W/(r-uW))-rt$` defines the logarithmic first integral, which must be constant (drift guard).
    *   **Potential Form (EFT):** The potential form for EFT must be `$V(\phi)=-\tfrac{1}{2}\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3$`.
    *   **Tachyonic Curvature:** `$\mu^2$` must be `$>0$` for tachyonic curvature.
    *   **Quartic Stabilizer:** `$\lambda$` must be `$>0$` for quartic stabilizer.
    *   **Cubic Tilt:** `$|\gamma|$` must be `$\ll \mu^2 \sqrt{\lambda}$` for small cubic tilt.
    *   **Azimuthal Mode Index:** `$\ell$` (azimuthal mode index) must be an integer `$\ge 0$`.
    *   **Plasticity Scale Cap:** The plasticity scale cap `$\alpha_{\text{plast}}$` must limit write magnitude such that `$\lVert \Delta^{+} \rVert \le \alpha_{\text{plast}}$`.
    *   **Mach Number:** The Mach number `$\mathrm{Ma}$` must be `$\ll 1$` for incompressible flows. LBM typically assumes Mach numbers `Ma ≲ 0.1` for weakly compressible flows.
    *   **Coefficient of Determination:** The coefficient of determination `$R^2$` must be in `$[0,1]$`.
    *   **Equation of State:** The equation-of-state parameter `$w$` is `0` (dust) for FRW residual test.
    *   **HLS $\to$ Skyrme Mapping:** Convention: `$C_{\rm match}=1$` for HLS $\to$ Skyrme mapping (trace/gauge choice fixed).
    *   **Secular Equation (Cylindrical Tube):** The secular equation for a cylindrical tube is `$\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\,\frac{I'_\ell(\kappa_{\rm in} R)}{I_\ell(\kappa_{\rm in} R)} = - \frac{K'_\ell(\kappa_{\rm out} R)}{K_\ell(\kappa_{\rm out} R)}$`.
    *   **Tachyonic Mode:** A mode is tachyonic if `$\kappa^2 > 0$`.
    *   **FRW Balance Control Variables:** Equation of state parameter `w` must be fixed to 0 (dust). Scaling law `ρ(a)` must be analytically set to `ρ_0 a^{-3}`. Time grid must be uniform `Δt`. Differentiation must use central differences.
    *   **Dark Photon Mass Definition:** Define mass as: $m_{A'}=g_D⟨S⟩$ after SSB; visible couplings $\propto \varepsilon$.
    *   **Physical Consistency (Nonsense Detectors):** Adhere to "nonsense detectors" to ensure physical consistency, including: Unitarity (no negative probabilities), Gauge Consistency (charges must cancel if the void field is gauged), Lorentz Invariance & Causality (maintain within EFT cutoffs; if bent, state where and how small), Portal Size (must be consistent with existing experimental bounds), Energy-Momentum Conservation ("Evaporation" must conserve energy-momentum, translated into decay, scattering, or phase change).
    *   **VDM Fluid Model Baseline Equations:** Incompressible Navier-Stokes, laminar flow.
    *   **VDM Fluid Model Regularized Variant:** Replace kinematic viscosity `ν` with `ν_eff` defined as `ν [1 + β Φ(‖∇u‖;τ_g,τ_u) + (1−β) Ψ(κ;τ_r)]`.
    *   **VDM Fluid Model `κ` and Activations:** `κ = ‖∇ × u‖` (vorticity magnitude), and `Φ,Ψ` must be soft-clamped activations (e.g., Softplus or logistic) with thresholds set by `τ_u,τ_g,τ_r`.
    *   **VDM Fluid Model `Φ` and `Ψ` Implementation:** Implement `Φ` using `softplus(G τ_g / c_u - 1.0)`. Implement `Ψ` using `softplus(κ τ_r / κ_0 - 1.0)`.
    *   **VDM Fluid Model `c_u` and `κ_0`:** Define `c_u` as `H/τ_u` and `κ_0` as `U_0/H`.
    *   **Conformal Metric:** The conformal metric **must be** `$g_{\mu\nu} = \phi^2 \eta_{\mu\nu}$` in Einstein Field Equations proof.
    *   **Total Void Evolution Rate:** The total void evolution rate `$\dot{W}$` **must be** the sum of `$\delta_{RE-VGSP}(W, t)$` and `$\delta_{GDSP}(W, t)$`.
    *   **Modulation Factors:** Modulation factors for `$\alpha$` and `$\beta$` **must be** mathematically derived from the domain's target sparsity and the void debt ratio (`$\beta/\alpha$`).
    *   **Bounded Potential:** The potential **must be made bounded** by default (e.g., using `$V(\phi)=-\tfrac{1}{2}\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4$`).
    *   **Local Covariant Conservation:** Local covariant conservation **must hold** (`$\nabla_\mu!\big(T^{\mu\nu}\Lambda+T^{\mu\nu}{\rm DM}+T^{\mu\nu}{\rm GW}+T^{\mu\nu}{\rm hor}\big)=0$`).
    *   **Causality/Locality:** Causality/locality must be ensured via a retarded kernel (`$K_{\rm ret}\propto\Theta(t-t'-|\mathbf x-\mathbf x'|)$` and normalized to GeV).
    *   **Partition Functions:** Partition functions **must guarantee** `$p_\Lambda+p_{\rm DM}+p_{\rm GW}=1$` with `$p_i\in[0,1]$`.
    *   **Observational Viability (Dark Energy):** Observational viability for dark energy must impose `$\,\big|w_{\rm eff}+1\big|\le \delta_w\, $` (e.g. `$\,\delta_w\sim 0.05\,$`) by requiring `$\,(\alpha_h/V_c)\,\dot S_{\rm hor}\ll 3H\,\rho_\Lambda\,$`.
    *   **Observational Viability (SIDM):** Observational viability for SIDM must ensure clusters satisfy `$\,(\sigma_T/m)\lesssim 10^{-3}\text{-}10^{-4}\ {\rm cm}^2\,{\rm g}^{-1}\,$`.
    *   **Structure Formation Constraint:** Structure formation constraint **must impose** `$\,f_{\rm inj}\ll 1\,$` for `$\,z\lesssim z_{\rm LSS}\,$`.
    *   **Horizon Entropy Restriction:** If desired, restrict `$\,\dot S_{\rm hor}\,$` to early epochs by a window `$\,W(t)\,$` with `$\,0\le W\le 1\,$` and replace `$\,\dot S_{\rm hor}\to W(t)\,\dot S_{\rm hor}\,$`.

*   **Unit & Dimensional Consistency:**
    *   **EFT Unit Convention:** Use natural units `c = ħ = k_B = 1`.
    *   **Wave Speed Unit Choice:** The wave speed `c` may be set to 1 by a benign rescaling of time/length units (e.g., choosing `Δt` and `a`, or `τ` and `a`). This is a units choice, not a constraint.
    *   **FRW RHS Units:** FRW RHS must be in `${\rm GeV}^2$` (natural units).
    *   **Continuity Equation RHS Units:** All Continuity Equation RHS must be in `${\rm GeV}^5$`.
    *   **Horizon Entropy Production Units:** `N` has units `${\rm GeV}^{-1}$`, `$\dot S_{\rm BH}$` and `$R_{\rm merg}$` are GeV, `$\Delta S_{\rm merg}$` is dimensionless, `$\Rightarrow \dot S_{\rm hor}$` is GeV.
    *   **Micro-informed Coefficients Units:** `$C_\alpha, C_\varepsilon$` are `$\mathcal O(1)$`, `$K_s$` in `${\rm GeV}$`, `$\kappa$` in `${\rm GeV}^2$`, `$|\Omega|$` in `${\rm GeV}$`, `$R_\ast$` in `${\rm GeV}^{-1}$`. Therefore, `$(|\Omega|\,R_\ast)$` is dimensionless, `$(\kappa/K_s)$` is GeV, and `$\alpha_h,\varepsilon_h$` are GeV.
    *   **Soliton Relations Units:** `$R_\ast$` in `${\rm GeV}^{-1}$`, `$X$` in `${\rm GeV}$`, `$m$` in `${\rm GeV}$`.
    *   **BH Entropy Units:** `$\dot S_{\rm BH}[{\rm GeV}],\ A[{\rm GeV}^{-2}],\ G[{\rm GeV}^{-2}],\ S_{\rm BH}\ \text{dimensionless}$`.
    *   **SU(2) Skyrme Microphysics Units:** `$F$` must be in [GeV], `$e$` dimensionless for SU(2) Skyrme Microphysics.
    *   **Unit Conversion ($v \to v/c$):** The unit conversion for `v` from km/s to natural units is `$v \to v/c$`, with `$c=2.99792458\times 10^5\ {\rm km/s}$`.
    *   **Dimensionless Groups (Memory Steering):** `Da` must be `np.inf` if `M0` is `0`. `Gam` must be `np.inf` if `L_scale` is `0`.
    *   **C-score:** `C_score` must be unitless.

*   **Boundary & Initial Conditions:**
    *   **General Requirements:** Boundary and initial conditions in `BC_IC_GEOMETRY.md` must link to equations/constants/symbols by anchor; do not restate them. The fitter and all residual/flux calculations must use the actual neighbor list (same stencil and BC as used during stepping). No complete-graph or dense approximations. When performing continuum integrations by parts, require either periodic BCs or no-flux (homogeneous Neumann) BCs (`n_hat * nabla phi = 0` on `partial Omega`).
    *   **Reaction-Diffusion (RD) Specifics:** Periodic BC (1D RD dispersion) must be enforced via periodic wrap in second-order difference stencil; conserves total mass `sum(u_i)`. Neumann BC (1D RD front speed): ghost cells must mirror interior; conserves total mass when reaction term `f === 0`. For conservation tests, use periodic BCs; Neumann BCs are reserved only for front-speed control runs. Use gated initial conditions (no pre-heating) for front-speed validation. Set far-ahead region exactly to `0.0` for front-speed initial conditions. Gate optional noise to the left side only for front-speed initial conditions. The far-field must remain near zero if using `Level=0.5` for front-speed tracking; always keep the far-field exactly zero until the front arrives for front-speed validation (gating is on by default). Keep amplitude small (linear regime) for dispersion; use an early-time fit window. Increase `N` and/or `T` as needed to ensure a clean linear regime and avoid boundary contamination. Ensure the front remains away from domain boundaries during the fit window for front-speed validation. The Tanh Step IC (RD front speed) requires the left region `u approx 1` (populated), and the right region `u = 0` (unpopulated). A near-void initial state is used for computational proof of logarithmic first integral.
    *   **Lattice Boltzmann Method (LBM) / Fluid Dynamics Specifics:** Periodic BC (2D Taylor-Green vortex): LBM streaming must use `np.roll`. Bounce-back No-slip (2D lid cavity): at solid boundaries, post-streaming populations must be reflected. Zou/He velocity BC (lid cavity top wall) imposes tangential velocity. Taylor-Green Vortex IC is used to validate viscosity recovery. Equilibrium IC is the default initialization for LBM. VDM Fluid Model Inlet BC can be uniform `u_x=U_0` or parabolic `u_x(y)=\frac{6U_0}{H^2}y(H-y)`, `u_y=0`. VDM Fluid Model Wall BC: no-penetration `u_n=0`, no-slip `u_t=0` (baseline). Do not relax the no-slip boundary condition for void-faithful fixes. VDM Fluid Model Outlet BC: Neumann on velocity, fixed reference pressure. VDM Fluid Model Initial Condition: start from rest; ramp inlet to `U_0` over `0.2\,H/U_0`. Do not change boundary laws to ensure `max(‖u‖)` remains finite.
    *   **Agency / Walker Specifics:** Periodic BC (walker glow): incoming flux from outside the domain must be taken from the opposite boundary. Neumann BC (walker glow): boundary incoming flux from outside must be zero. Absorbing Boundary (agency walkers): walkers that step outside `(Omega)` are removed. If an agency map `(M)` is logged, `(M|_partial_Omega = 0)` must be enforced for visualization. Reflecting Boundary (agency walkers): on attempted step `(Delta x)` that exits `(Omega)`, reflect the normal component at the boundary. Uniform Quiescent Agency Field serves as a clean baseline. Seeded Walker Distribution (Poisson) must be deterministic when seeded; supports side-by-side BC comparisons.

*   **Numerical Calculation Constraints:**
    *   **LBM Viscosity Tau Constraint:** The lattice relaxation time `τ` must be `> 0.5` for positive viscosity.
    *   **Division-by-Zero Prevention:** `1e-15` must be added to kinematic viscosity (`ν`) for Reynolds number, diffusivity (`D`) for Péclet number, and `U` or `D` for Damköhler number computations to prevent division-by-zero.
    *   **Damköhler Number Parameter Constraints:** `U` (`>0`), `L` (`>0`), `k` (`≥0`); `D` required for `mode="diffusive"`.
    *   **Damköhler Number Error Handling:** The `damkohler` function must raise a `ValueError` if the `mode` is not recognized or if `D` is missing for `mode="diffusive"`.
    *   **KPP Front Speed Preconditions:** `D` must be `≥ 0` and `r` must be `≥ 0`. A `ValueError` must be raised otherwise.
    *   **RD From Lattice Gamma Fallback:** If `gamma` is `None` in `LatticeParams` for `rd_from_lattice`, it must fall back to the site Laplacian map (`D = J a^2` and raw `r,u,λ`).
    *   **KG C2 From Lattice Convention:** The `kg_c2_from_lattice` function's `convention` parameter must be `'per-site'` or `'per-edge'`. A `ValueError` must be raised otherwise.
    *   **Stabilized Vacuum Lambda = 0:** If `p.lam` is `0` in `stabilized_vacuum`, the small-`λ` limit `φ* = r/α` (positive branch) must be used. `p.alpha` must be `> 0` for this case, otherwise a `ValueError` is raised.
    *   **Plotting Style Parameters:** Plots must update `plt.rcParams` with `figure.dpi: 100`, `savefig.dpi: 160`, `axes.grid: True`, `grid.alpha: 0.3`, `font.size: 11`.
    *   **Logarithmic Axis Data Sanitization:** When `logx` or `logy` is true, data values `x` or `y` must be sanitized to avoid `log(<=0)` by replacing non-positive values with `1e-30`.

## 9. Simulation Settings & Geometry

*   **General Simulation Parameters:**
    *   **VDM Fluid Model Nondimensional Control:** Set `H = 1`, `U₀ = 1`. Calculate `Re` as `U_0 H / ν`. Start simulations with `Re = 100`. Set kinematic viscosity `ν = 0.01` when `Re = 100`, `H = 1`, `U₀ = 1`. Set the end time `T` to `40 H/U_0`.
    *   **VDM Fluid Model Parameter Sweeps:** Conduct two sweeps: (A) Geometry sweep: `r_c = {0, 0.02, 0.05, 0.10}H`, baseline and VDM on. (B) VDM ablation: hold `r_c=0`, vary `$\beta \in \{0.0,0.3,0.6,0.9\}$`.
    *   **VDM Fluid Model Parameter Defaults:** Set the VDM mix weight `β = 0.6`. Set `τ_u = 1.0 H/U_0`. Set `τ_g = 0.05 H/U_0`. Set `τ_r = 0.5 H/U_0`. Set `c_u = 1` (derived from `H/τ_u`). Set `κ_0 = 1` (derived from `U_0/H`).
    *   **VDM Fluid Model Calibration Advice:** If `weights ≈ 0.6` are observed, set `β` such that `exp(-β D) ≈ 0.6` in typical high-stress regions. When `D = 1`, set `β ≈ ln(1/0.6) ≈ 0.5108`.
    *   **Constants (Metriplectic):** `dg_tol <= 1e-12`. `gate_slope >= 2.9`. `gate_R2 >= 0.999`. `dt_sweep_small > 0`. `j_only_rev_strict <= 1e-12`. `j_only_rev_cap <= 1e-10` (logged if strict fails, but does not change pass/fail). `j_only_l2_cap <= 1e-10`. `robust_v5_pass_rate_min >= 0.80`. `lyap_tol_pos <= 1e-12`. `strang_R2_min >= 0.999`.
    *   **Constants (FRW Residual):** `tol_rms <= 1e-6`.
    *   **Constants (A6 Collapse):** `env_max_threshold <= 0.02`.
    *   **`K` (Convergence Threshold):** Fixed at `0.5` for most numerical simulations. If `|ΔW_total| > K`, the simulation must be halted, and `t_final` recorded as the current step.
    *   **`ParentUniverse`:** Must be initialized with `cosmic_debt = 0.84`.
    *   **Higgs Field:** Symmetry breaking must be tracked (e.g., when `abs(H[t+1])` exceeds a threshold like `0.1`).
    *   **Gauge Coupling Constants:** For SU(3), SU(2), and U(1) must be calculated as `$\alpha_{base} / (1 + \ln(1 + r \times t_{final}))$` for respective ranks `r`.
    *   **Void Debt Ratio:** The void debt ratio `$\beta/\alpha$` is a fixed universal constant for domain modulation calculations (0.4).
    *   **Child Universe:** For Cosmogenesis, the child universe must evolve under void dynamics, and the resulting sparsity must be compared to the expected 84% from inherited debt.
    *   **Dark Matter Runs:** The simulation for Dark Matter must be executed `NUM_RUNS = 10` times to gather statistics.
    *   **Higgs Reference Scale:** The `higgs_reference_scale` must be calculated by dividing the experimental Higgs mass (124.0 GeV) by the `final_vev`, and `predicted_higgs_mass` obtained by multiplying `final_vev` by this scale.
    *   **Light Speed Scale:** The `light_speed_scale` must be computed by dividing the `target_light_speed` (299,792,458 m/s) by `final_value`. `predicted_light_speed` is then `final_value * light_speed_scale`.
    *   **Advisory Policy Parameter Nudges:** The `AdvisoryPolicy` may suggest bounded numerical parameter nudges (τ, u_clamp, U_lid).
    *   **Explicit Euler Solver:** Use **Explicit Euler** solver for RD front-speed and dispersion validation.
    *   **Small IID Gaussian Amplitude:** Start from small iid Gaussian amplitude `amp0 << 1` for dispersion validation to stay in the linear regime.
    *   **Early-Mid Window:** Use an early-mid window for fitting dispersion to avoid startup transients while staying in the linear regime.
    *   **Robust Linear Fit:** Use robust linear fit with MAD rejection for front-speed validation; apply median-slope fallback if needed.
    *   **GDSP Budget Gate:** `edges_touched ≤ budget_prune + 2·budget_bridge + budget_grow`.
    *   **Safety Rails:** System **must abort** if class min-degree floors/E-I checks would breach.
    *   **Emergent Budgets:** Emergent budgets **must be computed** from signals; **no static knobs**; environment knobs are debug-only.
    *   **Partition Kernels:** Partition kernels **must operate** on type-specific subsets.
    *   **GrowthArbiter:** `GrowthArbiter` **must handle** class-specific growth commands.
    *   **NeuronType Enumeration:** `NeuronType` enumeration (**INTEGRATOR, MESSENGER**, etc.) **must be defined** in a shared constants module.
    *   **Connectome Augmentation:** `Connectome` **must be augmented** with a type vector.
    *   **Neuron Class Learning Parameters:** Different neuron classes **must have** distinct learning parameters.
    *   **Messenger Neurons:** Messenger neurons **must be** fast-learning "scratchpads".
    *   **Integrator Neurons:** Integrator neurons **must be** stable long-term memory.
    *   **Parameter Adjustment (Tachyon Condensation):** Adjustment of `num_brackets`, `dr`, or $R$ range is required for re-attempt after parameter refinement.

*   **Geometry & Mesh (VDM Fluid Model Specific):**
    *   **Geometry:** The channel must be 2-D and have a 90° bend. Set inlet length `L_in` to `8H` and outlet length `L_out` to `12H`. The inner fillet radius `r_c` must be selected from `{0, 0.02H, 0.05H, 0.1H}`. Use `r_c = 0` to simulate a sharp corner. Do not alter the wall geometry for void-faithful fixes.
    *   **Mesh:** Use a graded quad/tri mesh. Refine the mesh near the inner wall. Set the base mesh resolution `Δ` to `H/80`. Apply geometric grading to achieve `Δ_min ≈ H/400`. Apply refinement within the box `Ω_refine = [-H..+H] × [-H..+H]`, centered at the corner.

## 10. File System & Scripting

*   **File System & Paths:**
    *   **DB Path Logging:** When a database path is resolved, the module **must log** its provenance (source of the path) at INFO level.
    *   **DB Schema Initialization:** On first creation, the module **must initialize** the schema.
    *   **DB Path Discovery Order:** Discover database paths in this order: CLI flags, environment variables (`VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`), optional `.env` files.
    *   **DB Path Resolution:** Public DB Path must be explicitly set via `VDM_APPROVAL_DB` or `--db` flag. Admin DB path can be set via `VDM_APPROVAL_ADMIN_DB` or defaults.
    *   **Results DB Path:** Per-domain results DBs must follow the path `Derivation/code/outputs/databases/<domain>.sqlite3`. Parent directories for the DB path must exist and be writable.
    *   **Directory Creation:** Directories for DB paths must be created if they do not exist (`parents=True`, `exist_ok=True`).
    *   **Table Naming:** Experiment table names must be sanitized script stems (e.g., `kg_light_cone`).
    *   **Table Uniqueness Constraint:** Experiment tables must have a `UNIQUE(tag, batch)` constraint.
    *   **Identifier Sanitization:** Identifiers must be lowercased, replace non `[a-zA-Z0-9_]` with underscores, and be prefixed with `t_` if they start with a digit. Only `[a-z0-9_]+` characters are allowed in sanitized identifiers.
    *   **Tag Allowance Check:** The `_ensure_tag_allowed` function must validate that the tag appears in the domain's approval manifest, specifically in `allowed_tags` and having an entry in `approvals[tag]`. This check is skipped if `RESULTSDB_SKIP_APPROVAL_CHECK=1` is set.
    *   **Approval Manifest Structure:** An approval manifest for a domain must be located at `code/physics/<domain>/APPROVAL.json` or `Derivation/<domain>/APPROVAL.json`. It must be valid JSON, contain `allowed_tags`, and an `approvals` dictionary with an entry for each allowed tag.
    *   **JSON Merge Behavior:** When merging JSON objects, if the existing content is not a dictionary, it must be treated as `{"_": base}` before merging.

*   **Scripting & Automation:**
    *   **Shell Script Discipline:** Shell scripts must exit on error (`set -e`), reference unset variables (`set -u`), and use pipefail (`set -o pipefail`).
    *   **Idempotent File Creation:** When creating files with `init_dark_photon_quantum_docs_v2.sh`, do not overwrite existing files.
    *   **Output Messaging:** Shell scripts must print "✓ Created: \$path" for each successfully created file.
    *   **Mandatory Argument:** `init_dark_photon_quantum_docs_v2.sh` requires a target directory path as an argument.
    *   **Function Definition:** Per-file creators must be defined as functions (e.g., `create_readme()`).
    *   **Here-Doc Usage:** Use `cat > "$path" <<'EOF'` for here-doc syntax.

## Key Highlights

* All project Tiers must comply with foundational axioms requiring measurable observables and dimensionless group scaling, ensuring every non-trivial statement maps to a falsifiable test protocol.
* The Void Dynamics Model integrates a reaction-diffusion equation for substrate reshaping and a hyperbolic equation for finite-speed signal transport, with a void-debt gate coupling them and throttling transport.
* Documentation and reporting must be whitepaper-grade, evidence-driven, and include numeric figure captions, explicit pass/fail gates, full provenance, and falsifiable claims with metrics and thresholds.
* All simulations must produce figures with numeric captions and paired CSV/JSON sidecars recording seed, commit hash, and metrics; failed runs must be quarantined with detailed contradiction reports.
* Rigorous validation is paramount, requiring numerical checks for axioms and conservation laws, ensuring reproducibility through recorded seeds, and failing the CI pipeline on any single test failure.
* A strict approval system mandates explicit authorization for all scripts and rejects unapproved runs, with tamper-evident auditing using SHA-256 row hashes for all experiment results.
* Coefficients for Effective Field Theories must be rigorously derived directly from the discrete model rules and demonstrate that higher-derivative terms are zero or suppressed, avoiding external postulates.
* The project enforces a tiered maturity ladder (T0-T9) with clear promotion gates, and critical development paths, like Memory Steering, are explicitly dependent on prior components such as the RD baseline being proven.

---

*Powered by AI Content Suite & Gemini*
