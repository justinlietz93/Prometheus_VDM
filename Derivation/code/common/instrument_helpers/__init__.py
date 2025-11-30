"""
Common instrument helpers for VDM runners.

This module provides reusable utilities for constructing meter-level
artifacts (PNG + CSV) in a way that keeps physics runners thin and
delegates plotting/IO details here.

For Phase-1 of the metriplectic instruments (meters-EBN) we expose a
skeleton helper that produces placeholder artifacts for meters that are
not yet implemented, while still exercising:

- Canonical plotting helpers
- Canonical io_paths routing (via common.plotting.core and common.io_paths)
- Consistent CSV structure for per-meter summaries

Physics-specific meters (cone-speed, Lyapunov, degeneracy) will later
extend this with real diagnostics while preserving this interface.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from common.plotting.core import apply_style, get_fig_ax, save_figure
from common.io_paths import log_path_by_tag, write_log
from common.domain_setup import metriplectic as ds_metriplectic


def skeleton_metriplectic_meter_artifacts(
    meter_name: str,
    tag: str,
    raw_params: Dict[str, Any],
    failed: bool,
) -> Dict[str, Path]:
    """
    Create placeholder artifacts for an unimplemented metriplectic meter.

    This helper is used during Phase-1.1/1.2 so that:
    - Runners do not embed plotting/CSV logic directly.
    - Artifacts are still routed via canonical helpers.
    - Normalized metriplectic parameters are visible in the CSV/JSON layer.

    Parameters
    ----------
    meter_name:
        Short meter name, e.g. "kg_cone", "kg_dispersion", "kg_energy_osc", "identity".
    tag:
        Spec tag string, e.g. "meters-ebn.v1" or a temporary skeleton tag.
    raw_params:
        Raw parameters dict from the spec entry for this meter.
    failed:
        Whether this run should be treated as failed / quarantined for IO routing.

    Returns
    -------
    artifacts:
        Dict with keys:
        - "figure": Path to the PNG placeholder figure.
        - "csv":    Path to a CSV stub summarizing the meter and params.
    """
    # Normalize shared parameters for visibility
    resolved = ds_metriplectic.normalize_params(raw_params)
    resolved_dict = ds_metriplectic.params_as_dict(resolved)

    # Placeholder figure
    apply_style("light")
    fig, ax = get_fig_ax(size=(6.0, 3.5))
    ax.axis("off")
    ax.text(
        0.5,
        0.55,
        f"{meter_name} meter (skeleton)",
        ha="center",
        va="center",
        fontsize=12,
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.35,
        "Implementation pending Phase-1.3/1.4/1.5.",
        ha="center",
        va="center",
        fontsize=8,
        transform=ax.transAxes,
    )
    slug = f"{meter_name}_meter__{tag}"
    fig_path = save_figure("metriplectic", slug, fig, failed=failed)

    # Minimal CSV with normalized params flattened as JSON string for now
    csv_path = log_path_by_tag(
        "metriplectic",
        f"{meter_name}_meter",
        tag,
        failed=failed,
        type="csv",
    )
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8") as fcsv:
        fcsv.write("name,tag,implemented,passed,params_normalized_json\n")
        import json as _json

        fcsv.write(
            f"{meter_name},{tag},False,False,"
            f"{_json.dumps(resolved_dict, sort_keys=True)}\n"
        )

    # Optionally emit a tiny JSON sidecar for quick inspection (no gates here)
    json_path = log_path_by_tag(
        "metriplectic",
        f"{meter_name}_meter_skeleton",
        tag,
        failed=failed,
        type="json",
    )
    write_log(
        json_path,
        {
            "meter": meter_name,
            "tag": tag,
            "implemented": False,
            "passed": False,
            "resolved_params": resolved_dict,
            "figure": str(fig_path),
            "csv": str(csv_path),
        },
    )

    return {"figure": fig_path, "csv": csv_path, "json": json_path}


__all__ = [
    "skeleton_metriplectic_meter_artifacts",
]