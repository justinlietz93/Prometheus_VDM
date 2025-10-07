"""Pytest configuration shim to normalize imports.

- Ensures the repository root is present on sys.path so imports like
  `Prometheus_VDM.*` and `fum_rt.*` resolve reliably during test collection.
"""
import os
import sys

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Historical import aliases: map Prometheus_VDM.derivation.* -> Derivation.*
import types as _types
import importlib as _importlib


def _alias_module(src: str, dst: str) -> None:
  """Alias module name 'src' to real module 'dst' for import compatibility.

  Creates parent chain and sets attributes so deep imports continue to work.
  """
  real = _importlib.import_module(dst)
  parts = src.split('.')

  # Ensure top-level package exists as a package module
  top = parts[0]
  if top not in sys.modules:
    top_mod = _types.ModuleType(top)
    top_mod.__path__ = []  # mark as pkg
    sys.modules[top] = top_mod
  parent_mod = sys.modules[top]

  # Walk/build chain and attach real module at the leaf
  accum = top
  for i in range(1, len(parts)):
    subname = parts[i]
    accum = f"{accum}.{subname}"
    is_leaf = (i == len(parts) - 1)
    child = sys.modules.get(accum)
    if child is None:
      child = real if is_leaf else _types.ModuleType(accum)
      if not is_leaf:
        child.__path__ = []  # treat as pkg
      sys.modules[accum] = child
    setattr(parent_mod, subname, child)
    parent_mod = child

  # Also register the src alias directly
  sys.modules[src] = real


# Best-effort aliasing; skip silently if the target package is missing at runtime
for _src, _dst in (
  ('Prometheus_VDM.derivation', 'Derivation'),
  ('Prometheus_VDM.derivation.code', 'Derivation.code'),
  ('Prometheus_VDM.derivation.code.physics', 'Derivation.code.physics'),
  ('Prometheus_VDM.derivation.code.physics.reaction_diffusion', 'Derivation.code.physics.reaction_diffusion'),
  ('Prometheus_VDM.derivation.code.physics.fluid_dynamics', 'Derivation.code.physics.fluid_dynamics'),
):
  try:
    _alias_module(_src, _dst)
  except ModuleNotFoundError:
    continue
