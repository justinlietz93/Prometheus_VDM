# Unifying Existing Work

## Update:

New urgent items moved to the front.  

- Finish metriplectic KG+RD core
- Stabilize CF ladder prerequisites
- Void-lensing interface program (highest priority)
- Lattice fields & continuum limits (CF10)
- CMB polarization birefringence gate

## 0. Foundations / Meta‑spec (existing TODO, on hold)

**Goal:** Define the objects and rules everything else must obey.

* **Docs**

  * `AXIOMS.md`, `SYMBOLS.md`, `EQUATIONS.md` (esp. VDM‑E‑107,‑108,‑109,‑106) 
  * `Derivation/Unification/T0_Unification_Program_Spec_v1.md`
* **Status:** **DONE (spec-level)**
* **Gaps:** none conceptually; just keep EQUATIONS/SYMBOLS synced as I add more.

---

## 1. Quantum waves → metriplectic split (J/M)

**Goal:** Start from quantum geometry and show why a J⊕M evolution is forced.

* **Docs**

  * **CF1_QGT_to_Metriplectic_Brackets** – QGT → (metric + symplectic) split (spec‑complete in EQUATIONS, full derivation partly in private notes). 
  * **CF6_Info_Geom_Fisher_Ruppeiner_Foundations** – Fisher/Ruppeiner geometry as the info‑theoretic layer over QGT. 
  * **T1_PROPOSAL_Schrodingerization_KvN_v1** – shows how classical J⊕M can be lifted into a single reversible KvN‑type Hamiltonian.
* **Status:**

  * Conceptual picture: **DONE**.
  * Fully written QGT→(I,Σ) derivation: **IN PROGRESS** (CF1 still missing the final “promote to canon” proof).
* **Gaps (action items):**

  * Finish CF1: explicit formulae for `𝓘[Ψ]` and `Σ[Ψ]` from QGT; prove metriplectic brackets satisfy A4.
  * Close Schrödingerization proof to show “J⊕M is a shadow of pure J” in extended space.

---

## 2. Lattice dynamics (KG + RD metriplectic engine)

**Goal:** Show that a scalar lattice with J⊕M really behaves like the void field.

* **Docs**

  * `RESULTS_KG_Noether_Invariants_v1.md` – exact energy/momentum conservation for J‑only KG.
  * `RESULTS_KG_Jonly_Locality_and_Dispersion.md` – clean light‑cone dispersion.
  * `RESULTS_Metriplectic_JMJ_RD_v1.md`, `RESULTS_KG_RD_Metriplectic.md`, `RESULTS_Metriplectic_Structure_Checks.md` – metriplectic structure, Strang defect scaling, H/S degeneracy checks. 
  * Logistic on‑site paper (logarithmic first integral).
* **Status:** **DONE (for scalar J⊕M)**
* **Gaps:**

  * Package this into one “VDM metriplectic engine” paper (KG + RD + structure + Strang). I already have all the results; this is mostly editorial.

---

## 3. Causality / finite‑speed transport

**Goal:** Explain why nothing outruns c, starting from RD‑like flows.

* **Docs**

  * **CF4_Telegraph_Fisher_Causality** – Cattaneo/telegraph derivation, c = √(D/τ), finite propagation theorem, and Fisher‑information interpretation. 
  * Causal‑DAG and Metriplectic‑Causal‑Dominance proposals in `Causality/` (in PROPOSALS registry). 
* **Status:** **DONE at theory level**, instruments **IN PROGRESS**.
* **Gaps:**

  * Finish a RESULTS doc for Causal‑DAG audit on the KG / RD sims to empirically show: inferred cone ≈ analytic cone.

---

## 4. Materialization: tachyonic condensation & hierarchy (A8)

**Goal:** Go from smooth void to structured interfaces (proto‑“lumps” / material features).

* **Docs**

  * **CF3_A8_Scaling_Hierarchical_Interfaces** – Γ‑convergence, tachyonic phase‑field, proof that hierarchy depth K(L) ~ Θ(log L). 
  * A8 Zenodo paper (`T8_A8_Lietz_Infinity_Resolution_Conjecture`).
  * FRW continuity/balance results: `RESULTS_FRW_Continuity_Residual_Quality_Check.md`, `T2_RESULTS_Topological_Ringdown_Meter_v1.md`.
* **Status:**

  * A8 mathematics: **DONE** (1D/phase‑field level).
  * Cosmological realization: **IN PROGRESS** (FRW meters, ringdown meter).
* **Gaps:**

  * One clean A8→FRW bridge paper: “tachyonic interfaces → effective ρ(a), p(a), H(a)” with explicit EOS fits.

---

## 5. Spinor emergence (matter from scalar)

**Goal:** Turn the scalar lattice into fermionic matter degrees of freedom.

* **Docs**

  * **CF8_Spinor_Emergence_Domain_Wall_Fermions** – domain‑wall construction, Ginsparg–Wilson operator, zero‑mode localization, 5D z as auxiliary coordinate. 
  * Nielsen–Ninomiya red‑team + defense docs.
