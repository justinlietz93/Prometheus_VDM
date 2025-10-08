# VDM Physics Derivation Project Structure

***Last updated: October 8, 2025 @ 3:34 AM***

## RULES

- **ALL** domain folders under `Derivation/code/physics` REQUIRE the following items:
  - `schema/` contains required schema files
  - `specs/` contains required spec files used to configure experiments and other metadata
  - `APPROVALS.json` contains required approval information
  - `README.md` contains required background, equations, and methods for experiments
- **ALL** experiments MUST use the helpers in `common/` for logs and figures handling, and can additionally be used for existing equations, constants, and additional theory-wide resources.
- Just for context, here are all current helpers:
  - `Derivation/code/common/authorization` **This is wired into the other helpers to enforce approval system**
  - `Derivation/code/common/plotting` **This is used by other helpers for plotting and creating figures**
  - `Derivation/code/common/data` **This is where admin credentials, approvals, and experiment results data is stored**
  - `Derivation/code/common/domain_setup` **This includes helpers for scaffolding new experiment code domain folders**
  - `Derivation/code/common/vdm_equations.py` **This should include all available equations involved in the Void Dynamics Theory**
  - `Derivation/code/common/io_paths.py` **This is a helper that correctly routes log and figure files to the respective folders**
  - `Derivation/code/common/constants.py` **Like the vdm_equations.py file, except it contains all the VDM specific constants for us in experiments**

```plaintext
Derivation/
>> ├── .gitignore
   └── code/
>>     ├── __init__.py
       ├── analysis/
       ├── common/
>>     │   ├── __init__.py
       │   ├── authorization/
>>     │   ├── constants.py
       │   │   (LOC: 140, Size: 5.4 KB)
       │   ├── data/
       │   ├── domain_setup/
>>     │   ├── io_paths.py
       │   │   (LOC: 118, Size: 4.5 KB)
       │   ├── plotting/
>>     │   └── vdm_equations.py
       │       (LOC: 266, Size: 9.0 KB)
       ├── computational_toy_proofs/ (Historical, not used. Just ignore this.)
       ├── obs/
       ├── outputs/
       │   ├── figures/
       │   │   ├── agency/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md (Explains plot methodology and reasoning)
       │   │   ├── collapse/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── conservation_law/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── cosmology/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── dark_photons/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── fluid_dynamics/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── memory_steering/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── metriplectic/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   ├── rd_conservation/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   │   └── reaction_diffusion/
       │   │   │   ├── failed_runs/
       │   │   │   └── README.md
       │   └── logs/
       │       ├── agency/
       │       │   ├── failed_runs/
>>     │       │   └── README.md (Explains experiment methodology and reasoning)
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
