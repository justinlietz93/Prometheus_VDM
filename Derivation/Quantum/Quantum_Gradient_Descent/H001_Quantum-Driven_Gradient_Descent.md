# H001 — Quantum‑Driven Gradient Descent (QGD)

**Classification:** Axiom‑core  
**Author:** Justin K. Lietz  
**Date:** 2025-11-06  
**Status:** HYPOTHESIS  
**One‑line objective:** A fast, coherent **J** limb accelerates/regularizes a slow **M** descent by reorienting the local geometry without violating metriplectic degeneracies.  

**Formal statement**
Let $( \partial_t q = J(q),\delta\mathcal I/\delta q + M(q)$,\delta\Sigma/\delta q ) with (J^\top=-J), (M^\top=M\ge0), (J,\delta\Sigma=0), (M,\delta\mathcal I=0). In a window with timescale ratio (\varepsilon=\tau_J/\tau_M\ll1), the coarse‑grained descent time to (\epsilon)-optimality, (T_\epsilon), satisfies
( S \equiv T_\epsilon^{(M)}/T_\epsilon^{(J+M)} > 1 ) and increases monotonically as (\varepsilon\downarrow) and curvature anisotropy (\chi=\lambda_{\max}/\lambda_{\min}\uparrow).

## **Predictions (decisive metrics)**

* **P1 (Isotropization):** Median (S(\varepsilon,\chi) > 1.5) on anisotropic bowls and Rosenbrock at fixed compute budget; echo‑verified J window.
* **P2 (Resonant saddle crossing):** In double‑well tests, crossing probability (p_{\text{cross}}(\omega_J)) has a peak with location within 30% of (\sqrt{|\lambda_{\text{saddle}}|}) and ≥3σ prominence.
* **P3 (Degeneracies):** Numerical checks of ( \langle J,\delta\Sigma,\delta\Sigma\rangle \approx 0) and ( \langle M,\delta\mathcal I,\delta\mathcal I\rangle \approx 0) throughout runs.

**Rationale**
Acceleration as *geometry + reorientation*: continuous‑time Bregman‑Lagrangian flows explain families of accelerated methods and their time‑dilation property (relevant to your “fast J, slow M” separation). These flows include damping and do **not** imply J is pure momentum; they justify that adding a reversible‑like component can reduce effective conditioning when properly coupled. 

**Preconditions & scope**
Small‑amplitude J window with echo fidelity scaling properly; finite‑speed locality; stationary noise.

## **Experiment plan**

* **E1 (Isotropization sweep):** Quadratic bowls with target (\chi\in{3,10,30}), sweep (\varepsilon). **Gates:** S‑curve monotone in (\chi) and (1/\varepsilon); echo scaling with integrator order.
* **E2 (Saddle resonance):** Double‑well; sweep (\omega_J), measure (p_{\text{cross}}). **Gate:** unimodal peak near (\sqrt{|\lambda_{\text{saddle}}|}).
* **E3 (Degeneracies):** Log inner‑product residuals for J/M degeneracies; **Gate:** all below threshold.

**Risks & kill‑methods**
Hidden coupling makes J inject entropy → fail if H‑theorem breaks. Acausal updates → cone audit fail triggers CONTRADICTION_REPORT.

**Links**
S*: (to be added) | T0_*: `T0_qgd_isotropization/`, `T0_qgd_saddle/` | Results: `results/qgd/*.json`
