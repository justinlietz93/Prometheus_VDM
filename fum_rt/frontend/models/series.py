from __future__ import annotations

import os
import math
from typing import Any, Dict, List
from dataclasses import dataclass


class StreamingZEMA:
    """
    Streaming z-score of deltas (ZEMA) with exponential moving averages.
    Matches legacy dashboard behavior exactly.
    """
    def __init__(self, half_life_ticks: int = 120):
        self.alpha = 1.0 - math.exp(math.log(0.5) / float(max(1, int(half_life_ticks))))
        self.mu = 0.0
        self.var = 1e-6
        self.prev = None

    def update(self, v: float) -> float:
        v = float(v)
        if self.prev is None:
            self.prev = v
            return 0.0
        d = v - self.prev
        self.prev = v
        a = self.alpha
        self.mu = (1.0 - a) * self.mu + a * d
        diff = d - self.mu
        self.var = (1.0 - a) * self.var + a * (diff * diff)
        sigma = (self.var if self.var > 1e-24 else 1e-24) ** 0.5
        return float(diff / sigma)


@dataclass
class SeriesState:
    """
    Rolling buffers for timeseries in the dashboard (unchanged semantics).
    """
    run_dir: str

    def __post_init__(self):
        self.events_path = os.path.join(self.run_dir, "events.jsonl")
        self.utd_path = os.path.join(self.run_dir, "utd_events.jsonl")
        self.events_size = 0
        self.utd_size = 0
        self.b1_ema = StreamingZEMA(half_life_ticks=120)
        self.t: List[int] = []
        self.active: List[float | None] = []
        self.avgw: List[float | None] = []
        self.coh: List[float | None] = []
        self.comp: List[float | None] = []
        self.b1z: List[float | None] = []
        self.val: List[float | None] = []
        self.val2: List[float | None] = []
        self.entro: List[float | None] = []
        self.speak_ticks: List[int] = []


def extract_tick(rec: Dict[str, Any]) -> int | None:
    for k in ("t", "tick"):
        if k in rec:
            try:
                return int(rec[k])
            except Exception:
                pass
    ex = rec.get("extra", {})
    for k in ("t", "tick"):
        if k in ex:
            try:
                return int(ex[k])
            except Exception:
                pass
    return None


def append_event(ss: SeriesState, rec: Dict[str, Any]):
    t = extract_tick(rec)
    if t is None:
        return
    ex = rec.get("extra", rec)
    ss.t.append(int(t))
    ss.active.append(ex.get("active_synapses"))
    ss.avgw.append(ex.get("avg_weight"))
    ss.coh.append(ex.get("cohesion_components"))
    cc = ex.get("complexity_cycles")
    ss.comp.append(cc)
    bz = ex.get("b1_z")
    if bz is None:
        v = 0.0 if cc is None else float(cc)
        bz = ss.b1_ema.update(v)
    ss.b1z.append(float(bz))
    # Robust SIE valence extraction with fallbacks (handles various field names and ranges)
    val = ex.get("sie_valence_01")
    if val is None:
        for k in ("sie_valence", "valence"):
            v = ex.get(k)
            if v is not None:
                try:
                    fv = float(v)
                    # Normalize [-1,1] -> [0,1] if appropriate
                    val = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                except Exception:
                    val = v
                break
        if val is None:
            sie = ex.get("sie") or {}
            if isinstance(sie, dict):
                if "valence_01" in sie:
                    val = sie.get("valence_01")
                elif "valence" in sie:
                    try:
                        fv = float(sie.get("valence"))
                        val = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                    except Exception:
                        val = sie.get("valence")
    ss.val.append(val)
    val2 = ex.get("sie_v2_valence_01")
    if val2 is None:
        for k in ("sie_v2_valence", "sie_v2"):
            v = ex.get(k)
            if v is not None:
                try:
                    fv = float(v)
                    val2 = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                except Exception:
                    val2 = v
                break
        if val2 is None:
            sie2 = ex.get("sie_v2") or {}
            if isinstance(sie2, dict):
                if "valence_01" in sie2:
                    val2 = sie2.get("valence_01")
                elif "valence" in sie2:
                    try:
                        fv = float(sie2.get("valence"))
                        val2 = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                    except Exception:
                        val2 = sie2.get("valence")
    ss.val2.append(val2)
    ss.entro.append(ex.get("connectome_entropy"))


def append_say(ss: SeriesState, rec: Dict[str, Any]):
    name = (rec.get("macro") or rec.get("name") or rec.get("kind") or "").lower()
    if name != "say":
        return
    t = rec.get("t") or rec.get("tick") or rec.get("meta", {}).get("t") or rec.get("meta", {}).get("tick")
    if t is None:
        return
    try:
        ss.speak_ticks.append(int(t))
    except Exception:
        pass


def ffill(arr: List[Any]) -> List[float | None]:
    out: List[float | None] = []
    last: float | None = None
    for x in arr:
        if x is None:
            out.append(last)
        else:
            try:
                v = float(x)
            except Exception:
                v = last
            out.append(v)
            last = v
    return out