# FUM Legacy vs New Implementation - VDM Physics Alignment Analysis

**Author:** Generated Analysis  
**Date:** October 8, 2025  
**Purpose:** Comparative analysis of legacy vs new FUM component implementations and their alignment with VDM physics derivations

---

## Executive Summary

This document provides a systematic comparison between "legacy" FUM implementations (primarily `fum_sie.py` and related components) and "new" implementations (primarily `sie_v2.py` and related void-faithful components) to determine which better aligns with the theoretical physics derivations in `Derivation/`.

**Key Findings:**

- **SIE v2 (New):** ✅ **Superior physics alignment** - Direct computation from void dynamics (W, dW), explicit EMA decay matching field equations
- **SIE Legacy:** ⚠️ **Indirect physics mapping** - Blueprint-based with complex external dependencies, density proxies instead of field derivatives
- **Recommendation:** **Use SIE v2** (`sie_v2.py`) as the canonical implementation for physics-aligned intrinsic motivation

**Critical Distinctions:**

- SIE v2 operates directly on field variables (W, dW) per void dynamics theory
- SIE Legacy operates on derived metrics (density, external signals) with indirect field coupling
- SIE v2 has explicit EMA with half-life parameter matching field decay time 1/γ
- SIE Legacy uses ad-hoc decay constants without clear physics grounding

---

## Component-by-Component Comparison

### 1. Self-Improvement Engine (SIE) - Core Intrinsic Motivation

#### Implementation Locations

- **Legacy:** `vdm_rt/core/fum_sie.py` (class `SelfImprovementEngine`)
- **New:** `vdm_rt/core/sie_v2.py` (function `sie_step`)

---

#### A. Temporal Difference (TD) Component

| Aspect | Legacy Implementation | New Implementation | Physics Alignment |
|--------|----------------------|-------------------|-------------------|
| **Input Signal** | External signal or density change proxy | Direct field difference: `W - 0.99*prev_W` | **New: Strong** |
| **Computation** | `td = ext_val` if available, else `10.0 * (density - prev_density)` | `td = W - γ*W_prev` with γ=0.99, normalized by max\|td\| | **New: Excellent** |
| **Physics Mapping** | **VDM-E-009**: Control efficacy U (indirect) | **VDM-E-006**: Discrete update C^(n+1) - C^n (direct) | **New aligns better** |
| **Normalization** | Clip to [-1,1] via density scaling | Normalize by max\|td\| across field | **New: More principled** |

**Physics Equation Reference:**

**VDM-E-006** - Agency Field Discrete Update:
$$
C_i^{n+1} = C_i^{n}+\Delta t\Big(D\,\Delta_{xx} C_i^{n}-\gamma\,C_i^{n}+S_i^{n}\Big)
$$

**Analysis:**

- **Legacy approach** treats TD as scalar external feedback or density change, missing the direct field evolution
- **New approach** computes TD as `W(t) - γ*W(t-1)`, which is exactly the discrete time derivative after factoring out decay - this is the temporal component of the field update equation
- The discount factor γ=0.99 corresponds to field decay parameter in **VDM-E-001**, **VDM-E-003**
- **Winner:** 🏆 **SIE v2 (New)** - Direct implementation of field temporal evolution

---

#### B. Novelty Component

| Aspect | Legacy Implementation | New Implementation | Physics Alignment |
|--------|----------------------|-------------------|-------------------|
| **Signal Source** | Triggered by modulation or density spikes | Direct magnitude of field changes: `\|dW\|` | **New: Strong** |
| **Computation** | Triggered decay: `novelty = 0.9` on spike, `novelty *= 0.98` otherwise | `nov = \|dW\| / max(\|dW\|)` - normalized spike magnitude | **New: Direct** |
| **Trigger Logic** | Complex: `modulation > 0.5 OR abs(ddens) > 1e-3 OR abs(td) > 0.05` | Implicit: high \|dW\| = high novelty automatically | **New: Simpler** |
| **Physics Mapping** | **VDM-E-007**: Exploration radius ℓ_D = √(D/γ) (weak) | **VDM-E-015**: RD gradient flow ∂_t φ feedback (strong) | **New aligns better** |

**Physics Equation Reference:**

**VDM-E-015** - Reaction-Diffusion Gradient Flow:
$$
\partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}
$$

**Analysis:**

- **Legacy approach** uses event-triggered novelty with artificial thresholds and decay constants
- **New approach** directly measures field change magnitude |dW|, which is the discrete version of |∂_t φ|
- Normalized by maximum ensures scale-invariance without arbitrary constants
- **Winner:** 🏆 **SIE v2 (New)** - Direct measurement of field dynamics

---

