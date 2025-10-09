<!-- DOC-GUARD: CANONICAL -->
<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/units_normalization_maintenance.md -->
<!--markdownlint-disable MD033 MD001-->
# VDM Units & Nondimensionalization (Auto-compiled)

Last updated: 2025-10-09 (commit 09f871a)

**Scope:** Single source of truth for unit systems and nondimensionalization maps used in this repository.  
**Rules:** Other docs link here; do not restate units elsewhere.  
**MathJax:** GitHub-safe `$...$` / `$$...$$` only.

---

## 1) Base Unit Systems

- **System:** Nondimensional • **Scope:** VDM control parameters, dimensionless groups • **Source:** `derivation/CONSTANTS.md:10-14 • ec0833a`
  - **Notes:** Universal learning rates (ALPHA, BETA), reference frequency (F_REF), phase sensitivity (PHASE_SENS), CFL factors are declared nondimensional.

- **System:** LBM units (lattice units) • **Scope:** Fluid dynamics sector (LBM/BGK) • **Source:** `derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:3,106 • ec0833a`
  - **Notes:** Lattice Boltzmann Method with $dx = dt = 1$ in lattice units; $c_s^2 = 1/3$ for D2Q9; kinematic viscosity $\nu = c_s^2 (\tau - 0.5)$.

- **System:** Lattice units (RD sector) • **Scope:** Discrete reaction-diffusion models • **Source:** `derivation/EQUATIONS.md:640 • ec0833a`
  - **Notes:** Ring composite radius $R_* \approx 8.1$ (lattice units); discrete lattice spacing $a$ as fundamental scale.

- **System:** GeV (natural units) • **Scope:** EFT/Voxtrium mapping • **Source:** `derivation/effective_field_theory/fum_voxtrium_mapping.md:47-52 • ec0833a`
  - **Notes:** Natural units $c = \hbar = k_B = 1$; field dimension $[\phi] = \mathrm{GeV}$; Lagrangian density $[\mathcal{L}] = \mathrm{GeV}^4$ in $D=4$.

---

## 2) Reference Scales (only those present)

| Symbol | Meaning | Units/System | Source (path:lines • commit) | Notes |
|---|---|---|---|---|
| $a$ | Lattice spacing | length | derivation/SYMBOLS.md:24 • ec0833a | Coarse cell size; enters $D = J a^2$ and $c^2$ mappings |
| $L$ | Characteristic length scale | length | derivation/SYMBOLS.md:162 • ec0833a | Spatial scale for stability conditions and dimensionless groups |
| $T$ | Characteristic time scale | time | derivation/SYMBOLS.md:162 • ec0833a | Temporal scale for stability conditions |
| $c_s$ | Lattice sound speed | LBM velocity | derivation/SYMBOLS.md:144 • ec0833a | Model constant $c_s = 1/\sqrt{3}$ in D2Q9 |
| $D$ | Continuum diffusion coefficient | length²/time | derivation/SYMBOLS.md:25 • ec0833a | Mapped from lattice: $D = J a^2$ or $D = (J/z)a^2$ |
| $r$ | RD growth rate | 1/time | derivation/SYMBOLS.md:27 • ec0833a | Linear growth term: $r = \alpha - \beta$ |
| $u$ | RD saturation coefficient | 1/(time·conc) | derivation/SYMBOLS.md:27 • ec0833a | Quadratic saturation: $u = \alpha$ |
| $J$ | Discrete diffusive coupling | 1/time | derivation/SYMBOLS.md:23 • ec0833a | Hopping strength between lattice sites |
| $\tau$ | BGK relaxation time | time steps | derivation/SYMBOLS.md:142 • ec0833a | Controls LBM viscosity; $\tau > 0.5$ for stability |
| $\nu$ | Kinematic viscosity | length²/time | derivation/SYMBOLS.md:143 • ec0833a | LBM: $\nu = \frac{1}{3}(\tau - \frac{1}{2})$ |
| $\phi_0$ | Field scale (EFT) | GeV | derivation/effective_field_theory/fum_voxtrium_mapping.md:50 • ec0833a | Dimensionalization: $\phi_{\mathrm{dimless}} = \phi_{\mathrm{phys}}/\phi_0$ |
| $\tau_{\mathrm{scale}}$ | Time scale (EFT) | GeV⁻¹ | derivation/effective_field_theory/fum_voxtrium_mapping.md:51 • ec0833a | EFT dimensionalization: $t_{\mathrm{dimless}} = t_{\mathrm{phys}}/\tau_{\mathrm{scale}}$ |
| $M_0$ | Memory field scale | dimensionless | derivation/memory_steering/memory_steering.md:59 • ec0833a | Characteristic memory strength for normalization |
| $R_0$ | Usage field scale | dimensionless | derivation/memory_steering/memory_steering.md:59 • ec0833a | Characteristic usage/co-activation scale |

