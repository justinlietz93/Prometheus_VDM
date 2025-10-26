# PROPOSAL: False‑Vacuum Metastability and “Void‑Debt” Asymmetry in VDM — Pre‑Registration v1

**Proposer:** Justin K. Lietz
**Date:** 2025‑10‑13
**Tag:** FV‑VoidDebt‑v1
**Gate Set:** prereg_main
**Provenance:** commit = 09f571e8edaf344582b2db86aa4e5e1bee25c615 · prov_hash = {{SALTED_HASH_AUTOFILL}}

---

## 1. Abstract

We propose a whitepaper‑grade, preregistered program to study **false‑vacuum metastability** and a minimal analogue of **matter–antimatter asymmetry** ("void‑debt") within the Void Dynamics Model (VDM). A scalar **β‑field** with a tilted double‑well potential provides false and true vacua; **announcer** fields provide gauge‑like mediation; the **Self‑Improvement Engine (SIE)** sets global couplings/tilt; and a conserved **B‑charge** with chemical potential or CP‑violating coupling provides an asymmetry source. We design three decisive experiments with quantitative gates: (A) **bubble nucleation** and critical‑radius scaling (thin‑wall test), (B) **false‑vacuum lifetime** via survival analysis, and (C) **net charge production** during bubble growth (chemical‑potential or CP‑pumping route). Compliance includes determinism receipts, operator/BC matching, two‑resolution checks, and energy/entropy ledgers. PASS yields a falsifiable account of metastability and asymmetry in A4‑split dynamics; FAIL with meters green produces a contradiction report with artifacts.

---

## 2. Background & Scientific Rationale

**VDM axioms.** We work under A0–A7. The state (q=(\beta,\mathcal A,\ldots)) evolves as
[\partial_t q = J(q),\frac{\delta\mathcal I}{\delta q} + M(q),\frac{\delta\Sigma}{\delta q},\qquad J^\top=-J,\ M^\top=M\ge 0.]
**Symmetry (A3)** induces currents; **Entropy law (A5)** constrains any metric leg; **Scale program (A6)** demands predictions in dimensionless groups.

**Physics target.** Cosmology and particle theory allow a Universe residing in a **metastable vacuum** (false vacuum) that is long‑lived due to a barrier. Decay proceeds by **nucleation of true‑vacuum bubbles**. Baryon asymmetry requires out‑of‑equilibrium conditions and T/C/CP violation (Sakharov‑style). We model these ingredients natively in VDM: β provides the order parameter; announcers provide local mediation; SIE sets global couplings and the small tilt; a B‑current plus chemical potential or CP term biases charge production.

**Novelty.** Unlike textbook scalar field toy models, our prereg frames the problem inside **VDM’s metriplectic split** with explicit **meters** (reversibility, H‑theorem ledgers), a **compliance snapshot**, and **resolution‑robust** gates. The “void‑debt” channel is tested in two ways (chemical‑potential bias and CP‑pumping) with explicit nulls.

---

## 3. Formal Model (minimal working form)

### 3.1 Fields and functionals

* **β‑field (order parameter).** Potential
  [ V_\beta(\beta)=\tfrac{\lambda}{4}(\beta^2-v^2)^2+\epsilon,\beta, ]
  with small tilt (\epsilon) set by **SIE** ((\epsilon\ll \lambda v^3)).
* **Announcers** (\mathcal A): gauge‑like steering/connection fields coupling to currents; kinetic term in (\mathcal I) and optional tiny quadratic metric in (\Sigma) for numerical damping.
* **B‑charge**: conserved current (J_B^\mu). We consider two asymmetry mechanisms:

  1. **Chemical potential route:** add (\mu_B J_B^0) to (\mathcal I) (grand‑canonical bias).
  2. **CP‑pumping route:** couple (\beta) to announcer curvature via a Chern–Simons‑like term (\kappa_{CP},\beta,\mathcal F\tilde{\mathcal F}) that pumps (Q_B) during moving walls.

The action and entropy functionals (schematic):
[ \mathcal I[q]= \int!\big( |\nabla\beta|^2 + V_\beta(\beta) + \mathcal L_{\mathcal A}(\mathcal A) + \mathcal L_\text{int}(\beta,\mathcal A,J_B) \big),dx,]
[ \Sigma[q]=\Sigma_{\mathcal A}[\mathcal A]\ \text{(optional, small)}. ]
Dynamics follow A4 with J‑dominant flow; M is micro and ledgered if enabled.

