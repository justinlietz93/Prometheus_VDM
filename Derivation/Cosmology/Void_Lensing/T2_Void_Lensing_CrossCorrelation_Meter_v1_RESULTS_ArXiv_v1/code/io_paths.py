from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Minimal I/O helpers for the T2 Void Lensing Cross-Correlation Meter v1 arXiv
package.

This module provides a tiny subset of the functionality of the full VDM
`Derivation.code.common.io_paths` helpers, but is completely self-contained
and approval-free:

- no environment variables,
- no provenance databases,
- no quarantine routing.

All paths are resolved relative to the arXiv package root and written under
an `outputs/` directory in this tree.
"""

from pathlib import Path
from typing import Any
from datetime import datetime
import json

__all__ = ["build_slug", "log_path", "figure_path", "write_log"]


def _root_dir() -> Path:
    """Return the arXiv package root directory."""
    # This file lives in <root>/code/io_paths.py
    return Path(__file__).resolve().parent.parent


def build_slug(experiment_name: str, run_name: str, tag: str | None = None) -> str:
    """
    Build a timestamped slug for log and figure filenames.

    The format roughly matches the canonical VDM convention:

        YYYYMMDD_HHMMSS_experiment_name_run_name[_tag]
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    parts = [timestamp, experiment_name, run_name]
    if tag is not None and tag != "":
        parts.append(tag)
    return "_".join(parts)


def log_path(domain: str, slug: str, failed: bool = False, type: str = "json") -> Path:
    """
    Construct a path for a log file under outputs/logs/{domain}/....

    Parameters
    ----------
    domain:
        Logical subdirectory, e.g. "void_lensing" or "void_lensing_grid".
    slug:
        Filename stem without extension.
    failed:
        If True, the file is routed under a "failed_runs/" subdirectory.
    type:
        File extension (e.g. "json" or "csv").
    """
    root = _root_dir() / "outputs" / "logs" / domain
    if failed:
        root = root / "failed_runs"
    root.mkdir(parents=True, exist_ok=True)
    ext = type.lstrip(".")
    return root / f"{slug}.{ext}"


def figure_path(domain: str, slug: str, failed: bool = False) -> Path:
    """Construct a path for a PNG figure under outputs/figures/{domain}/...."""
    root = _root_dir() / "outputs" / "figures" / domain
    if failed:
        root = root / "failed_runs"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"{slug}.png"


def write_log(path: Path, payload: Any) -> None:
    """Write a JSON payload to disk with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")