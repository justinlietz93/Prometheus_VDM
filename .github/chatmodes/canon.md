# Technical Summary Report

**Generated on:** October 26, 2025 at 2:39 AM CDT

---

## Generated Summary

## Technical Rules Distilled from Multiscale System Specifications and Scientific Validations

This document synthesizes core technical rules, constraints, and requirements spanning theoretical physics, numerical simulations, and software architecture. These rules serve as commandments for development, validation, and documentation across the entire system.

### I. Mathematical Foundations & Physics Principles

1.  **Variational Principles & Equations of Motion:**
    *   Derive equations of motion for continuous systems from Hamilton's principle.
    *   Apply the general Euler-Lagrange equation for field $\eta_\rho$ depending on 4-coordinates $x^\nu$: $\frac{\partial \mathcal{L}}{\partial \eta_\rho} - \frac{\partial}{\partial x^\nu} \left( \frac{\partial \mathcal{L}}{\partial \eta_{\rho,\nu}} \right) = 0$. For 1D, single field systems, this simplifies to $\frac{\partial \mathcal{L}}{\partial \eta} - \frac{d}{dt} \left( \frac{\partial \mathcal{L}}{\partial \dot{\eta}} \right) - \frac{d}{dx} \left( \frac{\partial \mathcal{L}}{\partial \eta'} \right) = 0$.
    *   Hamilton's equations must be expressed as $\dot{\eta} = [\eta, H]$ or $\dot{\eta} = J \frac{\partial H}{\partial \eta}$.
    *   Calculate the total time derivative of an arbitrary function $u(q, p, t)$ in Hamiltonian mechanics as: $\frac{du}{dt} = [u, H] + \frac{\partial u}{\partial t}$.
    *   For action-angle variables, use $\dot{w_i} = \nu_i(J_1, ..., J_n) = \frac{\partial H}{\partial J_i}$ for angle variable equations of motion.
    *   The mean frequency $\nu_k$ for a multiply periodic system is defined as $\lim_{T \to \infty} \frac{m_k}{T} = \nu_k$.
2.  **Rigid Body Dynamics:**
    *   A rigid body is defined as a system of mass points where distances between all pairs of points remain constant throughout the motion.
    *   Specify a rigid body's configuration in space using exactly six independent generalized coordinates.
    *   The angular velocity vector $\omega$ is assumed to be constant throughout a rigid body.
    *   Use Euler's Equation for Newtonian equations of motion relative to body axes: $(dL/dt)_b + \omega \times L = N$.
    *   For principal axes, apply Euler's equations: $I_i \frac{d\omega_i}{dt} + \epsilon_{ijk} \omega_j \omega_k I_k = N_i$.
    *   For a rigid body with one fixed point and principal axes, apply specific Euler's equations: $I_1 \frac{d\omega_1}{dt} - \omega_2 \omega_3 (I_2 - I_3) = N_1$, $I_2 \frac{d\omega_2}{dt} - \omega_3 \omega_1 (I_3 - I_1) = N_2$, $I_3 \frac{d\omega_3}{dt} - \omega_1 \omega_2 (I_1 - I_2) = N_3$.
    *   For nonrigid motion where rotating axes coincide with instantaneous principal axes, use $I_i \frac{d\omega_i}{dt} + \epsilon_{ijk} \omega_j \omega_k I_k - \sum_m \frac{dI_{im}}{dt} \omega_m = N_i$.
3.  **Small Oscillations:**
    *   The equations of motion for small oscillations must be $T_{ij} \ddot{\eta}_j + V_{ij} \eta_j = 0$.
    *   Amplitude factors $a_j$ must satisfy $\sum_j (V_{ij} - \omega^2 T_{ij}) a_j = 0$.
    *   The determinantal condition $det(V_{ij} - \omega^2 T_{ij}) = 0$ must be satisfied to find small oscillation frequencies.
    *   Eigenvectors $a_{ij}$ must satisfy $\sum_j a_{ij} (V_{ij} - \lambda_i \delta_{ij}) = 0$ and $\sum_j a_{ij}^2 = 1$.
    *   Normal coordinates $\xi_k$ must satisfy $\ddot{\xi}_k + \omega_k^2 \xi_k = 0$.
4.  **Field Equations & Hamiltonian Densities:**
    *   For a complex scalar field with Lagrangian density $L = c^2 \phi^{,\mu} \phi^*_\mu - \mu_0^2 c^2 \phi \phi^*$, the field equations are $(\Box + \mu_0^2) \phi = 0$ and $(\Box + \mu_0^2) \phi^* = 0$.
    *   For a real scalar field in one spatial dimension with $L = \frac{1}{2} [ (\frac{1}{c})^2 (\frac{\partial \phi}{\partial t})^2 - (\frac{\partial \phi}{\partial x})^2 - \mu_0^2 c^2 (1 - \cos \phi) ]$, the field equation is $\frac{1}{c^2} \frac{\partial^2 \phi}{\partial t^2} - \frac{\partial^2 \phi}{\partial x^2} = \mu_0^2 c^2 \sin \phi$.
    *   For the electromagnetic field with $L = -\frac{1}{4} F^{\mu \nu} F_{\mu \nu} + \frac{1}{c} j^\mu A_\mu$, the Euler-Lagrange equations are $\frac{\partial F^{\mu \nu}}{\partial x^\nu} = \frac{1}{c} j^\mu$.
    *   For the complex scalar field, the Hamiltonian density is defined as $\mathcal{H} = \pi \dot{\phi} + \pi^* \dot{\phi}^* - \mathcal{L}$, with conjugate momenta $\pi = \dot{\phi}^*$ and $\pi^* = \dot{\phi}$.
    *   For the sine-Gordon field, the Hamiltonian density is defined as $\mathcal{H} = \frac{1}{2} [ \pi^2 + c^2 (\frac{\partial \phi}{\partial x})^2 + \mu_0^2 c^2 (1 - \cos \phi) ]$, where $\pi = \frac{1}{c^2} \frac{\partial \phi}{\partial t}$.
    *   The Laplacian is defined as $\nabla^2 = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + \cdots$ (positive semi-definite on lattice).
    *   The d'Alembertian is defined as $\Box = \partial_t^2 - c^2 \nabla^2$.
    *   Assume $\mu^2 > 0$ implies $V''(0) = -\mu^2 < 0$ (tachyonic curvature).
    *   Lagrangian density $\mathcal{L}$ terms must be combinations of fields and other quantities to produce a 4-scalar.
    *   Restrict the Lagrangian density $\mathcal{L}$ to field quantities or their first derivatives.
    *   Interactions between fields must occur at a point to be consistent with special relativity.
    *   Interaction between a field and a particle must be possible at a given point in spacetime.
5.  **Symmetry & Conservation Laws:**
    *   **Linear Algebra:** The orthogonality condition must hold for direction cosines $a_{ij}$: $\sum_l a_{il} a_{jl} = \delta_{ij}$. The determinant's value must be preserved under a similarity transformation: $|A'| = |A|$. The secular equation for real orthogonal matrices representing rigid body motion must have a root $\lambda = +1$. Any non-trivial real orthogonal matrix must have exactly one eigenvalue of +1. All eigenvalues of a real orthogonal matrix must have unit magnitude: $\lambda \lambda^* = 1$. Infinitesimal rotation matrices $\epsilon$ must be antisymmetric: $\epsilon = -\tilde{\epsilon}$. Infinitesimal rotation generators $M_i$ must satisfy the commutation relations $[M_i, M_j] = \epsilon_{ijk} M_k$.
    *   **Inertia:** The inertia tensor $I_{ij}$ must be symmetric: $I_{ij} = I_{ji}$. If the origin of the body system is the center of mass, total angular momentum and total kinetic energy must decompose into translational and rotational contributions. The moment of inertia $I_O$ about an arbitrary axis relates to $I_{CM}$ about a parallel axis through the center of mass by $I_O = I_{CM} + M(R \times n)^2$. Principal moments of inertia must be time-independent. Solve the eigenvalue equation $I_{ij} R_j = I R_i$ to find the direction of each principal axis.
    *   **Conserved Quantities:** For torque-free motion of a rigid body, kinetic energy and the total angular momentum vector must be constant in time. For a symmetrical rigid body, $\omega_3$ must be a constant. Generalized momenta corresponding to cyclic coordinates must be constant in time. If there is no component of torque along an axis, the components of angular momentum along that axis must be constant in time. For a conservative system, total energy $E$ must be constant in time. If the Lagrangian $L$ is not an explicit function of time, the Jacobi integral (Hamiltonian) is conserved. If a coordinate $q_j$ is cyclic, its canonical momentum $p_j$ is conserved.
    *   **Molecular Symmetries:** In the second mode of a linear molecule, outer atoms must vibrate exactly out of phase to conserve linear momentum. For symmetrical molecules, amplitudes of end atoms must be identical in magnitude, end atoms travel in the same direction, and the center atom revolves in the opposite direction to keep the center of mass at rest. For a linear molecule, the two modes of perpendicular vibration are degenerate and their frequencies are equal.
    *   **Canonical Mechanics:** Canonical transformations must satisfy group properties: identity, inverse, closure under composition, and associativity. Poisson brackets must satisfy: antisymmetry, linearity, the product rule, and Jacobi's Identity. Fundamental Poisson brackets for canonical variables $(q_j, p_j)$ must satisfy: $[q_j, q_k] = 0 = [p_j, p_k]$ and $[q_j, p_k] = \delta_{jk} = -[p_j, q_k]$. All Poisson brackets must be invariant under canonical transformations.
    *   **Constants of Motion:** A function $u(q, p, t)$ is a constant of motion if and only if $\frac{du}{dt} = [u, H] + \frac{\partial u}{\partial t} = 0$. If a function $u$ does not depend explicitly on time, the condition for being a constant of motion simplifies to $[u, H] = 0$. The Poisson bracket of any two constants of the motion is also a constant of the motion.
    *   **Symmetry & Hamiltonian:** If a system is symmetrical under an operation, the Hamiltonian must remain unaffected under the corresponding transformation.
    *   **Angular Momentum (Poisson Brackets):** For any system vector $F$ (function only of $q,p$), $[F, L \cdot n] = n \times F$ or $[F_i, L_j] = \epsilon_{ijk} F_k$. Components of total canonical angular momentum $L$ must satisfy: $[L, L \cdot n] = n \times L$, $[L_i, L_j] = \epsilon_{ijk} L_k$, and $[L^2, L \cdot n] = 0$.
    *   **Lie Algebras:** A non-commutative algebra is a Lie algebra if its elements $u_i$ satisfy the Poisson bracket properties and the condition $[u_i, u_j] = \sum_k c_{ij}^k u_k$. Lie groups of infinitesimal canonical transformations whose generators are constants of motion must be symmetry groups of the system and leave the Hamiltonian invariant.
    *   **Adiabatic Invariants:** Under sufficiently slow variation of a parameter (adiabatic change), the action variable $J$ must remain constant to first order. For a charged particle in a slowly varying magnetic field, its magnetic moment $M = \frac{T_\perp}{B}$ is adiabatically invariant.
    *   **Stress-Energy Tensor:** The stress-energy tensor $T^{\mu\nu}$ must be a linear, symmetric 4-tensor. $T^{\mu\nu} u_\nu$ is interpreted as the 4-momentum density in the observer's frame. $T^{\mu\nu} u_\mu u_\nu$ is interpreted as the mass-energy density in the rest frame. The stress-energy tensor for a perfect fluid is $T_{ab} = (\rho + p)u_a u_b + p g_{ab}$. In the rest frame, $T^{00} = \rho c^2$ and momentum density $T^{0j} u_j = 0$. The covariant angular momentum density tensor $M^{\mu \nu \lambda} = \frac{1}{c} (x^\mu T^{\nu \lambda} - x^\nu T^{\mu \lambda})$ must be antisymmetric in $\mu$ and $\nu$. A symmetric stress-energy tensor is required for the conservation of the global quantity $M^{\mu\nu} = \int M^{\mu\nu\lambda} dS_\lambda$.
    *   **Noether's Theorem:** For flat 4-space, Noether's theorem applies if: (1) The Lagrangian density is form-invariant, and (2) The action integral is invariant. If Noether's theorem conditions hold, $r$ conserved quantities must exist, each satisfying $\frac{\partial}{\partial x^\nu} [ (\frac{\partial \mathcal{L}}{\partial \phi_{,\nu}}) (Y_{pr} - \phi_{,\lambda} X^\lambda_r) + \mathcal{L} X^\nu_r ] = 0$. If $\mathcal{L}$ does not depend explicitly on $x^\mu$, the conservation theorem $\frac{\partial T^\nu_\mu}{\partial x^\nu} = 0$ must hold for the stress-energy tensor $T^\nu_\mu = (\frac{\partial \mathcal{L}}{\partial \phi_{,\nu}}) \phi_{,\mu} - \mathcal{L} \delta^\nu_\mu$. If $\mathcal{L}$ and the action integral are invariant under a gauge transformation of the first kind ($\delta x = 0$, $\delta \phi_p = c_p \phi_p$), a conserved current $J^\nu = c_p (\frac{\partial \mathcal{L}}{\partial \phi_{,\nu}}) \phi_p$ must exist, satisfying $\frac{\partial J^\nu}{\partial x^\nu} = 0$. For a discrete system, the conservation theorem is $\frac{d}{dt} [ (\frac{\partial L}{\partial \dot{q}_k}) (Y_{kr} - \dot{q}_k X_r) + L X_r ] = 0$.
6.  **Locality, Causality & Constraints:**
    *   Minimal requirements for a system of first-order equations to exhibit chaos are that they must be nonlinear and have at least three variables.
7.  **PDE Type, Regularity & Well-Posedness:**
    *   **Eigenvalue Problems:** Require $det(A - \lambda I) = 0$ for non-trivial solutions. For principal moments of inertia, solve $det(I_{ij} - I \delta_{ij}) = 0$.
    *   **Hamilton-Jacobi Equation:** The Hamilton-Jacobi equation for Hamilton's principal function $S(q, P, t)$ is $H(q, \frac{\partial S}{\partial q}, t) + \frac{\partial S}{\partial t} = 0$. When the Hamiltonian $H(q,p)$ does not depend explicitly on time, the Hamilton-Jacobi equation for Hamilton's characteristic function $W(q, P)$ is $H(q, \frac{\partial W}{\partial q}) = \alpha_1$. A complete solution to the Hamilton-Jacobi equation for $S$ must be written as $S(q_1, ..., q_n; \alpha_1, ..., \alpha_n, t)$, where none of the $n$ independent constants $\alpha_i$ is solely additive. A complete solution to the Hamilton-Jacobi equation for $W$ must contain $n-1$ non-trivial constants of integration $\alpha_2, ..., \alpha_n$, which, together with $\alpha_1$, form a set of $n$ independent constants.
    *   **Separability:** A coordinate $q_j$ is separable in the Hamilton-Jacobi equation if $q_j$ and its conjugate momentum $p_j$ can be segregated in the Hamiltonian into a function $f(q_j, p_j)$ that does not contain any other variables. The Hamilton-Jacobi equation is completely separable if all coordinates are separable. For orthogonal coordinate systems, the Hamilton-Jacobi equation is separable if: (1) The Hamiltonian is conserved, (2) The Lagrangian is no more than a quadratic function of generalized velocities, so $H = \frac{1}{2} p \cdot T^{-1} \cdot p + V(q)$, (3) The elements $a_i$ of vector $\mathbf{a}$ in $T^{-1}$ are functions only of the corresponding coordinate $q_i$, (4) The potential function $V(q)$ can be written as $V(q) = \sum_j \frac{V_j(q_j)}{\phi_{ji}}$, (5) If $\phi^{-1}$ is a matrix with elements $\delta_{ij}\phi_{ij}^{-1} = \frac{1}{T_{ii}}$, and diagonal elements of both $\phi$ and $\phi^{-1}$ depend only on $q_i$. If these Staeckel conditions are satisfied, Hamilton's characteristic function is completely separable, $W(q) = \sum_i W_i(q_i)$, with $W_i$ satisfying equations of the form $(\frac{\partial W_i}{\partial q_i})^2 = -2V_i(q_i) + 2\sum_j \gamma_j$.
8.  **Boundary & Initial Conditions:**
    *   In Hamilton's principle for continuous systems, the variation $\delta\eta$ must vanish at the temporal endpoints $t_1, t_2$ and the spatial limits $x_1, x_2$ of integration.
    *   The variation $\delta\eta_\rho$ must vanish at the bounding surface $S$ of the 4-space region of integration.
    *   Integration in Hamilton's principle in all Lorentz frames must be over a region in 4-space contained between two spacelike hypersurfaces and bounded by intersecting timelike surfaces.
9.  **Constitutive Relations & Material Laws:**
    *   In the continuous limit ($a \to 0$) for an elastic rod, the ratio $m/a$ must become the mass per unit length $\mu$, and $ka$ must become Young's modulus $Y$.
    *   The spatial charge density $\rho$ corresponding to a particle of charge $q$ at point $s$ must be $\rho = q \delta(\mathbf{r}-\mathbf{s})$.
    *   The spatial current density $\mathbf{j}$ must be $\mathbf{j} = q \delta(\mathbf{r}-\mathbf{s}) \mathbf{v}(\mathbf{r})$.
10. **Coriolis Force:**
    *   The Coriolis force on a moving particle must be perpendicular to both the angular velocity $\omega$ and the particle's velocity $v$.
    *   The Coriolis force deflects projectiles to the right in the northern hemisphere and reverses in the southern, being zero at the equator.
    *   A body falling freely in the northern hemisphere must be deflected to the East.
11. **Canonical Transformations:**
    *   A restricted canonical transformation is one in which time does not appear explicitly in the equations of transformation: $Q_i = Q_i(q, p)$, $P_i = P_i(q, p)$.
    *   For infinitesimal canonical transformations (ICTs), retain only first-order terms in the infinitesimals in all calculations.
    *   The Hamiltonian used in the generalized equation of motion must be appropriate to the particular set of canonical variables being used.
    *   Upon transforming to another set of variables by a time-dependent canonical transformation, change to the transformed Hamiltonian $K$.
    *   For a real canonical transformation, the Jacobian determinant $|M|$ must be $+1$.
    *   For a generating function $F_1(q, Q)$ to exist, the partial derivative $\partial Q / \partial p$ must not vanish.
    *   An integrable Hamiltonian $H(q,p,t)$ is defined as one where a canonical transformation to new variables $P_i, Q_i$ exists such that all $Q_i$ are cyclic ($H = H(P_1, ..., P_n; t)$) and Hamilton's equations can be readily integrated.

### II. Configuration & Data Schemas

1.  **Required Fields:**
    *   All fields explicitly marked as 'Y' in their respective configuration or metrics tables must be present.
    *   The top-level `files` array property is required for `PYTHON_PACKAGE_SCHEMA`.
    *   Each item within the `files` array must be an object and include `fileName` and `fileContent` properties.
    *   `source_path`, `line_no`, and `text` fields are required for `SayRecord`.
    *   `tick` and `kind` fields are required for `Observation`.
    *   `kind` field is required for `BaseEvent`.
2.  **Field Types & Constraints (General):**
    *   **Numeric Fields:**
        *   **Integers:** `neurons`, `k`, `hz`, `status_interval`, `bundle_size`, `candidates`, `walkers`, `hops`, `stim_group_size`, `stim_max_symbols`, `speak_cooldown_ticks`, `b1_half_life_ticks`, `viz_every`, `log_every`, `checkpoint_every`, `checkpoint_keep`, `nx`, `ny`, `Nx`, `Ny`, `batch_size`, `max_bundle_mb`, `line_no`, `loop_len`, `max_ops`, `max_emits`, `ttl`, `step`, `node`, `u`, `v`, `motif_id`.
        *   **Floats:** `threshold`, `lambda_omega`, `prune_factor`, `stim_amp`, `stim_decay`, `speak_z`, `speak_hysteresis`, `speak_valence_thresh`, `tau`, `void_gain`, `rho_floor`, `H`, `L_in`, `L_out`, `rc`, `rho`, `nu`, `U0`, `dt`, `t_end`, `regularizer.beta`, `regularizer.tau_r`, `regularizer.kappa`, `regularizer.alpha`, `regularizer.tau_u`, `regularizer.tau_g`, `r`, `u` (in metrics context), `T`, `W0`, `delta_Q_max`, `W_min`, `W_max`, `slope`, `intercept`, `r2`, `novelty`, `hab`, `w`, `amp`, `energy_budget`, `f_vac`, `f_grain`, `f_gw`, `coverage_phys`, `coverage_raw`, `finite_fraction`, `e_rev`.
        *   **Booleans:** `use_time_dynamics`, `sparse_mode`, `speak_auto`, `periodic_x`, `periodic_y`, `void_enabled`, `void_use_modulation`, `allow_dirty`, `create_thumbs`, `regularizer.enabled`, `save_streamlines`, `save_vorticity`, `save_maxspeed_scan`, `acceptance.passed`, `curvature_ok`, `passed`.
    *   **Strings:** `domain`, `void_domain`, `probe_mode`, `adapter_path`, `walls`, `inlet`, `outlet`, `solver`, `kind`, `fileName`, `fileContent`, `timestamp_utc`, `metrics_version`, `tag`, `horizon_id`.
    *   **Path Objects:** `storage_root`.
    *   **Sequences/Lists:** `concepts` (str), `layers` (str), `steps` (int), `seeds` (int), `dts` (floats), `delta_Q_max_list` (floats), `nodes` (any), `dt_list` (floats).
    *   **Tuples:** `forcing` (two floats).
    *   **Nullable:** `duration` (integer or null), `u_clamp` (float or None), `adapter_path` (string or None).
3.  **Field Value Constraints (Specific):**
    *   **General Numeric:** All numeric fields must be greater than or equal to 0, unless specified otherwise.
    *   **Positive Numeric ( > 0 ):**
        *   `neurons`, `k`, `hz` (`schema-run-profile`)
        *   `nx`, `ny` (`schema-lbmconfig`, `schema-vdm-corner-config`)
        *   `tau` (`schema-lbmconfig`)
        *   `rho_floor` (`schema-lbmconfig`)
        *   `batch_size`, `max_bundle_mb` (`schema-geometryrunconfig`)
        *   `H`, `rho`, `U0`, `nu`, `dt`, `t_end` (`schema-vdm-corner-config`)
        *   `tau_min`, `U_min`, `uclamp_min` (`PolicyBounds`)
        *   `line_no` (`SayRecord`)
        *   `r`, `u`, `dt`, `T`, `W0` (`schema-runmetrics`)
        *   `ttl` (`BiasHintEvent`)
        *   `dt_ret` (`HorizonActivityEvent`)
        *   All numeric parameters within the `params` object (`QFUM Metrics JSON Output`)
    *   **Non-Negative Numeric ( >= 0 ):**
        *   `rc` (`schema-vdm-corner-config`)
        *   `delta_Q_max` (`schema-runmetrics`)
        *   `t` (`Petition`, `HorizonActivityEvent`)
        *   `tick` (`Observation`, `BudgetTick`)
        *   `loop_len` (`Observation`)
        *   `novelty`, `hab` (`DeltaEvent`)
        *   `u` (source node ID), `v` (target node ID) (`EdgeOnEvent`/`EdgeOffEvent`)
        *   `node` (neuron/node ID) (`SpikeEvent`, `DeltaWEvent`)
        *   `amp` (activity magnitude) (`SpikeEvent`)
        *   `motif_id` (`MotifEnterEvent`/`MotifExitEvent`)
        *   If present, `adc_territories`, `adc_boundaries`, `adc_cycle_hits` (`ADCEvent`)
        *   `energy_budget` (`RouterSplitEvent`)
        *   `max_ops`, `max_emits` (`BudgetTick`)
        *   Values in `dt_list` array (`KG Energy Oscillation Summary`)
        *   `e_rev` (`KG Energy Oscillation Summary`)
        *   `max_us` (micro time budget)
    *   **Ranges & Specific Values:**
        *   `tau` must be greater than 0.5 for stability (`schema-lbmconfig`, `PolicyBounds`).
        *   If `u_clamp` is not None, it must be greater than 0 (`schema-lbmconfig`).
        *   `tau_max` must be greater than `tau_min`. `U_max` must be greater than `U_min`. `uclamp_max` must be greater than `uclamp_min` (`PolicyBounds`).
        *   `concepts`, `layers`, and `steps` fields must be non-empty sequences (`schema-geometryrunconfig`).
        *   The `adapter_path` format must be `module:ClassName` (`schema-geometryrunconfig`, `VDM Corner Config`).
        *   The `kind` field must be one of `['div', 'swirl', 'shear']` for `Petition`.
        *   The `kind` field must be one of "region_stat", "boundary_probe", "cycle_hit", or "novel_frontier" for `Observation`.
        *   The length of the `nodes` list must be less than or equal to 256 (`Observation`).
        *   The `sign` field must be one of `[-1, 0, +1]` (`SpikeEvent`).
        *   The `w` (optional weight) field should typically be greater than 0 (`VTTouchEvent`).
        *   The `ttl` field must be greater than or equal to 1 for `BudgetTick`.
        *   The `x` field must contain between 1 and 4 finite coordinates (`HorizonActivityEvent`).
        *   The `dotA` (observable production rate) field must not be equal to 0 (`HorizonActivityEvent`).
        *   The `horizon_id` field must be non-empty (`HorizonActivityEvent`).
        *   `f_vac`, `f_grain`, and `f_gw` must be within the range `[0, 1]` for `RouterSplitEvent`.
        *   The sum of `f_vac`, `f_grain`, and `f_gw` must equal 1.0 (within a tolerance of 1e-9) for `RouterSplitEvent`.
        *   The `version` field must be "1.0" for `QFUM Metrics JSON Output`.
        *   The `timestamp_utc` field must be in ISO 8601 format (`QFUM Metrics JSON Output`).
        *   The `acceptance.passed` field must be the logical conjunction of all its sub-gates (`QFUM Metrics JSON Output`).
        *   The `metrics_version` field must be "v2-phys-aware" for `Tube Spectrum Summary`.
        *   `coverage_phys` and `coverage_raw` must be within the range `[0, 1]` for `Tube Spectrum Summary`.
        *   The `coverage` field must be equal to `coverage_phys` for `Tube Spectrum Summary`.
        *   The `attempts_raw` field must equal the product of `|R_sweep|` and `(ell_max+1)` (`Tube Spectrum Summary`).
        *   `finite_fraction` must be within the range `[0, 1]` for `Tube Condensation Summary`.
        *   The `passed` field must be true if and only if `finite_fraction` is greater than or equal to 0.80 AND `curvature_ok` is true (`Tube Condensation Summary`).
        *   The `tag` field must be "KG-energy-osc-v1" for `KG Energy Oscillation Summary`.
        *   The length of `dt_list` must equal the length of `AH` (`KG Energy Oscillation Summary`).
        *   `fit.R2` must be within the range `[0, 1]` for `KG Energy Oscillation Summary`.
        *   The `passed` flag must reflect the conjunction of KG gates defined in the canon (`KG Energy Oscillation Summary`).
        *   `dts` (list of time step sizes) and `delta_Q_max_list` (maximum invariant drifts) must have the same length (`ConvergenceMetrics`).
        *   `r2` (R² coefficient of determination) must be within the range `[0, 1]` (`ConvergenceMetrics`).

### III. Syntax & Naming Conventions

1.  **Document Authority:** The `NAMING_CONVENTIONS.md` document is the single source of truth for naming conventions.
2.  **Mathematical Symbol Styling:**
    *   Use `\mathbf{}` for vectors (e.g., `$\mathbf{x}$`).
    *   Use `\boldsymbol{}` for multi-channel fields (e.g., `$\boldsymbol{\phi}(\mathbf{x},t)$`).
    *   Use `\mathcal{}` for sets/spaces (e.g., `$\mathcal{W}$`).
    *   Use `\mathbb{R}^d`, `\mathbb{R}^C` for field spaces (e.g., `$\mathbf{x}\in\mathbb{R}^d$`).
    *   Use `\mathbb{Z}_N` for lattice spaces (e.g., `$\mathbb{Z}_N$`).
    *   Use `\mathrm{}` for named operators (e.g., `$\mathrm{nbr}(i)$`).
    *   Use standard notation for differential operators (e.g., `$\nabla^2$`).
    *   Use `\mathrm{}` or plain text for named dimensionless groups (e.g., `$\mathrm{Re}$`).
    *   Use italic (default) for functions (e.g., `$V(\phi)$`).
    *   Use italic (default) for Greek scalars (e.g., `$\rho(\mathbf{x},t)$`).
    *   Use italic (default) for indices (e.g., `$i, j$`).
3.  **Cross-linking & Anchors:**
    *   Use `vdm-e-###` for equation headers and link to them using `#vdm-e-###`.
    *   Use `sym-...` for symbol anchors and add them to `SYMBOLS.md` to enable stable deep linking.
    *   Use `const-...` for constant anchors and link to them using `#const-...`.
    *   Use `geom-...` for geometry anchors.
    *   Use `bc-...` for BC anchors.
    *   Use `ic-...` for IC anchors.
    *   Use `data-...` for data product anchors.
    *   Plan to use `vdm-a-###` for algorithm IDs.
    *   Use varied anchor patterns for units/normalization (e.g., `#kappa-l`).
    *   Plan to use `kpi-...` for metric anchors.
4.  **MathJax Usage:** Use GitHub-safe `$...$`/`$$...$$` for MathJax only when quoting existing snippets.
5.  **Matrix & Vector Conventions:**
    *   When using $\theta_{ij}$ or $a_{ij}$ for direction cosines, the first index refers to the primed system and the second to the unprimed system.
    *   Express unit vectors in the primed system in terms of unit vectors in the unprimed system using direction cosines as coefficients.
    *   Relate components of any vector $G$ in the primed system to its components in the unprimed system using direction cosines.
    *   Basis vectors in both coordinate systems must be orthogonal and have unit magnitude.
    *   Employ the Einstein summation convention: sum over all possible values of any index that appears two or more times in a term.
    *   Apply matrix multiplication associatively: $(AB)C = A(BC)$.
    *   The number of columns of the first matrix must equal the number of rows of the second matrix for matrix multiplication to be defined.
    *   For orthogonal matrices, the reciprocal matrix is the transposed matrix: $A^{-1} = \tilde{A}$, and elements relate as $a^{-1}_{ij} = a_{ji}$.
    *   Diagonal elements of an antisymmetric matrix must be zero.
6.  **Rotation Definitions:**
    *   Define Euler angles as a specific sequence of three rotations: $\phi$ (counterclockwise about z), $\theta$ (counterclockwise about new x-axis, line of nodes), $\psi$ (counterclockwise about new z-axis).
    *   Calculate the complete transformation matrix $A$ for Euler angles as the product $BCD$.
    *   Obtain the inverse transformation matrix for Euler angles by transposing the forward transformation matrix.
    *   Define Cayley-Klein parameters as complex numbers with constraints $\beta = -\gamma^*$ and $\delta = \alpha^*$.
    *   Define Euler parameters as real quantities satisfying $e_0^2 + e_1^2 + e_2^2 + e_3^2 = 1$.
    *   Express the rotation matrix $A$ in terms of Euler parameters using Eq. (4.47').
7.  **Diagonalization:** Construct the similarity transformation matrix for diagonalization using eigenvectors as its columns.

### IV. Numerical Methods & Simulation

1.  **Numerical Stability & Accuracy:**
    *   Use central differences when both neighbors exist; otherwise, use forward/backward differences.
    *   Propagate NaN if any operand is missing or NaN.
    *   Use a small tolerance $\varepsilon_{\text{fd}}$ (e.g., $10^{-9}$) for sign/zero checks.
    *   Apply isotonic regression along E if monotonicity in E is violated before evaluating E_min.
    *   Evaluate monotonicity conditions with tolerance $\varepsilon_{\text{mono}}$ (default $10^{-9}$).
    *   If monotonicity conditions fail, regenerate data or apply axis-wise isotonic smoothing before downstream calculations.
    *   Disable noise and sinusoidal modulation for order-of-accuracy and Lyapunov tests.
    *   Ensure CFL (Courant-Friedrichs-Lewy) constraint `cfl <= 0.5` for stability.
    *   Ensure Mach constraint $\mathrm{Ma} \ll 1$ for incompressible flow (LBM).
    *   Ensure Void Mach constraint $M_v < 1$ for stability.
    *   Set $\Delta t\_\max = 0.8/\omega\_\max$ for metriplectic system stability control.
    *   For light-cone measurements, ensure fitted front speed $v \le c(1+\epsilon)$ with $\epsilon = 0.02$.
    *   For Noether invariants, ensure energy drift $\max \Delta E \le 10^{-12}$ or $\max \Delta E \le 10\,\epsilon\sqrt{N}$.
    *   For Noether invariants, ensure momentum drift $\max \Delta P \le 10^{-12}$ or $\max \Delta P \le 10\,\epsilon\sqrt{N}$.
    *   For Noether invariants, ensure reversibility $\|\Delta\|_{\infty} \le 10^{-10}$.
    *   Enforce $\Delta L \le 0$ for M and JMJ (metriplectic systems).
    *   Enforce identity residuals $\le 1\text{e-}12$ for M and JMJ (metriplectic systems).
    *   Ensure symplectic J reversibility $\le 1\text{e-}12$.
    *   Set symplectic J energy drift gate at $\le 1\text{e-}12$ (strict).
    *   Ensure Strang order two-grid slope $p \gtrsim 2$ with high $R^2$ for metriplectic systems.
    *   Ensure defect slope is near 3 for Strang (metriplectic systems).
    *   Ensure J-unitarity/reversibility by having $\|W_2-W_0\|_\infty$ small after $+\Delta t$ then $-\Delta t$.
    *   Ensure J-unitarity/reversibility by having $L^2$ drift near machine precision.
    *   Ensure DG monotonicity with $\Delta L_h \le 0$ per step.
    *   Set reversibility tolerance at $10^{-7}$ for metriplectic systems.
    *   Set $L^2$ drift tolerance at $2\times10^{-8}$ for metriplectic systems.
    *   For J-only (spectral) gates, adopt a pragmatic cap scaled to FFT round-off: $\|W_2-W_0\|_\infty\le c\,\epsilon_{\text{mach}}\sqrt{N}$. Do not silently relax thresholds.
2.  **Initial Conditions (ICs):**
    *   Initialize ICs with band-limited sinusoids with random phases within bands (metriplectic systems).
    *   Normalize ICs to fixed amplitude (metriplectic systems).
    *   Use multiple seeds per band for ICs (metriplectic systems).
    *   Generate periodic ICs for ($\phi, \pi$) using seeded noise (seed_scale = 0.05) for KG $\oplus$ RD metriplectic.
    *   Initialize a single Fourier mode for dispersion tests.
    *   Initialize a narrow Gaussian for light cone tests.
    *   Use random initial field & momentum with small amplitude (seed_scale=0.05) for Noether invariants.
3.  **Numerical Grids & Parameters:**
    *   Use $N=256$, $\Delta x=1$ grid with periodic BC for KG J-only simulations.
    *   Use parameters $(c,m)=(1.0,0.5)$ for KG J-only simulations.
    *   Use small amplitudes for dispersion tests.
    *   Use fixed RNG seeds with seed_scale $=0.05$ for KG J-only simulations.
    *   Use $N=256$, $\Delta x=1.0$ grid for Noether invariants.
    *   Use parameters $c=1$, $m=1$ for Noether invariants.
    *   Select $\Delta t = 0.005$ for Noether invariants.
    *   Use 512 Störmer–Verlet steps for integration of Noether invariants.
    *   Use N=256, $\Delta x=1$ grid for KG $\oplus$ RD metriplectic.
    *   Use 10 seeds with seed_scale = 0.05 for KG $\oplus$ RD metriplectic.
    *   Use parameters (c, m, D, r, u) = (1.0, 0.5, 1.0, 0.2, 0.25) for KG $\oplus$ RD metriplectic.
    *   Fix grid, parameters, and tolerances for KG $\oplus$ RD metriplectic.
    *   Use spectral M-Laplacian for KG $\oplus$ RD metriplectic.
    *   Use DG tolerance $1\text{e-}12$ for KG $\oplus$ RD metriplectic.
    *   Use JMJ and MJM composition for KG $\oplus$ RD metriplectic.
    *   Parameterize spectral vs stencil Laplacian options via `m_lap_operator`.

### V. Validation & Metrics

1.  **General Validation Principles:**
    *   Establish reproducible numeric checks for the RD canonical model.
    *   Define quantitative acceptance criteria and reproducible verification protocol for memory steering mechanism.
    *   Define falsifiable acceptance thresholds for the fluids sector (LBM→NS).
    *   Establish scientific significance of agency "smoke tests."
    *   All KPIs in `VALIDATION_METRICS.md` must pass for the physics validation CI task.
2.  **Cosmology Validation:**
    *   Validate FRW energy continuity with source bookkeeping.
    *   Measure the RMS residual of the continuity equation under controlled scenarios.
    *   Apply causal sourcing gates.
    *   The RMS continuity residual must be $\le$ double precision scale tolerance.
    *   Fix equation of state $w$ to 0 (dust) for FRW continuity identity tests.
    *   Use $\rho(a)=\rho_0 a^{-3}$ analytically for dust scaling law tests.
    *   Use uniform $\Delta t$ for the time grid.
    *   Use central differences for numerical differentiation of $\rho a^3$.
    *   Compare RMS_FRW to gate threshold $10^{-6}$.
3.  **Metriplectic Systems Validation:**
    *   Compute $H_d(t)$ per step.
    *   Aggregate medians of $A_H$ and $A_H/\bar H$ across seeds at each $\Delta t$.
    *   Fit $\log A_H$ vs $\log \Delta t$.
    *   For dispersion, regress $\omega^2$ vs $k^2$ with slope $\approx c^2$, intercept $\approx m^2$, and $R^2 \ge 0.999$.
    *   Report $R^2$ for light-cone fit.
    *   For dispersion, run short windows to estimate $\omega$, sweep a small set of $k$, fit $\omega^2$ vs $k^2$, and log slope, intercept, and $R^2$.
    *   For light cone, threshold on $|\phi|$ to measure radius $R(t)$ over steps, fit $R(t)$ vs $t$ for speed, and log slope and $R^2$.
    *   Record per-step absolute drift for Noether invariants.
    *   For reversibility test (Noether), integrate forward 512 steps, then backward 512 steps, and measure sup-norm difference.
    *   Target two-grid slope $\ge 2.90$ with R² $\ge 0.999$ for Strang (metriplectic).
    *   For KG $\oplus$ RD metriplectic, enforce $\Delta L \le 0$, identity residuals $\le 1\text{e-}12$, slope $\ge 2.90$ with R² $\ge 0.999$, reversibility $\le 1\text{e-}12$, and route failures under `failed_runs/`.
    *   Complement the strict reversibility gate with an oscillation-based energy gate.
    *   Adopt composite ($\phi, \pi$) two-grid norm and re-fit slopes.
    *   Extend small-$\Delta t$ sweep to probe asymptotics.
    *   JMJ (stencil-DG baseline) slope must be $\ge 2.90$.
    *   JMJ (spectral-DG option) slope must be $\ge 3.00$.
    *   Keep J-only reversibility and $L^2$ drift gates.
    *   Log measured $c$ for J-only (spectral) gates.
    *   Ensure J skew $\langle v, J v \rangle = 0$ in exact arithmetic. Use median absolute value over random v for J skew gate; ensure median $|\langle v, J v \rangle| \le 1\text{e-}12$.
    *   Ensure M PSD $\langle u, M u \rangle \ge 0$. Use zero negative counts over random u for M PSD gate; ensure neg_count = 0 with tolerance $1\text{e-}12$.
    *   For coupled KG$\oplus$RD states, extend M operator check blockwise to confirm block-PSD.
    *   Validate logarithmic first integral Q(W,t) = ln(W/(r - u W)) - r t for autonomous on-site logistic ODE numerically.
    *   Ensure Q_FUM drift absolute value $\Delta Q \le 10^{-8}$.
4.  **Decoherence Portals Validation:**
    *   Ensure Fisher consistency (relative error $\le 10\%$).
    *   Ensure noise budget residuals are within spec.
    *   Compare $|\hat\epsilon-\epsilon_\text{true}|/\epsilon_\text{true}$ to the 10% gate.
    *   Compute noise budget residuals against modeled noise components and verify they lie within spec.
5.  **Tube Spectrum & Condensation Validation:**
    *   Use $\mathrm{cov}_{\rm phys}$ for gating.
    *   Ensure spectrum coverage gate $\mathrm{cov}_{\rm phys} \ge 0.95$.
    *   Report $\mathrm{cov}_{\rm raw}$.
    *   Ensure condensation curvature gate has an interior minimum $R_\star$ with a quadratic coefficient $a>0$.
    *   Ensure condensation curvature gate has finite_fraction $\ge 0.80$.
6.  **Reaction-Diffusion (RD) Model Validation:**
    *   Validate front speed and linear dispersion.
    *   Ensure RD front speed relative error (rel_err) is $\le 0.05$.
    *   Ensure RD front speed $R^2$ is $\ge 0.98$.
    *   Ensure RD dispersion median relative error (med_rel_err) is $\le 0.10$.
    *   Ensure RD dispersion $R^2$ array is $\ge 0.98$.
    *   Validate theoretical front speed $c_{th} = 2\sqrt{D r}$ against measured front position tracking with Neumann BCs.
    *   Cross-check gradient-based speed.
    *   Validate per-mode growth rate $\sigma(m)$ via linear fit of log|Û_m(t)| against discrete and continuum theory.
    *   Ensure median relative error $\le 0.10$ over good modes (R²_mode $\ge 0.95$).
    *   Ensure R²_array $\ge 0.98$.
7.  **Memory Steering Validation:**
    *   Validate fixed-point convergence, boundedness, and canonical void target convergence.
    *   Ensure memory steering drift absolute value $\le 0.02$.
    *   Ensure memory steering target absolute deviation $|M_{final} - 0.6| \le 0.02$.
    *   Ensure memory steering SNR improvement $\ge 3$ dB.
    *   Run memory steering acceptance harness with fixed parameters (g=0.12, $\lambda$=0.08).
    *   Verify all memory steering acceptance checks pass.
8.  **Fluid Dynamics Validation (LBM→NS):**
    *   Certify reduction to Navier-Stokes.
    *   Validate Taylor-Green vortex and lid-driven cavity benchmarks.
    *   Ensure Taylor-Green vortex viscosity relative error $\le 0.05$ at baseline grid $\ge 256^2$.
    *   Ensure Lid-driven cavity maximum divergence $\le 10^{-6}$ for double precision.
    *   Fit viscous decay E(t) = E₀ exp(-2 $\nu$ k² t).
    *   Verify |$\nu_{fit}$ - $\nu_{th}$| / $\nu_{th}$ $\le 5\%$ at baseline grid $\ge 256^2$.
    *   Monitor divergence norm.
    *   Verify max_t ‖∇·v‖₂ $\le 10^{-6}$ (double precision).
    *   Verify max |Δu| = 0 and |Δv| = 0 at the end of matched runs for walker-flow interaction.

### VI. Architecture & Implementation

1.  **Core System Principles:**
    *   Prioritize implementing conservation laws.
    *   Prioritize implementing dimensionless constants.
    *   Prioritize integrating reaction-diffusion.
    *   Prioritize coupling memory steering.
    *   Prioritize implementing effective field theory.
    *   Prioritize implementing fluid dynamics.
    *   Establish a rigorous axiomatic foundation for VDM.
    *   Derive continuum dynamics from a discrete action principle.
    *   Apply discrete Euler-Lagrange equations rigorously to derive second-order time dynamics naturally.
    *   Derive exact spatial kinetic prefactor $c_{\text{lat}} a^2 (\nabla\phi)^2$ from discrete interaction energy via Taylor expansion on a cubic lattice.
    *   Ensure exact value $c_{\text{lat}} = 2$ for 3D cubic lattice.
    *   Ensure Lorentz invariance condition $c^2 = 2J a^2$.
    *   Define scaling limits with fixed wave speed.
    *   Establish field redefinition.
    *   Derive continuum action from discrete limit.
    *   Add quartic stabilization to potential.
    *   Determine parameter constraints for global minimum existence.
    *   Calculate vacuum solutions.
    *   Apply Noether's theorem to derive conserved currents.
    *   Analyze symmetry breaking patterns.
    *   Complete conservation law framework.
    *   Verify energy and momentum conservation.
    *   Ensure sparsity constraint $\kappa \ll 1$ (edits per DOF per step).
    *   Ensure time scale separation $\epsilon \ll 1$ (slow/fast layer ratio).
    *   Use $\sum_{j \in N(i)} (W_j - W_i)$ for discrete diffusion.
    *   `substrate.py` must integrate RD field coupling.
    *   `substrate.py` must integrate memory field.
    *   `void_dynamics_adapter.py` must use dimensionless groups instead of hard-coded constants.
    *   `revgsp.py` plasticity must be modulated by physical fields ($\phi$, $M$).
    *   `gdsp.py` structural plasticity must respect conservation laws.
    *   Normative math must be defined in `derivation/EQUATIONS.md`.
    *   Numbers must be defined in `derivation/CONSTANTS.md`.
    *   Symbols/units must be defined in `derivation/SYMBOLS.md` and `derivation/UNITS_NORMALIZATION.md`.
    *   The canonical map must be defined in `CANON_MAP.md`.
2.  **Simulation Loop & Control Flow (`VDM-A-001`):**
    *   Check `duration_s` termination condition if provided.
    *   Poll control plane for external `phase.json` updates.
    *   Run RE-VGSP learner only if `ENABLE_REVGSP=1`.
    *   Run GDSP structural actuator only if `ENABLE_GDSP=1`.
    *   Apply B1 detector on connectome observations.
    *   Process inbound message queue.
    *   Run void scouts within a bounded micro time budget (`max_us`).
    *   Fold events into metrics (`tick_fold`).
    *   Emit "why" (say text composition) every N ticks (optionally).
    *   Run smoke tests (boundary checks) (optionally).
    *   Emit status and macro observations (logging, Redis).
    *   Save checkpoint if `checkpoint_every` divides `step`.
    *   Visualize (plots, maps publish) (optionally).
    *   Sleep to match target hz.
    *   Terminate if `duration_s` wall-clock expires or `KeyboardInterrupt` occurs.
    *   `nx.connectome`, `nx.sie`, `nx.ute`, `nx.utd` must be initialized.
    *   `nx.run_dir` must exist for checkpoints/logs.
    *   Connectome topology and weights must be updated per tick.
    *   Metrics must be published to bus/logs/Redis.
    *   Checkpoints must be saved at configured intervals.
    *   Execution must be single-threaded per tick.
    *   Steps must be sequential.
    *   Use try-except wrappers on all subsystem calls.
    *   Perform silent no-op on errors when `VOID_STRICT=0`.
    *   `VOID_STRICT=1` must re-raise exceptions for debugging.
    *   Add fail-fast/telemetry path for GDSP.
    *   Fail fast for GDSP.
    *   Unify or validate overlapping scout flags.
    *   Keep Status HTTP localhost default.
    *   Gate optional token auth for Status HTTP.
    *   Ensure total wall-clock time is $\le$ `max_us` (best-effort).
    *   Ensure round-robin fairness over ticks.
    *   Clarify single admission gate for runner flags.
3.  **Connectome & Plasticity (`VDM-A-002`, `VDM-A-006`):**
    *   Return NaN or mask cells where V $\le 0$ for elasticity calculations.
    *   Record NA if no E on the grid achieves the target v0.
    *   Enforce non-negative weights summing to budget (B_i) via Euclidean projection.
    *   Evaluate monotonicity before applying the weight update rule.
    *   Disable universal domain modulation factor for physics tests until proven.
    *   Remove any ability to use dense backend for GDSP.
    *   Use sparse only for GDSP.
    *   Do not use dense scan branch.
    *   `NO_DENSE_CONNECTOME=1` environment gate must be enforced.
    *   Remove dense rebuild / dense top-k path.
    *   Wire deterministic RNG for structural rewiring.
    *   Adhere to "no dense path whatsoever" policy for connectome.
    *   Ensure `delta_re_vgsp`, `delta_gdsp`, `universal_void_dynamics` alias sampler functions are available.
    *   Ensure `A` is symmetric.
    *   Ensure approximately `k` neighbors per node.
    *   Ensure `W` stays in `[0,1]`.
    *   Ensure `E` is derived from `W` and `A`.
    *   Emit events only for visited nodes/edges.
    *   `W` must be CSR weights/state, shape `[n,n]`.
    *   Operate on `W.data`.
    *   `W.indices`/`W.indptr` must remain unchanged.
    *   Densification is forbidden for `W`.
    *   `E` must be CSR with identical sparsity pattern as `W`.
    *   Three-factor scaling must be applied via `ΔW *= E.data`.
    *   No densification must occur anywhere in `VDM-A-006`.
    *   `neuron_polarities.shape` must be `(n,)` if provided.
    *   Value changes must be bounded by chosen clamps.
    *   Eligibility decays must be handled in separate E-update pseudocode.
    *   If `domain_modulation` lookup fails, use `dm := 1.0` and log a warning.
    *   If `E` pattern mismatches `W`, raise an error or resync pattern explicitly.
    *   Do not silently densify if `E` pattern mismatches `W`.
    *   Use emergent budgets (no static knobs).
    *   Enforce `edges_touched ≤ budget_prune + 2·budget_bridge + budget_grow` for the budget gate.
    *   Abort if class min-degree floors/E-I checks would breach.
    *   Add `TagEvent(kind="tag.*", …)` to existing event types.
    *   Fold `TagEvent` into incremental reducers (EWMA/CMS/UF) for the scoreboard.
    *   Expose `tick(scoreboard, budgets, territory)` for GDSP.
    *   GDSP `tick` must call existing sparse edit routines (prune/grow/bridge/cull) under budgets.
    *   Compute emergent budgets per territory from void-debt/SIE, fragmentation (UF components), and backlog EWMA.
    *   Establish a system where distinct neuron classes are managed and allocated to hardware best suited for their computational profile.
    *   Define `NeuronType` enumeration (INTEGRATOR, MESSENGER, etc.) in a shared constants module.
    *   Write GPU kernels to operate on subsets of neuron arrays based on type.
    *   Partition data for MI100 (integrators) and 7900 XTX (messengers).
    *   Allow different neuron classes to have distinct learning parameters.
    *   Enable a mix of fast-adapting and slow, stable learning to prevent catastrophic forgetting.
4.  **Alias Sampling (`VDM-A-005`):**
    *   Ensure `p.size > 0` and `p.sum() > 0` for alias sampling.
    *   Ensure `prob.size == alias.size == N`.
    *   Ensure draws from the alias table reproduce the original distribution.
    *   Use uniform distribution fallback (`p = 1/N`) if `p.sum() <= 0`.
5.  **Threshold Adaptation (`VDM-A-007`):**
    *   Truncate histories to last 100 samples.
    *   Ensure thresholds stay within `[min, max]` bounds.
    *   Ensure histories are bounded to last 100 samples.
    *   Add regression coverage for threshold adaptation / activity damping.
6.  **Walker Behavior (`VDM-A-008`, `VDM-A-009`):**
    *   Clamp walker position to interior band `[0.5, nx-1.5] x [0.5, ny-1.5]`.
    *   Jitter walker inward if `solid[y_new, x_new]` is true.
    *   Ensure walker stays inside fluid domain.
    *   Do not write to simulation state (read-only).
    *   Ensure read-only walker usage does not alter flow fields.
    *   Ensure suggested parameters stay within bounds.
    *   Keep stencil baseline available for ablations.
    *   For new mixed-model experiments (e.g., KG $\oplus$ RD), prefer the spectral-DG option (param-gated).

### VII. Project & Experiment Management

1.  **Document Standards:**
    *   Extract rules only from repository evidence.
    *   Link to canonical symbols, equations, units, and constants.
    *   Do not redefine symbols, equations, units, or constants in `NAMING_CONVENTIONS.md` or `OPEN_QUESTIONS.md`.
    *   Quote or condense from sources in `OPEN_QUESTIONS.md`.
    *   Do not restate math or numbers in `OPEN_QUESTIONS.md`.
2.  **File Management:**
    *   Always update canonical files in the `Derivation/` folder root upon new discoveries or confirmed experiment results.
    *   Update canonical files only after creating a `RESULTS_` file in the designated `Derivation/{domain}` folder.
    *   Use the `io_paths.py` helper for all outputs, artifact paths, and naming.
3.  **Experiment Lifecycle:**
    *   All new experiments must have a proposal file created first.
    *   Follow the specified template for proposal files: `Derivation/Writeup_Templates/PROPOSAL_PAPER_TEMPLATE.md`.
    *   Place proposal files in the correct domain folder: `derivation/{domain/topic folder}`.
    *   All completed experiments must have a results write-up.
    *   Follow specified standards for results write-ups: `Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md`.
    *   Place results files in the correct domain folder next to the corresponding proposal.
    *   All new experiments must be approved by Justin K. Lietz before running.
    *   Pre-register tags (e.g., `KG-noether-v1`) with proposal & schema.
    *   Approve manifest using script-scoped HMAC.
    *   Ensure `io_paths` policy and approvals are in effect for `VDM-A-022`.
4.  **Artifacts & Logging:**
    *   All experiment runs must produce a minimum of 1 figure, 1 CSV log, and 1 JSON log as artifacts.
    *   Emit PNG plot of $r(t)$, CSV of time series, JSON log with parameters and gate outcome for FRW continuity.
    *   Every figure must have CSV/JSON sidecars under `outputs/{figures,logs}/metriplectic` tagged `kgRD‑v1`.
    *   Use PNG/CSV/JSON artifacts with `common/io_paths.py` helper.
    *   Route failed gate artifacts to `failed_runs/`.
    *   Route artifacts from unapproved runs under `failed_runs/`.
    *   Pin artifacts (e.g., `RESULTS_Decoherence_Portals.md`).
    *   Log experiment results to DB.
    *   Log determinism receipts (checkpoint buffer hashes) for identity audits.
    *   Log measured $c$ for J-only (spectral) gates.
5.  **Failure Handling & Gates:**
    *   Emit a contradiction report if a gate fails.
    *   Make no claims if a gate fails.
    *   Perform JSON schema validation for experiment results.
    *   Use approval-gated tag `KG-energy-osc-v1`.
    *   Run `KG-noether-v1` as a cross-check.
    *   Use tag `KG-noether-v1` for Noether invariant tests.
    *   Stamp unapproved runs `{ engineering_only:true, quarantined:true }`.
    *   Quarantine unapproved runs for `VDM-A-022`.
    *   Establish and continuously run 'Physics Validation Task' within CI pipeline.
    *   Ensure automated, ongoing verification of all established physics tests.
    *   Ensure real-time detection of critical failures like tachyonic roots.
    *   Enforce failures for KG $\oplus$ RD metriplectic under `failed_runs/`.
    *   Document and log FFT round-off rationale for J-only.

### VIII. Interfaces & Protocols

1.  **GeometryProbeAdapter Protocol:**
    *   Implementations must provide a `prepare` method with the signature `(self, config: "GeometryRunConfig") -> None`.
    *   Implementations must provide a `load_checkpoint` method with the signature `(self, step: int) -> None`.
    *   Implementations must provide an `encode_concepts` method with the signature `(self, concepts: Sequence[str], layer_name: str) -> np.ndarray`.
    *   The `encode_concepts` method must return a NumPy array with the shape `(len(concepts), neurons)`.
2.  **Event Immutability:** All event objects (`BaseEvent`, `DeltaEvent`, `VTTouchEvent`, `EdgeOnEvent`/`EdgeOffEvent`, `SpikeEvent`, `DeltaWEvent`, `MotifEnterEvent`/`MotifExitEvent`, `ADCEvent`, `BiasHintEvent`, `HorizonActivityEvent`, `RouterSplitEvent`, `BudgetTick`) must be immutable (frozen dataclass).

## Key Highlights

* This document synthesizes core technical rules, constraints, and requirements, serving as commandments for development, validation, and documentation across the entire system.
* Equations of motion for continuous systems must be derived from Hamilton's principle, and conservation laws are fundamentally linked to symmetries via Noether's theorem.
* All fields explicitly marked as 'Y' in configuration or metrics tables must be present, with strict numeric, type, and range constraints enforced for data integrity and system stability.
* Critical numerical stability, such as the CFL constraint `cfl <= 0.5`, and accuracy requirements, like energy drift `<= 10^-12` for Noether invariants, are strictly enforced, with thresholds not to be silently relaxed.
* All Key Performance Indicators (KPIs) in `VALIDATION_METRICS.md` must pass for the physics validation CI task, establishing quantitative acceptance criteria and reproducible verification protocols.
* Core architectural principles prioritize implementing conservation laws, deriving continuum dynamics from discrete action principles, and enforcing a sparsity constraint where edits per degree of freedom per step are much less than one.
* The simulation loop mandates single-threaded, sequential steps with try-except wrappers; `VOID_STRICT=1` must re-raise exceptions for debugging, while `VOID_STRICT=0` performs silent no-ops on errors.
* Connectome structural plasticity (GDSP) must operate exclusively in sparse mode, strictly adhering to a 'no dense path whatsoever' policy to maintain efficiency and architectural constraints.
* All new experiments require proposal approval before running, and every experiment run must produce a minimum of one figure, one CSV log, and one JSON log as artifacts for reproducibility and analysis.
* All event objects, ranging from `BaseEvent` to `RouterSplitEvent`, must be immutable (frozen dataclass) to ensure data integrity throughout the system.

## Next Steps & Suggestions

* Investigate and validate the consistency and correctness of cross-domain couplings, specifically how physical fields (e.g., scalar field phi, memory field M) modulate plasticity mechanisms in `revgsp.py` and `gdsp.py`, and how `substrate.py` integrates these multi-scale fields.
* Perform a comprehensive code audit across all connectome and plasticity modules to rigorously enforce the 'no dense path whatsoever' policy, actively removing any remaining dense code branches, fallbacks, or inadvertently dense operations.
* Develop or enhance an automated real-time dashboard for all critical physics validation gates, providing immediate alerts and detailed reports for any deviations from specified tolerances and acceptance criteria, particularly for stability-critical metrics (e.g., energy drift, Mach constraints, tachyonic roots).
* Conduct a thorough review of all numeric constraints and stability tolerances across the technical specifications, consolidating them into a centralized, version-controlled system to ensure consistent application and prevent subtle integration issues across numerical methods and validation tests.

---

*Powered by AI Content Suite & Gemini*
