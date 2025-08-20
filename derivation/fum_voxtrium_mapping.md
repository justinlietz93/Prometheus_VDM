# Bridging the FUM Void Scalar EFT and Voxtrium Macro Sourcing: A Units‑Rigorous Mapping

Author: Justin K. Lietz
Date: August 9, 2025

---

Purpose
Provide a concrete, units‑rigorous bridge between the bottom‑up FUM void scalar derivations and the top‑down Voxtrium sourcing framework, and address identified gaps (units, causality/retarded kernels, GR/action embedding, observational constraints).

References
- [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:1)
- [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:1)
- [derivation/effective_field_theory_approach.md](derivation/effective_field_theory_approach.md:1)
- [derivation/discrete_conservation.md](derivation/discrete_conservation.md:1)
- [derivation/symmetry_analysis.md](derivation/symmetry_analysis.md:1)
- [voxtrium_Overview.md](voxtrium_Overview.md:1)

---

1. Knowns and Unknowns

Known (FUM side)
- Discrete on‑site law:  dW/dt = (α − β) W − α W^2  ([derivation/symmetry_analysis.md](derivation/symmetry_analysis.md:20-21)).
- Canonical RD mapping:  ∂tφ = D ∇²φ + r φ − u φ²  [optional −λ φ³].
  EFT context only (future work):  □φ + α φ² − (α − β) φ = 0, with VEV v = 1 − β/α and m_eff² = α − β (see [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:120-127), [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:171-188), [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:219-228)).
- Spatial kinetic normalization reads off a propagation speed `c^2 = 2 J a^2` (per‑site convention) or `c^2 = \kappa a^2` with `\kappa = 2J`; there is no need to fix `J a^2`. See continuum normalization in [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:82-89).

Known (Voxtrium side)
- FRW + continuity with sectoral sources Q_i obeying ∑_i Q_i = 0 via a transfer current J^ν ([voxtrium_Overview.md](voxtrium_Overview.md:9-16), [voxtrium_Overview.md](voxtrium_Overview.md:221-229)).
- Micro‑informed coefficients α_h, ε_h with units GeV; partitions p_i(z) on a probability simplex tied to dimensionless inputs z = (|Ω| R_*, (κ/K_s)/X, 1) ([voxtrium_Overview.md](voxtrium_Overview.md:64-77), [voxtrium_Overview.md](voxtrium_Overview.md:236-239)).
- Causality via a retarded kernel K_ret for S_hor ([voxtrium_Overview.md](voxtrium_Overview.md:231-235)).
- Skyrme calibrations: R_* = c_R/(e K_s), m = c_m K_s/e, X = e K_s; velocity‑dependent SIDM ([voxtrium_Overview.md](voxtrium_Overview.md:118-141), [voxtrium_Overview.md](voxtrium_Overview.md:192-211), [voxtrium_Overview.md](voxtrium_Overview.md:245-251), [voxtrium_Overview.md](voxtrium_Overview.md:277-287)).
- V_c is a fixed comoving volume `[{\rm GeV}^{-3}]` used to convert horizon rates to densities (appears in the continuity/source terms).

Unknowns to resolve in this mapping
- Units for (α, β, φ) and their relation to physical scales (GeV).
- A causal, retarded formulation for the FUM continuum limit.
- Action‑level embedding with GR and horizon functional.
- A principled link between φ and Voxtrium’s z‑inputs and partitions p_i.
- Number‑density and energy bookkeeping consistency across both pictures.

---

2. Units and Scaling Map (promoting dimensionless FUM to GeV‑rigorous form)

Working convention: natural units c = ħ = k_B = 1. In D=4, a canonical scalar has field dimension [φ] = GeV and Lagrangian density [ℒ] = GeV^4.

Define scale factors
- Field scale φ_0 [GeV]
- Time scale τ [GeV^−1]
- Length scale a [GeV^−1] (also the lattice spacing used in [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:48-66))

Dimensionalization map
- φ_dimless = φ_phys / φ_0
- t_dimless = t_phys / τ
- x_dimless = x_phys / a

