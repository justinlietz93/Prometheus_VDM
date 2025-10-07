# Progress (Updated: 2025-10-07)

## Done

- Created `vdm_equations.py` with potential/reaction/dispersion/front-speed/mappings/KG speed and vacuum evaluators.
- Added gated unit test `test_vdm_equations.py` and package initializers for Derivation packages.
- Smoke-checked module with internal self-check (OK).

## Doing

- Offer to wire new module into existing physics runners to de-duplicate formulas.

## Next

- Auto-compile constants/equations into the module (codegen) to prevent drift.
- Enable Codacy CLI MCP and run analysis on new files once available.
