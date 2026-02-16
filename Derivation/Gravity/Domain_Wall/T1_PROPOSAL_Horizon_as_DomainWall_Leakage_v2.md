<!-- White Paper Proposal Template

ATTENTION! Proposal documents should be whitepaper-grade with full structure, explicit gates, and provenance.
This file is authored to follow the repository template as closely as possible while staying within a T1 scope.
-->

# 1. T1 - Horizon-as-Domain-Wall Leakage Meter (Proto-model) — v2

> **Created Date:** 2026-02-15  
> **Commit:** 910d211  
> **Salted hash:** TBD (generated at commit time; store salt + hashes in prereg JSON)  
> **Proposer contact(s):** (justin@neuroca.ai)  
> **License:** See LICENSE in repository  
> **Short summary (one sentence TL;DR):** This proposal defines a proto-model and runner scaffold to test whether CF8 domain-wall capture + leakage (residual mass / tunneling overlap) can implement a controlled, falsifiable *horizon-like* one-way stripping mechanism, with a temperature-like emission proxy treated strictly as a descriptive diagnostic.

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

This proposal introduces a controlled numerical experiment family designed to test a specific operational identification: that a horizon-like, information-stripping boundary can be instantiated by a CF8-style domain wall with localized zero-modes and exponentially suppressed bulk leakage. The work is scoped as a **T1 proto-model**: it does not claim astrophysical black holes are already derived, and it does not import GR horizon axioms. Instead, it builds a reproducible instrumented runner that (i) constructs domain-wall backgrounds, (ii) injects controlled excitations, (iii) measures **bulk→wall capture** and **wall→bulk leakage** as separate, operationally defined maps, and (iv) reports an “emission proxy spectrum” of leaked exterior content. The primary deliverable is a runner + metrics + gates that can later be upgraded to T2 (instrument certification) and then to a T3/T4 phenomenon claim.

---

## 4. Background & Scientific Rationale

### 4.1 Canonical prerequisites (already in-repo)

This proposal is downstream of:

- **Metriplectic program axioms (A0–A7)** (closure, locality, symmetry, J/M split, entropy law, measurability).
- **CF8 (Spinor Emergence / Domain Wall Fermions)**: domain walls support localized modes and exponentially small overlap/leakage between separated walls.
- **Tachyonic condensation / tube interior results** (where applicable): provide a mechanism for stable condensed regions and boundary formation.

**Placement note (existing horizon work):** The repository already includes an **Analog Horizon** proposal in the VDM validation-phase cluster. This document is intended as a *microphysical variant* anchored to CF8 domain-wall leakage. If adopted, it should be cross-linked to the existing horizon branch (or nested under it) to avoid duplicative “horizon” meters.

### 4.2 The gap this proposal addresses

CF8 provides domain-wall mathematics and numerical behavior in the context of emergent spinors. What is not formalized (runner-backed, gate-tested) is the following package:

1. A boundary treated operationally as **bulk→wall stripping/capture** versus **wall→bulk emission/leakage**, with both maps measured under a declared numerical instrument.
2. A measurable **leakage spectrum** (residual overlap / tunneling) summarized as a **temperature-like emission proxy** (fit statistic; not an equilibrium claim).
3. A controlled mapping from wall parameters (thickness, separation, coupling) to capture/leakage rates, with reproducible uncertainty and ablations against numerical artifacts.

This proposal focuses on (1)–(3) as a proto-model, without assuming GR horizons.

### 4.3 Scientific motivation

If a CF8 domain wall can reliably (a) capture bulk excitations into a localized subspace and (b) exhibit exponentially small but measurable leakage back into the exterior, then a disciplined bridge from CF8 microstructure toward gravity/cosmology branches becomes possible. The correct first step is not “derive Hawking”; it is to build an instrument that cleanly separates capture from leakage and proves these quantities are not numerical artifacts.

---

## 5. Intellectual Merit and Procedure

### 5.1 Experimental Setup and Diagnostics

**System under study:** a lattice field configuration with a tunable domain-wall background and injected excitations.

**Geometric convention (local and operational):** The wall is embedded with a declared normal coordinate $z$ and center at $z=0$. Two bulk half-spaces are defined purely by sign:

- bulk side **L**: $z<0$  
- bulk side **R**: $z>0$

No global “in/out” orientation is assumed by canon, so both sides are treated symmetrically and tested explicitly.

**Independent variables (planned sweep axes):**

- Wall thickness parameter (e.g., $\xi$) and amplitude scale (background vacua values).
- Optional second wall / barrier width ($L$) for a two-wall overlap control.
- Injection parameters (center, width, carrier wavenumber $k_0$, amplitude; energy fixed by normalization).
- J/M composition choice (J-only, M-only, JMJ Strang) to separate reversible transport from dissipative stripping.
- Measurement noise / filter settings for spectral summaries (declared; no adaptive tuning).

