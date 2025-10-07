from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.memory.field
Purpose: Event-driven memory field with write-decay-spread dynamics (void-faithful).

Design constraints
- Sparse-first: no dense global passes; updates are event-local only.
- No schedulers: called from the per-tick CoreEngine fold path.
- No scans in core/ or maps/: bounded working set; pruning uses sampling.
- Maps/frame v1/v2 unchanged (telemetry-only); this reducer is for local steering.
- Guards pass; control-impact is minimal since this only folds small event batches.

Dynamics (per tick, event-driven)
- On node touch (vt_touch at node i):
    m[i] ← m[i] * exp(-δ·Δt) + γ · r_i · Δt
  where r_i is a small stimulus inferred from event weight (default 1.0).

- On edge_on(i, j) smoothing (one-edge local spread):
    δm = κ · (m[j] − m[i]) · Δt
    m[i] += δm
    m[j] −= δm

- Optional burst footprints:
    SpikeEvent(node=j, amp) → m[j] += γ_s · amp · Δt
    DeltaWEvent(node=j, dw) → m[j] += γ_w · |dw| · Δt

Snapshot
- memory_head: top-k [[node, value], ...] by current m value (k=head_k, default 256)
- memory_p95/p99/max/count: summaries of working set
- memory_dict: bounded dictionary {node: m} (size ≤ keep_max)

Tuning (dimensionless)
- gamma (γ): write gain
- delta (δ): exponential decay rate per tick
- kappa (κ): one-edge smoothing coupling
- touch_gain, spike_gain, dW_gain: per-event scalings feeding the write term
"""

from typing import Dict, Iterable, List, Tuple
import math
import random

from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent, SpikeEvent, DeltaWEvent


class MemoryField:
    """
    Event-driven, bounded memory field.

    Parameters:
      - head_k: top-k head size for memory_head
      - keep_max: max retained working-set size (defaults to 16×head_k)
      - seed: RNG seed for pruning sampling
      - gamma: write gain (γ)
      - delta: decay rate (δ) per tick (0..1)
      - kappa: one-edge smoothing coupling (κ)
      - touch_gain/spike_gain/dW_gain: event-to-write scaling
    """

    __slots__ = (
        "head_k",
        "keep_max",
        "rng",
        "_m",
        "_last_tick",
        "gamma",
        "delta",
        "kappa",
        "touch_gain",
        "spike_gain",
        "dW_gain",
    )

    def __init__(
        self,
        head_k: int = 256,
        keep_max: int | None = None,
        seed: int = 0,
        *,
        gamma: float = 0.05,
        delta: float = 0.01,
        kappa: float = 0.10,
        touch_gain: float = 1.0,
        spike_gain: float = 0.20,
        dW_gain: float = 0.10,
    ) -> None:
        self.head_k = int(max(8, head_k))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))
        self._m: Dict[int, float] = {}
        self._last_tick: Dict[int, int] = {}

        # dynamics
        self.gamma = float(max(0.0, gamma))
        self.delta = float(max(0.0, min(1.0, delta)))
        self.kappa = float(max(0.0, kappa))
        self.touch_gain = float(max(0.0, touch_gain))
        self.spike_gain = float(max(0.0, spike_gain))
        self.dW_gain = float(max(0.0, dW_gain))

    # ---------------- internal helpers ----------------

    def _decay_to(self, node: int, tick: int) -> None:
        lt = self._last_tick.get(node)
        if lt is None:
            self._last_tick[node] = tick
            return
        dt = max(0, int(tick) - int(lt))
        if dt > 0:
            # Exponential decay: m *= exp(-δ·Δt). Use (1-δ)^Δt for stability when δ small.
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
        # Drop smallest m in the sample
        sample.sort(key=lambda k: self._m.get(k, 0.0))
        for k in sample[:target_drop]:
            self._m.pop(k, None)
            self._last_tick.pop(k, None)

    # ---------------- public API ----------------

    def fold(self, events: Iterable[object], tick: int) -> None:
        """
        Fold a batch of events at integer tick.
        """
        t = int(tick)
        γ = self.gamma
        δ = self.delta
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
                # decay-then-write at node i
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
                # local smoothing on the edge (u, v)
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
        Return bounded snapshot of the field.
        """
        if not self._m:
            return {
                "memory_head": [],
                "memory_p95": 0.0,
                "memory_p99": 0.0,
                "memory_max": 0.0,
                "memory_count": 0,
                "memory_dict": {},
            }

        # head top-k
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

        out_dict: Dict[int, float] = {int(k): float(v) for k, v in self._m.items()}

        return {
            "memory_head": [[int(k), float(v)] for k, v in head],
            "memory_p95": q(0.95),
            "memory_p99": q(0.99),
            "memory_max": float(vals[-1]),
            "memory_count": int(len(vals)),
            "memory_dict": out_dict,
        }

    # ---------------- taps / adapters ----------------

    def get_m(self, i: int) -> float:
        """
        O(1) local read for node i.
        """
        try:
            return float(self._m.get(int(i), 0.0))
        except Exception:
            return 0.0

    def get_many(self, idxs) -> Dict[int, float]:
        """
        Return {i: m[i]} for a small iterable of indices.
        """
        out: Dict[int, float] = {}
        try:
            for j in idxs or []:
                try:
                    out[int(j)] = float(self._m.get(int(j), 0.0))
                except Exception:
                    continue
        except Exception:
            pass
        return out

    def update_from_events(self, events, dt_ms: int | float | None = None) -> None:
        """
        Alias for fold() to support adapter-style interfaces. dt_ms is ignored; tick should be provided in events or by the caller.
        """
        # Use last seen tick for touched nodes when missing; safe fallback 0.
        # Here we just pass 0; runtime passes proper tick to fold() already.
        self.fold(events, tick=0)

    def snapshot_head(self, head_k: int | None = None) -> List[List[float]]:
        """
        Convenience: return just the head list (top-k) [[node, value], ...]
        """
        k = int(self.head_k if head_k is None else max(1, head_k))
        snap = self.snapshot(head_n=k)
        head = snap.get("memory_head", []) if isinstance(snap, dict) else []
        return head or []

    def snapshot_dict(self, cap: int = 2048) -> Dict[int, float]:
        """
        Convenience: return a bounded dict {node:value}.
        """
        snap = self.snapshot(head_n=self.head_k)
        dct = snap.get("memory_dict", {}) if isinstance(snap, dict) else {}
        if not isinstance(dct, dict):
            return {}
        if len(dct) <= int(cap):
            return {int(k): float(v) for k, v in dct.items()}
        try:
            import heapq as _heapq
            items = list(dct.items())
            top = _heapq.nlargest(int(cap), items, key=lambda kv: kv[1])
            return {int(k): float(v) for k, v in top}
        except Exception:
            keys = list(dct.keys())[: int(cap)]
            return {int(k): float(dct[k]) for k in keys if k in dct}

    # ---------------- dimensionless knobs (read-only) ----------------

    @property
    def D_a(self) -> float:
        """Write gain (γ)"""
        return float(self.gamma)

    @property
    def Lambda(self) -> float:
        """Decay rate (δ)"""
        return float(self.delta)

    @property
    def Gamma(self) -> float:
        """One-edge smoothing (κ)"""
        return float(self.kappa)

    @property
    def Theta(self) -> float:
        """
        Steering coefficient placeholder (field does not steer directly).
        Provided for dimensional consistency; steering lives in walkers.
        """
        return 0.0


__all__ = ["MemoryField"]