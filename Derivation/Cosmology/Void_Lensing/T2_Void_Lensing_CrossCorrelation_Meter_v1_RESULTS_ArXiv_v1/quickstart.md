# T2 Void Lensing Cross-Correlation Meter v1 – Quickstart (ArXiv Package)

This folder contains a **self-contained, approval-free** snapshot of the code and configuration
needed to reproduce the synthetic-mocks calibration and tuned mocks-grid runs for the
T2 Void Lensing Cross-Correlation Meter v1, without cloning the full VDM repository.

The goal is to let an external reader:

- Re-run the **single-backend PyTwinPeaks calibration** and the
  **three-family v3 mocks grid** used in the paper.
- Inspect all relevant **code, specs, and schemas** in one place.
- Avoid any internal approval machinery or project-specific infrastructure.

This snapshot is intentionally minimal and focused on the two runs reported in the paper.

---

## 1. Contents

All paths below are relative to this directory:

- `main.tex` – LaTeX source of the arXiv paper.
- `references.bib` – BibTeX file for the paper.
- `logs/` – Curated JSON/CSV run logs for the canonical and v3-grid runs.
- `figures/` – PNG figures used in the paper.

### Code (standalone, no approvals)

- `code/run_void_lensing_meter_synthetic_mocks.py` – Standalone experiment runner:
  - Loads a mocks spec (v1 or v3 grid).
  - Builds a grid over `(backend, z_bin, R_v_bin, seed)`.
  - Generates synthetic profiles via the mocks backend.
  - Calls the void-lensing meter core in profile mode.
  - Aggregates metrics and evaluates H1–H3 gates.
  - Writes JSON / CSV logs and PNG diagnostics into `outputs/`.

- `code/meter.py` – Void-lensing meter core (profile-mode only):
  - Implements wall metrics (`S_wall`, `R^2_{\text{wall}}`),
    shoulder metrics (`A_{\text{sh}}`, `x_{\text{sh}}`),
    interface-count metrics (`\beta_{\text{interface}}`, uncertainty),
    and auxiliary diagnostics (SNR, quality flags).
  - Pure numpy, with no I/O, approvals, or survey-specific dependencies.

- `code/mocks.py` – Synthetic mocks backend:
  - Generates stacked convergence profiles `κ(x)` with:
    - A linear wall in `x ∈ [0.8, 1.2]`,
    - A compensation shoulder,
    - Controlled interface-count structure for testing `\beta`.
  - Provides three morphology families via the `mocks_family` parameter:
    - `"PyTwinPeaks"`,
    - `"FlagshipLike"`,
    - `"stress_test"`.
  - Also provides helper generators for shoulder/no-shoulder AUROC tests.

- `code/void_lensing_meter_gates.py` – Gate logic for H1–H3:
  - H1: `R^2_{\text{wall}} ≥ 0.98`,
  - H2: `\mathrm{AUROC}_{\text{sh}} ≥ 0.90`,
  - H3: `\beta_{\text{bias}} ≤ 0.10`.
  - Returns structured pass/fail status without any side effects.

- `code/io_paths.py` – Minimal I/O helper for this package:
  - Writes logs under `outputs/logs/...`.
  - Writes figures under `outputs/figures/...`.
  - **No approval env vars, no quarantine routing, no databases.**

These files are copies/variants of the corresponding modules from the full VDM repo,
but refactored to use only relative imports and a local `io_paths.py`. Any approval
or internal policy machinery has been removed.

### Specs and schemas

- `specs/void_lensing_meter-mocks-v1.json` – Single-backend PyTwinPeaks spec used
  for the canonical calibration run.
- `specs/void_lensing_meter-mocks-grid-v3.json` – Three-family v3 mocks-grid spec
  covering:
  - `backends = ["PyTwinPeaks", "FlagshipLike", "stress_test"]`,
  - `z_bins = [[0.2, 0.6], [0.6, 1.0]]`,
  - `R_v_bins = [[10.0, 30.0]]`,
  with shared control parameters (`n_radial_bins`, `x_wall_range`, `x_bg_range`,
  `lambda_ref`, `min_voids_per_bin`, etc.).
- `schemas/void_lensing_meter-v1.schema.json` – JSON schema describing the expected
  meter metrics payload.

---

## 2. Environment and dependencies

The standalone code is intentionally light on dependencies:

- Python ≥ 3.10 (tested with CPython 3.11).
- Python packages:
  - `numpy`
  - `matplotlib`

