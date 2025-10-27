"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Maps frames ring buffer (drop-oldest, thread-safe, void-faithful).

Canonical location: fum_rt.io.visualization.maps_ring

Purpose
- Provide a tiny, bounded ring for maps frames (header+payload) with drop-oldest semantics.
- Decouples producers (telemetry/core engine) from consumers (UI/websocket) without scans.
- O(1) amortized operations; no full-buffer copies; copies only payload bytes as provided.

Contract
- Frame header schema is producer-defined; commonly:
  {topic, ver?, tick, n, shape, channels, dtype, endianness, stats, ...}
- Payload is a bytes-like buffer; typically planar blocks (e.g., Float32 LE: heat|exc|inh).

Usage
- nx._maps_ring = MapsRing(capacity=int(os.getenv("MAPS_RING", 3)))
- Producer: nx._maps_ring.push(tick, header, payload)
- Consumer: ring.latest(), ring.drain(max_items)

Security / Backpressure
- Always drops the oldest on overflow.
- Readers can choose to read only latest() to avoid client backlog.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import threading


@dataclass(frozen=True)
class MapsFrame:
    tick: int
    header: Dict[str, Any]
    payload: bytes
    seq: int  # monotonically increasing sequence id


class MapsRing:
    """
    Bounded, thread-safe ring buffer for maps frames.

    - push(): appends a frame, dropping the oldest when at capacity.
    - latest(): returns the newest frame or None.
    - drain(max_items): returns up to max_items frames from oldest to newest.
      Use latest() if you only need the most recent frame to minimize bandwidth.
    """

    __slots__ = ("capacity", "_lock", "_buf", "_seq", "_drop_count")

    def __init__(self, capacity: int = 3) -> None:
        self.capacity = max(1, int(capacity))
        self._lock = threading.Lock()
        self._buf: List[MapsFrame] = []
        self._seq = 0
        self._drop_count = 0

    def push(self, tick: int, header: Dict[str, Any], payload: bytes) -> int:
        """
        Append a frame; drop oldest on overflow.
        Returns the sequence id assigned to the inserted frame.
        """
        if not isinstance(payload, (bytes, bytearray, memoryview)):
            # Normalize to bytes once (producers should pass bytes already)
            try:
                payload = bytes(payload)  # type: ignore[assignment]
            except Exception:
                payload = b""
        with self._lock:
            self._seq += 1
            f = MapsFrame(tick=int(tick), header=dict(header or {}), payload=bytes(payload), seq=self._seq)
            if len(self._buf) >= self.capacity:
                self._buf.pop(0)
                self._drop_count += 1
            self._buf.append(f)
            return f.seq

    def latest(self) -> Optional[MapsFrame]:
        with self._lock:
            if not self._buf:
                return None
            return self._buf[-1]

    def drain(self, max_items: Optional[int] = None) -> List[MapsFrame]:
        """
        Return up to max_items frames in order (oldest..newest).
        Does not mutate the ring (non-destructive view); consumers should track seq.
        """
        with self._lock:
            if not self._buf:
                return []
            if max_items is None or max_items <= 0:
                return list(self._buf)
            return list(self._buf[-int(max_items):])

    def size(self) -> int:
        with self._lock:
            return len(self._buf)

    def dropped(self) -> int:
        """
        Returns the number of frames dropped due to overflow since creation.
        """
        with self._lock:
            return int(self._drop_count)

    def __len__(self) -> int:
        return self.size()


__all__ = ["MapsRing", "MapsFrame"]