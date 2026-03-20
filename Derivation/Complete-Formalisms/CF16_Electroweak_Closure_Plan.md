# CF16 Plan — Electroweak Fiber Splitting, Chiral Weak Coupling, and Gauge Mixing in VDM

Date: 2026-03-20  
Status: Planning document  
Purpose: Close the electroweak sector cleanly, with no dependence on stale numerics and no outsourcing of core proof burden.

---

## 1. Scope

This paper must close the following, and only the following:

1. the emergence of the electroweak fiber structure as a realized split of the gauge/fiber sector,
2. why the weak interaction couples only to left-handed fermionic modes,
3. how neutral gauge mixing produces the physical photon and Z sectors,
4. how the Weinberg angle enters that mixing,
5. how the W and Z mass relations arise after symmetry breaking,
6. how the Higgs scalar appears as the normal mode of the broken vacuum/interface sector.

This paper should **not** attempt to close quantitative confinement or loop/running-coupling physics. Those belong to later papers.

---

## 2. Canon inheritance to use explicitly

The paper should build only from already-earned structures:

- **A(-1), CF000** — primitive bifurcation law, non-discharge, orthogonal re-articulation, dependence order.
- **CF00** — carrier, variation structure, complex fiber, local phase redundancy.
- **CF03** — tachyonic instability / interface-forcing / vacuum re-expression structure.
- **CF08** — domain-wall fermions, chiral localization, boundary-hosted handedness.
- **CF09** — U(1) gauge emergence, Berry/Wilczek–Zee style gauge hosting, multi-mode fiber structure.
- **CF13** — chirality/orientation from the ORS half-turn boundary.
- **CF14** — stationary action as temporal effective invariant.
- **CF15** — zero-cost directions, Noether charges, symmetry breaking through the M-limb, Higgs/Goldstone language already partially closed as descendants.

Anything not licensed by those papers must be derived in CF16 itself.

---

## 3. What must be proven in CF16

## 3.1 Fiber-level electroweak split

Need to prove that the realized gauge/fiber structure at the relevant layer decomposes as

$$
SU(2)_L \times U(1)_Y,
$$

with a precise VDM interpretation of each factor.

Required work:

- define the multi-mode fiber sector cleanly,
- show why one factor is the already-earned abelian phase structure,
- show why the remaining non-abelian internal rotation acts on a two-component weak doublet structure,
- explain why this is not an inserted Standard Model group label, but the minimal realized symmetry consistent with the fiber degeneracy and chirality architecture.

**Closure target:** a theorem that the minimal electroweak-hosting realized fiber is exactly an abelian hypercharge factor plus a left-acting two-mode non-abelian factor.

## 3.2 Left-handed-only weak coupling

Need a theorem that only left-handed fermions couple to the weak SU(2) sector.

Required work:

- define what “left-handed” means in VDM terms using CF08 + CF13, not imported representation language,
- show that the oriented/domain-wall construction localizes one handedness into the active weak-hosting sector,
- show that the opposite handedness does not inhabit the same weak doublet-hosting structure,
- derive right-handed weak singlets as a structural consequence, not an assumption.

**Closure target:** a theorem that weak non-abelian coupling is restricted to the boundary-hosted handed sector selected by the chiral/oriented construction.

## 3.3 Hypercharge assignment logic

Need to define what the hypercharge-like quantity is in VDM terms and how it is assigned.

Required work:

- define the abelian charge carried alongside the non-abelian weak structure,
- show how it distinguishes the doublet/singlet sectors,
- derive or constrain the relative charge assignments needed for neutral mixing and electric charge recovery,
- make clear which assignments are fully derived and which may still require a normalization convention.

**Closure target:** either full derivation of the electroweak charge assignment pattern, or an honest theorem-plus-normalization statement that isolates the only remaining convention freedom.

## 3.4 Neutral gauge mixing and Weinberg angle

Need a derivation of the neutral-sector mixing.

Required work:

- define the neutral weak gauge direction and the hypercharge gauge direction,
- derive the physical massless and massive neutral combinations,
- show why one combination remains the unbroken electromagnetic direction,
- define the mixing angle geometrically or fiber-theoretically,
- identify exactly what determines the Weinberg angle in the VDM architecture.

**Closure target:** a theorem giving the neutral-sector diagonalization and a definition/theorem for the Weinberg angle as the mixing parameter of the broken electroweak fiber.

## 3.5 W and Z mass generation

Need to derive the W and Z mass ratio from the broken-sector structure.

Required work:

- use CF03/CF15 symmetry-breaking architecture rather than imported Higgs-mechanism prose,
- define the vacuum/interface mode that breaks the electroweak sector,
- show how the charged weak directions pick up equal mass,
- show how the neutral massive direction acquires a different mass set by the same mixing angle,
- recover the mass relation of the form
  $$m_W = m_Z \cos\theta_W$$
  or its VDM-equivalent statement.

**Closure target:** a theorem giving the W/Z mass relation as a forced consequence of the broken neutral/charged decomposition.

## 3.6 Electromagnetic recovery

Need to show that the surviving massless gauge direction is exactly electromagnetism.

