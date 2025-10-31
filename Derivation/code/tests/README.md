# Tests (Derivation/code/tests/{domain}/)

Purpose

- Unit and regression tests for physics domains. Tests are fast, headless (no figures/logs), and assert numeric tolerances.

Directory layout

- Each domain has its own subfolder:
  - reaction_diffusion/
  - fluid_dynamics/
  - tachyonic_condensation/
- Example
  - [test_taylor_green_decay.py](Prometheus_VDM/Derivation/code/tests/fluid_dynamics/test_taylor_green_decay.py:1) - verifies ν recovery from Taylor-Green energy decay with |ν_fit-ν_th|/ν_th ≤ 5%.

Conventions

- Location: Derivation/code/tests/{domain}/test_*.py
- Tests must not write figures/logs; benchmarks do that (see physics/README).
- Keep runtimes short (< 10 s typical).
- Use explicit numeric tolerances with clear failure messages.

Running tests (PowerShell)

- Always activate venv first:
  - & .\venv\Scripts\Activate.ps1
- Run a single test file:
  - python -m pytest Prometheus_VDM/Derivation/code/tests/fluid_dynamics/test_taylor_green_decay.py -q
- Run an entire domain:
  - python -m pytest Prometheus_VDM/Derivation/code/tests/fluid_dynamics -q
- Run all tests:
  - python -m pytest Prometheus_VDM/Derivation/code/tests -q

Pathing rules (applies repo‑wide)

- Simulations/benchmarks: Derivation/code/physics/{domain}/*.py
- Tests: Derivation/code/tests/{domain}/test_*.py
- Figures: Derivation/code/outputs/figures/{domain}/
- Logs: Derivation/code/outputs/logs/{domain}/
- This naming ensures domain‑scoped artifacts and simple globbing.

Example: Taylor-Green (fluid_dynamics)

- Unit test: [test_taylor_green_decay.py](Prometheus_VDM/Derivation/code/tests/fluid_dynamics/test_taylor_green_decay.py:1)
  - Builds a small D2Q9 LBM system (τ=0.8 ⇒ ν_th=(τ-0.5)/3).
  - Samples energy E(t) and fits log E.
  - Uses correct lattice scaling K² = k²(1/nx² + 1/ny²).
  - Asserts |ν_fit-ν_th|/ν_th ≤ 0.05.
- Benchmark (separate, writes artifacts): see physics/README
  - [taylor_green_benchmark.py](Prometheus_VDM/Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1)

Adding a new test

1) Create file under the correct domain, e.g. Derivation/code/tests/reaction_diffusion/test_new_check.py
2) Import the simulation helper(s) from physics when needed.
3) Keep it headless; assert numeric tolerances.
4) Ensure deterministic seeds when randomness is involved.

CI notes

- Recommended command in CI:
  - python -m pytest Prometheus_VDM/Derivation/code/tests -q
- Keep per‑test runtime bounded to prevent CI timeouts.

Contact/ownership

- Physics validation is owned by Physicist Mode. If a test needs heavier data generation, move that to a benchmark script and leave the test as a quick numeric check.
