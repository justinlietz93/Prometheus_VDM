# VDM Physics Derivation Project Structure

## RULES

- **ALL** domain folders under Derivation/code/physics REQUIRE the following items:
  - schema/
  - specs/
  - APPROVALS.json
  - README.md
- **ALL** experiments MUST use the helpers in common/ for logs and figures handling, and can additionally be used for existing equations, constants, and additional theory-wide resources.

```plaintext
Derivation/
>> ├── .gitignore
   └── code/
>>     ├── Void_Debt_Modulation.py
       │   (LOC: 136, Size: 5.8 KB)
>>     ├── Void_Equations.py
       │   (LOC: 120, Size: 4.7 KB)
>>     ├── __init__.py
       │   (LOC: 1, Size: 42 B)
       ├── analysis/
>>     │   ├── README.md
       │   │   (LOC: 25, Size: 1.1 KB)
>>     │   ├── build_and_test_H_candidate.py
       │   │   (LOC: 160, Size: 5.5 KB)
>>     │   ├── edge_ansatz_fit.py
       │   │   (LOC: 23, Size: 560 B)
>>     │   ├── fit_H_edge.py
       │   │   (LOC: 103, Size: 3.3 KB)
>>     │   ├── flux_sweep.py
       │   │   (LOC: 125, Size: 4.7 KB)
>>     │   ├── flux_symbolic.py
       │   │   (LOC: 18, Size: 460 B)
>>     │   ├── flux_symbolic_full.py
       │   │   (LOC: 100, Size: 3.8 KB)
>>     │   ├── grid_tau0.py
       │   │   (LOC: 122, Size: 4.1 KB)
>>     │   └── optimize_H_params.py
       │       (LOC: 195, Size: 6.5 KB)
       ├── common/
>>     │   ├── __init__.py
       │   │   (LOC: 1, Size: 49 B)
       │   ├── authorization/
>>     │   │   ├── README.md
       │   │   │   (LOC: 37, Size: 1.5 KB)
>>     │   │   ├── __init__.py
       │   │   │   (LOC: 7, Size: 213 B)
>>     │   │   ├── approval.py
       │   │   │   (LOC: 627, Size: 25.1 KB)
>>     │   │   └── approve_tag.py
       │   │       (LOC: 318, Size: 13.7 KB)
>>     │   ├── constants.py
       │   │   (LOC: 140, Size: 5.4 KB)
       │   ├── data/
>>     │   │   ├── __init__.py
       │   │   │   (LOC: 0, Size: 0 B)
>>     │   │   ├── approval.db
       │   │   │   (LOC: 0, Size: 0 B)
       │   │   ├── result_data/
>>     │   │   └── results_db.py
       │   │       (LOC: 494, Size: 20.2 KB)
       │   ├── domain_setup/
>>     │   │   ├── README.md
       │   │   │   (LOC: 29, Size: 1.7 KB)
>>     │   │   └── __init__.py
       │   │       (LOC: 0, Size: 0 B)
>>     │   ├── io_paths.py
       │   │   (LOC: 118, Size: 4.5 KB)
       │   ├── plotting/
>>     │   │   ├── README.md
       │   │   │   (LOC: 25, Size: 1.0 KB)
>>     │   │   ├── __init__.py
       │   │   │   (LOC: 11, Size: 538 B)
>>     │   │   ├── core.py
       │   │   │   (LOC: 50, Size: 1.3 KB)
>>     │   │   ├── helpers.py
       │   │   │   (LOC: 156, Size: 4.5 KB)
>>     │   │   └── types.py
       │   │       (LOC: 24, Size: 629 B)
>>     │   └── vdm_equations.py
       │       (LOC: 266, Size: 9.0 KB)
       ├── computational_toy_proofs/
       ├── obs/
>>     │   ├── README.md
       │   │   (LOC: 24, Size: 857 B)
>>     │   └── walker_glow.py
       │       (LOC: 140, Size: 4.7 KB)
       ├── outputs/
       │   ├── figures/
       │   │   ├── agency/
       │   │   │   └── failed_runs/
       │   │   ├── collapse/
       │   │   │   └── failed_runs/
       │   │   ├── conservation_law/
       │   │   │   └── failed_runs/
       │   │   ├── cosmology/
       │   │   │   └── failed_runs/
       │   │   ├── dark_photons/
       │   │   │   └── failed_runs/
       │   │   ├── fluid_dynamics/
       │   │   │   └── failed_runs/
       │   │   ├── memory_steering/
       │   │   │   └── failed_runs/
       │   │   ├── metriplectic/
       │   │   │   └── failed_runs/
       │   │   ├── rd_conservation/
       │   │   │   └── failed_runs/
       │   │   └── reaction_diffusion/
       │   │       └── failed_runs/
       │   └── logs/
       │       ├── agency/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── collapse/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── conservation_law/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── cosmology/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── dark_photons/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── fluid_dynamics/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── memory_steering/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── metriplectic/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       ├── rd_conservation/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       │       └── reaction_diffusion/
       │       │   ├── failed_runs/
>>     │       │   └── README.md
       ├── physics/
>>     │   ├── README.md
       │   ├── agency/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── axioms/
>>     │   │   └── verify_discrete_EL.py
       │   ├── collapse/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── conservation_law/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── cosmology/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── dark_photons/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── fluid_dynamics/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── memory_steering/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── metriplectic/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   ├── rd_conservation/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       │   └── reaction_diffusion/
>>     │   │   ├── APPROVAL.json
>>     │   │   ├── specs/
       │   │   └── schemas/
       └── tests/
>>         ├── README.md
           ├── fluid_dynamics/
           ├── memory_steering/
           ├── reaction_diffusion/
>>         ├── etc...
```
