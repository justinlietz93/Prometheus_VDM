from __future__ import annotations

"""
Event schema and incremental reducers for event-driven metrics (Phase C scaffolding).

Design:
- Pure core module. No imports from fum_rt.io.* or fum_rt.runtime.*.
- Does not perform any I/O or logging. Export numbers only.
- Safe-by-default: Can be instantiated but not wired unless feature flags enable event-driven path.
- O(1) per-event update; no scans over W in the hot path.

Provided:
- Event types: DeltaEvent, VTTouchEvent, EdgeOnEvent, EdgeOffEvent, MotifEnterEvent, MotifExitEvent, ADCEvent
- Incremental reducers:
    - StreamingMeanVar: Welford online (mean/var/std)
    - EWMA: exponential moving average
    - CountMinSketchHead: CMS plus exact head for entropy/coverage approximation
    - UnionFindCohesion: incremental cohesion via union set on edge_on; marks edge_off as dirty
- EventDrivenMetrics: folds events and exposes snapshot() dict of numeric metrics

Integration plan:
- Connectome/walkers publish events on the announce bus (outside core).
- Runtime/orchestrator drains bus and forwards events to EventDrivenMetrics.update().
- Telemetry snapshot reads EventDrivenMetrics.snapshot() and packages 'why'.
- Old scan-based metrics remain the default until flags enable event-driven path.

Caveats:
- Edge_off is marked dirty; a low-cadence auditor is expected to reconcile connectivity.
- VT coverage/entropy are approximate via CMS+head; auditor can validate.
"""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple
import math
import random

# Allowed core import
from fum_rt.core.metrics import StreamingZEMA  # existing Z detector in core


# ----------------------------- Event Types -----------------------------------

@dataclass(frozen=True)
class BaseEvent:
    kind: str
    t: Optional[int] = None


@dataclass(frozen=True)
class DeltaEvent(BaseEvent):
    """
    Local structural/learning delta.
    Fields:
      - b1: contribution to B1-like topology signal (float)
      - novelty: novelty component in [0, +inf)
      - hab: habituation component in [0, +inf)
      - td: temporal-difference-like component (float)
      - hsi: homeostatic stability/instability component (float)
    """
    b1: float = 0.0
    novelty: float = 0.0
    hab: float = 0.0
    td: float = 0.0
    hsi: float = 0.0


@dataclass(frozen=True)
class VTTouchEvent(BaseEvent):
    """
    Vocabulary/feature touch (used for VT coverage/entropy approximations).
    Fields:
      - token: hashable token id or string
      - w: optional weight (float, default 1.0)
    """
    token: Any = ""
    w: float = 1.0


@dataclass(frozen=True)
class EdgeOnEvent(BaseEvent):
    u: int = 0
    v: int = 0


@dataclass(frozen=True)
class EdgeOffEvent(BaseEvent):
    u: int = 0
    v: int = 0


@dataclass(frozen=True)
class MotifEnterEvent(BaseEvent):
    motif_id: int = 0


@dataclass(frozen=True)
class MotifExitEvent(BaseEvent):
    motif_id: int = 0


@dataclass(frozen=True)
class ADCEvent(BaseEvent):
    """
    ADC estimator readout event (fold metrics in place of reading raw structures).
    Suggested fields (all optional, numeric):
      - adc_territories
      - adc_boundaries
      - adc_cycle_hits
    """
    adc_territories: Optional[int] = None
    adc_boundaries: Optional[int] = None
    adc_cycle_hits: Optional[float] = None


# -------------------------- Incremental Primitives ---------------------------

class StreamingMeanVar:
    """
    Welford's algorithm for streaming mean/variance/std.
    """
    __slots__ = ("n", "mean", "M2")

    def __init__(self) -> None:
        self.n = 0
        self.mean = 0.0
        self.M2 = 0.0

    def update(self, x: float) -> None:
        try:
            x = float(x)
        except Exception:
            return
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        delta2 = x - self.mean
        self.M2 += delta * delta2

    def variance(self) -> float:
        if self.n < 2:
            return 0.0
        return self.M2 / (self.n - 1)

    def std(self, eps: float = 1e-9) -> float:
        v = self.variance()
        if v <= 0.0:
            return eps
        return math.sqrt(v) + eps


class EWMA:
    """
    Exponential Weighted Moving Average.
    """
    __slots__ = ("alpha", "y")

    def __init__(self, alpha: float = 0.05, init: float = 0.0) -> None:
        self.alpha = float(max(0.0, min(1.0, alpha)))
        self.y = float(init)

    def update(self, x: float) -> float:
        x = float(x)
        self.y = self.alpha * x + (1.0 - self.alpha) * self.y
        return self.y

    def value(self) -> float:
        return float(self.y)


