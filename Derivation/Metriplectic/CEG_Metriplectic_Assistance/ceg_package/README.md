# CEG Metriplectic Instrument Package

**Author:** Justin K. Lietz — Neuroca, Inc.  
**ORCID:** [0009-0008-9028-1366](https://orcid.org/0009-0008-9028-1366)  
**Repo:** [github.com/justinlietz93/Prometheus_VDM](https://github.com/justinlietz93/Prometheus_VDM)  
**License:** See LICENSE at repository root

---

## What This Is

A self-contained instrument for measuring **Counterfactual Echo Gain (CEG)** — a
gate-certified observable that quantifies whether a model-aware time-reversal improves
state recovery vs a model-blind baseline.

The physics: a **metriplectic split** — conservative J-limb (Hamiltonian, symplectic,
energy-preserving) composed with dissipative M-limb (entropy-producing, gradient flow)
via **Strang splitting**: J(dt/2) → M(dt) → J(dt/2).

The observable:

```
CEG = (E_baseline - E_assisted) / E_baseline ∈ [0, 1]
```

Five instrument gates certify each run:
- **G1** (Noether): J-only energy drift ≤ tolerance
- **G2** (H-theorem): M-only entropy production ≥ 0
- **G3** (Energy match): baseline and assisted use identical work budgets
- **G4** (Strang defect): splitting error scales as O(dt³) with R² ≥ 0.999
- **G5** (CEG threshold): median CEG across seeds ≥ 0.05

**Published result** (2025-11-04): 12 seeds × 5 λ values, all gates pass, median
CEG > 0 at λ > 0. See `published_results/ceg_summary.csv` for full data.

---

## Quick Start

```bash
# Requirements: Python 3.10+, numpy, scipy (matplotlib optional for plots)
pip install numpy scipy matplotlib

# Run with default spec (N=256, dt=0.02, 12 seeds, 5 lambda values)
python run_ceg.py

# Run with custom spec
python run_ceg.py --spec specs/default_v1c.json

# Run with inline overrides
python run_ceg.py --N 128 --dt 0.05 --seeds 1,2,3
```

---

## Using the Instrument Programmatically

```python
from ceg_instrument import run_ceg, CegSpec

spec = CegSpec(
    grid={"N": 256, "dx": 1.0},
    params={
        "c": 1.0,           # wave speed (J-limb KG)
        "m": 0.5,           # mass (J-limb KG)
        "D": 1.0,           # diffusion coeff (M-limb RD)
        "r": 0.1,           # reaction rate (M-limb RD)
        "u": 0.0,           # saturation (M-limb RD)
        "m_lap_operator": "spectral",
    },
    dt=0.02,
    steps=200,
    seeds=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    lambdas=[0.0, 0.1, 0.2, 0.3, 0.5],
    budget=1e-2,
)

results = run_ceg(spec)

# What you get back:
print(results["ceg_summary"])           # {λ: {median, mean, n}}
print(results["gate_ledger_summary"])   # {gate: {passed, failed, pass_rate}}

# Per-seed detail:
for s in results["gate_ledger_per_seed"]:
    print(f"Seed {s['seed']}: {[g['gate'] + ':' + str(g['passed']) for g in s['gates']]}")
```

---

## Directory Structure

```
ceg_package/
├── README.md                    # This file
├── CITATION.cff                 # Citation metadata
├── run_ceg.py                   # One-file entry point
├── ceg_instrument/
│   ├── __init__.py              # Public API: run_ceg, CegSpec
│   ├── assisted_echo.py         # Core experiment logic (self-contained)
│   ├── kg_ops.py                # Klein-Gordon operators (Verlet, spectral)
│   ├── j_step.py                # Conservative J-step (spectral advection)
│   ├── compose.py               # Metriplectic composition (Strang splitting)
│   ├── echo_metrics.py          # CEG metric and H-energy norm
│   ├── echo_gates.py            # Gate checks G1–G4
│   ├── kg_noether.py            # Noether invariant utilities
│   └── rd_solver.py             # DG Newton RD solver (M-step)
├── specs/
│   └── default_v1c.json         # Canonical pre-registration spec
├── published_results/
│   ├── gate_ledger.json         # Full run log (2025-11-04)
│   └── ceg_summary.csv          # CEG summary CSV
└── paper/
    └── README.md                # How to find/compile the TeX paper
```

---

## Adapting for Your Own Model

The instrument is modular. To test a different dynamical system:

1. **Replace the J-step** (conservative limb): provide any function
   `(phi, pi, dt, dx, c, m) -> (phi_new, pi_new)` that is reversible and
   energy-preserving. Currently this is Störmer-Verlet for Klein-Gordon.

2. **Replace the M-step** (dissipative limb): provide any function
   `(W, dt, dx, params) -> (W_new, stats)` that is entropy-producing. Currently
   this is the discrete-gradient reaction-diffusion step with Newton solver.

3. **Change the correction oracle**: the `assist_mode` parameter controls whether
   the assisted arm uses `"model_aware"` (steepest descent on H-energy distance)
   or `"model_blind"` (random correction with same work budget).

---

## Physical Interpretation

The CEG observable measures the informational advantage of a model-aware agent
in reversing dissipative dynamics. When λ > 0, the assisted arm applies corrections
proportional to the error direction (∇_H of the H-energy distance to the reference
state). A positive CEG means the model-aware corrections outperform random ones at
the same energy cost — evidence that the model captures genuine causal structure of
the dissipation.
