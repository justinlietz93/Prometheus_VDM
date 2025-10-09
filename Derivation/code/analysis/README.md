# analysis/ - exploratory math and prototypes

Purpose

- A sandbox for derivations and exploratory scripts (symbolic CAS, algebraic checks, tiny numeric experiments).
- Example: `flux_symbolic_full.py` uses SymPy to solve for discrete flux coefficients in a small-N setting.

What it is not

- Not part of the production runtime, approval gate, or standardized outputs.
- Not a global utility library. When a script becomes generally useful, promote it into `common/` or a domain runner under `physics/` with proper approval and IO helpers.

When to promote or retire

- Promote when: the idea stabilizes and is reused by experiments.
- Retire/archive when: the exploration is concluded and superseded by formal code.

Usage tips

- Keep one-off `__main__` smoke checks here; avoid adding external dependencies.
- If you need figures/logs for comparison, consider porting the logic into a proper runner that uses `common/plotting` and `common/io_paths` so artifacts are tracked and quarantined per policy.

Ownership

- Maintainers: core devs only. Keep it lean to avoid confusion with production code.
