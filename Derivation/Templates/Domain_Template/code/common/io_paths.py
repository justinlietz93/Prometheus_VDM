# derivation/code/common/io_paths.py
'''
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


# Example usage inside a physics script:

from pathlib import Path
import matplotlib.pyplot as plt
from common.io_paths import figure_path, log_path, write_log

domain, slug = "fluid_dynamics", "corner_test_r_c_scan"

# ... run simulation, compute metrics -> 'metrics' dict

# Save figure
fig_path = figure_path(domain, slug, failed=False)
plt.savefig(fig_path, dpi=160, bbox_inches="tight")

# Save log
log = {
    "timestamp": __import__("datetime").datetime.now().isoformat(),
    "git_hash": "YOUR_GIT_HASH_HERE",
    "seed": 1234,
    "domain": domain,
    "slug": slug,
    "params": {"H":1.0, "nu":1e-3, "...":"..."},
    "metrics": metrics,
    "status": "success"
}
write_log(log_path(domain, slug, failed=False, type="json"), log)

# In Markdown (relative to derivation/):
# ![Corner test r_c scan](code/outputs/figures/fluid_dynamics/20250823_corner_test_r_c_scan.png)
# [Run log](code/outputs/logs/fluid_dynamics/20250823_corner_test_r_c_scan.json)

'''
import csv
from pathlib import Path
from datetime import datetime
import json
import os

DERIVATION_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = DERIVATION_ROOT / "outputs"

def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(p: Path) -> Path:
    """Ensure that a directory exists."""
    p.mkdir(parents=True, exist_ok=True)
    return p

def build_slug(name: str, tag: str | None = None) -> str:
    """Build a canonical slug from a base name and optional tag.
    Keeps policy centralized so figures/logs remain consistent across experiments.
    """
    base = str(name).strip()
    if tag is None or str(tag).strip() == "":
        return base
    return f"{base}_{str(tag).strip()}"

def figure_path(domain: str, slug: str, failed: bool=False) -> Path:
    """Generate a path for saving a figure.
    Args:
        domain (str): The domain of the experiment (e.g., "fluid_dynamics").
        slug (str): A short descriptive identifier for the experiment.
        failed (bool): Whether this is for a failed run."""
    base = OUTPUTS / "figures" / domain / ("failed_runs" if failed else "")
    return ensure_dir(base) / f"{_ts()}_{slug}.png"

def figure_path_by_tag(domain: str, name: str, tag: str | None, failed: bool=False) -> Path:
    """Figure path using name+optional tag to build the slug centrally."""
    return figure_path(domain, build_slug(name, tag), failed=failed)

def log_path(domain: str, slug: str, failed: bool=False, type: str="json") -> Path:
    """Generate a path for saving a log file.
    Args:
        domain (str): The domain of the experiment (e.g., "fluid_dynamics").
        slug (str): A short descriptive identifier for the experiment.
        failed (bool): Whether this is for a failed run.
        type (str): The log file type, either 'json' or 'csv'."""
    base = OUTPUTS / "logs" / domain / ("failed_runs" if failed else "")
    return ensure_dir(base) / f"{_ts()}_{slug}.{type}"

def log_path_by_tag(domain: str, name: str, tag: str | None, failed: bool=False, type: str="json") -> Path:
    """Log path using name+optional tag to build the slug centrally."""
    return log_path(domain, build_slug(name, tag), failed=failed, type=type)

def write_log(path: Path, data: dict):
    """Write a log file in JSON or CSV format.
    Args:
        path (Path): The file path to write the log to.
        data (dict): The log data to write."""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        if path.suffix == ".json":
            json.dump(data, f, indent=2, sort_keys=True)
        elif path.suffix == ".csv":
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
