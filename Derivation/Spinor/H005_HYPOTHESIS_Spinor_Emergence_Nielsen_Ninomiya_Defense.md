# HYPOTHESES

---

## H005 — Spinor Emergence Nielsen-Ninomiya Defense

**Classification:** Axiom-core  
**Owner:** Justin K. Lietz  
**Status:** ACTIVE  
>*PROVEN requires all gates to PASS with figure+JSON artifacts.
**One-line objective:** The VDM J-limb scalar lattice produces emergent Dirac spinors via domain-wall fermions that satisfy the Ginsparg-Wilson relation, evading Nielsen-Ninomiya doubling through topological separation and preserving exact chiral symmetry at the lattice scale.

### Formal statement

On a cubic lattice with scalar field $W_i$ governed by the discrete action [VDM-AX-004](../AXIOMS.md#vdm-ax-004), there exists a construction of effective fermion operators $\psi(x)$ through:

1. **Domain-wall mechanism** ([Kaplan, 1992](https://doi.org/10.1016/0370-2693(92)91112-M)): A kink profile in the scalar background creates a $(d-1)$-dimensional interface supporting chiral bound states, with physical fermions localized to the domain wall and doublers exponentially suppressed in an auxiliary lattice coordinate $z$ used to construct domain-wall zero-modes.

2. **Ginsparg-Wilson operator**: The effective Dirac operator $D$ satisfies
   $$\{D, \gamma_5\} = a D \gamma_5 D + O(a^2)$$
   preserving exact chiral symmetry on the lattice without species doubling.

3. **Locality preservation**: In 3D, the Jordan-Wigner string operator is replaced by a **generalized construction** (e.g., Bravyi-Kitaev tree encoding) ensuring fermion hopping remains local with range $O(\log N)$ rather than $O(N)$.

4. **Residual mass suppression**: For domain walls separated by bulk depth $L_5$, the residual mass scales as
   $$m_{\text{res}} \sim e^{-\lambda L_5}$$
   where $\lambda > 0$ is the decay rate of the domain-wall bound state into the bulk.

5. **Lorentz invariance at low energy**: The dispersion relation $E^2(p)$ exhibits rotational symmetry at $|p| \ll \pi/a$ with metriplectic M-limb dissipation smoothing lattice anisotropies via renormalization group flow.

### Predictions (decisive metrics – pass/fail)

- **P1 (Ginsparg-Wilson relation):** $\| \{D, \gamma_5\} - a D \gamma_5 D \|_{\infty} \leq 10^{-12}$ on coarse cells of size $\ell = 4a$.
- **P2 (Residual mass scaling):** $m_{\text{res}}(L_5) / m_{\text{res}}(L_5/2) \leq e^{-\lambda L_5/2}$ with $\lambda \geq 0.1/a$.
- **P3 (Dispersion linearity):** For $|p| < \pi/(10a)$, $R^2$ of linear fit $E(p) = v_F |p| + O(p^3)$ satisfies $R^2 \geq 0.9999$.
- **P4 (Rotational isotropy):** Angular variation of $E(p)$ at fixed $|p| = 0.1\pi/a$: $\Delta E / \bar{E} \leq 10^{-3}$.
- **P5 (Locality of JW string):** For generalized Jordan-Wigner on 3D lattice, fermion operator support scales as $O(\log^2 N)$ sites (Bravyi-Kitaev bound).

Each prediction must pass in dedicated T1-tier numerical tests with deterministic seeds and provenance logging.

### Rationale (bounded)

**Prior results supporting this approach:**

1. **Kaplan fermions** (Kaplan, 1992; Shamir, 1993): Domain-wall fermions successfully implement chiral symmetry on the lattice in lattice QCD simulations, with residual masses $m_{\text{res}} \sim 10^{-3}$ for practical $L_5 \sim 10-20$.

2. **Ginsparg-Wilson relation** ([Ginsparg & Wilson, 1982](https://doi.org/10.1103/PhysRevD.25.2649)): Provides the fundamental framework for exact chiral symmetry on the lattice; implemented via overlap operators (Neuberger, 1998) and domain-wall constructions.

3. **Bravyi-Kitaev transformation** ([Bravyi & Kitaev, 2002](https://doi.org/10.1006/aphy.2002.6254)): Reduces Jordan-Wigner string nonlocality from $O(N)$ to $O(\log N)$ on cubic lattices, preserving fermion algebra with logarithmic overhead.

4. **VDM J-limb structure**: The conservative metriplectic limb [VDM-AX-004](../AXIOMS.md#vdm-ax-004) already supports:
   - Klein-Gordon dynamics in continuum limit [VDM-AX-C02](../AXIOMS.md#vdm-ax-c02)
   - Noether currents from translation symmetry [VDM-AX-A3](../AXIOMS.md#vdm-ax-a3)
   - Topological defects (kinks, domain walls) from tachyonic potential

**Dimensional argument:**  
A domain wall in a $(d+1)$-dimensional scalar theory naturally supports $(d-1)$-dimensional chiral fermions. The VDM scalar lattice in 3+1D with a tachyonic kink in an auxiliary lattice coordinate $z$ used to construct domain-wall zero-modes hosts 2+1D chiral modes at the wall. Doubling is avoided by exponential localization: physical fermions at $z=0$, doublers at $z=\pm\infty$.

**Nielsen-Ninomiya evasion:**  
The No-Go theorem requires **locality**, **translation invariance**, and **hermiticity** for the **same lattice**. Domain-wall fermions break the assumption by:
- Adding a bulk dimension (translation symmetry broken along $z$)
- Confining physical states to a topological defect (not uniformly distributed)

### Preconditions & scope

**Domain:**  
- Cubic lattice $\mathbb{Z}^3 \times \mathbb{Z}$ (space-time) with spacing $a$.
- Scalar field $W_i$ with tachyonic potential $V(W) = -\frac{1}{2}\mu^2 W^2 + \frac{1}{4}\lambda W^4$.
- Auxiliary lattice coordinate $z \in [0, L_5]$ used to construct domain-wall zero-modes with domain wall at $z=0$.

**Parameters:**  
- Lattice spacing: $a \in [0.01, 0.1]$ (dimensionless units with $\hbar = c = 1$).
- Coupling: $J \in [0.1, 10]$ (kinetic energy scale).
- Potential: $\mu^2 > 0$ (tachyonic), $\lambda > 0$ (stabilizing).
- Bulk depth: $L_5 \in [5, 50]$ lattice sites.
- Coarse-graining scale: $\ell = 4a$ (for Clifford algebra construction).

**Timescale window:**  
- Low-energy effective theory: $E < 0.1 \pi/a$ (continuum limit).
- Chiral modes: wavelengths $\lambda \gg a$ (long-wavelength approximation).

**Exclusions:**  
- High-energy regime $E \sim \pi/a$ (lattice cutoff effects dominate).
- Strong-coupling regime where continuum limit breaks down.
- Extremely small $L_5 < 5$ (residual mass too large).

### Experiment plan (E1, E2, …)

- **E1 (Domain-wall profile):** Construct a static kink background $W_{\text{bg}}(z)$ in the 5th dimension; verify exponential decay $|W - W_{\pm}| \sim e^{-\lambda z}$ with $\lambda > 0$.
  - **Inputs:** Potential parameters $(\mu, \lambda)$, bulk size $L_5$.
  - **Outputs:** Profile $W_{\text{bg}}(z)$, decay rate $\lambda$, PNG figure.
  - **Gates:** $\lambda \geq 0.1/a$, exponential fit $R^2 \geq 0.99$.
  - **Artifact paths:** `Derivation/code/outputs/figures/spinor/domain_wall_profile.png`, `Derivation/code/outputs/logs/spinor/domain_wall_profile.json`.

- **E2 (Bound-state spectrum):** Solve the linearized discrete Dirac equation around $W_{\text{bg}}(z)$ for the lowest-energy mode; verify linear dispersion $E(p) \propto |p|$ near $p=0$.
  - **Inputs:** Background $W_{\text{bg}}$, coarse cell size $\ell=4a$.
  - **Outputs:** Dispersion $E(p)$, Fermi velocity $v_F$, PNG figure, CSV log.
  - **Gates:** Linear fit $R^2 \geq 0.9999$ for $|p| < 0.1\pi/a$, $v_F / c \in [0.1, 10]$.
  - **Artifact paths:** `Derivation/code/outputs/figures/spinor/dispersion_linear.png`, `Derivation/code/outputs/logs/spinor/dispersion_linear.csv`.

- **E3 (Ginsparg-Wilson verification):** Construct the effective Dirac operator $D$ on coarse cells; numerically verify $\{D, \gamma_5\} = a D \gamma_5 D$ to machine precision.
  - **Inputs:** Lattice configuration, coarse cell $\ell=4a$, gamma matrices $\gamma^\mu$.
  - **Outputs:** Residual $\| \{D, \gamma_5\} - a D \gamma_5 D \|_{\infty}$, PNG figure, JSON log.
  - **Gates:** Residual $\leq 10^{-12}$.
  - **Artifact paths:** `Derivation/code/outputs/figures/spinor/ginsparg_wilson_check.png`, `Derivation/code/outputs/logs/spinor/ginsparg_wilson_check.json`.

- **E4 (Residual mass scaling):** Vary bulk depth $L_5 \in \{5, 10, 20, 40\}$; measure $m_{\text{res}}$ from the zero-momentum fermion propagator.
  - **Inputs:** Domain-wall backgrounds with varying $L_5$.
  - **Outputs:** $m_{\text{res}}(L_5)$, exponential fit parameters, PNG figure, CSV log.
  - **Gates:** Exponential scaling $m_{\text{res}}(L_5) \sim e^{-\lambda L_5}$ with $R^2 \geq 0.99$, $\lambda \geq 0.1/a$.
  - **Artifact paths:** `Derivation/code/outputs/figures/spinor/residual_mass_scaling.png`, `Derivation/code/outputs/logs/spinor/residual_mass_scaling.csv`.

- **E5 (Lorentz invariance check):** Compute $E(p)$ for fixed $|p| = 0.1\pi/a$ at 24 angular directions; verify rotational symmetry.
  - **Inputs:** Bound-state Hamiltonian, momentum grid.
  - **Outputs:** Angular variation $\Delta E / \bar{E}$, polar plot, JSON log.
  - **Gates:** $\Delta E / \bar{E} \leq 10^{-3}$.
  - **Artifact paths:** `Derivation/code/outputs/figures/spinor/lorentz_isotropy_polar.png`, `Derivation/code/outputs/logs/spinor/lorentz_isotropy.json`.

- **E6 (Locality of JW string):** Implement Bravyi-Kitaev transformation on a $32^3$ lattice; measure operator support scaling.
  - **Inputs:** 3D cubic lattice, fermion creation/annihilation sites.
  - **Outputs:** Operator support size vs $N$, log-log plot, CSV log.
  - **Gates:** Support $\leq C \log^2 N$ with $C \sim 1$.
  - **Artifact paths:** `Derivation/code/outputs/figures/spinor/bk_locality_scaling.png`, `Derivation/code/outputs/logs/spinor/bk_locality_scaling.csv`.

### Rough roadmap from CF* to T9

**Ideal path:**

1. **CF* (Complete Formalism):** Derive domain-wall fermions from VDM J-limb; prove Ginsparg-Wilson relation analytically; establish Bravyi-Kitaev construction for 3D.
   - Deliverable: `CF*_Spinor_Emergence_Domain_Wall_Fermions.md` with lemmas and proofs.

2. **T0 (Concept):** Minimal numerical checks of domain-wall profile and bound-state existence.
   - Deliverable: `T0_PROPOSAL_Spinor_Emergence_Domain_Wall.md`, `T0_RESULTS_Spinor_Emergence_Domain_Wall.md`.

3. **T1 (Proto-model):** Full implementation of E1-E6 with pass/fail gates; verify all 5 predictions.
   - Deliverable: `T1_PROPOSAL_Spinor_Emergence_v2.md`, `T1_RESULTS_Spinor_Emergence_v2.md`.

4. **T2 (Instrument):** Certify fermion operators as validated meters for measuring baryon-like charges and spin currents.
   - Deliverable: `T2_PROPOSAL_Fermion_Operators_Certification.md`, `T2_RESULTS_Fermion_Operators_Certification.md`.

5. **T3-T6:** Apply to baryogenesis, proton stability, chiral anomaly cancelation.

6. **T7-T8:** Out-of-sample predictions (e.g., coupling to gauge fields, finite temperature).

7. **T9:** External reproduction (lattice QCD community validating VDM domain-wall construction).

**Response to proven failure:**

- If **P1 fails** (Ginsparg-Wilson violated): Investigate whether a Wilson-like term appears; attempt overlap operator construction; if unrecoverable, flag chiral symmetry as broken and pivot to massive Dirac theory (Standard Model-incompatible but still interesting for effective field theory).

- If **P2 fails** (residual mass does not decay exponentially): Domain-wall mechanism may be invalid; check for tunneling saturation or bulk instabilities; consider alternative constructions (staggered fermions, twisted boundary conditions).

- If **P3 fails** (dispersion not linear): Low-energy effective theory may have higher-order corrections; investigate whether $v_F$ depends on lattice artifacts; recalibrate coarse-graining scale $\ell$.

- If **P4 fails** (Lorentz violation persists): Check if M-limb dissipation is insufficient for RG flow to isotropy; may require explicit smoothing or larger coarse-graining scale; if unrecoverable, accept approximate Lorentz symmetry with quantified violation.

- If **P5 fails** (JW string remains non-local): Fall back to 1D/2D systems where standard JW works; for 3D, explore alternative fermionization schemes (slave-particle methods, gauge constraints).

- **Kill criterion:** If **any two** of P1-P5 fail with residuals exceeding thresholds by $>10\times$, halt T1 and document as a falsified hypothesis. Issue `CONTRADICTION_REPORT.json` and archive under `failed_runs/`.

### Risks & kill‑methods

**Risk 1: Domain-wall fermions require fine-tuning.**  
Nielsen-Ninomiya is evaded by topology, but practical $L_5$ may be too large (computationally expensive) or too small (residual mass too large). If $m_{\text{res}} > 0.1 m_{\text{physical}}$ for accessible $L_5 \leq 50$, the construction is not phenomenologically viable.

**Kill method:** Run E4 with $L_5 \in \{5, 10, 20, 40\}$. If $m_{\text{res}}(40)$ does not reach $< 10^{-2}$, abandon and document.

**Risk 2: Bravyi-Kitaev overhead breaks causality.**  
Even with $O(\log N)$ support, the effective speed of light for fermions may depend on $N$, violating [VDM-AX-A2](../AXIOMS.md#vdm-ax-a2). If information propagates faster than $c$ in the emergent theory, local causality is broken.

**Kill method:** Run E6 and measure fermion propagation speed $v_F$ vs $N$. If $v_F(N) / c$ grows with $N$, the theory is non-local and invalid.

**Risk 3: Lattice anisotropy persists at low energy.**  
If the dispersion relation remains "squarish" (hypercubic symmetry instead of $SO(3)$) even at $|p| \ll \pi/a$, Lorentz invariance is broken. This would invalidate Standard Model compatibility.

**Kill method:** Run E5. If $\Delta E / \bar{E} > 10^{-2}$ for $|p| = 0.1\pi/a$, the effective theory is not rotationally invariant. Document as Lorentz-violating and assess phenomenological impact.

**Risk 4: Ginsparg-Wilson is not achieved.**  
If the effective operator is Wilson-like (explicit chiral symmetry breaking), fermions acquire hard masses unrelated to Higgs coupling. This would prevent chiral Standard Model reproduction.

**Kill method:** Run E3. If $\| \{D, \gamma_5\} - a D \gamma_5 D \|_{\infty} > 10^{-10}$, chiral symmetry is explicitly broken. Attempt overlap operator; if that also fails, document and pivot to non-chiral effective theory.

**Risk 5: Doublers re-emerge.**  
If the domain-wall separation is insufficient or the Bravyi-Kitaev transformation is incorrectly implemented, doublers may appear in the spectrum at high momentum.

**Kill method:** In E2, scan full Brillouin zone $|p| \leq \pi/a$. If additional zero-energy modes appear at $p = (\pi/a, 0, 0)$ or other high-symmetry points, doubling is not resolved. Halt and investigate bulk decoupling failure.

### Links

- **H*_** (this hypothesis): `H001_HYPOTHESIS_Spinor_Emergence_Nielsen_Ninomiya_Defense.md`
- **CF*_** (complete formalism): `CF*_Spinor_Emergence_Domain_Wall_Fermions.md` (to be created)
- **T1_** (proposal): `T1_PROPOSAL_Spinor_Emergence_v2.md` (to be updated)
- **T1_** (results): `T1_RESULTS_Spinor_Emergence_v2.md` (to be created after experiments)
- **Canonical axioms:** [AXIOMS.md](../AXIOMS.md) (VDM-AX-004, A2, A3, A4)
- **Canonical equations:** [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
- **Nielsen-Ninomiya references:**
  - [Nielsen & Ninomiya (1981)](https://doi.org/10.1016/0550-3213(81)90535-X) - Original No-Go theorem
  - [Kaplan (1992)](https://doi.org/10.1016/0370-2693(92)91112-M) - Domain-wall fermions
  - [Ginsparg & Wilson (1982)](https://doi.org/10.1103/PhysRevD.25.2649) - Chiral symmetry on the lattice
  - [Bravyi & Kitaev (2002)](https://doi.org/10.1006/aphy.2002.6254) - Fermionic quantum computation

### Version history

- v0.1 2025-11-20 – copilot/evaluate-ninomiya-theorem - created in response to Red Team Assessment
