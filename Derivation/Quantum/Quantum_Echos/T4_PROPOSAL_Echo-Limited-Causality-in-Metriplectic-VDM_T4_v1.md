<!-- ATTENTION! The proposal documents you create MUST BE whitepaper-grade documents with full structure, full narrative, MathJax-rendered equations (Meaning use Github MathJax syntax, $ ... $ and $$ ... $$ instead of other syntax), numeric figure captions tied to actual artifacts if using any for background, explicit thresholds with pass/fail gates, and provenance. You need to imagine if the document will be getting submitted for proposal at the most highly respected and quality Physics journals on Earth. -->

# White Paper Proposal Template

It is MANDATORY and IMPORTANT to include the substance of the outlined topics. The length of the proposal should not exceed five U.S. letter-sized pages (including figures and references). Language and phrasing in this document should be objective and third perspectivem, placing the VDM as the subject. When describing methods the focus should be on what is predicted, planned, and what will be done rather than using perspective based verbiage (example: "We/I/They propose a metriplectic..." would be wrong. Instead, do this "Proposed in this document is a metriplectic..." or even "VDM proposes a metriplectic...")

> {git rev-parse HEAD} and put the latest commit here for provenance.
> Additionally, create a hash salted with the commit and put it here.

<!-- This MUST included the grade of proposal this is. The grade of the proposal should be the same as the grade of the RESULTS_* if the runs pass.

Shown in a table below is the T0–T9 maturity ladder. This ladder distinguishes between:

- **Meters/instruments** (T2): Proven testing measurement apparatus
- **Phenomena** (T3+): Making physics claims with those proven meters
- **Preregistered claims** (T4-T6): Formal hypothesis testing
- **Robustness & validation** (T7-T8): Out-of-sample prediction
- **Reproduction** (T9): External verification

Tier Grades

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

Additionally, if this PROPOSAL document is graded above T0, there should be existing supporting work referenced for each tier in sequence. For example, if a T4 experiment is proposed there must be a T0, T1, T2, and T3 that exists within the repository referenced with paths for any existing PROPOSAL and RESULTS documents listed. The figures and logs can also be referenced from each of those prior work items. There should be at a minimum of one for each, but no max limit.

In order for any experiment to run or pass, PROPOSAL_ documents MUST be created. Reference some brief approval standards here C:\git\Prometheus_VDM\derivation\code\common\authorization\README.md
-->

## 1. Tier Grade, Proposal Title and Date

**Tier Grade:** T4 (Prereg) — building on existing T0–T3 artifacts in canon (see §4 Provenance & maturity ladder) 

**Proposal Title:** *Echo‑Limited Causality in Metriplectic VDM: Does $J\oplus M$ Impose a Finite Propagation Speed on the Agency Field?*

**Date:** October 26, 2025
**Commit:** 09f571e8edaf344582b2db86aa4e5e1bee25c615

## 2. List of proposers and associated institutions/companies

**Proposer:** Justin K. Lietz — Prometheus_VDM / VDM Project (independent research program)

## 3. Abstract

Proposed in this document is a preregistered experiment to test a central causality claim of the Void Dynamics Model (VDM): when metriplectic dynamics couple a conservative “$J$” limb (hyperbolic/Klein–Gordon‑type) to a dissipative “$M$” limb (reaction–diffusion/agency field), the interaction enforces a finite domain of influence on information transport in the $M$ limb; operational propagation speed must not exceed the $J$‑sector characteristic speed $c$ derived from the lattice microparameters. The experiment uses VDM’s canonical equations and gates to (i) instrument a reversible $J$ “echo window,” (ii) drive a localized perturbation, (iii) measure first‑arrival and level‑set front times for the agency field $C(x,t)$, and (iv) apply pass/fail cones relative to $c$. Outcomes adjudicate whether $J\oplus M$ dynamics inherit the locality cone demanded by VDM Axiom A2 (Local Causality) and A4 (Dual Generators) without adding external forces. Results will be published as RESULTS_* with artifacted JSON/CSV, figures, and contradiction reports per repository standards.   

## 4. Background & Scientific Rationale

