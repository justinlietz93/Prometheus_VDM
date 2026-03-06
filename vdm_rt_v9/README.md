# VDM Runtime v9 - CF-Aligned Implementation

## Overview

This is a complete reimplementation of the VDM (Void Dynamics Model) runtime with **full alignment** to the CF (Complete Formalism) documents. All parameters are now derived from quantum geometric structure rather than engineering proxies.

## Key Changes from v8

### 1. QGT-Derived Parameters (CF01)

**Before (v8 - Engineering Proxies):**
```python
D_DIFF = C_SQ / GAMMA_DAMP  # VDM-E-050 - engineering parameter
TAU = 1.0 / GAMMA_DAMP      # CF04 Section 2.1 - cited but not derived
```

**After (v9 - CF-Derived):**
```python
# Parameters derived from QGT computation
qgt_result = compute_qgt(hamiltonian, parameters)
gamma, D, tau = derive_telegraph_parameters_from_qgt(qgt_result)
```

### 2. Contact Geometry (CF02)

**New Module: `contact_geometry.py`**
- Contact 1-form: `α = ds - p_i dq^i`
- Reeb vector field: `ι_R α = 1, ι_R dα = 0`
- GENERIC evolution: `ẋ = L∇E + M∇S`

### 3. A8 Hierarchy Verification (CF03)

**New Module: `a8_hierarchy.py`**
- Interface counting: `N(L) = Θ(log(L/ℓ₀))`
- Perimeter reduction principle
- Gamma-convergence: `E_ε → c₀ Per as ε → 0`

### 4. Measurement Theory (CF07)

**New Module: `measurement_theory.py`**
- Decoherence time: `τ_D = ℏ/(k_B T λ²)`
- Pointer basis einselection: `||[H_SE, Π_i]|| ≤ ε`
- Born rule derivation from symmetry
- Causal horizon: `h_causal = c_signal / v_th`

### 5. Spinor Emergence (CF08)

**New Module: `spinor_emergence.py`**
- Domain-wall profile: `φ_bg(z) = φ_+ tanh(z/ξ)`
- Chiral zero modes: `χ_0(z) ∝ dφ_bg/dz`
- Ginsparg-Wilson operator: `{D, γ⁵} = a D γ⁵ D`
- Nielsen-Ninomiya defenses P1-P5

### 6. Gauge Emergence (CF09)

**New Module: `gauge_emergence.py`**
- Berry connection: `A_μ(x) = i⟨ψ(x)|∂_μ ψ(x)⟩`
- Field strength: `F_μν = ∂_μ A_ν - ∂_ν A_μ`
- Maxwell action: `S = -1/(4g²) ∫ F_μν F^μν`
- Weinberg-Witten compatibility

### 7. Gauge Bosons Replace Walkers

**Before (v8 - Heuristic Walkers):**
```python
class WalkerEvent:
    source: int
    target: int
    # Walkers were engineering proxies
```

**After (v9 - Gauge Bosons from Berry Connection):**
```python
@dataclass
class GaugeBosonEvent:
    source: int
    target: int
    boson: GaugeBoson  # Emerges from Berry connection
    emission_time: int
    arrival_time: int
```

### 8. Debt from Fisher Information (CF06)

**Before (v8 - Engineering Parameter):**
```python
BETA_DEBT = 0.1  # Engineering parameter
```

**After (v9 - Derived from Information Geometry):**
```python
def derive_beta_debt_from_fisher_info(fisher_metric, temperature):
    # β_debt ~ 1 / (kT · Tr(g_F))
    return 1.0 / (temperature * np.trace(fisher_metric))
```

## Module Structure

```
vdm_runtime/
├── __init__.py              # Package exports and integration
├── qgt.py                   # CF01: QGT → Metriplectic
├── contact_geometry.py      # CF02: Contact → GENERIC
├── a8_hierarchy.py          # CF03: A8 Scaling
├── void_equations.py        # CF04/CF11: Telegraph/Void
├── integrability_closure.py # CF05: Integrability
├── measurement_theory.py    # CF07: Measurement/Decoherence
├── spinor_emergence.py      # CF08: Domain-Wall Fermions
├── gauge_emergence.py       # CF09: Berry Connection → Gauge
├── gauge.py                 # CF09: Gauge Boson Dynamics
└── connectome.py            # CF03/CF07/CF11: Connectome
```

## Usage

### Basic Usage

```python
from vdm_runtime import (
    create_connectome_cf,
    run_simulation_cf,
    compute_qgt,
    CFDerivedParameters
)

# Create connectome with CF-derived parameters
connectome = create_connectome_cf(
    adj=adjacency_array,
    n_nodes=1000,
    max_degree=6,
    hamiltonian=my_hamiltonian,
    parameter_range=parameter_array
)

# Run simulation
history = run_simulation_cf(connectome, n_steps=1000, dt=0.1)
```

### Advanced: QGT Computation

