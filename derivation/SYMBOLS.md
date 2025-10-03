# VDM Notation Reference Sheet (v0.3)

*Canonical symbols for the Void Dynamics Model physics theory*

## Core Fields & Objects

| Symbol                                             | Meaning                        | When / Why                                          | Tiny Example                                                                                           |
| -------------------------------------------------- | ------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| $\mathbf{x}\in\mathbb{R}^d,; t$                    | spatial coordinate, time       | state lives on lattice/continuum                    | probe field at walker location $x_w(t)$                                                                |
| $\boldsymbol{\phi}(\mathbf{x},t)\in\mathbb{R}^{C}$ | $C$-channel field stack (fast) | reaction–diffusion-like substrate                   | $\partial_t\boldsymbol{\phi}=\mathbf{D}\nabla^2\boldsymbol{\phi}+\mathbf{R}(\boldsymbol{\phi})+\cdots$ |
| $\mathcal{V}(\mathbf{x},t)$                        | “void” baseline scalar         | reference/energy-like background for gating         | prefer edits near $\mathcal{V}$ minima                                                                 |
| $\rho(\mathbf{x},t)$                               | activity density (saliency)    | cheap heatmap of local events                       | $\rho=\sum_w K_\sigma(\mathbf{x}-\mathbf{x}_w)$                                                        |
| $\mathcal{W}$                                      | set of walkers                 | local samplers/processors                           | $w\in\mathcal{W}$ carries state $s_w$                                                                  |
| $s_w$                                              | walker state tuple             | $(\mathbf{x}_w,\mathbf{v}_w,\theta_w,q_w,\kappa_w)$ | position, motion, phase, tag, channel key                                                              |
| $\mathbf{u}(t)$                                    | external input stream          | drives the substrate / sensors                      | inject to bus $\mathcal{B}_0$                                                                          |

## Discrete Lattice → Continuum (RD) Mapping

| Symbol            | Meaning                         | When / Why                         | Tiny Example                                                                          |   |                          |
| ----------------- | ------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------- | - | ------------------------ |
| $W_i(t)$          | node state at site $i$          | base discrete walker density       | $\dot W_i = (\alpha-\beta)W_i - \alpha W_i^2 + J!\sum_{j\in\mathrm{nbr}(i)}(W_j-W_i)$ |   |                          |
| $\mathrm{nbr}(i)$ | neighbor set | coordination $z=\lvert \mathrm{nbr}(i)\rvert$ | enters diffusion mapping |
| $J$               | diffusive coupling              | hopping strength between sites     | maps to continuum $D$                                                                 |   |                          |
| $a$               | lattice spacing                 | coarse cell size                   | enters $D$ and $c^2$                                                                  |   |                          |
| $D$               | continuum diffusion coefficient | $D = J a^2$ or $D=\tfrac{J}{z}a^2$ | RD term $D\nabla^2\phi$                                                               |   |                          |
| $\alpha,\beta$    | on-site creation/loss rates     | $r=\alpha-\beta,\ u=\alpha$        | sets logistic parameters                                                              |   |                          |
| $r,u$             | RD growth/saturation            | linear and quadratic terms         | $\partial_t\phi=D\nabla^2\phi+r\phi-u\phi^2$                                          |   |                          |
| $Q(W,t)$          | logarithmic first integral      | invariant of on-site logistic      | $Q=\ln!\frac{W}{r-uW}-rt=\text{const}$ (drift guard)                                  |   |                          |
| $\Delta Q$        | change in conserved quantity    | discrete time evolution            | $\Delta Q_i = Q_i(t+\Delta t) - Q_i(t)$                                                |   |                          |
| $\Delta W$        | change in node state            | discrete update                    | $\Delta W_i = W_i(t+\Delta t) - W_i(t)$                                                |   |                          |
| $\Delta t$        | discrete time step              | temporal discretization            | enter CFL stability conditions                                                         |   |                          |
| $N(i)$            | neighbor set of node $i$        | graph connectivity                 | $N(i) = \mathrm{nbr}(i)$ for lattice                                                   |   |                          |
| $F(W)$            | discrete dynamics function      | RHS of discrete ODE                | $F(W)=(\alpha-\beta)W-\alpha W^2$                                                      |   |                          |
| $H_{ij}$          | discrete flux $i \to j$         | conserved-quantity transport       | $\Delta Q_i = \sum_j (H_{ji} - H_{ij})$                                                |   |                          |
| $c_k$             | flux ansatz coefficients        | parameterize $H_{ij}$              | $H_{ij}=\sum_k c_k W_i^{a_k} W_j^{b_k}$                                                |   |                          |

