# Physics scripts (Derivation/code/physics/{domain}/)

Purpose

- Domain-scoped simulation and benchmark scripts. These are the source of truth for producing physics figures and logs under Derivation/code/outputs/.

## Rules

- **ALL** domain folders under `Derivation/code/physics` REQUIRE the following items:
  - `schema/` contains required schema files
  - `specs/` contains required spec files used to configure experiments and other metadata
  - `APPROVALS.json` contains required approval information
  - `README.md` contains required background, equations, and methods for experiments
- **ALL** experiments MUST use the helpers in `common/` for logs and figures handling, and can additionally be used for existing equations, constants, and additional theory-wide resources.
- Just for context, here are all current helpers:
  - `Derivation/code/common/authorization` **This is wired into the other helpers to enforce approval system**
    - Read this for context: [authorization/README.md](/Derivation/code/common/authorization/README.md)
  - `Derivation/code/common/plotting` **This is used by other helpers for plotting and creating figures**
  - `Derivation/code/common/data` **This is where admin credentials, approvals, and experiment results data is stored**
  - `Derivation/code/common/domain_setup` **This includes helpers for scaffolding new experiment code domain folders**
  - `Derivation/code/common/vdm_equations.py` **This should include all available equations involved in the Void Dynamics Theory**
  - `Derivation/code/common/io_paths.py` **This is a helper that correctly routes log and figure files to the respective folders**
  - `Derivation/code/common/constants.py` **Like the vdm_equations.py file, except it contains all the VDM specific constants for us in experiments**

## Directory layout

- Each research domain gets its own subfolder and must be scaffolded as follows:
  - Derivation/code/physics/{domain}/
    - schemas/{schema_name}.schema.json
    - specs/{spec_name}.{run_tag}.json
    - APPROVAL.json (this is where approval hashes will be checked against)
    - Any experiment scripts, code files, or other experiment specific extras will go here. Run scripts will need to import and use the common/ helpers, and have the designated tag. See [Metriplectic/](/Derivation/code/physics/metriplectic) as an example.

## Output routing

- Always use the [io_paths.py](/Derivation/code/common/io_paths.py) helper to handle this.
- Figures → Derivation/code/outputs/figures/{domain}/
- Logs    → Derivation/code/outputs/logs/{domain}/
- Filenames: YYYYMMDD_hhmmss_{experiment name}_{tag}.ext (UTC timestamp)

## Conventions

- Location: Derivation/code/physics/{domain}/*.py
- Scripts must:
  - Accept reproducible CLI (with seeds where applicable).
  - Emit JSON logs with theory, params, metrics, outputs.figure, timestamp.
  - Emit a PNG figure (unless explicitly headless by design).
  - Record a pass/fail gate in metrics when applicable.
  - Use all helpers that are relevant / required: Derivation/code/common
  - Be approved by Justin K. Lietz, read the authorization README: Derivation/code/common/authorization/README.md
- Heavy numerics go here; unit tests belong under Derivation/code/tests/{domain}/.

## Examples

## Metriplectic (KG RD)

- [Approved Metriplectic Experiments](/Derivation/code/physics/metriplectic)
- Pre-requisite PROPOSAL writeups, along with post experiment RESULTS writeups: [Derivation/Metriplectic](/Derivation/Metriplectic)

## Fluid Dynamics (LBM→NS)

- Solver:
  - [fluids/lbm2d.py](/Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1)
- Taylor-Green benchmark:
  - Runs TG vortex and fits log E(t) to recover ν.
  - Uses lattice scaling K² = k²(1/nx² + 1/ny²).
  - Outputs → figures/logs under fluid_dynamics/.
- Lid-driven cavity benchmark:
  - Runs no-slip box with moving lid; monitors ‖∇·v‖₂.
  - Outputs → figures/logs under fluid_dynamics/.
