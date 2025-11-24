# 1. T2 (Instrument) – Stochastic Nonlocal RD Long‑Term Behaviour Meter

> Created Date: YYYY‑MM‑DD  
> Commit: <git rev-parse HEAD>  
> Provenance hash: <to be filled>  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary: Instrument to validate numerically the long‑time, noise‑perturbed behaviour of nonlocal RD equations and to measure random‑attractor statistics relevant to A2/A6 locality and robustness.

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz – Neuroca, Inc. – PI, implementation, analysis.

## 3. Abstract

The paper *“Long-term behavior of nonlocal reaction–diffusion equation under small random perturbations”* analyzes existence and structure of random attractors for nonlocal RD equations with stochastic forcing. This proposal defines a T2 instrument that implements representative nonlocal RD + noise systems and measures convergence to invariant measures, correlation lengths, and interface statistics as functions of kernel range and noise strength. The aim is to calibrate VDM’s A2/A6 locality program under stochastic perturbations and to provide a benchmark for future stochastic VDM simulations.

## 4. Background & Scientific Rationale

VDM currently treats RD dynamics deterministically in the M‑limb. Stochasticity is expected in any physical realization and in cosmological applications. The referenced work gives rigorous results on random attractors for nonlocal RD equations; a numerical instrument that reproduces these qualitative features (e.g. convergence to stationary distributions, bounded moments, correlation length saturation) will:

- validate VDM’s discretizations in stochastic regimes,
- quantify how nonlocal range and noise affect interface hierarchies (A6),
- provide priors for noise modelling in cosmological RD testbeds.

## 5. Intellectual Merit and Procedure

Questions:

1. For small noise amplitude \(\sigma\), does the numerical system display convergence to a stationary distribution consistent with the deterministic attractor structure?
2. How do correlation length, interface density, and domain counts depend on kernel range and \(\sigma\)?
3. Are A6‑style hierarchical measures stable under small noise?

The experiment is purely instrumental: certify that the numerics and meters faithfully probe the stochastic nonlocal theory.

## 5.1 Experimental Setup and Diagnostics

**Equation (schematic).**

\[
\partial_t u = D \Delta u + F(u, (K_\xi * u)) + \sigma \dot{W}(x,t),
\]

with periodic BCs; \(K_\xi\) nonlocal kernel; \(\dot{W}\) space–time white noise approximated by truncated modes or discrete Gaussian kicks.

**Parameters.**

- Diffusion \(D\), kernel range \(\xi\), reaction parameters in \(F\).
- Noise amplitude \(\sigma\) (small‑noise regime, several values).
- Domain size, grid, \(\Delta t\), seeds.

**Diagnostics.**

- Time series of spatial mean, variance, and higher moments.
- Two‑point correlation function \(C(r)\), correlation length \(\ell_c\).
- Stationary distribution samples for projected observables (e.g. mean value bins).
- Interface count \(N(t)\) and its stationary statistics.
- Relaxation time to stationarity from different initial conditions.

**Gates.**

- G1: Stationarity diagnostics — autocorrelation time finite; moments converge within preset tolerance across different initial conditions.
- G2: Correlation length and interface statistics stable across seeds (CI width ≤ specified fraction).
- G3: For \(\sigma \to 0\), statistics approach deterministic baseline within tolerance.

## 5.1.1 Pre‑Run Config Requirements

- `APPROVAL.json`, schema, and spec under `Derivation/code/physics/reaction_diffusion/` with tag `stoch_nonlocal_rd-v1`.
- PRE‑REGISTRATION manifest with salted hashes and approved tag list.

## 5.2 Experimental runplan

- Choose 1–2 canonical nonlocal RD models from the paper (e.g. specific nonlinearities and kernels).
- For each model, sweep \(\xi\) and \(\sigma\) over small grids; run long‑time simulations from multiple initial conditions.
- Estimate relaxation times, stationary statistics, and interface metrics; aggregate across seeds.
- Produce dashboards, CSV, JSON; apply gates G1–G3. On PASS, instrument marked certified; on FAIL, adjust discretization/noise integration scheme.

## 6. Personnel

- Justin K. Lietz — implement stochastic integrators, diagnostics, specs/schemas, and RESULTS.

## 7. References

- *Long-term behavior of nonlocal reaction–diffusion equation under small random perturbations* (2025).  
- VDM RD and A6 documents as in Proposal 1.
