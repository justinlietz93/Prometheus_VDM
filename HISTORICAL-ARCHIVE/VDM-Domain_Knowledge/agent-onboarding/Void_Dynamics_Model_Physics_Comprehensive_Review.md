# Void Dynamics Model Physics: Comprehensive Review

**Author:** Justin K. Lietz  
**Date:** September 5, 2025  

## 1. Overview and Core Principles

The Void Dynamics Model (VDM) is a theoretical framework that bridges discrete neural network dynamics with continuum field theories. It posits that macroscopic physical phenomena emerge from microscopic information processing in neural substrates. The model is built on several core principles:

- **Discrete-to-Continuum Mapping**: Microscopic node states $W_i(t)$ map to a continuum field $\phi(\vec{x}, t)$ via local averaging.
- **Reaction-Diffusion as Canonical**: First-order time dynamics described by reaction-diffusion PDEs form the validated baseline.
- **Effective Field Theory Framework**: Second-order Lorentz-invariant dynamics provide a rigorous foundation for future work.
- **Units Rigor**: All quantities are dimensionally consistent, with explicit mappings to physical scales (GeV).

### Key Mathematical Structures
- **Discrete Node Dynamics**:
  $$
  \frac{dW_i}{dt} = (\alpha - \beta) W_i - \alpha W_i^2 + J \sum_{j \in N(i)} (W_j - W_i)
  $$
- **Continuum Field Definition**:
  $$
  \phi(\vec{x}_i, t) \equiv \frac{1}{|N(i)| + 1} \sum_{j \in \{i\} \cup N(i)} W_j(t)
  $$

## 2. Reaction-Diffusion: The Canonical Model

The primary continuum limit derived from the discrete dynamics is the reaction-diffusion equation:

$$
\partial_t \phi = D \nabla^2 \phi + r \phi - u \phi^2
$$

### Parameter Mapping
- **Diffusion Coefficient**: $D = J a^2$ (per-site coupling) or $D = (J/z) a^2$ (neighbor-averaged)
- **Growth Rate**: $r = \alpha - \beta$
- **Saturation Coefficient**: $u = \alpha$

### Fixed Points and Stability
- **Trivial Fixed Point**: $\phi = 0$ (unstable for $r > 0$)
- **Non-trivial Fixed Point**: $\phi^* = r/u = 1 - \beta/\alpha$ (stable for $r > 0$)
- **Linear Stability Analysis**:
  - Around $\phi = 0$: $\sigma(k) = r - D k^2$
  - Around $\phi^*$: $\sigma(k) = -r - D k^2$

### Validation Results
- **Dispersion Relation**: Confirmed $\sigma(k) = r - D k^2$ with median relative error $\leq 2 \times 10^{-3}$ and $R^2 \geq 0.999$
- **Front Speed**: Fisher-KPP speed $c_{\text{front}} = 2\sqrt{D r}$ validated with $|c_{\text{meas}} - c_{\text{th}}| / c_{\text{th}} \leq 6\%$ and $R^2 \geq 0.9999$

## 3. Effective Field Theory Approach

While the RD model is canonical, an Effective Field Theory (EFT) framework provides a more rigorous foundation for future extensions. The EFT is derived from a discrete action principle.

### Discrete Lagrangian
$$
L^n = a^d \sum_i \left[ \frac{1}{2} \left( \frac{W_i^{n+1} - W_i^n}{\Delta t} \right)^2 - \frac{\kappa}{2} \sum_{\mu=1}^d (W_{i+\mu}^n - W_i^n)^2 - V(W_i^n) \right]
$$

### Continuum Limit
- **Kinetic Term**: $\frac{1}{2} (\partial_t \phi)^2$
- **Spatial Gradient Term**: $J a^2 (\nabla \phi)^2$ with $c^2 = 2 J a^2$
- **Potential**: $V(\phi) = \frac{\alpha}{3} \phi^3 - \frac{\alpha - \beta}{2} \phi^2$

### Euler-Lagrange Equation
$$
\partial_t^2 \phi - c^2 \nabla^2 \phi + V'(\phi) = 0
$$
where $V'(\phi) = \alpha \phi^2 - (\alpha - \beta) \phi$.

