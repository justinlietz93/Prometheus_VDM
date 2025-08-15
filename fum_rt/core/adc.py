# adc.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Active Domain Cartography (ADC) — incremental, void-faithful reducer.

Design
- ADC consumes compact Observation events from the void-walker announcement bus.
- It never inspects raw W or dense adjacency; all inputs are announcements.
- Territories and boundaries are updated locally per event (O(1) per event).
- Provides lightweight map metrics for Nexus logging and self-speak decisions.

Territories
- Coarse "concept regions" indexed by a composite key (domain_hint, coverage_id).
- Each territory tracks EWMA stats (w_mean/var, s_mean), a mass (support), a confidence,
  and a TTL (decays unless reinforced).

Boundaries
- Abstract edges between territories tracking cut_strength EWMA, churn, and TTL.

Events
- region_stat: assimilation into a nearest territory (or create).
- boundary_probe: update boundary signal (if 2+ territories exist).
- cycle_hit: bumps a cycle counter (B1 proxy) surfaced in map metrics.
- novel_frontier: creates/boosts a new/sibling territory with low initial confidence.

This is a minimal, safe baseline. You can evolve the territory identity function
from (domain_hint, coverage_id) to a learned centroid distance when you add one.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional, Iterable
import math
from .announce import Observation


@dataclass
class _EWMA:
    """Numerically stable EWMA with alpha in (0,1]."""
    alpha: float
    mean: float = 0.0
    var: float = 0.0
    init: bool = False

    def update(self, x: float):
        a = self.alpha
        if not self.init:
            self.mean = float(x)
            self.var = 0.0
            self.init = True
            return
        # Welford-style EMA
        delta = float(x) - self.mean
        self.mean += a * delta
        self.var = (1 - a) * (self.var + a * delta * delta)


@dataclass
class Territory:
    key: Tuple[str, int]  # (domain_hint, coverage_id)
    id: int
    mass: float = 0.0
    conf: float = 0.0
    ttl: int = 120
    w_stats: _EWMA = field(default_factory=lambda: _EWMA(alpha=0.15))
    s_stats: _EWMA = field(default_factory=lambda: _EWMA(alpha=0.15))

    def reinforce(self, w_mean: float, s_mean: float, add_mass: float, add_conf: float, ttl_init: int):
        self.w_stats.update(w_mean)
        self.s_stats.update(s_mean)
        self.mass += max(0.0, add_mass)
        self.conf = min(1.0, self.conf + max(0.0, add_conf))
        self.ttl = max(self.ttl, int(ttl_init))


@dataclass
class Boundary:
    a: int
    b: int
    cut_stats: _EWMA = field(default_factory=lambda: _EWMA(alpha=0.2))
    churn: _EWMA = field(default_factory=lambda: _EWMA(alpha=0.2))
    ttl: int = 120

    def reinforce(self, cut_strength: float, ttl_init: int):
        prev = float(self.cut_stats.mean) if self.cut_stats.init else 0.0
        self.cut_stats.update(cut_strength)
        self.churn.update(abs(float(self.cut_stats.mean) - prev))
        self.ttl = max(self.ttl, int(ttl_init))


