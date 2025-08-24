from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_heat_scout

HeatScout (read-only, void-faithful):
- Local-only neighbor selection using a softmax over map signals.
- Supports trail repulsion (short-term) and optional memory steering (long-term).
- Emits vt_touch and edge_on events; no writes; no scans.

Logit per neighbor j:
    logit_j = theta_mem * m_j - rho_trail * htrail_j + gamma_heat * h_j

Where:
- m_j: slow memory value (maps.get("memory_dict", {})[j]) if provided; else 0.
- htrail_j: short-term trail/heat value (maps["trail_dict"] if present, else maps["heat_dict"]; fallback 0).
- h_j: HeatMap score (maps["heat_dict"] if present; fallback 0).
- theta_mem (can be ±) sets attraction (>) or repulsion (<) to memory.
- rho_trail >= 0 repels recently traversed/hot nodes.
- gamma_heat >= 0 biases toward heat fronts when desired (default 1.0).
- tau > 0 is temperature (lower tau = sharper decisions).

Notes:
- If maps dicts are absent, falls back to priority head nodes (if any), then blue-noise hop.
- Priority seed set still used for initial pool bias via _priority_set().
"""

from typing import Any, Dict, Optional, Set, Sequence, List
import math
import random

from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent, VTTouchEvent, EdgeOnEvent


def _head_to_set(maps: Optional[Dict[str, Any]], key: str, cap: int = 512) -> Set[int]:
    out: Set[int] = set()
    if not isinstance(maps, dict):
        return out
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
        return out
    return out


def _head_to_dict(maps: Optional[Dict[str, Any]], key: str, cap: int = 2048) -> Dict[int, float]:
    d: Dict[int, float] = {}
    if not isinstance(maps, dict):
        return d
    try:
        head = maps.get(key, []) or []
        if isinstance(head, dict):
            # already a dict
            for k, v in list(head.items())[: cap]:
                try:
                    d[int(k)] = float(v)
                except Exception:
                    continue
            return d
        for pair in head[: cap]:
            try:
                n = int(pair[0])
                s = float(pair[1]) if len(pair) > 1 else 1.0
            except Exception:
                continue
            if n >= 0:
                d[n] = s
    except Exception:
        return d
    return d


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


class HeatScout(BaseScout):
    """
    Activity-driven scout with optional memory steering and trail repulsion.
    Defaults preserve legacy behavior (follow heat; no memory, no repulsion).
    """

    __slots__ = ("theta_mem", "rho_trail", "gamma_heat", "tau")

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 64,
        seed: int = 0,
        *,
        theta_mem: float = 0.0,
        rho_trail: float = 0.0,
        gamma_heat: float = 1.0,
        tau: float = 1.0,
    ) -> None:
        super().__init__(budget_visits=budget_visits, budget_edges=budget_edges, ttl=ttl, seed=seed)
        self.theta_mem = float(theta_mem)
        self.rho_trail = float(max(0.0, rho_trail))
        self.gamma_heat = float(max(0.0, gamma_heat))
        self.tau = float(max(1e-6, tau))

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer HeatMap head indices for seeds
        return _head_to_set(maps, "heat_head", cap=max(64, self.budget_visits * 8))

    def _pick_neighbor_scored(
        self,
        neigh: Sequence[int],
        maps: Optional[Dict[str, Any]],
    ) -> Optional[int]:
        if not neigh:
            return None
        # Pull small dicts from maps (bounded heads or dict snapshots)
        md = maps.get("memory_dict", {}) if isinstance(maps, dict) else {}
        hd = maps.get("heat_dict", {}) if isinstance(maps, dict) else {}
        td = maps.get("trail_dict", {}) if isinstance(maps, dict) else {}
        # Allow fallback to heat as trail if explicit trail absent
        use_td = td if td else hd

        logits: List[tuple[int, float]] = []
        for v in neigh:
            j = int(v)
            try:
                m_j = float(md.get(j, 0.0))
            except Exception:
                m_j = 0.0
            try:
                htrail_j = float(use_td.get(j, 0.0))
            except Exception:
                htrail_j = 0.0
            try:
                h_j = float(hd.get(j, 0.0))
            except Exception:
                h_j = 0.0
            s = (self.theta_mem * m_j) - (self.rho_trail * htrail_j) + (self.gamma_heat * h_j)
            logits.append((j, s / self.tau))
        return _softmax_choice(logits)

    def step(
        self,
        connectome: Any,
        bus: Any = None,  # unused
        maps: Optional[Dict[str, Any]] = None,
        budget: Optional[Dict[str, int]] = None,
    ) -> List[BaseEvent]:
        # Inline copy of BaseScout.step to insert map-aware neighbor choice.
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

                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if neigh:
                        v = self._pick_neighbor_scored(neigh, maps)
                        if v is None or v == cur:
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


__all__ = ["HeatScout"]
