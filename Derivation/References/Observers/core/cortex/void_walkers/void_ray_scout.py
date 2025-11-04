"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_ray_scout

VoidRayScout (read-only, void-faithful):
- Physics-aware routing that prefers neighbors with favorable local change in a fast field φ.
- Local scoring (no scans): for hop i→j, s_j = lambda_phi * (φ[j] - φ[i]) + theta_mem * m[j]
- Temperatured choice via softmax over neighbors; strictly local reads.
- Emits vt_touch and edge_on events; optional spike can be added by subclasses if needed.

Signals (read-only):
- connectome.phi: per-node scalar field (Sequence/ndarray-like) when present; otherwise treated as zeros.
- maps["memory_dict"]: optional slow memory field (bounded dict snapshot), default empty.

Guardrails:
- No global scans or dense conversions.
- Operates only on local neighbor lists and small map snapshots.
- No schedulers; TTL/budget bounded; emits compact events only.

References:
- Refractive-index steering law: P(i→j) ∝ exp(Θ · m[j]) with logistic 2-way fork (see Derivation/memory_steering.md).
"""

from typing import Any, Dict, Optional, Set, Sequence, List
import math

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


def _softmax_choice(pairs: Sequence[tuple[int, float]]) -> Optional[int]:
    if not pairs:
        return None
    try:
        m = max(l for _, l in pairs)
        ws = [math.exp(l - m) for _, l in pairs]
        Z = sum(ws)
        if Z <= 0.0:
            # fallback to uniform pick among candidates
            return pairs[0][0]
        r = (hash((len(pairs), m, Z)) & 0xFFFF) / 65535.0 * Z  # deterministic-ish fallback
        acc = 0.0
        for (i, _), w in zip(pairs, ws):
            acc += w
            if r <= acc:
                return i
        return pairs[-1][0]
    except Exception:
        try:
            return int(pairs[0][0])
        except Exception:
            return None


class VoidRayScout(BaseScout):
    """
    Physics-aware scout: routes along favorable local φ gradients with optional memory steering.
    """

    __slots__ = ("lambda_phi", "theta_mem", "tau")

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 64,
        seed: int = 0,
        *,
        lambda_phi: float = 1.0,
        theta_mem: float = 0.0,
        tau: float = 1.0,
    ) -> None:
        super().__init__(budget_visits=budget_visits, budget_edges=budget_edges, ttl=ttl, seed=seed)
        self.lambda_phi = float(lambda_phi)
        self.theta_mem = float(theta_mem)
        self.tau = float(max(1e-6, tau))

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer HeatMap head when available for initial seeds (bounded, read-only)
        return _head_to_set(maps, "heat_head", cap=max(64, self.budget_visits * 8))

    def _pick_neighbor_scored(
        self,
        cur: int,
        neigh: Sequence[int],
        connectome: Any,
        maps: Optional[Dict[str, Any]],
    ) -> Optional[int]:
        if not neigh:
            return None

        # φ values: read only local entries (no scans)
        phi = getattr(connectome, "phi", None)

        def _phi(idx: int) -> float:
            try:
                if phi is None:
                    return 0.0
                return float(phi[idx])
            except Exception:
                return 0.0

        phi_i = _phi(int(cur))
        md = maps.get("memory_dict", {}) if isinstance(maps, dict) else {}

        logits: List[tuple[int, float]] = []
        for v in neigh:
            j = int(v)
            try:
                m_j = float(md.get(j, 0.0))
            except Exception:
                m_j = 0.0
            s = (self.lambda_phi * (_phi(j) - phi_i)) + (self.theta_mem * m_j)
            logits.append((j, s / self.tau))
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
                        v = self._pick_neighbor_scored(cur, neigh, connectome, maps)
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


__all__ = ["VoidRayScout"]