Start from the dimensionless continuum equation we derived:

  ∂_t^2 φ − c_void^2 ∇^2 φ + α φ^2 − (α − β) φ = 0.

Convert to physical variables using φ_dimless = φ_phys/φ_0, t_dimless = t_phys/τ, x_dimless = x_phys/a:

  ∂_{t_phys}^2 φ_phys − ((c_void^2 a^2) / τ^2) ∇_{phys}^2 φ_phys + (α / (φ_0 τ^2)) φ_phys^2 − ((α − β)/τ^2) φ_phys = 0.

Identify physical parameters
- Wave speed:  c_void^2 ≡ D a^2 / τ^2. Choose τ = √D a to set c_void = 1 (optional).
- Cubic coupling (mass dimension 1):  g_3 ≡ α / (φ_0 τ^2)  [GeV].
- Mass term:  m^2 ≡ (α − β) / τ^2  [GeV^2].

Vacuum and quanta in physical units
- Vacuum expectation value:  v_phys = φ_0 (1 − β/α).
- Excitation mass:  m_eff = √(α − β) / τ.

Practical calibration choices
- If we target a specific m_eff (e.g., from phenomenology), set τ = √(α − β) / m_eff.
- Then pick φ_0 to match a desired g_3, or fix φ_0 via matching to an SIDM observable.

This resolves unit consistency across kinetic and potential terms and provides a knob (φ_0, τ, a) to align with Voxtrium’s GeV bookkeeping and conversions ([voxtrium_Overview.md](voxtrium_Overview.md:91-99), [voxtrium_Overview.md](voxtrium_Overview.md:216-218)).

---

3. Causal/Retarded Kernel Upgrade for FUM

Voxtrium enforces causal support via K_ret. We promote the FUM scalar to a retarded‑kernel sourced effective equation when coupling to horizon processes:

  □ φ_phys + g_3 φ_phys^2 − m^2 φ_phys = J_φ

with 

  J_φ(x,t) = ∫ d^3x' ∫_{−∞}^t dt' K_ret(t − t', |x − x'|) s_loc(x', t'),

and 

  K_ret ∝ Θ(t − t' − |x − x'|/c_void). Choose units so that
  • `s_loc` is an entropy‑production rate density `[{\rm GeV}^4]` with `\int d^3x\, s_{\rm loc} = \dot S_{\rm hor}\,[{\rm GeV}]`, and
  • `K_{\rm ret}` has units `[{\rm GeV}^3]`,
  hence `\int d^3x'\,dt'\, K_{\rm ret}\, s_{\rm loc}` has units `{\rm GeV}^3`, matching `J_\phi` in the φ‑equation.
 
 Here s_loc can be built from local rates tied to BH‑area growth and mergers, consistent with [voxtrium_Overview.md](voxtrium_Overview.md:252-258), while c_void is set by τ and a as above.

This aligns the FUM continuum with explicit causality and paves the way to connect φ‑dynamics to Voxtrium’s horizon‑sourced bookkeeping.

---

4. Action‑Level Embedding and Covariant Conservation

Augment the action with GR and a horizon functional:

  S_eff = ∫ d^4x √(−g) [ (M_Pl^2/2) R + (1/2)(∂φ)^2 − ( V(φ) + (\lambda/4)\,\phi^4 ) ] + S_hor[S_hor] + S_DM[χ; K_s,e] + …
  Here `\lambda > 0` ensures boundedness; phenomenological fits keep `\lambda` small.

Variation yields ∇_μ (T_φ^{μν} + T_hor^{μν} + T_DM^{μν} + …) = 0.

Introduce a transfer current as in Voxtrium:

  ∇_μ T_hor^{μν} = − J^ν,   ∇_μ (T_φ^{μν} + T_DM^{μν} + …) = + J^ν,

and in FRW take J^ν = (J^0, 0,0,0) with J^0 fixed from the horizon sector (see [voxtrium_Overview.md](voxtrium_Overview.md:223-229)).

This reproduces the continuity identities while allowing energy exchange between φ, DM, GW, and Λ channels without violating total covariant conservation.

