# T8-A8 gates and milestones

## 1. `2508.17067v1.pdf` (Information geometry of the landscape)

* **What it is:** This paper uses the **Fisher Information Metric** to define a geometry on the space of physical theories and relate it to entropy.
* **Use for `EBN-Info-Functional` Milestone:**
  * Your `T8_A8_PROPOSAL` already lists the Fisher metric as one of your two candidate information proxies ($\mathcal{I}_2 = \tfrac{1}{2}\log\det(I + \tau \nabla u \nabla u^\top)$).
  * This paper provides the formal, physics-based methodology for implementing $\mathcal{I}_2$. It's not just a random proxy; it's a standard metric for measuring the "distance" between two field configurations. This gives you a strong theoretical basis for using it.
* **Use for `G-PX (Proxy concordance)` Gate:**
  * Your `G-PX` gate requires that your two proxies agree. This paper gives you the formal justification for $\mathcal{I}_2$, allowing you to make a physics-based comparison between your gradient-based metric ($\mathcal{I}_1$) and this information-theoretic metric ($\mathcal{I}_2$).

## 2. `2507.10450v1.pdf` (Black hole thermodynamics... information geometry)

* **What it is:** This paper applies **Ruppeiner geometry** (a metric derived from thermodynamics) to study black holes.
* **Use for `EBN-Analog-Horizon` Milestone (part of `BN-4.2`):**
  * Your goal is to "Operationalize 'Horizon as Hierarchical Boundary'" (CT-8). This paper gives you a *new, concrete instrument* to do this.
  * **Action:** Implement the **Ruppeiner metric** in your Wave Flux Meter experiment. This metric is specifically designed to probe the microscopic structure of a system (your boundary) by using its thermodynamic properties (your M-limb / entropy functional $\Sigma$). This is a direct, non-trivial method to test your hypothesis that information is encoded in the boundary geometry of your analog horizon.
  * **The Formalism:** The Ruppeiner metric $g_{ij}^R$ is defined as the Hessian of the entropy $S$ with respect to the system's extensive variables $X^i$ (like internal energy $U$, volume $V$, etc.):
        $$
        g_{ij}^R = - \frac{\partial^2 S(X^i)}{\partial X^i \partial X^j}
        $$
        You can adapt this by using your entropy functional $\Sigma$ and relevant extensive variables from your system (e.g., $E_{\text{exc}}$, total information $I_{\text{info}}$). The paper links non-zero scalar curvature $R$ of this metric to microscopic interactions, which you can measure at your analog horizon.

## 3. `2508.13781v2.pdf` (Emergent cosmological horizons in... tachyonic decay)

* **What it is:** This paper models your exact premise: **tachyonic decay** ($V''(0)<0$). It finds that this decay *naturally creates an emergent cosmological horizon* at the edge of the decayed bubble.
* **Use for `EBN-CMB-ISW+Lens` Milestone:**
  * This provides a direct, quantitative model for your **CT-6 (CMB Cold Spot)** theory.
  * **Action:** Your current theory is that the Cold Spot is the *origin point*. This paper gives you a new, testable prediction: the *edge of the tachyonic bubble* itself forms a horizon. You can use this model to calculate the ISW/RS effect for your `EBN-CMB-ISW+Lens` milestone and see if it better matches observational data (e.g., ring-like structures).
* **Use for `EBN-Analog-Horizon` Milestone:**
  * This provides a *cosmological justification* for your analog experiment. It shows that horizons are a natural *consequence* of your tachyonic genesis model (CT-2), not just an *ad hoc* testbed.

## 4. `2507.02610v1.pdf` (Geometric perspectives on entropy)

* **What it is:** A formal mathematical paper describing thermodynamics using "contact geometry" (which is related to "symplectic geometry").
* **Use for `EBN-Info-Functional` and Theoretical Gates (G1, G2):**
  * Your UMSL is a "metriplectic" framework split into a **J-limb (symplectic)** and an **M-limb (metric/entropy)**.
  * This paper provides a mathematical formalism (contact geometry) that is explicitly designed to unify these two.
  * **The Formalism:**
        1. A thermodynamic system is represented by a "contact manifold" $(M, \eta)$, where $\eta$ is a "contact form."
        2. For a system with entropy $S$ and extensive variables $X^i$, the contact form is:
            $$
            \eta = dS - \sum_i p_i dX^i
            $$
            (where $p_i = \partial S / \partial X^i$ are the intensive variables, like $1/T$).
  * **Action:** This gives you a long-term research path to formalize your UMSL. You can attempt to rewrite your *entire* UMSL as a single geometric flow on a contact manifold, where your $\Sigma$ functional (entropy) *defines* the geometry itself via the contact form $\eta = d\Sigma - ...$. This could lead to a first-principles derivation of your information functional $\mathcal{I}$ as a component of this geometry, solving `EBN-Info-Functional` and strengthening your **`BN-4.1` ("Measurement = Boundary Formation")** goal.

