# Repository Facts

## Basic Information
- **Repository URL**: https://github.com/justinlietz93/Prometheus_FUVDM
- **Default Branch**: main  
- **HEAD Commit SHA**: cc751434d0882d76cb36f1624c384d7a1c623da0
- **Python Version**: 3.12.3

## Major Dependencies
- **PyTorch**: torch (deep learning framework)
- **NetworkX**: networkx (graph operations)
- **SciPy**: scipy (sparse matrix operations, scientific computing)
- **NumPy**: numpy (numerical computations)
- **Visualization**: matplotlib, plotly, dash
- **TDA**: ripser, persim (topological data analysis)
- **Audio**: librosa
- **Storage**: h5py, redis
- **Testing**: pytest

## Custom Extensions
- No custom C++/CUDA/ROCm extensions detected
- Pure Python implementation with scientific libraries

## Top-Level Module Tree (depth ≤ 3)

```
Prometheus_FUVDM/
├── fum_rt/                     # Main runtime system
│   ├── core/                   # Core algorithms
│   │   ├── connectome.py       # Dense connectome (validation-only)
│   │   ├── sparse_connectome.py # Void-faithful sparse implementation
│   │   ├── neuroplasticity/    # GDSP and plasticity
│   │   │   └── gdsp.py        # Graph Dynamic Structural Plasticity
│   │   └── cortex/            # Cortical structures
│   │       └── void_walkers/  # Walker implementations
│   ├── physics/               # Physics engines
│   │   └── rd_dispersion_runner.py # RD field validation
│   ├── nexus.py              # Main orchestrator
│   └── tests/                # Runtime tests
├── derivation/               # Theoretical foundations
│   ├── code/                 # Derivation code and validation
│   │   ├── physics/          # Physics implementations
│   │   └── tests/           # Theory validation tests
│   └── CORRECTIONS.md       # Key theoretical corrections
├── fum_live.py              # Main entry point  
└── test_axiomatic_theory.py # Theory validation
```

## Core File Glossary

### Runtime Core (fum_rt/)
- `nexus.py` - Main orchestration loop; coordinates walkers, GDSP, and events
- `core/connectome.py` - Dense connectome implementation (FORCE_DENSE required)
- `core/sparse_connectome.py` - Void-faithful sparse connectome for scale
- `core/neuroplasticity/gdsp.py` - Single-writer topology/weight authority
- `core/cortex/void_walkers/base.py` - Base walker with TTL-limited exploration
- `core/cortex/void_walkers/void_heat_scout.py` - Heat-driven walker
- `core/cortex/void_walkers/void_ray_scout.py` - Physics-aware gradient walker
- `core/cortex/void_walkers/void_memory_ray_scout.py` - Memory-driven walker
- `physics/rd_dispersion_runner.py` - RD field engine validation runner

### Entry Points  
- `fum_live.py` - Main live system entry point
- `fum_rt/run_nexus.py` - Nexus runner with configuration options

### Theory & Validation (derivation/)
- `derivation/CORRECTIONS.md` - Critical theoretical corrections and validations  
- `derivation/code/physics/` - Physics engine implementations and validation
- `test_axiomatic_theory.py` - Top-level axiomatic theory validation

### Configuration
- `requirements.txt` - Python dependencies
- `run_profiles/` - Runtime configuration profiles (if present)