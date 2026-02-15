<!-- White Paper Proposal Template

ATTENTION! Proposal documents should be whitepaper-grade with full structure, explicit gates, and provenance.
This file is authored to follow the repository template as closely as possible while staying within a T1 scope.
-->

# 1. T1 - Horizon-as-Domain-Wall Leakage Meter (Proto-model)

> **Created Date:** 2026-02-15  
> **Commit:** UNKNOWN (not available in this sandbox)  
> **Salted hash:** TBD (generated at commit time; store salt + hashes in prereg JSON)  
> **Proposer contact(s):** (justin@neuroca.ai)  
> **License:** See LICENSE in repository  
> **Short summary (one sentence TL;DR):** This proposal defines a proto-model and runner scaffold to test whether CF8 domain-wall leakage (residual mass / tunneling overlap) can serve as a controlled, falsifiable *horizon one-way projection* mechanism with a temperature-like emission proxy.

***Practical provenance pattern***

- Compute salted hashes with a random salt; store `base_sha256`, `salt_hex`, `salted_sha256` in the prereg.
- Commit prereg.
- Optional: timestamp the tag externally (OpenTimestamps/RFC3161) for independent dating.

***Avoid circularity***

- No external GR/QFT identities are assumed as axioms.
- Hawking-temperature matching is treated as an *aspirational derived-limit check*, not as a pass criterion for the T1 gates.

---

## 2. List of proposers and associated institutions/companies

- **Justin K. Lietz** — PI / implementer / approver (as applicable per authorization policy).

---

## 3. Abstract

This proposal introduces a controlled numerical experiment family designed to test a specific identification: that a one-way information-stripping boundary in VDM can be instantiated by a CF8-style domain wall with localized zero-modes and exponentially suppressed bulk leakage. The work is scoped as a **T1 proto-model**: it does not claim astrophysical black holes are already derived, but instead builds a reproducible instrumented runner that (i) constructs domain-wall backgrounds, (ii) injects wavepackets across the boundary, (iii) measures projection onto localized modes and leakage back into the exterior, and (iv) reports a temperature-like emission proxy derived from the leakage spectrum. The primary deliverable is a runner + metrics + gates that can later be upgraded to T2 (instrument certification) and then to a T3/T4 phenomenon claim.

---

## 4. Background & Scientific Rationale

### 4.1 Canonical prerequisites (already in-repo)

This proposal is downstream of:

- **Metriplectic program axioms (A0–A7)** (closure, locality, symmetry, J/M split, entropy law, measurability).
- **CF8 (Spinor Emergence / Domain Wall Fermions)**: domain walls support localized modes and exponentially small overlap/leakage between separated walls.
- **Tachyonic condensation / tube interior results** (where applicable): provide a mechanism for stable condensed regions and boundary formation.

### 4.2 The gap this proposal addresses

CF8 provides domain-wall mathematics and numerical behavior in the context of emergent spinors. What is not formalized as a *runner-backed, gate-tested instrument* is the following package:

1. A boundary treated operationally as **one-way projection** (external-to-internal vs internal-to-external asymmetry).
2. A measurable **leakage spectrum** (residual overlap / tunneling) that can be summarized as a **temperature-like emission proxy**.
3. A controlled mapping from wall parameters (thickness, separation, coupling) to leakage rate(s), with reproducible uncertainty.

This proposal focuses on (1)–(3) as a proto-model, without assuming GR horizons.

### 4.3 Scientific motivation

If a domain-wall boundary in VDM can reliably implement a one-way stripping/projection map while producing an approximately thermal leakage spectrum, then the identification “horizon-like boundary = metriplectic domain wall” becomes testable in a controlled sandbox. This gives a disciplined bridge from CF8 (microstructure) toward Gravity/Cosmology branches, without importing external primitives.

---

## 5. Intellectual Merit and Procedure

### 5.1 Experimental Setup and Diagnostics

**System under study:** a lattice field configuration with a tunable domain-wall background and injected excitations.

**Independent variables (planned sweep axes):**

- Wall thickness parameter (e.g., $\,\xi$) and amplitude scale (background vacua values).
- Effective separation or “barrier width” ($L$) for a two-wall configuration (optional control).
- Injection packet parameters (center, width, carrier wavenumber $k_0$, amplitude).
- J/M composition choice (J-only, M-only, JMJ Strang) to separate reversible transport from dissipative stripping.

**Dependent variables (primary observables):**

- **Projection fraction** onto localized wall modes (defined operationally via overlap with a numerically extracted localized basis).
- **Leakage rate** (time-decay constant of localized-mode energy or probability into bulk exterior, fit on a declared window).
- **Emission proxy spectrum**: spectral density of leaked signal in the exterior region.

**Diagnostics required (count + outputs):**

- 1× localized mode extractor (basis build / SVD / eigen-solve) → `modes.npz` + `modes.json`
- 1× projection meter (overlap time-series) → `projection.csv` + `projection.json`
- 1× leakage fit (rate + CI) → `leakage_fit.json`
- 3× figures (minimum): space-time heatmap, projection vs time, leakage-spectrum plot.

**New scripts required (paths to be created in the repository):**