### 3.2 Dimensionless groups (A6)

Let (d) be spatial dimension (we prereg 2D for visualization; thin‑wall constants adjusted accordingly). Define
[ \Pi_1=\frac{\Delta V}{\sigma},,\quad \Pi_2=\ell,\Gamma^{1/d},,\quad \Pi_3=\frac{\mu_B}{T_\text{eff}}\ \text{or}\ \kappa_{CP}/\kappa_0,,\quad \Pi_4=\frac{\xi}{L},, ]
where (\Delta V) is vacuum energy gap, (\sigma) wall tension, (\Gamma) nucleation rate, (\ell) a characteristic length, (\xi) correlation length, (L) box size.

---

## 4. Hypotheses & KPI Gates (pre‑registered)

### H‑A: Bubble nucleation & thin‑wall scaling (β only)

1. **Critical radius:** In dimension (d), the thin‑wall model predicts ( R_c = \kappa_d,\sigma/\Delta V ) with known (\kappa_d). **Gate:** measured (R_c) vs (\sigma/\Delta V) fits (R_c=K,\sigma/\Delta V) with (R^2\ge 0.99) and (|K/\kappa_d-1|\le 0.15).
2. **Work/energy check:** Bubble growth work (W(R)) exhibits the expected extremum at (R_c). **Gate:** derivative zero within numerical tolerance and curvature sign correct.

### H‑B: False‑vacuum lifetime (metastability)

3. **Exponential tail:** Survival probability (S(t)) of the false vacuum follows an exponential tail (S(t)\approx\exp(-\Gamma t)). **Gate:** exponential fit (R^2\ge0.99); KS test p(>0.1) on tail; rate CI reported.
4. **Resolution robustness:** Doubling spatial resolution changes (\Gamma) by (<10%). **Gate:** relative shift CI excludes (\ge10%) change.

### H‑C: Net charge production (void‑debt analogue)

5. **Chemical‑potential route:** With (\mu_B>0), bubble growth yields positive net (\Delta Q_B) vs (\mu_B=0) null. **Gate:** (\langle\Delta Q_B\rangle_{\mu_B>0}-\langle\Delta Q_B\rangle_{0} \ge \delta_Q) with 95% CI excluding 0 ((\delta_Q) set by pilot).
6. **CP‑pumping route:** With (\kappa_{CP}\neq 0), moving walls pump (Q_B). **Gate:** linear‑response slope (d\langle\Delta Q_B\rangle/d\kappa_{CP}) positive with 95% CI; sign flips when (\kappa_{CP}\to-\kappa_{CP}).
7. **Sakharov checklist:** Logs must show (i) out‑of‑equilibrium (nonzero wall velocity), (ii) CP violation ((\mu_B\neq 0) or (\kappa_{CP}\neq 0)), (iii) charge reprocessing pathway via announcers. **Gate:** all three flags present.

### Meters (required but not theory‑decisive)

* **Determinism receipts:** threads, BLAS/FFT libs, plan mode; checkpoint equality clause (bitwise/(\infty)‑norm/ULP) with non‑empty hashes.
* **Operator/BC identity:** evolution and analysis use identical operators/BCs (ID echoed).
* **H‑theorem ledger:** if any M‑step used, per‑step (\Delta L_h\le 0) with micro‑tolerance.
* **Zero‑signal guards:** nucleation and (Q_B) metrics must exceed pre‑declared floors or are UNDEFINED→FAIL.

---

## 5. Intellectual Merit and Procedure

### 5.1 Experimental Setup and Diagnostics

* **Domain & BCs:** 2D square (L\times L) with reflective BCs (or periodic for β‑only tests where appropriate).
* **Integrators:** J‑dominant (Störmer–Verlet or split‑step Strang). Optional tiny metric (discrete gradient) for stabilization; ledgered if enabled.
* **Initialization:** β prepared near the **false vacuum** with small spatial noise; true‑vacuum seeding via localized perturbations for Rc measurement.
* **Announcers:** enable kinetic term (\mathcal L_{\mathcal A}); Gauss‑law/constraint residuals monitored (tolerance pre‑declared).
* **Asymmetry channel:** choose **either** (\mu_B) (chemical potential) **or** (\kappa_{CP}) (CP coupling) per run.
* **Diagnostics:** potential/gradient energy budgets; bubble radius estimator; wall tension (\sigma) via static kink fit; survival analysis (many seeds); net (\Delta Q_B) with CI; compliance snapshot.

