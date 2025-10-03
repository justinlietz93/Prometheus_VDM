# VDM Canonical Equations & Procedural Math (Auto-compiled)
*Defining equations and procedural math currently present in this repository.*

- Source of truth: extracted from repository files; do not edit equations here without updating their sources.
- MathJax only: use `$...$` and `$$...$$`; no numbering/tags/environments not supported by GitHub.
- Labels: entries are headed by `VDM-E-###` (header anchors); no equation tags inside MathJax.

---

#### VDM-E-001 — Agency/Consciousness Field Evolution
**Context:** derivation/AGENCY_FIELD.md:38-39 • Commit: 6885588

$$
\partial_t C(x,t) = D\,\nabla^2 C(x,t) - \gamma\, C(x,t) + S(x,t)
$$

**Notes:** Core field equation for agency/consciousness order parameter; $C$ spreads via diffusion $D$, decays at rate $\gamma$, driven by source $S$ from organized information processing.

---

#### VDM-E-002 — Agency Field Composite Source
**Context:** derivation/AGENCY_FIELD.md:47-48 • Commit: 6885588

$$
S(x,t) = \sigma(x)\,\big[\kappa_1 P(x,t)+\kappa_2 I_{\text{net}}(x,t)+\kappa_3 U(x,t)\big] \times g(V)\,h(B)
$$

**Notes:** Source combines predictive power $P$, integration $I_{\text{net}}$, control efficacy $U$, gated by option capacity $V$ and balance $B$; scaled by substrate susceptibility $\sigma$.

---

#### VDM-E-003 — Agency Field Steady State
**Context:** derivation/AGENCY_FIELD.md:62-64 • Commit: 6885588

$$
C_{\text{ss}}=\frac{S_0}{\gamma},\qquad
C(t)=C_{\text{ss}}+\big(C(0)-C_{\text{ss}}\big)e^{-\gamma t}
$$

**Notes:** For uniform source $S_0$, field settles to $C_{\text{ss}}=S_0/\gamma$ and relaxes exponentially with decay time $1/\gamma$.

---

#### VDM-E-004 — Agency Field Causal Solution
**Context:** derivation/AGENCY_FIELD.md:72 • Commit: 6885588

$$
C(x,t)=\iint G_{\text{ret}}(x{-}x',t{-}t')\,S(x',t')\,dx'\,dt'
$$

**Notes:** Retarded Green's function $G_{\text{ret}}$ ensures causality; no superluminal influence ($G_{\text{ret}}=0$ for $t'<t$).

---

#### VDM-E-005 — Agency Field Regional Budget
**Context:** derivation/AGENCY_FIELD.md:81-85 • Commit: 6885588

$$
\frac{dQ_C}{dt}
=\int_{\partial\Omega} D\,\nabla C\cdot n\,dA
-\gamma \int_{\Omega} C\,dV
+\int_{\Omega} S\,dV
$$

**Notes:** Change in regional charge $Q_C$ equals boundary flux minus decay plus sources; flux/decay/source accounting.

---

#### VDM-E-006 — Agency Field Discrete Update
**Context:** derivation/AGENCY_FIELD.md:93-94 • Commit: 6885588

$$
C_i^{n+1} = C_i^{n}+\Delta t\Big(D\,\Delta_{xx} C_i^{n}-\gamma\,C_i^{n}+S_i^{n}\Big)
$$

**Notes:** Explicit Euler discretization; requires CFL condition $\Delta t \lesssim \Delta x^2/(2dD)$ for stability.

---

#### VDM-E-007 — Agency Field Dimensionless Form
**Context:** derivation/AGENCY_FIELD.md:102-105 • Commit: 6885588

$$
\partial_{\tilde t} C = \nabla_{\tilde x}^2 C - C + \tilde S(\tilde x,\tilde t)
$$

with $\tilde t=\gamma t$, $\tilde x=x/\ell_D$, $\ell_D=\sqrt{D/\gamma}$

**Notes:** Dimensionless rescaling by decay time and diffusion length for cross-system comparison.

---

#### VDM-E-008 — Agency Field Portal Modulation (Optional)
**Context:** derivation/AGENCY_FIELD.md:113 • Commit: 6885588

$$
\varepsilon_{\text{eff}}(x,t)=\varepsilon_0\big(1+\alpha\,C(x,t)\big),\quad |\alpha|\ll 1
$$

**Notes:** Optional dark-sector portal coupling; portal signal leans toward high-$C$ regions without becoming new force.

---

#### VDM-E-009 — Control Efficacy
**Context:** derivation/AGENCY_FIELD.md:53-54 • Commit: 6885588

$$
U =\frac{\mathbb{E}[L_{\text{no-control}}] - \mathbb{E}[L_{\text{control}}]}{\text{energy used}}
$$

**Notes:** Control efficacy: error reduction per unit energy; used in agency field source term.

---

#### VDM-E-010 — VDM C-Score
**Context:** derivation/AGENCY_FIELD.md:122 • Commit: 6885588

$$
C_\tau = \big[\mathrm{z}(P_\tau/J)+\mathrm{z}(U_\tau)+\mathrm{z}(V_\tau)\big]\times B
$$