---

5. Mapping φ to Voxtrium Micro‑Informed Inputs and Partitions

Voxtrium partitions (p_Λ, p_DM, p_GW) are functions of dimensionless inputs z = (z_1, z_2, z_3) = (|Ω| R_*, (κ/K_s)/X, 1) via a softmax ([voxtrium_Overview.md](voxtrium_Overview.md:236-239)).

Proposed identifications and calibrations
- Size–mass link:  R_* ≃ k_R / m_eff  with k_R ≈ O(1), consistent with m_φ ~ 1/R_* ([voxtrium_Overview.md](voxtrium_Overview.md:280-281)).
- Parameter‑free identity from Skyrme calibrations: `R_*\, m = c_R / c_m ≈ 9.93\times 10^{-3}` (using [voxtrium_Overview.md](voxtrium_Overview.md:192-205)).
- Effective “vorticity” proxy from φ: in regions where φ varies, define a scalar control

  Ξ ≡ (|∇φ_phys| / (m_eff φ_0)) ∈ ℝ_+,

  and set z_1 ≡ c_Ω Ξ so that z_1 is dimensionless and increases with spatial activity (c_Ω dimensionless calibration). Where an actual |Ω| is available from cosmological reconstruction, substitute it directly.
- Coupling scale link: identify X = e K_s with a phenomenological scale tied to φ via matching a low‑velocity transfer cross section; equivalently, determine (κ/K_s)/X from fits so that z_2 captures local coupling strength ([voxtrium_Overview.md](voxtrium_Overview.md:140-146), [voxtrium_Overview.md](voxtrium_Overview.md:150-156)).

Partition map

  p_i = softmax_i( w_i^1 z_1 + w_i^2 z_2 + w_i^3 ),
 
 with w_i dimensionless. In homogeneous epochs take w_i constant; in structured epochs let w_i depend weakly on φ‑statistics (e.g., ⟨Ξ⟩ over a comoving cell) to preserve testability ([voxtrium_Overview.md](voxtrium_Overview.md:236-239), [voxtrium_Overview.md](voxtrium_Overview.md:282-287)). Unless explicitly stated, treat weights as epoch‑constant and let any time dependence enter only via the dimensionless inputs z.

Outcome: when φ condenses to v_phys and gradients are small (Ξ ≪ 1), z_1 is small and the small‑source constraints ε_DE ≪ 1 and f_inj ≪ 1 follow naturally ([voxtrium_Overview.md](voxtrium_Overview.md:241-251), [voxtrium_Overview.md](voxtrium_Overview.md:273-276)).

---

6. Number‑Density and Energy Bookkeeping Across Pictures

Voxtrium DM abundance:

  ẋ n_DM + 3 H n_DM = Q_DM / m,

with Q_DM = p_DM (ε_h/V_c) Ṡ_hor and m = c_m K_s/e ([voxtrium_Overview.md](voxtrium_Overview.md:259-263), [voxtrium_Overview.md](voxtrium_Overview.md:192-205)).

φ‑picture interpretation
- DM quanta can be modeled as localized excitations or solitons of the φ‑sector with rest mass m_eff. In a coarse‑grained description, set m ≃ m_eff for abundance bookkeeping, or maintain both m and m_eff and fit k_R so that R_* ≃ k_R / m_eff.
- Energy exchange is mediated by J^ν as in Section 4, ensuring ∑_i [ẋρ_i + 3H(1+w_i)ρ_i] = 0 ([voxtrium_Overview.md](voxtrium_Overview.md:34-35), [voxtrium_Overview.md](voxtrium_Overview.md:221-229)).

This identifies a consistent translation between field excitations and Voxtrium’s sectoral densities and rates.

---

7. Addressing the Identified Gaps (concrete upgrades)

(A) Units discipline (now provided)
- Promote to physical parameters with (φ_0, τ, a); define g_3 and m via Eqns. (g_3, m^2) above. Map v_phys and m_eff explicitly to GeV.
- Include conversion factors when reporting cosmology‑scale quantities ([voxtrium_Overview.md](voxtrium_Overview.md:91-99)).