**VDM canon & scope.** VDM asserts a void‑field program with axioms A0–A7 (Closure, Void Primacy, Local Causality, Symmetry, Metriplectic split, Entropy law, Scale program, Measurability). Axiom A4 structures time‑evolution as a metriplectic sum with degeneracies $J^\top=-J$, $M^\top=M!\ge!0$, and $J,\delta\Sigma=0$, $M,\delta\mathcal I=0$. Axiom A2 requires finite propagation of influence (locality cone) for appropriate branches. 

**Canonical equations.** The $J$ limb admits a Klein–Gordon (KG) continuum limit, $\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0$ with $c^{2}=2Ja^{2}$ derived exactly from the discrete action; the $M$ limb admits an overdamped reaction–diffusion (RD) limit, $\partial_t\phi=D\nabla^{2}\phi + f(\phi)$, and for the agency field $C$ specifically, $\partial_t C = D\nabla^2 C - \gamma C + S(x,t)$ with standard Green‑function causal solutions under retarded kernels. 

**Problem.** RD equations are parabolic and analytically nonlocal in support (instantaneous tails), whereas KG is hyperbolic with a finite domain of dependence. The open question is whether the metriplectic coupling $J\oplus M$ makes operational propagation in the $M$ limb respect the $J$‑sector cone in the coupled system without ad hoc constraints. This is a direct test of VDM’s locality stance (A2) and metriplectic degeneracy (A4) in a mixed‑flow regime and links to causal‑process accounts requiring finite‑speed mediation.  

**Maturity ladder & provenance.**

* **T0 (Concept):** Axioms A0–A7 and metriplectic structure declared canonically. 
* **T1 (Proto‑model):** Discrete action, KG/RD limits, agency‑field equations compiled in EQUATIONS.md. 
* **T2 (Instrument):** Validated meters include RD dispersion and Fisher–KPP front speed with quantitative gates (e.g., $c_{\text{front}}=2\sqrt{Dr}$; PROVEN). 
* **T3 (Smoke):** Locality diagnostics for KG (cone slope $\approx c$), Noether/H‑theorem monitors, dimensionless scaling program (A6). 
  This proposal (T4) preregisters a falsifiable causality claim using those meters.

**Novelty & impact.** Demonstrating a cone‑limited $M$ limb under $J\oplus M$ would provide a unifying causal constraint across conservative/dissipative branches, clarifying how “measurement/agency” processes inherit relativistic structure from reversible dynamics within VDM’s axiomatic closure. This would enable subsequent cross‑checks toward EFT/QFT compatibility and observational proxies. 

**Critiques & mitigation.** (i) “Parabolic implies instantaneous tails”: the design uses operational speeds (first‑arrival/level‑set) and cone gates rather than strict support. (ii) “Numerical artifacts”: meters are treated as instruments with stability/CFL and conservation gates; uncertainties are reported with multi‑seed and resolution sweeps per RESULTS standards and documentation rules.  

## 5. Intellectual Merit and Procedure

**(1) Importance.** The test probes VDM’s axiom‑level locality by measuring whether coupling alone constrains dissipative transport speeds; this is decisive for theory coherence.  

**(2) Potential impact.** A positive result supports a metriplectic bridge between quantum‑like reversible dynamics and classical measurement‑like flows, setting stage for out‑of‑time‑order echo diagnostics in later tiers. A negative result triggers a CONTRADICTION_REPORT and theory adjustment. 

**(3) Clarity & approach.** The plan uses only canon equations, dimensionless groups, and gate‑driven meters (Noether, H‑theorem, dispersion, front‑speeds), avoiding external forces and adhering to axiomatic closure. 

**(4) Rigor & discipline.** Thresholded gates, preregistration, and explicit uncertainty are specified; logical and mathematical presentation follows repository rules for rigor and proof analysis.  

### 5.1 Experimental Setup and Diagnostics

**Governing fields.**

* $J$ limb (reversible): $\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0$, $c^2=2Ja^2$. 
* $M$ limb (agency): $\partial_t C = D\nabla^2 C - \gamma C + S(\phi,\dot\phi,\nabla\phi)$; canonical source structure follows VDM agency definitions. 

