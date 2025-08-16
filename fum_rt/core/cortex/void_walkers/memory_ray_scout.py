from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.memory_ray_scout

MemoryRayScout (read-only, void-faithful):
- Implements refractive-index steering using a slow memory field m.
- Local selection: P(i→j) ∝ exp(Theta * m[j]) with temperature tau (Boltzmann choice).
- Falls back to HeatMap head/dict when memory is absent to keep behavior useful OOTB.
- Emits vt_touch and edge_on events; no writes; no scans.

Signals (read-only):
- maps["memory_dict"] (preferred): bounded dict {node: value}
- maps["memory_head"] (optional): head list [[node, score], ...] for seeds
- Fallbacks:
  * maps["heat_dict"] / maps["heat_head"] used when memory is not available

Guardrails:
- No global scans or dense conversions; neighbors only.
- No schedulers; TTL/budget bounded; emits compact events only.

Fork law (two-branch junction):
- P(A) = sigmoid(Theta * (m_A - m_B)) for tau = 1, aligning with derivation/memory_steering.md
"""

from typing import Any, Dict, Optional, Set, Sequence, List
import math
import random

from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent, VTTouchEvent, EdgeOnEvent


def _head_to_set(maps: Optional[Dict[str, Any]], keys: Sequence[str], cap: int = 512) -> Set[int]:
    out: Set[int] = set()
    if not isinstance(maps, dict):
        return out
    for key in keys:
        try:
            head = maps.get(key, []) or []
            for pair in head[: cap]:
                try:
                    n = int(pair[0])
                except Exception:
                    continue
                if n >= 0:
                    out.add(n)
        except Exception:
            continue
    return out


def _dict_from_maps(maps: Optional[Dict[str, Any]], keys: Sequence[str]) -> Dict[int, float]:
    if not isinstance(maps, dict):
        return {}
    for key in keys:
        try:
            d = maps.get(key, {}) or {}
            # Accept dict snapshots directly; if head list was mistakenly passed, adapt minimally
            if isinstance(d, dict):
                return {int(k): float(v) for k, v in d.items()}  # type: ignore[arg-type]
            if isinstance(d, list):
                out: Dict[int, float] = {}
                for pair in d:
                    try:
                        n = int(pair[0])
                        s = float(pair[1]) if len(pair) > 1 else 1.0
                    except Exception:
                        continue
                    if n >= 0:
                        out[n] = s
                if out:
                    return out
        except Exception:
            continue
    return {}


def _softmax_choice(pairs: Sequence[tuple[int, float]]) -> Optional[int]:
    if not pairs:
        return None
    try:
        m = max(l for _, l in pairs)
        ws = [math.exp(l - m) for _, l in pairs]
        Z = sum(ws)
        if Z <= 0.0:
            return random.choice([i for i, _ in pairs])
        r = random.random() * Z
        acc = 0.0
        for (i, _), w in zip(pairs, ws):
            acc += w
            if r <= acc:
                return i
        return pairs[-1][0]
    except Exception:
        try:
            return int(random.choice([i for i, _ in pairs]))
        except Exception:
            return None


class MemoryRayScout(BaseScout):
    """
    Memory-driven scout: routes toward neighbors with higher memory values m[j].
    """

    __slots__ = ("theta_mem", "tau")

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 64,
        seed: int = 0,
        *,
        theta_mem: float = 0.8,
        tau: float = 1.0,
    ) -> None:
        super().__init__(budget_visits=budget_visits, budget_edges=budget_edges, ttl=ttl, seed=seed)
        self.theta_mem = float(theta_mem)
        self.tau = float(max(1e-6, tau))

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer memory head; fallback to heat head for useful boot behavior
        return _head_to_set(maps, keys=("memory_head", "heat_head"), cap=max(64, self.budget_visits * 8))

    def _pick_neighbor_scored(
        self,
        neigh: Sequence[int],
        maps: Optional[Dict[str, Any]],
    ) -> Optional[int]:
        if not neigh:
            return None
        # Prefer memory; fallback to heat as slow proxy
        md = _dict_from_maps(maps, keys=("memory_dict", "heat_dict"))
        logits: List[tuple[int, float]] = []
        th = float(self.theta_mem)
        inv_tau = 1.0 / float(self.tau)
        for v in neigh:
            j = int(v)
            try:
                m_j = float(md.get(j, 0.0))
            except Exception:
                m_j = 0.0
            s = th * m_j
            logits.append((j, s * inv_tau))
        return _softmax_choice(logits)

    def step(
        self,
        connectome: Any,
        bus: Any = None,  # unused
        maps: Optional[Dict[str, Any]] = None,
        budget: Optional[Dict[str, int]] = None,
    ) -> List[BaseEvent]:
        events: List[BaseEvent] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events

        b_vis = self.budget_visits
        b_edg = self.budget_edges
        ttl = self.ttl
        tick = 0
        seeds = None
        if isinstance(budget, dict):
            try:
                b_vis = int(budget.get("visits", b_vis))
            except Exception:
                pass
            try:
                b_edg = int(budget.get("edges", b_edg))
            except Exception:
                pass
            try:
                ttl = int(budget.get("ttl", ttl))
            except Exception:
                pass
            try:
                tick = int(budget.get("tick", 0))
            except Exception:
                tick = 0
            try:
                seeds = list(budget.get("seeds", []))
            except Exception:
                seeds = None

        b_vis = max(0, min(b_vis, N))
        b_edg = max(0, b_edg)
        ttl = max(1, ttl)

        priority: Set[int] = set()
        try:
            priority = self._priority_set(maps)
        except Exception:
            priority = set()

        if seeds:
            try:
                pool: Sequence[int] = tuple(int(s) for s in seeds if 0 <= int(s) < N) or tuple(priority) or tuple(range(N))
            except Exception:
                pool = tuple(priority) or tuple(range(N))
        else:
            pool = tuple(priority) or tuple(range(N))

        edges_emitted = 0
        visits_done = 0

        while visits_done < b_vis and pool:
            try:
                u = int(self.rng.choice(pool))
            except Exception:
                break

            cur = u
            depth = 0
            while depth < ttl:
                # Touch current node
                events.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(cur), w=1.0))
                visits_done += 1
                if visits_done >= b_vis:
                    break

                # Probe one neighbor edge if budget remains
                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if neigh:
                        v = self._pick_neighbor_scored(neigh, maps)
                        if v is None or v == cur:
                            # fallback to blue-noise hop
                            try:
                                v = int(self.rng.choice(tuple(neigh)))
                            except Exception:
                                break
                        if v != cur:
                            events.append(EdgeOnEvent(kind="edge_on", t=tick, u=int(cur), v=int(v)))
                            edges_emitted += 1
                            cur = int(v)
                        else:
                            break
                    else:
                        break
                else:
                    break

                depth += 1

        return events


__all__ = ["MemoryRayScout"]