class ADC:
    def __init__(self, r_attach: float = 0.25, ttl_init: int = 120, split_patience: int = 6):
        self.r_attach = float(r_attach)
        self.ttl_init = int(max(1, ttl_init))
        self.split_patience = int(max(1, split_patience))

        self._territories: Dict[Tuple[str, int], Territory] = {}
        self._id_seq: int = 1
        self._boundaries: Dict[Tuple[int, int], Boundary] = {}
        self._frontier_counter: Dict[Tuple[str, int], int] = {}
        self._cycle_events: int = 0  # accumulated since last metrics call

    # --- Public API ---

    def update_from(self, observations: Iterable[Observation]) -> None:
        for o in observations:
            kind = getattr(o, "kind", "")
            if kind == "region_stat":
                self._accumulate_region(o)
            elif kind == "boundary_probe":
                self._accumulate_boundary(o)
            elif kind == "cycle_hit":
                self._note_cycle(o)
            elif kind == "novel_frontier":
                self._note_frontier(o)
        self._decay()

    def get_metrics(self) -> Dict[str, float]:
        """Return a small metrics dict and reset transient counters."""
        terr_count = len(self._territories)
        bnd_count = len(self._boundaries)
        cycles = self._cycle_events
        self._cycle_events = 0
        return {
            "adc_territories": int(terr_count),
            "adc_boundaries": int(bnd_count),
            "adc_cycle_hits": int(cycles),
        }

    # --- Internals ---

    def _territory_for(self, domain_hint: str, cov_id: int) -> Territory:
        key = (str(domain_hint or ""), int(cov_id))
        t = self._territories.get(key)
        if t is None:
            t = Territory(key=key, id=self._id_seq, ttl=self.ttl_init)
            self._id_seq += 1
            self._territories[key] = t
        return t

    def _accumulate_region(self, o: Observation):
        t = self._territory_for(o.domain_hint, o.coverage_id)
        # Attach if "close": here closeness is discretized by coverage bin match via key.
        # When you add a real centroid, use a distance threshold compared to r_attach.
        add_mass = max(1.0, float(len(o.nodes)))
        add_conf = 0.02
        t.reinforce(w_mean=float(o.w_mean), s_mean=float(o.s_mean),
                    add_mass=add_mass, add_conf=add_conf, ttl_init=self.ttl_init)

    def _accumulate_boundary(self, o: Observation):
        # Pick two "closest" territories by coverage bin neighborhood:
        # Here we approximate by choosing (domain_hint, cov_id) and (domain_hint, cov_id±1)
        t1 = self._territory_for(o.domain_hint, o.coverage_id)
        # neighbor bin
        neighbor_cov = int(max(0, min(9, int(o.coverage_id + (1 if (o.coverage_id % 2 == 0) else -1)))))
        t2 = self._territory_for(o.domain_hint, neighbor_cov)
        a, b = (t1.id, t2.id) if t1.id < t2.id else (t2.id, t1.id)
        key = (a, b)
        bnd = self._boundaries.get(key)
        if bnd is None:
            bnd = Boundary(a=a, b=b, ttl=self.ttl_init)
            self._boundaries[key] = bnd
        bnd.reinforce(float(o.cut_strength), ttl_init=self.ttl_init)

    def _note_cycle(self, o: Observation):
        self._cycle_events += 1
        # Optionally: attach cycles to a territory using coverage bin
        t = self._territory_for(o.domain_hint, o.coverage_id)
        t.conf = min(1.0, t.conf + 0.01)
        t.ttl = max(t.ttl, self.ttl_init)

    def _note_frontier(self, o: Observation):
        key = (str(o.domain_hint or ""), int(o.coverage_id))
        cnt = self._frontier_counter.get(key, 0) + 1
        self._frontier_counter[key] = cnt
        if cnt >= self.split_patience:
            # Create or boost a new sibling territory by nudging coverage bin
            sib_cov = int(max(0, min(9, int(o.coverage_id + 1))))
            sib = self._territory_for(o.domain_hint, sib_cov)
            sib.reinforce(w_mean=float(o.w_mean), s_mean=float(o.s_mean),
                          add_mass=max(1.0, float(len(o.nodes))), add_conf=0.05, ttl_init=self.ttl_init)
            self._frontier_counter[key] = 0

    def _decay(self):
        # TTL decay and garbage collection for stale items with low confidence/mass
        drop_terr = []
        for key, t in self._territories.items():
            t.ttl -= 1
            if t.ttl <= 0 and (t.conf < 0.05 or t.mass < 5.0):
                drop_terr.append(key)
        for key in drop_terr:
            self._territories.pop(key, None)

        drop_bnd = []
        for key, b in self._boundaries.items():
            b.ttl -= 1
            if b.ttl <= 0 and (not b.cut_stats.init or b.cut_stats.mean < 1e-4):
                drop_bnd.append(key)
        for key in drop_bnd:
            self._boundaries.pop(key, None)