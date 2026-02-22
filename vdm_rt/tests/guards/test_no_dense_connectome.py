import importlib
import pytest


def test_connectome_module_removed():
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("vdm_rt.core.connectome")


def test_sparse_connectome_exports_connectome():
    mod = importlib.import_module("vdm_rt.core.sparse_connectome")
    assert hasattr(mod, "Connectome")
