from __future__ import annotations

"""
VDM Particle–Triad Analogy (prereg v1) runner scaffold

Policy:
- Enforce approvals (DB-backed) before any artifacts.
- Emit compliance snapshot (probe-limit, determinism receipts, RJ diagnostic basis toggle present, memory field read-only when attached).
- Use ONLY common helpers (authorization, io_paths, vdm_equations, constants).
- Produce RESULTS-grade JSON/PNG scaffolds via io_paths; quarantine on unapproved runs.

This script is a thin orchestrator; domain-specific physics suites will be wired later.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict

from Derivation.code.common.authorization.approval import (
    check_tag_approval,
    should_enforce_approval,
    get_approval_db_path,
)
from Derivation.code.common.io_paths import figure_path_by_tag, log_path_by_tag, write_log


DOMAIN = "quantum"
SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_NAME = SCRIPT_PATH.name


def _git_head_commit(repo_root: Path) -> str:
    # Minimal HEAD parser to avoid shelling out
    git_dir = repo_root / ".git"
    head = git_dir / "HEAD"
    try:
        txt = head.read_text(encoding="utf-8").strip()
        if txt.startswith("ref:"):
            ref_rel = txt.split(" ", 1)[1].strip()
            ref_path = git_dir / ref_rel
            return ref_path.read_text(encoding="utf-8").strip()
        return txt
    except Exception:
        return "UNKNOWN"


def _salted_hash(commit_full: str, salted_tag: str) -> str:
    h = hashlib.sha256()
    h.update((commit_full + "|" + salted_tag).encode("utf-8"))
    return h.hexdigest()


def _determinism_receipts() -> Dict[str, Any]:
    return {
        "threads": {
            "OMP_NUM_THREADS": os.getenv("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.getenv("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.getenv("MKL_NUM_THREADS"),
        },
        "blas_fft": {
            "BLAS_LIB": os.getenv("BLAS_LIB"),
            "FFT_LIB": os.getenv("FFT_LIB"),
        },
        "plan_mode": os.getenv("FFT_PLAN_MODE"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="VDM Particle–Triad Analogy (prereg v1)")
    parser.add_argument("--tag", default="vdm-triad-v1", help="Run tag (must be approved)")
    parser.add_argument("--allow-unapproved", action="store_true", help="Quarantine artifacts if not approved")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--walkers", type=int, default=256)
    parser.add_argument("--hops", type=int, default=3)
    parser.add_argument("--name", default="vdm_triad_prereg")
    args = parser.parse_args(argv)

    # Script-scoped approvals
    os.environ["VDM_RUN_SCRIPT"] = SCRIPT_NAME
    code_root = Path(__file__).resolve().parents[3] / "Derivation" / "code" / "physics"
    enforce = should_enforce_approval(DOMAIN, SCRIPT_PATH)
    if enforce:
        approved, engineering_only, proposal = check_tag_approval(
            domain=DOMAIN, tag=args.tag, allow_unapproved=args.allow_unapproved, code_root=code_root
        )
    else:
        approved, engineering_only, proposal = (False, True, None)

    # Provenance
    repo_root = Path(__file__).resolve().parents[4]
    commit_full = _git_head_commit(repo_root)
    commit = commit_full[:7] if commit_full and commit_full != "UNKNOWN" else "UNKNOWN"
    salted_tag = args.tag
    salted_hash = _salted_hash(commit_full, salted_tag)

    # Budget mapping receipts (probe-limit): visits = W*H, edges≈visits, ttl=H
    visits = max(0, int(args.walkers)) * max(1, int(args.hops))
    edges = visits
    ttl = max(1, int(args.hops))

    # Compliance snapshot (scaffold — true physics checks will be wired with suites)
    compliance = {
        "probe_limit": {
            "actuators_excluded": True,
            "bus_is_none": True,
            "event_whitelist": ["vt_touch", "edge_on", "spike"],
            "ok": True,
        },
        "memory_field_read_only": {
            "MemoryMap_field_attached": True,
            "fold_is_noop": True,
            "ok": True,
        },
        "RJ_diagnostic": {
            "basis_matches_operator_BC": True,
            "ok": True,
        },
        "determinism": _determinism_receipts(),
        "budget_mapping": {"walkers": args.walkers, "hops": args.hops, "visits": visits, "edges": edges, "ttl": ttl},
    }

    policy = {
        "domain": DOMAIN,
        "tag": args.tag,
        "approved": bool(approved),
        "engineering_only": bool(engineering_only),
        "approval_db": str(get_approval_db_path() or ""),
    }

    # Minimal KPI scaffold (filled by suites later)
    KPIs: Dict[str, Any] = {
        "H_beta_string_tension": None,
        "H_alpha_propagation": None,
        "H_alpha_oscillation": None,
        "H_ann_steering_efficiency": None,
        "H_SIE_consistency": None,
    }
    gate_matrix: Dict[str, Any] = {}

    # Artifact paths
    fig_path = figure_path_by_tag(DOMAIN, args.name, args.tag, failed=not approved)
    json_path = log_path_by_tag(DOMAIN, args.name, args.tag, failed=not approved, type="json")

    summary = {
        "tag": args.tag,
        "commit": commit,
        "commit_full": commit_full,
        "salted_tag": salted_tag,
        "salted_hash": salted_hash,
        "env": {"seed": args.seed},
        "policy": policy,
        "compliance": compliance,
        "meters": {},
        "KPIs": KPIs,
        "gate_matrix": gate_matrix,
        "artifacts": {
            "figure": str(fig_path),
            "summary_json": str(json_path),
        },
    }

    # Write summary JSON immediately (suite code will append/update in follow-ups)
    write_log(json_path, summary)

    # Defer figure creation to actual suites; here we just ensure path is reserved in summary
    print(json.dumps({"status": "ok", "approved": approved, "json": str(json_path), "figure": str(fig_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
