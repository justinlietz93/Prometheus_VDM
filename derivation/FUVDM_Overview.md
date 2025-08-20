# FUVDM Overview

> Model class (canonical): First-order reaction–diffusion (Fisher/KPP)
>
> ∂t φ = D ∇² φ + r φ − u φ² [ − λ φ³ (optional stabilization) ]
>
> EFT/Klein–Gordon claims are quarantined under effective_field_theory_approach.md (Future Work). When referenced, m_eff = √(α−β); numeric value depends on α,β.

## Fundamental Discrete Law

dW/dt = (α − β) W − α W²

## Primary Continuum Description (Reaction–Diffusion)

∂t φ = D ∇² φ + r φ − u φ²  [ − λ φ³ optional ]

- Mapping: D = J a² (or D = (J/z) a² if neighbor-average), r = α, u = β.
- Stability: for r>0, φ=0 is dynamically unstable; homogeneous fixed point φ* = r/u is stable.

## EFT (Future Work)

See derivation/effective_field_theory_approach.md for second‑order dynamics and mass m_eff = √(α−β). Do not mix EFT claims into RD narrative.