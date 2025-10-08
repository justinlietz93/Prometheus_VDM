# obs/ — observability helpers (read-only diagnostics)

Purpose

- Small utilities that compute derived signals/fields from simulation state without feeding back into dynamics.
- Example: `walker_glow.py` accumulates local fire events and incoming flux magnitudes to produce a glow field M.

What it is not

- Not part of the core model update; observables are read-only.
- Not automatically used by runners unless explicitly imported.

Usage

- Import and call from an experiment to compute diagnostics, then plot via `common/plotting`.
- Keep parameters (e.g., alpha, beta, BCs) explicit for clarity and reproducibility.

Promotion policy

- If an observable becomes standard for a domain, consider promoting it into a domain-specific module or `common/observability/`.

Ownership

- Maintainers: core devs. Keep APIs narrow and pure (no side effects).
