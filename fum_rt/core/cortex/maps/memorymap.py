"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.cortex.maps.memorymap
Purpose: Memory map view for scouts/UI with bounded head/dict (void-faithful, no scans).

Design
- Single source of truth for slow memory field m[i] must live outside maps/ (e.g., core/memory/field.py).
- This class acts as a thin VIEW/ADAPTER over that field when provided (preferred).
- If no field is provided, it can optionally run as a bounded reducer proxy (Pattern B) that folds events
  but only retains a small working set (no full-N vector).

Contracts
- snapshot() returns:
    {
      "memory_head": list[[node, value], ...],   # top-k bounded
      "memory_p95": float,
      "memory_p99": float,
      "memory_max": float,
      "memory_count": int,
      "memory_dict": {node: value}               # bounded dictionary
    }

Guardrails
- No global scans; bounded working set only when operating in reducer-proxy mode.
- When a field is attached, fold() is a no-op; view delegates to the field snapshot.
"""

from typing import Any, Dict, Iterable, List
import math
import random

from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent, SpikeEvent, DeltaWEvent


class MemoryMap:
    """
    Thin view over MemoryField (preferred), with bounded fallback reducer (proxy) if field absent.

    Parameters:
      - field: optional memory field owner (preferred). When set, this map only adapts snapshots.
      - head_k: top-k head size for "memory_head"
      - dict_cap: maximum items to include in "memory_dict"
      - keep_max: maximum retained working-set size when operating in proxy mode (defaults to 16×head_k)
      - gamma/delta/kappa/touch_gain/spike_gain/dW_gain: only used in proxy mode
    """

    __slots__ = (
        "field",
        "head_k",
        "dict_cap",
        "keep_max",
        "rng",
        "_m",           # proxy-mode working set (absent when field provided)
        "_last_tick",   # proxy-mode last-tick tracker
        "gamma",
        "delta",
        "kappa",
        "touch_gain",
        "spike_gain",
        "dW_gain",
    )

    def __init__(
        self,
        field: Any | None = None,
        *,
        head_k: int = 256,
        dict_cap: int = 2048,
        keep_max: int | None = None,
        seed: int = 0,
        # proxy-mode dynamics
        gamma: float = 0.05,
        delta: float = 0.01,
        kappa: float = 0.10,
        touch_gain: float = 1.0,
        spike_gain: float = 0.20,
        dW_gain: float = 0.10,
    ) -> None:
        self.field = field
        self.head_k = int(max(8, head_k))
        self.dict_cap = int(max(8, dict_cap))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))

        # proxy-mode state (only used when field is None)
        self._m: Dict[int, float] = {}
        self._last_tick: Dict[int, int] = {}

        # proxy-mode parameters
        self.gamma = float(max(0.0, gamma))
        self.delta = float(max(0.0, min(1.0, delta)))
        self.kappa = float(max(0.0, kappa))
        self.touch_gain = float(max(0.0, touch_gain))
        self.spike_gain = float(max(0.0, spike_gain))
        self.dW_gain = float(max(0.0, dW_gain))

    # ---------------- adapter path (preferred) ----------------

    def _snapshot_from_field(self) -> Dict[str, object]:
        """Delegate snapshot to the owning field and adapt keys/caps."""
        fld = self.field
        if fld is None:
            return {}
        try:
            snap = fld.snapshot(head_n=self.head_k)  # expects keys memory_head/memory_dict/etc.
        except Exception:
            return {}
        if not isinstance(snap, dict):
            return {}

        head = snap.get("memory_head", []) or []
        dct = snap.get("memory_dict", {}) or {}

        # Cap dictionary size deterministically by highest values
        if isinstance(dct, dict) and len(dct) > self.dict_cap:
            try:
                import heapq as _heapq
                items = list(dct.items())
                top = _heapq.nlargest(int(self.dict_cap), items, key=lambda kv: kv[1])
                dct = {int(k): float(v) for k, v in top}
            except Exception:
                # Fallback: arbitrary trim
                keys = list(dct.keys())[: self.dict_cap]
                dct = {int(k): float(dct[k]) for k in keys if k in dct}

        p95 = snap.get("memory_p95", 0.0)
        p99 = snap.get("memory_p99", 0.0)
        vmax = snap.get("memory_max", 0.0)
        cnt = snap.get("memory_count", len(dct) if isinstance(dct, dict) else 0)

        return {
            "memory_head": head,
            "memory_p95": float(p95),
            "memory_p99": float(p99),
            "memory_max": float(vmax),
            "memory_count": int(cnt),
            "memory_dict": dct,
        }

    # ---------------- proxy-mode helpers (no field) ----------------

    def _decay_to(self, node: int, tick: int) -> None:
        lt = self._last_tick.get(node)
        if lt is None:
            self._last_tick[node] = tick
            return
        dt = max(0, int(tick) - int(lt))
        if dt > 0:
            try:
                base = max(0.0, 1.0 - self.delta)
                factor = base ** dt
            except Exception:
                factor = math.exp(-self.delta * float(dt))
            self._m[node] = float(self._m.get(node, 0.0)) * float(factor)
            self._last_tick[node] = tick

    def _ensure_and_decay(self, node: int, tick: int) -> None:
        n = int(node)
        if n not in self._m:
            self._m[n] = 0.0
            self._last_tick[n] = int(tick)
        else:
            self._decay_to(n, int(tick))

    def _prune(self) -> None:
        size = len(self._m)
        target_drop = size - self.keep_max
        if target_drop <= 0:
            return
        keys = list(self._m.keys())
        sample_size = min(len(keys), max(256, target_drop * 4))
        sample = self.rng.sample(keys, sample_size) if sample_size > 0 else keys
        sample.sort(key=lambda k: self._m.get(k, 0.0))
        for k in sample[:target_drop]:
            self._m.pop(k, None)
            self._last_tick.pop(k, None)

    # ---------------- API ----------------

    def fold(self, events: Iterable[object], tick: int) -> None:
        """
        Fold a batch of events.
        - If a field is attached, this is a no-op (owner already folds).
        - If no field, run bounded proxy updates (no scans).
        """
        if self.field is not None:
            return  # delegate model dynamics elsewhere

        t = int(tick)
        γ = self.gamma
        κ = self.kappa
        tg = self.touch_gain
        sg = self.spike_gain
        wg = self.dW_gain

        for e in events:
            k = getattr(e, "kind", None)

            if k == "vt_touch" and isinstance(e, VTTouchEvent):
                try:
                    i = int(e.token)
                except Exception:
                    continue
                if i < 0:
                    continue
                self._ensure_and_decay(i, t)
                r_i = float(getattr(e, "w", 1.0))
                self._m[i] = float(self._m.get(i, 0.0)) + float(γ * tg * r_i)
                if len(self._m) > self.keep_max:
                    self._prune()

            elif k == "edge_on" and isinstance(e, EdgeOnEvent):
                try:
                    u = int(getattr(e, "u", -1))
                    v = int(getattr(e, "v", -1))
                except Exception:
                    continue
                if u < 0 or v < 0:
                    continue
                self._ensure_and_decay(u, t)
                self._ensure_and_decay(v, t)
                mu = float(self._m.get(u, 0.0))
                mv = float(self._m.get(v, 0.0))
                d = float(κ * (mv - mu))
                self._m[u] = mu + d
                self._m[v] = mv - d
                if len(self._m) > self.keep_max:
                    self._prune()

            elif k == "spike" and isinstance(e, SpikeEvent):
                try:
                    j = int(getattr(e, "node", -1))
                except Exception:
                    continue
                if j < 0:
                    continue
                self._ensure_and_decay(j, t)
                amp = float(getattr(e, "amp", 1.0))
                self._m[j] = float(self._m.get(j, 0.0)) + float(γ * sg * amp)
                if len(self._m) > self.keep_max:
                    self._prune()

            elif k == "delta_w" and isinstance(e, DeltaWEvent):
                try:
                    j = int(getattr(e, "node", -1))
                except Exception:
                    continue
                if j < 0:
                    continue
                self._ensure_and_decay(j, t)
                dw = abs(float(getattr(e, "dw", 0.0)))
                self._m[j] = float(self._m.get(j, 0.0)) + float(γ * wg * dw)
                if len(self._m) > self.keep_max:
                    self._prune()

    def snapshot(self, head_n: int = 16) -> Dict[str, object]:
        """
        Return bounded snapshot dictionary per contract.
        - If field is present: adapt its snapshot and cap dict to dict_cap.
        - Else: produce from proxy working set (bounded by keep_max).
        """
        if self.field is not None:
            out = self._snapshot_from_field()
            if out:
                return out
            # fallthrough on error to proxy-mode snapshot (empty)

        if not self._m:
            return {
                "memory_head": [],
                "memory_p95": 0.0,
                "memory_p99": 0.0,
                "memory_max": 0.0,
                "memory_count": 0,
                "memory_dict": {},
            }

        # Head top-k
        try:
            import heapq as _heapq
            head = _heapq.nlargest(int(min(self.head_k, max(1, head_n))), self._m.items(), key=lambda kv: kv[1])
        except Exception:
            head = sorted(self._m.items(), key=lambda kv: kv[1], reverse=True)[: int(min(self.head_k, max(1, head_n)))]

        vals = sorted(float(v) for v in self._m.values())

        def q(p: float) -> float:
            if not vals:
                return 0.0
            i = min(len(vals) - 1, max(0, int(math.floor(p * (len(vals) - 1)))))
            return float(vals[i])

        # Cap dictionary size
        if len(self._m) > self.dict_cap:
            try:
                import heapq as _heapq
                items = list(self._m.items())
                top = _heapq.nlargest(int(self.dict_cap), items, key=lambda kv: kv[1])
                out_dict: Dict[int, float] = {int(k): float(v) for k, v in top}
            except Exception:
                keys = list(self._m.keys())[: self.dict_cap]
                out_dict = {int(k): float(self._m[k]) for k in keys if k in self._m}
        else:
            out_dict = {int(k): float(v) for k, v in self._m.items()}

        return {
            "memory_head": [[int(k), float(v)] for k, v in head],
            "memory_p95": q(0.95),
            "memory_p99": q(0.99),
            "memory_max": float(vals[-1]),
            "memory_count": int(len(vals)),
            "memory_dict": out_dict,
        }


__all__ = ["MemoryMap"]