## Scalar EFT (Tachyon, Quartic $\phi^4$, Masses)

| Symbol                              | Meaning                 | When / Why                    | Tiny Example                                                                        |        |                         |
| ----------------------------------- | ----------------------- | ----------------------------- | ----------------------------------------------------------------------------------- | ------ | ----------------------- |
| $V(\phi)$                           | EFT potential energy    | symmetry breaking / stability | $V(\phi)=-\tfrac{1}{2}\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3$ |        |                         |
| $\mu^2>0$                           | tachyonic curvature     | drives condensation           | $V''(0)=-\mu^2<0$                                                                   |        |                         |
| $\lambda>0$                         | quartic stabilizer      | Mexican-hat shape             | minima at $\pm v$ with $v=\mu/\sqrt{\lambda}$                                       |        |                         |
| $\gamma$ | small cubic tilt | selects unique vacuum | $\lvert \gamma \rvert \ll \mu^2 \sqrt{\lambda}$ |
| $m_{\mathrm{eff}}^2$                | physical mass at vacuum | fluctuation spectrum          | $m_{\mathrm{eff}}^2=V''(v)=2\mu^2$                                                  |        |                         |
| $m_{\text{in}}^2, m_{\text{out}}^2$ | tube problem masses     | inside/outside background     | $m_{\text{in}}^2=-\mu^2,\ m_{\text{out}}^2=2\mu^2$                                  |        |                         |
| $c$                                 | wave propagation speed  | from lattice micro-params     | $c^2=2Ja^2$                                                                         |        |                         |
| $\Box$                              | d’Alembertian operator  | wave/field operator           | $\Box=\partial_t^2-c^2\nabla^2$; EFT EOM: $\Box\phi+V'(\phi)=0$                     |        |                         |
| $R$                                 | tube/cylinder radius    | boundary quantization scale   | finite-domain mode analysis                                                         |        |                         |

## Discrete Conservation Law & Energy Decomposition

| Symbol                    | Meaning                         | When / Why                          | Tiny Example                                                                      |
| ------------------------- | ------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------- |
| $\mathcal{H}_i$           | discrete Hamiltonian at node    | total energy density                | $\mathcal{H}_i = \mathcal{K}_i + V(W_i) + \mathcal{I}_i$                          |
| $\mathcal{K}_i$           | kinetic energy at node          | rate-of-change squared              | $\mathcal{K}_i = \tfrac{1}{2}(\dot{W}_i)^2 = \tfrac{1}{2}[F(W_i)]^2$             |
| $\mathcal{I}_i$           | interaction energy at node      | coupling to neighbors               | $\mathcal{I}i = \tfrac{1}{2}\sum{j \in N(i)} J, (W_j - W_i)^2$                   |
| $\vec{J}_i$               | energy flux vector from node    | discrete divergence in conservation | $\frac{\Delta \mathcal{H}_i}{\Delta t} + \nabla \cdot \vec{J}_i = 0$             |
| $\nabla \cdot$            | discrete divergence operator    | flux balance on graph               | sums net flow across edges                                                        |

## Walkers & Local Dynamics

| Symbol                      | Meaning                    | When / Why                         | Tiny Example                                          |
| --------------------------- | -------------------------- | ---------------------------------- | ----------------------------------------------------- |
| $\mathbf{x}_w(t)$           | walker position            | sample/report local state          | drift to gradients                                    |
| $\mathbf{v}_w(t)$           | walker velocity            | biased random/greedy motion        | $\mathbf{v}_w \propto -\nabla \Phi_k(\mathbf{x}_w,t)$ |
| $\pi_w$                     | local policy               | chooses step/update                | softmax/Gibbs over local scores                       |
| $m_w$                       | message/metric packet      | report to bus/scoreboard           | $m_w=(t,\mathbf{x}_w,f_w)$                            |
| $\Delta^{+}_{w,c}$          | sparse local patch edit    | plastic write to channel $c$       | $\phi_c!\leftarrow!\phi_c+\gamma_c\Delta^{+}_{w,c}$   |
| $\mathcal{N}_r(\mathbf{x})$ | neighborhood of radius $r$ | receptive field for sampling/edits | compact patch support                                 |

## Control Plane: Buses, Scoreboard & Gating

