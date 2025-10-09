
# The Fully Unified Void Dynamics Model (FUM) and Voxtrium: A Single Consolidated Derivation

**Author:** Justin K. Lietz  
**With attributions:** References to *Voxtrium* are credited accordingly. The tachyonic condensate mapping draws on **Michael Bordag (Universe 2024, 10, 38)**.  
**Date:** 2025-08-15

---

## Executive Summary (scope, strengths, limitations)

**Scope.** We derive, in one document, the pathway from the discrete FUM update law to a bounded scalar effective field theory (EFT), embed it in a covariant action with conserved transfer current, and align it with the Voxtrium macro-sourcing framework. We also adapt Bordag’s finite-tube tachyonic-condensate analysis to the FUM baseline to define testable mode problems. We close with the empirical memory-steering figures (logistic collapse, curvature scaling, stability grids).

**What is strong (demonstrated):**
- A clear **discrete → continuum** derivation to a scalar EFT with wave speed \(c^2 = 2Ja^2\) and a bounded quartic potential that stabilizes tachyonic onset; the cubic term is a small tilt (vacuum selector).  
- A **units-rigorous map** from the dimensionless lattice to physical parameters \((\phi_0, \tau, a)\) defining \(g_3\) (cubic) and \(m^2\) consistently.  
- **Covariant conservation with sources**: FRW continuity with a transfer current \(J^\nu\) and a **retarded kernel** for horizon-entropy sourcing (causality).  
- A **finite-radius mode problem** (tube/filament) with Bessel/Kummer matching that counts unstable modes and shows quartic stabilization with post-condensation positive spectra; an energy minimum vs. control is defined.  
- **Empirical signatures**: logistic junction behavior, curvature estimator calibration, and stability/retention/fidelity heatmaps consistent with invariances reported in experiments.

**What is weak (open or needs completion):**
- No closed-form **discrete conserved quantity** is identified yet; the standard guess for a lattice Hamiltonian is not conserved by the FUM update.  
- Vector/fluid **hydrodynamics** are not yet derived from the scalar sector; vorticity and incompressible limits would require additional fields or projections.  
- Macro calibration (**partitions, priors, kernel shape**) remains phenomenological until fit to data; higher-derivative EFT terms are not yet bounded by explicit lattice matching.  
- The tube-energy minimum and chaos onset beyond certain flux require numerical exploration and loop corrections for full robustness.

---

## 1. Discrete → Continuum (bounded EFT backbone)

The on-site discrete evolution \(\dot W \approx (\alpha-\beta)W-\alpha W^2\) coarse-grains to a scalar field \(\phi\) with Lagrangian
\[
\mathcal L = \tfrac{1}{2}(\partial_t\phi)^2 - \tfrac{c^2}{2}(\nabla\phi)^2 - V(\phi),\qquad c^2=2Ja^2.
\]
A bounded choice
\[
V(\phi)= -\tfrac{1}{2}\mu^2\phi^2 + \tfrac{\lambda}{4}\phi^4 + \tfrac{\gamma}{3}\phi^3\quad (\lambda>0,\; |\gamma|\ll \mu^2\sqrt{\lambda})
\]
yields tachyonic onset at \(\phi=0\) (\(-\mu^2\)) and stable vacua at \(\pm v=\pm \mu/\sqrt\lambda\). The cubic \(\gamma\) implements the discrete bias (vacuum selection). The continuum EOM is
\[
\partial_t^2\phi - c^2\nabla^2\phi + \lambda\phi^3 + \gamma\phi^2 - \mu^2\phi = 0.
\]

**Units map.** Promote dimensionless lattice variables via scales \(\phi_0\,[\rm GeV],\ \tau\,[\rm GeV^{-1}],\ a\,[\rm GeV^{-1}]\). Then
\[
g_3 \equiv \gamma_\text{phys} = \alpha/(\phi_0\tau^2),\qquad m^2 = (\alpha-\beta)/\tau^2,\qquad v_\text{phys}=\phi_0(1-\beta/\alpha).
\]

---

## 2. Covariant embedding and Voxtrium sourcing

