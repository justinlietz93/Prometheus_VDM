"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
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