---

## 3) Nondimensionalization Maps (forward & inverse)

##### LBM Lattice Units → Physical Units

**Context:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:3,106 • ec0833a

$$
\Delta x_{\mathrm{lattice}} = 1, \quad \Delta t_{\mathrm{lattice}} = 1, \quad c_s = \frac{1}{\sqrt{3}}
$$

$$
\nu_{\mathrm{lattice}} = \frac{1}{3}\left(\tau - \frac{1}{2}\right)
$$

**Related:** Dimensionless numbers computed in lattice units: [Re](#re-lbm), [Ma](#ma-lbm), [Pe](#pe-lbm).

---

##### Discrete Lattice → Continuum (RD)

**Context:** derivation/SYMBOLS.md:23-27; derivation/foundations/continuum_stack.md:29,36 • ec0833a

$$
D = J a^2 \quad \text{(site Laplacian)}
$$

$$
D = \frac{J}{z} a^2 \quad \text{(neighbor-average form)}
$$

$$
r = \alpha - \beta, \quad u = \alpha
$$

**Inverse:** Not explicitly stated; mapping is lattice → continuum only.

**Related:** Discrete RDE: [VDM-E-019](../derivation/EQUATIONS.md#vdm-e-019); Continuum RDE: [VDM-E-020](../derivation/EQUATIONS.md#vdm-e-020).

---

##### Dimensionless RD Rescaling

**Context:** derivation/foundations/continuum_stack.md:74 • ec0833a

$$
x \to \frac{x}{L}, \quad t \to \frac{t}{T}
$$

**Notes:** Choose $L$ and $T$ to set desired scales for $D$ and $r$; used in experiments to report dimensionless groups $\Pi_{Dr} = D/(rL^2)$.

---

##### Agency Field Dimensionless Form

**Context:** derivation/EQUATIONS.md:81-87 • ec0833a

$$
\tilde{t} = \gamma t, \quad \tilde{x} = \frac{x}{\ell_D}, \quad \ell_D = \sqrt{\frac{D}{\gamma}}
$$

**Inverse:**

$$
t = \frac{\tilde{t}}{\gamma}, \quad x = \ell_D \, \tilde{x}
$$

**Related:** Agency field equation [VDM-E-007](../derivation/EQUATIONS.md#vdm-e-007).

---

##### EFT Dimensionalization (FUM → Voxtrium)

**Context:** derivation/effective_field_theory/fum_voxtrium_mapping.md:54-80 • ec0833a

$$
\phi_{\mathrm{dimless}} = \frac{\phi_{\mathrm{phys}}}{\phi_0}, \quad t_{\mathrm{dimless}} = \frac{t_{\mathrm{phys}}}{\tau_{\mathrm{scale}}}, \quad x_{\mathrm{dimless}} = \frac{x_{\mathrm{phys}}}{a}
$$

**Inverse:**

$$
\phi_{\mathrm{phys}} = \phi_0 \, \phi_{\mathrm{dimless}}, \quad t_{\mathrm{phys}} = \tau_{\mathrm{scale}} \, t_{\mathrm{dimless}}, \quad x_{\mathrm{phys}} = a \, x_{\mathrm{dimless}}
$$

**Physical parameters:**

$$
c_{\mathrm{void}}^2 = \frac{D a^2}{\tau_{\mathrm{scale}}^2}, \quad g_3 = \frac{\alpha}{\phi_0 \tau_{\mathrm{scale}}^2} \, [\mathrm{GeV}], \quad m^2 = \frac{\alpha - \beta}{\tau_{\mathrm{scale}}^2} \, [\mathrm{GeV}^2]
$$

**Vacuum and mass:**

$$
v_{\mathrm{phys}} = \phi_0 \left(1 - \frac{\beta}{\alpha}\right), \quad m_{\mathrm{eff}} = \frac{\sqrt{\alpha - \beta}}{\tau_{\mathrm{scale}}}
$$

**Related:** EFT potential $V(\phi)$ in [effective_field_theory_approach.md](../derivation/effective_field_theory/effective_field_theory_approach.md).

---

##### Memory Steering Field Normalization

**Context:** derivation/memory_steering/memory_steering.md:59 • ec0833a

$$
m = \frac{M}{M_0}, \quad \rho = \frac{R}{R_0}
$$

**Notes:** Dimensionless memory field $m$ and usage proxy $\rho$ normalized by characteristic scales.

**Related:** Memory steering equations in [memory_steering.md](../derivation/memory_steering/memory_steering.md).

---

## 4) Per-Quantity Units (as used)

| Quantity (link to symbol)                                     | Units/System   | Where Stated                                               | Notes                                                        |
| ------------------------------------------------------------- | -------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| $\alpha$<sup>[↗](../derivations/SYMBOLS.md#sym-alpha)</sup>   | nondimensional | derivation/CONSTANTS.md:10 • ec0833a                       | Universal learning rate ALPHA = 0.25                         |
| $\beta$<sup>[↗](../derivations/SYMBOLS.md#sym-beta)</sup>     | nondimensional | derivation/CONSTANTS.md:11 • ec0833a                       | Universal plasticity rate BETA = 0.1                         |
| $c_s^2$<sup>[↗](../derivations/SYMBOLS.md#sym-cs)</sup>       | LBM units      | derivation/CONSTANTS.md:12 • ec0833a                       | CS2 = 1/3 in D2Q9 lattice                                    |
| $D$<sup>[↗](../derivations/SYMBOLS.md#sym-D)</sup>            | length²/time   | derivation/CONSTANTS.md:15-17 • ec0833a                    | Diffusion coefficients: D = 1.0, 0.5, 0.25 in RD experiments |
| $r$<sup>[↗](../derivations/SYMBOLS.md#sym-r)</sup>            | 1/time         | derivation/CONSTANTS.md:16-18 • ec0833a                    | Growth rates: r = 0.25, 0.5, 1.0 in RD experiments           |
| $N$<sup>[↗](../derivations/SYMBOLS.md#sym-N)</sup>            | sites          | derivation/CONSTANTS.md:19 • ec0833a                       | Grid resolution: 256, 512, 1024                              |
| $\tau$<sup>[↗](../derivations/SYMBOLS.md#sym-tau)</sup>       | time steps     | derivation/CONSTANTS.md:29-31 • ec0833a                    | BGK relaxation: 0.8, 0.9, 1.0 (LBM)                          |
| $U$<sup>[↗](../derivations/SYMBOLS.md#sym-U)</sup>            | LBM velocity   | derivation/CONSTANTS.md:36,38 • ec0833a                    | Lid velocity 0.1; Taylor-Green amplitude 0.05                |
| $\nu$<sup>[↗](../derivations/SYMBOLS.md#sym-nu)</sup>         | lattice units  | derivation/code/common/dimensionless_vdm.py:17 • ec0833a | Computed from $\tau$: $\nu = (\tau - 0.5)/3$                 |
| $g$<sup>[↗](../derivations/SYMBOLS.md#sym-g)</sup>            | nondimensional | derivation/CONSTANTS.md:42,53 • ec0833a                    | Void gain: 0.5 (lid cavity), 0.12 (memory steering)          |
| $\Theta$<sup>[↗](../derivations/SYMBOLS.md#sym-Theta)</sup>   | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:21 • ec0833a         | Junction gate strength; fit scale parameter                  |
| $\Lambda$<sup>[↗](../derivations/SYMBOLS.md#sym-Lambda)</sup> | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:22 • ec0833a         | Exploration/retention ratio; dispersion-to-convergence       |
| $\Gamma$<sup>[↗](../derivations/SYMBOLS.md#sym-Gamma)</sup>   | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:23 • ec0833a         | Retention fraction; memory persistence ~0.3-0.75             |
| $D_a$<sup>[↗](../derivations/SYMBOLS.md#sym-Da)</sup>         | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:24 • ec0833a         | Anisotropic diffusion index: {1, 3, 5, 7} discrete           |
| $V_{\text{useful\_bits}}$<sup>[↗](../derivations/SYMBOLS.md#sym-V-useful)</sup> | bits          | derivation/EQUATIONS.md:VDM-E-083,VDM-E-084 • HEAD | Useful reachable entropy; operational agency capacity |
| $E$<sup>[↗](../derivations/SYMBOLS.md#sym-E)</sup>                                | steps         | derivation/EQUATIONS.md:VDM-E-081 • HEAD           | Discrete action/energy budget used by the probe       |
| $p_{\text{slip}}$<sup>[↗](../derivations/SYMBOLS.md#sym-p-slip)</sup>            | 1 (prob.)     | derivation/EQUATIONS.md:VDM-E-081 • HEAD           | Per-step actuator slip probability in $[0,1]$         |
| $G_E$<sup>[↗](../derivations/SYMBOLS.md#sym-GE-Gp)</sup>                          | bits/step     | derivation/EQUATIONS.md:VDM-E-081 • HEAD           | Sensitivity $\partial_E V$ (finite-difference)        |
| $G_p$<sup>[↗](../derivations/SYMBOLS.md#sym-GE-Gp)</sup>                          | bits/(unit slip) | derivation/EQUATIONS.md:VDM-E-081 • HEAD        | Sensitivity $\partial_{p_{\text{slip}}} V$ (FD)       |
| $\epsilon_E$<sup>[↗](../derivations/SYMBOLS.md#sym-elasticities)</sup>            | nondimensional | derivation/EQUATIONS.md:VDM-E-082 • HEAD          | Elasticity $\dfrac{E}{V}\partial_E V$ (when $V>0$)    |
| $\epsilon_p$<sup>[↗](../derivations/SYMBOLS.md#sym-elasticities)</sup>            | nondimensional | derivation/EQUATIONS.md:VDM-E-082 • HEAD          | Elasticity $\dfrac{p_{\text{slip}}}{V}\partial_{p}V$ (when $V>0$) |
| $E_{\min}^{(v_0)}$<sup>[↗](../derivations/SYMBOLS.md#sym-Emin-v0)</sup>          | steps         | derivation/EQUATIONS.md:VDM-E-083 • HEAD           | Minimal budget to reach $V\!\ge\!v_0$ at slip $p$     |
| $n_{\text{act}}$<sup>[↗](../derivations/SYMBOLS.md#sym-n-act)</sup>               | actuators     | derivation/CONSTANTS.md:§Agency • HEAD             | Actuator count used in the probe context              |

---

## 5) Dimensionless Numbers (unit statements only)

| Name | Unit Status / Normalization Note | Appears In | Source |
|---|---|---|---|
| <a id="re-lbm"></a>$\mathrm{Re}$ (Reynolds) | Nondimensional; $\mathrm{Re} = UL/\nu$ in LBM units | LBM benchmarks | derivation/SYMBOLS.md:145; derivation/DIMENSIONLESS_CONSTANTS.md:17 • ec0833a |
| <a id="ma-lbm"></a>$\mathrm{Ma}$ (Mach) | Nondimensional; $\mathrm{Ma} = U/c_s$ in LBM units | LBM benchmarks | derivation/SYMBOLS.md:146; derivation/DIMENSIONLESS_CONSTANTS.md:18 • ec0833a |
| <a id="pe-lbm"></a>$\mathrm{Pe}$ (Péclet) | Nondimensional; $\mathrm{Pe} = UL/D$ | RD-fluid coupling | derivation/SYMBOLS.md:147; derivation/code/common/dimensionless_vdm.py:29 • ec0833a |
| <a id="pi-dr"></a>$\Pi_{Dr}$ | Nondimensional; $\Pi_{Dr} = D/(rL^2)$ at chosen scale $L$ | RD experiments | derivation/SYMBOLS.md:134; derivation/DIMENSIONLESS_CONSTANTS.md:19 • ec0833a |
| <a id="c-star"></a>$c^*$ | Nondimensional; $c^* = c/(2\sqrt{Dr})$ normalized KPP speed | RD front speed | derivation/SYMBOLS.md:135; derivation/CONSTANTS.md:129 • ec0833a |
| <a id="da-damkohler"></a>$\mathrm{Da}$ (Damköhler) | Nondimensional; reaction/transport rate ratio | RD regime classification | derivation/SYMBOLS.md:136; derivation/code/common/dimensionless_vdm.py:33 • ec0833a |
| <a id="void-debt"></a>$\mathcal{D}$ (Void Debt) | Nondimensional; unresolved debt / resolved flux | VDM control | derivation/SYMBOLS.md:118; derivation/DIMENSIONLESS_CONSTANTS.md:30 • ec0833a |
| <a id="xi"></a>$\Xi$ (Coupling Ratio) | Nondimensional; $\Xi = g_{\mathrm{void}}/\gamma_{\mathrm{relax}}$ | VDM control | derivation/SYMBOLS.md:119; derivation/DIMENSIONLESS_CONSTANTS.md:38 • ec0833a |
| <a id="m-void"></a>$M_v$ (Void Mach) | Nondimensional; $M_v = J_{\mathrm{void}}/c_{\mathrm{signal}}$; require $M_v < 1$ | VDM stability | derivation/SYMBOLS.md:120; derivation/DIMENSIONLESS_CONSTANTS.md:64 • ec0833a |
| <a id="sigma"></a>$\Sigma$ (Symmetry Debt) | Nondimensional; broken-symmetry / conserved flux | VDM regime | derivation/SYMBOLS.md:121; derivation/DIMENSIONLESS_CONSTANTS.md:89 • ec0833a |
| <a id="lambda-disp"></a>$\Lambda$ (Dispersion) | Nondimensional; dispersion / convergence (Lyapunov-like) | VDM control | derivation/SYMBOLS.md:122; derivation/DIMENSIONLESS_CONSTANTS.md:97 • ec0833a |
| <a id="theta"></a>$\Theta$ (Junction Gate) | Nondimensional; junction gate strength | Memory steering | derivation/SYMBOLS.md:123; derivation/DIMENSIONLESS_CONSTANTS.md:77 • ec0833a |
| <a id="gamma-ret"></a>$\Gamma$ (Retention) | Nondimensional; memory persistence fraction | Memory steering | derivation/SYMBOLS.md:124; derivation/DIMENSIONLESS_CONSTANTS.md:23 • ec0833a |
| <a id="kappa-l"></a>$\kappa L$ | Nondimensional; curvature × scale (path bending) | Memory steering | derivation/SYMBOLS.md:126; derivation/DIMENSIONLESS_CONSTANTS.md:25 • ec0833a |
| <a id="si"></a>$\mathrm{Si}$ (Steering) | Nondimensional; $\mathrm{Si} = \Theta \|\nabla m\| / \lambda$ | Memory steering | derivation/code/common/dimensionless_vdm.py:48 • ec0833a |
| <a id="pi-void"></a>$\Pi_{\mathrm{void}}$ | Nondimensional; $\Pi_{\mathrm{void}} = (\Lambda \cdot \Theta)/\Gamma$ | Void reorganization | derivation/code/common/dimensionless_vdm.py:52 • ec0833a |

---

<!-- BEGIN AUTOSECTION: UNITS-INDEX -->
<!-- Tool-maintained list of anchors for quick lookup -->

**Quick Index:**

- [LBM Lattice Units](#lbm-lattice-units--physical-units)
- [Discrete Lattice → Continuum (RD)](#discrete-lattice--continuum-rd)
- [Dimensionless RD Rescaling](#dimensionless-rd-rescaling)
- [Agency Field Dimensionless Form](#agency-field-dimensionless-form)
- [EFT Dimensionalization](#eft-dimensionalization-fum--voxtrium)
- [Memory Steering Normalization](#memory-steering-field-normalization)
- [Reynolds Number (Re)](#re-lbm)
- [Mach Number (Ma)](#ma-lbm)
- [Péclet Number (Pe)](#pe-lbm)
- [Dimensionless Diffusion (Π_Dr)](#pi-dr)
- [Normalized KPP Speed (c*)](#c-star)
- [Damköhler Number (Da)](#da-damkohler)
- [Void Debt (D)](#void-debt)
- [Coupling Ratio (Ξ)](#xi)
- [Void Mach (M_v)](#m-void)
- [Symmetry Debt (Σ)](#sigma)
- [Dispersion (Λ)](#lambda-disp)
- [Junction Gate (Θ)](#theta)
- [Retention (Γ)](#gamma-ret)
- [Curvature Scale (κL)](#kappa-l)
- [Steering Number (Si)](#si)
- [Void Reorganization (Π_void)](#pi-void)

<!-- END AUTOSECTION: UNITS-INDEX -->

## Change Log

- 2024-10-03 • Initial compilation from repository sources • ec0833a
