from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_frontier_scout

FrontierScout (read-only, void-faithful):
- Skims component boundaries and likely bridge frontiers to refresh cohesion/cycle estimators.
- Purely local heuristics; no scans. Emits vt_touch and edge_on only.

Local neighbor score for hop u→j (bounded, read-only):
    s_j = + w_cold * cold[j]
          - w_heat * heat[j]
          - w_shn  * shared_neighbors(u, j)
          + w_deg  * I[deg(j) != deg(u)]

Inputs (optional):
- maps["cold_head"] / maps["heat_head"] to derive small dicts (bounded).
- Only local neighbor lists are read; no global adjacency or dense-array access.

Guardrails:
- No schedulers; TTL/budgets enforce bounds.
- No writes; events only.
"""

from typing import Any, Dict, Optional, Set, Sequence, List
import math

from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent, VTTouchEvent, EdgeOnEvent


def _head_to_dict(maps: Optional[Dict[str, Any]], key: str, cap: int = 1024) -> Dict[int, float]:
    out: Dict[int, float] = {}
    if not isinstance(maps, dict):
        return out
    try:
        head = maps.get(key, []) or []
        head = head[: cap]
        vmax = 0.0
        tmp: List[tuple[int, float]] = []
        for pair in head:
            try:
                n = int(pair[0])
                s = float(pair[1]) if len(pair) > 1 else 1.0
            except Exception:
                continue
            if n >= 0:
                tmp.append((n, s))
                vmax = max(vmax, s)
        if vmax <= 0.0:
            for n, s in tmp:
                out[n] = 1.0
        else:
            for n, s in tmp:
                out[n] = max(0.0, min(1.0, s / vmax))
    except Exception:
        return out
    return out


class FrontierScout(BaseScout):
    """
    Boundary/cohesion probe: prefer edges that look like weak cuts or cross-degree boundaries.
    """

    __slots__ = ("w_cold", "w_heat", "w_shn", "w_deg", "tau")

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 64,
        seed: int = 0,
        *,
        w_cold: float = 1.0,
        w_heat: float = 0.5,
        w_shn: float = 0.25,
        w_deg: float = 0.5,
        tau: float = 1.0,
    ) -> None:
        super().__init__(budget_visits=budget_visits, budget_edges=budget_edges, ttl=ttl, seed=seed)
        self.w_cold = float(max(0.0, w_cold))
        self.w_heat = float(max(0.0, w_heat))
        self.w_shn = float(max(0.0, w_shn))
        self.w_deg = float(max(0.0, w_deg))
        self.tau = float(max(1e-6, tau))

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer coldest tiles as starting seeds
        out: Set[int] = set()
        if not isinstance(maps, dict):
            return out
        try:
            head = maps.get("cold_head", []) or []
            for pair in head[: max(64, self.budget_visits * 8)]:
                try:
                    n = int(pair[0])
                    if n >= 0:
                        out.add(n)
                except Exception:
                    continue
        except Exception:
            return out
        return out

    @staticmethod
    def _shared_neighbors(connectome: Any, u: int, v: int, cap: int = 128) -> int:
        try:
            nu = set(int(x) for x in (connectome.neighbors(u) or []))  # type: ignore[attr-defined]
        except Exception:
            try:
                nu = set(int(x) for x in (connectome.get_neighbors(u) or []))  # type: ignore[attr-defined]
            except Exception:
                nu = set()
        try:
            nv_list = (connectome.neighbors(v) or [])  # type: ignore[attr-defined]
        except Exception:
            try:
                nv_list = (connectome.get_neighbors(v) or [])  # type: ignore[attr-defined]
            except Exception:
                nv_list = []
        # Bound cost: only check up to 'cap' neighbors of v
        cnt = 0
        for x in list(nv_list)[: max(0, int(cap))]:
            try:
                if int(x) in nu:
                    cnt += 1
            except Exception:
                continue
        return int(cnt)

    @staticmethod
    def _deg(connectome: Any, u: int) -> int:
        try:
            xs = connectome.neighbors(u)  # type: ignore[attr-defined]
        except Exception:
            try:
                xs = connectome.get_neighbors(u)  # type: ignore[attr-defined]
            except Exception:
                xs = []
        try:
            return int(len(xs or []))
        except Exception:
            return 0

    def _pick_neighbor_scored(
        self,
        cur: int,
        neigh: Sequence[int],
        connectome: Any,
        maps: Optional[Dict[str, Any]],
    ) -> Optional[int]:
        if not neigh:
            return None
        cold = _head_to_dict(maps, "cold_head", cap=1024)
        heat = _head_to_dict(maps, "heat_head", cap=1024)

        du = self._deg(connectome, int(cur))
        logits: List[tuple[int, float]] = []
        inv_tau = 1.0 / self.tau
        for v in neigh:
            j = int(v)
            shn = float(self._shared_neighbors(connectome, int(cur), j, cap=64))
            dj = self._deg(connectome, j)
            s = (
                (self.w_cold * float(cold.get(j, 0.0)))
                - (self.w_heat * float(heat.get(j, 0.0)))
                - (self.w_shn * shn)
                + (self.w_deg * (1.0 if dj != du else 0.0))
            )
            logits.append((j, s * inv_tau))

        # Softmax
        try:
            m = max(l for _, l in logits)
            ws = [math.exp(l - m) for _, l in logits]
            Z = sum(ws)
            if Z <= 0.0:
                return int(logits[0][0])
            r = (hash((cur, du, len(neigh))) & 0xFFFF) / 65535.0 * Z
            acc = 0.0
            for (i, _), w in zip(logits, ws):
                acc += w
                if r <= acc:
                    return i
            return int(logits[-1][0])
        except Exception:
            try:
                return int(logits[0][0])
            except Exception:
                return None

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

                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if neigh:
                        v = self._pick_neighbor_scored(int(cur), neigh, connectome, maps)
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


__all__ = ["FrontierScout"]