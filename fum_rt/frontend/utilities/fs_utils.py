"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import os
import json
from typing import Any, List


def list_runs(root: str) -> List[str]:
    """
    List run directories under root, sorted by mtime desc.
    Mirrors logic from the legacy dashboard for identical behavior.
    """
    if not os.path.exists(root):
        return []
    items = []
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            try:
                mt = os.path.getmtime(path)
            except Exception:
                mt = 0.0
            items.append((mt, path))
    items.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in items]


def read_json_file(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def write_json_file(path: str, data: Any) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        return True
    except Exception:
        return False


def _list_files(path: str, exts: List[str] | None, recursive: bool = False) -> List[str]:
    """
    List files under a path, optionally filtered by extensions and recursively.
    Excludes common compressed archive extensions to mirror prior UI behavior.
    Returns relative paths when recursive=True, otherwise basenames.
    """
    if not os.path.isdir(path):
        return []

    found: List[str] = []
    compressed_exts = {".zip", ".gz", ".bz2", ".xz", ".rar", ".7z"}
    try:
        if not recursive:
            return [
                f
                for f in os.listdir(path)
                if (exts is None or any(f.lower().endswith(e) for e in exts))
                and not any(f.lower().endswith(c) for c in compressed_exts)
            ]

        for root, _, files in os.walk(path):
            for f in files:
                if (exts is None or any(f.lower().endswith(e) for e in exts)) and not any(
                    f.lower().endswith(c) for c in compressed_exts
                ):
                    # store relative path from the initial scan path
                    rel_path = os.path.relpath(os.path.join(root, f), path)
                    found.append(rel_path)
        return found
    except Exception:
        return []


def latest_checkpoint(run_dir: str) -> str | None:
    """
    Return the absolute path to the latest checkpoint (.h5 or .npz) in a run directory,
    determined by numeric step parsed from filenames like state_000123.h5/npz.
    """
    try:
        files = []
        for fn in os.listdir(run_dir):
            if fn.startswith("state_") and (fn.endswith(".h5") or fn.endswith(".npz")):
                ext = ".h5" if fn.endswith(".h5") else ".npz"
                step_str = fn[6:-len(ext)]
                try:
                    s = int(step_str)
                    files.append((s, os.path.join(run_dir, fn)))
                except Exception:
                    pass
        if files:
            files.sort(key=lambda x: x[0], reverse=True)
            return files[0][1]
    except Exception:
        return None
    return None