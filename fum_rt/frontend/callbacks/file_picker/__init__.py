from __future__ import annotations

"""
File Picker callbacks package.

Exports:
- register_file_picker_static
- register_file_picker_engram

Implementation files:
- common.py      (shared callback logic: navigation, tree rendering, status, confirm)
- registrars.py  (thin wrappers: static and dynamic/engram root selection)
"""

from .registrars import (
    register_file_picker_static,
    register_file_picker_engram,
)

__all__ = ["register_file_picker_static", "register_file_picker_engram"]