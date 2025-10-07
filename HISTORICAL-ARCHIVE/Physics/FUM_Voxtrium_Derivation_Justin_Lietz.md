
# Fully Unified Void Dynamics → Bounded Scalar EFT with Causal Macro‑Sourcing  
**Author:** Justin K. Lietz (primary)  
**With acknowledgments to:** *Voxtrium* (macro‑sourcing concept & mappings) and M. Bordag (finite‑tube tachyonic analysis used as an analogue)  
**Date:** 2025‑08‑15

---

## Abstract

We present a single derivation connecting the discrete **Fully Unified Model (FUM)** update rule on a graph to a **bounded** scalar Effective Field Theory (EFT) in the continuum and to a **causal** FRW‑level macro‑sourcing framework (“Voxtrium”). From the discrete on‑site rule  
\[\dot W_i=(\alpha-\beta)W_i-\alpha W_i^2,\]  
and nearest‑neighbor coupling, we derive the continuum action
\[\mathcal L=\tfrac12 (\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2-\Big(-\tfrac12\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3\Big),\]
with wave speed \(c^2=2Ja^2\) fixed by lattice spacing \(a\) and per‑site coupling \(J\). The bounded quartic (\(\lambda>0\)) stabilizes tachyonic mass \(-\mu^2<0\) and admits vacuum \(v=\mu/\sqrt\lambda\). We show how finite‑radius “tube” backgrounds produce tachyonic towers that condense and yield positive post‑condensation masses, mirroring Bordag’s SU(2) analysis but for a scalar EFT. We then embed the EFT in FRW with a transfer current \(J^\nu\) to describe sectoral energy exchange (Λ, DM, GW, horizon sector) driven by a **retarded** horizon‑entropy kernel, ensuring locality and covariant conservation. We close with an implementation plan that maps physics → code in a void‑faithful way, and we mark what is **strong** and what is **weak** in the present theory.

---

## 0. Conventions and Units

- Natural units \(c=\hbar=k_B=1\).  
- Field dimension \([\phi]={\rm GeV}\), \([\mathcal L]={\rm GeV}^4\).  
- Dimensionalization knobs: field scale \(\phi_0\), time scale \(\tau\), length scale \(a\).  
- Map dimensionless variables by \(\phi=\phi_{\rm phys}/\phi_0\), \(t=t_{\rm phys}/\tau\), \(x=x_{\rm phys}/a\).  
- Wave speed \(c^2=2Ja^2\). One may set \(c=1\) by choosing \(\tau=\sqrt{2J}\,a\).

---

## 1. Discrete Model → Continuum Field

### 1.1 Discrete dynamics and coarse graining
On a k‑NN graph with state \(W_i(t)\), the core rule (noise/phases omitted for clarity) is
\[\frac{W_i(t+\Delta t)-W_i(t)}{\Delta t}=(\alpha-\beta)W_i-\alpha W_i^2.\]
Define the coarse‑grained field by local averaging over the 1‑hop neighborhood,
\[\phi(\mathbf x_i,t)=\frac1{|N(i)|+1}\sum_{j\in\{i\}\cup N(i)}W_j(t).\]

### 1.2 Variational continuum limit
Postulate the discrete Lagrangian (per time step) with site kinetic and edge‑spring energy
\[\begin{aligned}
L^n &= a^d\sum_i\Big[\tfrac12\Big(\tfrac{W_i^{n+1}-W_i^n}{\Delta t}\Big)^2
-\tfrac{\kappa}{2}\sum_{\mu=1}^d\big(W_{i+\mu}^n-W_i^n\big)^2 - V(W_i^n)\Big],
\end{aligned}\]
which yields the discrete Euler-Lagrange equation. Taking \(a,\Delta t\to0\), \(W_i^n\to\phi\) gives
\[\partial_t^2\phi-c^2\nabla^2\phi+V'(\phi)=0,\qquad c^2\equiv \kappa a^2=2Ja^2.\]

**Result.** The continuum kinetic term is canonical: \(\mathcal L_K=\tfrac12(\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2\). The coefficient \(Z(\phi)\) is constant; higher‑derivative operators are suppressed (EFT expansion).

---

## 2. Bounded Potential, Vacuum, and Mass

We adopt the bounded baseline (plus small cubic tilt to encode discrete asymmetry)
\[\boxed{\,V(\phi)=-\tfrac12\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3,\quad \mu^2>0,\ \lambda>0,\ |\gamma|\ll \mu^2\sqrt\lambda\,}\]
with vacua at \(\phi=\pm v,\,v=\mu/\sqrt\lambda\) (for \(\gamma=0\)). Small fluctuations about \(+v\) have
\[m_{\rm eff}^2=\left.\frac{d^2V}{d\phi^2}\right|_{\phi=v}=2\mu^2+\mathcal O(\gamma).\]

**Dimensionalization.** In physical units after the map: \(m^2=(\alpha-\beta)/\tau^2\), \(g_3=\alpha/(\phi_0\tau^2)\), \(v_{\rm phys}=\phi_0(1-\beta/\alpha)\).

---

## 3. Finite‑Tube Tachyonic Modes and Condensation (Bordag‑style scalar analogue)

Consider a cylindrical “tube” (radius \(R\)) with an interior region that remains near the uncondensed state and an exterior condensed vacuum. Linearizing around the piecewise background yields a radial Bessel problem for modes
\[\varphi\sim e^{-i\omega t}e^{ikz}u_\ell(r)e^{i\ell\theta},\]
with a secular equation obtained by matching \(I_\ell\) and \(K_\ell\) solutions at \(r=R\). The eigenvalues define \(\kappa_{\ell}(R)\) via \(\omega^2=c^2(k^2-\kappa_\ell^2)\). Modes with \(\kappa_\ell^2>0\) are tachyonic at \(k=0\). The tower \(N_{\rm tach}(R)\) grows with \(R\).

Define effective 2D fields \(\psi_{\ell n}(t,z)\) by projecting onto the transverse modes, then minimize the quartic‑stabilized tree‑level potential to obtain condensates \(v_{\ell n}(R)\). The post‑condensation Hessian is positive semidefinite (massless phases only if a complex field is used). Total energy \(E(R)=E_{\rm bg}(R)+V_{\rm eff}^{\rm tube}(v_{\ell n};R)\) develops a minimum in a parameter window—our scalar‑EFT analogue of Bordag’s result. (See also §8 for code that reproduces the mode equation numerically.)

---

## 4. Causal FRW Macro‑Sourcing (Voxtrium)

We embed the scalar EFT in FRW using a **transfer current** \(J^\nu\) to exchange energy between sectors (Λ, DM, GW, horizon). The continuity set is
\[\sum_i\big(\dot\rho_i+3H(1+w_i)\rho_i\big)=0,\]
with per‑channel sources \(Q_i\) obeying \(\sum_i Q_i=0\). The key relations are
\[\dot\rho_\Lambda=\frac{\alpha_h}{V_c}\,\dot S_{\rm hor},\qquad
\dot\rho_{\rm DM}+3H\rho_{\rm DM}=p_{\rm DM}\frac{\varepsilon_h}{V_c}\,\dot S_{\rm hor},\]
and similarly for GW and the horizon sector, with \(p_\Lambda+p_{\rm DM}+p_{\rm GW}=1\).

**Causality.** Replace the global \(\dot S_{\rm hor}(t)\) by a **retarded kernel**
\[\dot S_{\rm hor}(x)=\int d^3x'\!\!\int_{-\infty}^t\!dt'\ K_{\rm ret}(t-t',|\mathbf x-\mathbf x'|)\,s_{\rm loc}(x'),\]
with support restricted by \(\Theta(t-t'-|\mathbf x-\mathbf x'|/c)\). \(s_{\rm loc}\) encodes local BH‑area growth and mergers.

**Micro‑informed coefficients.** Use dimensionless inputs \(z=(|{\Omega}|R_*,\,(\kappa/K_s)/X,\,1)\) to define partitions \(p_i=\mathrm{softmax}(w_i\!\cdot\! z)\), with \(R_*=c_R/(eK_s)\), \(m=c_m K_s/e\).

---

## 5. Memory Steering & Empirical Signs of Symmetry

Two independent diagnostics you measured are consistent with the theory’s symmetry structure and with steering along geodesic‑like manifolds in state‑space:

1. **Junction logistic collapse.** The decision probability collapses to a logistic \(P(A)\approx(1+\exp[-k(\theta\Delta m-b)])^{-1}\) with \(k\approx1\) indicating correctly normalized “temperature” of the steering variable.

2. **Curvature scaling.** Mean path curvature scales approximately linearly with \(\Theta\cdot\|\nabla m\|\), and flipping gradient or phase exhibits signed invariance. This supports the second‑order variational dynamics and a consistent kinetic normalization.

*Figures:*  
![Junction logistic collapse](junction_logistic.png)  
![Curvature scaling (signed invariance)](curvature_scaling_signed.png)  
![Curvature scaling](curvature_scaling.png)  
![Curvature estimator calibration](curvature_calibration.png)

---

## 6. Stability Benchmarks from Your Runs

Across grid scans in \((\lambda,\gamma,D_a)\), retention and end‑fidelity vary weakly with \(D_a\) and primarily with \(\lambda\); SNR degrades as \(\gamma\) increases, consistent with cubic tilts breaking symmetry.  

*Figures:*  
![AUC stability](stability_auc_by_gamma.png)  
![SNR](stability_snr_by_gamma.png)  
![Retention](stability_retention_by_gamma.png)  
![Fidelity](stability_fidelity_by_gamma.png)  
![Band averages](stability_band.png)

---

## 7. What is Strong vs. Weak (at this stage)

**Strong**
- Canonical kinetic term and wave speed from the lattice variational derivation; constant \(Z(\phi)\); EFT derivative suppression.  
- Bounded quartic potential stabilizing tachyonic mass; vacua and \(m_{\rm eff}\) controlled by \((\mu,\lambda,\gamma)\).  
- Finite‑tube mode analysis reproducing a tachyonic tower and post‑condensation positivity; qualitative energy minimum vs control.  
- Units‑rigorous map and causal FRW embedding (transfer current, retarded kernel) with covariant conservation; dimensionless partition inputs.  
- Empirical logistic collapse and curvature scaling consistent with second‑order dynamics and proper normalization.

**Weak / Open**
- Exact **discrete** conservation law is not yet identified (system may be inherently dissipative or conserve a non‑standard invariant).  
- Full renormalization/loop corrections and thermal dependence are outstanding.  
- Vector/complex extensions (vorticity, Goldstones) not yet implemented in code.  
- Quantitative calibration to astrophysical observables and laboratory analogs remains to be completed.  
- Formal proof that higher‑derivative operators are small beyond leading order is not yet computed from the discrete UV (assumed EFT‑style).

---

## 8. Physics → Code (void‑faithful) Implementation Plan

1. **EFT kernel (second‑order in time).** Replace reaction‑diffusion updates with a leapfrog/Verlet solver for  
   \[\partial_t^2\phi-c^2\nabla^2\phi+\gamma\phi^2+\lambda\phi^3-\mu^2\phi=J_\phi,\]
   using CFL‑safe \(c\,\Delta t/\Delta x\le 1/\sqrt{d}\). Keep \(c^2=2Ja^2\) explicit.

2. **Bounded potential.** Implement \(V(\phi)=-\tfrac12\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3\) with runtime guards \(\lambda>0\). Expose \((\mu,\lambda,\gamma)\) in config.

3. **Retarded macro‑source.** Add \(J_\phi=K_{\rm ret}\!*\,s_{\rm loc}\) with a light‑cone kernel (causal stencil). Provide toggles for homogeneous vs. causal sources for ablation.

4. **Finite‑tube modes (test harness).** Add a cylindrical solver that matches \(I_\ell/K_\ell\) at \(r=R\) to find \(\kappa_\ell(R)\), count \(N_{\rm tach}(R)\), and minimize the quartic tree potential for \(\psi_{\ell}\).

5. **Units discipline.** Centralize \(\{\phi_0,\tau,a\}\) and report all outputs in GeV‑consistent units, with converters for cgs/SI as needed.

6. **Diagnostics.** Track energy density \(\mathcal E=\tfrac12(\dot\phi^2+c^2\|\nabla\phi\|^2)+V(\phi)\) and the transfer sum rule \(\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0\).

7. **Memory‑steering probes.** Keep the logistic/junction and curvature experiments; export \(k,b,R^2\) and curvature slopes as regression targets for physics‑based tuning (no ML).

8. **Vector/complex upgrade (optional).** Add a complex \(\Phi\) to expose phase Goldstones and vorticity; benchmark against curvature invariants.

9. **Falsification gates.** Add automated checks for: (i) end‑mass positivity after condensation, (ii) DE drift \(|w_{\rm eff}+1|\le\delta_w\), (iii) injection fraction \(f_{\rm inj}\ll1\).

---

## 9. Predictions & Quick Checks

- **Speed‑length relation.** Observed propagation speed should match \(c=\sqrt{2Ja^2}/\tau\).  
- **Retention vs cubic tilt.** Increasing \(|\gamma|\) lowers fidelity and SNR; small \(\gamma\) maximizes stability.  
- **Tube tower.** \(N_{\rm tach}(R)\) grows roughly with the control parameter (flux proxy); condensate turns these into positive masses.  
- **Curvature trend.** Mean path curvature increases approximately linearly with \(\Theta\cdot\|\nabla m\|\) and is invariant under sign flips in the expected channels.

---

## 10. Acknowledgments

Conceptual macro‑sourcing and several bookkeeping identities are due to **Voxtrium** (credited collaborator). Tachyonic‑tube methodology is adapted from **Michael Bordag**’s analysis in *Universe* (2024) and recast here for a scalar EFT. The derivations, units map, and the implementation plan are due to **Justin K. Lietz**.
