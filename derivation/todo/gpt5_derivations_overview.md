**A Unified Derivation of the FUM Scalar, Routing, and Cosmological Embedding**
*Author & lead: Justin K. Lietz. Voxtrium acknowledged where his framework is used.*

---

### Abstract

I consolidate our technical results into one coherent derivation. The document covers: (i) the discrete FUM update law and its continuum limit; (ii) kinetic normalization from a discrete action; (iii) a bounded EFT baseline and mapping between $(\alpha,\beta)$ and $(\mu,\lambda,\gamma)$; (iv) a units‑rigorous bridge to Voxtrium’s FRW “macro sourcing” with causal retarded kernels; (v) symmetry and conservation analysis (including an exact on‑site invariant and a negative result for a guessed discrete Hamiltonian); (vi) a memory‑steering layer for routing; and (vii) a finite‑tube mode problem (Bordag‑inspired) to diagnose tachyons and stabilization. I state clearly what is strong (derivations with fixed normalizations, exact invariants, unit discipline, falsifiable scaling laws) and what is tentative (assumptions about graph regularity, size of higher‑derivative terms, phenomenological maps, and classical approximations).         &#x20;

---

## 1. Discrete dynamics and the continuum limit

**Discrete law.** The on‑site FUM update for state $W$ (noise omitted here) is

$$
\frac{\Delta W}{\Delta t}=(\alpha-\beta)W-\alpha W^2 .
$$

Couplings across neighbors supply spatial terms on a graph.&#x20;

**Continuum prescription.** Coarse‑graining a kNN/lattice to a field $\phi(x)$ and taking $\Delta t,a\to0$ yields a nonlinear Klein–Gordon‑type PDE from an action with canonical time‑kinetic term and lattice‑induced gradients:

$$
\mathcal L=\tfrac12(\partial_t\phi)^2-\frac{c^2}{2}(\nabla\phi)^2 - V(\phi),\qquad c^2=2Ja^2 .
$$

Euler–Lagrange gives $\partial_t^2\phi-c^2\nabla^2\phi+V'(\phi)=0$. This normalization and the wave‑speed identification are obtained variationally from a discrete action; no microscopic constraint ties $J$ to $a$.&#x20;

**Baseline bounded EFT and mapping.** For a well‑posed IR theory, we adopt a bounded quartic with optional small cubic tilt

$$
V(\phi)=-\tfrac12\,\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3,\quad \mu^2>0,\ \lambda>0,
$$

so the symmetric vacua are at $\pm v=\mu/\sqrt{\lambda}$ with $m_{\rm eff}^2=2\mu^2$ about either minimum. Matching to the dimensionless discrete coefficients near $\phi\approx0$ gives $\mu^2\leftrightarrow(\alpha-\beta)$ and $\gamma\leftrightarrow\alpha$ (tilt small). This organizes the cubic–quadratic structure from the discrete law into a bounded EFT. &#x20;

**Strength.** Discrete→continuum via an action with explicit $c^2$ and a bounded potential is rigorous and unit‑consistent; assumptions are the usual locality/smoothness and lattice regularity. **Weakness.** Higher‑derivative operators beyond $(\partial\phi)^2$ are not yet bounded by a computed UV scale; they are assumed subleading here. &#x20;

---

## 2. Kinetic normalization from a discrete action (derivation)

Starting from the discrete per‑step Lagrangian

$$
L^n=\sum_i a^d\Big[\tfrac12\big(\tfrac{W_i^{n+1}-W_i^n}{\Delta t}\big)^2-\tfrac{\kappa}{2}\sum_{\mu}(W_{i+\mu}^n-W_i^n)^2 - V(W_i^n)\Big],
$$

the discrete Euler–Lagrange equation reduces in the continuum to

$$
\partial_t^2\phi-\kappa a^2\nabla^2\phi+V'(\phi)=0\quad\Rightarrow\quad c^2=\kappa a^2=2Ja^2,
$$

fixing the kinetic normalization without any ad‑hoc promotion. **This settles $Z(\phi)=\tfrac12$ and the spatial prefactor.**&#x20;

