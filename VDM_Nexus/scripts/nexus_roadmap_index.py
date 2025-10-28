#!/usr/bin/env python3
"""
VDM Nexus — Roadmap Index Builder (Phase 1 · Task 1.3)

Purpose:
- Build a read-only, structured index of experiments from canonical sources to support Nexus dashboard surfaces.
- Do NOT derive maturity tiers from Markdown; only link to tier standards and progress summaries.
- Source of truth remains in Derivation/. This tool just enumerates and aggregates paths/metadata.

Canonical references (read-only; do not parse for logic):
- Tier ladder and standards: [TIER_STANDARDS.md](../../Derivation/TIER_STANDARDS.md:1)
- Canon map: [CANON_MAP.md](../../Derivation/CANON_MAP.md:1)
- Data products: [DATA_PRODUCTS.md](../../Derivation/DATA_PRODUCTS.md:1)
- Roadmap (planning-only): [ROADMAP.md](../../Derivation/ROADMAP.md:1)
- Progress findings: [VDM-Progress-Findings.md](../../Derivation/VDM-Progress-Findings.md:1)
- Approvals CLI: [approve_tag.py](../../Derivation/code/common/authorization/approve_tag.py:1)
- IO helper (artifacts routing): [io_paths.py](../../Derivation/code/common/io_paths.py:1)

Scope & Policy:
- Read-only scan of repository paths; no writes to Derivation/.
- Outputs a JSON index by default at VDM_Nexus/reports/nexus-roadmap-index.v1.json (overwritable via CLI).
- Environment root resolution precedence: CLI flags > env > .env (same policy as other Nexus CLIs).
- Emits deterministic JSON (sorted keys) for reproducible diffs.

Usage:
  # Print to stdout
  python3 VDM_Nexus/scripts/nexus_roadmap_index.py --repo-root . --json

  # Write to the default reports path and also print a short summary
  python3 VDM_Nexus/scripts/nexus_roadmap_index.py --repo-root . --write

Notes:
- Maturity tier tagging should use structured sources only when/if added (e.g., JSON registries). Until then,
  this tool links to tier docs (TIER_STANDARDS.md) and progress summaries without inferring tier from Markdown.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_ENV_FILE = Path(".env")


def _read_env_file(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    try:
        if path.is_file():
            for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return env


def _resolve_repo_root(cli_repo_root: Optional[str]) -> Path:
    if cli_repo_root:
        return Path(cli_repo_root).resolve()
    return Path(".").resolve()


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_head(repo_root: Path) -> Optional[str]:
    try:
        import subprocess

        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo_root))
        return out.decode("utf-8", errors="ignore").strip()
    except Exception:
        return None


def _choose(dotenv: Dict[str, str], key: str, cli_val: Optional[str]) -> Tuple[Optional[str], str]:
    if cli_val is not None and cli_val != "":
        return cli_val, "cli"
    if key in os.environ and os.environ[key] != "":
        return os.environ[key], "env"
    if key in dotenv and dotenv[key] != "":
        return dotenv[key], ".env"
    return None, "unset"


@dataclass
class ApprovalsInfo:
    manifest_path: Optional[str]
    allowed_tags: List[str]
    approvals: Dict[str, Dict[str, Any]]
    schema_dir: Optional[str]

    @staticmethod
    def empty() -> "ApprovalsInfo":
        return ApprovalsInfo(manifest_path=None, allowed_tags=[], approvals={}, schema_dir=None)


@dataclass
class DomainCodeEntry:
    domain: str
    code_path: str
    approvals: ApprovalsInfo
    outputs: Dict[str, Any]


@dataclass
class DocBucketEntry:
    bucket: str
    proposals: List[str]
    results: List[str]


def _list_physics_domains(repo_root: Path) -> List[Path]:
    base = repo_root / "Derivation" / "code" / "physics"
    if not base.exists():
        return []
    return sorted([p for p in base.iterdir() if p.is_dir()])


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _collect_approvals_info(domain_dir: Path) -> ApprovalsInfo:
    # Primary convention uses APPROVAL.json for a domain
    manifest = domain_dir / "APPROVAL.json"
    if not manifest.exists():
        return ApprovalsInfo.empty()
    data = _read_json(manifest) or {}
    allowed = list(sorted((data.get("allowed_tags") or [])))
    approvals = data.get("approvals") or {}
    schema_dir = data.get("schema_dir")
    return ApprovalsInfo(
        manifest_path=str(manifest.relative_to(domain_dir.parents[3])) if manifest.exists() else None,
        allowed_tags=allowed,
        approvals=approvals,
        schema_dir=(str(Path(schema_dir)) if schema_dir else None),
    )


def _count_files_under(path: Path, exts: Optional[Tuple[str, ...]] = None) -> int:
    if not path.exists():
        return 0
    n = 0
    for p in path.rglob("*"):
        if not p.is_file():
            continue
        if exts is None:
            n += 1
        else:
            if p.suffix.lower() in exts:
                n += 1
    return n


def _collect_outputs(repo_root: Path, domain_name: str) -> Dict[str, Any]:
    base_logs = repo_root / "Derivation" / "code" / "outputs" / "logs" / domain_name
    base_figs = repo_root / "Derivation" / "code" / "outputs" / "figures" / domain_name
    out = {
        "logs_total": _count_files_under(base_logs, exts=(".json", ".csv")),
        "logs_failed_runs": _count_files_under(base_logs / "failed_runs", exts=(".json", ".csv")),
        "figures_total": _count_files_under(base_figs, exts=(".png", ".jpg", ".jpeg", ".webp", ".svg")),
    }
    # Include relative paths for UI navigation
    try:
        out["logs_path"] = str(base_logs.relative_to(repo_root))
    except Exception:
        out["logs_path"] = str(base_logs)
    try:
        out["figures_path"] = str(base_figs.relative_to(repo_root))
    except Exception:
        out["figures_path"] = str(base_figs)
    return out


_EXCLUDE_DOC_BUCKETS = {
    "References",
    "Speculations",
    "Draft-Papers",
    "Converging_External_Research",
    "Supporting_Work",
    "Templates",
    "References",  # duplicate guard
}


def _scan_doc_buckets(repo_root: Path) -> List[DocBucketEntry]:
    deriv = repo_root / "Derivation"
    if not deriv.exists():
        return []
    buckets: Dict[str, Tuple[List[str], List[str]]] = {}
    for child in sorted([p for p in deriv.iterdir() if p.is_dir()]):
        if child.name in _EXCLUDE_DOC_BUCKETS:
            continue
        # Gather proposals and results in this bucket
        props: List[str] = []
        ress: List[str] = []
        for p in child.rglob("PROPOSAL_*.md"):
            try:
                props.append(str(p.relative_to(repo_root)))
            except Exception:
                props.append(str(p))
        for p in child.rglob("RESULTS_*.md"):
            try:
                ress.append(str(p.relative_to(repo_root)))
            except Exception:
                ress.append(str(p))
        if props or ress:
            props_sorted = sorted(props)
            ress_sorted = sorted(ress)
            buckets[child.name] = (props_sorted, ress_sorted)
    entries: List[DocBucketEntry] = []
    for name in sorted(buckets.keys()):
        pr, rs = buckets[name]
        entries.append(DocBucketEntry(bucket=name, proposals=pr, results=rs))
    return entries


def _build_index(repo_root: Path) -> Dict[str, Any]:
    # Resolve physics code domains
    code_domains: List[DomainCodeEntry] = []
    for ddir in _list_physics_domains(repo_root):
        domain_name = ddir.name
        approvals = _collect_approvals_info(ddir)
        outputs = _collect_outputs(repo_root, domain_name)
        try:
            code_rel = str(ddir.relative_to(repo_root))
        except Exception:
            code_rel = str(ddir)
        code_domains.append(
            DomainCodeEntry(
                domain=domain_name,
                code_path=code_rel,
                approvals=approvals,
                outputs=outputs,
            )
        )

    # Resolve doc buckets (per top-level Derivation subfolder)
    doc_buckets = _scan_doc_buckets(repo_root)

    # Compose references (read-only anchors; UI should link and display banners/commits, not parse)
    references = {
        "tier_standards": "Derivation/TIER_STANDARDS.md",
        "canon_map": "Derivation/CANON_MAP.md",
        "data_products": "Derivation/DATA_PRODUCTS.md",
        "roadmap": "Derivation/ROADMAP.md",
        "progress_findings": "Derivation/VDM-Progress-Findings.md",
    }

    # Serialize
    out = {
        "set_id": "nexus-roadmap-index",
        "set_version": "1.0",
        "updated_utc": _iso_now(),
        "repo_head": _git_head(repo_root),
        "references": references,
        "code_domains": [
            {
                "domain": e.domain,
                "code_path": e.code_path,
                "approvals": {
                    "manifest_path": e.approvals.manifest_path,
                    "allowed_tags": e.approvals.allowed_tags,
                    "approvals": e.approvals.approvals,
                    "schema_dir": e.approvals.schema_dir,
                },
                "outputs": e.outputs,
            }
            for e in code_domains
        ],
        "doc_buckets": [asdict(b) for b in doc_buckets],
        # Placeholder for future structured tier registries (not derived from Markdown)
        "tier_registry": None,
        "notes": [
            "Do not infer tier (T0–T9) from Markdown; link to TIER_STANDARDS.md and progress summaries only.",
            "Approvals and outputs are enumerated from structured sources (JSON manifests, filesystem artifacts).",
            "Future: integrate approvals DB and structured registries when available to tag maturity in a first-class way.",
        ],
    }
    return out


def _default_report_path(repo_root: Path) -> Path:
    return repo_root / "VDM_Nexus" / "reports" / "nexus-roadmap-index.v1.json"


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(
        description="VDM Nexus — build a read-only roadmap index from canonical sources (no Derivation writes)"
    )
    ap.add_argument("--repo-root", help="Path to repo root (default: cwd)")
    ap.add_argument("--json", action="store_true", help="Emit index JSON to stdout")
    ap.add_argument("--write", action="store_true", help="Write index JSON to VDM_Nexus/reports (or --out)")
    ap.add_argument("--out", help="Optional explicit output path for --write")
    args = ap.parse_args(argv)

    repo_root = _resolve_repo_root(getattr(args, "repo_root", None))
    dotenv = _read_env_file(repo_root / DEFAULT_ENV_FILE)

    # Resolve environment precedence for consistency; not used heavily here but printed for audit.
    repo_root_val, repo_root_src = _choose(dotenv, "VDM_REPO_ROOT", getattr(args, "repo_root", None))
    resolved_env = {}
    if repo_root_val:
        resolved_env["VDM_REPO_ROOT"] = str(Path(repo_root_val).resolve())

    index = _build_index(repo_root)

    # Decide outputs
    wrote_path: Optional[Path] = None
    if args.write:
        out_path = Path(args.out) if args.out else _default_report_path(repo_root)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, sort_keys=True)
            f.write("\n")
        wrote_path = out_path

    if args.json:
        print(json.dumps(index, indent=2, sort_keys=True))

    # Print a short human summary if writing and not dumping JSON
    if args.write and not args.json:
        cd = index.get("code_domains", [])
        db = index.get("doc_buckets", [])
        print("[NEXUS][ROADMAP] Wrote roadmap index")
        print(f"  repo_root: {repo_root}")
        print(f"  VDM_REPO_ROOT: {resolved_env.get('VDM_REPO_ROOT','') or '(unset)'}  [src={repo_root_src}]")
        print(f"  code domains: {len(cd)}")
        print(f"  doc buckets:  {len(db)}")
        if wrote_path:
            try:
                print(f"  out: {wrote_path.relative_to(repo_root)}")
            except Exception:
                print(f"  out: {wrote_path}")

    # Exit code 0 on success; non-zero if neither write nor json selected (still allow 0 to ease piping)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))