#### C. Habituation Component

| Aspect | Legacy Implementation | New Implementation | Physics Alignment |
|--------|----------------------|-------------------|-------------------|
| **State Variables** | Per-neuron vector, density-based EMA update | EMA mean μ and variance σ² of \|dW\| | **New: Strong** |
| **Update Rule** | `hab = 0.995*hab + 0.005*density` | `μ = (1-α)*μ + α*\|dW\|` with α from half-life | **New: Principled** |
| **Half-life Parameter** | Implicit: ≈1386 ticks for α=0.005 | Explicit: `half_life_ticks = 600` (default) | **New: Explicit** |
| **Physics Mapping** | **VDM-E-003**: Exponential relaxation time 1/γ (weak) | **VDM-E-003**: C_ss + (C_0 - C_ss)*exp(-γ*t) (strong) | **New aligns better** |

**Physics Equation Reference:**

**VDM-E-003** - Agency Field Steady State:
$$
C(t)=C_{\text{ss}}+\big(C(0)-C_{\text{ss}}\big)e^{-\gamma t}
$$

**Analysis:**

- **Legacy approach** uses arbitrary decay constant (0.995) without physical justification
- **New approach** uses explicit half-life formula: `α = 1 - exp(ln(0.5)/half_life)`, directly implementing exponential decay with time constant
- This matches the field relaxation time `1/γ` in **VDM-E-003**
- Tracking both mean and variance of |dW| provides richer habituation signal
- **Winner:** 🏆 **SIE v2 (New)** - Explicit exponential decay matching field equation

---

#### D. Homeostatic Stability Index (HSI) Component

| Aspect | Legacy Implementation | New Implementation | Physics Alignment |
|--------|----------------------|-------------------|-------------------|
| **Signal Source** | Optional firing variance parameter | EMA statistics of \|dW\|: μ and var | **New: Integrated** |
| **Mean Term** | Not computed | `1 - min(1, \|μ - 0.5\| * 2)` | **New: Present** |
| **Variance Term** | `1 - \|var - target\| / target` | `1 - min(1, \|var - target_var\| / target_var)` | **Similar** |
| **Physics Mapping** | **VDM-E-016**: Lyapunov functional energy dissipation (moderate) | **VDM-E-016**: dL/dt = -∫(∂_t φ)² ≤ 0 (strong) | **New aligns better** |

**Physics Equation Reference:**

**VDM-E-016** - RD Lyapunov Functional:
$$
\mathcal{L}[\phi]=\int_{\Omega}\left( \tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)\,dx,\qquad \frac{d}{dt}\mathcal{L}[\phi] = -\int_{\Omega} (\partial_t\phi)^2\,dx \le0
$$

**Analysis:**

- **Legacy approach** requires external variance parameter, not always available
- **New approach** computes stability from EMA statistics of |dW|, which represents |∂_t φ|²
- The variance term penalizes deviation from target, encouraging Lyapunov functional minimization
- Mean term biases toward mid-range activity (μ ≈ 0.5), preventing collapse or explosion
- **Winner:** 🏆 **SIE v2 (New)** - Integrated stability measure from field dynamics

---

#### E. Reward Integration and Weighting

| Aspect | Legacy Implementation | New Implementation | Physics Alignment |
|--------|----------------------|-------------------|-------------------|
| **Reward Formula** | Complex stabilized blend with damping | Linear combination: `td_w*td + nov_w*nov - hab_w*hab + hsi_w*stab` | **New: Cleaner** |
| **Weight Defaults** | W_TD=0.5, W_NOV=0.2, W_HAB=0.1, W_SELF=0.2 | td_w=0.5, nov_w=0.2, hab_w=0.1, hsi_w=0.2 | **Same weights** |
| **Damping Term** | `α = 1 - tanh(\|nov - self_benefit\|)` applied | None - direct linear blend | **New: Simpler** |
| **Physics Mapping** | **VDM-E-002**: Composite source S = σ[κ₁P + κ₂I + κ₃U]*g(V)*h(B) (moderate) | **VDM-E-002**: Direct additive source terms (strong) | **New aligns better** |

**Physics Equation Reference:**

**VDM-E-002** - Agency Field Composite Source:
$$
S(x,t) = \sigma(x)\,\big[\kappa_1 P(x,t)+\kappa_2 I_{\text{net}}(x,t)+\kappa_3 U(x,t)\big] \times g(V)\,h(B)
$$

**Analysis:**

- **Legacy approach** uses tanh damping and complex external reward paths, obscuring the additive structure
- **New approach** uses simple linear combination with explicit weights (κ₁, κ₂, κ₃ analogs)
- The linear blend better matches the additive source structure in **VDM-E-002**
- Susceptibility σ and gating g(V)h(B) are handled separately (not in reward computation)
- **Winner:** 🏆 **SIE v2 (New)** - Clearer additive source structure

