# Derivation Outputs (Figures + Logs)

This folder is the canonical on-disk destination for experiment artifacts produced by code under `Derivation/code/`.

Use the IO helper for all writes:

- `Derivation/code/common/io_paths.py`
- This data is also held in [Google Drive](https://drive.google.com/drive/folders/1AQIXT0VUrPuYPUzLYgOyT-4GvNbUF3JK?usp=drive_link)

## Directory layout

- `figures/<domain>/...`
  - PNGs (and occasional media) produced by runs.
- `logs/<domain>/...`
  - Machine-readable run logs (JSON) and tabular summaries (CSV).

Each domain folder may contain a `failed_runs/` subfolder. Runs are automatically quarantined there when policy requires it.

## Artifact requirements (minimum)

For any experiment run that claims a result:

- At least **1 figure** (usually `.png`)
- At least **1 JSON log** (full params + metrics)
- At least **1 CSV log** (summary / sweep table)

## Naming convention

Artifacts are timestamp-prefixed using `YYYYmmdd_HHMMSS` and a human slug:

- `figures/<domain>/YYYYmmdd_HHMMSS_<slug>.png`
- `logs/<domain>/YYYYmmdd_HHMMSS_<slug>.json`
- `logs/<domain>/YYYYmmdd_HHMMSS_<slug>.csv`

The slug should be stable and descriptive (e.g., `corner_test_r_c_scan`, `dp_noise_budget_smoke`).

## Policy / quarantine behavior

The IO helper enforces the local policy gate:

- If approval is required and not granted, `failed=True` is forced and artifacts go under `failed_runs/`.
- If `VDM_POLICY_HARD_BLOCK=1` is set and approval is missing, the run should raise instead of writing.

This keeps unapproved runs from being mixed into “success” outputs.

## Example usage (Python)

```python
import matplotlib.pyplot as plt

from common.io_paths import figure_path, log_path, write_log

domain = "fluid_dynamics"
slug = "corner_test_r_c_scan"

# ... run simulation, compute metrics -> metrics dict

fig_out = figure_path(domain, slug, failed=False)
plt.savefig(fig_out, dpi=160, bbox_inches="tight")

write_log(
  log_path(domain, slug, failed=False, type="json"),
  {
    "domain": domain,
    "slug": slug,
    "seed": 1234,
    "params": {"...": "..."},
    "metrics": {"...": "..."},
    "status": "success",
  },
)
```

## Linking artifacts in Derivation markdown

From a markdown file under `Derivation/`, link artifacts like:

- `![Caption](code/outputs/figures/<domain>/YYYYmmdd_HHMMSS_<slug>.png)`
- `[Run log](code/outputs/logs/<domain>/YYYYmmdd_HHMMSS_<slug>.json)`

## Provenance indexing

This directory is included in the automated provenance indexing system via:

- `Derivation/code/outputs/PROVENANCE_index.json`

The parent code tree is also indexed separately via:

- `Derivation/code/PROVENANCE_index.json`

## Off-repo storage (when artifacts are too large)

If an artifact set is too large to live in git, store it off-repo (e.g., Drive) and register it in the remote artifacts index under `runs/`.
