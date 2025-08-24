from __future__ import annotations

import os
import re
from glob import glob

# CI guard: scouts must remain void-faithful (no scans, no dense ops)
# Scope: core/cortex/void_walkers/*.py

HERE = os.path.abspath(os.path.dirname(__file__))
REPO_CORE = os.path.abspath(os.path.join(HERE, "..", "..", "core"))
WALKERS_DIR = os.path.join(REPO_CORE, "cortex", "void_walkers")


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_void_walkers_exist():
    assert os.path.isdir(WALKERS_DIR), f"Missing walkers dir: {WALKERS_DIR}"
    py_files = sorted(glob(os.path.join(WALKERS_DIR, "*.py")))
    assert py_files, "No walker .py files found under core/cortex/void_walkers"


def test_walkers_no_scans_or_dense_calls():
    # Disallow global scans and dense conversions in walkers
    banned = re.compile(
        r"(synaptic_weights|eligibility_traces|\.adj\b|toarray|tocsr|csr|coo|networkx)",
        re.IGNORECASE,
    )
    py_files = sorted(glob(os.path.join(WALKERS_DIR, "*.py")))
    assert py_files, "No walker .py files found to check"

    # Allowlist minimal: base and the specific walkers are still subject to the same guard
    for p in py_files:
        src = _read(p)
        assert not banned.search(src), f"Walker contains forbidden identifier(s): {p}"


def test_walkers_readonly_contract_mentions():
    # Ensure docstrings emphasize read-only/event-driven (lightweight heuristic)
    py_files = sorted(glob(os.path.join(WALKERS_DIR, "*.py")))
    key_terms = ("read-only", "void-faithful")
    found = 0
    for p in py_files:
        head = _read(p)[:512].lower()
        if all(k in head for k in key_terms):
            found += 1
    # Require at least two walkers to include contract language (base + ≥1 walker)
    assert found >= 2, "Expected read-only/void-faithful contract emphasized in walker docstrings"