"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Boundary and policy guard tests.

Scope:
- Enforce core/ isolation: no imports from fum_rt.io, fum_rt.runtime, or fum_rt.nexus
- Enforce runtime/ is NumPy-free: runtime contains no 'import numpy' or 'from numpy ...'
- Enforce IDF/lexicon coupling remains outside core/: core must not import IO IDF or reference compute_idf_scale

These tests are inexpensive and run as plain file-content checks (no heavy imports).
"""

import re
from pathlib import Path

# ---------- helpers ----------


def _project_root(start: Path | None = None) -> Path:
    """
    Locate repository root by searching upward for a directory that contains 'fum_rt'.
    """
    cur = (start or Path(__file__)).resolve().parent
    for _ in range(10):
        if (cur / "fum_rt").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # Fallback to current file's grandparent
    return (start or Path(__file__)).resolve().parents[2]


def _iter_py_files(dir_path: Path):
    for p in dir_path.rglob("*.py"):
        # Skip compiled or hidden
        if p.name.startswith("."):
            continue
        yield p


def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


# ---------- tests ----------


def test_core_does_not_import_runtime_or_io():
    """
    core/* must not import fum_rt.io.*, fum_rt.runtime.*, or fum_rt.nexus.*
    """
    root = _project_root()
    core_dir = root / "fum_rt" / "core"

    forbidden_re = re.compile(
        r"^\s*(from|import)\s+fum_rt\.(io|runtime|nexus)\b",
        re.MULTILINE,
    )

    offenders: list[Path] = []
    for py in _iter_py_files(core_dir):
        txt = _read_text(py)
        if forbidden_re.search(txt):
            offenders.append(py)

    assert not offenders, f"Forbidden imports in core/: {', '.join(str(p) for p in offenders)}"


def test_core_does_not_import_idf_or_lexicon_io():
    """
    core/* must not import IDF or lexicon IO implementations.
    """
    root = _project_root()
    core_dir = root / "fum_rt" / "core"

    # Match explicit IDF import lines and calls to compute_idf_scale
    idf_import_re = re.compile(
        r"^\s*(from\s+fum_rt\.io\.lexicon\.idf\s+import\b|import\s+fum_rt\.io\.lexicon\.idf\b)",
        re.MULTILINE,
    )
    idf_call_re = re.compile(r"\bcompute_idf_scale\b")

    offenders: list[str] = []
    for py in _iter_py_files(core_dir):
        txt = _read_text(py)
        if idf_import_re.search(txt):
            offenders.append(f"{py}: idf_import")
        if idf_call_re.search(txt):
            offenders.append(f"{py}: compute_idf_scale_ref")

    assert not offenders, "IDF references found in core/: " + ", ".join(offenders)


def test_runtime_is_numpy_free():
    """
    runtime/* must not import numpy directly; all numeric kernels live in core/*.
    """
    root = _project_root()
    rt_dir = root / "fum_rt" / "runtime"

    numpy_re = re.compile(
        r"^\s*(from\s+numpy\s+import|import\s+numpy(\s+as\s+np)?\b|from\s+numpy\b)",
        re.MULTILINE,
    )

    offenders: list[Path] = []
    for py in _iter_py_files(rt_dir):
        txt = _read_text(py)
        if numpy_re.search(txt):
            offenders.append(py)

    assert not offenders, f"runtime/ uses numpy: {', '.join(str(p) for p in offenders)}"


def test_core_files_exist_expected_brain_modules():
    """
    Sanity: ensure key core modules exist to host internals.
    """
    root = _project_root()
    core_dir = root / "fum_rt" / "core"
    expected = [
        "connectome.py",
        "sparse_connectome.py",
        "adc.py",
        "metrics.py",
        "signals.py",
        "proprioception/events.py",
        "fum_sie.py",
        "sie_v2.py",
    ]
    missing = []
    for rel in expected:
        if not (core_dir / rel).exists():
            missing.append(rel)
    assert not missing, f"Missing core internals modules: {missing}"


def test_runtime_loop_refs_core_and_seams_only():
    """
    Ensure runtime loop/stepper reference core seams for numeric logic.
    """
    root = _project_root()
    loop_py = (root / "fum_rt" / "runtime" / "loop.py")
    loop_pkg_init = (root / "fum_rt" / "runtime" / "loop" / "__init__.py")
    stepper_py = (root / "fum_rt" / "runtime" / "stepper.py")

    # Check loop module exists either as a single file or as a package
    assert loop_py.exists() or loop_pkg_init.exists(), "runtime/loop module not found (file or package)"
    assert stepper_py.exists(), "runtime/stepper.py not found"

    loop_src = loop_py if loop_py.exists() else loop_pkg_init
    loop_txt = _read_text(loop_src)
    step_txt = _read_text(stepper_py)

    # loop should import telemetry.tick_fold and core.signals.apply_b1_detector via runtime seams
    assert "runtime.telemetry" in loop_txt and "tick_fold" in loop_txt, "loop missing telemetry.tick_fold seam"
    assert "core.signals" in loop_txt, "loop missing core.signals seam usage"

    # stepper should import core.signals helpers and compute_metrics from core
    assert "core.signals" in step_txt and "compute_metrics" in step_txt, "stepper.py should use core signals/metrics"


if __name__ == "__main__":
    # Allow running as a script for local quick checks
    import sys

    root = _project_root()
    tests = [
        test_core_does_not_import_runtime_or_io,
        test_core_does_not_import_idf_or_lexicon_io,
        test_runtime_is_numpy_free,
        test_core_files_exist_expected_brain_modules,
        test_runtime_loop_refs_core_and_seams_only,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"[OK] {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {t.__name__}: {e}", file=sys.stderr)
    sys.exit(1 if failed else 0)