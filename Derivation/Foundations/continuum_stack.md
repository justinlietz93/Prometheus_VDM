# Continuum Stack - Discrete → Continuum (RD baseline; EFT active, KPI-gated)

Tags: [PROVEN], [STRUCTURE], [DOC SYNC]

Purpose

- Provide the stepwise map from the discrete site model to continuum PDEs.
- Establish the RD branch as canonical for first‑order time dynamics; maintain EFT/KG (second‑order) as an active, KPI‑gated branch with explicit acceptance criteria.
- Fix nomenclature and parameter mapping reused across derivations and validations.

Assumptions/Parameters

- Lattice spacing a, coordination z (nearest neighbors).
- Coupling J (diffusive exchange scale).
- On‑site parameters α, β (logistic).
- Field W_i(t) on sites i; continuum field φ(x,t) after coarse‑graining.
- Units: time step τ_u, length a; RD uses first‑order ∂t φ; EFT uses second‑order ∂t² φ with c² from the discrete action.

Discrete law (nearest‑neighbor, logistic on‑site)

- Site ODE:
  dW_i/dt = (α - β) W_i - α W_i^2 + J Σ_{j∈nbr(i)} (W_j - W_i)
- Notes:
  - The exchange term preserves the lattice mean; signs ensure diffusion‑like smoothing.
  - For small amplitude about W ≈ 0, the kinetics are linearized by dropping -α W_i^2.

Continuum limit (stepwise)

1) Coarse‑grain W_i → φ(x,t) with x on a regular lattice, spacing a.
2) Write the discrete Laplacian in central‑difference form and expand:
   Σ_{j∈nbr(i)} (W_j - W_i) = a² ∇²φ + O(a⁴ ∇⁴φ)
3) Identify the continuum parameters:
   - Diffusion: D = J a² (site Laplacian) or D = (J/z) a² (neighbor‑average form)
   - Growth and saturation: r = α - β, u = α
4) Leading‑order RD PDE (canonical):
   ∂t φ = D ∇²φ + r φ - u φ²

PDE/Action/Potential branches

- RD branch [PROVEN, canonical]:
  - ∂t φ = D ∇²φ + r φ - u φ² with D = J a² (or (J/z) a²), r = α - β, u = α.
  - Closest discrete check: linear growth/dispersion and Fisher-KPP pulled‑front speed.
- EFT/KG branch [PLAUSIBLE, active]:
  - Second‑order time with action‑derived kinetic normalization:
    ∂t² φ + γ ∂t φ - c² ∇² φ + V′(φ) = 0, with c² = 2 J a² (per‑site) or c² = κ a², κ=2J (per‑edge).
  - Mass parameter follows m_eff² = V″(v) at the vacuum v; not used in RD validations.
  - See [kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:1) and [effective_field_theory_approach.md](Prometheus_VDM/derivation/effective_field_theory/effective_field_theory_approach.md:1).

Fixed points & stability (RD)

- Homogeneous fixed points: φ=0 and φ*= r/u (for r>0, φ*>0).
- Linear stability:
  - Around φ=0: σ = r - D k² (unstable for small k if r>0).
  - Around φ*: σ = -r - D k² < 0 for r>0 (stable).

Dispersion relations

- Continuum RD (Fourier mode k): σ(k) = r - D k². [PROVEN]
- Discrete lattice (mode index m on N sites, periodic):
  σ_d(m) = r - (4D/dx²) sin²(π m/N) with dx = L/N. Small‑k expansion recovers σ ≈ r - D k². [PROVEN]
- See validation script: [rd_dispersion_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:1) and doc [rd_dispersion_validation.md](Prometheus_VDM/derivation/reaction_diffusion/rd_dispersion_validation.md:1).

Front speed (Fisher-KPP)

- Theory: c_front = 2 √(D r). [PROVEN]
- Experiment: [rd_front_speed_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:1) and doc [rd_front_speed_validation.md](Prometheus_VDM/derivation/reaction_diffusion/rd_front_speed_validation.md:1).

Conservation or Lyapunov notes

- Diffusion decreases spatial variance; the reaction term sets carrying capacity φ* = r/u.
- Global positivity is preserved given nonnegative initial data under the canonical discretization. [PLAUSIBLE]
- Noether‑style invariants apply to the EFT action, not to the RD dissipative flow; see [symmetry_analysis.md](Prometheus_VDM/derivation/foundations/symmetry_analysis.md:1) for context. [SCOPE]

Numerical plan + acceptance (recap)

- Grids: N ∈ {1024, 2048}, domain length L≈200; CFL≈0.2.
- Acceptance gates:
  - Front speed: |c_meas - c_th| / c_th ≤ 6% and R² ≥ 0.9999 on the tracked front interval.
  - Dispersion: median relative error ≤ 2×10⁻³ and R²_array ≥ 0.999.
- Outputs auto‑routed to derivation/code/outputs/{figures,logs}/reaction_diffusion with timestamped names.
- See logs referenced in [LOG_20250824.md](Prometheus_VDM/derivation/DAILY_LOGS/LOG_20250824.md:1).

Units and normalization

- RD: choose units so that D and r have desired scales; rescale x→x/L, t→t/T as needed.
- EFT: keep c² = 2 J a² mapping explicit; units can set c=1 after identification. [REFERENCE]
- See [discrete_to_continuum.md](Prometheus_VDM/derivation/foundations/discrete_to_continuum.md:1) and status log [CORRECTIONS.md](Prometheus_VDM/derivation/CORRECTIONS.md:1).

Results (pointers)

- Front‑speed PASS and dispersion PASS recorded with figures/logs; see:
  - [rd_front_speed_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:1)
  - [rd_dispersion_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:1)
- Overview banner and dimensionless constants: [VDM_Overview.md](Prometheus_VDM/derivation/VDM_Overview.md:1).

Open questions

- Formal Lyapunov functional for the RD logistic‑diffusion flow on bounded domains. [NEEDS DATA]
- Quantitative criteria for when a second‑order EFT branch becomes necessary. [PLAUSIBLE]
- Coupling of memory‑steering overlays to the RD baseline; see [memory_steering.md](Prometheus_VDM/derivation/memory_steering/memory_steering.md:1). [PLAUSIBLE]

Provenance

- Kinetic/action normalization: [kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:1).
- Discrete→continuum baseline: [discrete_to_continuum.md](Prometheus_VDM/derivation/foundations/discrete_to_continuum.md:1).
- Status/edits: [CORRECTIONS.md](Prometheus_VDM/derivation/CORRECTIONS.md:1).
