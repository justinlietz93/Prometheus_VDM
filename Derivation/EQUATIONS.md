<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/equations_maintenance.md -->
<!-- markdownlint-disable MD033 -->
# VDM Canonical Equations & Procedural Math (Auto-compiled)

Note on scope: This document reflects the latest accepted canonical equations only. Historical notes and timeline are maintained in Derivation/CORRECTIONS.md and memory-bank/decisionLog.md.

Last updated: 2025-11-05 (commit a48f2d2)

*Defining equations and procedural math currently present in this repository.*

- Source of truth: extracted from repository files; do not edit equations here without updating their sources.
- MathJax only: use `$...$` and `$$...$$`; no numbering/tags/environments not supported by GitHub.
- Labels: entries are headed by `VDM-E-###` (header anchors); no equation tags inside MathJax.

---

## VDM-E-001 - Agency/Consciousness Field Evolution

**Context:** Derivation/AGENCY_FIELD.md:38-39 • Commit: 6885588

$$
\partial_t C(x,t) = D\,\nabla^2 C(x,t) - \gamma\, C(x,t) + S(x,t)
$$

**Notes:** Core field equation for agency/consciousness order parameter; $C$ spreads via diffusion $D$, decays at rate $\gamma$, driven by source $S$ from organized information processing.

---

### VDM-E-002 - Agency Field Composite Source

**Context:** Derivation/AGENCY_FIELD.md:47-48 • Commit: 6885588

$$
S(x,t) = \sigma(x)\,\big[\kappa_1 P(x,t)+\kappa_2 I_{\text{net}}(x,t)+\kappa_3 U(x,t)\big] \times g(V)\,h(B)
$$

**Notes:** Source combines predictive power $P$, integration $I_{\text{net}}$, control efficacy $U$, gated by option capacity $V$ and balance $B$; scaled by substrate susceptibility $\sigma$.

---

#### VDM-E-003 - Agency Field Steady State

**Context:** Derivation/AGENCY_FIELD.md:62-64 • Commit: 6885588

$$
C_{\text{ss}}=\frac{S_0}{\gamma},\qquad
C(t)=C_{\text{ss}}+\big(C(0)-C_{\text{ss}}\big)e^{-\gamma t}
$$

**Notes:** For uniform source $S_0$, field settles to $C_{\text{ss}}=S_0/\gamma$ and relaxes exponentially with decay time $1/\gamma$.

---

#### VDM-E-004 - Agency Field Causal Solution

**Context:** Derivation/AGENCY_FIELD.md:72 • Commit: 6885588

$$
C(x,t)=\iint G_{\text{ret}}(x{-}x',t{-}t')\,S(x',t')\,dx'\,dt'
$$

**Notes:** Retarded Green's function $G_{\text{ret}}$ ensures causality; no superluminal influence ($G_{\text{ret}}=0$ for $t'<t$).

---

#### VDM-E-005 - Agency Field Regional Budget

**Context:** Derivation/AGENCY_FIELD.md:81-85 • Commit: 6885588

$$
\frac{dQ_C}{dt}
=\int_{\partial\Omega} D\,\nabla C\cdot n\,dA
-\gamma \int_{\Omega} C\,dV
+\int_{\Omega} S\,dV
$$

**Notes:** Change in regional charge $Q_C$ equals boundary flux minus decay plus sources; flux/decay/source accounting.

---

#### VDM-E-006 - Agency Field Discrete Update

**Context:** Derivation/AGENCY_FIELD.md:93-94 • Commit: 6885588

$$
C_i^{n+1} = C_i^{n}+\Delta t\Big(D\,\Delta_{xx} C_i^{n}-\gamma\,C_i^{n}+S_i^{n}\Big)
$$

**Notes:** Explicit Euler discretization; requires CFL condition $\Delta t \lesssim \Delta x^2/(2dD)$ for stability.

---

#### VDM-E-007 - Agency Field Dimensionless Form

**Context:** Derivation/AGENCY_FIELD.md:102-105 • Commit: 6885588

$$
\partial_{\tilde t} C = \nabla_{\tilde x}^2 C - C + \tilde S(\tilde x,\tilde t)
$$

with $\tilde t=\gamma t$, $\tilde x=x/\ell_D$, $\ell_D=\sqrt{D/\gamma}$

**Notes:** Dimensionless rescaling by decay time and diffusion length for cross-system comparison.

---

#### VDM-E-008 - Agency Field Portal Modulation (Optional)

**Context:** Derivation/AGENCY_FIELD.md:113 • Commit: 6885588

$$
\varepsilon_{\text{eff}}(x,t)=\varepsilon_0\big(1+\alpha\,C(x,t)\big),\quad |\alpha|\ll 1
$$

**Notes:** Optional dark-sector portal coupling; portal signal leans toward high-$C$ regions without becoming new force.

---

#### VDM-E-009 - Control Efficacy

**Context:** Derivation/AGENCY_FIELD.md:53-54 • Commit: 6885588

$$
U =\frac{\mathbb{E}[L_{\text{no-control}}] - \mathbb{E}[L_{\text{control}}]}{\text{energy used}}
$$

**Notes:** Control efficacy: error reduction per unit energy; used in agency field source term.

---

#### VDM-E-010 - VDM C-Score

**Context:** Derivation/AGENCY_FIELD.md:122 • Commit: 6885588

$$
C_\tau = \big[\mathrm{z}(P_\tau/J)+\mathrm{z}(U_\tau)+\mathrm{z}(V_\tau)\big]\times B
$$

**Notes:** Comparative score over horizon $\tau$: z-scores of prediction per joule, control efficacy, option capacity, multiplied by balance.

---

#### VDM-E-011 - Discrete Action (Axiom 4)

**Context:** agent-onboarding/axiomatic_theory_development.md:38-39 • Commit: 6885588

$$
S(W)= \sum_{n} \Delta t \sum_{i} a^{d} \left( \frac{1}{2} (\Delta_t W_i)^2 - \frac{J}{2}\sum_{j\in N(i)}(W_j-W_i)^2 - V(W_i) \right), \quad J>0
$$

**Notes:** Fundamental discrete action for VDM; kinetic + interaction + potential terms on cubic lattice with spacing $a$.

---

#### VDM-E-012 - Potential and Derivatives (Axiom 3)

**Context:** agent-onboarding/axiomatic_theory_development.md:35 • Commit: 6885588

$$
V'(\phi)=\alpha\phi^{2}-r\phi+\lambda\phi^{3},\quad V''(\phi)=2\alpha\phi-r+3\lambda\phi^{2},\quad V'''(\phi)=2\alpha+6\lambda\phi
$$

with potential $V(\phi)=\tfrac{\alpha}{3}\phi^{3}-\tfrac{r}{2}\phi^{2}+\tfrac{\lambda}{4}\phi^{4}$, $r=\alpha-\beta$, $\lambda\ge0$

**Notes:** Admissible potential class with quartic stabilization; single authoritative definition of derivatives.

---

#### VDM-E-013 - Discrete Euler-Lagrange Equation

**Context:** agent-onboarding/axiomatic_theory_development.md:48 • Commit: 6885588

$$
\frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{\Delta t^{2}} = 2J \sum_{j\in N(i)}(W_j^{n}-W_i^{n}) - V'(W_i^{n})
$$

**Notes:** Second-order discrete field equation from variational principle; naturally arises without "promotion" from first-order.

---

#### VDM-E-014 - Continuum Klein-Gordon Form (EFT/KG Branch)

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-014"></a>
<!-- markdownlint-enable MD033 -->

**Context:** agent-onboarding/axiomatic_theory_development.md:51 • Commit: 6885588

$$
\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0, \qquad c^{2}=2J a^{2}
$$

**Notes:** Continuum limit of discrete action; inertial/EFT branch marked [EFT-KG]; $c^2=2Ja^2$ from exact Taylor expansion. Used by [VDM-A-013](ALGORITHMS.md#vdm-a-013) and [VDM-A-014](ALGORITHMS.md#vdm-a-014).

---

#### VDM-E-015 - Reaction-Diffusion Gradient Flow

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-015"></a>
<!-- markdownlint-enable MD033 -->

**Context:** agent-onboarding/axiomatic_theory_development.md:56-57 • Commit: 6885588

$$
\partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}, \quad D=2J a^{2}
$$