* **Status:** **Theory scaffold DONE**, numerics **GAP**.
* **Gaps:**

  * Companion notebook with an explicit domain‑wall spectrum plot and residual mass scaling ~ e^{-λL₅}.

---

## 6. Gauge emergence (connections on spinor bundles)

**Goal:** Get Maxwell/Yang–Mills fields as geometry, not extra particles.

* **Docs**

  * **CF9_Gauge_Emergence_Berry_Connection** – Berry connection from CF8 spinor bands, geometric gauge fields, Weinberg–Witten compatibility. 
  * H0XX_NonAbelian_Gauge_Emergence + T6_PROPOSAL_Gauge_Emergence_v1 (non‑Abelian generalization).
* **Status:** **Scaffold DONE**, **no full numerical verification yet**.
* **Gaps:**

  * Compute Berry curvatures from an explicit CF8 lattice model, show emergent U(1) field satisfies the Maxwell‑like equations in the long‑wavelength limit.
  * Extend the formalism in H0XX into at least one concrete SU(2) toy example.

---

## 7. Dark matter / dark energy from the lattice

**Goal:** Treat the plastic lattice + A8 hierarchy as the “dark sector”.

* **Docs**

  * A8 hierarchy (CF3 again) → cosmic web scaling. 
  * `Cosmology/FRW_*` results + FRW balance/continuity checks. 
  * `Dark_Matter/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md` for micro→macro DM bridge. 
  * H0ZZ_HYPOTHESIS_A8_Interface_Seeds_BH_Populations_and_GW_Ladder.
* **Status:** **Conceptual story in place, meters partially implemented.**
* **Gaps:**

  * Define an explicit “lattice stress–energy tensor” T^μν_void[Φ] and show:

    * homogeneous part → dark‑energy‑like EOS,
    * hierarchical clumping → halo‑like effective DM (at least in 1D/2D).
  * Pilot SkyrmeSIDM × VDM test using the T5 proposal.

---

## 8. Gravity + expansion (effective GR limit + strong field)

**Goal:** From lattice stress–energy to something GR‑like in weak field, then test ringdown / horizons.

* **Docs**

  * Gravity regression & analog horizon: `T5_PROPOSAL_Gravity_Regression_v1.md`, `T5_PROPOSAL_Analog_Horizon_v1.md`.
  * H0YY_HYPOTHESIS_VDM_Horizon_Structure_and_Strong_Field_Gravity.
  * Ringdown: `T2_RESULTS_Topological_Ringdown_Meter_v1.md`. 
* **Status:** **Scaffold / instruments IN PROGRESS**, no “VDM→Einstein equations” derivation yet.
* **Gaps:**

  * Weak‑field: derive an effective Poisson equation for small lattice perturbations; fit to rotation curves / lensing in at least one toy halo.
  * Strong‑field: show that certain tachyonic interface configurations behave like horizon‑like regions (redshift, QNM spectrum) and compare to GR ringdown data via the ringdown meter.

---

## 9. Packing density / life / ϕ≈0.55

**Goal:** Connect A8 + metriplectic dynamics to the 0.55 packing motif (proteins, random close packing, etc.).

* **Docs**

  * Logistic on‑site first integral paper.
  * A8 hierarchy (again) for “packing into boundaries”. 
  * Agency/CEG/assisted‑echo paper for adaptive structures.
* **Status:** **Speculative but framed.**
* **Gaps:**

  * A small CF‑level derivation: show a simple metriplectic packing model tends toward ϕ≈0.55 in 2D/3D random packing (e.g., via Monte Carlo or granular‑like sim).
  * Explicit link from A8 interfaces + reaction‑diffusion morphogenesis → “prebiotic” cluster statistics.

---

## 10. “Rest of physics & cosmology”

**Goal:** Use the same machinery to hit the standard checklist: SM fields, BH population, CMB, etc.

* **Docs (already scaffolded):**

  * Non‑Abelian gauge: H0XX.
  * Horizons & strong field: H0YY.
  * BH seeds + GW ladder + cosmology probes: H0ZZ, CMB EBN pipeline (T2_PROPOSAL_EBN_CMB_Pipeline_v1), ringdown meter, FRW meters, dark photon portals, Skyrme SIDM, etc. 
* **Status:** **I have boxes on the checklist for almost every major observable.**
* **Gaps:**

  * For each H*/T* cosmology doc: at least one concrete meter/RESULTS file that touches real data (CMB, LSS, ringdown, BH mass function, etc.) even in toy form.

---

What’s left is:

1. Finishing a few algebraic proofs (CF1/QGT, Schrödingerization, T^μν_void).
2. Converting more of the cosmology/gauge scaffolds into **RESULTS** documents tied to real or mock data.
3. Packaging some of the chains (e.g., “metriplectic engine”, “A8 hierarchy → FRW”, “spinor+gauge emergence”) into stand‑alone papers.
