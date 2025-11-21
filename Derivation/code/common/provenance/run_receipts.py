#!/usr/bin/env python3
"""Common helpers for VDM run receipts and provenance enforcement.

This module is intended to satisfy the Phase‑0 provenance checklist in
PRIVATE/VDM_VALIDATION_TODO.md by centralising:
  - Loading `PROVENANCE_manifest.json` and exposing `tree_hash` / git commit.
  - Computing salted provenance hashes from a commit and run tag/config.
  - Assembling per‑run JSON receipt fragments with determinism and hardware info.

Runners can import `build_run_receipts` and merge the returned dict into their
summary JSON so that every validation‑phase run exposes the same fields:
`git_commit`, `tree_hash`, salted provenance hash, IEEE‑754 flag, seeds,
hardware, and all gate outcomes.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

_MANIFEST_CACHE: Dict[Path, Dict[str, Any]] = {}
_REPO_ROOT_CACHE: Optional[Path] = None


def _find_repo_root(start: Optional[Path] = None) -> Path:
    """Locate the repository root (directory that owns PROVENANCE_manifest.json).

    We walk parents from *start* upward until we find PROVENANCE_manifest.json,
    falling back to the 4th parent of this file (…/Prometheus_VDM) if no
    manifest is present.
    """
    global _REPO_ROOT_CACHE
    if _REPO_ROOT_CACHE is not None:
        return _REPO_ROOT_CACHE

    here = (start or Path(__file__)).resolve()
    for p in [here] + list(here.parents):
        candidate = p / "PROVENANCE_manifest.json"
        if candidate.exists():
            _REPO_ROOT_CACHE = p
            return p
    # Fallback: assume we are in Derivation/code/common/provenance/
    # parents[4] ≈ repo root for the standard layout.
    try:
        root = here.parents[4]
    except IndexError:
        root = here.anchor  # type: ignore[assignment]
    _REPO_ROOT_CACHE = Path(root)
    return _REPO_ROOT_CACHE


def load_manifest(repo_root: Optional[Path] = None) -> Tuple[Path, Dict[str, Any]]:
    """Load PROVENANCE_manifest.json from *repo_root* (or discover it).

    Returns (root_path, manifest_dict). If the manifest cannot be found or
    parsed, the dict will be empty but the function will not raise.
    """
    root = _find_repo_root(repo_root)
    manifest_path = root / "PROVENANCE_manifest.json"
    if manifest_path in _MANIFEST_CACHE:
        return root, _MANIFEST_CACHE[manifest_path]

    data: Dict[str, Any] = {}
    try:
        text = manifest_path.read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception:
        data = {}
    _MANIFEST_CACHE[manifest_path] = data
    return root, data


def _git_head_commit(repo_root: Path) -> Tuple[str, str]:
    """Best‑effort HEAD commit (full, short) without invoking git binaries.

    Falls back to "UNKNOWN" if .git cannot be parsed.
    """
    git_dir = repo_root / ".git"
    head = git_dir / "HEAD"
    try:
        txt = head.read_text(encoding="utf-8").strip()
        if txt.startswith("ref:"):
            ref_rel = txt.split(" ", 1)[1].strip()
            ref_path = git_dir / ref_rel
            commit_full = ref_path.read_text(encoding="utf-8").strip()
        else:
            commit_full = txt
    except Exception:
        commit_full = "UNKNOWN"
    commit_short = commit_full[:7] if commit_full and commit_full != "UNKNOWN" else "UNKNOWN"
    return commit_full, commit_short


def _compute_salted_hash(commit_full: str, salted_tag: str) -> Optional[str]:
    """Compute salted provenance hash sha256(f"{commit}|{salted_tag}")."""
    if not commit_full or commit_full == "UNKNOWN":
        return None
    try:
        h = hashlib.sha256()
        h.update(f"{commit_full}|{salted_tag}".encode("utf-8"))
        return h.hexdigest()
    except Exception:
        return None


def _ieee754_double_precision() -> bool:
    """Detect whether Python floats are IEEE‑754 double precision.

    This checks mantissa bits and radix from sys.float_info. On CPython this
    should be True on all supported platforms.
    """
    info = sys.float_info
    return (info.radix == 2 and info.mant_dig == 53)


def _hardware_receipts() -> Dict[str, Any]:
    """Minimal hardware/environment description for reproducibility."""
    rec: Dict[str, Any] = {}
    try:
        uname = platform.uname()
        rec.update(
            {
                "system": uname.system,
                "node": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
                "processor": uname.processor,
            }
        )
    except Exception:
        rec.setdefault("system", "unknown")
    try:
        rec["cpu_count"] = os.cpu_count()
    except Exception:
        pass
    rec.setdefault("python_version", platform.python_version())
    return rec


@dataclass
class RunReceipts:
    """Container for common run‑level provenance receipts.

    The .as_dict() method returns a JSON‑serialisable mapping that can be
    merged into a runner's summary log.
    """
    repo_root: Path
    git_commit_full: str
    git_commit: str
    manifest_commit: Optional[str]
    manifest_tree_hash: Optional[str]
    manifest_generated_utc: Optional[str]
    salted_tag: str
    salted_hash: Optional[str]
    ieee754_double: bool
    seeds: Sequence[int]
    hardware: Dict[str, Any]
    gate_outcomes: Dict[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        """Return a JSON‑ready dict with both nested and alias fields.

        Top‑level aliases (git_commit, tree_hash, salted_hash, ieee_754_double_precision,
        seeds, hardware, gate_outcomes) are included to make schema bindings simple.
        """
        return {
            "repo_root": str(self.repo_root),
            "manifest": {
                "git_commit": self.manifest_commit,
                "tree_hash": self.manifest_tree_hash,
                "generated_utc": self.manifest_generated_utc,
            },
            "git": {
                "head_commit": self.git_commit_full,
                "head_short": self.git_commit,
            },
            "salted_provenance": {
                "salted_tag": self.salted_tag,
                "salted_hash": self.salted_hash,
            },
            # Aliases required by the Phase‑0 checklist
            "git_commit": self.git_commit,
            "tree_hash": self.manifest_tree_hash,
            "salted_hash": self.salted_hash,
            "ieee_754_double_precision": bool(self.ieee754_double),
            "seeds": list(self.seeds),
            "hardware": dict(self.hardware),
            "gate_outcomes": dict(self.gate_outcomes),
        }


def build_run_receipts(*,
                      tag: str,
                      seeds: Optional[Sequence[int]] = None,
                      gate_outcomes: Optional[Mapping[str, Any]] = None,
                      repo_root: Optional[Path] = None,
                      salted_tag_env_var: str = "VDM_SALTED_TAG",
                      ) -> Dict[str, Any]:
    """Construct a canonical run‑receipts dict for JSON logs.

    Parameters
    ----------
    tag:
        Logical run tag (e.g. prereg or experiment tag).
    seeds:
        Sequence of integer seeds used in the run (may be empty).
    gate_outcomes:
        Mapping from gate name to verdict / diagnostic payload.
    repo_root:
        Optional explicit repository root. If omitted, it is auto‑discovered.
    salted_tag_env_var:
        Name of environment variable that can override the salted tag
        (defaults to "VDM_SALTED_TAG").
    """
    root, manifest = load_manifest(repo_root)
    manifest_commit = manifest.get("git_commit") if isinstance(manifest, dict) else None
    manifest_tree_hash = manifest.get("tree_hash") if isinstance(manifest, dict) else None
    manifest_generated_utc = manifest.get("generated_utc") if isinstance(manifest, dict) else None

    git_full, git_short = _git_head_commit(root)

    env_tag = os.getenv(salted_tag_env_var)
    salted_tag = env_tag if env_tag is not None and env_tag.strip() else tag
    salted_hash = _compute_salted_hash(git_full, salted_tag)

    ieee = _ieee754_double_precision()
    hw = _hardware_receipts()

    if seeds is None:
        seed_list: Sequence[int] = []
    else:
        seed_list = [int(s) for s in seeds]

    gates: Dict[str, Any] = dict(gate_outcomes or {})

    rr = RunReceipts(
        repo_root=root,
        git_commit_full=git_full,
        git_commit=git_short,
        manifest_commit=manifest_commit,
        manifest_tree_hash=manifest_tree_hash,
        manifest_generated_utc=manifest_generated_utc,
        salted_tag=salted_tag,
        salted_hash=salted_hash,
        ieee754_double=ieee,
        seeds=seed_list,
        hardware=hw,
        gate_outcomes=gates,
    )
    return rr.as_dict()


__all__ = ["load_manifest", "build_run_receipts", "RunReceipts"]