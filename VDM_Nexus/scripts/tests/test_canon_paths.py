"""Unit tests for the canon path resolver scaffolding."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


MODULE_PATH = Path("VDM_Nexus/scripts/canon_paths.py").resolve()
REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("nexus_canon_paths", str(MODULE_PATH))
    assert spec and spec.loader, "Failed to create module spec for canon_paths"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


@pytest.fixture(scope="module")
def canon_paths_module() -> ModuleType:
    return _load_module()


@pytest.fixture(scope="module")
def resolver(canon_paths_module: ModuleType):
    return canon_paths_module.CanonResolver.from_sources(str(REPO_ROOT))


def test_repo_root_resolution(resolver, canon_paths_module: ModuleType):
    assert resolver.repo_root == REPO_ROOT
    assert resolver.derivation_root == REPO_ROOT / "Derivation"
    head = resolver.git_head()
    if head is not None:
        assert len(head) == 40


def test_resolve_known_anchor(resolver):
    path, fragment = resolver.resolve("Derivation/AXIOMS.md#vdm-ax-a0")
    assert path == REPO_ROOT / "Derivation" / "AXIOMS.md"
    assert fragment == "vdm-ax-a0"


def test_resolve_rejects_empty(resolver, canon_paths_module: ModuleType):
    with pytest.raises(canon_paths_module.CanonPathError):
        resolver.resolve("   ")


def test_resolve_prevents_escape(resolver, canon_paths_module: ModuleType):
    with pytest.raises(canon_paths_module.CanonPathError):
        resolver.resolve("Derivation/../README.md")


def test_metadata_for_existing_file(resolver):
    path, _ = resolver.resolve("Derivation/AXIOMS.md")
    metadata = resolver.metadata(path)
    assert metadata.exists is True
    assert metadata.size_bytes and metadata.size_bytes > 0
    assert metadata.sha256 and len(metadata.sha256) == 64
    if metadata.last_commit is not None:
        assert len(metadata.last_commit) == 40


def test_metadata_for_missing_file(resolver):
    missing = resolver.repo_root / "Derivation" / "__does_not_exist__.md"
    metadata = resolver.metadata(missing)
    assert metadata.exists is False
    assert metadata.sha256 is None
    assert metadata.size_bytes is None
    assert metadata.last_commit is None