**Metriplectic split (A4).** $\partial_t q = J(q),\delta \mathcal I/\delta q + M(q),\delta \Sigma/\delta q$ with degeneracies; diagnostic invariants $g_1,g_2$ are computed to verify $J,\delta\Sigma=0$, $M,\delta\mathcal I=0$ to tolerance. 

**Dimensionless program (A6).** Use $\tilde t=\gamma t$, $\tilde x=x/\ell_D$, $\ell_D=\sqrt{D/\gamma}$ for $C$; normalize $r/(ct)$ for cone plotting; maintain unit‑free acceptance bands. 

**Stimulus & echo window.** Localized reversible “kick” in $\phi$ at $t=0$ followed by a time‑symmetric $J$ echo window (forward–backward split) to bound numerical dispersion and isolate causal mediation into $C$. No body forces are added to $C$ beyond $S(\cdot)$. 

**Primary diagnostics.**

1. **Cone test (arrival‑time):** For concentric radii ${r_k}$, compute $t_{50%}(r_k)$ when $C$ crosses a pre‑registered fractional level of its local peak; estimate $\hat v(r_k)=r_k/t_{50%}(r_k)$.
2. **Front test (level‑set):** Track $C=\theta$ isocontours; regress $\hat c_{\text{front}}$ vs $c$.
3. **Energy/entropy monitors:** Noether energy drift in $J$ limb; discrete Lyapunov decrease for $M$ limb.
4. **Degeneracy residuals:** $g_1,g_2$ per A4 notes.  

**Meters & numbers.** RD front/dispersion meters (validated); KG locality meter; agency‑field discrete update with CFL guard. Defaults (e.g., $D$, $r$, grid sizes) taken from CONSTANTS.md unless otherwise stated.  

**Optional samplers.** Walker‑based local samplers (activity density $\rho$; message packets $m_w$) provide sparse arrival detection and cross‑checks; definitions per symbols sheet.  

**Quality gates (pass/fail).**

* **Cone gate (primary):** $\max_{r,t}\hat v(r)\ \le\ (1+\varepsilon_c),c$ with $\varepsilon_c=0.02$, across $\ge 8$ seeds and two resolutions; any single breach beyond statistical CI triggers fail.
* **Noether gate (J):** $|\Delta \mathcal H|/\mathcal H_0 \le 10^{-8}$ per $J$‑period (grid‑refined).
* **H‑theorem gate (M):** $\Delta \mathcal L \le 0$ per step with discrete‑gradient update; zero crossings investigated.
* **Degeneracy gate (A4):** $g_1,g_2 \le 10^{-10}$ (grid‑refined).
* **RD meter sanity:** Reproduce $\sigma(k)=r-Dk^2$ and $c_{\text{front}}=2\sqrt{Dr}$ within documented tolerances prior to main runs. 

**Equipment / compute.** AMD ROCm stack (MI‑class GPUs or CPU fallback), Linux, FP64 where required; solver tolerances and utilization logged; environment captured via `systemspecs` per RESULTS standards. Measurement limitations (precision, aliasing, boundary) are noted and mitigated with standard numerical practice.  

### 5.2 Experimental runplan

**Plan to employ resources.**

1. Calibrate meters (RD dispersion/front; KG locality; agency update stability).
2. Run $J$‑only echo window sanity to pin $c$ and Noether drift.
3. Activate $J\oplus M$ coupling with preregistered $S(\cdot)$; execute impulse and collect $C$ fields.
4. Compute arrival and front metrics; produce cone plots in $(r/(ct),C)$ space.
5. Sweep grid/time resolutions and seeds; repeat with altered $D,\gamma$ to test dimensionless collapse. 

**Runtime estimate & datasets.** Wall‑clock and storage footprints are logged stage‑wise; processed data are CSV/JSON with commit and seed in filenames per RESULTS standards. 

**Success action.** If all gates pass, the claim is promoted to **RESULTS_*** with **T4 (Prereg)** grade; thresholds, numeric figure captions, and artifact paths are registered per RESULTS_PAPER_STANDARDS. **T5 (Pilot)** runs are then scheduled to execute the preregistered design at limited scale (multiple seeds/hardware, minimal parameter set). Contingent on T5 success, a **T6 (Main Result)** execution is conducted at full preregistered scope. Post‑T6, **T7 (Out‑of‑sample prediction)** tests and **T8 (Robustness validation & parameter sweeps)** are undertaken. Planning for **T9 (External verification/reproduction)** proceeds in parallel with artifact packaging.

