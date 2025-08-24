from __future__ import annotations

"""
File Picker Controller Utilities

Purpose:
- Provide bounded, reusable filesystem helpers for the Dash file-picker
- Centralize path clamping, directory listing, and initial tree construction
- Ensure safety (no traversal beyond root), performance (scandir), and filtering (exts, dotfiles)

Design constraints:
- Sparse-first: single-directory listings only (no recursion)
- No schedulers
- No scans in core/ or maps/ (caller controls roots; we only walk the provided path)
- Contracts: Pure functions with deterministic outputs for given inputs
"""

import os
from typing import List, Tuple, Dict, Any


def clamp_to_root(path: str, root: str) -> str:
    """
    Clamp an arbitrary path to the provided root. If 'path' escapes 'root', return the root.

    Args:
        path: Any filesystem path (relative or absolute)
        root: Root boundary (absolute or relative, coerced to absolute internally)

    Returns:
        Absolute path inside 'root' (or the root itself when 'path' escapes)
    """
    try:
        root_abs = os.path.abspath(root)
        path_abs = os.path.abspath(path)
        common = os.path.commonpath([root_abs, path_abs])
        return path_abs if common == root_abs else root_abs
    except Exception:
        return os.path.abspath(root)


def is_within_root(path: str, root: str) -> bool:
    """
    Check if 'path' is within 'root' boundary.

    Returns:
        True if path is inside root, False otherwise (including exceptions).
    """
    try:
        root_abs = os.path.abspath(root)
        path_abs = os.path.abspath(path)
        return os.path.commonpath([root_abs, path_abs]) == root_abs
    except Exception:
        return False


def list_dir(path: str, exts: List[str] | None = None, hide_dotfiles: bool = True) -> Tuple[List[str], List[str]]:
    """
    List a single directory (bounded IO).

    Args:
        path: Directory to list (absolute or relative)
        exts: Optional list of allowed file extensions (e.g., [".json", ".csv"]); when None or empty, allow all
        hide_dotfiles: When True, hide entries whose name starts with '.'

    Returns:
        (subdirs, files) — both sorted, names only (no absolute paths)

    Policy:
        - No scans in 'core/' or 'maps/' at any depth. If the resolved path contains either
          restricted segment, short-circuit and return empty results. This enforces the global
          guard while keeping IO strictly bounded.
    """
    subdirs: List[str] = []
    files: List[str] = []
    try:
        pabs = os.path.abspath(path)
        # Enforce "no scans in core/ or maps/" at any depth
        parts = os.path.normpath(pabs).split(os.sep)
        if "core" in parts or "maps" in parts:
            return [], []

        lower_exts = [e.lower() for e in (exts or [])]
        allow_all = not lower_exts
        with os.scandir(pabs) as it:
            for entry in it:
                name = entry.name
                if hide_dotfiles and name.startswith("."):
                    continue
                try:
                    if entry.is_dir(follow_symlinks=False):
                        # Don't even offer restricted dirs for expansion
                        if name not in ("core", "maps"):
                            subdirs.append(name)
                    else:
                        if allow_all or any(name.lower().endswith(e) for e in lower_exts):
                            files.append(name)
                except Exception:
                    # Skip entries that cause IO/stat errors
                    continue
    except Exception:
        return [], []
    subdirs.sort()
    files.sort()
    return subdirs, files


def init_tree(root: str, exts: List[str] | None = None, hide_dotfiles: bool = True) -> Dict[str, Any]:
    """
    Construct the initial tree structure for a file-picker rooted at 'root'.

    Structure:
        {
          "root": <abs_root>,
          "nodes": {
             <abs_root>: {
                "expanded": True,
                "subdirs": [<names>],
                "files": [<names>]
             }
          }
        }

    Notes:
      - Bounded IO: lists only the root directory once for initialization
      - No recursion; deeper nodes are discovered on user toggle via list_dir()
    """
    rabs = os.path.abspath(root)
    subdirs, files = list_dir(rabs, exts=exts, hide_dotfiles=hide_dotfiles)
    return {
        "root": rabs,
        "nodes": {
            rabs: {
                "expanded": True,
                "subdirs": subdirs or [],
                "files": files or [],
            }
        },
    }


def next_children(path: str, exts: List[str] | None = None, hide_dotfiles: bool = True) -> Tuple[List[str], List[str]]:
    """
    One-step discovery for a directory node. Intended for use when the user expands a folder.
    """
    pabs = os.path.abspath(path)
    return list_dir(pabs, exts=exts, hide_dotfiles=hide_dotfiles)