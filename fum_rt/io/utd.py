
import sys, json, os

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
        self._fh = open(self.path, 'a', encoding='utf-8')
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
        self._fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self._fh.flush()

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
        self._fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self):
        try:
            try:
                self._persist_macro_board()
            except Exception:
                pass
            self._fh.close()
        except Exception:
            pass