| Symbol                              | Meaning                  | When / Why                             | Tiny Example                                 |
| ----------------------------------- | ------------------------ | -------------------------------------- | -------------------------------------------- |
| $\mathcal{B}_{\ell}$                | bus at level $\ell$      | hierarchical I/O                       | pool $\downarrow$ / broadcast $\uparrow$     |
| $\mathcal{H}$                       | bus hierarchy            | $(\mathcal{B}_0,\ldots,\mathcal{B}_L)$ | coarse $\leftrightarrow$ fine control        |
| $\mathcal{A},,\oplus$               | aggregator, merge op     | reduce messages to stats               | $(\oplus_w m_w)$ per tile/time               |
| $\mathcal{S}(t)$                    | scoreboard state         | budgets, priorities, masks             | enforce sparsity & safety                    |
| $\mathbf{g}(t)\in\mathbb{R}^{K}$    | GDSP score vector        | global scores per objective            | top - $k$ targets                              |
| $\boldsymbol{\gamma}(\mathbf{x},t)$ | gating mask $\in[0,1]^C$ | channel/space control of writes        | apply: $\boldsymbol{\gamma}\odot\Delta^{+}$  |
| $B_k(t)$                            | budget for objective $k$ | quota / rate-limit for edits           | $B_k!\leftarrow!B_k-\text{cost}(\Delta^{+})$ |
| $\tau_k$                            | gate threshold           | pass/fail for edits                    | pass if score $\ge \tau_k$                   |
| $\mathcal{C}$                       | constraint set           | safety/consistency rules               | forbids conflicting edits                    |

## Memory Steering & Plasticity (Slow Bias)

| Symbol                           | Meaning                           | When / Why                  | Tiny Example                                             |
| -------------------------------- | --------------------------------- | --------------------------- | -------------------------------------------------------- |
| $\boldsymbol{\mu}(\mathbf{x},t)$ | memory-steering field (slow)      | biases fast rules safely    | multiplies/tweaks reaction term                          |
| $\alpha_{\text{plast}}$ | plasticity scale cap | limits write magnitude | $\lVert \Delta^{+} \rVert \le \alpha_{\text{plast}}$ |
| $\epsilon$                       | time-scale ratio ($\epsilon\ll1$) | separates slow/fast layers  | $\partial_t\boldsymbol{\mu}=\epsilon,\mathcal{F}(\cdot)$ |
| $\mathcal{P}$                    | plasticity policy                 | chooses edit & kernel shape | pick channel $c$, kernel width                           |
| $\mathcal{J},,R_t$               | objective, reward                 | steer toward useful memory  | $\mathcal{J}=\sum_t\gamma^t R_t$                         |

## Global Controllers (SIE / ADC)

| Symbol         | Meaning                      | When / Why                        | Tiny Example                                                                              |
| -------------- | ---------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------- |
| $\mathrm{SIE}$ | Self Improvement Engine      | global self-evaluation and tuning | computes $\mathbf{g}(t)$, updates $B_k$, refines $\pi_w$, adjusts $\alpha_{\text{plast}}$ |
| $\mathrm{ADC}$ | Adaptive Domain Cartographer | maps objectives to domains        | sets $\boldsymbol{\gamma}$, selects targets, chooses $\mathcal{N}_r$                      |

## Field Dynamics & Potentials

| Symbol                          | Meaning                       | When / Why                       | Tiny Example                                                                                                             |
| ------------------------------- | ----------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| $\mathbf{R}(\boldsymbol{\phi})$ | reaction (on-site) term       | local rule family                | $R_c=r_c,\phi_c!\left(1-\frac{\phi_c}{K_c}\right)$ (logistic)                                                            |
| $\mathbf{D}$                    | diffusion tensor              | $\mathrm{diag}(D_c)$ per-channel | $D_c\nabla^2\phi_c$                                                                                                      |
| $\Phi_c(\phi_c)$                | potential energy per channel  | stability/saturation             | quartic: $\Phi_c=\tfrac{\lambda_c}{4}(\phi_c^2-v_c^2)^2$                                                                 |
| $-\Phi_c'$                      | potential force               | gradient flow / regularization   | $-\Phi_c'=-\lambda_c\phi_c(\phi_c^2-v_c^2)$                                                                              |
| $\Phi_c^{\text{stab}}$          | quartic stabilizer (no break) | soft amplitude clipping          | $\Phi_c^{\text{stab}}=\tfrac{\lambda_c}{4}\phi_c^4$                                                                      |
| $\star$                         | full fast step                | compose physics + edits          | $\phi_c^{t+\Delta t}=\phi_c^t+D_c\nabla^2\phi_c,\Delta t+R_c,\Delta t-\Phi_c',\Delta t+\gamma_c!\sum_w!\Delta^{+}_{w,c}$ |

