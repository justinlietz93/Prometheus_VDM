# CEG Metriplectic Instrument — Release Package

**Counterfactual Echo Gain (CEG): Future-Aware Metriplectic Assistance Yields Gate-Certified Echo Improvement**

Author: Justin K. Lietz · Neuroca, Inc. · ORCID: [0009-0008-9028-1366](https://orcid.org/0009-0008-9028-1366)

---

## Section A: What This Is

### The Observable

**CEG (Counterfactual Echo Gain)** is a gate-certified instrument that measures whether a model-aware time-reversal (*assisted echo*) recovers a forward state more accurately than a model-blind baseline echo, under strict physics certification gates.

```
CEG = (E_baseline − E_assisted) / E_baseline  ∈  [0, 1]
```

A positive CEG means the model-aware reverse trajectory is closer to the true forward state than the model-blind one. CEG = 0 means no benefit; CEG = 1 means perfect recovery by the assisted echo.

**Published result**: 12 seeds, 5 λ values, all gates 100% pass, **median CEG = 0.0546 at λ = 0.5**.

---

### The Metriplectic Split

The forward dynamics are composed of two limbs via **Strang splitting** (J→M→J, step sizes dt/2, dt, dt/2):

| Limb | Symbol | Role |
|------|--------|------|
| **J-limb** | Conservative | Hamiltonian/symplectic dynamics. Exact spectral advection. Reversible, energy-preserving. |
| **M-limb** | Dissipative | Entropy-producing. Reaction-diffusion with discrete gradient (DG) integrator. Irreversible. |

The Strang composition gives second-order accuracy and satisfies both conservation laws (J) and the H-theorem (M) simultaneously.

---

### The Gate System

Before any CEG result is reported, five physics gates must all pass:

| Gate | Name | What it checks |
|------|------|----------------|
| **G1** | Noether / J-drift | J-only forward trajectory conserves discrete energy to within tolerance (max drift ≤ tol). Certifies the conservative limb is unitary. |
| **G2** | H-theorem / M-monotonicity | M-only trajectory monotonically increases entropy (`Δσ_min > 0`). Certifies the dissipative limb is physically correct. |
| **G3** | Energy-match | Work done by baseline and assisted reversal on the forward state differ by < 1e-4 (relative). Ensures the comparison is fair. |
| **G4** | Strang defect scaling | Global error scales as dt² (R² ≥ 0.9999, slope ≈ 2). Certifies second-order composition. |
| **G5** | CEG positive | Median CEG at the largest λ ≥ 0.05. The instrument reports a result only if there is a detectable gain. |

**All five gates passed 100% across all 12 seeds in the published run.**

---

## Section B: Recreating the Published Results

### Prerequisites

```bash
pip install numpy scipy
```

### Entry Point

The instrument lives at `Derivation/code/` in the repository. The entry point is `assisted_echo.py`, invoked as a module:

```bash
# From repository root
cd Derivation/code

# Run the exact preregistered experiment (v1c spec, N=256, dt=0.02, 12 seeds)
python -m physics.metriplectic.assisted_echo \
  --spec physics/metriplectic/specs/assisted_echo.v1c.json \
  --allow-unapproved

# Outputs land in:
#   Derivation/code/outputs/logs/metriplectic/    (JSON gate ledger + CSV summary)
#   Derivation/code/outputs/figures/metriplectic/ (PNG figures)
```

The `--allow-unapproved` flag bypasses the internal preregistration approval check so external collaborators can run without needing an approval token.

### Available Spec Variants

| Spec file | Configuration |
|-----------|---------------|
| `specs/assisted_echo.v1c.json` | **Canonical** — N=256, dx=1.0, dt=0.02, budget=1e-2 |
| `specs/assisted_echo.v1c_N512_dt0p04.json` | N=512, dt=0.04 |
| `specs/assisted_echo.v1c_N1024_dt0p04.json` | N=1024, dt=0.04 |
| `specs/assisted_echo.v1c_walker.json` | With walker perturbation (amp=0.2, width=8) |
| `specs/assisted_echo.v1c_budget0p03_*.json` | Higher budget variants |

### Published Logs (Bundled in This Package)

- `logs/assisted_echo_run.json` — Full gate ledger, per-seed CEG values, all diagnostics
- `logs/ceg_summary.csv` — λ vs median/mean CEG table

See `logs/README.md` for data dictionary and gate result summary.

---

## Section C: Using the Instrument on Your Own Model

### Programmatic API

```python
from physics.metriplectic.assisted_echo import EchoSpec, run_assisted_echo

spec = EchoSpec(
    grid={"N": 256, "dx": 1.0},
    params={
        "c": 1.0,                      # wave speed (J-limb)
        "m": 0.5,                      # mass parameter (J-limb)
        "D": 1.0,                      # diffusion coefficient (M-limb)
        "r": 0.1,                      # reaction rate (M-limb)
        "u": 0.0,                      # reaction saturation (M-limb)
        "m_lap_operator": "spectral",  # or "stencil"
    },
    dt=0.02,
    steps=200,
    seeds=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    lambdas=[0.0, 0.1, 0.2, 0.3, 0.5],
    budget=1e-2,
    tag="my-experiment"
)

results = run_assisted_echo(spec)

# Results contain:
# results["ceg_summary"]          — {λ: {median, mean, n}}
# results["gate_ledger_per_seed"] — per-seed gate pass/fail
# results["gate_ledger_summary"]  — aggregate pass rates
# results["per_seed"]             — full per-seed data
# results["telemetry_rows"]       — per-step traces
```

### Module Architecture

| Module | Role |
|--------|------|
| `assisted_echo.py` | Main runner. `run_assisted_echo(spec) -> dict`. Forward JMJ integration, RP-1 gate calibration, baseline vs assisted reverse, CEG computation, gate aggregation. |
| `kg_ops.py` | Spectral operators: Laplacian, gradient, KG energy, Störmer-Verlet stepper. The physics primitives. |
| `compose.py` | Strang composition: `jmj_strang_step` = J(dt/2) → M(dt) → J(dt/2). M-step wraps a DG (discrete gradient) Newton solver for the reaction-diffusion dissipator. |
| `j_step.py` | Pure J-limb: exact spectral advection (unitary, L2-preserving, reversible). |
| `kg_noether.py` | Noether invariant verification (discrete energy conservation under Verlet). |
| `echo_metrics.py` | H-norm error computation and CEG formula. |
| `echo_gates.py` | Gate functions: `gate_noether()`, `gate_h_theorem()`, `gate_energy_match()`, `gate_strang_defect()`. Each returns `{"gate": name, "passed": bool, ...diagnostics}`. |
| `metriplectic_structure_checks.py` | Algebraic verification: J skew-symmetry, M positive semi-definiteness. |
| `common/io_paths.py` | Artifact routing (timestamps, quarantine on failure). |
| `common/plotting/assisted_echo_plots.py` | Publication figure generation from JSON/CSV artifacts. |

### Adapting for a Different Model

The J-limb and M-limb are composable. To instrument a different dynamical system:

1. **Provide your own J-step function** — takes `(state, dt, dx, params)`, returns updated state. Must be reversible and energy-preserving.
2. **Provide your own M-step function** — takes `(state, dt, dx, params)`, returns updated state. Must produce non-negative entropy change (`Δσ ≥ 0`).
3. **Pass them to `jmj_strang_step`** in `compose.py` — the Strang splitting wrapper accepts any J/M pair.

The gate system is **model-agnostic**:
- G1 checks J-only reversibility (your J-step, not the default KG one)
- G2 checks M-only entropy production (your M-step)
- G3 checks work-matching between baseline and assisted reversal
- G4 checks Strang splitting second-order convergence

The CEG observable only needs:
- A **norm function** `E(state)` to measure recovery error
- A way to run **baseline** (model-blind) and **assisted** (model-aware) reverse trajectories

---

## Section D: File Manifest

```
release_pack/
├── README.md              — This file
├── CITATION.cff           — Machine-readable citation (CFF 1.2.0)
├── quickstart.sh          — One-shot: preflight test → run → check outputs
├── paper/
│   └── README.md          — Points to TeX/MD/bib source + compile instructions
├── logs/
│   ├── README.md          — Data dictionary + gate results + provenance
│   ├── assisted_echo_run.json  — Full gate ledger from published run
│   └── ceg_summary.csv         — λ vs median/mean CEG table
└── instrument/
    └── README.md          — Full source tree map with module roles
```

**Instrument source** (lives in main repo under `Derivation/code/`):

```
physics/metriplectic/
├── assisted_echo.py              — Main runner + EchoSpec
├── kg_ops.py                     — Spectral physics primitives
├── j_step.py                     — Pure J-limb (FFT advection)
├── compose.py                    — Strang composition (JMJ)
├── kg_noether.py                 — Noether invariant checks
├── echo_metrics.py               — H-norm, CEG formula
├── echo_gates.py                 — G1–G4 gate functions
├── metriplectic_structure_checks.py  — J/M algebraic checks
├── specs/                        — Experiment spec JSON files
└── schemas/                      — JSON Schema validators
common/
├── io_paths.py                   — Artifact routing
├── authorization/approval.py     — Run approval system
└── plotting/assisted_echo_plots.py  — Figure generator
tests/metriplectic/
├── test_assisted_echo_preflight.py
└── test_instrumented_ceg.py
```

---

## Section E: Citation

```
Justin K. Lietz (2025). "Counterfactual Echo Gain (CEG): Future-Aware Metriplectic
Assistance Yields Gate-Certified Echo Improvement." Neuroca, Inc.
ORCID: 0009-0008-9028-1366
Repository: https://github.com/justinlietz93/Prometheus_VDM
Commit: 10eb904d385927cc8132919288fbeb52b401ae04
```

See `CITATION.cff` for the machine-readable version (compatible with Zenodo, GitHub, etc.).