### Bounded EFT Baseline
To ensure boundedness, a symmetric quartic potential is adopted:
$$
V(\phi) = -\frac{1}{2} \mu^2 \phi^2 + \frac{\lambda}{4} \phi^4
$$
- **Vacuum Expectation Value**: $v = \mu / \sqrt{\lambda}$
- **Effective Mass**: $m_{\text{eff}} = \sqrt{2} \mu$

A small cubic tilt $\gamma \phi^3/3$ maps to the original parameters:
- $\mu^2 \leftrightarrow \alpha - \beta$
- $\gamma \leftrightarrow \alpha$

## 4. Memory Steering Principles

Memory steering introduces a refractive index model where neural activity modulates information propagation.

### Refractive Index Model
- **Index Definition**: $n = \exp(\eta M)$
- **Ray Curvature**: $\vec{r}'' = \eta \nabla_\perp M$
- **Memory Dynamics**: $\partial_t M = \gamma R - \delta M + \kappa \nabla^2 M$

### Dimensionless Groups
- **Steering Number**: $\Theta = \eta \gamma R_0 L^2 / c_0$
- **Damköhler Number**: $D_a = \gamma R_0 / \delta$
- **Diffusion Number**: $\Lambda = \kappa / (\delta L^2)$
- **Attenuation Number**: $\Gamma = \alpha L / c_0$

### Graph Discretization
- **Transition Probabilities**: $p_{ij} \propto \exp(-\beta E_{ij})$ with softmax normalization
- **Energy Function**: $E_{ij} = \| \vec{x}_j - \vec{x}_i \| / n(\vec{x}_i)$

## 5. Fluid Dynamics Foundations

The VDM exhibits fluid-like behavior in certain limits, validated via Lattice Boltzmann Method (LBM) simulations.

### Navier-Stokes Limit
- **Operational Reduction**: D2Q9 BGK LBM converges to Navier-Stokes with viscosity $\nu = c_s^2 (\tau - \Delta t/2)$
- **Structural Reduction**: Conserved fields (mass, momentum) and Newtonian closure

### Validation Benchmarks
- **Taylor-Green Vortex**: Viscous decay fit with $|\nu_{\text{fit}} - \nu_{\text{th}}| / \nu_{\text{th}} \leq 5\%$
- **Lid-Driven Cavity**: Divergence constraint $\max \| \nabla \cdot \vec{v} \|_2 \leq 10^{-6}$

### Void-Walker Announcers
- **Passive Observability**: Non-intrusive measurement of fluid properties
- **Petition Types**: Saturation (`sat`), gradient (`grad`), shear (`shear`)

## 6. Conservation Laws and Symmetries

### Discrete Conservation
- **On-site Invariant**: $Q_i = \frac{1}{2} W_i^2$ (approximately conserved)
- **Global Invariant**: $\sum_i Q_i$ (drift $\leq 10^{-8}$ per step with guards)

### Symmetry Analysis
- **Time Translation**: Energy-like quantity derived from Noether's theorem
- **Spatial Translation**: Momentum-like quantity
- **Scale Invariance**: Emerging in critical regimes

### Lyapunov Functionals
- **For RD Systems**: Minimization of free energy functionals
- **For EFT**: Action principles with conserved charges

## 7. Units and Dimensional Analysis

### Physical Units Map
- **Field Scale**: $\phi_0$ [GeV]
- **Time Scale**: $\tau$ [GeV$^{-1}$]
- **Length Scale**: $a$ [GeV$^{-1}$]

### Dimensionful Equations
- **RD Equation**:
  $$
  \partial_t \phi = D \nabla^2 \phi + r \phi - u \phi^2
  $$
  with $D = J a^2$, $r = (\alpha - \beta)/\tau$, $u = \alpha/(\phi_0 \tau)$

- **EFT Equation**:
  $$
  \partial_t^2 \phi - c^2 \nabla^2 \phi + g_3 \phi^2 - m^2 \phi = 0
  $$
  with $c^2 = 2 J a^2$, $g_3 = \alpha/(\phi_0 \tau^2)$, $m^2 = (\alpha - \beta)/\tau^2$