## Dimensionless Groups — VDM Control & Stability

| Symbol        | Meaning                     | When / Why                              | Tiny Example                     |
| ------------- | --------------------------- | --------------------------------------- | -------------------------------- |
| $\mathcal{D}$ | void debt number            | unresolved debt / resolved flux         | “information Reynolds”           |
| $\Xi$         | coupling ratio              | $g_{\text{void}}/\gamma_{\text{relax}}$ | phase-lock threshold             |
| $M_v$         | void Mach number            | $J_{\text{void}}/c_{\text{signal}}$     | stability requires $M_v<1$       |
| $\Sigma$      | symmetry debt ratio         | broken-symmetry / conserved flux        | regime classifier                |
| $\Lambda$     | dispersion / convergence    | exploration vs consolidation            | boundary $\sim 1$                |
| $\Theta$      | junction gate strength      | scale in $\Theta,\Delta m$              | e.g. $k!\approx!1,\ b!\approx!0$ |
| $\Gamma$      | retention fraction          | memory persistence                      | $0.3$ – $0.75$                     |
| $D_a$         | anisotropic diffusion index | transport anisotropy class              | ${1,3,5,7}$ discrete             |
| $\kappa L$ | curvature $\times$ scale | path bending measure | compare to $\Theta\lVert \nabla m\rVert$ |
| $g$           | void gain                   | stabilization / bias strength           | e.g. $0.5$                       |
| $\kappa$      | sparsity ratio              | edits per DOF per step                  | keep $\kappa\ll1$                |

## Dimensionless Groups — RD Systems

| Symbol      | Meaning                | When / Why                | Tiny Example                        |
| ----------- | ---------------------- | ------------------------- | ----------------------------------- |
| $\Pi_{Dr}$  | diffusion at scale $L$ | $D/(rL^2)$                | pick $L$ per experiment             |
| $c^*$       | normalized KPP speed   | $c/(2\sqrt{Dr})$          | $\approx 0.95\text{–}1.0$ when validated |
| \mathrm{Da} | Damköhler number       | reaction / transport rate | regime classifier                   |

## Dimensionless Groups — LBM / Fluids

| Symbol      | Meaning             | When / Why                                    | Tiny Example                     |
| ----------- | ------------------- | --------------------------------------------- | -------------------------------- |
| $\tau$      | BGK relaxation time | controls viscosity                            | $\tau>0.5$                       |
| $\nu$       | kinematic viscosity | $\tfrac{1}{3}!\left(\tau-\tfrac{1}{2}\right)$ | e.g. $\nu=0.1333$ for $\tau=0.9$ |
| $c_s$       | lattice sound speed | model constant                                | $1/\sqrt{3}$                     |
| \mathrm{Re} | Reynolds number     | $UL/\nu$                                      | inertia vs viscosity             |
| \mathrm{Ma} | Mach number         | $U/c_s$                                       | keep $\ll 1$ for incompressible  |
| \mathrm{Pe} | Péclet number       | $UL/D$                                        | advection vs diffusion           |

## Diagnostics & Data Products

| Symbol                | Meaning                      | When / Why                    | Tiny Example                                          |
| --------------------- | ---------------------------- | ----------------------------- | ----------------------------------------------------- |
| $H_k(\mathbf{x},t)$ | heatmap for metric $k$ | visualize activity/flow | $H_k=\sum_w K_\sigma(\mathbf{x}-\mathbf{x}w),f{w,k}$ |
| $\Pi_c(t)$ | channel utilization | budget/throughput per channel | $\Pi_c=\sum_w \lVert \Delta^{+}*{w,c}\rVert$ |
| $\mathrm{KDE}*\sigma$ | kernel density estimate | smooth sparse events | choose $\sigma$ per scale |
| $\Lambda(t)$ | first-integral drift monitor | sanity check (logistic) | $\Lambda=\lVert I_{\log}(\phi,t)-I_{\log}(\phi,0)\rVert$ |

## Scales & Stability Conditions

| Symbol | Meaning           | When / Why                 | Tiny Example                                                 |
| ------ | ----------------- | -------------------------- | ------------------------------------------------------------ |
| $L,;T$ | space/time scales | units and stability limits | diffusive CFL: $\Delta t\le \tfrac{\Delta x^2}{2d,D_{\max}}$ |