- `Derivation/code/physics/gravity/horizon_domainwall/run_horizon_wall_leakage.py`
- `Derivation/code/physics/gravity/horizon_domainwall/metrics.py`
- `Derivation/code/physics/gravity/horizon_domainwall/schemas/horizon_wall_leakage.schema.json`
- `Derivation/code/physics/gravity/horizon_domainwall/specs/horizon_wall_leakage.v1.json`

### 5.1.1 Pre-Run Config Requirements

To align with approval/authorization policy, the runner should be paired with:

- `Derivation/code/physics/gravity/horizon_domainwall/APPROVAL.json`
- `Derivation/code/physics/gravity/horizon_domainwall/schemas/horizon_wall_leakage.schema.json`
- `Derivation/code/physics/gravity/horizon_domainwall/specs/horizon_wall_leakage.v1.json`

The schema must enumerate all parameters with units/normalization and disallow undeclared keys.

### 5.2 Methods / Protocol

**High-level procedure (per run):**

1. **Construct background:** initialize field with a single wall (and optionally a paired wall) using the CF8 background profile.
2. **Extract localized basis:** numerically identify localized modes (restricted operator / eigenmodes) on the wall neighborhood.
3. **Inject excitation:** create a wavepacket on one side and evolve under a declared stepper (J-only, M-only, or JMJ Strang).
4. **Measure projection + leakage:** compute overlap onto localized basis each step; compute exterior-region flux and spectrum.
5. **Fit leakage rate:** fit an exponential tail on a pre-registered time window; report CI via bootstrap or multi-seed replicate.
6. **Gate checks:** verify global gates (degeneracies, H-theorem where relevant, locality where relevant) and run-specific gates below.

**Controls / ablations (required):**

- **No-wall control:** same injection with homogeneous background; projection fraction must be consistent with zero within tolerance.
- **Wall-removed control:** interpolate wall amplitude to zero; verify projection collapses.
- **Integrator swap:** at least two steppers (e.g., symplectic vs non-symplectic) to ensure leakage is not a numerical artifact.

### 5.3 Acceptance gates and thresholds (T1)

Because this is T1, gates focus on *instrument sanity* rather than astrophysical matching.

**G0 (Artifacts):** every run emits `metrics.json`, `trace.csv`, `gates.json`, and ≥3 figures with matching CSV/JSON sidecars.

**G1 (Localization):** extracted localized modes satisfy a declared localization metric (e.g., ≥90% of norm inside a fixed wall neighborhood).

**G2 (One-way asymmetry under M):** under a configuration where M dominates stripping, inward-crossing projection fraction exceeds outward-crossing projection fraction by a declared factor (e.g., ≥2×), holding injection energy fixed.

**G3 (Leakage exponential tail):** leakage fit achieves $R^2\ge 0.98$ on the pre-registered window and is stable (≤10% shift) under a ±20% window perturbation.

**G4 (Resolution robustness):** leakage rate changes by ≤15% under a two-grid refinement test (e.g., $\Delta x \to \Delta x/2$ with consistent CFL policy).

**G5 (Global gates):**

- J/M degeneracy residuals remain below the global tolerance throughout.
- H-theorem holds for M-only steps (where evaluated).
- Locality audit passes for J-only (hyperbolic) runs.

### 5.4 What counts as “success” at T1

PASS is defined strictly by G0–G5. Any discussion of Hawking-like scaling is recorded as exploratory diagnostics, not as a PASS condition.

---

## 6. Broader impacts / ethics / safety

- No human-subject data.
- Compute budget controlled by declared grid/time limits.
- Explicitly avoids anthropomorphic framing; “information stripping” is defined only via measurable projection + leakage observables.

---

## 7. Risks, criticisms, and kill plans

**Risk 1: Numerical leakage mistaken for physical leakage.**

- Mitigation: integrator swap + two-grid test + ablation controls.
- Kill: if G4 fails or leakage rate varies wildly with stepper choice.

**Risk 2: “One-way” behavior is an artifact of initial/boundary conditions.**

- Mitigation: enforce symmetric ICs across wall; flip injection side; rerun.
- Kill: if asymmetry disappears under symmetric construction.

**Risk 3: Localized basis is ill-defined / non-robust.**

- Mitigation: specify basis extraction method and stability checks.
- Kill: if G1 fails consistently or basis changes discontinuously with small perturbations.

---

## 8. Expected artifacts (paths)

- `Derivation/code/outputs/logs/gravity/horizon_domainwall/<tag>/`  
  - `runs.csv`, `metrics.json`, `gates.json`, `fit/leakage_fit.json`
- `Derivation/code/outputs/figures/gravity/horizon_domainwall/<tag>/`  
  - `spacetime_field.png`, `projection_timeseries.png`, `leakage_spectrum.png`
- `Derivation/code/outputs/reports/gravity/horizon_domainwall/<tag>/`  
  - `CONTRADICTION_REPORT.json` on any gate fail

---

## 9. References (repository-internal)

- `Derivation/Complete-Formalisms/CF8_Spinor_Emergence_Domain_Wall_Fermions.md`
- `Derivation/Complete-Formalisms/CF4_Telegraph_Fisher_Causality.md` (locality/relaxation context)
- `Derivation/AXIOMS.md` (A0–A7)
- `Derivation/VALIDATION_METRICS.md` (global gate definitions)
- `Derivation/TIER_STANDARDS.md` (T0–T9 maturity ladder)