**Notes:** Comparative score over horizon $\tau$: z-scores of prediction per joule, control efficacy, option capacity, multiplied by balance.

---

#### VDM-E-011 — Discrete Action (Axiom 4)
**Context:** agent-onboarding/axiomatic_theory_development.md:38-39 • Commit: 6885588

$$
S(W)= \sum_{n} \Delta t \sum_{i} a^{d} \left( \frac{1}{2} (\Delta_t W_i)^2 - \frac{J}{2}\sum_{j\in N(i)}(W_j-W_i)^2 - V(W_i) \right), \quad J>0
$$

**Notes:** Fundamental discrete action for FUVDM; kinetic + interaction + potential terms on cubic lattice with spacing $a$.

---

#### VDM-E-012 — Potential and Derivatives (Axiom 3)
**Context:** agent-onboarding/axiomatic_theory_development.md:35 • Commit: 6885588

$$
V'(\phi)=\alpha\phi^{2}-r\phi+\lambda\phi^{3},\quad V''(\phi)=2\alpha\phi-r+3\lambda\phi^{2},\quad V'''(\phi)=2\alpha+6\lambda\phi
$$

with potential $V(\phi)=\tfrac{\alpha}{3}\phi^{3}-\tfrac{r}{2}\phi^{2}+\tfrac{\lambda}{4}\phi^{4}$, $r=\alpha-\beta$, $\lambda\ge0$

**Notes:** Admissible potential class with quartic stabilization; single authoritative definition of derivatives.

---

#### VDM-E-013 — Discrete Euler-Lagrange Equation
**Context:** agent-onboarding/axiomatic_theory_development.md:48 • Commit: 6885588

$$
\frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{\Delta t^{2}} = 2J \sum_{j\in N(i)}(W_j^{n}-W_i^{n}) - V'(W_i^{n})
$$

**Notes:** Second-order discrete field equation from variational principle; naturally arises without "promotion" from first-order.

---

#### VDM-E-014 — Continuum Klein-Gordon Form (EFT/KG Branch)
**Context:** agent-onboarding/axiomatic_theory_development.md:51 • Commit: 6885588

$$
\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0, \qquad c^{2}=2J a^{2}
$$

**Notes:** Continuum limit of discrete action; inertial/EFT branch marked [EFT-KG]; $c^2=2Ja^2$ from exact Taylor expansion.

---

#### VDM-E-015 — Reaction-Diffusion Gradient Flow
**Context:** agent-onboarding/axiomatic_theory_development.md:56-57 • Commit: 6885588

$$
\partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}, \quad D=2J a^{2}
$$

**Notes:** Overdamped/gradient-flow limit under time-scale separation; RD canonical form.

---

#### VDM-E-016 — RD Lyapunov Functional
**Context:** agent-onboarding/axiomatic_theory_development.md:58-60 • Commit: 6885588

$$
\mathcal{L}[\phi]=\int_{\Omega}\left( \tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)\,dx,\qquad \hat V'(\phi)=-f(\phi)
$$

with time derivative $\frac{d}{dt}\mathcal{L}[\phi] = -\int_{\Omega} (\partial_t\phi)^2\,dx \le0$

**Notes:** Energy dissipation functional for RD; monotone decreasing under periodic or no-flux BCs.

---

#### VDM-E-017 — Linear RD Dispersion
**Context:** agent-onboarding/axiomatic_theory_development.md:155 • Commit: 6885588

$$
\sigma(k)=r-Dk^{2}
$$

**Notes:** Growth rate of Fourier mode $e^{ikx}$ linearized at $\phi=0$; Theorem U1.

---

#### VDM-E-018 — KPP Front Speed
**Context:** agent-onboarding/axiomatic_theory_development.md:163 • Commit: 6885588

$$
c_{front}=2\sqrt{D r}
$$

**Notes:** Pulled front speed for Fisher-KPP equation under monostable conditions; Theorem U2. Numeric validation: rel-err ≈ 4.7%, R²≈0.999996.

---

#### VDM-E-019 — Stationary Point Solutions
**Context:** agent-onboarding/axiomatic_theory_development.md:207 • Commit: 6885588

$$
\phi_{\pm}=\frac{-\alpha \pm \sqrt{\alpha^{2}+4\lambda r}}{2\lambda}
$$

when $\lambda>0$ and $V'(\phi)=0$

**Notes:** Vacuum solutions from potential calculus; $\phi=0$ or roots of $\lambda \phi^{2}+\alpha\phi-r=0$.

---

#### VDM-E-020 — Spatial Taylor Remainder Bound
**Context:** agent-onboarding/axiomatic_theory_development.md:126-127 • Commit: 6885588

$$
\|\Delta_a\phi-\nabla^{2}\phi\|_{\infty} \le C_{spatial}\, a^{2}\, \|\nabla^{4}\phi\|_{\infty},\qquad C_{spatial}=\frac{d}{12}
$$

**Notes:** Lemma S.1; controls error in replacing discrete Laplacian with continuum operator; $d$ is dimension.

---

#### VDM-E-021 — Temporal Taylor Remainder Bound
**Context:** agent-onboarding/axiomatic_theory_development.md:133 • Commit: 6885588

