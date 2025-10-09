# Finite‑Tube Mode Analysis for the FUM Scalar (Bordag‑inspired)

>
> Author: Justin K. Lietz  
> Date: August 9, 2025
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.<br>
> Commercial use requires written permission from Justin K. Lietz.
>
> See LICENSE file for full terms.

---

## 1. Objective

Adapt the finite‑radius flux‑tube machinery in Bordag (Universe 2024) to the FUM scalar EFT so we can:

- Predict and count tachyonic (unstable) orbital modes in finite domains (tubes/filaments).
- Demonstrate quartic stabilization via condensation and show the full post‑condensation mass spectrum is non‑negative.
- Find a true energy minimum vs a control parameter (tube size/“flux” proxy), reproducing the qualitative structure of Fig. 1/3/5 in Bordag’s paper.

We work from the bounded baseline EFT and kinetic normalization already established in:

- Baseline quartic EFT and cubic tilt: see [derivation/foundations/discrete_to_continuum.md](Prometheus_VDM/derivation/foundations/discrete_to_continuum.md:125-228)
- Kinetic normalization and action‑based derivation: see [derivation/effective_field_theory/kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:78-134)
- Units map and FRW bookkeeping (used later for background energy): see [derivation/effective_field_theory/fum_voxtrium_mapping.md](Prometheus_VDM/derivation/effective_field_theory/fum_voxtrium_mapping.md:44-121)

We will mirror the analytical spine of Bordag’s finite‑radius analysis but for a real (optionally complex) scalar coupled only through its potential.

---

## 2. Baseline EFT, Units, and Geometry

Working in natural units \(c=\hbar=k_B=1\). The bounded baseline potential is
\[
V(\phi)\;=\;-\frac{1}{2}\,\mu^2\,\phi^2\;+\;\frac{\lambda}{4}\,\phi^4,\qquad \mu^2>0,\ \lambda>0,
\]
optionally augmented by a small cubic tilt
\[
V(\phi)\;\to\;V(\phi)\;+\;\frac{\gamma}{3}\,\phi^3,\qquad |\gamma|\ll \mu^2\sqrt{\lambda},
\]
to select a unique vacuum near \(+v\) with \(v=\mu/\sqrt{\lambda}\). Small fluctuations about \(\pm v\) have
\[
m_{\rm eff}^2\;=\;2\,\mu^2 \quad (\text{to leading order in }\gamma).
\]

Kinetic normalization in the dimensionless continuum:
\[
\mathcal L_K\;=\;\frac{1}{2}(\partial_t\phi)^2\;-\;J a^2\,(\nabla\phi)^2,\qquad c^2\equiv 2 J a^2,
\]
or equivalently \(\mathcal L_K=\frac{1}{2}(\partial_t\phi)^2-\frac{c^2}{2}(\nabla\phi)^2\).
No microscopic relation ties \(J\) to \(a\); one may set \(c=1\) by a units choice. See [derivation/effective_field_theory/kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:117-134).

Geometry: a straight cylinder (“tube”) of radius \(R\) aligned with the \(z\)-axis; we analyze the transverse \((x,y)\) plane in polar coordinates \((r,\theta)\). Inside the tube we can sustain an approximately “false‑vacuum”/uncondensed configuration that drives tachyonic behavior in the fluctuation spectrum; outside, we take the condensed vacuum.

---

## 3. Piecewise Background and Linearized Fluctuations

We define a static, piecewise‑constant background
\[
\phi_0(r)\;=\;\begin{cases}
\phi_{\rm in} \approx 0, & r<R \quad (\text{uncondensed/tachyonic})\\
\phi_{\rm out} \approx v, & r>R \quad (\text{condensed})
\end{cases}
\]
and consider small fluctuations \(\varphi(x)\) with \(\phi=\phi_0+\varphi\). Linearizing the EOM yields
\[
\big(\, \partial_t^2 - c^2 \nabla_\perp^2 - c^2 \partial_z^2 \,\big)\,\varphi \;+\; V''(\phi_0)\,\varphi \;=\;0,
\]
with
\[
V''(\phi)= -\mu^2 + 3\lambda \phi^2 + 2\gamma \phi.
\]
To leading order (and \(\gamma\to 0\) here for clarity),
\[
m_{\rm in}^2 \equiv V''(\phi_{\rm in}\approx 0) = -\mu^2 \;,&\quad\text{(tachyonic inside)}
\]
\[
m_{\rm out}^2 \equiv V''(\phi_{\rm out}\approx v) = 2\,\mu^2 \;,&\quad\text{(massive outside)}.
\]