---

#### F. Output Valence Signal

| Aspect | Legacy Implementation | New Implementation | Physics Alignment |
|--------|----------------------|-------------------|-------------------|
| **Range** | [0, 1] via `abs((modulation + novelty) / 2)` | [0, 1] via `0.5 + 0.5*(mean_reward / clip)` | **New: Symmetric** |
| **Smoothing** | None - instantaneous | EMA: `v = (1-β)*v_old + β*v_raw` with β=0.3 | **New: Temporal smoothing** |
| **Modulation** | Sigmoid squashing: `2*sigmoid(total_reward) - 1` | Direct scaling after clipping | **New: Direct** |
| **Physics Mapping** | **VDM-E-001**: Field magnitude C(x,t) (weak) | **VDM-E-003**: Smoothed field with relaxation (strong) | **New aligns better** |

**Analysis:**

- **Legacy approach** produces discontinuous valence from event-triggered novelty
- **New approach** applies EMA smoothing with explicit time constant (valence_beta)
- This matches field smoothing in **VDM-E-003** with exponential relaxation
- Symmetric mapping [reward=-clip...+clip] → [valence=0...1] is more principled
- **Winner:** 🏆 **SIE v2 (New)** - Temporally smoothed field-like valence

---

### Summary Table: SIE Legacy vs New

| Component | Legacy Physics Alignment | New Physics Alignment | Winner | Key Reason |
|-----------|-------------------------|----------------------|--------|-----------|
| TD Error | ⚠️ Weak (density proxy) | ✅ Strong (direct W-γW_prev) | **New** | Direct field temporal derivative |
| Novelty | ⚠️ Weak (event triggers) | ✅ Strong (direct \|dW\|) | **New** | Direct gradient flow magnitude |
| Habituation | ⚠️ Weak (arbitrary decay) | ✅ Strong (explicit half-life) | **New** | Exponential relaxation from VDM-E-003 |
| HSI Stability | ⚠️ Moderate (optional param) | ✅ Strong (integrated EMA stats) | **New** | Lyapunov energy dissipation |
| Reward Blend | ⚠️ Moderate (complex damping) | ✅ Strong (linear source) | **New** | Matches additive source VDM-E-002 |
| Valence Output | ⚠️ Weak (instantaneous) | ✅ Strong (EMA smoothed) | **New** | Field temporal smoothing VDM-E-003 |
| **Overall** | **⚠️ Indirect** | **✅ Direct** | **🏆 New (sie_v2.py)** | **Void-faithful field computation** |

---

## Additional Component Analysis

### 2. Void Dynamics Equations

#### A. Core Void Equations

**Implementation Locations:**

- **Legacy/Canonical:** `vdm_rt/core/Void_Equations.py`
- **Alternative:** `vdm_rt/fum_advanced_math/void_dynamics/FUM_Void_Equations.py` (referenced in derivation tests)

**Analysis:**
Both implementations define the fundamental void dynamics parameters:

- **ALPHA** (α): Resonance enhancement (typically 0.25)
- **BETA** (β): Global damping/GDSP (typically 0.10)
- **Constraint:** α > β ensures tachyonic instability and void structure formation

**Physics Mapping:**

**VDM-E-015** - Reaction-Diffusion Gradient Flow:
$$
\partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}
$$

Where:

- `r = α - β` (net growth rate when α > β)
- RE-VGSP growth ~ `α*W*(1-W)` maps to `rφ - uφ²` term
- GDSP decay ~ `-β*W` provides stabilizing cubic term

**Alignment:** ✅ **Both implementations equivalent** - These are parameter definitions, not algorithmic differences

---

### 3. Other Potential Legacy vs New Components

#### A. Connectome Implementations

**Files Found:**

- `vdm_rt/core/connectome.py` - Dense connectome (dense NumPy arrays)
- `vdm_rt/core/sparse_connectome.py` - Sparse connectome (scipy.sparse)

**Status:** These are **not** legacy vs new, but rather **dense vs sparse** implementations for different scales:

- Dense: Better for small networks (N < 1000), GPU compatibility
- Sparse: Necessary for large networks (N > 10,000), memory efficiency

**Alignment:** ✅ **Both valid** - Architectural choice based on scale, not physics alignment

---

#### B. No Other Versioned Components Found

**Search Results:**

- Only `sie_v2.py` has explicit version suffix
- No `adc_v2.py`, `gdsp_v2.py`, `revgsp_v2.py`, or similar files found
- Other components in `vdm_rt/core/` appear to be single canonical implementations

