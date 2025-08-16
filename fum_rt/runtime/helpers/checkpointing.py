"""
Runtime helper: checkpointing and retention.

Provides:
- save_tick_checkpoint(): periodic snapshot with retention, behavior-preserving.
"""

from __future__ import annotations

from typing import Any

from fum_rt.core.memory import save_checkpoint
from fum_rt.runtime.retention import prune_checkpoints as _prune_ckpt


def save_tick_checkpoint(nx: Any, step: int) -> None:
    """
    Save checkpoint and run retention policy when configured. Mirrors original behavior.
    """
    try:
        if getattr(nx, "checkpoint_every", 0) and (int(step) % int(nx.checkpoint_every)) == 0 and int(step) > 0:
            try:
                path = save_checkpoint(
                    nx.run_dir,
                    int(step),
                    nx.connectome,
                    fmt=getattr(nx, "checkpoint_format", "h5") or "h5",
                    adc=getattr(nx, "adc", None),
                )
                try:
                    nx.logger.info("checkpoint_saved", extra={"extra": {"path": str(path), "step": int(step)}})
                except Exception:
                    pass
                if int(getattr(nx, "checkpoint_keep", 0)) > 0:
                    try:
                        summary = _prune_ckpt(nx.run_dir, keep=int(nx.checkpoint_keep), last_path=path)
                        try:
                            nx.logger.info("checkpoint_retention", extra={"extra": summary})
                        except Exception:
                            pass
                    except Exception:
                        pass
            except Exception as e:
                try:
                    nx.logger.info("checkpoint_error", extra={"extra": {"err": str(e)}})
                except Exception:
                    pass
    except Exception:
        pass


__all__ = ["save_tick_checkpoint"]