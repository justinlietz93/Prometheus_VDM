import importlib
import os
import sys
import types
import pytest


def test_import_guard_blocks_dense_by_default(monkeypatch):
    # Ensure FORCE_DENSE is not set
    monkeypatch.delenv("FORCE_DENSE", raising=False)
    # Importing dense connectome module should raise due to top-level guard
    with pytest.raises(RuntimeError):
        importlib.invalidate_caches()
        if "fum_rt.core.connectome" in sys.modules:
            del sys.modules["fum_rt.core.connectome"]
        importlib.import_module("fum_rt.core.connectome")


def test_dense_branch_raises_when_forced_but_no_dense_policy(monkeypatch):
    # Allow import of dense module, but enforce NO_DENSE_CONNECTOME policy at runtime
    monkeypatch.setenv("FORCE_DENSE", "1")
    monkeypatch.setenv("NO_DENSE_CONNECTOME", "1")
    monkeypatch.delenv("ALLOW_DENSE_VALIDATION", raising=False)

    import importlib
    import numpy as np

    importlib.invalidate_caches()
    if "fum_rt.core.connectome" in sys.modules:
        del sys.modules["fum_rt.core.connectome"]
    mod = importlib.import_module("fum_rt.core.connectome")
    # Construct Connectome in dense structural mode with small N
    C = mod.Connectome(N=64, k=8, structural_mode="dense")
    # Step call should raise under NO_DENSE_CONNECTOME policy
    with pytest.raises(RuntimeError):
        C.step(t=0.0, domain_modulation=1.0, sie_drive=1.0, use_time_dynamics=True)