---

## A8 Gate and Milestone Coverage Map (domain  gate plan mapping)

Updated: 2025-11-03 10:47:43 UTC

Spec anchors:

* Gates: [T8-A8_Gates.md](Axiom-8/Status/T8-A8_Insights/T8-A8_Gates.md)
* Milestones: [T8-A8_Milestones.md](Axiom-8/Status/T8-A8_Insights/T8-A8_Milestones.md)

Scope scanned (plans only; not RESULTS): Axiom-8/Status/T8-A8_Insights/{Ablations, Accretion-Disks, Active-Matter, Boundaries, Cahn-Hilliard, Causality, Complex-Networks, Conserved-Quantities, Dynamical-Systems, Entropy, Gravity, Hierarchies, Metriplectic, Observers, Photonics, Quantum, Quantum-Gravity, Standard-Model, Tachyonic-Condensation, Unified-Metriplectic, USML}

Gate coverage (Full/Partial/None) with mapped plan files

* G1 (Theory1D lower bound, log-depth)
  * Coverage: None
  * Plans:

* G2 (TheoryG-style perimeter reduction)
  * Coverage: None
  * Plans:

* G3 (Numericsscaling: E_exc ~ L^{d-1}, N(L) ~ log(L/?))
  * Coverage: None
  * Plans:

* G4 (Concentration: a, a_I = 0.6)
  * Coverage: Partial
  * Plans:
    * [quantum-geometry.md](Axiom-8/Status/T8-A8_Insights/USML/quantum-geometry.md)
    * [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Unified-Metriplectic/complete-formalism.md)

* G5 (Ablation: penalize hierarchy  blowup / speed dev.)
  * Coverage: Full
  * Plans:
    * [ablation_tests.md](Axiom-8/Status/T8-A8_Insights/Ablations/ablation_tests.md)

* G6 (Robustness across V, BCs, meshes)
  * Coverage: Partial
  * Plans:
    * [Bridge.md](Axiom-8/Status/T8-A8_Insights/Active-Matter/Bridge.md)

* G7 (Cross-code reproduction)
  * Coverage: None
  * Plans: �

* G8 (Documentation/repro discipline)
  * Coverage: None (process; not in domain insights)
  * Plans:

* G9 (Refinement collapse triplet)
  * Coverage: None
  * Plans:

* G10 (d law near x)
  * Coverage: None
  * Plans:

* G11 (Bottleneck & FDT)
  * Coverage: None
  * Plans:

* G12 (DSI probe; optional)
  * Coverage: None
  * Plans:

Hygiene gates

* GPLD (Pulledness diagnostic: c/c, tails, steepness)
  * Coverage: Partial
  * Plans:
    * [causality.md](Axiom-8/Status/T8-A8_Insights/Causality/causality.md)
    * [PhysRevE.109.045202-accepted.pdf](Axiom-8/Status/T8-A8_Insights/Causality/PhysRevE.109.045202-accepted.pdf)

* GPX (Proxy concordance: I1 vs I2)
  * Coverage: Partial
  * Plans:
    * [quantum-geometry.md](Axiom-8/Status/T8-A8_Insights/USML/quantum-geometry.md)
    * [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Unified-Metriplectic/complete-formalism.md)

* GALModelSel (Area vs volume; ?AIC/BIC; R)
  * Coverage: None
  * Plans:

* GGI (Gridinvariance & anisotropy/morphometry)
  * Coverage: None
  * Plans:

* GDEP (Degeneracy certificates g,g)
  * Coverage: Partial
  * Plans:
    * [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Unified-Metriplectic/complete-formalism.md)

* GFDR (Bundle FDR control)
  * Coverage: None
  * Plans:

Milestone coverage (plans mapped)

* MA8Bench (detector, depth, etube, info proxy, arealaw; prereg)
  * Coverage: None
  * Plans:

