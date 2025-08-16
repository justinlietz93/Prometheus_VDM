from __future__ import annotations

"""
Package shim for the runtime loop.

Exports run_loop from the submodule [main.py](fum_rt/runtime/loop/main.py:1) so that
callers can continue to use `from fum_rt.runtime.loop import run_loop` without caring
about file layout.

This arrangement removes ambiguity when both a subpackage `runtime/loop/` and a legacy
sibling module `runtime/loop.py` exist on disk.
"""

from .main import run_loop

__all__ = ["run_loop"]