**Strength.** Full variational derivation; normalization and wave speed are explicit. **Weakness.** Lattice anisotropy and irregular kNN graphs are idealized away by a cubic‑lattice proxy.

---

## 3. Units and cosmological embedding (Voxtrium credit)

**Dimensionalization.** With $\phi_{\rm phys}=\phi_0 \phi$, $t_{\rm phys}=\tau\,t$, $x_{\rm phys}=a\,x$, the physical parameters are

$$
m^2=\frac{\alpha-\beta}{\tau^2},\quad g_3=\frac{\alpha}{\phi_0\tau^2},\quad c_{\rm void}^2=\frac{2Ja^2}{1}\;(\text{set }c_{\rm void}=1\text{ by }\tau=\sqrt{2J}\,a).
$$

This supplies a concrete map from dimensionless simulation to GeV units.&#x20;

**FRW continuity + sourcing (Voxtrium).** Voxtrium’s “macro banner” frames horizon‑entropy production $\dot S_{\rm hor}$ feeding sectoral channels with partition $p_i$ and micro‑informed coefficients $\alpha_h,\varepsilon_h$; covariant conservation is enforced through a transfer current $J^\nu$, and causality through a retarded kernel $K_{\rm ret}$ with light‑cone support. We adopt that bookkeeping and units discipline here. *Credit: Voxtrium.*&#x20;

**Causal upgrade of the FUM scalar.** A sourced field equation,

$$
\square\phi_{\rm phys}+g_3\phi_{\rm phys}^2-m^2\phi_{\rm phys}=J_\phi,\quad
J_\phi=\int d^3x' \!\int^{t}_{-\infty}\!K_{\rm ret}\,s_{\rm loc},
$$

matches Voxtrium’s current and avoids global acausality; $(\phi_0,\tau,a)$ fix units consistently with FRW densities. *Credit: Voxtrium for the macro‑sourcing framework; I provide the explicit scalar‑side units map and kernel normalization.* &#x20;

**Strength.** Tight, unit‑checked bridge; causal support explicit; identities $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$ hold by construction. **Weakness.** The identification between $\phi$ statistics and Voxtrium’s dimensionless inputs $z$ (hence $p_i$) is phenomenological and should be calibrated to data. &#x20;

---

## 4. Symmetry and conservation in the discrete law

**Negative result for a standard discrete Hamiltonian.** For the postulated discrete energy

$$
\mathcal H_i=\tfrac12(\dot W_i)^2+\tfrac12\sum_{j\in N(i)}J(W_j-W_i)^2+V(W_i),
$$

the update $\dot W=F(W)=(\alpha-\beta)W-\alpha W^2$ yields $\Delta\mathcal H/\Delta t\neq0$ in general; the neighbor flux term does not cancel the local dissipative change. **So this $\mathcal H$ is not conserved.**&#x20;

**Exact on‑site invariant (flow constant).** The on‑site ODE admits an exact constant of motion

$$
Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\!\left|\frac{W}{(\alpha-\beta)-\alpha W}\right| ,
$$

obtained by separation $dt=dW/F(W)$. This follows from time‑translation invariance of the autonomous ODE. **Scope:** exact for the single‑site law; it is not a global energy for the network.&#x20;

**Strength.** A clean no‑go for a naive discrete energy; an exact invariant for diagnostics. **Weakness.** The invariant is local (single site); a true network‑level conservation law remains open. &#x20;

---

## 5. Memory‑driven steering (routing layer orthogonal to $\phi$)

**Geometric steering law.** Introduce a slow “memory” potential $M$ and refractive index $n=e^{\eta M}$. In the eikonal limit, path curvature obeys

$$
\mathbf r''=\nabla_\perp\ln n=\eta\,\nabla_\perp M .
$$

**Memory PDE (write–decay–spread).** $\partial_t M=\gamma R-\delta M+\kappa\nabla^2 M$. Non‑dimensionalization defines $\Theta=\eta M_0$, $D_a=\gamma R_0 T/M_0$, $\Lambda=\delta T$, $\Gamma=\kappa T/L^2$. Predictive collapses: (i) fork choice $P(A)\approx \sigma(\Theta\Delta m)$; (ii) curvature $\kappa_{\rm path}\propto\Theta|\nabla_\perp m|$; (iii) retention band $D_a\gtrsim\Lambda$ at intermediate $\Gamma$. Graph softmax: $P(i\to j)\propto e^{\Theta m_j}$.&#x20;