You can install these with:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\activate  # Windows PowerShell

pip install numpy matplotlib
```

No other external libraries, databases, or VDM-internal tooling are required.

---

## 3. Running the canonical PyTwinPeaks mocks calibration

From this directory:

```bash
cd Derivation/Cosmology/Void_Lensing/T2_Void_Lensing_CrossCorrelation_Meter_v1_RESULTS_ArXiv_v1

# Activate your virtualenv if you created one
# source venv/bin/activate

python code/run_void_lensing_meter_synthetic_mocks.py \
  --spec specs/void_lensing_meter-mocks-v1.json
```

This will:

1. Load the v1 spec (`void_lensing_meter-mocks-v1.json`).
2. Build a small grid with:
   - `backend = "PyTwinPeaks"`,
   - `z_bin = [0.2, 0.8]`,
   - `R_v_bin = [10.0, 60.0]`,
   - `seed ∈ {0, 1, 2, 3}`.
3. Generate synthetic profiles and run the meter.
4. Aggregate ensemble metrics and evaluate H1–H3.
5. Write artifacts under:

   - `outputs/logs/void_lensing/..._runs.json`
   - `outputs/logs/void_lensing/..._gates.json`
   - `outputs/logs/void_lensing/..._runs.csv`
   - `outputs/figures/void_lensing/..._profile.png`

The metrics in the `..._gates.json` file should match the canonical values
reported in the paper up to small floating-point differences:

- `R2_wall ≈ 1.0`,
- `AUROC_sh = 1.0`,
- `beta_bias = 0.0`,
- overall `status = "PASSED"`.

---

## 4. Running the tuned v3 mocks-grid calibration

To reproduce the three-family v3 mocks grid run used in the paper:

```bash
python code/run_void_lensing_meter_synthetic_mocks.py \
  --spec specs/void_lensing_meter-mocks-grid-v3.json
```

This will:

1. Load the v3 grid spec (`void_lensing_meter-mocks-grid-v3.json`).
2. Build a Cartesian grid over:

   - `backend ∈ {"PyTwinPeaks", "FlagshipLike", "stress_test"}`,
   - `z_bin ∈ {[0.2, 0.6], [0.6, 1.0]}`,
   - `R_v_bin ∈ {[10.0, 30.0]}`,
   - `seed ∈ {0, 1, 2, 3}`.

3. Generate synthetic profiles for each grid cell and run the meter.
4. Aggregate ensemble metrics and evaluate H1–H3.
5. Write artifacts under:

   - `outputs/logs/void_lensing_grid/..._runs.json`
   - `outputs/logs/void_lensing_grid/..._gates.json`
   - `outputs/logs/void_lensing_grid/..._runs.csv`
   - `outputs/figures/void_lensing_grid/..._profile.png`

The ensemble metrics in the v3 `..._gates.json` output should match the
Values reported in the paper (again up to floating-point noise):

- `R2_wall ≈ 0.9999999999999553`,
- `AUROC_sh = 1.0`,
- `beta_bias = 0.0`,
- overall `status = "PASSED"`.

---

## 5. How this differs from the full VDM repository

This arXiv snapshot is **not** a drop-in replacement for the full VDM
codebase. Key differences:

- **No approval system or policy checks.**
  - The internal `VDM_REQUIRE_APPROVAL`, `VDM_POLICY_APPROVED`, and
    quarantine routing are removed.
  - All runs write into `outputs/` under this directory without any
    authorization gates.

- **No provenance databases.**
  - The full repository tracks provenance via `run_receipts`, SQLite
    databases, and CI guards.
  - Here, logs are plain JSON/CSV files containing only what is needed
    to reproduce the paper’s metrics.

- **Focused scope.**
  - Only the meter core, mocks backend, gate logic, minimal I/O helper,
    and the specific v1/v3 specs and schema are included.
  - Real survey backends (HSC, DES, ACT, etc.) and other domains are
    intentionally omitted.

For authoritative, canonical code and for use in new experiments within
the VDM program, refer to the full repository and the canonical files
under:

- Meter and mocks: `Derivation/code/physics/cosmology/void_lensing/`
- Common helpers: `Derivation/code/common/`

This arXiv package is a **read-only, self-contained reproduction bundle**
for the T2 Void Lensing Cross-Correlation Meter v1 synthetic-mocks
calibration and tuned v3 mocks grid.