We separate variables
\[
\varphi(t,r,\theta,z)= e^{-i\omega t} e^{i k z} \sum_{\ell\in\mathbb Z} u_{\ell}(r) e^{i\ell\theta}.
\]
The radial modes \(u_\ell(r)\) obey
\[
\left[\,-c^2\left(\frac{d^2}{dr^2} + \frac{1}{r}\frac{d}{dr} - \frac{\ell^2}{r^2}\right) + m^2(r)\,\right]u_\ell(r)\;=\;(\omega^2 - c^2 k^2)\,u_\ell(r),
\]
with \(m^2(r)=m_{\rm in}^2\) for \(r<R\) and \(m_{\rm out}^2\) for \(r>R\).

Introduce the (transverse) separation constant \(\kappa^2\) via
\[
\omega^2 - c^2 k^2 \equiv - c^2 \kappa^2.
\]
Then the radial equation becomes Bessel‑type with piecewise constant coefficients.

---

## 4. Radial Solutions and Matching Conditions

Inside (\(r<R\); tachyonic \(m_{\rm in}^2=-\mu^2\)):
\[
\left(\frac{d^2}{dr^2}+\frac{1}{r}\frac{d}{dr}-\frac{\ell^2}{r^2}\right) u_\ell^{\rm (in)}(r) \;=\; \left(\kappa_{\rm in}^2\right) u_\ell^{\rm (in)}(r),
\qquad \kappa_{\rm in}^2 \equiv \frac{\mu^2}{c^2} - \kappa^2.
\]
Regular at \(r=0\) \(\Rightarrow\) \(u_\ell^{\rm (in)}(r) = A_\ell I_\ell(\kappa_{\rm in} r)\) if \(\kappa_{\rm in}^2>0\), with \(I_\ell\) modified Bessel.

Outside (\(r>R\); massive \(m_{\rm out}^2=2\mu^2\)):
\[
\left(\frac{d^2}{dr^2}+\frac{1}{r}\frac{d}{dr}-\frac{\ell^2}{r^2}\right) u_\ell^{\rm (out)}(r) \;=\; -\left(\kappa_{\rm out}^2\right) u_\ell^{\rm (out)}(r),
\qquad \kappa_{\rm out}^2 \equiv \kappa^2 + \frac{2\mu^2}{c^2}.
\]
Normalizable at \(r\to\infty\) \(\Rightarrow\) \(u_\ell^{\rm (out)}(r) = B_\ell K_\ell(\kappa_{\rm out} r)\) with \(K_\ell\) modified Bessel of the second kind.

