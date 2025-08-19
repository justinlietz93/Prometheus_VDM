from __future__ import annotations

"""
Legacy shim for File Picker registrars.

Delegates to fum_rt.frontend.callbacks.file_picker_registrars to maintain import compatibility.
"""

from fum_rt.frontend.callbacks.file_picker_registrars import (
    register_file_picker_static,
    register_file_picker_engram,
)

__all__ = ["register_file_picker_static", "register_file_picker_engram"]