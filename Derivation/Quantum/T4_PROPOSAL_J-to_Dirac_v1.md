
# 1. T4 (Prereg) - T4 — J→Dirac‑Aligned False‑Vacuum Metastability & Void‑Debt Asymmetry (Preregistration v1)

> Created Date:  2025-10-30  
> Upstream commit:  
> Salted provenance hash: d517ec575ce4af31bccfffc42bf3e84cfbe1ef6cfd1b625403ee6e6923ba9b1a  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: Dual-license (academic open use + commercial by written permission of Justin K. Lietz)  
> Short summary (one sentence TL;DR):  Preregistered scalar‑field false‑vacuum program rewritten to (i) front‑load symmetry regime flags, (ii) add ablation/nulls and explicit asymmetry gate, and (iii) constrain any metric leg to be Lindblad‑compatible; retains thin‑wall/lifetime gates and charge‑production routes.

## 2. List of proposers and associated institutions/companies

**Author/PI:** Justin K. Lietz — Neuroca AI (VDM program): design, prereg approval, interpretation, RESULTS authorship.  
**Implementer(s):** Justin K. Lietz + VDM physicist‑coding agent — runners/analysis per clean architecture; compliance snapshots; gate matrix; artifact governance.

## 3. Abstract

Proposed here is a preregistered, instrument‑grade study of scalar‑field **false‑vacuum metastability** and a minimal analogue of **matter–antimatter asymmetry** (“void‑debt”) inside VDM’s A4 split. This rewrite integrates the **J→Dirac** directives: (i) fermions are not claimed from a scalar; fermionic claims require a spinor/Dirac limb in J; (ii) any **metric (M)** leg is treated as **Lindblad‑compatible** decoherence (complete positivity, trace preservation, entropy monotonicity); (iii) the apparent tension between a conserved invariant and a net asymmetry is resolved by declaring **symmetry regimes** up front with explicit ablations. The original thin‑wall, lifetime, and charge‑production gates are retained with minor clarifications to meters and regime flags. fileciteturn1file1 fileciteturn1file11

## 4. Background & Scientific Rationale

**VDM axioms & split.** State \(q\) evolves under A0–A7 with Poisson (J) and metric (M) legs; predictions are framed in dimensionless groups. This program is J‑dominant (reversible waves, bubble kinematics) with an *optional*, ledgered M micro‑step only for stabilizing numerics, now constrained to Lindblad‑safe behavior. fileciteturn1file15

**Physics target.** A tilted double‑well scalar potential yields false and true vacua; decay proceeds by **bubble nucleation** and growth. Asymmetry generation borrows Sakharov conditions via out‑of‑equilibrium walls and either a **chemical potential** or **CP‑pumping** coupling. fileciteturn1file15

**J→Dirac alignment (scope note).** No fermionic matter is asserted in this scalar prereg. The program explicitly adopts: “fermions from J” only after upgrading to a **spinor Dirac limb** with appropriate discretization and gauge linking; **M** is reserved for **decoherence/entropy** (Lindblad‑compatible), and **J+M** for metriplectic coupling tests. Those upgrades live in parallel T4s and inform meters but are not required to pass the scalar false‑vacuum gates here. fileciteturn1file11 fileciteturn1file12

## 5. Intellectual Merit and Procedure

**Importance.** False‑vacuum decay and baryogenesis analogues test VDM’s ability to express metastability and controlled asymmetry within A4 without external “forces.”  
**Impact.** Passing the prereg produces artifact‑grade evidence that A4 supports metastability and controllable asymmetry and that asymmetry collapses under symmetry restoration; failure with meters green yields a contradiction report for targeted revision.  
**Approach & rigor.** Explicit meters (determinism receipts; operator/BC identity; entropy ledger if M used), predeclared thresholds with resolution checks, and ablations that toggle symmetry breakers. fileciteturn1file14

### 5.1 Experimental Setup and Diagnostics