**Required Figures (with PNG+CSV+JSON sidecars)**
F1. *Potential & thin‑wall geometry.* (a) (V_\beta(\beta)) with minima/tilt; (b) schematic of work (W(R)) vs (R) showing (R_c).
F2. *Critical‑radius scaling.* Measured (R_c) vs (\sigma/\Delta V); fit with slope/captioned CI.
F3. *Bubble growth & energy.* Radius/time with overlay of energy budgets.
F4. *False‑vacuum survival.* Survival curve (S(t)) with exponential fit, KS stats, and rate CI; inset shows resolution robustness.
F5. *Charge production.* (a) (\Delta Q_B) vs (\mu_B) (or (\kappa_{CP})) with slope and CI; (b) sign‑flip check.
F6. *Meters.* Determinism/no‑switch timeline; H‑theorem series (if M used); operator/BC IDs.

### 5.2 Experimental Runplan (risk‑reduced)

1. **Meters first (tiny grids).** Reversibility ≤ (10^{-12}); operator/BC match; determinism receipts; (if used) H‑theorem micro‑tol.
2. **Thin‑wall pilot.** Measure (\sigma), (\Delta V); seed bubbles to bracket (R_c); size time step ladder.
3. **Lifetime pilot.** 50–100 seeds; validate exponential tail and set floors.
4. **Asymmetry pilot.** Small (\mu_B) or (\kappa_{CP}) sweep; estimate (\delta_Q) and slope; finalize gates.
5. **Full prereg execution.** Run prereg seeds/horizons; compute BCa‑bootstrap CIs (10k); assemble gate matrix; publish RESULTS.

**Runtime estimate.** Pilots: minutes on CPU; full prereg: hours. No new external dependencies.

---

## 6. Compliance Snapshot (preflight — must be printed before stepping)

* boundary_model = reflective|periodic (declared per suite)
* operator_id == analysis_operator_id (match)
* determinism = {threads, BLAS, FFT, plan, checkpoint_hash_count>0, clause}
* metric_ledger = enabled?|micro_tol|violations
* zero_signal_floors = {min_detectable_rate, min_detectable_charge}
* resolution_pair = {N,2N} scheduled for robustness
* gauss_law_residual_tol = value (announcers)
* hard_fail_on_any_FAIL = true

---

## 7. Nulls & Ablations (identifiability)

* **Tilt‑off null:** set (\epsilon=0); nucleation rate and (R_c) scaling should change as predicted; asymmetry should vanish in chemical‑potential route with (\mu_B=0).
* **Announcer‑off null:** disable (\mathcal A) (or decouple); CP‑pumping route must collapse (no curvature channel).
* **Resolution null:** swap analysis operator/BC; expected **FAIL‑FAST** (diagnostic) proving the match guard works.

---

## 8. Success/Failure Interpretation

* **PASS:** Correct thin‑wall scaling ((R_c)), exponential survival with robust (\Gamma), and positive net (\Delta Q_B) with the correct sign under CP/chemical‑potential drives; meters green. Interpretation: **metastability and asymmetry are natural** in VDM’s A4 split with SIE‑set couplings; announcers provide the local mediation.
* **FAIL with meters green:** specific limb falsified for this parameter box; open **CONTRADICTION_REPORT** with artifacts and logs; revisit (\mathcal I,\Sigma) choices or ranges in a new tag.

---

## 9. Personnel

**Justin K. Lietz** — PI: experimental design, prereg approval, interpretation, RESULTS authorship.
**Physicist‑coding agent** — implementation of runners/analysis per clean architecture; compliance snapshots; gate matrix; artifact governance.

---

## 10. References (internal)

AXIOMS.md; EQUATIONS.md; RESULTS_PAPER_STANDARDS.md; Rules for Advanced Classical Mechanics and Field Theory; Rules for Quantum Field Theory; internal memos on announcers, memory steering, and VDM meters.