Matching at \(r=R\) (continuity of \(u\) and \(u'\)):
\[
A_\ell I_\ell(\kappa_{\rm in} R) \;=\; B_\ell K_\ell(\kappa_{\rm out} R),
\]
\[
A_\ell \kappa_{\rm in} I'_\ell(\kappa_{\rm in} R) \;=\; - B_\ell \kappa_{\rm out} K'_\ell(\kappa_{\rm out} R).
\]
Eliminate \(A_\ell/B_\ell\) to obtain the secular equation for \(\kappa\):
\[
\boxed{ \;\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\,\frac{I'_\ell(\kappa_{\rm in} R)}{I_\ell(\kappa_{\rm in} R)}
\;=\; - \frac{K'_\ell(\kappa_{\rm out} R)}{K_\ell(\kappa_{\rm out} R)}\; }.
\]
Each root \(\kappa=\kappa_\ell(R)\) determines a mode. Tachyonic (unstable) modes correspond to \(\omega^2<0\) for some \(k\); equivalently, sufficiently large \(\kappa\) such that \(\omega^2=c^2(k^2-\kappa^2)<0\) at \(k=0\).

Counting unstable modes:

- At \(k=0\), \(\omega^2=-c^2\kappa^2\). A mode is tachyonic if \(\kappa^2>0\).
- The number \(N_{\rm tach}(R)\) is the count of \(\ell\) for which the secular equation admits \(\kappa_\ell^2>0\).

This mirrors Bordag’s finite‑radius tower and the scaling \(N_{\rm tach}\sim \text{(control parameter)}\).

---

## 5. Effective 2D Mode Reduction and Quartic Couplings

Expand \(\varphi\) in the orthonormal set \(\{u_{\ell n}(r)e^{i\ell\theta}\}\) (including radial overtones \(n\) if present) and integrate over the transverse plane to obtain a 2D effective action in \((t,z)\):
\[
S_{\rm eff}^{(2D)} \;=\; \int dt\,dz\;\sum_{\ell,n} \left[ \frac{1}{2}\left( \dot\psi_{\ell n}^2 - c^2 (\partial_z \psi_{\ell n})^2 \right) - \frac{1}{2} m_{\ell n}^2(R)\,\psi_{\ell n}^2 \right] \;-\; \frac{1}{4} \sum_{\{\ell_i n_i\}} N_4(\ell_i n_i;R)\, \psi_{\ell_1 n_1}\psi_{\ell_2 n_2}\psi_{\ell_3 n_3}\psi_{\ell_4 n_4},
\]
with
\[
m_{\ell n}^2(R) \;\equiv\; -\,c^2 \kappa_{\ell n}^2(R),
\]
and quartic couplings obtained from overlap integrals using the original \(\lambda\phi^4\) term:
\[
N_4(\ell_i n_i;R) \;\propto\; \lambda \int_0^\infty r\,dr \int_0^{2\pi}\!d\theta\;\prod_{i=1}^4 \, u_{\ell_i n_i}(r) e^{i\ell_i\theta},
\]
subject to \(\sum_i \ell_i=0\) by \(\theta\) integration. The normalization/weighting follows the kinetic inner product implied by \(\mathcal L\).

---

## 6. Condensation and Post‑Condensation Mass Matrix

At tree level, minimize the effective potential
\[
V_{\rm eff}^{\rm tube}(\{\psi\},R) \;=\; \sum_{\ell n} \frac{1}{2} m_{\ell n}^2(R)\,\psi_{\ell n}^2 \;+\; \frac{1}{4} \sum_{\{\ell_i n_i\}} N_4(\ell_i n_i;R)\,\psi_{\ell_1 n_1}\psi_{\ell_2 n_2}\psi_{\ell_3 n_3}\psi_{\ell_4 n_4}
\]
to get condensates \(v_{\ell n}(R)\). The (tree‑level) mass matrix about the condensate is the Hessian
\[
\left(M^2\right)_{(\ell n),(\ell' n')}(R) \;=\; \left.\frac{\partial^2 V_{\rm eff}^{\rm tube}}{\partial \psi_{\ell n}\,\partial \psi_{\ell' n'}}\right|_{\psi=v}.
\]
Acceptance criterion (Bordag‑parallel): all eigenvalues of \(M^2\) are \(\ge 0\) after condensation, with Goldstone phases (if a complex scalar is used) remaining massless as appropriate.

---

## 7. Total Energy vs Control and the Minimum

Define the total energy as
\[
E(R) \;=\; E_{\rm bg}(R) \;+\; V_{\rm eff}^{\rm tube}\big(\{v_{\ell n}(R)\},R\big).
\]

- In Bordag’s SU(2) case, \(E_{\rm bg}\propto B^2 R^2\) from the chromomagnetic background.
- In our scalar‑only EFT, one can adopt a phenomenological background proxy if coupling to external sectors is present (e.g., Voxtrium sourcing); in a pure scalar test, set \(E_{\rm bg}=0\) and examine whether \(V_{\rm eff}^{\rm tube}\) develops a nontrivial \(R\)‑dependence with a minimum due to mode structure and normalization.

For FRW‑consistent background bookkeeping use the transfer‑current formalism in [derivation/effective_field_theory/fum_voxtrium_mapping.md](Prometheus_VDM/derivation/effective_field_theory/fum_voxtrium_mapping.md:106-121) when embedding in cosmology; here we remain in a static Minkowski test.

Acceptance criterion: an \(R_\ast\) at which \(E(R)\) has a true minimum (Bordag’s Fig. 5 analogue).

---

## 8. Thermal Corrections (optional)

At high temperature, the effective mass receives thermal contributions \(m^2(T)\sim m^2 + c_T \lambda T^2\), tending to restore symmetry (melt the condensate). A CJT/Hartree or high‑\(T\) expansion can be layered onto \(V_{\rm eff}^{\rm tube}\) to show \(v_{\ell n}\to 0\) as \(T\) increases, mirroring Bordag’s qualitative result.

---

## 9. Computational Pipeline and APIs

We propose two modules to implement and test this analysis:

1) cylinder_modes.py (radial/matching solver)

- API:
  - compute_kappas(R, params) -> list of roots {(\(\ell\), n, \(\kappa_{\ell n}\))}
    - params: \(\mu, \lambda, \gamma, c\) and numerical tolerances; optionally max \(|\ell|\) and radial overtone cutoff
  - mode_functions(R, root) -> callable u_{\ell n}(r) with normalization info
- Core tasks:
  - Solve the secular equation
    \[
    \frac{\kappa_{\rm in}}{\kappa_{\rm out}}\,\frac{I'_\ell(\kappa_{\rm in} R)}{I_\ell(\kappa_{\rm in} R)}
    \;=\; - \frac{K'_\ell(\kappa_{\rm out} R)}{K_\ell(\kappa_{\rm out} R)},
    \]
    with \(\kappa_{\rm in}^2=\mu^2/c^2-\kappa^2\) and \(\kappa_{\rm out}^2=\kappa^2+2\mu^2/c^2\).
  - Count \(N_{\rm tach}(R)\) from roots with \(\kappa^2>0\).
  - Return normalized u’s (with weight \(r\,dr\,d\theta\)).

2) condense_tube.py (tree‑level condensation and spectra)

- API:
  - build_N4(R, modes, params) -> sparse tensor or contracted quartic map
  - find_condensate(R, modes, N4, params) -> \(\{v_{\ell n}\}\)
  - mass_matrix(R, modes, v, N4, params) -> eigenvalues/eigenvectors
  - energy_scan(R_grid, …) -> E(R) with identified minima
- Outputs:
  - Plots mirroring Bordag:
    - \(\kappa_\ell(R)\) vs \(R\) (pre‑condensation “tachyonic tower”)
    - \(v_{\ell n}(R)\) vs \(\ell\) (condensate structure)
    - \(E(R)\) vs \(R\) with true minimum (if present)

Units and normalizations:

- Use the dimensionless \(c\) from \(\mathcal L_K=\frac{1}{2}(\partial_t\phi)^2-\frac{c^2}{2}(\nabla\phi)^2\). Convert to physical units via \((\phi_0,\tau,a)\) as in [derivation/effective_field_theory/fum_voxtrium_mapping.md](Prometheus_VDM/derivation/effective_field_theory/fum_voxtrium_mapping.md:44-80) when needed.

---

## 10. Acceptance Criteria (Bordag‑parallel)

- Tachyonic mode tower: discrete \(\kappa_\ell(R)\) solutions with a finite count \(N_{\rm tach}(R)\) that grows with \(R\) (qualitatively matching a \(\delta\)-like control).
- Post‑condensation positivity: all Hessian eigenvalues \(\ge 0\) (massless phases only if a complex field is used).
- Energy minimum: \(E(R)\) develops a genuine minimum for some parameter window (quartic strengths), analogous to Bordag’s \(\lambda\)‑dependence in Fig. 5.

---

## 11. Notes on Complex Extension and Goldstones (optional)

Promote \(\phi\) to a complex field \(\Phi\) to demonstrate explicit Goldstone modes in the broken phase. The radial analysis proceeds similarly with coupled channels for real/imaginary parts; post‑condensation, phases are massless while radial modes are massive. This reproduces the “massless Goldstone + massive radial” structure standard in SSB.

---

## 12. References and Pointers

- Bordag, M. (2024). Universe 10, 38. Finite‑radius chromomagnetic flux tube, tachyonic gluon modes, quartic stabilization, and energy minima. Local copy: [universe-10-00038-v2.pdf](Prometheus_VDM/derivation/supporting_work/external_references/papers/universe-10-00038-v2.pdf)
- FUM kinetic/action derivation and normalization: [derivation/effective_field_theory/kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:78-134)
- Discrete‑to‑continuum and bounded baseline potential (adopted here): [derivation/foundations/discrete_to_continuum.md](Prometheus_VDM/derivation/foundations/discrete_to_continuum.md:125-228)
- Units/FRW/current bookkeeping (for background energy coupling in cosmology): [derivation/effective_field_theory/fum_voxtrium_mapping.md](Prometheus_VDM/derivation/effective_field_theory/fum_voxtrium_mapping.md:106-121)

---

## 13. Summary

This appendix defines a concrete, testable finite‑domain mode problem for the FUM scalar EFT. It specifies the radial eigenvalue condition, mode counting, quartic projections, condensation, mass‑matrix positivity, and an energy‑vs‑size scan with clear acceptance criteria aligned to Bordag’s analysis. The companion code modules [cylinder_modes.py](fum_sim/cylinder_modes.py:1) and [condense_tube.py](fum_sim/condense_tube.py:1) will implement the solver and diagnostics, producing the three replication plots and an \(R_\ast\) selection where applicable.