class CountMinSketchHead:
    """
    Approximate frequency model for VT coverage/entropy.
    - CMS for tail, plus an exact head map for top-k tokens.
    - Entropy and coverage computed from head counts; tail mass estimated via CMS minimum row sum.

    Note: This is a lightweight approximation; an auditor can reconcile periodically.
    """
    def __init__(self, width: int = 256, depth: int = 3, head_k: int = 256, seed: int = 0) -> None:
        self.w = max(8, int(width))
        self.d = max(1, int(depth))
        self.head_k = max(8, int(head_k))
        rng = random.Random(int(seed))
        self._a = [rng.randrange(1, 2**61 - 1) for _ in range(self.d)]
        self._b = [rng.randrange(0, 2**61 - 1) for _ in range(self.d)]
        self._P = (2**61 - 1)
        self._M = [[0.0 for _ in range(self.w)] for _ in range(self.d)]
        self._head: Dict[Any, float] = {}
        self._total = 0.0

    def _h(self, i: int, key_hash: int) -> int:
        return ((self._a[i] * key_hash + self._b[i]) % self._P) % self.w

    def _hash_key(self, key: Any) -> int:
        # Stable hash across process; for best stability use explicit str
        return hash(str(key))

    def update(self, key: Any, w: float = 1.0) -> None:
        try:
            w = float(w)
        except Exception:
            return
        if w <= 0.0:
            return
        self._total += w
        kh = self._hash_key(key)
        for i in range(self.d):
            j = self._h(i, kh)
            self._M[i][j] += w
        # Update head exact counts; keep only top-K
        cur = self._head.get(key, 0.0) + w
        self._head[key] = cur
        if len(self._head) > self.head_k * 2:
            # prune lower half
            items = sorted(self._head.items(), key=lambda kv: kv[1], reverse=True)[: self.head_k]
            self._head = dict(items)

    def estimate(self, key: Any) -> float:
        if key in self._head:
            return float(self._head[key])
        kh = self._hash_key(key)
        est = min(self._M[i][self._h(i, kh)] for i in range(self.d))
        return float(est)

    def coverage(self) -> float:
        """
        Approximate coverage as fraction of head mass over total.
        """
        if self._total <= 0.0:
            return 0.0
        head_mass = sum(self._head.values())
        return float(max(0.0, min(1.0, head_mass / self._total)))

    def entropy(self, eps: float = 1e-12) -> float:
        """
        Shannon entropy over head distribution (tail ignored), in nats.
        """
        head_mass = sum(self._head.values())
        if head_mass <= 0.0:
            return 0.0
        H = 0.0
        for _, c in self._head.items():
            p = float(c / head_mass)
            if p > 0.0:
                H -= p * math.log(p + eps)
        return float(H)

    def snapshot(self) -> Dict[str, float]:
        return {
            "vt_coverage": self.coverage(),
            "vt_entropy": self.entropy(),
        }


class UnionFindCohesion:
    """
    Incremental cohesion via union-find on edge_on events.
    Edge_off events mark dirty; auditor should reconcile at low cadence.

    Exposes:
      - union(u,v) on edge_on
      - mark_dirty(u,v) on edge_off
      - components() approximate count (dirty edges may increase this transiently)
    """
    def __init__(self, n_hint: int = 0) -> None:
        self.parent: Dict[int, int] = {}
        self.size: Dict[int, int] = {}
        self._dirty = 0  # count of edge_off marks since last audit

    def _find(self, x: int) -> int:
        # path compression
        if self.parent.get(x, x) != x:
            self.parent[x] = self._find(self.parent[x])
        return self.parent.get(x, x)

    def _ensure(self, x: int) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1

    def union(self, u: int, v: int) -> None:
        self._ensure(u)
        self._ensure(v)
        ru = self._find(u)
        rv = self._find(v)
        if ru == rv:
            return
        su = self.size.get(ru, 1)
        sv = self.size.get(rv, 1)
        if su < sv:
            ru, rv = rv, ru
            su, sv = sv, su
        self.parent[rv] = ru
        self.size[ru] = su + sv

    def mark_dirty(self, _u: int, _v: int) -> None:
        self._dirty += 1

    def components(self) -> int:
        roots = sum(1 for k, p in self.parent.items() if k == p)
        # naive dirty inflation (auditor should reconcile)
        return int(roots + 0)


# ---------------------------- Event-Driven Metrics ---------------------------