```python
from vdm_runtime import compute_qgt, construct_metriplectic_operators

# Compute QGT from Hamiltonian
qgt_result = compute_qgt(hamiltonian, parameters)

# Verify properties
assert qgt_result.verify_hermiticity()
assert qgt_result.verify_positive_semidefinite()

# Construct metriplectic operators
operators = construct_metriplectic_operators(qgt_result)
```

### Advanced: Gauge Emergence

```python
from vdm_runtime import (
    compute_berry_connection,
    compute_field_strength,
    compute_maxwell_action
)

# Compute Berry connection from eigenstates
berry = compute_berry_connection(eigenstate_func, coordinates)

# Compute field strength
F = compute_field_strength(berry, x)

# Compute Maxwell action
action = compute_maxwell_action(F, volume_element=1.0)
```

## CF Alignment Verification

```python
from vdm_runtime import print_cf_alignment_report

print_cf_alignment_report()
```

Output:
```
============================================================
VDM Runtime v9 - CF Alignment Report
============================================================

CF01_QGT_Metriplectic:
  Implemented: True
  Key Features:
    - QGT computation from eigenstates
    - Berry curvature extraction
    - Metriplectic operator construction
    - Degeneracy verification

CF02_Contact_GENERIC:
  Implemented: True
  Key Features:
    - Contact 1-form construction
    - Reeb vector field computation
    - GENERIC evolution equation
    - Contact-to-GENERIC mapping

... (all CF documents)

============================================================
All parameters derived from QGT/Contact geometry
NO engineering proxies used
============================================================
```

## CFN Gates Implemented

Each module includes validation functions for CFN (CF Notebook) gates:

| Gate | CF Document | Description |
|------|-------------|-------------|
| G1 | CF01 | Q† = Q (Hermiticity) |
| G2 | CF01 | g ≥ 0 (Positive semidefinite) |
| G3 | CF01 | J·∇Σ = 0 (Degeneracy) |
| G4 | CF01 | M·∇I = 0 (Degeneracy) |
| G5 | CF02 | α ∧ (dα)^n ≠ 0 (Contact) |
| G6 | CF02 | ι_R α = 1 (Reeb) |
| G7 | CF02 | ι_R dα = 0 (Reeb) |
| G8 | CF02 | L·∇S = 0 (GENERIC) |
| G9 | CF02 | M·∇E = 0 (GENERIC) |
| G10 | CF03 | φ_bg = φ_+ tanh(z/ξ) |
| G11 | CF08 | χ_0 ∝ dφ_bg/dz |
| G12 | CF08 | {D, γ⁵} = a D γ⁵ D |
| G13-G17 | CF08 | Nielsen-Ninomiya P1-P5 |
| G18 | CF09 | A_μ real |
| G19 | CF09 | F_μν = -F_νμ |
| G20 | CF09 | ∂_[λ F_μν] = 0 (Bianchi) |
| G21 | CF09 | S gauge invariant |
| G22-G24 | CF07 | ρ Hermitian, positive, normalized |
| G25 | CF07 | ρ diagonal in pointer basis |
| G26 | CF07 | ||[H_SE, Π_i]|| ≤ ε |
| G27 | CF07 | Σ P(i) = 1 |
| G28 | CF07 | h_causal = c/v_th |
| G29 | CF03 | E_hier < E_uniform |
| G30 | CF03 | E_ε → c₀ Per |
| G31 | CF05 | ∇f · F = Kf |
| G32 | CF05 | dI/dt = 0 |
| G33-G34 | CF05 | H, S are Casimirs |
| G35 | CF05 | No extra Casimirs |

## Migration from v8

### Legacy Code

```python
# v8 style (still works)
from vdm_runtime import Connectome
connectome = Connectome(adj, n_nodes, max_degree)
connectome.step()  # Uses CF-derived mechanisms internally
```

### New CF-Aligned Code

```python
# v9 style (recommended)
from vdm_runtime import create_connectome_cf, run_simulation_cf
from vdm_runtime.gauge_emergence import compute_berry_connection

# Create with CF parameters
connectome = create_connectome_cf(
    adj, n_nodes, max_degree,
    hamiltonian=my_hamiltonian,
    parameter_range=params
)

# Create Berry connection from eigenstates
def eigenstate_func(x):
    # Return |ψ(x)⟩
    pass

berry = compute_berry_connection(eigenstate_func, coordinates)

# Run with gauge bosons
n_active, n_warm, n_bonds, kT = connectome.step_cf(berry, dt=0.1)
```

## Dependencies

- numpy >= 1.20
- scipy >= 1.7
- sympy >= 1.9 (for symbolic computations)

## License

See LICENSE file for details.

## References

- CF01: QGT to Metriplectic Brackets
- CF02: Contact to Metriplectic Evolution
- CF03: A8 Scaling and Hierarchical Interfaces
- CF04: Telegraph-Fisher Dynamics
- CF05: Integrability and Closure
- CF06: Information Geometry Foundations
- CF07: Measurement Theory and Decoherence
- CF08: Spinor Emergence via Domain-Wall Fermions
- CF09: Gauge Emergence via Berry Connection
- CF10: Lattice Fluids and Continuum
- CF11: Dark Sector Metriplectic
