"""
Redis publishing helpers (optional, bounded, void-faithful).

- Publishes status metrics and/or latest maps/frame from the in-process ring to Redis Streams.
- No schedulers or background threads here; caller invokes once per tick from the runtime loop.
- Uses MAXLEN trimming to keep Redis bounded (drop-oldest), mirroring in-memory ring semantics.

Enable via env:
  REDIS_URL=redis://127.0.0.1:6379/0
  ENABLE_REDIS_STATUS=1
  ENABLE_REDIS_MAPS=1
  REDIS_STREAM_STATUS=fum:status         (optional; default shown)
  REDIS_STREAM_MAPS=fum:maps             (optional; default shown)
  REDIS_STATUS_MAXLEN=2000               (approximate trim)
  REDIS_MAPS_MAXLEN=3                    (approximate trim)
"""

from __future__ import annotations

from typing import Any, Dict, Optional
import os
import json

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None  # lazy-fail if missing


def _truthy(x: Any) -> bool:
    try:
        if isinstance(x, (int, float, bool)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False


def _get_client(nx: Any) -> Optional["redis.Redis"]:
    """
    Lazy-initialize and cache a Redis client on nx._redis_client.
    Returns None if redis-py is unavailable or the URL/env is missing.
    """
    if redis is None:
        return None
    try:
        cli = getattr(nx, "_redis_client", None)
        if cli is not None:
            return cli
    except Exception:
        cli = None
    try:
        url = os.getenv("REDIS_URL", "").strip()
        if not url:
            return None
        cli = redis.from_url(url, decode_responses=False)  # keep bytes payloads raw
        setattr(nx, "_redis_client", cli)
        return cli
    except Exception:
        return None


def maybe_publish_status_redis(nx: Any, metrics: Dict[str, Any], step: int) -> None:
    """
    Publish a compact status JSON to a bounded Redis Stream once per tick.

    Fields:
      stream = REDIS_STREAM_STATUS (default 'fum:status')
      MAXLEN  = REDIS_STATUS_MAXLEN (default 2000, approximate)
      entry   = { 'json': b'{"type":"status",...}' }
    """
    try:
        if not _truthy(os.getenv("ENABLE_REDIS_STATUS", "0")):
            return
        cli = _get_client(nx)
        if cli is None:
            return
        stream = os.getenv("REDIS_STREAM_STATUS", "fum:status")
        try:
            maxlen = int(os.getenv("REDIS_STATUS_MAXLEN", "2000"))
        except Exception:
            maxlen = 2000

        # Select a compact subset to keep bandwidth low
        m = metrics or {}
        payload = {
            "type": "status",
            "t": int(step),
            "phase": int(m.get("phase", 0)),
            "neurons": int(getattr(nx, "N", 0)),
            "b1_z": float(m.get("b1_z", 0.0)),
            "cohesion_components": int(m.get("cohesion_components", 0)),
            "vt_entropy": float(m.get("vt_entropy", 0.0)),
            "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
            "sie_v2_valence_01": float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0))),
        }
        js = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        cli.xadd(stream, {"json": js}, maxlen=maxlen, approximate=True)
    except Exception:
        # Never disrupt runtime parity
        pass


def maybe_publish_maps_redis(nx: Any, step: int) -> None:
    """
    Publish the latest maps/frame (u8 preferred) to a bounded Redis Stream once per tick.

    - Reads the newest frame from nx._maps_ring (if present).
    - Skips if no new frame (seq unchanged).
    - Writes XADD with MAXLEN ~ REDIS_MAPS_MAXLEN (default 3) to keep memory bounded.
    - Fields: { 'header': b'{"tick":...}', 'payload': <raw-bytes> }
    """
    try:
        if not _truthy(os.getenv("ENABLE_REDIS_MAPS", "0")):
            return
        cli = _get_client(nx)
        if cli is None:
            return
        ring = getattr(nx, "_maps_ring", None)
        if ring is None:
            return
        fr = ring.latest()
        if fr is None:
            return

        # Skip if we've already published this seq
        try:
            last_seq = int(getattr(nx, "_maps_last_seq_redis", 0))
        except Exception:
            last_seq = 0
        if getattr(fr, "seq", 0) == last_seq:
            return

        stream = os.getenv("REDIS_STREAM_MAPS", "fum:maps")
        try:
            maxlen = int(os.getenv("REDIS_MAPS_MAXLEN", "3"))
        except Exception:
            maxlen = 3

        # Serialize header compactly; payload is raw bytes (u8 preferred)
        try:
            hdr_text = json.dumps(fr.header, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        except Exception:
            hdr_text = json.dumps({"topic": "maps/frame", "tick": int(getattr(fr, "tick", step))}, separators=(",", ":")).encode("utf-8")

        payload_bytes = bytes(getattr(fr, "payload", b"") or b"")
        cli.xadd(stream, {"header": hdr_text, "payload": payload_bytes}, maxlen=maxlen, approximate=True)

        # Mark as published
        try:
            setattr(nx, "_maps_last_seq_redis", int(getattr(fr, "seq", 0)))
        except Exception:
            pass
    except Exception:
        # Never disrupt runtime parity
        pass


__all__ = ["maybe_publish_status_redis", "maybe_publish_maps_redis"]