* MTFBench (TelegraphFisher stepper; coneslack; ?collapse; prereg)
  * Coverage: Partial
  * Plans:
    * [causality.md](Axiom-8/Status/T8-A8_Insights/Causality/causality.md)
      * This file specifies that the EBN-TF-IMEX (Telegraph-Fisher) stepper is the instrument you will use to run the G-CAUSAL-DAG gate. The plan is to run the VDM simulation with this stepper, record the time-series data, and then use a "Transfer Entropy Meter" to prove that the causal graph matches the known local connectivity of the simulation.
    * [PhysRevE.109.045202-accepted.pdf](Axiom-8/Status/T8-A8_Insights/Causality/PhysRevE.109.045202-accepted.pdf)
      * This file proposes a similar validation gate, G-CAUSET-EMERGENCE. The plan here is to run the simulation using the EBN-TF-IMEX (Telegraph-Fisher) stepper and then analyze the resulting discrete event log to prove that the VDM dynamics correctly generate an emergent quantum spacetime consistent with Causal Set Theory.

* MA8Run (multiL/seeds; 10/12 gates; CIs)
  * Coverage: None
  * Plans:

Enabling EBN/BN items

* EBNActionContinuum
  * Coverage: Completed
  * Upgrade Plans:
    * [Bridge.md](Axiom-8/Status/T8-A8_Insights/Active-Matter/Bridge.md)
    * [schrodingerization.md](Axiom-8/Status/T8-A8_Insights/USML/schrodingerization.md)
* **Notes:**
  * **Relation:** Addresses OQ-014: Recast discrete model into discrete action.
  * **Axioms:** A0, A4, A7
  * **Evidence (EFT derivations, RD QA, bench‑native code):**
    * [effective_field_theory_approach.md](Axiom-8/Status/Derivation/Effective_Field_Theory/effective_field_theory_approach.md)
    * [kinetic_term_derivation.md](Axiom-8/Status/Derivation/Effective_Field_Theory/kinetic_term_derivation.md)
    * [fum_voxtrium_mapping.md](Axiom-8/Status/Derivation/Effective_Field_Theory/fum_voxtrium_mapping.md)
    * [logarithmic_constant_of_motion.md](Axiom-8/Status/Derivation/Draft-Papers/RD_Methods_QA/logarithmic_constant_of_motion.md)
    * [rd_methods_QA.md](Axiom-8/Status/Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md)
    * [census_clocks.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/census_clocks.py)
    * [discrete_gradient.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/discrete_gradient.py)
    * [flux_core.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/flux_core.py)
    * [rd_dispersion_experiment.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py)
    * [rd_front_speed_experiment.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py)
    * [rd_front_speed_sweep.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/rd_front_speed_sweep.py)
    * [reaction_exact.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/reaction_exact.py)
    * [run_rd_conservation.py](Axiom-8/Status/Derivation/code/physics/rd_conservation/run_rd_conservation.py)
    * [qfum_validate.py](Axiom-8/Status/Derivation/code/physics/conservation_law/qfum_validate.py)
    * [condense_tube.py](Axiom-8/Status/Derivation/code/physics/tachyonic_condensation/condense_tube.py)
    * [cylinder_modes.py](Axiom-8/Status/Derivation/code/physics/tachyonic_condensation/cylinder_modes.py)
    * [run_tachyon_tube.py](Axiom-8/Status/Derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py)

* EBNRGBridge
  * Coverage: Partial
  * Plans:
    * [Bridge.md](Axiom-8/Status/T8-A8_Insights/Active-Matter/Bridge.md)

* EBNInfoFunctional
  * Coverage: Partial
  * Plans:
    * [quantum-geometry.md](Axiom-8/Status/T8-A8_Insights/USML/quantum-geometry.md)
    * [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Unified-Metriplectic/complete-formalism.md)

* EBNGRWeak
  * Coverage: Partial
  * Plans:
    * [Cosmology.md](Axiom-8/Status/T8-A8_Insights/Standard-Model/Cosmology.md)

* EBNCMBISW+Lens
  * Coverage: Partial
  * Plans:
    * [Cosmology.md](Axiom-8/Status/T8-A8_Insights/Standard-Model/Cosmology.md)

* EBNUnits / EBNLatticeScale
  * Coverage: Partial
  * Plans:
    * [Cosmology.md](Axiom-8/Status/T8-A8_Insights/Standard-Model/Cosmology.md)