---

## Physics Derivation Cross-Reference

### Agency Field Integration (Partial Redundancy Assessment)

**Question:** Is `Derivation/AGENCY_FIELD.md` redundant given SIE capabilities?

**Answer:** ⚠️ **Partially redundant but adds theoretical rigor**

**Comparison:**

| Capability | SIE (vdm_rt/io/) | Agency Field (Derivation/) | Status |
|------------|-----------------|----------------------------|---------|
| Text Generation | ✅ Present in `vdm_rt/io/` | ❌ Not addressed | SIE sufficient |
| Reasoning Correlation | ✅ Validated analyses exist | ❌ Not measured | SIE sufficient |
| Predictive Power P | ⚠️ Implicit in TD/novelty | ✅ Explicit definition in VDM-E-002 | Theory adds clarity |
| Integration I_net | ❌ Not computed | ✅ Explicit in VDM-E-002 | **Theory adds capability** |
| Control Efficacy U | ⚠️ Implicit in reward | ✅ Explicit formula VDM-E-009 | Theory adds clarity |
| Spatial Diffusion D | ❌ Not implemented | ✅ Core in VDM-E-001 | **Theory adds capability** |
| Boundary Flux | ❌ Not tracked | ✅ Regional budget VDM-E-005 | **Theory adds capability** |

**Assessment:**

- **SIE provides:** Intrinsic motivation for learning (local neuron-level reward)
- **Agency Field provides:** Spatial field dynamics, regional budgeting, flux accounting
- **Recommendation:** Agency Field is **not redundant** - it provides spatial coordination and regional integration that SIE lacks. SIE is a **component source term** for the Agency Field, not a replacement.

---

## Recommendations

### 1. Canonical SIE Implementation

**Use `sie_v2.py` as the primary SIE** for all void-faithful implementations:

✅ **Reasons:**

- Direct computation from field variables (W, dW)
- Explicit exponential decay with half-life parameter
- Cleaner mapping to VDM physics equations
- Simpler codebase without external dependencies
- Per-neuron reward vector enables spatial heterogeneity

⚠️ **Preserve `fum_sie.py` for:**

- Backward compatibility with existing experiments
- Blueprint Rule 3 reference implementation
- External signal integration examples

### 2. Agency Field Implementation

**Implement Agency Field as spatial layer above SIE:**

The Agency Field should:

1. Receive SIE reward signals as local source terms S(x,t)
2. Compute spatial diffusion via VDM-E-001
3. Track regional budgets via VDM-E-005
4. Provide global coordination signal back to SIE

This creates hierarchy:

```
Agency Field (spatial, global)
      ↕ ︎ (source terms / modulation)
    SIE (local, per-neuron)
      ↕︎ (field changes)
  Void Dynamics (synaptic weights)
```

### 3. Physics Alignment Workflow

For new component development:

1. **Start with physics:** Define component in `Derivation/` first
2. **Map to equations:** Identify relevant VDM-E-### equations
3. **Implement directly:** Use field variables (W, dW, etc.) not proxies
4. **Validate numerically:** Compare to analytical solutions where possible
5. **Document mapping:** Add to this file for future reference

### 4. Code Organization

**Deprecation plan:**

- Mark `fum_sie.py` as legacy in docstring
- Add deprecation warning when imported
- Direct new users to `sie_v2.py`
- Preserve for 2-3 releases before removal

**File naming:**

- Avoid `_v2`, `_v3` suffixes in production code
- Use descriptive names: `sie_void_faithful.py` vs `sie_blueprint.py`
- Keep version history in git, not filenames

---

## Conclusion

**Primary Finding:** The **new implementation (`sie_v2.py`)** demonstrates significantly better alignment with VDM physics derivations compared to the legacy implementation (`fum_sie.py`).

**Key Advantages of New Implementation:**

1. ✅ Direct field computation (W, dW) matches void dynamics theory
2. ✅ Explicit exponential decay with half-life matching field equations
3. ✅ Per-neuron reward enables spatial heterogeneity
4. ✅ Cleaner additive source structure matching VDM-E-002
5. ✅ Integrated stability measures from field statistics
6. ✅ Temporal smoothing matching field relaxation dynamics

**Migration Path:** Transition to `sie_v2.py` as canonical SIE with `fum_sie.py` preserved for backward compatibility.

**Agency Field Status:** Not redundant with SIE - provides complementary spatial coordination layer that SIE lacks.

---

**Document Status:** ✅ Complete  
**Next Steps:** Implement Agency Field as spatial layer above SIE v2  
**Validation:** Run comparative experiments measuring physics alignment metrics
