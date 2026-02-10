# CF11: Dark Sector Emergence from Metriplectic Dynamics

**Date:** 2026-02-06  

**Revision:** 2026-02-07 — tightened for CFN readiness
**Status:** Corrected rewrite (T1 formalism) — ready for T2 lattice validation + T3 cosmology regression  
**Prerequisites:** CF01 (QGT → J⊕M), CF03 (A8 hierarchical interfaces), CF04 (Telegraph–Fisher causality), CF10 (lattice→continuum program)  
**Scope classification:** **Derived-limit** (cosmology/continuum modeling built on axiom-core metriplectic structure)

---

## Executive Summary

This document defines a **clean, falsifiable** way to interpret the VDM metriplectic split as an **effective two-component “dark sector”** at cosmological scales, without postulating new fundamental particles.

What CF11 does **and does not** claim:

- **Does:**  
  1) Provides a **well-posed decomposition of dynamics** into reversible (J) and irreversible (M) channels (imported from CF01).  
  2) Defines an **operational split of coarse-grained stress-energy** into two effective components, plus a controlled “interaction remainder,” using **mode projections** (not an ad hoc field split).  
  3) Derives **equations-of-state (EoS) limits** under explicit, checkable regime assumptions:
     - a coherent, slowly varying, nearly homogeneous sector has **w ≈ −1**;  
     - a defect/oscillation-dominated, non-relativistic sector has **w ≈ 0**.  
  4) Converts the split into **binary falsification gates** on lattice simulations (T2) and cosmological data (T3+).

- **Does not:**  
  - Claim that a literal field identity **Φ = Φ_J + Φ_M** is globally unique for all configurations.  
  - Claim exact “cross-term cancellation” beyond the quadratic/controlled regime where it can be proven.  
  - Smuggle dissipation into a covariant “Lagrangian.” Dissipation enters via **M and Σ**, as in metriplectic/GENERIC form.

---

## 0. Corrections vs CF11 v1.0 (for provenance)

This rewrite fixes the specific failure modes in the previous draft:

1. **Invalid projectors** (e.g., “\(P_J = J/\sqrt{J^2+M^2}\)”) are removed. The split is now defined via **spectral (Riesz) projections** of the linearized generator, which is mathematically standard and testable.
2. The document no longer asserts a global **L²-orthogonality** \(\int \Phi_J\Phi_M = 0\) as a fundamental theorem. Orthogonality is instead defined **with respect to a chosen quadratic form** (energy Hessian / quantum metric) and only within the regime where the projection is defined.
3. The stress-energy discussion is rewritten to avoid incorrect curved-space Noether formulas and non-minimal coupling mistakes. The main text uses a **minimal derived-limit scalar-field proxy**; optional curvature couplings are quarantined to an appendix.
4. The EoS derivations are corrected:
   - \(w = (\epsilon-1)/(\epsilon+1)\) with \(w\approx -1 + 2\epsilon\) for \(\epsilon\ll 1\) (no spurious factors).
   - The “\(w_M\to 0\)” limit is derived via **(i) non-relativistic defect kinematics** and **(ii) rapid oscillation in a quadratic minimum**, not via inconsistent algebra.
5. “Telegraph speed” is aligned with CF04/CF03: finite front speed is governed by **\(c=\sqrt{D/\tau}\)** (CF04) and can be throttled by hierarchy via **\(c_{\mathrm{eff}}=c_0 e^{-\beta D_{\mathrm{void}}/2}\)** (CF03 / VDM‑E‑106).

---

## 1. Imports from earlier CF modules

### 1.1 Metriplectic structure (CF01, CF02)

We assume the axiom-core form (A4):

\[
\partial_t q \;=\; J(q)\,\frac{\delta \mathcal{I}}{\delta q} \;+\; M(q)\,\frac{\delta \Sigma}{\delta q},
\qquad
J^\top=-J,\;\; M^\top=M\ge 0,
\]
with degeneracy conditions
\[
J(q)\,\frac{\delta \Sigma}{\delta q}=0,\qquad
M(q)\,\frac{\delta \mathcal{I}}{\delta q}=0,
\]
and entropy law
\[
\frac{d\Sigma}{dt}=\left\langle \frac{\delta\Sigma}{\delta q},\, M\,\frac{\delta\Sigma}{\delta q}\right\rangle \ge 0.
\]