### Worked Example
For $\alpha = 0.25$, $\beta = 0.10$, $m_{\text{eff}} = 1$ GeV:
- $\tau = \sqrt{\alpha - \beta}/m_{\text{eff}} \approx 0.3873$ GeV$^{-1}$
- $\phi_0 = \alpha/(g_3 \tau^2)$ with $g_3 = 0.1$ GeV gives $\phi_0 \approx 16.67$ GeV
- $v_{\text{phys}} = \phi_0 (1 - \beta/\alpha) \approx 10.00$ GeV

## 8. Integration with Voxtrium Framework

The VDM integrates with the Voxtrium macro-sourcing framework via a rigorous units map and causal kernels.

### Causal Retarded Kernels
- **Source Term**: $J_\phi(x,t) = \int d^3x' \int_{-\infty}^t dt' K_{\text{ret}}(t - t', |x - x'|) s_{\text{loc}}(x', t')$
- **Kernel Support**: $K_{\text{ret}} \propto \Theta(t - t' - |x - x'|/c)$

### Action-Level Embedding
$$
S_{\text{eff}} = \int d^4x \sqrt{-g} \left[ \frac{M_{\text{Pl}}^2}{2} R + \frac{1}{2} (\partial \phi)^2 - V(\phi) \right] + S_{\text{hor}} + S_{\text{DM}} + \cdots
$$

### Transfer Current
- **Covariant Conservation**: $\nabla_\mu (T_\phi^{\mu\nu} + T_{\text{hor}}^{\mu\nu} + T_{\text{DM}}^{\mu\nu}) = 0$
- **Energy Exchange**: Mediated by $J^\nu$ with $J^0$ from horizon sector

### Partition Mapping
- **Dimensionless Inputs**: $\vec{z} = (|\Omega| R_*, (\kappa/K_s)/X, 1)$
- **Softmax Partitions**: $p_i = \text{softmax}_i( w_i^1 z_1 + w_i^2 z_2 + w_i^3 )$
- **Field Proxy**: $\Xi = |\nabla \phi| / (m_{\text{eff}} \phi_0)$ for $z_1$

## 9. Validation and Benchmarking Summary

### Success Criteria
- **RD Front Speed**: $\leq 6\%$ error, $R^2 \geq 0.9999$
- **RD Dispersion**: $\leq 0.2\%$ error, $R^2 \geq 0.999$
- **Fluid Viscosity**: $\leq 5\%$ error
- **Conservation**: Drift $\leq 10^{-8}$ per step

### Experimental Results
- All RD validations passed with documented figures and logs
- Fluid dynamics benchmarks met specifications
- Memory steering experiments show qualitative agreement

## 10. Open Questions and Future Directions

1. **Formal Lyapunov Functional**: For RD systems on bounded domains
2. **Second-Order EFT Branch**: Criteria for when it becomes necessary
3. **Memory Steering Coupling**: Quantitative integration with RD baseline
4. **Hidden Symmetries**: Exploration of additional conservation laws
5. **Observational Constraints**: Connection to cosmological data

## Conclusion

The Void Dynamics Model provides a mathematically rigorous framework that connects discrete neural dynamics to continuum physics. The reaction-diffusion equation serves as the validated canonical model, while the EFT approach offers a foundation for future extensions. Integration with Voxtrium ensures unit consistency and causal structure. Experimental validations confirm the theoretical derivations across multiple domains.

## References

1. `derivation/continuum_stack.md`
2. `derivation/discrete_to_continuum.md`
3. `derivation/effective_field_theory_approach.md`
4. `derivation/kinetic_term_derivation.md`
5. `derivation/fum_voxtrium_mapping.md`
6. `derivation/memory_steering/memory_steering.md`
7. `derivation/fluid_dynamics/fluids_limit.md`
8. `derivation/reaction_diffusion/validation_*.md`
9. `derivation/CORRECTIONS.md`
10. `derivation/DIMENSIONLESS_CONSTANTS.md`