**Notes:** Overdamped/gradient-flow limit under time-scale separation; RD canonical form. Used by [VDM-A-013](ALGORITHMS.md#vdm-a-013).

---

#### VDM-E-016 - RD Lyapunov Functional

**Context:** agent-onboarding/axiomatic_theory_development.md:58-60 • Commit: 6885588

$$
\mathcal{L}[\phi]=\int_{\Omega}\left( \tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)\,dx,\qquad \hat V'(\phi)=-f(\phi)
$$

with time derivative $\frac{d}{dt}\mathcal{L}[\phi] = -\int_{\Omega} (\partial_t\phi)^2\,dx \le0$

**Notes:** Energy dissipation functional for RD; monotone decreasing under periodic or no-flux BCs.

---

#### VDM-E-017 - Linear RD Dispersion

**Context:** agent-onboarding/axiomatic_theory_development.md:155 • Commit: 6885588

$$
\sigma(k)=r-Dk^{2}
$$

**Notes:** Growth rate of Fourier mode $e^{ikx}$ linearized at $\phi=0$; Theorem U1.

---

#### VDM-E-018 - KPP Front Speed

**Context:** agent-onboarding/axiomatic_theory_development.md:163 • Commit: 6885588

$$
c_{front}=2\sqrt{D r}
$$

**Notes:** Pulled front speed for Fisher-KPP equation under monostable conditions; Theorem U2. Numeric validation: rel-err ≈ 4.7%, R²≈0.999996.

---

#### VDM-E-019 - Stationary Point Solutions

**Context:** agent-onboarding/axiomatic_theory_development.md:207 • Commit: 6885588

$$
\phi_{\pm}=\frac{-\alpha \pm \sqrt{\alpha^{2}+4\lambda r}}{2\lambda}
$$

when $\lambda>0$ and $V'(\phi)=0$

**Notes:** Vacuum solutions from potential calculus; $\phi=0$ or roots of $\lambda \phi^{2}+\alpha\phi-r=0$.

---

#### VDM-E-020 - Spatial Taylor Remainder Bound

**Context:** agent-onboarding/axiomatic_theory_development.md:126-127 • Commit: 6885588

$$
\|\Delta_a\phi-\nabla^{2}\phi\|_{\infty} \le C_{spatial}\, a^{2}\, \|\nabla^{4}\phi\|_{\infty},\qquad C_{spatial}=\frac{d}{12}
$$

**Notes:** Lemma S.1; controls error in replacing discrete Laplacian with continuum operator; $d$ is dimension.

---

#### VDM-E-021 - Temporal Taylor Remainder Bound

**Context:** agent-onboarding/axiomatic_theory_development.md:133 • Commit: 6885588

$$
\|\delta_{tt}\phi-\partial_{tt}\phi\|_{\infty} \le C_{time}\, \Delta t^{2}\, \|\partial_{t}^{4}\phi\|_{\infty},\qquad C_{time}=\frac{1}{12}
$$

**Notes:** Lemma T.1; controls error in replacing discrete second time difference with continuum operator.

---

#### VDM-E-022 - Dimensionless RD Scaling

**Context:** agent-onboarding/axiomatic_theory_development.md:422-427 • Commit: 6885588

$$
t' = r t,\quad x' = x\sqrt{r/D},\quad \phi = \phi_{*}\, y
$$

yields $\partial_{t'} y = \nabla_{x'}^{2} y + y - y^{2} - \Lambda\, y^{3}$

with $\Lambda=\lambda r/u^{2}$ (when $u>0$), $\phi_{*}=r/u$ or $\sqrt{r/\lambda}$

**Notes:** Dimensionless collapse for RD PDE; front speed becomes $\hat c = 2$, dispersion $\hat\sigma(k')=1-k'^{2}$.

---

#### VDM-E-023 - Discrete Flux Conservation

**Context:** agent-onboarding/axiomatic_theory_development.md:102-106 • Commit: 6885588

$$
F_{ij}=-\frac{D}{a}\,(\phi_j-\phi_i),\qquad F_{ij}=-F_{ji}
$$

with update $\phi_i^{n+1}=\phi_i^{n}-\frac{\Delta t}{a}\sum_{j\in N(i)}F_{ij}$

**Notes:** Lemma F.1; antisymmetric edge fluxes conserve total mass $\sum_i \phi_i$ with periodic or Neumann BCs when $f\equiv 0$.

---

#### VDM-E-024 - Asynchronous Census Hazard and Clock

**Context:** agent-onboarding/axiomatic_theory_development.md:513-515 • Commit: 6885588

$$
h_i := \big| D\,\Delta_a \phi_i + f(\phi_i) \big|,\qquad c_i^{n+1} \leftarrow c_i^{n} + h_i\,\Delta t
$$

**Notes:** Local hazard for event-driven sparse updates; site $i$ fires when $c_i \ge 1$ with micro-step $\delta t_i = \theta / h_i$ for quantum $\theta\in(0,1]$.

---

#### VDM-E-025 - Exact Logistic Reaction Step

**Context:** agent-onboarding/axiomatic_theory_development.md:519-521 • Commit: 6885588

$$
W^{+}=\frac{r\,W\,e^{r\delta t}}{u\,W\,(e^{r\delta t}-1)+r}
$$

for $dW/dt = r\,W - u\,W^{2}$

**Notes:** Closed-form exact solution for on-site reaction over time $\delta t$; used in census engine. Also in Derivation/code/rd/reaction_exact.py:7.

---

#### VDM-E-026 - Discrete Gradient Lyapunov Step

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-026"></a>
<!-- markdownlint-enable MD033 -->

**Context:** agent-onboarding/axiomatic_theory_development.md:110-112 • Commit: 6885588

$$
\mathcal{L}^{n+1}-\mathcal{L}^{n} = -\Delta t\,\left\|\frac{\phi^{n+1}-\phi^{n}}{\Delta t}\right\|_{2}^{2}\le 0
$$

with $\frac{\phi^{n+1}-\phi^{n}}{\Delta t} = D\nabla^{2}_h \bar\phi + \bar f$, $\hat V'(\bar\phi)=-\bar f$

**Notes:** Lemma DG.1; discrete-gradient update preserves energy monotonicity. Used by [VDM-A-013](ALGORITHMS.md#vdm-a-013).

---

#### VDM-E-027 - RD On-Site (Discrete)

**Context:** Derivation/VDM_Overview.md:23-24 • Commit: 6885588

$$
\frac{d W_i}{dt} = (\alpha - \beta)\, W_i - \alpha \, W_i^{2} + J \sum_{j\in \mathrm{nbr}(i)} (W_j - W_i)
$$

**Notes:** Discrete on-site dynamics near homogeneous state; canonical RD branch [PROVEN].

---

#### VDM-E-028 - RD Continuum PDE

**Context:** Derivation/VDM_Overview.md:31 • Commit: 6885588

$$
\partial_t \phi = D\, \nabla^{2}\phi + r\, \phi - u\, \phi^{2} \quad \bigl[ -\lambda\, \phi^{3} \text{ (optional stabilization)} \bigr]
$$

**Notes:** Continuum reaction-diffusion equation; $\lambda\phi^3$ term optional for stabilization.

---

#### VDM-E-029 - RD Discrete-to-Continuum Mapping

**Context:** Derivation/VDM_Overview.md:39-43 • Commit: 6885588

$$
\begin{aligned}
D &= J a^{2} && \text{(site Laplacian)}\\
D &= \tfrac{J}{z} a^{2} && \text{(neighbor-average form)}\\
r &= \alpha - \beta,\quad u = \alpha
\end{aligned}
$$

**Notes:** Exact parameter mapping from discrete to continuum; $z$ is coordination number.

---

#### VDM-E-030 - EFT Kinetic Normalization (Active; KPI-gated)

**Context:** Derivation/VDM_Overview.md:52-54 • Commit: 6885588

$$
c^{2} = 2 J a^{2} \quad \text{(per-site)}, \qquad c^{2} = \kappa a^{2},\; \kappa = 2J \quad \text{(per-edge)}
$$

**Notes:** EFT/KG branch [PLAUSIBLE]; active with KPI gates and provenance; distinct from RD diffusion coefficient $D$.

---

#### VDM-E-031 - EFT Second-Order Field Equation (Active; KPI-gated)

**Context:** Derivation/VDM_Overview.md:60-62 • Commit: 6885588

$$
\square \phi + V'(\phi) = 0, \qquad \square = \partial_t^{2} - c^{2} \nabla^{2}
$$

**Notes:** Klein-Gordon form; EFT branch [PLAUSIBLE].

---

#### VDM-E-032 - EFT Effective Mass (Active; KPI-gated)

**Context:** Derivation/VDM_Overview.md:68-70 • Commit: 6885588

$$
m_{\mathrm{eff}}^{2} = V''(v)
$$

**Notes:** Effective mass parameter-dependent on vacuum $v$; EFT branch.

---

#### VDM-E-033 - RD Front Speed (Validated)

**Context:** Derivation/VDM_Overview.md:110 • Commit: 6885588

$$
c_{\text{front}} = 2\sqrt{D r}
$$

**Notes:** Fisher-KPP pulled front speed [PROVEN]; validated with rel_err ≈ 0.047, R² ≈ 0.999996. See Derivation/reaction_diffusion/rd_front_speed_validation.md.

---

#### VDM-E-034 - RD Discrete Dispersion

**Context:** Derivation/VDM_Overview.md:122-124 • Commit: 6885588

$$
\sigma_d(m) = r - \frac{4D}{\Delta x^{2}} \sin^{2}\!\left(\frac{\pi m}{N}\right)
$$

**Notes:** Discrete dispersion for periodic domain mode $m$; continuum limit gives $\sigma(k) = r - D k^{2}$ with $k = 2\pi m/L$.

---

#### VDM-E-035 - RD Continuum Dispersion (Validated)

**Context:** Derivation/VDM_Overview.md:128-130 • Commit: 6885588

$$
\sigma(k) = r - D k^{2}, \qquad k = \frac{2\pi m}{L}
$$

**Notes:** Linearized growth rate about $\phi \approx 0$ [PROVEN]; median rel. error ≈ 1.45×10⁻³, R² ≈ 0.99995. See Derivation/reaction_diffusion/rd_dispersion_validation.md.

---

#### VDM-E-036 - RD Homogeneous Fixed Point

**Context:** Derivation/VDM_Overview.md:150-152 • Commit: 6885588

$$
\phi^{\star} = \frac{r}{u} = 1 - \frac{\beta}{\alpha} \qquad (r = \alpha - \beta,\; u = \alpha)
$$

**Notes:** Stable fixed point for $r>0$; $\phi=0$ is dynamically unstable.

---

#### VDM-E-037 - Axiomatic Effective Mass Squared

**Context:** Derivation/axiomatic_theory_development.md:428 • Commit: 6885588

$$
V_{\text{eff}}(\eta) = \frac{1}{2}m_{\text{eff}}^2 \eta^2 + \frac{g_3}{3!}\eta^3 + \frac{g_4}{4!}\eta^4 + \ldots
$$

where $m_{\text{eff}}^2 = V''(v_\lambda) > 0$ ensures stability

**Notes:** Effective potential around vacuum for symmetry breaking analysis; Phase III.1.

---

#### VDM-E-038 - Discrete Euler-Lagrange Variation

**Context:** Derivation/axiomatic_theory_development.md:257 • Commit: 6885588

$$
\frac{\delta S}{\delta W_i^n} = \Delta t \cdot a^d \left[ \frac{\partial \mathcal{L}_i^n}{\partial W_i^n} + \frac{\partial \mathcal{L}_i^{n-1}}{\partial W_i^n} + \sum_{j \in N(i)} \frac{\partial \mathcal{L}_j^n}{\partial W_i^n} \right]
$$

**Notes:** Variational derivative of action with respect to field at site $i$, time $n$; includes self, past, and neighbor contributions.

---

#### VDM-E-039 - Discrete Field Equation Terms

**Context:** Derivation/axiomatic_theory_development.md:260-264 • Commit: 6885588

From $\mathcal{L}_i^n$:

$$\frac{\partial \mathcal{L}_i^n}{\partial W_i^n} = -\frac{1}{\Delta t^2}(W_i^{n+1} - W_i^n) + J \sum_{j \in N(i)}(W_j^n - W_i^n) - V'(W_i^n)$$

From $\mathcal{L}_i^{n-1}$:
$$\frac{\partial \mathcal{L}_i^{n-1}}{\partial W_i^n} = \frac{1}{\Delta t^2}(W_i^n - W_i^{n-1})$$

**Notes:** Individual term-by-term contributions to discrete Euler-Lagrange equation.

---

#### VDM-E-040 - Taylor Expansion for Spatial Interaction

**Context:** Derivation/axiomatic_theory_development.md:292-295 • Commit: 6885588

$$
(W_{i+\mu} - W_i)^2 + (W_{i-\mu} - W_i)^2 = 2a^2 \left(\frac{\partial \phi}{\partial x_\mu}\right)^2 + O(a^4)
$$

summing over directions $\mu$ gives $\sum_{j \in N(i)}(W_j - W_i)^2 = 2a^2 |\nabla \phi|^2 + O(a^4)$

**Notes:** Exact derivation of spatial kinetic prefactor $c_{\text{lat}} = 2$ for 3D cubic lattice (Derivation 1.3.1).

---

#### VDM-E-041 - Lorentz Invariance Condition

**Context:** Derivation/axiomatic_theory_development.md:306-309 • Commit: 6885588

$$
c^2 = J a^2 = 2Ja^2
$$

**Notes:** Exact spatial kinetic prefactor for Lorentz-invariant continuum action; resolves "exact derivation" gap.

---

#### VDM-E-042 - Continuum Action

**Context:** Derivation/axiomatic_theory_development.md:341 • Commit: 6885588

$$
S_{\text{continuum}} = \int dt \int d^d x \left[ \frac{1}{2}\left(\frac{\partial \phi}{\partial t}\right)^2 - \frac{c^2}{2}|\nabla \phi|^2 - V(\phi) \right]
$$

**Notes:** Continuum limit of discrete action; standard scalar field theory form.

---

#### VDM-E-043 - Klein-Gordon with Nonlinear Potential

**Context:** Derivation/axiomatic_theory_development.md:352 • Commit: 6885588

$$
\frac{\partial^2 \phi}{\partial t^2} - c^2 \nabla^2 \phi + V'(\phi) = 0
$$

**Notes:** Continuum field equation from Euler-Lagrange; second-order hyperbolic PDE.

---

#### VDM-E-044 - RD Overdamped Limit

**Context:** Derivation/axiomatic_theory_development.md:357-361 • Commit: 6885588

$$
\frac{\partial \phi}{\partial t} \approx \frac{c^2}{\gamma} \nabla^2 \phi - \frac{1}{\gamma} V'(\phi)
$$

with diffusion coefficient $D = c^2/\gamma = 2Ja^2/\gamma$ and reaction term $f(\phi) = -V'(\phi)/\gamma$

**Notes:** Overdamped regime where $\frac{\partial^2 \phi}{\partial t^2} \ll c^2 \nabla^2 \phi$; $\gamma$ is damping coefficient.

---

#### VDM-E-045 - Energy Density

**Context:** Derivation/axiomatic_theory_development.md:386-387 • Commit: 6885588

$$
\rho_i^n = \frac{1}{2}\left(\frac{W_i^{n+1} - W_i^n}{\Delta t}\right)^2 + \frac{J}{2}\sum_{j \in N(i)}(W_j^n - W_i^n)^2 + V(W_i^n)
$$

**Notes:** Noether current from time translation invariance; kinetic + interaction + potential energy.

---

#### VDM-E-046 - Momentum Density (Discrete)

**Context:** Derivation/axiomatic_theory_development.md:400-401 • Commit: 6885588

$$
\mathbf{p}_i^n = -\frac{J a^{d-1}}{2} \sum_{j \in N(i)} (W_j^n - W_i^n) \hat{\mathbf{n}}_{ij} \frac{W_i^{n+1} - W_i^n}{\Delta t}
$$

**Notes:** Noether current from spatial translation invariance; $\hat{\mathbf{n}}_{ij}$ is unit vector from site $i$ to $j$.

---

#### VDM-E-047 - Continuum Energy Density (Hamiltonian)

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-047"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/axiomatic_theory_development.md:433 • Commit: 6885588

$$
\mathcal{H}(\phi, \dot{\phi}, \nabla\phi) = \frac{1}{2}\dot{\phi}^2 + \frac{c^2}{2}|\nabla\phi|^2 + V(\phi)
$$

**Notes:** Continuum energy density; conserved under time translation symmetry.

---

#### VDM-E-048 - Energy Flux (Poynting Vector)

**Context:** Derivation/axiomatic_theory_development.md:437-442 • Commit: 6885588

$$
\mathbf{S} = -c^2 \dot{\phi} \nabla\phi
$$

with conservation law $\frac{\partial \mathcal{H}}{\partial t} + \nabla \cdot \mathbf{S} = 0$

**Notes:** Energy flux for scalar field; verified using Klein-Gordon equation. Used by [VDM-A-014](ALGORITHMS.md#vdm-a-014). Additional location: Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md:14,33-35 where the continuity residual is written as $r = \partial_t e + \nabla\cdot\mathbf{s}$.

---

#### VDM-E-049 - Stress-Energy Tensor

**Context:** Derivation/axiomatic_theory_development.md:455-462 • Commit: 6885588

$$
T^{\mu\nu} = \partial^\mu \phi \partial^\nu \phi - g^{\mu\nu} \mathcal{L}
$$

with components $T^{00} = \mathcal{H}$, $T^{0i} = \dot{\phi} \partial_i \phi$, $T^{ij} = \partial_i \phi \partial_j \phi - \delta_{ij}[\frac{c^2}{2}|\nabla\phi|^2 + V(\phi)]$

**Notes:** Complete stress-energy tensor framework; $\partial_\mu T^{\mu\nu} = 0$ ensures conservation.

---

#### VDM-E-050 - RD Parameter Mapping

**Context:** Derivation/axiomatic_theory_development.md:515-521 • Commit: 6885588

Diffusion coefficient: $D = \frac{c^2}{\gamma} = \frac{2Ja^2}{\gamma}$

Reaction term: $f(\phi) = -\frac{V'(\phi)}{\gamma} = \frac{1}{\gamma}\left[(\alpha-\beta)\phi - \alpha\phi^2 - \lambda\phi^3\right]$

Parameter mapping: $r = \frac{\alpha-\beta}{\gamma}$, $u = \frac{\alpha}{\gamma}$, $\kappa = \frac{\lambda}{\gamma}$

**Notes:** Exact correspondence between discrete lattice and continuum RD parameters (Phase IV.1).

---

#### VDM-E-051 - Lyapunov Functional for RD

**Context:** Derivation/axiomatic_theory_development.md:578-579 • Commit: 6885588

$$
\mathcal{V}[\phi] = \int_\Omega \left[ \frac{D}{2}|\nabla\phi|^2 + \hat{V}(\phi) \right] dx
$$

where $\hat{V}(\phi) = \int_0^\phi f(\xi) d\xi$

**Notes:** Energy functional for RD system; $\frac{d\mathcal{V}}{dt} = -\int_\Omega (\frac{\partial \phi}{\partial t})^2 dx \leq 0$ ensures stability.

---

#### VDM-E-052 - RD Front Speed Theoretical Prediction

**Context:** Derivation/axiomatic_theory_development.md:646 • Commit: 6885588

$$
c_{\text{front}} = 2\sqrt{Dr} = 2\sqrt{\frac{2Ja^2(\alpha-\beta)}{\gamma^2}} = \frac{2a\sqrt{2J(\alpha-\beta)}}{\gamma}
$$

**Notes:** Theoretical front speed from parameter mapping; agrees with computational validation within 5% error.

---

#### VDM-E-053 - Fixed Point Consistency Check

**Context:** Derivation/axiomatic_theory_development.md:653-654 • Commit: 6885588

$$
\frac{r}{u} = \frac{\alpha-\beta}{\alpha} = 1 - \frac{\beta}{\alpha}
$$

**Notes:** Exactly matches theoretical vacuum solution in small-$\lambda$ limit.

---

#### VDM-E-054 - Void Scale Characteristic Length

**Context:** Derivation/axiomatic_theory_development.md:679 • Commit: 6885588

$$
R_* = \frac{\pi a}{\sqrt{2J(\alpha-\beta)}} \approx 8.1 \text{ (lattice units)}
$$

**Notes:** Characteristic void scale from theory; matches computational domain sizes used in validations.

---

#### VDM-E-055 - Tachyon Condensation Mode Spectrum

**Context:** Derivation/axiomatic_theory_development.md:690-693 • Commit: 6885588

$$
\omega_n^2 = c^2 k_n^2 - (\alpha-\beta) < 0
$$

for $k_n = n\pi/R$ with $n < n_{\max} = \frac{R}{\pi}\sqrt{\frac{\alpha-\beta}{c^2}}$

**Notes:** Unstable modes in finite-tube analysis; drives tachyon condensation mechanism.

---

#### VDM-E-056 - Tube Radius Selection

**Context:** Derivation/axiomatic_theory_development.md:695 • Commit: 6885588

$$
R_* \sim \frac{\pi c}{\sqrt{\alpha-\beta}} = \frac{\pi\sqrt{2Ja^2}}{\sqrt{\alpha-\beta}}
$$

**Notes:** Natural scale for void structures; emerges from tachyon condensation analysis.

---

#### VDM-E-057 - Post-Condensation Mass

**Context:** Derivation/axiomatic_theory_development.md:698 • Commit: 6885588

$$
m_{\text{eff}}^2 = V''(v_\lambda) = 2\alpha v_\lambda - (\alpha-\beta) + 3\lambda v_\lambda^2 > 0
$$

**Notes:** Positive mass-squared spectrum after condensation to vacuum $v_\lambda$.

---

#### VDM-E-058 - Stabilized Potential

**Context:** Derivation/axiomatic_theory_development.md:1119 • Commit: 6885588

$$
V_{\text{stabilized}}(\phi) = \frac{\alpha}{3}\phi^3 - \frac{\alpha-\beta}{2}\phi^2 + \frac{\lambda}{4}\phi^4
$$

**Notes:** Quartic stabilization term ensures $V(\phi) \to +\infty$ as $|\phi| \to \infty$ when $\lambda > 0$.

---

#### VDM-E-059 - Stabilized Vacuum Solution

**Context:** Derivation/axiomatic_theory_development.md:1132 • Commit: 6885588

$$
v_{\lambda} = \frac{-\alpha + \sqrt{\alpha^2 + 4\lambda(\alpha-\beta)}}{2\lambda}
$$

**Notes:** Physical vacuum for $\phi > 0$ when $\alpha > \beta$; $small\text{-}\lambda$ expansion: $v_{\lambda} \approx \frac{\alpha-\beta}{\alpha} - \frac{\lambda(\alpha-\beta)^2}{2\alpha^3} + O(\lambda^2)$.

---

#### VDM-E-060 - Effective Mass at Stabilized Vacuum

**Context:** Derivation/axiomatic_theory_development.md:1138-1141 • Commit: 6885588

$$
m_{\text{eff}}^2 = V''(v_{\lambda}) = 2\alpha v_{\lambda} - (\alpha-\beta) + 3\lambda v_{\lambda}^2 \approx (\alpha-\beta) + O(\lambda)
$$

**Notes:** Effective mass for small $\lambda$ perturbative regime.

---

#### VDM-E-061 - VDM Morphology/Assimilation Field (Fluids)

**Context:** Derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:12 • Commit: 6885588

$$
\partial_t s = \nabla\!\cdot\!\big(D_s\,M(s,\mathcal{D})\,\nabla s\big) + F(s;\text{valence},\text{resonance})
$$

**Notes:** RD-type evolution for substrate/connectome morphing variable $s(x,t)$; diffusion modulated by $M(s,\mathcal{D})$.

---

#### VDM-E-062 - VDM Signal/Transport Field (Fluids)

**Context:** Derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:17 • Commit: 6885588

$$
\tau_u\,\partial_{tt}u + \partial_t u = c^2\nabla^2 u - \frac{\partial V}{\partial u}(u,s)
$$

**Notes:** Telegraph/damped Klein-Gordon for excitations/flux $u(x,t)$; finite-speed propagation.

---

#### VDM-E-063 - VDM Void-Debt Modulation

**Context:** Derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:24-25 • Commit: 6885588

$$
\partial_t \mathcal{D}=\frac{1}{\tau_g}\,g\!\left(\kappa,\lvert\nabla u\rvert,\lvert\nabla s\rvert\right)-\frac{\mathcal{D}}{\tau_r}
$$

$$
M(s,\mathcal{D})=M_0\,e^{-\beta\mathcal{D}},\quad c_{\text{eff}}(x,t)=c_0\,e^{-\frac12\beta\mathcal{D}}
$$

**Notes:** Debt variable $\mathcal{D}(x,t)$ gates diffusion and transport; steep gradients incur debt, locally throttling mobility; relaxes with $\tau_r$.

---

#### VDM-E-064 - Memory Steering Refractive Index

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:21 • Commit: 6885588

$$
n(x,t) = \exp[\eta M(x,t)]
$$

with ray bending $r'' = \nabla_{\perp} \ln n = \eta \nabla_{\perp} M$

**Notes:** Geometric optics limit; rays bend toward memory gradients via refractive index; $\eta$ is coupling strength.

---

#### VDM-E-065 - Memory Field Dynamics

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:25-26 • Commit: 6885588

$$
\partial_t M = \gamma R - \delta M + \kappa \nabla^2 M
$$

**Notes:** Slow memory field PDE; $R$ is usage/co-activation rate (STDP proxy), $\gamma$ write gain, $\delta$ decay, $\kappa$ consolidation/spread.

---

#### VDM-E-066 - Memory Steering Dimensionless Groups

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:30 • Commit: 6885588

$$
\Theta = \eta M_0,\quad D_a = \gamma R_0 T / M_0,\quad \Lambda = \delta T,\quad \Gamma = \kappa T / L^2
$$

**Notes:** Dimensionless groups with rulers $L$, $T$, $M_0$, $R_0$; $\Theta$ is junction gating strength, $D_a$ is anisotropic diffusion index, $\Lambda$ is retention fraction, $\Gamma$ is spatial consolidation.

---

#### VDM-E-067 - Memory Junction Choice Probability

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-067"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:35-36 • Commit: 6885588

$$
P(A) \approx \sigma(\Theta \Delta m)
$$

**Notes:** Logistic probability at fork; $\Delta m$ is memory difference between branches, $\sigma$ is sigmoid. Used by [VDM-A-021](ALGORITHMS.md#vdm-a-021).

---

#### VDM-E-068 - Graph Laplacian for Memory Discretization

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:86-94 • Commit: 6885588

$$
L = D - A
$$

**Notes:** Unnormalized graph Laplacian for discrete memory PDE; $D$ is degree matrix, $A$ is adjacency; continuum analogue of $-\nabla^2$.

---

#### VDM-E-069 - Discrete Memory Update (Euler)

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:42 • Commit: 6885588

$$
m \leftarrow m + dt ( \gamma r - \delta m - \kappa L m )
$$

**Notes:** Explicit Euler step for memory field on graph; $r$ is usage proxy vector.

---

#### VDM-E-070 - Memory-Based Transition Probability

**Context:** Derivation/code/physics/memory_steering/memory_steering.py:44-45 • Commit: 6885588

$$
P(i\to j) \propto \exp(\Theta m_j)
$$

**Notes:** Softmax steering from node $i$ to neighbor $j$; at two-branch junction reduces to $P(A)=\sigma(\Theta \Delta m)$.

---

#### VDM-E-071 - Logistic Invariant Q (ODE)

**Context:** Derivation/code/rd/reaction_exact.py:16 • Commit: 6885588

$$
Q(W,t) = \ln\left( \frac{W}{r - u W} \right) - r t
$$

**Notes:** Conserved quantity for logistic ODE $dW/dt = r W - u W^2$; used for diagnostics only (not PDE invariant).

---

#### VDM-E-072 - Discrete Hamiltonian Density

**Context:** Derivation/conservation_law/discrete_conservation.md:32-33 • Commit: 6885588

$$
\mathcal{H}_i = \frac{1}{2}\left(\frac{dW_i}{dt}\right)^2 + \frac{1}{2} \sum_{j \in N(i)} J (W_j - W_i)^2 + V(W_i)
$$

**Notes:** Postulated discrete energy density at site $i$; kinetic + interaction + potential terms. Used for conservation law analysis.

---

#### VDM-E-073 - Discrete Conservation Law Form

**Context:** Derivation/conservation_law/discrete_conservation.md:46-48 • Commit: 6885588

$$
\frac{\Delta \mathcal{H}_i}{\Delta t} + \nabla \cdot \vec{J}_i = 0
$$

**Notes:** Local conservation law on graph; change in energy balanced by flux $\vec{J}_i$ across edges. Discrete analogue of $\nabla_\mu T^{\mu\nu} = 0$.

---

#### VDM-E-074 - Potential Energy Dissipation Rate

**Context:** Derivation/conservation_law/discrete_conservation.md:76-77 • Commit: 6885588

$$
\frac{\Delta V(W_i)}{\Delta t} \approx -[F(W_i)]^2
$$

with $F(W_i) = (\alpha - \beta)W_i - \alpha W_i^2$

**Notes:** Rate of change of potential energy always non-positive; describes intrinsically dissipative system.

---

#### VDM-E-075 - Discrete Lattice Lagrangian (Per Time Step)

**Context:** Derivation/foundations/void_dynamics_theory.md:98-103 • Commit: 6885588

$$ L^n = a^d \sum_i \left[ \tfrac{1}{2}\left(\tfrac{W_i^{n+1}-W_i^{n}}{\Delta t}\right)^2 + \tfrac{\kappa}{2}\sum_{\mu=1}^{d}\big(W_{i+\mu}^{n}-W_i^{n}\big)^2 + V!\big(W_i^{n}\big) \right] $$

**Notes:** Discrete Lagrangian for lattice action; $\kappa$ is per-edge coupling ($\kappa = 2J$ in per-site convention).

---

#### VDM-E-076 - Discrete Euler-Lagrange (Second-Order)

**Context:** Derivation/foundations/void_dynamics_theory.md:111-114 • Commit: 6885588

$$
\frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{(\Delta t)^2}
-\kappa\,\sum_{\mu=1}^d \big(W_{i+\mu}^{n}+W_{i-\mu}^{n}-2W_i^{n}\big)
+V'\!\big(W_i^{n}\big)=0
$$

**Notes:** Second-order discrete field equation from variational principle; no "promotion" needed-arises naturally from action.

---

#### VDM-E-077 - Continuum Field Equation from Lattice

**Context:** Derivation/foundations/void_dynamics_theory.md:134 • Commit: 6885588

$$
\partial_t^2\phi - \kappa\,a^2\,\nabla^2\phi + V'(\phi)=0
$$

**Notes:** Continuum limit of discrete Euler-Lagrange; wave speed $c^2 = \kappa\,a^2$ (or $c^2=2J\,a^2$ in per-site convention).

---

#### VDM-E-078 - Continuum Lagrangian Density

**Context:** Derivation/foundations/void_dynamics_theory.md:146 • Commit: 6885588

$$
\mathcal{L} = \frac{1}{2}(\partial_t\phi)^2 - \frac{\kappa a^2}{2}(\nabla\phi)^2 - V(\phi)
$$

**Notes:** Drop-in continuum Lagrangian from lattice limit; equivalent to $\tfrac12(\partial_t\phi)^2 - J a^2(\nabla\phi)^2 - V(\phi)$ with $c^2=2Ja^2$ in per-site convention.

---

#### VDM-E-079 - Spatial Taylor Expansion (Exact Coefficient)

**Context:** Derivation/foundations/void_dynamics_theory.md:37 • Commit: 6885588

$$
\sum_{j}(W_j-W_i)^2 \to c_\text{lat}\,a^2(\nabla\phi)^2+\mathcal{O}(a^4)
$$

**Notes:** Exact derivation of spatial kinetic prefactor from discrete interaction; Lorentz invariance fixes $c_\text{lat}J a^2=1$ in chosen units for 3D cubic lattice.

---

#### VDM-E-080 - Discrete Interaction Energy per Site

**Context:** Derivation/foundations/void_dynamics_theory.md:44 • Commit: 6885588

$$
\mathcal{L}_i=\tfrac12(\Delta_t W_i)^2-\tfrac12\sum_j J(W_j-W_i)^2 - V(W_i)
$$

**Notes:** Lattice Lagrangian density per node; apply discrete Euler-Lagrange to derive second-order time dynamics without hand-waving.

---

#### VDM-E-081 - Finite-difference estimators for $\nabla V$

<a id="vdm-e-081"></a>

**Context:** Agency Options Probe. Data come from `options.csv` with axes $E$ (steps) and $p_{\text{slip}}$ (probability). These estimates feed SIE/scoreboard gating and any policy that reacts to local capacity slope.

**Equation:**

On grid $(E_i,p_j)$,
$$
\widehat{\partial_E V}(E_i,p_j)=
\begin{cases}
\dfrac{V(E_{i+1},p_j)-V(E_i,p_j)}{E_{i+1}-E_i}, & \text{forward}\\[6pt]
\dfrac{V(E_i,p_j)-V(E_{i-1},p_j)}{E_i-E_{i-1}}, & \text{backward}
\end{cases}
$$

$$
\widehat{\partial_{p} V}(E_i,p_j)=
\begin{cases}
\dfrac{V(E_i,p_{j+1})-V(E_i,p_j)}{p_{j+1}-p_j}, & \text{forward}\\[6pt]
\dfrac{V(E_i,p_j)-V(E_i,p_{j-1})}{p_j-p_{j-1}}, & \text{backward}
\end{cases}
$$

Define $\widehat{\nabla V}=[\widehat{\partial_E V},\widehat{\partial_p V}]$ and $\|\widehat{\nabla V}\|_2=\sqrt{(\widehat{\partial_E V})^2+(\widehat{\partial_p V})^2}$.

**Notes:**

- Prefer **central differences** when both neighbors exist; fall back to the formulas above on boundaries.  
- Units: $\partial_E V$ in bits/step; $\partial_p V$ in bits per unit slip.  
- If any operand is missing/NaN, propagate NaN; optionally apply axis-wise **isotonic smoothing** to $V$ before differencing.  
- Use a small tolerance $\varepsilon_{\text{fd}}$ (e.g., $10^{-9}$) when checking signs/zeros to avoid flapping.

---

#### VDM-E-082 - Elasticities of $V$ (unitless)

<a id="vdm-e-082"></a>

**Context:** Dimensionless sensitivity for cross-regime comparison; used to decide whether budget vs. slip mitigation moves the needle more where we are.

**Equation:**
For $V>0$,
$$
\epsilon_E=\frac{E}{V}\,\partial_E V,\qquad
\epsilon_p=\frac{p_{\text{slip}}}{V}\,\partial_{p_{\text{slip}}} V.
$$

**Notes:**

- Compute with the finite-difference estimates from VDM-E-081.  
- Undefined when $V\le 0$; return NaN (or mask) in those cells.  
- Interpretation: $\epsilon_E=0.2$ means a 1% increase in $E$ raises $V$ by ~0.2%.

---

#### VDM-E-083 - Threshold energy for target capacity

<a id="vdm-e-083"></a>

**Context:** Capability boundary used by gating/planning (“just-viable” line). Plotted as $E_{\min}^{(v_0)}(p)$ for levels $v_0\in\{3,5,7\}$ bits.

**Equation:**
For target $v_0$ (bits),
$$
E_{\min}^{(v_0)}(p):=\arg\min_{E\in\mathbb{N}}\{\,V(E,p)\ge v_0\,\}.
$$

**Notes:**

- If **no** $E$ on the grid achieves $v_0$, record **NA**; optionally report an upper bound if extrapolation is disallowed.  
- Optional interpolation: piecewise-linear in $E$ to refine the boundary between integer budgets; document if enabled.  
- Monotonicity in $E$ is assumed (see VDM-E-084); if violated, apply isotonic regression along $E$ before evaluating.

---

#### VDM-E-084 - Monotonicity acceptance conditions (probe sanity)

<a id="vdm-e-084"></a>

**Context:** Sanity checks for the options probe; these are required before gradients/thresholds are trusted.

**Equation:**
For all $p$,
$$V(E+\Delta E,p)\ge V(E,p),$$
and for all $E$,
$$V(E,p+\Delta p)\le V(E,p).$$

**Notes:**

- Evaluate with tolerance $\varepsilon_{\text{mono}}$ (default $10^{-9}$). Ties within tolerance are acceptable.  
- If conditions fail, fix by (a) regenerating data, or (b) axis-wise isotonic smoothing before downstream calculations.  
- These checks justify using $E_{\min}^{(v_0)}(p)$ as a well-posed boundary and keep $\partial_E V$/$\partial_p V$ signs meaningful.

---

#### VDM-E-085 - Weight Update Rule (three stacked terms)

<a id="vdm-e-085"></a>

**Context:** [RUNTIME-ONLY] Derivation of the synaptic weight update in the Self-Improvement Engine (SIE), integrating time-dependent gain modulation with void-driven plasticity dynamics (RE-VGSP for resonance-enhanced growth and GDSP for goal-directed decay), anti-saturation regularization to prevent over-specialization, and a projection onto a budget-constrained simplex for resource allocation. This rule unifies cognitive adaptation principles with physical void debt mechanisms, supporting emergent intelligence in the Void Dynamics Model. • Source: fum_rt/core/fum_sie.py:1-260 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:23:39Z

**Equation:**
$$
\Delta W_{ij} = g_i(t) \times \underbrace{\Delta W_{ij}^{\text{void}}}_{\text{RE-VGSP + GDSP}} - \zeta \frac{\partial \Phi_{\text{sat}}(W_{ij})}{\partial W_{ij}} \xrightarrow{\text{project}} \text{simplex}(\text{budget} = B_i).
$$

**Notes:**

- $(g_i(t))$\: SIE gain factor, typically $(\eta (1 + \text{mod\_factor}) R\_{\text{total}})$\, where $(\text{mod\_factor} = 2\sigma(R\_{\text{total}}) - 1)$ modulates updates based on aggregated rewards (TD error, novelty, habituation, self-benefit); enables adaptive self-optimization.
- $(\Delta W\_{ij}^{\text{void}})$\: Combined RE-VGSP $((\alpha W\_{ij} (1 - W\_{ij}) + \text{noise}))$ and GDSP $((-\beta W\_{ij}))$ terms, yielding $((\alpha - \beta) W\_{ij} - \alpha W\_{ij}^2 + \text{noise})$\; models void debt-driven growth and dissipation, with optional time modulation $(\sin(2\pi f t))$ and domain scaling (e.g., via $(\beta / \alpha = 0.4)$\).
- Anti-saturation: $(\zeta > 0)$ scales the gradient of potential $(\Phi\_{\text{sat}})$ (e.g., quadratic $(\frac{1}{2} W\_{ij}^2)$\); prevents weight extrema, promoting dynamic responsiveness.
- Projection: Enforces non-negative weights summing to budget $(B\_i)$ via Euclidean projection; ensures sparsity and feasibility in resource-limited systems.
- Links to prior entries: Complements VDM-E-018 (Lyapunov for stability) and VDM-E-083 (budget thresholds); evaluate monotonicity per VDM-E-084 before application.
- Update via finite differences or exact gradients; monitor for convergence in metriplectic compositions.

---

#### VDM-E-086 - Resonance-Enhanced Valence-Gated Synaptic Plasticity (RE-VGSP)

<a id="vdm-e-086"></a>

**Context:** [RUNTIME-ONLY] Universal function for Resonance-Enhanced Valence-Gated Synaptic Plasticity within the void dynamics framework, modeling fractal energy drain and growth in void states. This component synchronizes with GDSP to drive adaptive evolution, serving as the growth-promoting term in void debt mechanisms for both cognitive stability in the Self-Improvement Engine (SIE) and physical pattern formation in the Void Dynamics Model (VDM). • Source: fum_rt/core/Void_Equations.py:22-55 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:23:39Z

**Equation:**
$$
\Delta_{\text{RE-VGSP}} = \alpha W (1 - W) + \text{noise},
$$

with optional time modulation: $(\Delta_{\text{RE-VGSP}} \cdot (1 + \phi \sin(2\pi f t)))$, and domain scaling applied to $(\alpha)$\.

**Notes:**

- $(\alpha)$\: Universal learning rate (default 0.25), scaled by domain modulation factor to adjust for physics contexts (e.g., quantum or cosmogenesis sparsity).
- $(W)$\: Current void state, normalized to [0,1] for logistic growth toward carrying capacity.
- $(\text{noise})$\: Stochastic term (uniform in [-0.02, 0.02]) for exploration and variability in adaptation.
- $(\phi)$\: Phase sensitivity (default 0.5); $(f)$\: Reference frequency (default 0.02) for oscillatory time dynamics.
- Domain modulation: Effective $(\alpha)$ multiplied by sparsity-derived factor (e.g., $(1.0 + (\text{sparsity fraction}^2) / (\beta / \alpha))$), unifying cognitive and physical regimes.
- Links to prior entries: Forms the growth component of VDM-E-085 (void update in SIE weights) and VDM-E-027 (RD reaction term); complements VDM-E-018 for Lyapunov monotonicity in dissipative flows.
- Evaluation: Finite-step updates via explicit Euler or metriplectic composition; monitor variance for stability in SIE simulations.
- Keep noise and sinusoial modulation off for order-of-accuracy and Lyapunov tests.

---

#### VDM-E-087 - Goal-Directed Structural Plasticity (GDSP)

<a id="vdm-e-087"></a>

**Context:** [RUNTIME-ONLY] Universal function for Goal-Directed Structural Plasticity within the void dynamics framework, modeling weak closure and dissipation in void states. This component synchronizes with RE-VGSP to enforce stability, serving as the decay term in void debt mechanisms for balancing growth in cognitive adaptation via the Self-Improvement Engine (SIE) and physical relaxation in the Void Dynamics Model (VDM). • Source: fum_rt/core/Void_Equations.py:56-88 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:23:39Z

**Equation:**
$$
\Delta_{\text{GDSP}} = -\beta W,
$$

with optional time modulation: $(\Delta_{\text{GDSP}} \cdot (1 + \phi \sin(2\pi f t)))$, and domain scaling applied to $(\beta)$\.

**Notes:**

- $(\beta)$\: Universal plasticity rate (default 0.1), scaled by domain modulation factor to tune dissipation across physics contexts.
- $(W)$\: Current void state, where linear decay prevents unbounded growth and promotes equilibrium.
- $(\phi)$\: Phase sensitivity (default 0.5); $(f)$\: Reference frequency (default 0.02) for time-dependent oscillations.
- Domain modulation: Effective $(\beta)$ multiplied by sparsity-derived factor (e.g., $(1.0 + (\text{sparsity fraction}^2) / (\beta / \alpha))$\), ensuring consistency with cognitive stability requirements.
- Links to prior entries: Forms the dissipative component of VDM-E-085 (void update in SIE weights) and VDM-E-001 (field decay term); ensures H-theorem compliance as in VDM-E-018.
- Evaluation: Combines with RE-VGSP for net void update; test for monotonic convergence in metriplectic integrators.
- Keep noise and sinusoial modulation off for order-of-accuracy and Lyapunov tests.

---

#### VDM-E-088 - Universal Void Dynamics (Combined RE-VGSP + GDSP)

<a id="vdm-e-088"></a>

**Context:** [RUNTIME-ONLY] Simplified interface for combined void dynamics, applying both RE-VGSP and GDSP with universal constants to compute a single-step evolution of void states. This function encapsulates the synergistic growth-dissipation balance central to void debt, enabling unified application in cognitive self-optimization via the Self-Improvement Engine (SIE) and physical emergence in the Void Dynamics Model (VDM). • Source: fum_rt/core/Void_Equations.py:91-99 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:23:39Z

**Equation:**
$$
\Delta W = \Delta_{\text{RE-VGSP}} + \Delta_{\text{GDSP}} = (\alpha - \beta) W - \alpha W^2 + \text{noise},
$$

with optional time modulation on each term and domain scaling applied to $(\alpha)$ and $(\beta)$.

**Notes:**

- Combines VDM-E-086 (RE-VGSP) and VDM-E-087 (GDSP) for net void debt-driven update, promoting logistic equilibrium with stochastic variability.
- Universal constants: $(\alpha = 0.25)$, $(\beta = 0.1)$, $(\phi = 0.5)$, $(f = 0.02)$\; noise uniform in [-0.02, 0.02].
- Domain modulation: Scales effective rates via sparsity fraction, e.g., $(1.0 + (\text{sparsity fraction}^2) / (\beta / \alpha = 0.4))$, bridging cognitive and physical domains.
- Links to prior entries: Direct basis for VDM-E-085 (SIE void term) and VDM-E-027 (discrete RD reaction); supports Lyapunov stability as in VDM-E-018.
- Evaluation: Use for iterative simulations; verify against metriplectic H-theorem for monotonicity.

---

#### VDM-E-089 - Universal Domain Modulation Factor

<a id="vdm-e-089"></a>

**Context:** [PLAUSIBLE] [RUNTIME-ONLY] Derivation of domain-specific modulation factors from void debt principles, scaling universal constants like $(\alpha)$ and $(\beta)$ based on target sparsity for different physics regimes. This function ensures cognitive stability constants generate realistic physics, unifying adaptation in the Self-Improvement Engine (SIE) with emergent behaviors in the Void Dynamics Model (VDM) across domains like quantum or cosmogenesis. • Source: fum_rt/core/Void_Debt_Modulation.py:49-55 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:23:39Z

**Equation:**
$$
\text{domain\_modulation} = 1.0 + \frac{(\text{sparsity\_fraction}^2)}{(\beta / \alpha)}
$$

where $(\text{sparsity\_fraction} = \text{target\_sparsity\_pct} / 100)$, and $(\beta / \alpha = 0.4)$\.

**Notes:**

- $(\text{target\_sparsity\_pct})$\: Domain-specific sparsity (e.g., 15.0 for quantum, 84.0 for cosmogenesis), defaulting to 25.0 if unspecified.
- Void debt ratio: Fixed at $(\beta / \alpha = 0.4)$\, derived from universal constants for learning stability.
- Application: Multiplies effective $(\alpha)$ or $(\beta)$ in void equations (e.g., VDM-E-086, -087), tuning for physical consistency without arbitrary adjustments.
- Links to prior entries: Modulates terms in VDM-E-085 (SIE weights) and VDM-E-027 (RD rates); validates against physics ranges (1.0-2.0) as in change log notes.
- Evaluation: Compute for parameter sweeps; ensure mean and std align with model stability (e.g., mean ~1.637 ± 0.741 in sample grids).
- Keep turned off for physics tests until [PROVEN]

---

#### VDM-E-090 - Two-Grid Error Metric and Log–Log Fit (Metriplectic QC)

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-090"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:58-118 • Commit: HEAD

Given a one-step map $\Phi_{\Delta t}$ and an initial state $W_0$, define the two-grid infinity-norm error

$$
e_{\infty}(\Delta t)
\;=\; \left\|\, \Phi_{\Delta t}(W_0) \;-
\; \Phi_{\Delta t/2}\big(\, \Phi_{\Delta t/2}(W_0) \,\big) \,\right\|_{\infty}.
$$

For a sweep of step sizes $\{\Delta t_i\}$, aggregate across seeds via the median $m_i=\operatorname{median}\, e_{\infty}(\Delta t_i)$, then perform an ordinary least-squares fit on log–log axes:

$$
x_i = \log \Delta t_i,\qquad y_i = \log m_i,\qquad
p = \frac{\operatorname{cov}(x,y)}{\operatorname{var}(x)},\quad b = \bar y - p\,\bar x,
$$

with coefficient of determination

$$
R^2 = 1 - \frac{\sum_i (y_i - (p x_i + b))^2}{\sum_i (y_i - \bar y)^2}.
$$

**Notes:** Used to assess convergence order $p$ and goodness-of-fit $R^2$ for M-only and JMJ schemes. Used by [VDM-A-016](ALGORITHMS.md#vdm-a-016), [VDM-A-017](ALGORITHMS.md#vdm-a-017), and [VDM-A-019](ALGORITHMS.md#vdm-a-019).

---

#### VDM-E-091 - Strang Composition Defect (JMJ vs MJM)

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-091"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:265-316 • Commit: HEAD

For Strang compositions $\Phi^{\text{JMJ}}_{\Delta t}$ and $\Phi^{\text{MJM}}_{\Delta t}$ applied to the same initial state $W_0$, define the defect

$$
\mathcal{D}_{\text{Strang}}(\Delta t)
\;=\; \left\|\, \Phi^{\text{JMJ}}_{\Delta t}(W_0) \;-
\; \Phi^{\text{MJM}}_{\Delta t}(W_0) \,\right\|_{\infty}.
$$

Fit $\mathcal{D}_{\text{Strang}}(\Delta t)$ versus $\Delta t$ on log–log axes as in VDM-E-090 to estimate slope (expected near $3$ for second-order symmetric schemes) and $R^2$.

**Notes:** Proxies commutator strength between J and M operators. Used by [VDM-A-018](ALGORITHMS.md#vdm-a-018).

---

#### VDM-E-092 - Discrete Lyapunov Functional (Grid Form)

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-092"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:142-190 • Commit: HEAD

On a regular grid with spacing $h$ and discrete gradient $\nabla_h$, define

$$
L_h[\phi] \;=\; \sum_{i} \Big( \tfrac{D}{2}\,\lvert \nabla_h \phi_i \rvert^2 + \hat V(\phi_i) \Big) h^d,
\qquad \text{with}\quad \hat V'(\phi) = - f(\phi),
$$

so that along a discrete-gradient (DG) dissipative step $\phi^{k}\!\to\!\phi^{k+1}$,

$$
\Delta L_h = L_h[\phi^{k+1}] - L_h[\phi^{k}] \;\le\; 0.
$$

**Notes:** Grid analogue of VDM-E-016 (RD Lyapunov); used to check per-step monotonicity under M-only or within JMJ. Used by [VDM-A-015](ALGORITHMS.md#vdm-a-015) and [VDM-A-019](ALGORITHMS.md#vdm-a-019).

---

#### VDM-E-093 - FRW Continuity Residual (Dust) and RMS

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-093"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/code/physics/cosmology/run_frw_balance.py:1-118 • Commit: HEAD

For scale factor $a(t)$, density $\rho(t)$, and equation-of-state parameter $w$, define the residual

$$
r(t) = \frac{d}{dt}\big(\rho(t)\, a(t)^3\big) + w\,\rho(t)\,\frac{d}{dt}\big(a(t)^3\big).
$$

In the dust control case $w=0$, this reduces to $r(t)=\tfrac{d}{dt}(\rho a^3)$. The discrete root-mean-square used in QC is

$$
\operatorname{RMS}(r) = \sqrt{\frac{1}{N} \sum_{n=1}^{N} r(t_n)^2 }.
$$

**Notes:** Identity test under synthetic inputs; machine-precision RMS indicates correct finite-difference implementation. Used by [VDM-A-020](ALGORITHMS.md#vdm-a-020).

---

#### VDM-E-094 - Scaling-Collapse Envelope (Junction Logistic Universality)

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-094"></a>
<!-- markdownlint-enable MD033 -->

**Context:** Derivation/code/physics/collapse/run_a6_collapse.py:1-154 • Commit: HEAD

Given reparameterized curves $P_i(X)$ with $X = \Theta\,\Delta m$, define the envelope

$$
E(X) = \max_i P_i(X) - \min_i P_i(X), \qquad \text{and} \qquad \mathrm{env\_max} = \sup_X E(X),
$$

computed on a shared $X$-grid via interpolation over the intersection of curve domains.

**Notes:** Universality gate uses $\mathrm{env\_max}$ threshold; logistic junction choice is given in VDM-E-067. Used by [VDM-A-021](ALGORITHMS.md#vdm-a-021).

---

#### VDM-E-095 - Tube Secular Equation (Tachyonic Interior, Massive Exterior)

**Context:** Derivation/Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md • Commit: 09f871a

$$
 f_\ell(\kappa;R,\mu,c)=\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\,\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)}+\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)}=0
$$

with

$$
\kappa_{\rm in}^2 = \frac{\mu^2}{c^2}-\kappa^2,\qquad \kappa_{\rm out}^2 = \kappa^2 + 2\frac{\mu^2}{c^2}.
$$

**Notes:** Cylindrical tube at axial wavenumber $k=0$ with tachyonic interior and massive exterior. Used by tube spectrum solver [VDM-A-022].

---

#### VDM-E-096 - Physically-Admissible Coverage Metrics (Tube Spectrum QC)

**Context:** Derivation/Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md • Commit: 09f871a

Primary KPI (gate):

$$
\mathrm{cov}_{\rm phys} = \frac{\#\,\text{roots found}}{\#\,\text{(}R,\ell\text{) with root-potential}},\quad \text{root-potential via sign change of } f_\ell(\kappa).
$$

Secondary (transparency):

$$
\mathrm{cov}_{\rm raw} = \frac{\#\,\text{roots found}}{\#\,(R,\ell)\,\text{in sweep}}.
$$

**Notes:** $\mathrm{cov}_{\rm phys}$ used for gating; $\mathrm{cov}_{\rm raw}$ reported for sweep comparability. Residual quality $\max|f_\ell(\kappa)|$ reported (v1 informational).

---

#### VDM-E-097 - Condensation Energy Model (Diagonal-\lambda) and Background

**Context:** Derivation/Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md • Commit: 09f871a

Mode quartic overlap and mass:

$$
N4_\ell = (2\pi)\,\lambda\int_0^\infty r\,u_\ell(r)^4\,dr,\qquad m_\ell^2 = -c^2\kappa_\ell^2.
$$

Background and total energy:

$$
E_{\rm bg}(R) = 2\pi\sigma R + \frac{\alpha}{R},\qquad E(R)=E_{\rm bg}(R)+\sum_\ell \Big[ \tfrac12 m_\ell^2 v_\ell^2 + \tfrac14 N4_\ell v_\ell^4 \Big].
$$

**Notes:** Adaptive radial integral with tail handling; curvature gate uses quadratic fit coefficient $a>0$ near interior minimum $R_\star$ (with $\Delta^2 E$ fallback).

---

#### VDM-E-114 - Scalar-wave continuity residual (energy balance)

**Context:** [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md:14) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
r = \partial_t e + \nabla\cdot\mathbf{s}
$$

**Notes:** Meter definition used in Wave Flux Meter Phase A (closed box). See also [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md:33-35). Related energy density and flux are defined in [VDM-E-047](Derivation/EQUATIONS.md#vdm-e-047) and [VDM-E-048](Derivation/EQUATIONS.md#vdm-e-048).

---

#### VDM-E-102 - KG linear dispersion (J-only diagnostic)

**Context:** [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:140-148) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
\omega^2 = c^2 k^2 + m^2
$$

**Notes:** Gate target used for KG diagnostics (slope/intercept fit). Additional location: [Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md:20).

---

#### VDM-E-103 - Strang error commutator scaling

**Context:** [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:259-263) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
\mathrm{Err}_{\text{Strang}}=\mathcal{O}\!\left(\Delta t^3,\,[A,[A,B]]+[B,[B,A]]\right)
$$

**Notes:** Procedural order diagnostic for composition methods; used to interpret two-grid slope and defect regressions when $[A,B]\neq 0$.

---

#### VDM-E-098 - FRW continuity residual (dust with equation-of-state parameter)

**Context:** [Derivation/SYMBOLS.md](Derivation/SYMBOLS.md:215-216) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
r(t)=\frac{d}{dt}\big(\rho\, a^3\big) + w\,\rho\,\frac{d}{dt}\!\big(a^3\big)
$$

**Notes:** Used for FRW continuity residual QC (dust baseline $w=0$) referenced by [Derivation/DATA_PRODUCTS.md](Derivation/DATA_PRODUCTS.md:231,261,279). TODO: add $w$ (equation-of-state parameter) to SYMBOLS.md (see [Derivation/SYMBOLS.md](Derivation/SYMBOLS.md:215)).

---

#### VDM-E-099 - M-step Lyapunov monotonicity (per-step)

**Context:** [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:168-170) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
\boxed{\ \Delta L_h \le 0\ \ \text{per step}\ }
$$

**Notes:** Axiom-level gate for discrete-gradient (metric) step. Keeps procedural statement intact as written in source. Symbol $L_h$ appears elsewhere in canon; if not present in SYMBOLS registry, align with existing entry. Additional context for metriplectic gates in [Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md:41-42).

---

#### VDM-E-100 - KG locality bound (front velocity)

**Context:** [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:145-148) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
\boxed{\ v_{\text{front}} \le c\,(1+\varepsilon)\ ,\ \ \varepsilon\ \text{set by discretization tolerance}\ }
$$

**Notes:** Conservative J-only diagnostics gate used with the KG limb (finite cone). See validated instrument summary in [Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md:19).

---

#### VDM-E-101 - Metriplectic degeneracy conditions (functional)

**Context:** [Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md:26) • Commit: 393ed61 • Last Updated: 2025-11-05T02:53:05Z

$$
\langle J\,\delta\Sigma,\,\delta\Sigma \rangle \approx 0
\qquad\text{and}\qquad
\langle M\,\delta I,\,\delta I \rangle \approx 0
$$

**Notes:** Gate targets for J/M orthogonality (grid-refined tolerances used in RESULTS). TODO: add $\delta\Sigma$ and $\delta I$ to SYMBOLS.md (see [Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md:26)) if not already present.

---

#### VDM-E-104 - Metriplectic evolution with degeneracies (spec-level)

**Context:** [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:52-56) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
\dot{\delta x} \;=\; \{x,H\}_J \;+\; (x,S)_M
$$

and

$$
\{S,\,\cdot\}_J \;=\; 0
\qquad\text{and}\qquad
(H,\,\cdot)_M \;=\; 0
$$

**Notes:** Spec-level statement in the T0 Unification hyper-proposal; included for traceability. Additional location (background and usage): [Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md:34-73). Status: In progress (spec-level).

---

#### VDM-E-105 - Telegraph characteristic speed from relaxation (spec-level)

**Context:** [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:326-333) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
c \;=\; \sqrt{\frac{D}{\tau}}
$$

**Notes:** Spec-level emergence path for finite-speed transport under moment-closure/relaxation. Additional location (tentative derivations and references): [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md:246-266). Status: In progress (spec-level). TODO: add $\tau$ to SYMBOLS.md if not already present (see context lines above).

---

#### VDM-E-106 - Void-debt throttled effective speed (spec-level)

**Context:** [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:52-56) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
c_{\mathrm{eff}} \;=\; c_0 \,\exp\!\big(-\tfrac{1}{2}\,\beta\, D\big)
$$

**Notes:** Spec-level throttling law adopted in the Unification spec; additional mention: [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:330-331). Status: In progress (spec-level). TODO: add $\beta$ and $D$ (void-debt) to SYMBOLS.md (see cited lines).

---

#### VDM-E-107 - Hierarchical interface-count scaling (spec-level, A8 program)

**Context:** [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:339-346) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
N(L) \;\sim\; \Theta(\log L)
$$

**Notes:** Spec-level scaling asserted in A8 hierarchy discussion. Tentative supporting sources and bridge sketches appear in: [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md:168-205,212-242). Status: In progress (spec-level). TODO: add $N$, $L$ to SYMBOLS.md if absent (see context lines above).

#### VDM-E-108 - Quantum Geometric Tensor (QGT) definition (spec-level)

**Context:** [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/Support/GPT-Gap-Fill.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/Support/GPT-Gap-Fill.md:50-55) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
Q_{\mu\nu}(R) \;=\; \langle \partial_\mu \psi \mid \partial_\nu \psi \rangle \;-\; \langle \partial_\mu \psi \mid \psi \rangle \, \langle \psi \mid \partial_\nu \psi \rangle
$$

**Notes:** Spec-level canonical definition used in QGT sources cited in PRIVATE collection. TODO: add $Q_{\mu\nu},\,\psi,\,\partial_\mu$ to SYMBOLS.md with units/normalization anchors.

---

#### VDM-E-109 - QGT split into quantum metric and Berry curvature (spec-level)

**Context:** [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/quantum-geometry.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/quantum-geometry.md:20-22) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
Q_{\mu\nu} \;=\; g_{\mu\nu} \;-\; \frac{i}{2}\,\Omega_{\mu\nu}
$$

**Notes:** Spec-level decomposition: real symmetric part $g_{\mu\nu}$ (metric/M‑limb) and imaginary antisymmetric part $\Omega_{\mu\nu}$ (Berry curvature/J‑limb). Additional location (background and mappings): [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/Support/GPT-Gap-Fill.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/Support/GPT-Gap-Fill.md:81-93). TODO: add $g_{\mu\nu},\,\Omega_{\mu\nu}$ to SYMBOLS.md.

---

#### VDM-E-110 - Schrödingerization (KvN lifting) equation (spec-level)

**Context:** [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/schrodingerization.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/schrodingerization.md:27-31) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
i\,\partial_t \lvert \psi \rangle \;=\; \hat{H}_{\mathrm{KvN}} \lvert \psi \rangle
$$

**Notes:** Spec-level formal lifting of dissipative PDEs to a purely Hamiltonian KvN system; used to unify J⊕M into a single reversible evolution in a higher-dimensional space. TODO: add $\hat{H}_{\mathrm{KvN}}$ and Dirac bra–ket symbols to SYMBOLS.md per house style.

---

#### VDM-E-111 - Transfer Entropy (causality meter definition)

**Context:** [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/causality.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/causality.md:21-24) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
TE_{X \to Y} \;=\; I\!\big( Y_{t+1}\,;\, X_t^{(k)} \,\big\vert\, Y_t^{(l)} \big)
$$

**Notes:** Instrument-level defining equation for the Causal DAG audit; used to validate A2 locality by reconstructing causal adjacency and cone-consistent delays. TODO: add $I(\cdot;\cdot\mid\cdot),\,TE_{X\to Y},\,k,\,l$ to SYMBOLS.md.

---

#### VDM-E-112 - Tachyonic instability condition (spec-level)

**Context:** [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/complete-formalism.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/complete-formalism.md:19-21) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
V''(0) \;<\; 0
$$

**Notes:** Spec-level defining condition for tachyonic regime referenced in A8 program materials and comparison with Sen’s conjecture. TODO: ensure $V(\phi)$ and derivatives are present in SYMBOLS.md with units.

---

#### VDM-E-113 - Excess-energy scaling at boundaries (A8 prediction, spec-level)

**Context:** [PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/complete-formalism.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/complete-formalism.md:117-121) • Commit: cbc3dd1 • Last Updated: 2025-11-05T03:18:26Z

$$
E_{\mathrm{exc}}(L) \;\sim\; L^{\,d-1}
$$

**Notes:** Spec-level scaling statement appearing as “Prediction P2”; used in hierarchy/area‑law discussions. Marked as in progress pending canon proofs. TODO: add $E_{\mathrm{exc}},\,L,\,d$ to SYMBOLS.md and link to VALIDATION_METRICS gate when promoted.

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-115"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-115 - Excess-energy functional (A8 setup)

**Context:** Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:27-33 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:32:39Z

$$
E_{\mathrm{exc}}[\phi;\Omega] \;=\; \int_{\Omega}\Big(\kappa\,\lvert\nabla \phi\rvert^2 \;+\; V(\phi) \;-\; V(\phi_\ast)\Big)\,dx
$$

**Notes:** A8 baseline energy functional for hierarchy/area-law analyses. TODO: add $\kappa$ to SYMBOLS.md (see [T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md](Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:27)).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-116"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-116 - Pulled-front tail and decay length (A8 setup)

**Context:** Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:55-60 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:32:39Z

$$
\phi(x) \sim A\,e^{-x/\lambda},
\qquad
\lambda \sim \sqrt{\frac{D}{r}}
$$

**Notes:** Exponential leading-edge for pulled fronts; decay length set by linear regime. Front speed $c_\star=2\sqrt{Dr}$ is anchored at [VDM-E-018](Derivation/EQUATIONS.md#vdm-e-018). TODO: add $A,\lambda$ to SYMBOLS.md (see [T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md](Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:55)).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-117"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-117 - Hierarchical gap condition (A8 definition)

**Context:** Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:75-81 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:32:39Z

$$
\mathrm{diam}(\Gamma_{\ell+1}) \;\in\; \big[\rho/C,\;C\rho\big]\cdot \mathrm{diam}(\Gamma_{\ell}),\quad \forall\,\ell
$$

**Notes:** Defines log-spaced interface scales in the hierarchical partition. TODO: add $\Gamma_\ell,\rho,C$ to SYMBOLS.md (see source lines).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-118"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-118 - Boundary energy concentration fraction (A8 definition)

**Context:** Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:85-91 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:32:39Z

$$
\liminf_{L\to\infty}\;
\frac{ \displaystyle \int_{\mathcal{N}_\epsilon(\cup_\ell \Gamma_\ell)} \kappa\,\lvert\nabla \phi_L\rvert^2\,dx }
     { \displaystyle E_{\mathrm{exc}}[\phi_L;\Omega_L] }
\;\ge\; \alpha
$$

**Notes:** Formalizes boundary-layer concentration of energy in A8. TODO: add $\mathcal{N}_\epsilon(\cdot),\alpha$ to SYMBOLS.md (see source lines).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-119"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-119 - Operational information-density proxies (A8 instruments)

**Context:** Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:97-105 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:32:39Z

$$\begin{aligned}
\mathcal{I}_1(x) &= \log\!\Big(1 + \frac{\lvert\nabla \phi(x)\rvert^2}{\sigma^2}\Big),\\[4pt]
\mathcal{I}_2(x) &= \tfrac{1}{2}\,\log\!\det\!\Big(I + \tau\,\nabla u(x)\,\nabla u(x)^\top\Big)
\end{aligned}$$

**Notes:** Proxies for operational information concentration near interfaces. TODO: add $\mathcal{I},\sigma,\tau,u$ to SYMBOLS.md (see source lines).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-120"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-120 - Tail cutoff and tail-loss functional (A8 truncation)
**Context:** Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:113-123 • Commit: a48f2d2 • Last Updated: 2025-11-05T04:32:39Z

$$
x_\star \;=\; \lambda\,\ln\!\Big(\frac{A}{\delta}\Big)
$$

$$
\mathcal{L}_\delta[\phi] \;\equiv\; \int_{x>x_\star}\!\Big(\kappa\,\lvert\nabla \phi\rvert^2 + \tfrac{r}{2}\,\phi^2\Big)\,dx
$$

$$
\mathcal{L}_\delta \;\propto\; \Big(\frac{\delta}{A}\Big)^{\!2}
$$

**Notes:** Linear-regime tail truncation produces localized loss functional used in A8 lemmas. TODO: add $\delta,x_\star$ to SYMBOLS.md (see source lines).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-121"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-121 - Rayleigh number (RB-Gate)
**Context:** [Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:31-34) • Commit: a48f2d2 • Last Updated: 2025-11-05T04:37:33Z

$$
\mathrm{Ra} \;=\; \frac{g\,\alpha\,\Delta T\,H^3}{\nu\,\kappa}
$$

**Notes:** Canonical control parameter for RB onset used in RB-Gate. TODO: add $\mathrm{Ra},\,g,\,\alpha,\,\Delta T,\,H,\,\nu,\,\kappa$ to SYMBOLS.md (see context lines above).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-122"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-122 - Boussinesq nondimensional RBC equations (RB-Gate)
**Context:** [Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:74-79) • Commit: a48f2d2 • Last Updated: 2025-11-05T04:37:33Z

$$\begin{aligned}
\partial_t \mathbf{u} + (\mathbf{u}\cdot\nabla)\mathbf{u} &= -\nabla p + \mathrm{Pr}\,\nabla^2 \mathbf{u} + \mathrm{Pr}\,\mathrm{Ra}\,\theta\,\hat{\mathbf{z}},\\
\partial_t \theta + (\mathbf{u}\cdot\nabla)\theta - w &= \nabla^2 \theta,\\
\nabla\cdot\mathbf{u} &= 0.
\end{aligned}$$

**Notes:** Nondimensional Oberbeck–Boussinesq form used to define RB-Gate dynamics. TODO: add $\mathrm{Pr},\,\theta,\,w,\,\hat{\mathbf{z}}$ to SYMBOLS.md (see source lines).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-123"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-123 - Nusselt number (dimensional and nondimensional) (RB-Gate)
**Context:** [Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:93-96) • Commit: a48f2d2 • Last Updated: 2025-11-05T04:37:33Z

$$
\mathrm{Nu} \;=\; \frac{\langle q_z\rangle}{k\,\Delta T/H},\qquad q_z=\rho c_p\,w\,T - k\,\partial_z T
$$

$$
\mathrm{Nu} \;=\; 1 + \langle w\theta\rangle - \langle \partial_z \theta\rangle
$$

**Notes:** Heat-transport diagnostic used near RB onset; both forms appear in the instrument description. TODO: add $\mathrm{Nu},\,q_z,\,k,\,\rho,\,c_p,\,T$ to SYMBOLS.md (see source lines).

---

<!-- markdownlint-disable MD033 -->
<a id="vdm-e-124"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-124 - Depth scaling at fixed microphysics (RB-Gate)
**Context:** [Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:127-128) • Commit: a48f2d2 • Last Updated: 2025-11-05T04:37:33Z

$$
H \mapsto 2H \;\Rightarrow\; \mathrm{Ra} \mapsto 8\,\mathrm{Ra},\quad \lambda_c \mapsto \approx 2\,\lambda_c
$$

**Notes:** Procedural scaling check used by RB-Gate. TODO: add $\lambda_c$ to SYMBOLS.md or CONSTANTS.md (critical wavelength), and link to BC-specific $k_c$ values in CONSTANTS.md when registered.

<!-- markdownlint-disable MD033 -->

#### VDM-E-125 - Strang composition map (JMJ) and order
**Context:** [RESULTS_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md:71-75) • Commit: HEAD • Last Updated: 2025-11-05T05:45:01Z

$$
\Phi^{\mathrm{JMJ}}_{\Delta t} \;=\; \Phi^{\mathrm{J}}_{\Delta t/2} \;\circ\; \Phi^{\mathrm{M}}_{\Delta t} \;\circ\; \Phi^{\mathrm{J}}_{\Delta t/2}, \qquad \text{global error } \mathcal{O}(\Delta t^2)
$$

**Notes:** Composition used throughout metriplectic runners; defect scaling and commutator context in [VDM-E-091](#vdm-e-091) and [VDM-E-103](#vdm-e-103).

---

#### VDM-E-126 - Taylor–Green energy decay (LBM→NS viscosity recovery)
**Context:** [taylor_green_benchmark.py](Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:93-105) • Commit: HEAD • Last Updated: 2025-11-05T05:45:01Z

$$
E(t) \;=\; E_0 \exp\!\Big(-2\,\nu\,k^2\big(\tfrac{1}{n_x^2}+\tfrac{1}{n_y^2}\big)\,t\Big)
$$

Slope inversion (fit on $\log E$ vs $t$):
$$
\nu_{\mathrm{fit}} \;=\; -\frac{s}{\,2 k^2\!\big(\tfrac{1}{n_x^2}+\tfrac{1}{n_y^2}\big)\,}
$$

**Notes:** Used to recover $\nu$ with ≤5% error gate; appears in fluids validation harness.

---

#### VDM-E-127 - Discrete Lyapunov functional (grid form; RD DG)
**Context:** [PROPOSAL_RD_Discrete_Conservation_vs_Balance.md](Derivation/Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md:91-101) • Commit: HEAD • Last Updated: 2025-11-05T05:45:01Z

$$
\mathcal{L}_h[W] \;=\; \sum_{i} \Big[ \tfrac{D}{2}\,\lvert \nabla_h W_i \rvert^2 + \hat V(W_i) \Big] \,\Delta x, \qquad \hat V'(W) = -\,f(W)
$$

Centered finite-difference operators:
$$
\nabla_h W_i \,=\, \frac{W_{i+1}-W_{i-1}}{2\,\Delta x}, \qquad
\Delta_h W_i \,=\, \frac{W_{i+1}-2W_i+W_{i-1}}{\Delta x^2}.
$$

**Notes:** Obj‑C discrete form paired with DG step; report $\Delta \mathcal{L}_h \le 0$ per step under periodic/no‑flux BCs. Related continuum form in [VDM-E-016](#vdm-e-016); DG monotonicity statement in [VDM-E-099](#vdm-e-099).
<a id="vdm-e-105"></a>
<!-- markdownlint-enable MD033 -->

#### VDM-E-105 - Telegraph characteristic speed from relaxation
**Context:** [Derivation/Transport/Telegraph_From_Relaxation/T1_PROPOSAL_Telegraph_From_Relaxation_v1.md](Derivation/Transport/Telegraph_From_Relaxation/T1_PROPOSAL_Telegraph_From_Relaxation_v1.md:9-12) • Commit: cbc3dd1 • Last Updated: 2025-11-05T04:43:40Z

$$
c \;=\; \sqrt{\frac{D}{\tau}}
$$

**Notes:** Spec-level speed law used by the Telegraph-from-Relaxation instrument to calibrate finite-speed transport; appears across causality meters. TODO: add $c,\,D,\,\tau$ to SYMBOLS.md (see source lines).

---