Interpretation (CF01):
- **J-channel**: reversible, Hamiltonian/symplectic transport (Berry curvature origin).
- **M-channel**: irreversible, gradient-flow transport (quantum metric / Fisher origin).

### 1.2 Hierarchical interfaces and void-debt throttling (CF03)

CF03 provides the hierarchy program and the speed throttling law (VDM‑E‑106):

\[
c_{\mathrm{eff}}(k)=c_0\,e^{-\beta D_{\mathrm{void}}(k)/2},
\qquad D_{\mathrm{void}}(k)\sim k \;\; \text{for depth } k.
\]

### 1.3 Finite-speed transport (CF04)

CF04 derives telegraph/Cattaneo transport, including the cone speed relation

\[
c = \sqrt{D/\tau},
\]

and provides numerical gates for light-cone preservation and dispersion consistency.

---

## 2. A derived-limit proxy model (scalar order parameter + metriplectic thermostat)

CF11’s cosmology statements require a concrete “bookkeeping” model that maps a VDM state \(q\) to (i) an energy-like conserved functional \(\mathcal{I}\), (ii) an entropy functional \(\Sigma\), and (iii) local densities usable on a lattice.

We use a **minimal derived-limit proxy** consistent with the CF03 phase-field picture, but we do it in a way that respects the metriplectic degeneracy condition \(M\,\delta \mathcal{I}=0\).

### 2.1 State, functionals, and why an extra variable is required

If you try to model “damping” using only a pair \((\Phi,\Pi)\), any explicit friction term \(-\Pi/\tau\) will generically **drain the energy functional** \(\mathcal{I}[\Phi,\Pi]\), violating the axiom-core condition \(d\mathcal{I}/dt=0\).

The standard metriplectic fix is simple: include a **reservoir coordinate** that stores the energy removed from the mechanical variables while increasing entropy.

Define the state
\[
q=(\Phi,\Pi,u),
\]
where \(u(x,t)\) is a local “internal energy / bath” density.

Choose the conserved functional
\[
\mathcal{I}[\Phi,\Pi,u] = \int d^3x\;\Big(\tfrac12 \Pi^2 + \tfrac12 |\nabla \Phi|^2 + V(\Phi) + u\Big),
\]
and an entropy functional of the form
\[
\Sigma[\Phi,\Pi,u] = \int d^3x\; s(u),
\qquad s'(u)>0.
\]

### 2.2 A concrete J and M that satisfy the degeneracy conditions

Let the Poisson operator act canonically on \((\Phi,\Pi)\) and leave \(u\) untouched:
\[
J=\begin{pmatrix}
0 & 1 & 0\\
-1& 0 & 0\\
0 & 0 & 0
\end{pmatrix}.
\]

