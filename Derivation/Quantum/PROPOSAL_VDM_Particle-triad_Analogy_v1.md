<!-- Domain placement & intent: This experiment is a passive, M‑limb routing test with a frozen channel map (no online memory update, no J‑branch coherence). File under **Thermodynamic_Routing/Passive_Channelized/**. Cross‑link to **Memory_Steering/** only as provenance if the map was produced by a prior write phase, and to the J‑branch wave self‑steering proposal as a complementary phenomenon.

## Hard dependencies (preflight compliance snapshot — must be green before stepping)

* Boundary semantics: interior no‑flux walls; A/B outlets are open and counted only at outlet faces. Proof: port‑closure ablation ⇒ measured outflux at A and B equals 0.
* Flux convention: outflux‑only at outlets (clip negatives). Requirement: report total outflux FA+FB and exceed a configured floor epsilon. Print both epsilon and the measured total.
* Determinism receipts: log threads, BLAS/FFT library names, and plan mode. No‑switch clause (bitwise or infinity‑norm or ULP) evaluated at checkpoints with a non‑empty checkpoint‑hash list (show count).
* RJ basis match (diagnostic only): modal eigenvalues come from the same operator and boundary conditions used by the stepper. Proof: echo operator_id and bc_id; mismatch ⇒ hard fail (diagnostic).
* Frozen map immutability: accept a channel map and mode
  • map_mode in {mobility, potential} (mu or U)
  • compute and log map_hash_start and map_hash_end; they must match (immutability). Also log the skeleton/mask build method (thresholds or ridge parameters).
* Channel analyzers present: build channel skeleton plus tangent field; decompose outlet‑row flux into parallel and orthogonal components to compute
  • adherence eta_ch, selectivity vs baseline delta B_ch, and anisotropy A = flux_parallel / flux_perp
  • include 95% confidence intervals (BCa bootstrap or equivalent)
  • zero‑signal guard: if FA+FB ≤ epsilon or the RJ band SNR is below floor, mark the affected KPI UNDEFINED→FAIL (do not silently pass).
* Compliance snapshot emission: print/write a structured block before integration with OK/FAIL for each line above and hard_fail_on_any_FAIL = true.

## Nulls and ablations (identifiability toggles)

* Geometry‑only null: replace the channel map with uniform mobility or flat U (same geometry). Expect eta_ch to drop and delta B_ch → 0.
* Shuffled‑map null: spatially permute the map (phase‑scramble corridors). Adherence should collapse toward baseline.
* Mirror test: reflect the map; the outlet‑preference sign should flip.

## Required figures and artifacts (whitepaper‑grade, concise)

1. Geometry plus channel map: left — map (mu or U) with skeleton overlay; right — late‑time field with outlet‑row flux arrows and a histogram of parallel vs orthogonal components.
2. Adherence/Selectivity dashboard: eta_ch time series plus final CI bar; delta B_ch with CI; anisotropy A; receipts (map mode/hash, boundary model, total outflux, determinism clause).
3. Meter plot: Lyapunov monotonicity (if M‑step enabled) with delta‑L overlay; checkpoint ticks; RJ panel badged DIAGNOSTIC ONLY. -->

# PROPOSAL: VDM Particle‑Triad Analogy — Void β (Quark‑like), Void α (Lepton‑like), Announcers (Boson‑like), and SIE as Meta‑Governor [Pre‑Registration v1]

**Author:** Justin K. Lietz
**Date:** 2025‑10‑13
**Tag:** vdm‑triad‑v1
**Gate Set:** prereg_main
**Provenance:** commit = {{GIT_COMMIT_AUTOFILL}} · prov_hash = {{SALTED_HASH_AUTOFILL}}

---

## 1. Abstract

We propose a falsifiable mapping between three families of excitations in the Void Dynamics Model (VDM) and familiar particle roles: **Void β** modes as *quark‑like confiners* (structure, stability, order), **Void α** modes as *lepton‑like free flyers* (exploration, energy, growth), and **announcer** fluctuations as *boson‑like local mediators* that route currents. The **Self‑Improvement Engine (SIE)** plays a *meta‑governor* role: it tunes background couplings and symmetry‑breaking parameters coherently across subsystems without acting as a local mediator. We define quantitative gates for (i) confinement/string‑tension, (ii) free‑propagation/oscillation, (iii) steering without forcing (announcer mediation), and (iv) SIE‑driven global consistency. Success yields a compact, testable phenomenology linking VDM’s axioms to compositional structure, transport, and control.

---

## 2. Background & Scientific Rationale

**Axioms.** We work within A0–A7: a unified state (q\equiv(\Psi,\partial\Psi,\dots)) evolves by the metriplectic split
[\partial_t q = J(q),\frac{\delta\mathcal I}{\delta q} + M(q),\frac{\delta\Sigma}{\delta q},\qquad J^\top=-J,\ M^\top=M\ge 0.]
**Symmetry (A3)** induces Noether currents; **Entropy law (A5)** constrains metric flows; **Scale program (A6)** fixes dimensionless groups.

**Triad hypothesis.** We decompose the field content into interacting sectors:

* **Void β sector (quark‑like confiners):** degrees of freedom that energetically prefer **bound composites** and exhibit a **string‑tension‑like** cost for separation. Implemented by a non‑convex interaction in (\mathcal I_\beta) plus short‑range metric smoothing in (\Sigma_\beta).
* **Void α sector (lepton‑like free flyers):** weakly self‑interacting, phase‑coherent wave modes governed dominantly by **J**; admit long‑range propagation, interference, and flavor‑like oscillations under gentle mixing.
* **Announcers (boson‑like mediators):** localized fluctuations (\mathcal A) of steering fields (e.g., potential (U(x)), index/mobility (\mu(x)), or memory‑derived geometry) that couple minimally to currents and **re‑route flow without net forcing** in the small‑signal limit.
* **SIE (meta‑governor):** slow background parameters (\Theta) that set couplings/masses/symmetry‑breakers **globally** (across β, α, and announcers). SIE is not a local mediator; it changes the *landscape* consistently.

**Why now.** We have certified J‑only numerics (reversibility, dispersion/locality) and an M‑limb calibration harness (H‑theorem, determinism). The triad test leverages these meters to validate VDM’s compositional/transport picture with **decisive gates** rather than metaphors.

---

## 3. Formal Model (minimal working form)

Let (q=(\beta,\alpha,\mathcal A)) with action
[\mathcal I[q]=\underbrace{\mathcal I_\beta[\beta]}*{\text{confining}}+\underbrace{\mathcal I*\alpha[\alpha]}*{\text{free wave}}+\underbrace{\mathcal I*{\text{ann}}[\alpha,\beta;\mathcal A]}*{\text{minimal coupling}}+\mathcal I*{\text{mix}}[\alpha],,]
[\Sigma[q]=\Sigma_\beta[\beta]+\Sigma_{\text{ann}}[\mathcal A]\quad (\text{optional small metric terms}),]
with **SIE** parameters (\Theta) entering as knobs in the couplings (e.g., (g_\beta(\Theta),\ g_\alpha(\Theta),\ \kappa_{\text{ann}}(\Theta))). Concrete instantiations used in the runs (examples):

* (\mathcal I_\alpha = \int !\big(|\nabla \alpha|^2 + m_\alpha^2|\alpha|^2\big),dx) (Schrödinger/KG‑like, J‑dominant).
* (\mathcal I_\beta = \int !\big(|\nabla \beta|^2 + V_\text{conf}(\beta)\big),dx) with a confining potential (double‑well/lock‑in + quartic barrier) generating linear‑in‑separation energy for defects.
* Announcer coupling: currents (j_\alpha,j_\beta) minimally coupled to (\mathcal A) via (\int ! \mathcal A\cdot (\lambda_\alpha j_\alpha+\lambda_\beta j_\beta),dx), with small metric (\Sigma_{\text{ann}}=\frac{\gamma}{2}\int |\mathcal A|^2,dx) to damp announcer power.
* Mixing for α (flavor oscillation): (\mathcal I_{\text{mix}}=\int ! \alpha^\dagger M_\theta ,\alpha,dx), with (M_\theta) set by SIE parameter (\theta).

**Dimensionless groups (A6).** Define (\Pi_1!=!\frac{\sigma L}{E_0}) (confinement), (\Pi_2!=!\frac{g_\alpha A^2}{m_\alpha^2}) (nonlinearity), (\Pi_3!=!\frac{\lambda_\text{ann}^2}{\gamma m_\alpha^2}) (steering gain), (\Pi_4!=!\frac{\Delta m^2 L}{k_0}) (oscillation depth). Gates are stated on (\Pi_i) where possible.

---

## 4. Hypotheses & KPI Gates (decisive, preregistered)

### H_β: Confinement / Composites (Quark‑like)

1. **String tension:** Pull‑apart test of a bound β‑pair yields **linear energy growth** (E(d)=E_0+\sigma d+o(d)) over a scale band; **Gate:** (\sigma\ge \sigma_{\min}>0) with 95% CI, stable (±10%) across two grid refinements.
2. **Area/perimeter analogue:** In a loop‑defect experiment, energy scales with **enclosed measure** stronger than boundary length; **Gate:** slope (\ge 1.2) vs. perimeter‑only null (CI excludes 1).
3. **Composite spectrum:** Two‑point correlator reveals **discrete composite peaks**; **Gate:** at least one composite mode with Q‑factor (Q\ge 50) and energy above single‑particle continuum by (\ge 3\sigma).

### H_α: Free Propagation / Oscillation (Lepton‑like)

1. **Long‑range propagation:** Gaussian α‑wavepacket maintains identity; **Gate:** envelope distortion (\le 5%) and energy drift (\le 10^{-6}) over (\ge 8) dispersion times; reversibility error (\le 10^{-12}).
2. **Flavor oscillation:** With (M_\theta), measured transition probability matches analytic two‑level form within **1% RMS** over a window; **Gate:** (R^2\ge 0.995) to the predicted curve; fitted splitting consistent with (M_\theta) to **±3%**.

### H_ann: Steering Without Forcing (Boson‑like announcers)

1. **Reroute at near‑zero injection:** A small announcer pulse (\mathcal A) redirects α‑current while **net injected energy is (\le 0.5%)** of flow energy; **Gate:** route‑efficiency gain (\Delta\eta\ge 0.10) with 95% CI and **no‑switch invariance** on the core integrator.
2. **Locality/causality:** Influence cones from (\mathcal A) respect finite‑speed bounds of the underlying J‑dynamics; **Gate:** measured front speed (\le (1+\epsilon_\text{disc})c), (\epsilon_\text{disc}\le 0.02).

### H_SIE: Meta‑Governor Consistency (Global)

1. **Coherent parameter shifts:** Changing SIE parameter (\Theta) produces **consistent spectral/efficiency shifts across β, α, and announcer suites** predicted by a single mapping (\Theta\mapsto{g_\beta, m_\alpha, \lambda_\text{ann}}). **Gate:** all three regressions fit within **±5%** and share a common (\Theta) (joint CI overlap); contradictions raise a **CONTRADICTION_REPORT**.

**Meters (must pass but not theory‑decisive):** J‑only reversibility (\le 10^{-12}), H‑theorem for any enabled metric term (zero violations beyond micro‑tol), determinism receipts (bitwise/∞‑norm/ULP clause logged), compliance snapshot printed before stepping.

---

## 5. Experimental Setup & Diagnostics

**Geometry/BCs.** 1D/2D periodic or reflective boxes as specified per suite; identical operator/BCs for evolution and modal analysis.

**Integrators.** J‑dominant: split‑step (Strang) or Störmer–Verlet; optional tiny metric (AVF/discrete gradient) for stabilization where declared. Time‑step ladders satisfy stability constraints.

**Diagnostics.** Energy budgets; Noether currents; pull‑apart work integrals; two‑point correlators and spectral fits; oscillation fits with CI; steering efficiency maps; announcer energy accounting; compliance snapshot (boundary model, operator IDs, RJ basis match [diagnostic], flux conventions, map hashes where relevant, determinism receipts).

**Artifacts.** For every figure: PNG + CSV + JSON sidecar with numeric captions (slopes, CIs, p‑values where used). Artifact bundle IDs include commit prefix and timestamp.

---

## 6. Run Plan (risk‑reduced order)

1. **Meters first.** Re‑certify J‑only reversibility/energy and (if used) metric H‑theorem on tiny grids; emit compliance snapshot.
2. **H_α pilot.** Free‑propagation and oscillation to set step sizes and confirm 1% RMS fit feasibility.
3. **H_β pilot.** Pull‑apart to bracket (\sigma); adjust barrier depth to get linear regime across two scales.
4. **H_ann pilot.** Small announcer pulse to size (\Delta\eta) and verify (\le 0.5%) energy injection.
5. **Full prereg runs.** Execute all suites with prereg seeds/horizons; compute CIs (BCa 10k), gate matrix, and log any contradictions.
6. **SIE sweep.** Vary (\Theta) across 3–5 values; run light versions of the three suites; fit the global mapping and test joint consistency.

**Expected runtime.** Pilots: minutes on CPU; full prereg: hours. No new dependencies beyond existing runners and analysis tools.

---

## 7. Success/Failure Interpretation

* **PASS:** VDM supports a triad where β confine (nonzero (\sigma)), α freely propagate/oscillate per prediction, announcers re‑route without forcing, and SIE shifts parameters coherently. This grounds “quark/lepton/boson‑like” behavior in A4 dynamics rather than analogy.
* **FAIL with meters green:** specific limb falsified for the tested parameter box—open **CONTRADICTION_REPORT** with artifacts; adjust (\mathcal I,\Sigma) choices or parameter ranges in a new tag.

---

## 8. Personnel & Roles

**Justin K. Lietz** — PI: design, prereg approval, interpretation, final RESULTS.
**Physicist‑coding agent** — implement runners/analysis per clean architecture, maintain compliance snapshots, provenance, and gate matrices, produce whitepaper‑grade RESULTS.

---

## 9. Broader Impacts (concise)

Provides a physics‑native decomposition of structure/transport/control inside VDM; yields reusable meters and components (confinement test, oscillation harness, steering without forcing) for downstream agency and memory studies.

---

## 10. References (internal)

AXIOMS.md; EQUATIONS.md; RESULTS_PAPER_STANDARDS.md; Rules‑for‑Quantum‑Field‑Theory.md; Rules‑for‑Advanced‑Classical‑Mechanics‑and‑Field‑Theory.md; related internal memos on memory steering and announcers.