$$
\|\delta_{tt}\phi-\partial_{tt}\phi\|_{\infty} \le C_{time}\, \Delta t^{2}\, \|\partial_{t}^{4}\phi\|_{\infty},\qquad C_{time}=\frac{1}{12}
$$

**Notes:** Lemma T.1; controls error in replacing discrete second time difference with continuum operator.

---

#### VDM-E-022 — Dimensionless RD Scaling
**Context:** agent-onboarding/axiomatic_theory_development.md:422-427 • Commit: 6885588

$$
t' = r t,\quad x' = x\sqrt{r/D},\quad \phi = \phi_{*}\, y
$$

yields $\partial_{t'} y = \nabla_{x'}^{2} y + y - y^{2} - \Lambda\, y^{3}$

with $\Lambda=\lambda r/u^{2}$ (when $u>0$), $\phi_{*}=r/u$ or $\sqrt{r/\lambda}$

**Notes:** Dimensionless collapse for RD PDE; front speed becomes $\hat c = 2$, dispersion $\hat\sigma(k')=1-k'^{2}$.

---

#### VDM-E-023 — Discrete Flux Conservation
**Context:** agent-onboarding/axiomatic_theory_development.md:102-106 • Commit: 6885588

$$
F_{ij}=-\frac{D}{a}\,(\phi_j-\phi_i),\qquad F_{ij}=-F_{ji}
$$

with update $\phi_i^{n+1}=\phi_i^{n}-\frac{\Delta t}{a}\sum_{j\in N(i)}F_{ij}$

**Notes:** Lemma F.1; antisymmetric edge fluxes conserve total mass $\sum_i \phi_i$ with periodic or Neumann BCs when $f\equiv 0$.

---

#### VDM-E-024 — Asynchronous Census Hazard and Clock
**Context:** agent-onboarding/axiomatic_theory_development.md:513-515 • Commit: 6885588

$$
h_i := \big| D\,\Delta_a \phi_i + f(\phi_i) \big|,\qquad c_i^{n+1} \leftarrow c_i^{n} + h_i\,\Delta t
$$

**Notes:** Local hazard for event-driven sparse updates; site $i$ fires when $c_i \ge 1$ with micro-step $\delta t_i = \theta / h_i$ for quantum $\theta\in(0,1]$.

---

#### VDM-E-025 — Exact Logistic Reaction Step
**Context:** agent-onboarding/axiomatic_theory_development.md:519-521 • Commit: 6885588

$$
W^{+}=\frac{r\,W\,e^{r\delta t}}{u\,W\,(e^{r\delta t}-1)+r}
$$

for $dW/dt = r\,W - u\,W^{2}$

**Notes:** Closed-form exact solution for on-site reaction over time $\delta t$; used in census engine. Also in derivation/code/rd/reaction_exact.py:7.

---

#### VDM-E-026 — Discrete Gradient Lyapunov Step
**Context:** agent-onboarding/axiomatic_theory_development.md:110-112 • Commit: 6885588

$$
\mathcal{L}^{n+1}-\mathcal{L}^{n} = -\Delta t\,\left\|\frac{\phi^{n+1}-\phi^{n}}{\Delta t}\right\|_{2}^{2}\le 0
$$

with $\frac{\phi^{n+1}-\phi^{n}}{\Delta t} = D\nabla^{2}_h \bar\phi + \bar f$, $\hat V'(\bar\phi)=-\bar f$

**Notes:** Lemma DG.1; discrete-gradient update preserves energy monotonicity.

---

#### VDM-E-027 — RD On-Site (Discrete)
**Context:** derivation/FUVDM_Overview.md:23-24 • Commit: 6885588

$$
\frac{d W_i}{dt} = (\alpha - \beta)\, W_i - \alpha \, W_i^{2} + J \sum_{j\in \mathrm{nbr}(i)} (W_j - W_i)
$$

**Notes:** Discrete on-site dynamics near homogeneous state; canonical RD branch [PROVEN].

---

#### VDM-E-028 — RD Continuum PDE
**Context:** derivation/FUVDM_Overview.md:31 • Commit: 6885588

$$
\partial_t \phi = D\, \nabla^{2}\phi + r\, \phi - u\, \phi^{2} \quad \bigl[ -\lambda\, \phi^{3} \text{ (optional stabilization)} \bigr]
$$

**Notes:** Continuum reaction-diffusion equation; $\lambda\phi^3$ term optional for stabilization.

---

#### VDM-E-029 — RD Discrete-to-Continuum Mapping
**Context:** derivation/FUVDM_Overview.md:39-43 • Commit: 6885588

$$
\begin{aligned}
D &= J a^{2} && \text{(site Laplacian)}\\
D &= \tfrac{J}{z} a^{2} && \text{(neighbor-average form)}\\
r &= \alpha - \beta,\quad u = \alpha
\end{aligned}
$$

**Notes:** Exact parameter mapping from discrete to continuum; $z$ is coordination number.

---

#### VDM-E-030 — EFT Kinetic Normalization (Quarantined)
**Context:** derivation/FUVDM_Overview.md:52-54 • Commit: 6885588

$$
c^{2} = 2 J a^{2} \quad \text{(per-site)}, \qquad c^{2} = \kappa a^{2},\; \kappa = 2J \quad \text{(per-edge)}
$$

**Notes:** EFT/KG branch [PLAUSIBLE]; quarantined as future work; distinct from RD diffusion coefficient $D$.

---

#### VDM-E-031 — EFT Second-Order Field Equation (Quarantined)
**Context:** derivation/FUVDM_Overview.md:60-62 • Commit: 6885588

$$
\square \phi + V'(\phi) = 0, \qquad \square = \partial_t^{2} - c^{2} \nabla^{2}
$$

**Notes:** Klein-Gordon form; EFT branch [PLAUSIBLE].

---

#### VDM-E-032 — EFT Effective Mass (Quarantined)
**Context:** derivation/FUVDM_Overview.md:68-70 • Commit: 6885588

$$
m_{\mathrm{eff}}^{2} = V''(v)
$$

**Notes:** Effective mass parameter-dependent on vacuum $v$; EFT branch.

---

#### VDM-E-033 — RD Front Speed (Validated)
**Context:** derivation/FUVDM_Overview.md:110 • Commit: 6885588

$$
c_{\text{front}} = 2\sqrt{D r}
$$

**Notes:** Fisher-KPP pulled front speed [PROVEN]; validated with rel_err ≈ 0.047, R² ≈ 0.999996. See derivation/reaction_diffusion/rd_front_speed_validation.md.

---

#### VDM-E-034 — RD Discrete Dispersion
**Context:** derivation/FUVDM_Overview.md:122-124 • Commit: 6885588

$$
\sigma_d(m) = r - \frac{4D}{\Delta x^{2}} \sin^{2}\!\left(\frac{\pi m}{N}\right)
$$

**Notes:** Discrete dispersion for periodic domain mode $m$; continuum limit gives $\sigma(k) = r - D k^{2}$ with $k = 2\pi m/L$.

---

#### VDM-E-035 — RD Continuum Dispersion (Validated)
**Context:** derivation/FUVDM_Overview.md:128-130 • Commit: 6885588

$$
\sigma(k) = r - D k^{2}, \qquad k = \frac{2\pi m}{L}
$$

**Notes:** Linearized growth rate about $\phi \approx 0$ [PROVEN]; median rel. error ≈ 1.45×10⁻³, R² ≈ 0.99995. See derivation/reaction_diffusion/rd_dispersion_validation.md.

---

#### VDM-E-036 — RD Homogeneous Fixed Point
**Context:** derivation/FUVDM_Overview.md:150-152 • Commit: 6885588

$$
\phi^{\star} = \frac{r}{u} = 1 - \frac{\beta}{\alpha} \qquad (r = \alpha - \beta,\; u = \alpha)
$$

**Notes:** Stable fixed point for $r>0$; $\phi=0$ is dynamically unstable.

---

#### VDM-E-037 — Axiomatic Effective Mass Squared
**Context:** derivation/axiomatic_theory_development.md:428 • Commit: 6885588

$$
V_{\text{eff}}(\eta) = \frac{1}{2}m_{\text{eff}}^2 \eta^2 + \frac{g_3}{3!}\eta^3 + \frac{g_4}{4!}\eta^4 + \ldots
$$

where $m_{\text{eff}}^2 = V''(v_\lambda) > 0$ ensures stability

**Notes:** Effective potential around vacuum for symmetry breaking analysis; Phase III.1.

---

#### VDM-E-038 — Discrete Euler-Lagrange Variation
**Context:** derivation/axiomatic_theory_development.md:257 • Commit: 6885588

$$
\frac{\delta S}{\delta W_i^n} = \Delta t \cdot a^d \left[ \frac{\partial \mathcal{L}_i^n}{\partial W_i^n} + \frac{\partial \mathcal{L}_i^{n-1}}{\partial W_i^n} + \sum_{j \in N(i)} \frac{\partial \mathcal{L}_j^n}{\partial W_i^n} \right]
$$

**Notes:** Variational derivative of action with respect to field at site $i$, time $n$; includes self, past, and neighbor contributions.

---

#### VDM-E-039 — Discrete Field Equation Terms
**Context:** derivation/axiomatic_theory_development.md:260-264 • Commit: 6885588

From $\mathcal{L}_i^n$:
$$\frac{\partial \mathcal{L}_i^n}{\partial W_i^n} = -\frac{1}{\Delta t^2}(W_i^{n+1} - W_i^n) + J \sum_{j \in N(i)}(W_j^n - W_i^n) - V'(W_i^n)$$

From $\mathcal{L}_i^{n-1}$:
$$\frac{\partial \mathcal{L}_i^{n-1}}{\partial W_i^n} = \frac{1}{\Delta t^2}(W_i^n - W_i^{n-1})$$

**Notes:** Individual term-by-term contributions to discrete Euler-Lagrange equation.

---

#### VDM-E-040 — Taylor Expansion for Spatial Interaction
**Context:** derivation/axiomatic_theory_development.md:292-295 • Commit: 6885588

$$
(W_{i+\mu} - W_i)^2 + (W_{i-\mu} - W_i)^2 = 2a^2 \left(\frac{\partial \phi}{\partial x_\mu}\right)^2 + O(a^4)
$$

summing over directions $\mu$ gives $\sum_{j \in N(i)}(W_j - W_i)^2 = 2a^2 |\nabla \phi|^2 + O(a^4)$

**Notes:** Exact derivation of spatial kinetic prefactor $c_{\text{lat}} = 2$ for 3D cubic lattice (Derivation 1.3.1).

---

#### VDM-E-041 — Lorentz Invariance Condition
**Context:** derivation/axiomatic_theory_development.md:306-309 • Commit: 6885588

$$
c^2 = J a^2 = 2Ja^2
$$

**Notes:** Exact spatial kinetic prefactor for Lorentz-invariant continuum action; resolves "exact derivation" gap.

---

#### VDM-E-042 — Continuum Action
**Context:** derivation/axiomatic_theory_development.md:341 • Commit: 6885588

$$
S_{\text{continuum}} = \int dt \int d^d x \left[ \frac{1}{2}\left(\frac{\partial \phi}{\partial t}\right)^2 - \frac{c^2}{2}|\nabla \phi|^2 - V(\phi) \right]
$$

**Notes:** Continuum limit of discrete action; standard scalar field theory form.

---

#### VDM-E-043 — Klein-Gordon with Nonlinear Potential
**Context:** derivation/axiomatic_theory_development.md:352 • Commit: 6885588

$$
\frac{\partial^2 \phi}{\partial t^2} - c^2 \nabla^2 \phi + V'(\phi) = 0
$$

**Notes:** Continuum field equation from Euler-Lagrange; second-order hyperbolic PDE.

---

#### VDM-E-044 — RD Overdamped Limit
**Context:** derivation/axiomatic_theory_development.md:357-361 • Commit: 6885588

$$
\frac{\partial \phi}{\partial t} \approx \frac{c^2}{\gamma} \nabla^2 \phi - \frac{1}{\gamma} V'(\phi)
$$

with diffusion coefficient $D = c^2/\gamma = 2Ja^2/\gamma$ and reaction term $f(\phi) = -V'(\phi)/\gamma$

**Notes:** Overdamped regime where $\frac{\partial^2 \phi}{\partial t^2} \ll c^2 \nabla^2 \phi$; $\gamma$ is damping coefficient.

---

#### VDM-E-045 — Energy Density
**Context:** derivation/axiomatic_theory_development.md:386-387 • Commit: 6885588

$$
\rho_i^n = \frac{1}{2}\left(\frac{W_i^{n+1} - W_i^n}{\Delta t}\right)^2 + \frac{J}{2}\sum_{j \in N(i)}(W_j^n - W_i^n)^2 + V(W_i^n)
$$

**Notes:** Noether current from time translation invariance; kinetic + interaction + potential energy.

---

#### VDM-E-046 — Momentum Density (Discrete)
**Context:** derivation/axiomatic_theory_development.md:400-401 • Commit: 6885588

$$
\mathbf{p}_i^n = -\frac{J a^{d-1}}{2} \sum_{j \in N(i)} (W_j^n - W_i^n) \hat{\mathbf{n}}_{ij} \frac{W_i^{n+1} - W_i^n}{\Delta t}
$$

**Notes:** Noether current from spatial translation invariance; $\hat{\mathbf{n}}_{ij}$ is unit vector from site $i$ to $j$.

---

#### VDM-E-047 — Continuum Energy Density (Hamiltonian)
**Context:** derivation/axiomatic_theory_development.md:433 • Commit: 6885588

$$
\mathcal{H}(\phi, \dot{\phi}, \nabla\phi) = \frac{1}{2}\dot{\phi}^2 + \frac{c^2}{2}|\nabla\phi|^2 + V(\phi)
$$

**Notes:** Continuum energy density; conserved under time translation symmetry.

---

#### VDM-E-048 — Energy Flux (Poynting Vector)
**Context:** derivation/axiomatic_theory_development.md:437-442 • Commit: 6885588

$$
\mathbf{S} = -c^2 \dot{\phi} \nabla\phi
$$

with conservation law $\frac{\partial \mathcal{H}}{\partial t} + \nabla \cdot \mathbf{S} = 0$

**Notes:** Energy flux for scalar field; verified using Klein-Gordon equation.

---

#### VDM-E-049 — Stress-Energy Tensor
**Context:** derivation/axiomatic_theory_development.md:455-462 • Commit: 6885588

$$
T^{\mu\nu} = \partial^\mu \phi \partial^\nu \phi - g^{\mu\nu} \mathcal{L}
$$

with components $T^{00} = \mathcal{H}$, $T^{0i} = \dot{\phi} \partial_i \phi$, $T^{ij} = \partial_i \phi \partial_j \phi - \delta_{ij}[\frac{c^2}{2}|\nabla\phi|^2 + V(\phi)]$

**Notes:** Complete stress-energy tensor framework; $\partial_\mu T^{\mu\nu} = 0$ ensures conservation.

---

#### VDM-E-050 — RD Parameter Mapping
**Context:** derivation/axiomatic_theory_development.md:515-521 • Commit: 6885588

Diffusion coefficient: $D = \frac{c^2}{\gamma} = \frac{2Ja^2}{\gamma}$

Reaction term: $f(\phi) = -\frac{V'(\phi)}{\gamma} = \frac{1}{\gamma}\left[(\alpha-\beta)\phi - \alpha\phi^2 - \lambda\phi^3\right]$

Parameter mapping: $r = \frac{\alpha-\beta}{\gamma}$, $u = \frac{\alpha}{\gamma}$, $\kappa = \frac{\lambda}{\gamma}$

**Notes:** Exact correspondence between discrete lattice and continuum RD parameters (Phase IV.1).

---

#### VDM-E-051 — Lyapunov Functional for RD
**Context:** derivation/axiomatic_theory_development.md:578-579 • Commit: 6885588

$$
\mathcal{V}[\phi] = \int_\Omega \left[ \frac{D}{2}|\nabla\phi|^2 + \hat{V}(\phi) \right] dx
$$

where $\hat{V}(\phi) = \int_0^\phi f(\xi) d\xi$

**Notes:** Energy functional for RD system; $\frac{d\mathcal{V}}{dt} = -\int_\Omega (\frac{\partial \phi}{\partial t})^2 dx \leq 0$ ensures stability.

---

#### VDM-E-052 — RD Front Speed Theoretical Prediction
**Context:** derivation/axiomatic_theory_development.md:646 • Commit: 6885588

$$
c_{\text{front}} = 2\sqrt{Dr} = 2\sqrt{\frac{2Ja^2(\alpha-\beta)}{\gamma^2}} = \frac{2a\sqrt{2J(\alpha-\beta)}}{\gamma}
$$

**Notes:** Theoretical front speed from parameter mapping; agrees with computational validation within 5% error.

---

#### VDM-E-053 — Fixed Point Consistency Check
**Context:** derivation/axiomatic_theory_development.md:653-654 • Commit: 6885588

$$
\frac{r}{u} = \frac{(\alpha-\beta)/\gamma}{\alpha/\gamma} = \frac{\alpha-\beta}{\alpha} = 1 - \frac{\beta}{\alpha}
$$

**Notes:** Exactly matches theoretical vacuum solution in small-$\lambda$ limit.

---

#### VDM-E-054 — Void Scale Characteristic Length
**Context:** derivation/axiomatic_theory_development.md:679 • Commit: 6885588

$$
R_* = \frac{\pi a}{\sqrt{2J(\alpha-\beta)}} \approx 8.1 \text{ (lattice units)}
$$

**Notes:** Characteristic void scale from theory; matches computational domain sizes used in validations.

---

#### VDM-E-055 — Tachyon Condensation Mode Spectrum
**Context:** derivation/axiomatic_theory_development.md:690-693 • Commit: 6885588

$$
\omega_n^2 = c^2 k_n^2 - (\alpha-\beta) < 0
$$

for $k_n = n\pi/R$ with $n < n_{\max} = \frac{R}{\pi}\sqrt{\frac{\alpha-\beta}{c^2}}$

**Notes:** Unstable modes in finite-tube analysis; drives tachyon condensation mechanism.

---

#### VDM-E-056 — Tube Radius Selection
**Context:** derivation/axiomatic_theory_development.md:695 • Commit: 6885588

$$
R_* \sim \frac{\pi c}{\sqrt{\alpha-\beta}} = \frac{\pi\sqrt{2Ja^2}}{\sqrt{\alpha-\beta}}
$$

**Notes:** Natural scale for void structures; emerges from tachyon condensation analysis.

---

#### VDM-E-057 — Post-Condensation Mass
**Context:** derivation/axiomatic_theory_development.md:698 • Commit: 6885588

$$
m_{\text{eff}}^2 = V''(v_\lambda) = 2\alpha v_\lambda - (\alpha-\beta) + 3\lambda v_\lambda^2 > 0
$$

**Notes:** Positive mass-squared spectrum after condensation to vacuum $v_\lambda$.

---

#### VDM-E-058 — Stabilized Potential
**Context:** derivation/axiomatic_theory_development.md:1119 • Commit: 6885588

$$
V_{\text{stabilized}}(\phi) = \frac{\alpha}{3}\phi^3 - \frac{\alpha-\beta}{2}\phi^2 + \frac{\lambda}{4}\phi^4
$$

**Notes:** Quartic stabilization term ensures $V(\phi) \to +\infty$ as $|\phi| \to \infty$ when $\lambda > 0$.

---

#### VDM-E-059 — Stabilized Vacuum Solution
**Context:** derivation/axiomatic_theory_development.md:1132 • Commit: 6885588

$$
v_{\lambda} = \frac{-\alpha + \sqrt{\alpha^2 + 4\lambda(\alpha-\beta)}}{2\lambda}
$$

**Notes:** Physical vacuum for $\phi > 0$ when $\alpha > \beta$; $small\text{–}\lambda$ expansion: $v_{\lambda} \approx \frac{\alpha-\beta}{\alpha} - \frac{\lambda(\alpha-\beta)^2}{2\alpha^3} + O(\lambda^2)$.

---

#### VDM-E-060 — Effective Mass at Stabilized Vacuum
**Context:** derivation/axiomatic_theory_development.md:1138-1141 • Commit: 6885588

$$
m_{\text{eff}}^2 = V''(v_{\lambda}) = 2\alpha v_{\lambda} - (\alpha-\beta) + 3\lambda v_{\lambda}^2 \approx (\alpha-\beta) + O(\lambda)
$$

**Notes:** Effective mass for small $\lambda$ perturbative regime.

---

#### VDM-E-061 — VDM Morphology/Assimilation Field (Fluids)
**Context:** derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:12 • Commit: 6885588

$$
\partial_t s = \nabla\!\cdot\!\big(D_s\,M(s,\mathcal{D})\,\nabla s\big) + F(s;\text{valence},\text{resonance})
$$

**Notes:** RD-type evolution for substrate/connectome morphing variable $s(x,t)$; diffusion modulated by $M(s,\mathcal{D})$.

---

#### VDM-E-062 — VDM Signal/Transport Field (Fluids)
**Context:** derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:17 • Commit: 6885588

$$
\tau_u\,\partial_{tt}u + \partial_t u = c^2\nabla^2 u - \frac{\partial V}{\partial u}(u,s)
$$

**Notes:** Telegraph/damped Klein-Gordon for excitations/flux $u(x,t)$; finite-speed propagation.

---

#### VDM-E-063 — VDM Void-Debt Modulation
**Context:** derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:24-25 • Commit: 6885588

$$
\partial_t \mathcal{D}=\frac{1}{\tau_g}\,g\!\left(\kappa,\lvert\nabla u\rvert,\lvert\nabla s\rvert\right)-\frac{\mathcal{D}}{\tau_r}
$$

$$
M(s,\mathcal{D})=M_0\,e^{-\beta\mathcal{D}},\quad c_{\text{eff}}(x,t)=c_0\,e^{-\frac12\beta\mathcal{D}}
$$

**Notes:** Debt variable $\mathcal{D}(x,t)$ gates diffusion and transport; steep gradients incur debt, locally throttling mobility; relaxes with $\tau_r$.

---

#### VDM-E-064 — Memory Steering Refractive Index
**Context:** derivation/code/physics/memory_steering/memory_steering.py:21 • Commit: 6885588

$$
n(x,t) = \exp[\eta M(x,t)]
$$

with ray bending $r'' = \nabla_{\perp} \ln n = \eta \nabla_{\perp} M$

**Notes:** Geometric optics limit; rays bend toward memory gradients via refractive index; $\eta$ is coupling strength.

---

#### VDM-E-065 — Memory Field Dynamics
**Context:** derivation/code/physics/memory_steering/memory_steering.py:25-26 • Commit: 6885588

$$
\partial_t M = \gamma R - \delta M + \kappa \nabla^2 M
$$

**Notes:** Slow memory field PDE; $R$ is usage/co-activation rate (STDP proxy), $\gamma$ write gain, $\delta$ decay, $\kappa$ consolidation/spread.

---

#### VDM-E-066 — Memory Steering Dimensionless Groups
**Context:** derivation/code/physics/memory_steering/memory_steering.py:30 • Commit: 6885588

$$
\Theta = \eta M_0,\quad D_a = \gamma R_0 T / M_0,\quad \Lambda = \delta T,\quad \Gamma = \kappa T / L^2
$$

**Notes:** Dimensionless groups with rulers $L$, $T$, $M_0$, $R_0$; $\Theta$ is junction gating strength, $D_a$ is anisotropic diffusion index, $\Lambda$ is retention fraction, $\Gamma$ is spatial consolidation.

---

#### VDM-E-067 — Memory Junction Choice Probability
**Context:** derivation/code/physics/memory_steering/memory_steering.py:35-36 • Commit: 6885588

$$
P(A) \approx \sigma(\Theta \Delta m)
$$

**Notes:** Logistic probability at fork; $\Delta m$ is memory difference between branches, $\sigma$ is sigmoid.

---

#### VDM-E-068 — Graph Laplacian for Memory Discretization
**Context:** derivation/code/physics/memory_steering/memory_steering.py:86-94 • Commit: 6885588

$$
L = D - A
$$

**Notes:** Unnormalized graph Laplacian for discrete memory PDE; $D$ is degree matrix, $A$ is adjacency; continuum analogue of $-\nabla^2$.

---

#### VDM-E-069 — Discrete Memory Update (Euler)
**Context:** derivation/code/physics/memory_steering/memory_steering.py:42 • Commit: 6885588

$$
m \leftarrow m + dt ( \gamma r - \delta m - \kappa L m )
$$

**Notes:** Explicit Euler step for memory field on graph; $r$ is usage proxy vector.

---

#### VDM-E-070 — Memory-Based Transition Probability
**Context:** derivation/code/physics/memory_steering/memory_steering.py:44-45 • Commit: 6885588

$$
P(i\to j) \propto \exp(\Theta m_j)
$$

**Notes:** Softmax steering from node $i$ to neighbor $j$; at two-branch junction reduces to $P(A)=\sigma(\Theta \Delta m)$.

---

#### VDM-E-071 — Logistic Invariant Q (ODE)
**Context:** derivation/code/rd/reaction_exact.py:16 • Commit: 6885588

$$
Q(W,t) = \ln\left( \frac{W}{r - u W} \right) - r t
$$

**Notes:** Conserved quantity for logistic ODE $dW/dt = r W - u W^2$; used for diagnostics only (not PDE invariant).

---

#### VDM-E-072 — Discrete Hamiltonian Density
**Context:** derivation/conservation_law/discrete_conservation.md:32-33 • Commit: 6885588

$$
\mathcal{H}_i = \frac{1}{2}\left(\frac{dW_i}{dt}\right)^2 + \frac{1}{2} \sum_{j \in N(i)} J (W_j - W_i)^2 + V(W_i)
$$

**Notes:** Postulated discrete energy density at site $i$; kinetic + interaction + potential terms. Used for conservation law analysis.

---

#### VDM-E-073 — Discrete Conservation Law Form
**Context:** derivation/conservation_law/discrete_conservation.md:46-48 • Commit: 6885588

$$
\frac{\Delta \mathcal{H}_i}{\Delta t} + \nabla \cdot \vec{J}_i = 0
$$

**Notes:** Local conservation law on graph; change in energy balanced by flux $\vec{J}_i$ across edges. Discrete analogue of $\nabla_\mu T^{\mu\nu} = 0$.

---

#### VDM-E-074 — Change in Potential Energy
**Context:** derivation/conservation_law/discrete_conservation.md:76-77 • Commit: 6885588

$$
\frac{\Delta V(W_i)}{\Delta t} \approx -[F(W_i)]^2
$$

with $F(W_i) = (\alpha - \beta)W_i - \alpha W_i^2$

**Notes:** Rate of change of potential energy always non-positive; describes intrinsically dissipative system.

---

#### VDM-E-075 — Discrete Lattice Lagrangian (Per Time Step)
**Context:** derivation/foundations/void_dynamics_theory.md:98-103 • Commit: 6885588

$$ L^n = a^d \sum_i \left[ \tfrac{1}{2}\left(\tfrac{W_i^{n+1}-W_i^{n}}{\Delta t}\right)^2 + \tfrac{\kappa}{2}\sum_{\mu=1}^{d}\big(W_{i+\mu}^{n}-W_i^{n}\big)^2 + V!\big(W_i^{n}\big) \right] $$

**Notes:** Discrete Lagrangian for lattice action; $\kappa$ is per-edge coupling ($\kappa = 2J$ in per-site convention).

---

#### VDM-E-076 — Discrete Euler-Lagrange (Second-Order)
**Context:** derivation/foundations/void_dynamics_theory.md:111-114 • Commit: 6885588

$$
\frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{(\Delta t)^2}
-\kappa\,\sum_{\mu=1}^d \big(W_{i+\mu}^{n}+W_{i-\mu}^{n}-2W_i^{n}\big)
+V'\!\big(W_i^{n}\big)=0
$$

**Notes:** Second-order discrete field equation from variational principle; no "promotion" needed—arises naturally from action.

---

#### VDM-E-077 — Continuum Field Equation from Lattice
**Context:** derivation/foundations/void_dynamics_theory.md:134 • Commit: 6885588

$$
\partial_t^2\phi - \kappa\,a^2\,\nabla^2\phi + V'(\phi)=0
$$

**Notes:** Continuum limit of discrete Euler-Lagrange; wave speed $c^2 = \kappa\,a^2$ (or $c^2=2J\,a^2$ in per-site convention).

---

#### VDM-E-078 — Continuum Lagrangian Density
**Context:** derivation/foundations/void_dynamics_theory.md:146 • Commit: 6885588

$$
\mathcal{L} = \frac{1}{2}(\partial_t\phi)^2 - \frac{\kappa a^2}{2}(\nabla\phi)^2 - V(\phi)
$$

**Notes:** Drop-in continuum Lagrangian from lattice limit; equivalent to $\tfrac12(\partial_t\phi)^2 - J a^2(\nabla\phi)^2 - V(\phi)$ with $c^2=2Ja^2$ in per-site convention.

---

#### VDM-E-079 — Spatial Taylor Expansion (Exact Coefficient)
**Context:** derivation/foundations/void_dynamics_theory.md:37 • Commit: 6885588

$$
\sum_{j}(W_j-W_i)^2 \to c_\text{lat}\,a^2(\nabla\phi)^2+\mathcal{O}(a^4)
$$

**Notes:** Exact derivation of spatial kinetic prefactor from discrete interaction; Lorentz invariance fixes $c_\text{lat}J a^2=1$ in chosen units for 3D cubic lattice.

---

#### VDM-E-080 — Discrete Interaction Energy per Site
**Context:** derivation/foundations/void_dynamics_theory.md:44 • Commit: 6885588

$$
\mathcal{L}_i=\tfrac12(\Delta_t W_i)^2-\tfrac12\sum_j J(W_j-W_i)^2 - V(W_i)
$$

**Notes:** Lattice Lagrangian density per node; apply discrete Euler-Lagrange to derive second-order time dynamics without hand-waving.

---

## Change Log
- VDM-E-001 to VDM-E-071 • 6885588 • Initial compilation from repository files
- VDM-E-072 to VDM-E-080 • 6885588 • Added discrete conservation law and lattice action equations from derivation/conservation_law/ and derivation/foundations/