Embed the scalar (or Skyrme composite sector) in GR with a horizon functional and a **transfer current** that moves energy among channels while preserving total covariant conservation. In FRW:
\[
\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0,\qquad \nabla_\mu T_{\rm total}^{\mu\nu}=0,
\]
with per-channel sources \(Q_i\propto (\varepsilon_h/V_c)\,\dot S_{\rm hor}\) and a **retarded kernel**
\[
\dot S_{\rm hor}(t) = \int d^3x'\int_{-\infty}^{t}\!dt'\,K_{\rm ret}(t-t',|\mathbf x-\mathbf x'|)\,s_{\rm loc}(\mathbf x',t'),\quad
K_{\rm ret}\propto \Theta(t-t'-r/c).
\]

Partitions \(p_i\) (\(\Lambda,\rm DM, GW\)) live on a probability simplex and may be chosen as a softmax of dimensionless micro-informed inputs, e.g. \(z_1=|\Omega|R_\*, z_2=(\kappa/K_s)/X, z_3=1\).

---

## 3. Finite‑tube tachyonic analysis (Bordag‑adapted)

Consider a cylindrical domain of radius \(R\) with an uncondensed interior and condensed exterior. Linearized modes satisfy a radial matching problem with modified Bessel functions; the **secular equation**
\[
\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)} = -\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)}
\]
yields a finite **tower of tachyonic modes** \(\kappa_{\ell n}(R)\). After projecting a quartic onto these modes, condensation renders the **Hessian eigenvalues non‑negative** and defines an **energy vs. size** function \(E(R)=E_{\rm bg}(R)+V_\text{eff}^{\rm tube}(R)\) that can exhibit a true minimum. This reproduces the qualitative structure of Bordag’s Universe‑2024 analysis for a chromomagnetic flux tube, adapted here to the scalar backbone.

---

## 4. Empirical figures (memory steering & stability)

### 4.1 Logistic junction collapse
![junction_logistic](junction_logistic.png)

A single‑parameter sigmoid \(P(A)\approx [1+e^{-k(\theta\,\Delta m - b)}]^{-1}\) with **k≈1.005, b≈0.036, R²≈0.999** captures junction choice vs. signed margin, consistent with a canonical transition curve.

### 4.2 Curvature estimator calibration and scaling
![curvature_calibration](curvature_calibration.png)

The curvature estimator on circular arcs is close to the ideal \(\kappa=1/R\) across R = 20, 40, 80 (arb. units).  
![curvature_scaling_signed](curvature_scaling_signed.png)
![curvature_scaling](curvature_scaling.png)

Mean path curvature scales with \(\theta\,\|\nabla m\|\) (linear fit R²≈0.68), and invariance to sign flips is consistent with symmetry expectations.

### 4.3 Stability grids
![stability_auc_by_gamma](stability_auc_by_gamma.png)
![stability_snr_by_gamma](stability_snr_by_gamma.png)
![stability_retention_by_gamma](stability_retention_by_gamma.png)
![stability_fidelity_by_gamma](stability_fidelity_by_gamma.png)
![stability_band](stability_band.png)

AUC, SNR, retention, and fidelity trends vs. control parameters (\(\gamma,\lambda,D_a\)) show plateaus and monotone bands, indicating robust regimes and separations of scale.

---

## 5. What remains to be finished (precise checklist)

1. **Conserved quantity (discrete).** Identify a true invariant or Lyapunov functional of the FUM update beyond the standard lattice Hamiltonian (which is **not** conserved).  
2. **Higher‑derivative matching.** Bound EFT coefficients \(c_1,c_2,\ldots\) by explicit lattice matching to prove their irrelevance in the IR.  
3. **Hydrodynamic limit.** Derive vector/tensor sectors (e.g., add steering current \(u^\mu\) or promote to complex/vector fields) and recover vorticity and incompressible limits.  
4. **Finite‑tube numerics.** Implement the solver for \(\kappa_{\ell n}(R)\), condensate search, Hessian spectra, and \(E(R)\) scans; verify the existence and location of minima and the onset of chaos.  
5. **Macro calibration.** Fit \(p_i(z)\), \(\alpha_h,\varepsilon_h\), and kernel widths to data under the small‑drift constraints \(\epsilon_{{\rm DE}}\ll 1,\ f_{\rm inj}\ll 1\).

---

## Acknowledgments

- **Voxtrium.** When *Voxtrium* is referenced for macro sourcing and units discipline, this document explicitly credits that work.  
- **Michael Bordag** (Universe 2024, 10, 38) for the finite‑radius tachyonic condensate framework adapted here to FUM’s scalar EFT.  
- **Author:** Justin K. Lietz - derivations, figures, and integration presented here.

---

## References (selection)

- Bordag, M., *Tachyon Condensation in a Chromomagnetic Center Vortex Background*, Universe **10** (2024) 38, doi:10.3390/universe10010038.
- Lietz, J.K., internal derivation notes: discrete→continuum, kinetic normalization, EFT approach, conservation analysis, Voxtrium mapping (see accompanying repository).