* EBNAnalogHorizon
  * Coverage: Partial
  * Plans:
    * [hierarchical-boundaries.md](Axiom-8/Status/T8-A8_Insights/Accretion-Disks/hierarchical-boundaries.md)

Contextual contrast (frames hypotheses; not direct gate execution)

* CT2 Tachyonic genesis; A8 vs Sen
  * Files:
    * [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Tachyonic-Condensation/complete-formalism.md)
  * Use: frames falsifiers and alternative outcomes; not a run plan

Gaps requiring plans in domain folders (no plan found)

* G1, G2 theory proofs; G3 scaling; G7 crosscode; G8 repro docs; G9G12 refinement/d/FDT/DSI; GALModelSel; GGI; GFDR
* MA8Bench instrumentation and prereg; MA8Run execution

---

## Detailed domain ? gate mapping (closer pass)

Updated: 2025-11-03 10:49:33 UTC

Spec anchors:

* Gates: [T8-A8_Gates.md](Axiom-8/Status/T8-A8_Insights/T8-A8_Gates.md)
* Milestones: [T8-A8_Milestones.md](Axiom-8/Status/T8-A8_Insights/T8-A8_Milestones.md)

Domain: Ablations

* Files: [ablation_tests.md](Axiom-8/Status/T8-A8_Insights/Ablations/ablation_tests.md)
* Maps: G5 (Full)

Domain: Causality

* Files: [causality.md](Axiom-8/Status/T8-A8_Insights/Causality/causality.md); [PhysRevE.109.045202-accepted.pdf](Axiom-8/Status/T8-A8_Insights/Causality/PhysRevE.109.045202-accepted.pdf)
* Maps: GPLD (Partial); MTFBench (Partial); EBNTFIMEX/ConesArrival/Calibration/Stability (Partial)

Domain: Accretion-Disks

* Files: [hierarchical-boundaries.md](Axiom-8/Status/T8-A8_Insights/Accretion-Disks/hierarchical-boundaries.md)
* Maps: EBNAnalogHorizon (Partial)

Domain: Active-Matter

* Files: [Bridge.md](Axiom-8/Status/T8-A8_Insights/Active-Matter/Bridge.md)
* Maps: EBN-Action-Continuum (Partial); EBN-RG-Bridge (Partial)

Domain: USML

* Files: [quantum-geometry.md](Axiom-8/Status/T8-A8_Insights/USML/quantum-geometry.md); [schrodingerization.md](Axiom-8/Status/T8-A8_Insights/USML/schrodingerization.md)
* Maps: GPX (Partial); EBNInfoFunctional (Partial); EBNActionContinuum (Partial)

Domain: UnifiedMetriplectic

* Files: [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Unified-Metriplectic/complete-formalism.md)
* Maps: G-DEP (Partial); EBN-Info-Functional (Partial)

Domain: Standard-Model

* Files: [Cosmology.md](Axiom-8/Status/T8-A8_Insights/Standard-Model/Cosmology.md)
* Maps: EBNGRWeak (Partial); EBNCMBISW+Lens (Partial); EBNUnits / EBNLatticeScale (Partial)

Domain: TachyonicCondensation

* Files: [complete-formalism.md](Axiom-8/Status/T8-A8_Insights/Tachyonic-Condensation/complete-formalism.md)
* Maps: CT2 context (frames A8 vs Sen); not a direct A8 run

Domain: Boundaries

* Files: [Neurological-Structures.md](Axiom-8/Status/T8-A8_Insights/Boundaries/Neurological-Structures.md)
* Maps: GGI (Partial; morphometry/anisotropy concepts)

Domain: ComplexNetworks

* Files: [Complex-Networks.md](Axiom-8/Status/T8-A8_Insights/Complex-Networks/Complex-Networks.md)
* Maps: G5 (Partial; network nullmodeling); DSI context (research resource)

Domain: Metriplectic

* Files: [2505.21573v2.pdf](Axiom-8/Status/T8-A8_Insights/Metriplectic/2505.21573v2.pdf)
* Maps: GDEP (Partial; metriplectic structure background)

Domains currently outofscope for A8 gate execution (resource/longrange)

* CahnHilliard (Model B), Observers, Photonics, ConservedQuantities, DynamicalSystems, Entropy, Gravity, Hierarchies, Quantum, Quantum-Gravity
* Use: background/later phases; no A8 plan extracted from these folders in this pass