**Dependent variables (primary observables):**

- **Bulk→wall capture fraction** $C_{\mathrm{L}}, C_{\mathrm{R}}$:
  fraction of injected bulk excitation energy (or probability mass) that is projected onto the localized wall subspace on a pre-registered window after interaction.
- **Wall→bulk escape fraction** $E$:
  fraction of energy (or probability mass) starting in a localized wall state that appears in the bulk region(s) on the same type of window.
- **Leakage rate** $\lambda$:
  exponential tail rate of localized-subspace content (or energy) decay into bulk, fit on a pre-registered window.
- **Emission proxy spectrum** $S(\omega)$:
  spectral density of leaked exterior content, plus a *fit parameter* $T_{\mathrm{proxy}}$ if a thermal-like parametric form is used. This is descriptive only.

**Diagnostics required (count + outputs):**

- 1× localized mode extractor (basis build / eigen-solve) → `modes.npz` + `modes.json`
- 1× capture meter (overlap time-series for L and R injections) → `capture.csv` + `capture.json`
- 1× escape meter (leakage time-series from localized IC) → `escape.csv` + `escape.json`
- 1× leakage fit (rate + CI) → `leakage_fit.json`
- 3× figures (minimum): space-time heatmap, capture/escape vs time, leakage-spectrum plot.

**New scripts required (paths to be created in the repository):**

- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/run_horizon_wall_leakage.py`
- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/metrics.py`
- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/schemas/horizon_wall_leakage.schema.json`
- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/specs/horizon_wall_leakage.v1.json`

*(If the existing Analog Horizon directory is preferred, place these under `Metriplectic/Analog_Horizon/...` instead; the key requirement is cross-linking and avoiding duplicate meters.)*

### 5.1.1 Pre-Run Config Requirements

To align with approval/authorization policy, the runner should be paired with:

- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/APPROVAL.json`
- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/schemas/horizon_wall_leakage.schema.json`
- `Derivation/code/physics/metriplectic/analog_horizon_domainwall/specs/horizon_wall_leakage.v1.json`

The schema must enumerate all parameters with units/normalization and disallow undeclared keys.

### 5.1.2 Reuse of CF8 infrastructure (efficiency + consistency)

The runner should reuse CF8 spinor/domain-wall infrastructure *wherever possible*:

- **Background construction:** reuse the canonical CF8 wall profile initializer (same discretization + BC conventions).
- **Localized mode extraction:** reuse CF8’s eigen-solve / Ginsparg–Wilson / localization checks (or wrap them) so the basis definition is consistent with the spinor sector.
- **Cross-check gate:** run at least one configuration that reproduces a CF8 localization/leakage sanity plot under the same code path before declaring horizon-runner outputs.

If reuse is impossible (due to BC, dimensionality, or operator differences), this proposal requires an explicit note in the prereg stating which CF8 components are reimplemented and which CF8 gates are reproduced as cross-validation.

### 5.2 Methods / Protocol

**Run families (minimum):**

- **(A) Bulk→wall capture (two-sided):** Inject a bulk wavepacket from L and independently from R (same energy normalization) and measure capture fraction $C_{\mathrm{L}}, C_{\mathrm{R}}$.
- **(B) Wall→bulk escape:** Initialize a localized wall mode (same normalized energy budget) and measure escape fraction $E$ and leakage rate $\lambda$ into bulk.
- **(C) Controls/ablations:** no-wall, wall-removed, integrator swap, and (optional) two-wall overlap control.

**High-level procedure (per run):**

1. **Construct background:** initialize field with a single wall (optionally a paired wall) using the CF8 background profile.
2. **Extract localized basis:** numerically identify localized modes on the wall neighborhood and record localization diagnostics.
3. **Inject excitation:** run family (A) and (B) ICs with declared stepper (J-only, M-only, or JMJ Strang).
4. **Measure capture + escape:** compute overlaps onto localized basis each step; compute exterior-region flux and spectrum.
5. **Fit leakage rate:** fit exponential tail(s) on pre-registered windows; report CI via bootstrap or multi-seed replicate.
6. **Gate checks:** verify global gates (degeneracies, H-theorem where relevant, locality where relevant) and run-specific gates below.

**Controls / ablations (required):**

- **No-wall control:** same injections with homogeneous background; capture fraction must be consistent with zero within tolerance.
- **Wall-removed control:** continuously dial wall amplitude → 0; verify capture collapses smoothly.
- **Integrator swap:** at least two steppers (e.g., symplectic-ish vs non-symplectic) to ensure leakage is not a numerical artifact.
- **Injection side flip:** capture runs must be performed from both L and R; results are reported separately, not averaged by default.

