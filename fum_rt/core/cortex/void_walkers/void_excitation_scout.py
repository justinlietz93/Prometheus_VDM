from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_excitation_scout

ExcitationScout (read-only, void-faithful):
- Duty: Map excitatory corridors, feeding ExcitationMap strictly via events.
- Strategy: Seed from ExcitationMap.exc_head; during walk, emit VTTouchEvent per visit and
            synthesize SpikeEvent(node, amp≈local_exc, sign=+1) with bounded amplitude in [0,1].
            Occasional EdgeOnEvent samples are produced by BaseScout's bounded walk; no global scans.
- No scans of global structures; uses local neighbor reads and bounded TTL/budgets.

Physics alignment (docs in /derivation):
- finite_tube_mode_analysis.md, discrete_to_continuum.md: fast φ-fronts (c^2 = 2 J a^2) guide recent activity.
- memory_steering.md: scouts do not write; they only observe and announce, keeping the φ sector void-faithful.
"""

from typing import Any, Dict, List, Optional, Set

from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent, SpikeEvent


def _head_lookup(maps: Optional[Dict[str, Any]], key: str, cap: int = 512) -> Dict[int, float]:
    """
    Build a bounded lookup {node: norm_score in [0,1]} from a head list [[node, score], ...].
    Normalization: divide by max(score) over the truncated head; empty -> {}.
    """
    if not isinstance(maps, dict):
        return {}
    try:
        head = maps.get(key, []) or []
        head = head[: cap]
        pairs: List[tuple[int, float]] = []
        for pair in head:
            try:
                n = int(pair[0])
                s = float(pair[1]) if len(pair) > 1 else 1.0
            except Exception:
                continue
            if n >= 0:
                pairs.append((n, s))
        if not pairs:
            return {}
        vmax = max(s for _, s in pairs) or 1.0
        return {n: max(0.0, min(1.0, s / vmax)) for (n, s) in pairs}
    except Exception:
        return {}


def _extract_head_nodes(maps: Optional[Dict[str, Any]], key: str, cap: int = 512) -> Set[int]:
    """
    Extract bounded set of node ids from a head list [[node, score], ...].
    """
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


class ExcitationScout(BaseScout):
    """
    Excitation-driven scout: routes toward nodes with higher ExcitationMap scores.
    Adds SpikeEvent(sign=+1) upon each vt_touch visit with amplitude ~ local excitation.
    """

    __slots__ = ()

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer ExcitationMap head indices
        return _extract_head_nodes(maps, "exc_head", cap=max(64, self.budget_visits * 8))

    def step(
        self,
        connectome: Any,
        bus: Any = None,
        maps: Optional[Dict[str, Any]] = None,
        budget: Optional[Dict[str, int]] = None,
    ) -> List[BaseEvent]:
        # Use BaseScout bounded walk to generate vt_touch and edge_on
        base_events = super().step(connectome, bus=bus, maps=maps, budget=budget)

        # Build local excitation amplitude lookup from snapshot head (bounded, read-only)
        exc_lookup = _head_lookup(maps, "exc_head", cap=max(64, self.budget_visits * 8))

        out: List[BaseEvent] = []
        for e in base_events:
            out.append(e)
            if getattr(e, "kind", None) == "vt_touch":
                token = getattr(e, "token", None)
                try:
                    node = int(token)
                except Exception:
                    node = None
                if node is not None and node >= 0:
                    # Amplitude in [0,1]; default to 0.5 when not found
                    amp = float(exc_lookup.get(node, 0.5))
                    out.append(SpikeEvent(kind="spike", t=getattr(e, "t", None), node=node, amp=amp, sign=+1))
        return out


__all__ = ["ExcitationScout"]