Required work:

- identify the unbroken zero-cost direction after electroweak breaking,
- prove that its conserved Noether charge is electric charge,
- show compatibility with CF09’s U(1) charge closure and CF15’s zero-cost conservation law.

**Closure target:** a corollary that electromagnetic gauge symmetry is the residual unbroken direction of electroweak mixing.

## 3.7 Higgs scalar closure at electroweak level

Need to make the Higgs role fully electroweak-specific.

Required work:

- specialize the already-closed CF15 Higgs/interface language to the electroweak vacuum,
- distinguish tangential Goldstone directions from the normal scalar mode,
- show how the tangential directions are absorbed into the weak gauge sector,
- isolate what remains as the physical scalar.

**Closure target:** a theorem/corollary pair closing the electroweak Higgs scalar as the normal mode of the symmetry-broken interface.

---

## 4. Suggested theorem spine

A clean theorem sequence is:

1. **Theorem 1 — Electroweak realized fiber theorem**  
   The minimal broken weak-gauge-hosting fiber decomposes into a left-acting two-mode non-abelian sector and an abelian hypercharge sector.

2. **Theorem 2 — Chiral weak-coupling theorem**  
   Only the boundary-hosted oriented handed sector couples to the weak non-abelian factor.

3. **Theorem 3 — Neutral mixing theorem**  
   The neutral electroweak sector diagonalizes into one massless and one massive direction.

4. **Definition 1 — Weinberg angle**  
   Define the neutral-sector mixing parameter geometrically.

5. **Theorem 4 — Charged/neutral mass theorem**  
   The charged and neutral massive weak sectors satisfy the electroweak mass relation.

6. **Corollary 1 — Electromagnetic residual symmetry**  
   The massless neutral direction is the unbroken electromagnetic gauge sector.

7. **Corollary 2 — Higgs scalar realization**  
   The physical scalar is the normal mode of the broken electroweak vacuum/interface.

---

## 5. What has to be defined explicitly in the paper

Do not leave these implicit:

- weak doublet in VDM language,
- weak singlet in VDM language,
- hypercharge in VDM language,
- electroweak vacuum/interface order parameter,
- neutral mixing basis,
- charged weak basis,
- unbroken electromagnetic direction,
- Weinberg angle,
- physical electric charge after mixing.

If any one of these is merely translated from standard notation without derivation, the paper will leak.

---

## 6. Validation logic required in the CF itself

The paper should state, in the CF, what would count as closure.

Required analytical checks:

- consistency of the electroweak fiber split with the canon inheritance stack,
- proof that the weak sector acts only on the left-handed boundary-hosted modes,
- neutral-sector diagonalization with one exactly massless direction,
- recovery of electric charge as the conserved residual Noether charge,
- derivation of the W/Z relation from the same broken-sector parameter.

Optional numeric/program witnesses for the paired CFN:

- toy matrix realization of neutral mixing,
- symbolic diagonalization of the neutral mass matrix,
- a minimal chiral/domain-wall mode witness showing left-only coupling,
- parameter sweep demonstrating the stable charged/neutral mass ratio under the derived normalization.

These numerics would be witnesses only, not proof burden.

---

## 7. What must be labeled honestly if not fully closed

If any of the following cannot be fully derived, they must be labeled explicitly:

- exact hypercharge normalization,
- exact numerical value of the Weinberg angle,
- fermion-generation structure beyond one minimal electroweak family,
- Yukawa hierarchy / flavor sector,
- radiative corrections to electroweak observables.

Do not pretend those are closed if the paper only closes the structural electroweak skeleton.

---

## 8. Deliverables for CF16

The paper is done only when it contains:

- a canon manifest,
- clean VDM-first definitions of electroweak objects,
- theorem-grade derivation of the electroweak split,
- theorem-grade derivation of left-handed weak coupling,
- theorem-grade derivation of neutral mixing and Weinberg angle,
- theorem-grade derivation of the W/Z mass relation,
- residual electromagnetic corollary,
- Higgs/interface closure in electroweak-specific form,
- falsification criteria,
- validation gates,
- CFN traceability plan.

---

## 9. Runtime relevance

This paper matters for runtime completion because it closes how:

- chirality-selective couplings emerge from the boundary-hosted architecture,
- gauge-sector splitting can produce selective interaction channels,
- broken/unbroken symmetry sectors coexist without ad hoc insertion,
- local structure can yield differentiated but lawful interaction pathways.

That is directly relevant to any runtime architecture that needs selective channel activation, stable neutral/background directions, and handed or role-specific coupling rules.

---

## 10. No-open-questions completion criterion

CF16 is complete only if the reader can answer, from the paper alone:

1. Why is the weak sector exactly non-abelian and left-acting?  
2. Why is there an accompanying abelian hypercharge sector?  
3. Why does neutral mixing occur?  
4. What determines the Weinberg angle?  
5. Why does one neutral direction stay massless?  
6. Why do the W and Z masses differ in the derived way?  
7. What, exactly, is the Higgs scalar in VDM terms?

If any of those are still answered by “that comes later,” the paper is not done.
