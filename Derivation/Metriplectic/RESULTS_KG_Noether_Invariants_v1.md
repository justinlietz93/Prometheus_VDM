# KG Noether Invariants - Discrete Energy & Momentum Conservation (Periodic BCs)

> Author: Justin K. Lietz  
> Date: 2025-10-08  
> Tag: KG-noether-v1  
> Domain: Metriplectic (J-only linear KG sector)
>
> TL;DR - This RESULTS page documents conservation of the Klein–Gordon discrete Noether invariants (energy and spatial translation momentum) under the Störmer–Verlet (leapfrog) integrator on a 1D periodic lattice. Both invariants are conserved to machine precision; observed per-step drifts are O(1e−17), far beneath the acceptance gate (≤ 1e−12 or 10 ε √N) and the reversibility test indicates exact round-trip recovery within numerical noise. This establishes that our discrete scheme faithfully realizes the continuous symmetries (time translation & spatial translation) required for subsequent coupled KG⊕RD diagnostics.

## Research Question

Does the symplectic Störmer–Verlet discretization of the linear periodic 1D KG equation preserve (i) discrete energy and (ii) discrete translation momentum to the expected symplectic accuracy bounds, demonstrating correct implementation of canonical Poisson flow in the J-only (hyperbolic) sector?

## Physical & Mathematical Background

Continuous 1D KG ($c = 1$ for brevity):

$$
\partial_{tt} \phi - c^2 \, \partial_{xx} \phi + m^2 \phi = 0
$$

Time translation symmetry ⇒ conserved energy:

$$
E = \int \left( \tfrac{1}{2}\pi^2 + \tfrac{1}{2} c^2 (\partial_x \phi)^2 + \tfrac{1}{2} m^2 \phi^2 \right) dx
$$

Space translation symmetry ⇒ conserved momentum:

$$
P = \int \pi\,\partial_x \phi\,dx
$$

Discretization with spectral periodic derivatives (grid spacing $\Delta x$, $N$ sites) and Störmer–Verlet time stepping introduces a leapfrog staggering. The discrete Noether invariants used:

$$
E_d = \tfrac{1}{2}\|\pi_{n+1/2}\|^2 + \tfrac{1}{2}\langle \phi_{n+1}, K\,\phi_n \rangle, \quad K\phi = -c^2 \Delta_h \phi + m^2 \phi
$$

$$
P_d = \langle \pi_{n+1/2}, \nabla_h (\tfrac{1}{2}(\phi_{n+1}+\phi_n)) \rangle
$$

These are exactly conserved for the linear system in exact arithmetic with periodic boundaries.

## Methods

- Runner: `Derivation/code/physics/metriplectic/kg_noether.py`
- Spec: `Derivation/code/physics/metriplectic/specs/kg_noether.v1.json` containing grid ($N=256$, $\Delta x=1.0$), parameters ($c=1$, $m=1$, tag, seed_scale), $\Delta t$ sweep; selected $\Delta t = 0.005$.
- Integration: 512 Störmer–Verlet steps.
- Random initial field & momentum with small amplitude (seed_scale=0.05) to avoid aliasing and maintain linear regime.
- Metrics captured every step for E_d and P_d midpoints; per-step absolute drift recorded.
- Reversibility test: integrate forward 512 steps, then backward 512 steps (dt → −dt) and measure sup-norm difference.
- Approval: tag `KG-noether-v1` pre-registered with proposal & schema; manifest approved using script-scoped HMAC.

## Gates

| Gate | Criterion |
|------|-----------|
| Energy drift | $\max \Delta E \le 10^{-12}$ or $\max \Delta E \le 10\,\epsilon\sqrt{N}$ |
| Momentum drift | $\max \Delta P \le 10^{-12}$ or $\max \Delta P \le 10\,\epsilon\sqrt{N}$ |
| Reversibility | $\|\Delta\|_{\infty} \le 10^{-10}$ |

For $N = 256$: $\sqrt{N}=16$, machine epsilon (float64) $\epsilon \approx 2.22\times10^{-16}$ ⇒ $10\epsilon\sqrt{N} \approx 3.55\times10^{-15}$.

## Results (KG-noether-v1)

Observed metrics:

- $\max \Delta E \approx 8.33\times10^{-17}$ ($\ll 10\,\epsilon\sqrt{N}$ and $\ll 10^{-12}$)
- $\max \Delta P \approx 2.60\times10^{-17}$ ($\ll 10\,\epsilon\sqrt{N}$ and $\ll 10^{-12}$)
- Reversibility $\|\Delta\|_{\infty} \approx 0$ (below $10^{-12}$ numerical noise floor)

Conclusion: All gates satisfied with wide margin; conservation is limited only by floating-point rounding (backward error $\mathcal{O}(\epsilon)$).

## Artifacts

- Figure: `Derivation/code/outputs/figures/metriplectic/20251008_184547_kg_noether_energy_momentum__KG-noether-v1.png`
- CSV: `Derivation/code/outputs/logs/metriplectic/20251008_184547_kg_noether_energy_momentum__KG-noether-v1.csv`
- JSON log (embedded in stdout; canonical path if added later) can be produced via rerun with same spec (approval locked).

## Interpretation - What This Test Proves

1. Symmetry Fidelity: Demonstrates discrete realization of continuous time and space translation symmetries - validating that the implemented Poisson bracket (J-only dynamics) is numerically faithful.
2. Baseline Integrity: Establishes a high-precision baseline invariant pair (E_d, P_d) for detecting future coupling defects when RD (metric M) is added; any drift beyond the O(ε) envelope flags regression.
3. Reversibility Quality: Near-exact round-trip confirms symplectic time-stepping integrity and absence of hidden damping/injection in the integrator pipeline.
4. Spectral Operator Sanity: Using spectral Laplacian and gradient, invariants hold; ensures no discretization phase error is accumulating that would spoil momentum conservation.
5. Policy Trust Stamp: Passing under approved tag conditions shows pipeline gating (proposal + schema + HMAC) allows only vetted invariants into canon; strengthens reproducibility and audit trail.

## Limitations & Next Steps

- Nonlinear Extensions: Current test is linear KG; inclusion of nonlinear self-interaction (e.g., $\lambda \phi^4$) requires modified discrete energy and potential alias-handling.
- Coupled KG⊕RD: Future mixed J+M runs must monitor whether dissipative channel perturbations preserve Poisson part invariants within expected interaction corrections.
- Higher Dimensions: 1D periodic lattice; extension to 2D/3D requires checking spectral shell treatment and potential anisotropy issues.
- Long-Time Behavior: 512 steps at dt=0.005 is modest; long-term backward error analysis could quantify modified Hamiltonian proximity.

## References

- Hairer, E., Lubich, C., & Wanner, G. (2006). *Geometric Numerical Integration*. Springer.
- Sanz-Serna, J. M., & Calvo, M. P. (1994). *Numerical Hamiltonian Problems*. Chapman & Hall.
- Morrison, P. J. (1986). A paradigm for joined Hamiltonian and dissipative systems. *Physica D*.

## Approval Trace

- Manifest: `Derivation/code/physics/metriplectic/APPROVAL.json` (tag KG-noether-v1)
- Schema: `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json`
- Proposal: `Derivation/Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md`
- Approval Key (HMAC): matches DB secret with message `metriplectic:kg_noether:KG-noether-v1`

---

*End of RESULTS report.*
