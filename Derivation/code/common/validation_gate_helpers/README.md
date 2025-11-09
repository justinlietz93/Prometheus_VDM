# Validation Gate Helpers — Domain-organized

This package contains reusable, domain-scoped helpers that evaluate VDM validation KPIs/gates. It is distinct from instrument helpers (which compute observables and meters). Gate helpers only decide pass/fail and compute the accompanying KPI metrics according to canon, with no plotting and no I/O side effects.

Related:

- Instrument helpers (meters): [prigogine_gates.py](../instrument_helpers/prigogine_gates.py)
- Canon KPIs/gates registry: [VALIDATION_METRICS.md](../../../VALIDATION_METRICS.md)
- Equations registry: [EQUATIONS.md](../../../EQUATIONS.md)
- Architecture and approvals policy: [ARCHITECTURE.md](../../ARCHITECTURE.md)

## Why a separate package?

- Separation of concerns:
  - instrument_helpers = compute observables/meter outputs
  - validation_gate_helpers = evaluate pass/fail against canonical KPIs and thresholds
- Traceability: each gate helper must point to a canonical anchor in VALIDATION_METRICS.md and (when applicable) EQUATIONS.md.
- Determinism and testability: pure functions, no I/O, unit-test friendly.

## Directory layout (by domain)

Create a subfolder per physics domain and place gate helper modules inside it. Suggested starting structure:

- boundaries/
  - gb_relaxation.py (gates: gamma2-law, asymmetric emission threshold, cycle Lyapunov monotonicity, protocol-insensitivity, dimensionless-collapse)
- nonequilibrium/
  - prigogine.py (gates: entropy production trend, bifurcation card, localized structure detection, branch classifier, branch stability plot)
- metriplectic/
  - metriplectic_core.py (gates: ΔL_h ≤ 0, identity residuals, two-grid slope, R²)
- cosmology/
  - frw_continuity.py (gate: RMS residual ≤ 1e-6 for dust, central differences)
- fluids/
  - lbm_ns.py (gates: viscosity and divergence tolerances, grayscale-readability probe)

You may add additional domain folders as needed, keeping names aligned with Derivation domain names.

## API contract

Gate helper functions must be pure and deterministic:

- Inputs: numerical arrays/structures for observables or statistics already computed by instrument helpers, plus any thresholds (if not fixed by canon).
- Outputs: a tuple (passed: bool, metrics: dict)
  - passed: bool — final gate decision per canon
  - metrics: dict — include all scalar KPI values, R², slopes, residuals, and any auxiliary statistics necessary for reporting

Implementation rules:

- Do not perform file I/O. Call sites are responsible for writing JSON/CSV/PNG artifacts via the repository I/O helpers.
- Do not plot. Return numbers only; figure generation belongs in analysis or runners.
- Double precision only (IEEE-754). Seed handling, when applicable, is performed by callers.
- Unit consistency: document expected units in the function docstring; validate/scale by dimensionless groups per canon when required.

## Canon alignment

For each gate helper:

- Link to its KPI anchor in [VALIDATION_METRICS.md](../../../VALIDATION_METRICS.md) using the section anchor (e.g., #kpi-gamma2-law).
- If an equation is referenced, link by anchor to [EQUATIONS.md](../../../EQUATIONS.md) (e.g., #vdm-e-160).
- Do not duplicate canonical numbers or equations here. This package implements the pass/fail calculation only.

Example docstring checklist:

- Canon anchors: VALIDATION_METRICS.md#kpi-..., EQUATIONS.md#vdm-e-...
- Assumptions and limitations
- Expected input shapes and units
- Returned metrics with names matching the KPI schema

## Naming conventions

- Module names: lowercase with underscores (e.g., gb_relaxation.py)
- Function names: gate_<short-kpi-id> (e.g., gate_gamma2_law, gate_asymmetric_emission_threshold)
- Metrics keys: match the canonical KPI field names where possible (e.g., "r2", "slope", "residual_rms", "acceptance", "tau_int")

## Relationship to instrument helpers

Instrument helpers often live in:

- [prigogine_gates.py](../instrument_helpers/prigogine_gates.py)
- Other domain-specific instruments under Derivation/code/common/instrument_helpers/

Callers should:

1) Compute observables with instrument helpers
2) Evaluate gates with validation_gate_helpers
3) Route artifacts via code/common/io_paths.py at the orchestration layer

## Roadmap

Short-term additions:

- boundaries/gb_relaxation.py: gates for VDM-E-160..164 (γ²-law, asymmetric emission threshold, cycle Lyapunov monotonicity, protocol-insensitivity, dimensionless collapse)
- nonequilibrium/prigogine.py: gates for self-organization KPIs (entropy production trend, bifurcation card, localized structures, branch classifier, branch stability)

Medium-term:

- metriplectic core gates (ΔL_h ≤ 0, identity residuals, two-grid slope ≥ 2.90, R² ≥ 0.999)
- acceptance-vs-stepsize diagnostics (HMC/RHMC) tied to ΔH scaling predictions

All additions must include unit tests and docstrings with canon anchors.
