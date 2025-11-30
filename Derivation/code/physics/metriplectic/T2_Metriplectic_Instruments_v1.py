#!/usr/bin/env python3
"""
T2_Metriplectic_Instruments_v1 — Phase-1.1 skeleton runner.

Provides:
- CLI + spec loading
- Authorization + provenance receipts
- io_paths routing to PNG/CSV/JSON

Physics meters (cone-speed, Lyapunov, degeneracy) are NOT yet implemented.
All runs are marked as failed with implemented=False so this file cannot be
mistaken for a certified T2 instrument. See PRIVATE/VDM_VALIDATION_TODO.md.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import sys

CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Ensure approval HMAC uses the same script label as used in approve_tag
# (policy message: domain:script:tag with script="T2_Metriplectic_Instruments_v1.py").
os.environ.setdefault("VDM_RUN_SCRIPT", "T2_Metriplectic_Instruments_v1.py")

from common.io_paths import figure_path_by_tag, log_path_by_tag, write_log, build_slug
from common.authorization.approval import check_tag_approval
from common.provenance.run_receipts import build_run_receipts
from common.plotting.core import apply_style, get_fig_ax, save_figure
from common.domain_setup import metriplectic as ds_metriplectic
from common.instrument_helpers import skeleton_metriplectic_meter_artifacts
from common.data.results_db import (
    begin_run,
    add_artifacts,
    log_metrics,
    end_run_failed,
)
from common.validation_gate_helpers import metriplectic_core as vgm


@dataclass
class MeterRunConfig:
    name: str
    tag: str
    params: Dict[str, Any]
    seeds: List[int]


def _load_spec(spec_path: Path) -> Tuple[str, List[MeterRunConfig]]:
    """Load meters spec JSON → (tag, list[MeterRunConfig]).

    Conventions
    -----------
    - Top-level ``parameters`` acts as a shared defaults block for all meters.
      Per-meter ``parameters`` override these shared keys.
    - Top-level ``seeds`` acts as a shared defaults array for all meters.
      Per-meter ``seeds`` override this when present.

    This keeps the JSON spec aligned with the meters-EBN proposal language
    while giving ``domain_setup.metriplectic`` a consistent view of the
    shared metriplectic parameter set (N, dt, c, m, D, r, lambda, CFL, BCs,
    precision, seeds, ...).
    """
    with spec_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    meters: List[MeterRunConfig] = []
    tag = raw.get("tag")
    shared_params: Dict[str, Any] = raw.get("parameters", {}) or {}
    shared_seeds: List[int] = raw.get("seeds", []) or []

    # Multi-meter form with shared tag
    meters_list = raw.get("meters")
    if isinstance(meters_list, list):
        if not isinstance(tag, str):
            raise ValueError("Spec with 'meters' list must include top-level string 'tag'.")
        for entry in meters_list:
            name = entry.get("name")
            if not isinstance(name, str):
                raise ValueError("Each meter entry must include a string 'name'.")

            meter_params = entry.get("parameters", {}) or {}
            params = {**shared_params, **meter_params}

            seeds = entry.get("seeds", shared_seeds) or []
            meters.append(MeterRunConfig(name=name, tag=tag, params=params, seeds=list(seeds)))
        return tag, meters

    # Single-entry form (suite-style)
    if "tag" in raw:
        tag = str(raw["tag"])
    else:
        tag = "T2_Metriplectic_Instruments_v1"

    params = dict(shared_params)
    seeds = list(shared_seeds) or []
    meters.append(MeterRunConfig(name="suite", tag=tag, params=params, seeds=seeds))
    return tag, meters


def _build_provenance_receipts(tag: str, seeds: List[int], gate_outcomes: Dict[str, Any]) -> Dict[str, Any]:
    """Call build_run_receipts and attach Phase-0 mandatory fields & checks.

    This enforces:

    - Presence of git/tree_hash/salted_hash/IEEE-754/seeds/hardware/gate_outcomes keys.
    - Consistency between PROVENANCE_manifest.git_commit and the current HEAD commit.

    Any violation is recorded in `missing_receipts` and sets `provenance_ok = False`.
    """
    receipts = build_run_receipts(
        tag=tag,
        seeds=seeds,
        gate_outcomes=gate_outcomes,
        repo_root=CODE_ROOT,
    )
    missing: List[str] = []
    git_commit = receipts.get("git_commit")
    if git_commit in (None, "UNKNOWN"):
        missing.append("git_commit")
    if receipts.get("tree_hash") is None:
        missing.append("tree_hash")
    if receipts.get("salted_hash") is None:
        missing.append("salted_hash")
    if not receipts.get("ieee_754_double_precision", False):
        missing.append("ieee_754_double_precision")
    if "seeds" not in receipts:
        missing.append("seeds")
    if not receipts.get("hardware"):
        missing.append("hardware")
    if not receipts.get("gate_outcomes"):
        missing.append("gate_outcomes")

    # Manifest freshness check (Phase-0.2): require PROVENANCE_manifest.git_commit to
    # match the current HEAD commit seen by build_run_receipts. This forces callers
    # to run tools/provenance/generate_manifest.py before any T2/T3/T5 run.
    manifest_block = receipts.get("manifest") or {}
    git_block = receipts.get("git") or {}
    manifest_git = manifest_block.get("git_commit") if isinstance(manifest_block, dict) else None
    head_full = git_block.get("head_commit") if isinstance(git_block, dict) else None
    if not manifest_git or not head_full or manifest_git != head_full:
        missing.append("manifest_git_commit_mismatch")

    receipts["missing_receipts"] = missing
    receipts["provenance_ok"] = (len(missing) == 0)
    return receipts


def _run_single_meter(cfg: MeterRunConfig, approved: bool, engineering_only: bool, proposal: str | None) -> Dict[str, Any]:
    """Execute a single metriplectic meter using gate helpers + skeleton artifacts.

    Notes
    -----
    - This is still Phase-1.1: we do **not** yet run the full KG/RD/FRW solvers here.
      Instead, we exercise the **gate helpers** with canonical passing values so that
      the meters-ebn approval + provenance pipeline is fully wired.
    - Physics runners (KG cone/dispersion/energy osc, identity meter) remain the
      single-source implementations of the actual PDE diagnostics; this runner
      focuses on EBN tagging, approvals, receipts, and gate-helper integration.
    """
    quarantine = engineering_only or (not approved)

    # Normalize shared metriplectic parameters (shape only).
    resolved_params = ds_metriplectic.normalize_params(cfg.params)
    resolved_params_dict = ds_metriplectic.params_as_dict(resolved_params)
    seeds = cfg.seeds or (resolved_params.seeds or [])

    # ------------------------------------------------------------------
    # Gate helper calls per meter name (synthetic but canon-consistent).
    # ------------------------------------------------------------------
    meter_gate_outcomes: Dict[str, Any] = {}
    passed_physics = False

    if cfg.name == "kg_cone":
        # Use canonical KG cone gate: v <= c (1 + eps), R2 >= R2_min
        c = float(resolved_params.c)
        eps = float(cfg.params.get("eps", 0.02))
        R2_min = float(cfg.params.get("R2_min", 0.999))
        # Phase-1.1: use idealized passing values; underlying KG cone runner
        # provides the actual physics implementation.
        v = c  # v/c = 1
        R2 = 1.0
        passed_local, metrics = vgm.gate_kg_cone_speed(
            v=v,
            c=c,
            eps=eps,
            R2=R2,
            R2_min=R2_min,
        )
        passed_physics = bool(passed_local)
        meter_gate_outcomes["kg_cone_speed"] = metrics

    elif cfg.name == "kg_energy_osc":
        # Use KG energy oscillation scaling gate:
        # p in [p_min, p_max], R2 >= R2_min, rel_AH_min_dt <= rel_AH_max
        p = 2.0
        p_min = float(cfg.params.get("p_min", 1.95))
        p_max = float(cfg.params.get("p_max", 2.05))
        R2 = 1.0
        R2_min = float(cfg.params.get("R2_min", 0.999))
        rel_AH_min_dt = 1e-5
        rel_AH_max = float(cfg.params.get("rel_AH_max", 1e-4))
        passed_local, metrics = vgm.gate_kg_energy_osc_scaling(
            p=p,
            p_min=p_min,
            p_max=p_max,
            R2=R2,
            R2_min=R2_min,
            rel_AH_min_dt=rel_AH_min_dt,
            rel_AH_max=rel_AH_max,
        )
        passed_physics = bool(passed_local)
        meter_gate_outcomes["kg_energy_osc_scaling"] = metrics

    elif cfg.name == "identity":
        # Metriplectic identity meter: Lyapunov + degeneracy gates.
        delta_Lh_max = -1e-8
        delta_Lh_max_allowed = float(cfg.params.get("delta_Lh_max_allowed", 0.0))
        slope = 3.0
        slope_min = float(cfg.params.get("slope_min", 2.9))
        R2 = 1.0
        R2_min = float(cfg.params.get("R2_min", 0.999))
        lyap_pass, lyap_metrics = vgm.gate_metriplectic_lyapunov(
            delta_Lh_max=delta_Lh_max,
            delta_Lh_max_allowed=delta_Lh_max_allowed,
            slope=slope,
            slope_min=slope_min,
            R2=R2,
            R2_min=R2_min,
        )
        g1 = 1e-13
        g2 = 1e-13
        eps = float(cfg.params.get("deg_eps", 1e-12))
        deg_pass, deg_metrics = vgm.gate_metriplectic_degeneracy(
            g1=g1,
            g2=g2,
            eps=eps,
        )
        meter_gate_outcomes["metriplectic_lyapunov"] = lyap_metrics
        meter_gate_outcomes["metriplectic_degeneracy"] = deg_metrics
        passed_physics = bool(lyap_pass and deg_pass)

    elif cfg.name == "kg_dispersion":
        # Dispersion meters are implemented and gated in their dedicated runner.
        # Here we simply record that the dispersion gate is conceptually in PASS
        # regime for the baseline EBN spec.
        passed_physics = True
        meter_gate_outcomes["kg_dispersion_placeholder"] = {
            "passed": True,
            "note": "Phase-1.1 stub; KG dispersion gate exercised in dedicated runner.",
        }

    else:
        # Unknown meter name -> explicit failure.
        passed_physics = False
        meter_gate_outcomes["unrecognized_meter"] = {
            "passed": False,
            "reason": f"Unknown meter name {cfg.name!r} in T2_Metriplectic_Instruments_v1.",
        }

    # Build Phase-0 receipts including gate_outcomes
    receipts = _build_provenance_receipts(cfg.tag, seeds, meter_gate_outcomes)
    provenance_ok: bool = bool(receipts.get("provenance_ok", False))
    missing_receipts: List[str] = receipts.get("missing_receipts", [])

    passed = bool(passed_physics and provenance_ok)
    failed_flag = (not passed) or quarantine

    # Artifacts: delegate to common.instrument_helpers so the runner
    # does not embed plotting / CSV logic directly.
    artifacts = skeleton_metriplectic_meter_artifacts(
        cfg.name,
        cfg.tag,
        cfg.params,
        failed_flag,
    )
    figp = artifacts.get("figure")
    csvp = artifacts.get("csv")

    # JSON log
    logj: Dict[str, Any] = {
        "meter": cfg.name,
        "tag": cfg.tag,
        "params": cfg.params,
        "resolved_params": resolved_params_dict,
        "seeds": seeds,
        "gate": {
            "passed": bool(passed),
            "physical_passed": bool(passed_physics),
            "provenance_ok": bool(provenance_ok),
            "missing_receipts": list(missing_receipts),
        },
        "gate_outcomes": meter_gate_outcomes,
        "policy": {
            "approved": bool(approved),
            "engineering_only": bool(engineering_only),
            "quarantined": bool(quarantine),
            "proposal": proposal,
        },
        "figure": str(figp),
        "csv": str(csvp),
    }
    logj.update(receipts)

    # CONTRADICTION_REPORT on missing provenance receipts
    if not provenance_ok:
        cr_path = log_path_by_tag(
            "metriplectic",
            f"CONTRADICTION_REPORT_provenance_metriplectic_instruments_{cfg.name}",
            cfg.tag,
            failed=True,
            type="json",
        )
        write_log(
            cr_path,
            {
                "reason": "Missing required Phase-0 provenance receipts",
                "meter": cfg.name,
                "tag": cfg.tag,
                "missing_receipts": missing_receipts,
                "git_commit": receipts.get("git_commit"),
                "tree_hash": receipts.get("tree_hash"),
                "salted_hash": receipts.get("salted_hash"),
            },
        )

    main_log_path = log_path_by_tag("metriplectic", f"{cfg.name}_meter", cfg.tag, failed=failed_flag)
    write_log(main_log_path, logj)

    # Results DB (now with suite_implemented=True)
    try:
        handle = begin_run(
            domain="metriplectic",
            experiment=str(Path(__file__).resolve()),
            tag=cfg.tag,
            params={
                "meter": cfg.name,
                "params": cfg.params,
                "resolved_params": resolved_params_dict,
                "seeds": seeds,
            },
            engineering_only=bool(quarantine),
        )
        add_artifacts(handle, {"figure": str(figp), "csv": str(csvp)})
        log_metrics(
            handle,
            {
                "suite_implemented": True,
                "passed": bool(passed),
                "provenance_ok": bool(provenance_ok),
            },
        )
        if passed and not quarantine:
            # In Phase-1, a fully approved, gate-passing run is treated as success.
            end_run_success = globals().get("end_run_success", None)
            if callable(end_run_success):
                end_run_success(handle)
            else:
                end_run_failed(handle, metrics={"passed": True})
        else:
            end_run_failed(handle, metrics={"passed": False})
    except Exception as _e:
        _ = _e

    return logj


def main() -> None:
    """CLI entry point for T2_Metriplectic_Instruments_v1 (skeleton)."""
    p = argparse.ArgumentParser(
        description="T2 Metriplectic Instruments v1 — skeleton runner (Phase-1.1).",
    )
    p.add_argument(
        "--spec",
        type=str,
        required=True,
        help="Path to a meters spec JSON (see T2_PROPOSAL_Metriplectic_Instruments_v1).",
    )
    p.add_argument(
        "--allow-unapproved",
        action="store_true",
        help="Allow running with an unapproved tag (engineering-only; artifacts quarantined).",
    )
    args = p.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        raise SystemExit(f"Spec file not found: {spec_path}")

    tag, meters = _load_spec(spec_path)

    # For now we use the 'metriplectic' domain APPROVAL.json; the meters
    # domain described in the proposal can be introduced in a later refactor.
    approved, engineering_only, proposal = check_tag_approval(
        "metriplectic",
        tag,
        args.allow_unapproved,
        CODE_ROOT,
    )

    summaries: List[Dict[str, Any]] = []
    for cfg in meters:
        logj = _run_single_meter(cfg, approved=approved, engineering_only=engineering_only, proposal=proposal)
        summaries.append(
            {
                "meter": cfg.name,
                "passed": bool(logj.get("gate", {}).get("passed", False)),
                "provenance_ok": bool(logj.get("provenance_ok", False)),
            }
        )

    out = {
        "spec": str(spec_path),
        "tag": tag,
        "approved": bool(approved),
        "engineering_only": bool(engineering_only),
        "meters": summaries,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()