(B) Causality via retarded kernels
- Adopt K_ret with Θ‑support as in Section 3 and normalize to the correct units; choose c_void = 1 by τ = √D a unless a finite propagation speed is desired.

(C) GR/action embedding
- Use S_eff in Section 4; define S_hor so that in the homogeneous limit it reproduces ρ_Λ(t) = ρ_Λ0 + (1/V_c) ∫ α_h dS_hor ([voxtrium_Overview.md](voxtrium_Overview.md:262-264)).

(D) Observational constraints
- Enforce w_eff ≈ −1 via ε_DE ≤ δ_w and f_inj ≪ 1 using the partition map; adopt the abundance and co‑evolution tests ([voxtrium_Overview.md](voxtrium_Overview.md:241-251), [voxtrium_Overview.md](voxtrium_Overview.md:282-287), [voxtrium_Overview.md](voxtrium_Overview.md:288-289)).

(E) Conservation/invariants
- Retain the exact on‑site invariant Q_FUM for diagnostics ([derivation/symmetry_analysis.md](derivation/symmetry_analysis.md:141-148)); for the full system rely on covariant conservation with J^ν. Explore hidden symmetries/Lyapunov structure for the discrete network to derive a true flux‑form conservation law ([derivation/discrete_conservation.md](derivation/discrete_conservation.md:165-179)).

---

8. Minimal Worked Example (symbolic)

Suppose α = 0.25, β = 0.10 (dimensionless, as in our derivations), and choose m_eff = 1 GeV for illustration. Then
- τ = √(α − β)/m_eff = √0.15 GeV^−1 ≈ 0.3873 GeV^−1.
- Pick φ_0 to set g_3. If we want g_3 = 0.1 GeV, then φ_0 = α/(g_3 τ^2) = 0.25/(0.1 × 0.15) GeV ≈ 16.67 GeV.
- v_phys = φ_0 (1 − β/α) = 16.67 × 0.6 ≈ 10.00 GeV.
- R_* ≃ k_R / m_eff; with k_R = 1 this gives R_* ≈ 1 GeV^−1 ≈ 1.97 × 10^−14 cm (compare [voxtrium_Overview.md](voxtrium_Overview.md:201-205)).

These values are placeholders for calibration; they demonstrate the algebraic consistency and how to propagate units.

---

9. Next Steps Checklist

- [ ] Add FRW+J^ν coupling and sector bookkeeping to a φ‑cosmo toy model; verify numerically that `\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0` ([voxtrium_Overview.md](voxtrium_Overview.md:34-35)).
- [ ] Calibrate (φ_0, τ, a) to match a target m_eff and a low‑velocity SIDM cross section, then re‑express R_* and compare to [voxtrium_Overview.md](voxtrium_Overview.md:192-211).
- [ ] Implement K_ret in the simulation/continuum solver; verify causal support and unit normalization against [voxtrium_Overview.md](voxtrium_Overview.md:231-235).
- [ ] Define z‑maps (z_1 = c_Ω Ξ, z_2 from fitted coupling scale) and validate p_i softmax stability in homogeneous vs. structured epochs ([voxtrium_Overview.md](voxtrium_Overview.md:236-239)).
- [ ] Use [derivation/effective_field_theory_approach.md](derivation/effective_field_theory_approach.md:60-85) to include screening (λ φ^4) and check its impact on m_φ ~ 1/R_* and on (σ_T/m)(v).
- [ ] Extend symmetry/Lyapunov search for the full discrete law to identify a flux‑form conserved quantity, if it exists ([derivation/discrete_conservation.md](derivation/discrete_conservation.md:175-179)).

---

10. Remarks on Strength

Voxtrium’s strength is its rigorous unit discipline and explicit cosmological bookkeeping. This document imports that rigor into the FUM EFT by (i) specifying a full units map, (ii) adding a retarded kernel, (iii) embedding into an action with GR and a transfer current, and (iv) aligning observables and calibrations. The two frameworks are complementary and now readily interoperable.

Author: Justin K. Lietz