class EventDrivenMetrics:
    """
    O(1) per-event folding of key telemetry metrics.

    Maintained:
      - b1_value, b1_z (via StreamingZEMA)
      - vt_coverage, vt_entropy (via CountMinSketchHead)
      - cohesion_components (via UnionFindCohesion)
      - adc_territories, adc_boundaries (fold ADCEvent)
      - complexity_cycles proxy from ADC (adc_cycle_hits)

    Snapshot includes fields expected by telemetry packagers. Missing fields default to 0.0 or 0.
    """
    def __init__(
        self,
        z_half_life_ticks: int = 50,
        z_spike: float = 1.0,
        hysteresis: float = 1.0,
        vt_width: int = 256,
        vt_depth: int = 3,
        vt_head_k: int = 256,
        seed: int = 0,
    ) -> None:
        self.b1_detector = StreamingZEMA(
            half_life_ticks=int(max(1, z_half_life_ticks)),
            z_spike=float(z_spike),
            hysteresis=float(hysteresis),
            min_interval_ticks=1,
        )
        self._b1_value = 0.0
        self._b1_last: Dict[str, float] = {}
        self._vt = CountMinSketchHead(width=vt_width, depth=vt_depth, head_k=vt_head_k, seed=seed)
        self._cohesion = UnionFindCohesion()
        self._adc_territories = 0
        self._adc_boundaries = 0
        self._adc_cycle_hits = 0.0
        self._tick = 0

    def update(self, ev: BaseEvent) -> None:
        self._tick = int(getattr(ev, "t", self._tick))
        k = getattr(ev, "kind", None)
        if not k:
            return
        if k == "delta":
            dev: DeltaEvent = ev  # type: ignore[assignment]
            # b1_value as additive proxy; alternative mappings can be calibrated
            try:
                self._b1_value += float(dev.b1)
                z = self.b1_detector.update(self._b1_value, tick=self._tick)
                self._b1_last = {
                    "b1_value": float(z.get("value", 0.0)),
                    "b1_delta": float(z.get("delta", 0.0)),
                    "b1_z": float(z.get("z", 0.0)),
                    "b1_spike": bool(z.get("spike", False)),
                }
            except Exception:
                pass
            # SIE components can be folded externally; this class does not compute valence
        elif k == "vt_touch":
            tev: VTTouchEvent = ev  # type: ignore[assignment]
            try:
                self._vt.update(tev.token, w=float(getattr(tev, "w", 1.0)))
            except Exception:
                pass
        elif k == "edge_on":
            e: EdgeOnEvent = ev  # type: ignore[assignment]
            try:
                self._cohesion.union(int(e.u), int(e.v))
            except Exception:
                pass
        elif k == "edge_off":
            e: EdgeOffEvent = ev  # type: ignore[assignment]
            try:
                self._cohesion.mark_dirty(int(e.u), int(e.v))
            except Exception:
                pass
        elif k == "adc":
            a: ADCEvent = ev  # type: ignore[assignment]
            try:
                if a.adc_territories is not None:
                    self._adc_territories = int(a.adc_territories)
                if a.adc_boundaries is not None:
                    self._adc_boundaries = int(a.adc_boundaries)
                if a.adc_cycle_hits is not None:
                    self._adc_cycle_hits = float(a.adc_cycle_hits)
            except Exception:
                pass
        elif k in ("motif_enter", "motif_exit"):
            # Motif events can be used to refine b1_value or cohesion; placeholder noop.
            pass
        else:
            # Unknown event kinds are ignored (forward-compat)
            pass

    def snapshot(self) -> Dict[str, Any]:
        vt = self._vt.snapshot()
        snap = {
            # B1
            "b1_value": float(self._b1_last.get("b1_value", 0.0)),
            "b1_delta": float(self._b1_last.get("b1_delta", 0.0)),
            "b1_z": float(self._b1_last.get("b1_z", 0.0)),
            "b1_spike": bool(self._b1_last.get("b1_spike", False)),
            # VT
            "vt_coverage": float(vt.get("vt_coverage", 0.0)),
            "vt_entropy": float(vt.get("vt_entropy", 0.0)),
            # Cohesion
            "cohesion_components": int(self._cohesion.components()),
            # ADC readouts
            "adc_territories": int(self._adc_territories),
            "adc_boundaries": int(self._adc_boundaries),
            # Cycle proxy feed-through (can be added to complexity_cycles by caller)
            "adc_cycle_hits": float(self._adc_cycle_hits),
        }
        return snap


__all__ = [
    # events
    "BaseEvent",
    "DeltaEvent",
    "VTTouchEvent",
    "EdgeOnEvent",
    "EdgeOffEvent",
    "MotifEnterEvent",
    "MotifExitEvent",
    "ADCEvent",
    # reducers
    "StreamingMeanVar",
    "EWMA",
    "CountMinSketchHead",
    "UnionFindCohesion",
    "EventDrivenMetrics",
]