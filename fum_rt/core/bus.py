# bus.py
"""
Lock-free announcement bus for void-walker observations (ADC input).

Blueprint alignment:
- Walkers traverse with void equations and publish compact Observation packets.
- ADC consumes only these announcements to maintain territories/boundaries incrementally.
- Cost is proportional to number of announcements, not to graph size.

Usage
- Producer (connectome walkers):
    bus.publish(observation)
- Consumer (Nexus/ADC loop):
    batch = bus.drain(max_items=2048)

Behavior
- Bounded deque with overwrite-on-full semantics (drop oldest) to keep runtime stable.
"""

from __future__ import annotations
from collections import deque
from typing import Deque, List, Any, Optional


class AnnounceBus:
    """Bounded, overwrite-on-full FIFO for Observation events."""
    def __init__(self, capacity: int = 65536):
        self._q: Deque[Any] = deque(maxlen=int(max(1, capacity)))

    @property
    def capacity(self) -> int:
        return int(self._q.maxlen or 0)

    def size(self) -> int:
        return len(self._q)

    def publish(self, obs: Any) -> None:
        """
        Append an event; when full, the oldest is dropped automatically.
        This keeps the system stable under load without backpressure deadlocks.
        """
        self._q.append(obs)

    def drain(self, max_items: int = 2048) -> List[Any]:
        """
        Pop up to max_items from the left, returning them in arrival order.
        """
        n = min(int(max_items), len(self._q))
        out: List[Any] = []
        append = out.append
        for _ in range(n):
            append(self._q.popleft())
        return out

    def clear(self) -> None:
        self._q.clear()