### 5.3 Acceptance gates and thresholds (T1)

Because this is T1, gates focus on *instrument sanity* rather than astrophysical matching.

**G0 (Artifacts):** every run emits `metrics.json`, `trace.csv`, `gates.json`, and ≥3 figures with matching CSV/JSON sidecars.

**G1 (Localization):** extracted localized modes satisfy a declared localization metric (e.g., ≥90% of norm inside a fixed wall neighborhood).

**G2 (One-way stripping defined operationally):** Under an M-dominated configuration,
- capture runs produce measured $C_{\mathrm{L}}, C_{\mathrm{R}}$ (both reported), and
- escape runs produce measured $E$,
and the **capture/escape asymmetry ratio**
  $$R \equiv \frac{\max(C_{\mathrm{L}}, C_{\mathrm{R}})}{\max(E,\,\epsilon)}$$
exceeds a declared factor (default prereg threshold: $R \ge 2$) while holding injection energy fixed.
If $C_{\mathrm{L}}$ and $C_{\mathrm{R}}$ differ by >20%, that asymmetry is reported as a finding; it does not invalidate the run, but it blocks any narrative that assumes side-independence.

**G3 (Leakage exponential tail):** leakage fit achieves $R^2\ge 0.98$ on the pre-registered window and is stable (≤10% shift) under a ±20% window perturbation.

**G4 (Resolution robustness):** leakage rate changes by ≤15% under a two-grid refinement test (e.g., $\Delta x \to \Delta x/2$ with consistent CFL policy). *(Note: this is a generous T1 threshold; T2 requires tighter convergence characterization and order reporting.)*

**G5 (Global gates):**

- J/M degeneracy residuals remain below the global tolerance throughout.
- H-theorem holds for M-only steps (where evaluated).
- Locality audit passes for J-only (hyperbolic) runs.

### 5.4 What counts as “success” at T1

PASS is defined strictly by G0–G5. Any discussion of Hawking-like scaling is recorded as exploratory diagnostics, not as a PASS condition. “Temperature-like” quantities are allowed only as explicitly labeled fit statistics on emitted spectra.

---

## 6. Broader impacts / ethics / safety

- No human-subject data.
- Compute budget controlled by declared grid/time limits.
- Explicitly avoids anthropomorphic framing; “information stripping” is defined only via measurable capture/leakage observables.

---

## 7. Risks, criticisms, and kill plans

**Risk 1: Numerical leakage mistaken for physical leakage.**

- Mitigation: integrator swap + two-grid test + no-wall/wall-removed controls.
- Kill: if G4 fails or leakage rate varies wildly with stepper choice.

**Risk 2: “One-way” behavior is an artifact of initial/boundary conditions or side labeling.**

- Mitigation: enforce symmetric BCs; perform both L and R capture injections; record $C_{\mathrm{L}}, C_{\mathrm{R}}$ separately; repeat with flipped wall profile if applicable.
- Kill: if $R$ collapses under side-flip or depends on arbitrary implementation choices.

**Risk 3: Localized basis is ill-defined / non-robust.**

- Mitigation: specify basis extraction method and stability checks; cross-validate with at least one CF8 reproduction configuration.
- Kill: if G1 fails consistently or basis changes discontinuously with small perturbations.

---

## 8. Expected artifacts (paths)

- `Derivation/code/outputs/logs/metriplectic/analog_horizon_domainwall/<tag>/`  
  - `runs.csv`, `metrics.json`, `gates.json`, `fit/leakage_fit.json`
- `Derivation/code/outputs/figures/metriplectic/analog_horizon_domainwall/<tag>/`  
  - `spacetime_field.png`, `capture_escape_timeseries.png`, `leakage_spectrum.png`
- `Derivation/code/outputs/reports/metriplectic/analog_horizon_domainwall/<tag>/`  
  - `CONTRADICTION_REPORT.json` on any gate fail

---

## 9. References (repository-internal)

- `Derivation/Complete-Formalisms/CF8_Spinor_Emergence_Domain_Wall_Fermions.md`
- `Derivation/Metriplectic/Analog_Horizon/T5_PROPOSAL_Analog_Horizon_v1.md` (existing horizon meter cluster; cross-link)
- `Derivation/Complete-Formalisms/CF4_Telegraph_Fisher_Causality.md` (locality/relaxation context)
- `Derivation/AXIOMS.md` (A0–A7)
- `Derivation/VALIDATION_METRICS.md` (global gate definitions)
- `Derivation/TIER_STANDARDS.md` (T0–T9 maturity ladder)

---

## 10. Version history

- v0.1 2026-02-15 — v1 created (proto-model runner + gates)
- v0.2 2026-02-15 — v2 tightened G2 operational definition (capture vs escape; two-sided injection) and added CF8 reuse expectations
