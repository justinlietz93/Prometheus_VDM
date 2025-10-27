"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import sys, json, os
from fum_rt.io.logging.rolling_jsonl import RollingJsonlWriter
try:
    # Prefer zip spooler when available
    from fum_rt.io.logging.rolling_jsonl import RollingZipJsonlWriter  # type: ignore
except Exception:
    RollingZipJsonlWriter = None  # type: ignore

class UTD:
    """Universal Transduction Decoder.
    Emits opportunistic outputs (stdout + file sink) and supports a simple macro board.

    API
    - emit_text(payload: dict, score: float=1.0)
    - register_macro(name: str, meta: dict | None=None) -> bool
    - list_macros() -> list[str]
    - emit_macro(name: str, args: dict | None=None, score: float=1.0)
    """
    def __init__(self, run_dir: str):
        self.run_dir = run_dir
        os.makedirs(self.run_dir, exist_ok=True)
        self.path = os.path.join(self.run_dir, 'utd_events.jsonl')
        # Prefer zip-spooled writer to bound disk pressure; fallback to rolling JSONL
        use_zip = True
        try:
            # Allow explicit opt-out via env
            use_zip = str(os.getenv("FUM_ZIP_SPOOL", "1")).strip().lower() in ("1", "true", "yes", "on", "y")
        except Exception:
            use_zip = True
        try:
            if use_zip and RollingZipJsonlWriter is not None:  # type: ignore
                self._writer = RollingZipJsonlWriter(self.path)  # type: ignore
            else:
                self._writer = RollingJsonlWriter(self.path)
        except Exception:
            # Safe fallback
            self._writer = RollingJsonlWriter(self.path)
        # Macro registry and on-disk macro board for persistence
        self._macro_registry = {}
        self._macro_board_path = os.path.join(self.run_dir, 'macro_board.json')
        # Eager-load persisted macro board if present
        try:
            if os.path.exists(self._macro_board_path):
                with open(self._macro_board_path, 'r', encoding='utf-8') as fh:
                    reg = json.load(fh)
                    if isinstance(reg, dict):
                        for name, meta in reg.items():
                            self._macro_registry[str(name)] = meta if isinstance(meta, dict) else {}
        except Exception:
            # do not fail runtime if file is corrupt
            pass

    def register_macro(self, name: str, meta: dict | None=None) -> bool:
        """Register a macro key with optional metadata; idempotent. Persists to macro_board.json."""
        try:
            self._macro_registry[name] = meta or {}
            try:
                self._persist_macro_board()
            except Exception:
                pass
            return True
        except Exception:
            return False

    def list_macros(self):
        """List available macro keys."""
        try:
            return sorted(self._macro_registry.keys())
        except Exception:
            return []

    def _persist_macro_board(self):
        """Write macro registry to run_dir/macro_board.json."""
        try:
            with open(self._macro_board_path, 'w', encoding='utf-8') as fh:
                json.dump(self._macro_registry, fh, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def emit_text(self, payload: dict, score: float=1.0):
        rec = {'type': 'text', 'payload': payload, 'score': float(score)}
        print("[UTD] text:", payload, f"(score={score:.3f})")
        try:
            line = json.dumps(rec, ensure_ascii=False)
            self._writer.write_line(line)
        except Exception:
            # keep stdout emission even if file writing fails
            pass

    def emit_macro(self, name: str, args: dict | None=None, score: float=1.0):
        """
        Emit a macro event. If the macro key is not registered, auto-register it
        (and persist to macro_board.json) to avoid breaking the runtime.
        """
        if name not in self._macro_registry:
            # go through register path so persistence occurs
            self.register_macro(name, {})
        rec = {'type': 'macro', 'macro': name, 'args': (args or {}), 'score': float(score)}
        print(f"[UTD] macro:{name}", (args or {}), f"(score={score:.3f})")
        try:
            line = json.dumps(rec, ensure_ascii=False)
            self._writer.write_line(line)
        except Exception:
            # keep stdout emission even if file writing fails
            pass

    def close(self):
        try:
            try:
                self._persist_macro_board()
            except Exception:
                pass
            # RollingJsonlWriter does not keep a persistent file handle; nothing to close.
        except Exception:
            pass