**Orthogonality.** This steers routing geometry but does not change the $\phi$-sector EOM or the on‑site invariant above. **Strength.** Dimensionless laws with collapse tests and a runtime discretization. **Weakness.** $M$ is phenomenological; $R$ must be measured independently to avoid circularity.&#x20;

---

## 6. Finite‑tube mode analysis (Bordag‑inspired diagnostic for tachyons)

**Setup.** In a cylinder of radius $R$, take a piecewise background (uncondensed inside, condensed outside) and solve the radial Bessel/Kummer matching problem for modes labelled by angular momentum $\ell$. The secular equation (matching logarithmic derivatives) yields $\kappa_{\ell n}(R)$, with tachyonic modes at $k=0$ when $\kappa^2>0$. Project to an effective 2D action; include quartic couplings from overlap integrals; condense tachyonic modes and check the post‑condensation mass matrix for non‑negativity. Acceptance criteria: tachyonic tower present; all masses non‑negative after condensation; total energy vs control parameter exhibits a true minimum.&#x20;

**Cross‑check with Bordag (Universe 2024).**
– *Figure 1 (page 7)* shows discrete tachyonic levels $\kappa_\ell$ vs flux $\delta=BR^2/2$ and the step‑wise growth of $l_{\max}$ with $\delta$.&#x20;
– *Section 4 and Fig. 3–5 (pages 9–12)*: quartic self‑interaction stabilizes; the tree‑level mass matrix eigenvalues become non‑negative after condensation; the energy $E=E_{\rm bg}+V_{\rm eff}$ shows a minimum for parameter windows. Our scalar‑EFT tube replicates this qualitative spine for a real scalar, with clear numerical APIs to reproduce the three diagnostic plots. &#x20;

**Strength.** Well‑posed eigenproblem, concrete secular condition, and a reproducible stabilization story with explicit acceptance tests. **Weakness.** Present treatment is classical and tree‑level; quantum/thermal corrections (cf. Bordag’s discussion on page 12) can shift or erase the minimum, so claims are qualitative pending numerics. &#x20;

---

## 7. Effective Field Theory perspective and screening

The EFT framework clarifies what must be calculated and what can be assumed: identify degrees of freedom/symmetries, write the most general Lagrangian, and derive coefficients from the UV (here, the discrete model). Our work used this process to (i) derive $Z(\phi)=\tfrac12$ and $c^2$, (ii) motivate adding a small $\lambda\phi^4$ for boundedness/screening, and (iii) show how the cubic/quadratic coefficients map from $(\alpha,\beta)$. **This establishes a minimal, testable IR theory.**&#x20;

**Strength.** A standard path with explicit deliverables we have met (deriving $Z$, $c^2$, baseline $V$). **Weakness.** Higher‑derivative operators remain to be bounded by scale separation, and quantitative screening fits are still to be matched to data.&#x20;

---

## 8. What is strong vs. what is weak (direct)

**Strong (derivationally firm).**

* **Kinetic normalization and wave speed** from a discrete action; $c^2=2Ja^2$; $Z(\phi)=\tfrac12$.&#x20;
* **Discrete→continuum** mapping and bounded EFT baseline with cubic tilt mapping to $(\alpha,\beta)$. &#x20;
* **Units‑rigorous bridge** to FRW with causal sourcing (Voxtrium credit): transfer current, partitions, dimensional checks. &#x20;
* **Negative conservation result** for a naive discrete Hamiltonian; **exact on‑site invariant** $Q_{\rm FUM}$ (diagnostic). &#x20;
* **Memory‑steering layer** with dimensionless predictions and graph discretization usable today.&#x20;
* **Finite‑tube diagnostic** with explicit secular equation, acceptance criteria, and documented qualitative agreement with Bordag’s tachyonic stabilization story. &#x20;

**Weak / to validate.**