Define a metric operator that couples \(\Pi\) and \(u\) through a rank‑1, positive semidefinite block:
\[
M(q)=\frac{1}{\tau\,s'(u)}\;
\begin{pmatrix}
0 & 0 & 0\\
0 & 1 & -\Pi\\
0 & -\Pi & \Pi^2
\end{pmatrix}
\;=\;\frac{1}{\tau\,s'(u)}\,v\,v^\top,
\quad
v=(0,1,-\Pi).
\]

Properties:

- **Symmetric PSD:** \(M=v v^\top/(\tau s')\ge 0\).
- **Energy degeneracy:** \(M\,\delta\mathcal{I}=0\) because \(\delta\mathcal{I}/\delta q=( -\nabla^2\Phi+V'(\Phi),\,\Pi,\,1)\) and \(v^\top(\delta\mathcal{I}/\delta q)=\Pi-\Pi\cdot 1=0\).
- **Entropy Casimir of J:** \(J\,\delta\Sigma=0\) because \(\delta\Sigma/\delta q=(0,0,s'(u))\) has support only on \(u\), and \(J\) does not move \(u\).

### 2.3 Resulting evolution (and the reduced damped equation)

The metriplectic evolution gives:
\[
\dot{\Phi}=\Pi,
\]
\[
\dot{\Pi}=\nabla^2\Phi - V'(\Phi)\;-\;\frac{1}{\tau}\Pi,
\]
\[
\dot{u}=\frac{1}{\tau}\Pi^2.
\]

So the *reduced* observable equation for \(\Phi\) is the familiar damped Klein–Gordon/Allen–Cahn type:
\[
\ddot{\Phi}+\frac{1}{\tau}\dot{\Phi}-\nabla^2\Phi+V'(\Phi)=0,
\]
but now it is explicitly the projection of a fully metriplectic, energy‑conserving system.

Entropy production is manifest:
\[
\dot{\Sigma}=\int d^3x\; s'(u)\dot{u}=\int d^3x\;\frac{1}{\tau}\Pi^2\;\ge 0.
\]

**Scope note:** This proxy is not claimed to be “the universe’s fundamental Lagrangian.” It is a derived-limit closure that (i) respects A4 degeneracy and (ii) provides lattice-measurable diagnostics for CF11’s dark-sector bookkeeping.

---

## 3. What “J-sector” and “M-sector” mean in CF11

### 3.1 The central mistake to avoid

The metriplectic split is a split of the **generator of motion**:
\[
\dot{q}=\dot{q}_J+\dot{q}_M,
\quad
\dot{q}_J := J\,\delta \mathcal{I}/\delta q,
\quad
\dot{q}_M := M\,\delta \Sigma/\delta q.
\]

It is **not automatically** a global split of the **state** \(q\) into two orthogonal fields \(q=q_J+q_M\).

To obtain a state-level split, we need an additional **projection choice**. CF11 makes that choice explicit and testable.

### 3.2 Mode-projection definition (spectral split)

Let \(\bar{q}(t)\) be a coarse-grained cosmological background (e.g., spatial mean on a comoving scale \(\ell\)). Consider perturbations \(\delta q := q-\bar{q}\) and linearize:

\[
\partial_t(\delta q) = \mathcal{L}(t)\,\delta q + \mathcal{N}(\delta q),
\]

where \(\mathcal{L}\) is the linearized generator and \(\mathcal{N}\) collects nonlinear terms.

**Assumption (S-gap):** On the time window and scale of interest, \(\mathcal{L}\) has a spectral separation between:
- an **oscillatory / reversible band** (eigenvalues with \(|\Re\lambda|\ll|\Im\lambda|\)), and
- a **relaxational / irreversible band** (eigenvalues with \(\Re\lambda\le -\gamma<0\)).

Under (S-gap), define the Riesz projectors \(P_J\) and \(P_M\) onto these bands. Then
\[
\delta q = \delta q_J + \delta q_M,
\qquad
\delta q_J:=P_J\delta q,
\qquad
\delta q_M:=P_M\delta q,
\qquad
P_JP_M=0.
\]

This is the mathematically correct replacement for the ad hoc projectors in CF11 v1.0.

**T2 requirement:** (S-gap) is not philosophical. It is a numerical gate: compute \(\mathrm{spec}(\mathcal{L})\) on the lattice and verify separation.

### 3.3 Sector energies and “cross-terms”

For the proxy model in §2, the quadratic energy in perturbations around \(\bar{q}\) is
\[
\delta^2 \mathcal{I}[\delta q] \;=\; \tfrac12 \langle \delta q,\; H_{\mathcal{I}}(\bar{q})\,\delta q\rangle,
\]
where \(H_{\mathcal{I}}\) is the Hessian (second variation) of \(\mathcal{I}\) at \(\bar{q}\).

Define sector energies
\[
E_J := \tfrac12 \langle \delta q_J,\; H_{\mathcal{I}}\,\delta q_J\rangle,
\qquad
E_M := \tfrac12 \langle \delta q_M,\; H_{\mathcal{I}}\,\delta q_M\rangle.
\]

The “interaction remainder” at quadratic order is
\[
E_{\times} := \langle \delta q_J,\; H_{\mathcal{I}}\,\delta q_M\rangle.
\]

If we choose \(P_J,P_M\) to be orthogonal projectors with respect to the \(H_{\mathcal{I}}\)-inner product (standard in modal analysis), then \(E_{\times}=0\) **exactly at quadratic order**. Outside the quadratic regime, the remainder is controlled by nonlinearities \(\mathcal{N}(\delta q)=O(\|\delta q\|^2)\) and should be treated as a measurable error term, not waved away.

---

## 4. Effective stress-energy and two-fluid bookkeeping

### 4.1 Proxy stress-energy for a minimally coupled scalar

In an FRW background with scale factor \(a(t)\), a minimally coupled scalar has the standard effective energy density and pressure (spatially averaged, assuming isotropy):

\[
\rho[\Phi] = \tfrac12 \dot{\Phi}^2 + \tfrac{1}{2a^2}|\nabla\Phi|^2 + V(\Phi),
\]
\[
p[\Phi] = \tfrac12 \dot{\Phi}^2 - \tfrac{1}{6a^2}|\nabla\Phi|^2 - V(\Phi).
\]

CF11 uses these only as **derived-limit diagnostics**: on the lattice, you can compute the analogous discrete quantities and form \(w:=p/\rho\).

### 4.2 Sector densities and pressures

Define coarse-grained sector densities by inserting the sector fields reconstructed from \(\delta q_J,\delta q_M\) into the quadratic approximations of \(\rho\) and \(p\), and averaging over a comoving window:

\[
\rho_J := \langle \rho[\Phi_J]\rangle_\ell,\quad p_J := \langle p[\Phi_J]\rangle_\ell,
\]
\[
\rho_M := \langle \rho[\Phi_M]\rangle_\ell,\quad p_M := \langle p[\Phi_M]\rangle_\ell,
\]
with an explicit tracked remainder
\[
\rho_\times := \langle \rho[\Phi]-\rho[\Phi_J]-\rho[\Phi_M]\rangle_\ell,
\quad
p_\times := \langle p[\Phi]-p[\Phi_J]-p[\Phi_M]\rangle_\ell.
\]

The entire point: **\(\rho_\times,p_\times\)** are not assumed small; they are measured and gated.

---

## 5. Equations of state: controlled limits and correct bounds

### 5.1 J-sector: vacuum-like limit \(w_J\approx -1\)

Define
\[
K_J := \tfrac12 \langle \dot{\Phi}_J^2\rangle_\ell,\quad
G_J := \tfrac{1}{2a^2}\langle |\nabla\Phi_J|^2\rangle_\ell,\quad
U_J := \langle V(\Phi_J)\rangle_\ell,
\]
so \(\rho_J = K_J+G_J+U_J\) and \(p_J = K_J-\tfrac13 G_J-U_J\).

If \(G_J\ll U_J\) (nearly homogeneous) and \(K_J\ll U_J\) (slow drift), define
\[
\epsilon_J := \frac{K_J}{U_J},\qquad \delta_J := \frac{G_J}{U_J}.
\]

Then the EoS satisfies the exact identity
\[
w_J = \frac{\epsilon_J-\frac13\delta_J-1}{\epsilon_J+\delta_J+1}.
\]

In particular, if \(\epsilon_J\le \epsilon_{\max}\) and \(\delta_J\le\delta_{\max}\), then
\[
|1+w_J| \le \frac{2\epsilon_{\max}+\frac23\delta_{\max}}{1-\epsilon_{\max}-\delta_{\max}}
\quad \text{(for }\epsilon_{\max}+\delta_{\max}<1\text{)}.
\]

This is the correct, bounded statement. There is no need to assert an exact constant \(w_J=-1\) unless the measured \(\epsilon_J,\delta_J\) force it.

### 5.2 M-sector: dust-like limit \(w_M\approx 0\)

There are two distinct, testable routes to \(w_M\approx 0\). CF11 allows either (or both), and the lattice decides which regime VDM actually realizes.

#### Route A: non-relativistic defect/particle kinematics

If the M-sector coarse-grains to a gas of localized structures with RMS velocity dispersion \(\sigma_v\ll 1\), then
\[
w_M \approx \frac{\sigma_v^2}{3}.
\]
This is the standard dust limit: pressure is kinetic, suppressed by \(v^2\).

**Lattice proxy:** identify defect cores / interface segments (CF03), track their velocities, and estimate \(\sigma_v\).

#### Route B: rapid oscillation in a quadratic minimum

Near a stable minimum, any smooth potential is locally quadratic:
\[
V(\Phi)\approx \tfrac12 m^2(\Phi-\Phi_\star)^2.
\]

If the M-sector is dominated by coherent oscillations about \(\Phi_\star\) with frequency \(m\gg H\) and with small gradient energy (\(G_M\ll K_M+U_M\)), then time-averaging over oscillations yields
\[
\langle K_M\rangle \approx \langle U_M\rangle,
\qquad
\Rightarrow\qquad
\langle w_M\rangle \approx 0.
\]

This is the cleanest scalar-field route to CDM-like behavior and is the correct replacement for the inconsistent algebra in CF11 v1.0.

**Lattice proxy:** measure oscillation frequency and verify \(m/H\gg 1\), and check \(\langle K_M\rangle/\langle U_M\rangle\to 1\).

---

## 6. Energy exchange \(Q^\mu\): definition, constraints, and what must be measured

### 6.1 Definition (bookkeeping, not vibes)

Once a split \(T^{\mu\nu}=T_J^{\mu\nu}+T_M^{\mu\nu}+T_\times^{\mu\nu}\) is chosen (with \(T_\times\) tracked), define the exchange current

\[
Q^\nu := -\nabla_\mu T_J^{\mu\nu}.
\]

Then automatically
\[
\nabla_\mu(T_J^{\mu\nu}+T_M^{\mu\nu}) = -\nabla_\mu T_\times^{\mu\nu},
\]
so in the controlled regime where \(T_\times\) is negligible (measured gate), the effective two-fluid description is consistent:
\[
\nabla_\mu T_J^{\mu\nu} \approx -Q^\nu,\qquad
\nabla_\mu T_M^{\mu\nu} \approx +Q^\nu.
\]

### 6.2 Constraint from the entropy law

The axiom-core entropy law gives a strict sign constraint:
\[
\dot{\Sigma}=\Big\langle \frac{\delta\Sigma}{\delta q},\,M\,\frac{\delta\Sigma}{\delta q}\Big\rangle \ge 0.
\]

In the proxy model of §2, this implies kinetic damping is non-negative:
\[
\frac{d}{dt}\int \tfrac12\Pi^2\,d^3x \le 0
\quad \text{(up to reversible transfers).}
\]

Operationally: if you claim \(Q\neq 0\), you must show it is compatible with \(\dot{\Sigma}\ge 0\) under your sign conventions. CF11 treats this as a **numerical consistency gate**, not an assumption.

### 6.3 Coincidence is a closure problem (and that’s good)

A metriplectic system guarantees monotone relaxation of an appropriate Lyapunov functional, but it does **not** uniquely fix a cosmological \(Q(z)\) without a closure linking coarse-grained variables to \((J,M,\mathcal{I},\Sigma)\).

Therefore CF11 adopts the disciplined stance:

- The “coincidence attractor” becomes a **binary claim only after** a specific \(Q\)-closure is selected and pre-registered.
- The closure is then judged by AIC/BIC and out-of-sample prediction (see §9).

---

## 7. Causality and stability: what is actually guaranteed

### 7.1 Finite-speed propagation

From CF04, telegraph/Cattaneo transport implies a finite front speed \(c=\sqrt{D/\tau}\). From CF03, hierarchy can throttle this to \(c_{\mathrm{eff}}\le c_0\) via void debt (VDM‑E‑106).

**Gate:** in simulations, measured signal fronts must satisfy \(|x|\le c_{\mathrm{eff}} t\) within a declared tolerance.

### 7.2 Stability is conditional (tachyonic phases are allowed)

CF03 intentionally uses tachyonic/unstable regimes to generate interfaces (condensation). Therefore CF11 does **not** claim global linear stability.

Instead it asserts a conditional statement:

- In post-condensation regions where the local curvature \(V''(\Phi_\star)>0\), linearized perturbations of the proxy model are damped by \(\tau^{-1}\) and are stable.
- Instability when \(V''<0\) is a **feature** (interface formation), and must match CF03’s gates (Γ-convergence, perimeter scaling, etc.).

---

## 8. A8 hierarchy connection and lensing/void observables

The only safe way to connect hierarchy to cosmology is operational:

- CF03 predicts hierarchical interface formation and void-debt accumulation.
- CF03/CF04 predict this modulates transport speeds (\(c_{\mathrm{eff}}\)) and therefore any propagation-based observable (lensing, time delays, wavefront distortions).

### 8.1 A minimal observable definition: hierarchy lensing bias

Define a dimensionless statistic \(\beta_{\mathrm{bias}}\) as:

\[
\beta_{\mathrm{bias}} := \frac{\kappa_{\mathrm{obs}}-\kappa_{\mathrm{baseline}}}{\kappa_{\mathrm{baseline}}},
\]

where \(\kappa_{\mathrm{baseline}}\) is the lensing convergence predicted by the chosen baseline model (ΛCDM/NFW/etc) and \(\kappa_{\mathrm{obs}}\) is measured.

**VDM qualitative prediction:** \(\beta_{\mathrm{bias}}\neq 0\) correlated with hierarchical boundary indicators (void debt / interface density).  
**ΛCDM expectation:** \(\beta_{\mathrm{bias}}\) shows no such correlation after controlling for mass tracers.

CF11 does **not** hard-code \(\rho_M^{\mathrm{eff}}=\rho_M e^{+\beta D/D_0}\) because that requires a gravity closure not completed in CF11.

---

## 9. Falsification gates (binary, pre-registrable)

### 9.1 T2 internal gates (lattice / simulation)

**G-CF11-T2-1 (Degeneracy):**  
Verify \(J\,\delta\Sigma \approx 0\) and \(M\,\delta\mathcal{I}\approx 0\) with declared tolerance (e.g., \(10^{-12}\) relative).

**G-CF11-T2-2 (Entropy law):**  
\(\Delta\Sigma \ge -\varepsilon_\Sigma\) per step (with \(\varepsilon_\Sigma\) set by numerical precision).

**G-CF11-T2-3 (Spectral gap / mode split validity):**  
Compute \(\mathrm{spec}(\mathcal{L})\) and confirm a separation parameter \(\gamma>0\) exists over the time window.

**G-CF11-T2-4 (Cross-term control):**  
\(|\rho_\times|/(\rho_J+\rho_M) \le \varepsilon_\times\) after coarse-graining.

**G-CF11-T2-5 (EoS regimes):**  
Measure \(w_J,w_M\) and verify they fall in declared bands *only when the corresponding regime diagnostics hold* (e.g., \(\epsilon_J,\delta_J\ll 1\) for \(w_J\approx -1\); \(m/H\gg 1\) or \(\sigma_v\ll 1\) for \(w_M\approx 0\)).  
This avoids circular “w≈0 because we said so” reasoning.

**G-CF11-T2-6 (Causality):**  
Front speed \(v_{\mathrm{front}}\le c_{\mathrm{eff}}(1+\eta)\) with \(\eta\) declared (CF04 typical tolerance \(\sim 0.02\)).

### 9.2 T3+ observational gates (cosmology)

These gates deliberately mirror your existing falsification style: one number, pre-registered dataset.

**G-CF11-T3-1 (Hierarchy lensing bias):**  
\(\beta_{\mathrm{bias}}\) vs hierarchy indicator shows either  
- detection: \(\beta_{\mathrm{bias}}>5\sigma\), or  
- null: \(|\beta_{\mathrm{bias}}|<1\sigma\) (then the hierarchy→lensing channel in CF11 is falsified).

**G-CF11-T3-2 (Model selection):**  
On a declared probe set (e.g., BAO+SNe+CMB distance priors + lensing),  
\[
\Delta\mathrm{AIC} = \mathrm{AIC}_{\Lambda\mathrm{CDM}}-\mathrm{AIC}_{\mathrm{VDM/CF11}}
\]
must satisfy a pre-registered threshold (e.g., \(\Delta\mathrm{AIC}\le -2\) for “VDM preferred,” \(\Delta\mathrm{AIC}\ge +10\) for “VDM rejected”).

**G-CF11-T3-3 (Interacting-fluid coupling):**  
If a specific \(Q(z;\theta)\) closure is pre-registered, then either  
- \(\theta\) is detected with \(>3\sigma\) and consistent with \(\dot{\Sigma}\ge 0\), or  
- \(\theta\) consistent with zero at \(<1\sigma\) (falsifying that closure).

---

## 10. Implementation notes (how to do the split without inventing math)

### 10.1 Computing the spectral projectors on a lattice

At each checkpoint time \(t_i\):

1. Linearize the discretized update rule to obtain the Jacobian \(L_i\) approximating \(\mathcal{L}(t_i)\).
2. Compute a real Schur decomposition \(L_i = Q T Q^\top\).
3. Identify eigenvalues belonging to the oscillatory band vs relaxational band using a declared criterion (e.g., \(\Re\lambda\le -\gamma\)).
4. Build the projectors \(P_J,P_M\) from the Schur blocks (standard invariant subspace extraction).
5. Project \(\delta q\) to get \(\delta q_J,\delta q_M\), then compute \(\rho_J,\rho_M,w_J,w_M,\rho_\times\).

This is reproducible, numerically stable, and avoids ad hoc “operator algebra” with \(J,M\).

---

## 11. Canon integration (equations + symbols to register)

### 11.1 Proposed new equations (numbers provisional)

- **VDM‑E‑145 (Mode split via spectral projectors):**  
  \(\delta q = P_J\delta q + P_M\delta q\), \(P_JP_M=0\).

- **VDM‑E‑146 (Sector energies from Hessian):**  
  \(E_J=\tfrac12\langle \delta q_J, H_{\mathcal{I}}\delta q_J\rangle\), \(E_M=\tfrac12\langle \delta q_M, H_{\mathcal{I}}\delta q_M\rangle\).

- **VDM‑E‑147 (J-sector EoS identity):**  
  \(w_J = (\epsilon_J-\delta_J/3-1)/(\epsilon_J+\delta_J+1)\).

- **VDM‑E‑148 (Dust limits):**  
  \(w_M\approx \sigma_v^2/3\) (defects) and \(\langle w_M\rangle\approx 0\) (quadratic rapid oscillation).

- **VDM‑E‑149 (Exchange current definition):**  
  \(Q^\nu := -\nabla_\mu T_J^{\mu\nu}\).

### 11.2 Proposed new symbols

- \(P_J,P_M\): spectral projectors onto oscillatory vs relaxational bands  
- \(\gamma\): spectral gap / relaxational decay rate threshold  
- \(\ell\): coarse-graining scale  
- \(\rho_\times,p_\times\): tracked interaction remainders  
- \(\epsilon_J,\delta_J\): J-sector kinetic/gradient ratios  
- \(\sigma_v\): M-sector velocity dispersion proxy  
- \(\beta_{\mathrm{bias}}\): hierarchy-lensing bias statistic

---

## 12. Red-team checklist (updated)

1. **“This is just relabeling ΛCDM.”**  
   The split is not a label; it is a measurable decomposition of dynamics into reversible/irreversible channels plus a tracked remainder, with explicit gates.

2. **“Your split is arbitrary.”**  
   The only arbitrariness is the coarse-graining scale and the band cut; both are declared and then constrained by the spectral-gap gate and cross-term gate.

3. **“You’re assuming w≈0 and w≈−1.”**  
   No: CF11 provides *conditions* under which those limits follow, and requires lattice proxies (\(\epsilon_J,\delta_J,m/H,\sigma_v\)) to be satisfied before the EoS gates are applied.

4. **“Energy exchange violates conservation.”**  
   Total conservation holds at the axiom-core level; \(Q^\nu\) is internal bookkeeping defined after a split and must be consistent with \(\dot{\Sigma}\ge 0\).

---

## 13. Closure statement

CF11 (rewritten) reduces the “dark sector from metriplectic dynamics” idea to something you can actually kill:

- A **defined**, numerically implementable J/M **mode split** (not hand-wavy field splitting).  
- Correct, bounded EoS limits that become *binary* once regime diagnostics are met.  
- A8 hierarchy linkage expressed as a **measurable bias statistic**, without inventing density laws.  
- A tight set of T2/T3 gates that produce a contradiction report if they fail.

**Tier:** T1 complete (formalism + gates)  
**Next validation:** T2 lattice runs implementing the spectral split + remainders; then T3 observational regression.

---
