from __future__ import annotations

"""
File Picker Status/Formatting Controller (atomic helpers)

Purpose:
- Pure helpers used by Dash callbacks and widgets to compute status strings and sizes
- Keep IO bounded and consistent with global guards via controller.list_dir()

Contracts:
- No recursion. Single-directory listings only.
- No scans in core/ or maps/ are enforced by file_picker_controller.list_dir
- Deterministic outputs; exceptions are contained and produce safe fallbacks.
"""

import os
from typing import List

from fum_rt.frontend.controllers.file_picker_controller import (
    list_dir as _ctl_list_dir,
)


def human_size(n: int | float) -> str:
    """
    Convert a byte count to a human-readable string.
    """
    try:
        n = int(n)
    except Exception:
        return "0 B"
    units = [("TB", 1024**4), ("GB", 1024**3), ("MB", 1024**2), ("KB", 1024), ("B", 1)]
    for label, factor in units:
        if n >= factor:
            if factor == 1:
                return f"{n} B"
            return f"{n / factor:.2f} {label}"
    return "0 B"


def sum_filesizes(dir_path: str, filenames: List[str] | None) -> int:
    """
    Sum sizes of the given filenames inside dir_path (non-recursive).
    """
    total = 0
    for name in (filenames or []):
        try:
            fp = os.path.join(dir_path, name)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
        except Exception:
            continue
    return total


def file_status_text(file_path: str) -> str:
    """
    Build status text for a single file path.
    """
    base = os.path.basename(file_path or "")
    try:
        size_b = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
        return f"File: {base} - Size: {human_size(size_b)}"
    except Exception:
        return f"File: {base} - Size: unknown"


def directory_status_text(dir_path: str, exts: List[str] | None = None, hide_dotfiles: bool = True) -> str:
    """
    Build status text for a directory: counts and aggregate size of visible files.

    IO is strictly bounded to a single directory via controller.list_dir.
    """
    try:
        if not (dir_path and os.path.isdir(dir_path)):
            return "Contains: 0 folders; 0 files; Total Size: 0 B"
        subdirs, files = _ctl_list_dir(dir_path, exts=exts or [], hide_dotfiles=hide_dotfiles)
        folders_n = len(subdirs or [])
        files_n = len(files or [])
        total_b = sum_filesizes(dir_path, files or [])
        return f"Contains: {folders_n} folders; {files_n} files; Total Size: {human_size(total_b)}"
    except Exception:
        return "Contains: 0 folders; 0 files; Total Size: 0 B"