> **Notes for editors (do not include in the final PDF):**
> – “Register thresholds, figures, and artifact paths” refers to the RESULTS_PAPER_STANDARDS requirements for numeric captions, CSV/JSON basenames, seed+commit in captions, and contradiction reports on gate failure. 
> – If an independent OTOC/echo‑witness thread is planned, reference it explicitly as a **separate** preregistered investigation that begins after T6 promotion.

---

### Minimal ladder plan for this project (for the “Tier Grade” box)

* **T4 (Prereg):** Formal preregistration and first execution against the stated gates (pass/fail recorded; no novelty claims beyond the preregistered hypothesis). 
* **T5 (Pilot):** Limited‑scale confirmation of protocol fidelity (multi‑seed/hardware sanity, stable estimates, no scope expansion). 
* **T6 (Main Result):** Full‑scale preregistered run; artifact‑pinned figures with numeric captions and provenance.
* **T7 (Out‑of‑sample prediction):** Hold‑out scenarios/circuits/parameter regimes not seen in T4–T6. 
* **T8 (Robustness & sweeps):** Systematic parameter sweeps and stress tests; document stability regions and failure modes. 
* **T9 (External verification):** Independent reproduction by external parties; publish repro bundle. 
 
**Failure action.** Emit CONTRADICTION_REPORT (gate, threshold, seed, commit, artifact pointer); analyze guilty lemma versus axioms per proof‑analysis rules; propose revised coupling or scope adjustment and re‑run as T1/T2.  

**Publication / display.** Results will be posted as RESULTS_* whitepaper‑grade documents with MathJax equations, numeric figure captions, provenance, and explicit pass/fail logs. Approvals follow the repository authorization policy (path: `derivation\code\common\authorization\README.md`). 

## 6. Personnel

**Role of proposer (Justin K. Lietz).** VDM architecture owner and experiment runner: designs preregistration and gates; implements solver configurations and meters; executes runs; performs uncertainty analysis; curates artifacts (JSON/CSV/figures); authors RESULTS_* according to repository writing standards. Team practices follow the project’s objective decision‑making rules (probabilistic confidence, red‑teaming) and adaptive‑organization guidance (transparent planning, range preservation).  

## 7. References

* **VDM Axioms (A0–A7), metriplectic split and locality requirements.** AXIOMS.md. 
* **Canonical equations (KG/RD/agency), meters (dispersion/front), and discretizations.** EQUATIONS.md. 
* **Constants & defaults for experiments (e.g., $D$, $r$, grid sizes, CFL).** CONSTANTS.md. 
* **Symbols & walker instrumentation used for optional samplers.** SYMBOLS.md. 
* **Mathematical rigor & proof‑analysis discipline.** Rules for Rigorous Mathematical Inquiry. 
* **Objective decision‑making & preregistration norms.** Rules for Objective Decision‑Making & Truth‑Seeking. 
* **Technical & numerical principles (sampling/filters/FFT/caution).** Compendium of Technical & Scientific Principles. 
* **Formal logic & definitional precision for presentation.** Rules from Logic/Set Theory/Discrete Math. 
* **Adaptive systems / agents (supporting walker semantics).** Rules for How Adaptation Builds Complexity. 
* **Data‑science & documentation rules (uncertainty, CV, calibration).** Rules for Data Science & Documentation. 
* **Causal systems & finite‑speed mediation rationale.** Rules for Causal Systems. 
* **Adaptive organizations & project culture.** Rules for Adaptive Organizations & Individual Growth. 
* **Whitepaper/Results authoring policy (structure, gates, artifacts).** PROPOSAL_PAPER_TEMPLATE / RESULTS_PAPER_STANDARDS.  

---

**Scope and compliance note.** Language is objective and third‑person; VDM is the subject. Claims are bounded by axioms and meters; thresholds are preregistered; no novelty is claimed for standard results (e.g., Fisher–KPP). All metrics map to equations and gates; failures will be reported with CONTRADICTION_REPORTs per RESULTS standards. 