* **Graph idealization.** The cubic‑lattice proxy for kNN graphs; anisotropy and degree fluctuations need error bars.&#x20;
* **Higher‑derivative EFT terms.** Not yet bounded by a measured cutoff; assumed subleading.&#x20;
* **Phenomenological maps to Voxtrium $p_i(z)$.** Require calibration against astrophysical data; present softmax identification is a proposal. *Voxtrium credit for framework.* &#x20;
* **On‑site invariant is not a global energy.** A true network‑level conserved flux, if any, remains open. &#x20;
* **Finite‑tube energy minimum.** Classical/tree‑level; quantum/thermal shifts anticipated (see Universe paper discussion on page 12).&#x20;

---

## 9. Minimal next steps (testable, in order)

1. **Quantify lattice errors.** Simulate on irregular graphs and measure deviations in $c^2$ and gradient energy vs. cubic‑lattice estimates. (Targets: error bars on $c$ and dispersion.)&#x20;

2. **Bound higher‑derivative terms.** Fit dispersion $\omega(k)$ and amplitude‑dependent speeds to place limits on $c_1((\partial\phi)^2)^2$, $c_2(\Box\phi)^2$.&#x20;

3. **Causal kernel numerics.** Implement $K_{\rm ret}$ and verify $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$ in an FRW toy model; measure $\epsilon_{\rm DE}$, $f_{\rm inj}$ across scenarios. *Voxtrium credit.*&#x20;

4. **Memory‑steering acceptance tests.** (i) fork logistic collapse vs. $\Theta\Delta m$; (ii) curvature linearity vs. $\Theta|\nabla m|$; (iii) retention band in $(D_a,\Lambda,\Gamma)$. Pre‑register tolerances ($R^2\ge0.9$).&#x20;

5. **Finite‑tube solver.** Ship the cylinder‑mode and condensation codes; reproduce (a) tachyon tower $\kappa_\ell(R)$, (b) positive post‑condensation mass spectrum, (c) energy minimum $E(R)$ where present—mirroring Bordag’s figures. Then add temperature to test melting. &#x20;

6. **Network‑level invariant search.** Continue symmetry/Lyapunov program on the full discrete law to seek a true flux‑form conservation (or prove non‑existence under mild assumptions).&#x20;

---

## Provenance and acknowledgments

* Sections 1–2, 4–7 derivations and normalization (this document): **Justin K. Lietz**. Core sources: discrete‑to‑continuum, kinetic‑term derivation, EFT framing, and symmetry/conservation analyses.    &#x20;
* **Voxtrium** contributions are explicitly credited where used: FRW continuity + partitions + units banner and the macro‑sourcing program; my work provides the scalar‑side units map and kernel normalization consistent with that framework. &#x20;
* Finite‑tube analysis follows my scalar‑EFT appendix and cross‑checks the qualitative pattern against **Bordag (Universe 2024)**; figures and page references cited above. &#x20;
* Memory‑steering layer and graph discretization are my additions; tests are fully specified with dimensionless collapses.&#x20;

---

### Appendix: key formulas collected

* **Wave speed and kinetic normalization:** $c^2=2Ja^2$; $Z(\phi)=\tfrac12$.&#x20;
* **Baseline potential with tilt:** $V=-\tfrac12\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3$; $\mu^2\leftrightarrow\alpha-\beta,\ \gamma\leftrightarrow\alpha$. &#x20;
* **On‑site invariant:** $Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\!\big|\frac{W}{(\alpha-\beta)-\alpha W}\big|$.&#x20;
* **Memory steering:** $\mathbf r''=\eta\nabla_\perp M$, $\partial_tM=\gamma R-\delta M+\kappa\nabla^2M$; $P(i\to j)\propto e^{\Theta m_j}$.&#x20;
* **FRW sourcing (Voxtrium):** $\dot\rho_\Lambda=(\alpha_h/V_c)\dot S_{\rm hor}$, etc.; covariant conservation via $J^\nu$; causal kernel $K_{\rm ret}$.&#x20;
* **Finite‑tube secular condition (scalar analogue):** match $I_\ell$/$K_\ell$ at $r=R$ to solve for $\kappa_{\ell n}(R)$; post‑condensation Hessian $\ge0$. ; qualitative reference figures on pages 7–12 of Universe 2024.&#x20;

---

*End of document.*