**Fields & functionals (minimal working form).**  
β‑field with tilted double‑well potential \( V_\beta(\beta)=\tfrac{\lambda}{4}(\beta^2-v^2)^2+\epsilon\,\beta \) with small tilt \(\epsilon\); announcer fields \(\mathcal A\) mediate currents; an optional conserved B‑charge current \(J_B^\mu\). Two asymmetry routes are preregistered: (i) add \(\mu_B J_B^0\) (grand‑canonical bias); (ii) couple \(\beta\) to announcer curvature via a Chern–Simons–type term with coefficient \(\kappa_{CP}\). Action/entropy are schematic:  
\[\mathcal I[q]=\int (|\nabla\beta|^2 + V_\beta + \mathcal L_\mathcal A + \mathcal L_\text{int})\,dx,\quad
\Sigma[q]=\Sigma_\mathcal A\ (\text{optional, small}).\]  
J drives the dynamics; any M step is micro, ledgered, and (per rewrite) Lindblad‑compatible. fileciteturn1file13

**Domain, BCs, integrators.** 2D square \(L\times L\); reflective BCs (or periodic for β‑only checks). J‑dominant integrators (Störmer–Verlet or split‑step Strang). If M is enabled, use discrete‑gradient flow with entropy ledger. Diagnostics: potential/gradient energy budgets; bubble radius estimator; wall tension \(\sigma\) (static kink fit); survival analysis (many seeds); net \(\Delta Q_B\) with CIs; compliance snapshot. fileciteturn1file17

**Pre‑Run Config Requirements.** Approval manifests, schema/spec JSONs, and prereg metadata must be present per template (paths and keys as specified). fileciteturn1file14

**Meters (must print before stepping).** Determinism receipts (threads/BLAS/FFT/plan; checkpoint equality clause), operator/BC identity echo, H‑theorem ledger if M used (\(\Delta L_h\le 0\) micro‑tol), zero‑signal floors for nucleation and charge metrics. fileciteturn1file17

**Lindblad‑compatibility (if M used).** Numerically verify complete positivity (eigs of \(\rho\) ≥ 0 to tolerance), trace preservation (\(\mathrm{Tr}\,\rho=1\pm 10^{-12}\)), and entropy monotonicity (slack ≤ \(10^{-10}\)). Degeneracy properties under J+M: M leaves H invariant to \(\le 10^{-10}\); J leaves S invariant to \(\le 10^{-10}\). fileciteturn1file11

### 5.2 Experimental Runplan (risk‑reduced)

1) **Meters first (tiny grids).** Reversibility ≤ \(10^{-12}\); operator/BC match; determinism receipts; (if M) H‑theorem micro‑tol.  
2) **Thin‑wall pilot.** Measure \(\sigma\), \(\Delta V\); seed bubbles to bracket \(R_c\); size \(\Delta t\) ladder.  
3) **Lifetime pilot.** 50–100 seeds; validate exponential tail and set floors.  
4) **Asymmetry pilot.** Small \(\mu_B\) or \(\kappa_{CP}\) sweep; estimate \(\delta_Q\) and slope; finalize gates.  
5) **Full prereg execution.** Run prereg seeds/horizons; compute BCa‑bootstrap CIs (10k); assemble gate matrix; publish RESULTS. fileciteturn1file16

## 6. Hypotheses, Variables, and KPI Gates (pre‑registered)

**Dimensionless program (A6).** Use \( \Pi_1=\Delta V/\sigma,\ \Pi_2=\ell\,\Gamma^{1/d},\ \Pi_3=\mu_B/T_\text{eff}\ \text{or}\ \kappa_{CP}/\kappa_0,\ \Pi_4=\xi/L \). fileciteturn1file18

### H‑A: Bubble nucleation & thin‑wall scaling (β‑only)
* **Critical radius:** \(R_c=\kappa_d\,\sigma/\Delta V\). **Gate:** fit \(R_c=K\,\sigma/\Delta V\) with \(R^2\ge 0.99\) and \(|K/\kappa_d-1|\le 0.15\).  
* **Work/energy check:** \(W(R)\) shows extremum at \(R_c\); derivative zero within tol; curvature sign correct. fileciteturn1file18

### H‑B: False‑vacuum lifetime (metastability)
* **Exponential tail:** \(S(t)\approx e^{-\Gamma t}\). **Gate:** exponential fit \(R^2\ge 0.99\); KS p\(>0.1\) on tail; CI for \(\Gamma\).  
* **Resolution robustness:** doubling spatial resolution changes \(\Gamma\) by \(<10\%\); CI excludes \(\ge 10\%\) change. fileciteturn1file10

