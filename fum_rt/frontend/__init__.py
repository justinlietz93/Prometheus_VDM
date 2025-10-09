"""
FUM Runtime Frontend (modularized)

Modules:
- fs_utils: filesystem helpers (runs listing, JSON IO) - re-exported from utilities.fs_utils
- tail: tailing JSONL with byte offsets - re-exported from utilities.tail
- series: streaming metrics buffers and helpers - re-exported from models.series
- process_manager: launch/stop runtime process from the UI - re-exported from services.process_manager
- app: Dash app entrypoint (build_app, main)
"""

# Re-export modules at package root for stable imports: fum_rt.frontend.fs_utils, etc.
from .utilities import fs_utils as fs_utils
from .utilities import tail as tail
from .models import series as series
from .services import process_manager as process_manager

__all__ = ["fs_utils", "tail", "series", "process_manager"]