### H‑C: Net charge production (void‑debt analogue)
* **Chemical‑potential route:** with \(\mu_B>0\), \(\langle\Delta Q_B\rangle\) exceeds \(\mu_B=0\) null. **Gate:** \(\langle\Delta Q_B\rangle_{\mu_B>0}-\langle\Delta Q_B\rangle_{0}\ge\delta_Q\) with 95% CI excluding 0 (\(\delta_Q\) set by pilot).  
* **CP‑pumping route:** with \(\kappa_{CP}\neq 0\), moving walls pump \(Q_B\). **Gate:** slope \(d\langle\Delta Q_B\rangle/d\kappa_{CP}>0\) with 95% CI; sign flips under \(\kappa_{CP}\to-\kappa_{CP}\).  
* **Sakharov checklist:** out‑of‑equilibrium walls; CP violation present; announcer‑mediated reprocessing. **Gate:** all three flags present. fileciteturn1file18

## 7. Symmetry Regimes, Nulls, and Ablations (J→Dirac alignment)

**Regime flag (this prereg):** **Open, broken** — at least one breaker active: absorbing/Dirichlet BC, biased source/noise \(+\epsilon\), or explicit memory coupling \(\mu\) breaking \(C\mapsto -C\).  
**Asymmetry gate (front‑loaded):**  
\[\boxed{\text{Gate FV‑A: }\ \mathbb E[\dot{\mathcal A}]>0 \ \text{with 95\% CI not crossing 0, and }\dot{\mathcal A}\to 0 \text{ when breakers}=0}\]  
where \(\mathcal A\) is the net “void‑debt” or charge functional. **Ablations:** toggle each breaker off and show asymmetry collapses to zero within error. (Also define the **Closed, symmetric** SIE‑Invariant regime elsewhere with \(|\Delta Q|/Q\le 10^{-6}\) drift gate.) fileciteturn1file12 fileciteturn1file3

## 8. Equipment / Hardware

**Compute environment.** CPU‑first implementation; AMD/ROCm stack if GPU is used; fp64 primary. Record system specs and utilization; pin math libraries and thread affinities.  
**Integrity/limits.** Log seeds, commits, environment file; disclose assistance roles. Report stage‑wise wall‑clock and footprint; state whether hardware differences change outcomes (and mitigations). fileciteturn1file9

## 9. Methods / Procedure (reproducible pipeline)

**Equations & discretizations.** J‑dominant scalar PDE with optional M as discrete‑gradient flow (if enabled) subject to Lindblad checks.  
**ICs/BCs, parameters, seeds.** β near false vacuum with small noise; localized seeds for \(R_c\); declare \(\lambda, v, \epsilon, \mu_B, \kappa_{CP}\), domain/step sizes; multi‑seed design.  
**Solvers.** Integrator choices and tolerances predeclared; stopping criteria; post‑processing (radius fits, survival analysis, bootstrap CIs).  
**Materials.** Repo paths (proposal/results), environment spec; dataset/IC generators and licenses.  
**Risk/Ethics.** Data licensing; compute cost/carbon; sandboxing/quotas. fileciteturn1file9

## 10. Results to be produced (figures & tables)

F1: Potential & thin‑wall geometry; F2: \(R_c\) scaling with CI; F3: Bubble growth & energy budgets; F4: Survival curve with KS stats; F5: Charge production vs \(\mu_B\) or \(\kappa_{CP}\) with slope/sign‑flip; F6: Meters (determinism, H‑theorem, operator/BC IDs). Each figure includes PNG+CSV+JSON sidecars, seed and commit in captions. fileciteturn1file17

## 11. Success/Failure Interpretation

**PASS:** Thin‑wall scaling, exponential survival with robust \(\Gamma\), and positive net \(\Delta Q_B\) with correct sign under CP/chemical‑potential drives; meters green.  
**FAIL with meters green:** open a **CONTRADICTION_REPORT** (gate, threshold, seed, commit, artifact pointer) and revise \(\mathcal I,\Sigma\) or ranges via a new tag. fileciteturn1file16

## 12. Cross‑links to parallel T4s (context only; not blocking)

* **PROPOSAL_J_to_Dirac_T4.md** — spinor Dirac limb (dispersion/norm/AB gates), gauge links, Lindblad M, metriplectic coupling, and regime reconciliation (invariant vs asymmetry). These inform meters and future coupling studies but are out‑of‑scope for this scalar prereg. fileciteturn1file11

## 13. References (internal)

Template and authoring standards; FV prereg source; J→Dirac directives and acceptance snippets. fileciteturn1file9 fileciteturn1file0 fileciteturn1file12
