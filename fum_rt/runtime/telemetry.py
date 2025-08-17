"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime telemetry packaging seam (Phase B).

Goals:
- Provide small, behavior-preserving builders for 'why' and 'status' payloads.
- Keep core numeric only; this module formats dicts but performs no logging or IO.
- Mirror existing Nexus packaging exactly to ensure byte-for-byte parity.

Policy:
- May import typing and stdlib only.
- No imports from io.* emitters; no file or JSON writes here.
"""

from typing import Any, Dict, Iterable, Set, Callable, Optional, Tuple, List
import os
import time

# --- Maps/frame quantization helpers (stdlib-only; no io.* imports) ---

import sys as _sys
import struct as _struct
from typing import Tuple as _Tuple


def _quantize_frame_v2_u8(header: Dict[str, Any], payload: bytes) -> _Tuple[Dict[str, Any], bytes]:
    """
    Convert a Float32 LE planar payload (heat|exc|inh) into u8 (frame.v2) using
    per-channel max from header["stats"]. No global scans; stats are computed
    upstream from bounded reducer working sets.

    Contract in:
      - header: dict with fields {"n", "channels", "dtype":"f32", "endianness":"LE", "stats":{ch:{max,...}}}
      - payload: bytes with 3*N float32 little-endian values back-to-back

    Contract out:
      - q_header: copy of header with:
          dtype="u8", ver="v2", quant="u8", endianness="LE" (kept for uniformity),
          scales: {ch: 255/max_ch if max_ch>0 else 0.0}
      - q_payload: bytes with 3*N uint8 values back-to-back
    """
    try:
        n = int(header.get("n", 0))
    except Exception:
        n = 0
    if n <= 0:
        return dict(header or {}), b""

    # Expect 3 channels in planar layout
    try:
        channels = list(header.get("channels", ["heat", "exc", "inh"]))
    except Exception:
        channels = ["heat", "exc", "inh"]
    if len(channels) != 3:
        # Fallback: assume 3 planar blocks regardless of names
        channels = ["heat", "exc", "inh"]

    expected_len = 3 * n * 4  # 3 blocks, float32
    if not isinstance(payload, (bytes, bytearray, memoryview)) or len(payload) < expected_len:
        # Malformed payload; return as-is
        return dict(header or {}), bytes(payload or b"")

    # Per-channel max from header (bounded working-set stats upstream)
    def _ch_max(name: str) -> float:
        try:
            return float(((header.get("stats") or {}).get(name) or {}).get("max", 0.0))
        except Exception:
            return 0.0

    max_heat = _ch_max("heat")
    max_exc = _ch_max("exc")
    max_inh = _ch_max("inh")

    s_heat = (255.0 / max_heat) if max_heat > 0.0 else 0.0
    s_exc = (255.0 / max_exc) if max_exc > 0.0 else 0.0
    s_inh = (255.0 / max_inh) if max_inh > 0.0 else 0.0

    mv = memoryview(payload)
    o0 = 0
    o1 = n * 4
    o2 = 2 * n * 4

    def _to_u8_block_le_f32(block: memoryview, count: int, scale: float) -> bytes:
        """
        Interpret block as little-endian float32 values and quantize to uint8 with clamping.
        Uses struct.iter_unpack to avoid NumPy dependency and respect endianness explicitly.
        """
        if scale <= 0.0 or count <= 0:
            return b"\x00" * max(0, count)
        # Fast path: if host is little-endian and struct supports buffer protocol efficiently
        it = _struct.iter_unpack("<f", block.tobytes())
        out = bytearray(count)
        i = 0
        for (v,) in it:
            if v <= 0.0:
                q = 0
            else:
                qf = v * scale
                if qf >= 255.0:
                    q = 255
                else:
                    # round-half-away-from-zero via +0.5 for positives
                    q = int(qf + 0.5)
            out[i] = q
            i += 1
            if i >= count:
                break
        # In case iter_unpack yielded fewer than count (should not happen), right-pad zeros
        if i < count:
            out.extend(b"\x00" * (count - i))
        return bytes(out)

    q_heat = _to_u8_block_le_f32(mv[o0:o1], n, s_heat)
    q_exc = _to_u8_block_le_f32(mv[o1:o2], n, s_exc)
    q_inh = _to_u8_block_le_f32(mv[o2:o2 + n * 4], n, s_inh)

    q_header = dict(header or {})
    q_header["dtype"] = "u8"
    q_header["ver"] = "v2"
    q_header["quant"] = "u8"
    # Keep endianness for uniformity in client code, though u8 is endianness-agnostic
    q_header["endianness"] = q_header.get("endianness", "LE")
    q_header["scales"] = {"heat": float(s_heat), "exc": float(s_exc), "inh": float(s_inh)}
    # Helpful size hint for clients
    q_header["payload_len"] = 3 * n  # bytes

    return q_header, (q_heat + q_exc + q_inh)

def _add_tiles_meta(header: Dict[str, Any], tile_cfg: str) -> Dict[str, Any]:
    """
    Inject non-invasive tiling metadata into a frame.v2 header without modifying payload bytes.
    This enables clients to interpret planar u8 payloads in tiles for large-N visualization.

    tile_cfg (case-insensitive):
      - "none"|"off"|"false"|"0": no tiles (no-op)
      - "auto": choose a square tile size targeting ~64x64 where possible
      - "<W>x<H>": explicit tile width/height (e.g., "64x64")
      - "<K>": square tile KxK (e.g., "128")

    Header additions:
      header["tiles"] = {
        "size": [tw, th],
        "grid": [gw, gh],       # number of tiles in x (width), y (height) directions
        "order": "row-major",   # tile order
        "layout": "planar",     # channel layout (heat|exc|inh planar blocks)
        "shape": [H, W],        # 2D shape of the frame
        "padded": max(0, H*W - n),
      }
    """
    try:
        cfg = str(tile_cfg or "").strip().lower()
    except Exception:
        cfg = "none"
    if cfg in ("none", "off", "false", "0", ""):
        return header

    try:
        shape = list(header.get("shape", []))
        if not (isinstance(shape, (list, tuple)) and len(shape) == 2):
            # Fallback to square from 'n' if shape missing
            n = int(header.get("n", 0))
            side = int(max(1, int((n or 1) ** 0.5)))
            H = side
            W = side
        else:
            H = int(shape[0])
            W = int(shape[1])
    except Exception:
        n = int(header.get("n", 0))
        side = int(max(1, int((n or 1) ** 0.5)))
        H = side
        W = side

    def _parse_tile(cfg_str: str) -> tuple[int, int]:
        # explicit WxH
        if "x" in cfg_str:
            parts = cfg_str.lower().split("x")
            try:
                tw = int(parts[0].strip())
                th = int(parts[1].strip())
                return max(1, tw), max(1, th)
            except Exception:
                pass
        # single integer
        try:
            k = int(cfg_str)
            return max(1, k), max(1, k)
        except Exception:
            pass
        # auto default
        # Aim for ~64x64 tiles, but constrain by frame dims
        tw = min(W, 64 if W >= 64 else max(8, W))
        th = min(H, 64 if H >= 64 else max(8, H))
        return max(1, tw), max(1, th)

    tw, th = (0, 0)
    if cfg == "auto":
        tw, th = _parse_tile(cfg)
    else:
        tw, th = _parse_tile(cfg)

    # Clamp to frame dimensions
    tw = max(1, min(tw, W))
    th = max(1, min(th, H))

    # Compute grid (tiles across width, height)
    def _ceil_div(a: int, b: int) -> int:
        return (a + b - 1) // b

    gw = _ceil_div(W, tw)
    gh = _ceil_div(H, th)

    n = int(header.get("n", 0))
    padded = max(0, (H * W) - n)

    out = dict(header or {})
    out["tiles"] = {
        "size": [int(tw), int(th)],
        "grid": [int(gw), int(gh)],
        "order": "row-major",
        "layout": "planar",
        "shape": [int(H), int(W)],
        "padded": int(padded),
    }
    # Ensure ver/dtype/quant are consistent for frame.v2 u8
    out["ver"] = out.get("ver", "v2")
    out["dtype"] = out.get("dtype", "u8")
    out["quant"] = out.get("quant", "u8")
    return out

def macro_why_base(nx: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Build the base 'why' dict used for macro emissions (before any caller-specific fields).
    Mirrors the inline block in Nexus: uses current metrics with explicit numeric casts.

    Caller may extend with additional telemetry fields, e.g. novelty_idf, composer_idf_k.
    """
    m = metrics or {}
    try:
        phase = int(getattr(nx, "_phase", {}).get("phase", 0))
    except Exception:
        try:
            phase = int(m.get("phase", 0))
        except Exception:
            phase = 0

    return {
        "t": int(step),
        "phase": phase,
        "b1_z": float(m.get("b1_z", 0.0)),
        "cohesion_components": int(m.get("cohesion_components", 0)),
        "vt_coverage": float(m.get("vt_coverage", 0.0)),
        "vt_entropy": float(m.get("vt_entropy", 0.0)),
        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
        "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0))),
    }


def status_payload(nx: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Build the open UTD status payload.
    Mirrors the inline block from Nexus with identical keys and casts.
    """
    m = metrics or {}
    try:
        phase = int(m.get("phase", int(getattr(nx, "_phase", {}).get("phase", 0))))
    except Exception:
        phase = 0

    return {
        "type": "status",
        "t": int(step),
        "neurons": int(getattr(nx, "N", 0)),
        "phase": phase,
        "cohesion_components": int(m.get("cohesion_components", 0)),
        "vt_coverage": float(m.get("vt_coverage", 0.0)),
        "vt_entropy": float(m.get("vt_entropy", 0.0)),
        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
        "active_edges": int(m.get("active_edges", 0)),
        "homeostasis_pruned": int(m.get("homeostasis_pruned", 0)),
        "homeostasis_bridged": int(m.get("homeostasis_bridged", 0)),
        "b1_z": float(m.get("b1_z", 0.0)),
        "adc_territories": int(m.get("adc_territories", 0)),
        "adc_boundaries": int(m.get("adc_boundaries", 0)),
        "sie_total_reward": float(m.get("sie_total_reward", 0.0)),
        "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
        "sie_v2_reward_mean": float(m.get("sie_v2_reward_mean", 0.0)),
        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", 0.0)),
        "ute_in_count": int(m.get("ute_in_count", 0)),
        "ute_text_count": int(m.get("ute_text_count", 0)),
    }


# --- Tick Telemetry Fold (bus drain + ADC + optional event-driven metrics + B1) ---

class _DynObs:
    """
    Minimal observation object for publishing runtime 'delta' events to the bus
    without importing core.announce.Observation. Adapter reads via getattr().
    """
    __slots__ = ("tick", "kind", "nodes", "meta")

    def __init__(self, tick: int, kind: str, nodes: Optional[Iterable[int]] = None, meta: Optional[Dict[str, Any]] = None) -> None:
        self.tick = int(tick)
        self.kind = str(kind)
        self.nodes = list(nodes or [])
        self.meta = dict(meta or {})

class _MapsObs:
    """
    Lightweight maps/frame observation for UI consumption.

    Contract:
      - kind: 'maps_frame'
      - header: dict with fields {topic, tick, n, shape, channels, dtype, endianness, stats}
      - payload: bytes containing Float32Array blocks back-to-back (LE): heat[n] | exc[n] | inh[n]
    """
    __slots__ = ("tick", "kind", "header", "payload")

    def __init__(self, tick: int, header: Dict[str, Any], payload: bytes) -> None:
        self.tick = int(tick)
        self.kind = "maps_frame"
        self.header = dict(header or {})
        self.payload = payload


def tick_fold(
    nx: Any,
    metrics: Dict[str, Any],
    drive: Dict[str, Any],
    td_signal: float,
    step: int,
    tick_rev_map: Optional[Dict[int, Any]] = None,
    *,
    obs_to_events: Optional[Callable[[Iterable[Any]], Iterable[Any]]] = None,
    adc_event: Optional[Callable[[Dict[str, Any], int], Any]] = None,
    apply_b1: Optional[Callable[[Any, Dict[str, Any], int], Dict[str, Any]]] = None,
) -> Tuple[Dict[str, Any], Set[Any]]:
    """
    Behavior-preserving fold of per-tick runtime telemetry:
      - Optionally publish a 'delta' event (feature-flagged) to the announce bus
      - Drain bus and derive void-topic symbols using tick_rev_map
      - Update ADC from drained observations; merge adc metrics
      - Optionally fold event-driven metrics (feature-flagged)
      - Update complexity proxy and apply B1 detector (via callback)
    Returns (metrics, void_topic_symbols)
    """
    m = metrics if isinstance(metrics, dict) else {}
    void_topic_symbols: Set[Any] = set()

    # 1) Optional delta event publish (telemetry-only; no dynamics change)
    try:
        if getattr(nx, "_evt_metrics", None) is not None:
            comps = {}
            try:
                comps = dict(drive.get("components", {}) or {})
            except Exception:
                comps = {}
            meta = {
                "b1": 0.0,  # cycle_hit provides primary b1 contributions; keep delta neutral
                "nov": float(comps.get("nov", 0.0)) if isinstance(comps, dict) else 0.0,
                "hab": float(comps.get("hab", 0.0)) if isinstance(comps, dict) else 0.0,
                "td": float(td_signal),
                "hsi": float(comps.get("hsi", 0.0)) if isinstance(comps, dict) else 0.0,
            }
            try:
                bus = getattr(nx, "bus", None)
                if bus is not None:
                    # Publish neutral 'delta' for b1/why folding
                    bus.publish(_DynObs(tick=int(step), kind="delta", nodes=[], meta=meta))
                    # Optionally synthesize bounded ΔW events to drive Exc/Inh maps without scans
                    try:
                        synth_flag = str(os.getenv("SYNTH_DELTA_W", "0")).strip().lower() in ("1", "true", "yes", "on", "y")
                    except Exception:
                        synth_flag = False
                    if synth_flag:
                        # Select a tiny working set of nodes from this tick's symbol→index map (bounded fan-out)
                        try:
                            if isinstance(tick_rev_map, dict):
                                node_keys = list(tick_rev_map.keys())
                            else:
                                node_keys = []
                        except Exception:
                            node_keys = []
                        # Keep at most 16 nodes; prefer stable order
                        try:
                            nodes_sel = [int(i) for i in sorted(node_keys)[:16]]
                        except Exception:
                            nodes_sel = []
                        # Map TD sign to ΔW direction; clip magnitude to avoid runaway (void-faithful bounded emit)
                        try:
                            tdv = float(td_signal)
                        except Exception:
                            tdv = 0.0
                        sign = 1.0 if tdv >= 0.0 else -1.0
                        mag = min(0.05, abs(tdv))  # 0 ≤ |dw| ≤ 0.05
                        dw_val = float(sign * mag)
                        if nodes_sel:
                            bus.publish(_DynObs(tick=int(step), kind="delta_w", nodes=nodes_sel, meta={"dw": dw_val}))
            except Exception:
                pass
    except Exception:
        pass

    # 2) Drain bus, derive topic symbols, update ADC, and fold event-driven metrics
    try:
        bus = getattr(nx, "bus", None)
        if bus is not None:
            obs_batch = bus.drain(max_items=int(getattr(nx, "bus_drain", 2048)))
            if obs_batch:
                # Expose drained observations for CoreEngine folding without re-drain
                try:
                    setattr(nx, "_last_obs_batch", obs_batch)
                except Exception:
                    pass
                # Map observed node indices back to symbols seen this tick
                try:
                    if isinstance(tick_rev_map, dict):
                        for obs in obs_batch:
                            try:
                                nodes = getattr(obs, "nodes", None)
                                if nodes:
                                    for idx in nodes:
                                        sym = tick_rev_map.get(int(idx))
                                        if sym is not None:
                                            void_topic_symbols.add(sym)
                            except Exception:
                                continue
                except Exception:
                    pass

                # Update ADC after extracting topic so we don't interfere with its logic
                try:
                    adc = getattr(nx, "adc", None)
                    if adc is not None:
                        adc.update_from(obs_batch)
                        adc_metrics = adc.get_metrics()
                    else:
                        adc_metrics = {}
                except Exception:
                    adc_metrics = {}
                # Expose ADC metrics for CoreEngine folding (no IO; runtime-local state only)
                try:
                    setattr(nx, "_last_adc_metrics", adc_metrics)
                except Exception:
                    pass

                # Optionally fold event-driven metrics telemetry
                try:
                    evtm = getattr(nx, "_evt_metrics", None)
                    if getattr(nx, "_engine", None) is None and evtm is not None:
                        if obs_to_events is not None:
                            try:
                                for _ev in obs_to_events(obs_batch) or []:
                                    try:
                                        evtm.update(_ev)
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                        if adc_event is not None:
                            try:
                                evtm.update(adc_event(adc_metrics, t=int(step)))
                            except Exception:
                                pass
                        try:
                            evsnap = evtm.snapshot()
                            if isinstance(evsnap, dict):
                                # Do not override legacy scan-based metrics; prefix event-driven keys.
                                for _k, _v in evsnap.items():
                                    try:
                                        # Preserve existing B1 detector outputs from apply_b1
                                        if str(_k).startswith("b1_") and _k in m:
                                            continue
                                        m[f"evt_{_k}"] = _v
                                    except Exception:
                                        continue
                        except Exception:
                            pass
                except Exception:
                    pass

                # Fold ADC metrics and complexity proxy
                try:
                    if isinstance(adc_metrics, dict):
                        m.update(adc_metrics)
                        m["complexity_cycles"] = float(m.get("complexity_cycles", 0.0)) + float(adc_metrics.get("adc_cycle_hits", 0.0))
                except Exception:
                    pass
    except Exception:
        pass

    # 2.9) Publish maps/frame (header+binary) if prepared by CoreEngine
    try:
        mf = getattr(nx, "_maps_frame_ready", None)
        if mf is not None and isinstance(mf, tuple) and len(mf) == 2:
            header, payload = mf

            # Ensure header has topic and tick without scanning arrays client-side
            try:
                if isinstance(header, dict):
                    if "topic" not in header:
                        header = dict(header)
                        header["topic"] = "maps/frame"
                    header["tick"] = int(step)
                else:
                    header = {"topic": "maps/frame", "tick": int(step)}
            except Exception:
                header = {"topic": "maps/frame", "tick": int(step)}

            # 2.9.a) Publish to bus for in-process consumers (unchanged)
            try:
                bus = getattr(nx, "bus", None)
            except Exception:
                bus = None
            if bus is not None:
                try:
                    bus.publish(_MapsObs(tick=int(step), header=header, payload=payload))
                except Exception:
                    pass

            # 2.9.b) Optional ring write with u8 quantization (frame.v2) and FPS limiter
            try:
                # FPS limiter (default: 10)
                try:
                    maps_fps = float(os.getenv("MAPS_FPS", "10"))
                except Exception:
                    maps_fps = 10.0
                now_ts = time.time()
                last_ts = float(getattr(nx, "_maps_last_emit_ts", 0.0))
                allow_emit = (maps_fps <= 0) or ((now_ts - last_ts) >= (1.0 / max(0.001, maps_fps)))

                if allow_emit:
                    mode = str(os.getenv("MAPS_MODE", "frame_v2_u8")).strip().lower()
                    tile_cfg = str(os.getenv("MAPS_TILE", "none")).strip().lower()

                    # Lazy-init ring if absent
                    ring = getattr(nx, "_maps_ring", None)
                    if ring is None:
                        try:
                            from fum_rt.io.visualization.maps_ring import MapsRing  # local import to avoid module-policy drift
                            cap = int(os.getenv("MAPS_RING", "3"))
                            nx._maps_ring = MapsRing(capacity=max(1, cap))
                            ring = nx._maps_ring
                        except Exception:
                            ring = None

                    if ring is not None:
                        # Only full-frame v2 for now; tiles reserved for very large N (stub)
                        if mode in ("frame_v2", "frame_v2_u8", "v2", "u8"):
                            # Quantize to u8 using per-channel max from header['stats']
                            q_header, q_payload = _quantize_frame_v2_u8(header, payload)
                            # Optional tile metadata (payload remains planar u8; clients may tile client-side)
                            try:
                                if tile_cfg not in ("none", "off", "false", "0", ""):
                                    q_header = _add_tiles_meta(q_header, tile_cfg)
                            except Exception:
                                pass
                            try:
                                ring.push(int(step), q_header, q_payload)
                                setattr(nx, "_maps_last_emit_ts", now_ts)
                            except Exception:
                                pass
                        elif mode in ("off", "none"):
                            # Skip ring write
                            pass
                        else:
                            # Unknown mode: default to frame_v2_u8
                            q_header, q_payload = _quantize_frame_v2_u8(header, payload)
                            # Apply tile metadata if requested
                            try:
                                if tile_cfg not in ("none", "off", "false", "0", ""):
                                    q_header = _add_tiles_meta(q_header, tile_cfg)
                            except Exception:
                                pass
                            try:
                                ring.push(int(step), q_header, q_payload)
                                setattr(nx, "_maps_last_emit_ts", now_ts)
                            except Exception:
                                pass
            except Exception:
                pass

            # Clear pointer to avoid re-publishing stale frames
            try:
                delattr(nx, "_maps_frame_ready")
            except Exception:
                pass
    except Exception:
        pass

    # 2.10) Expose dimensionless memory steering groups (telemetry-only; void-faithful)
    try:
        mf = getattr(nx, "_memory_field", None)
        if mf is not None:
            try:
                theta = float(getattr(mf, "Theta", 0.0))
            except Exception:
                theta = 0.0
            try:
                da = float(getattr(mf, "D_a", getattr(mf, "Da", 0.0)))
            except Exception:
                da = 0.0
            try:
                lam = float(getattr(mf, "Lambda", 0.0))
            except Exception:
                lam = 0.0
            try:
                gam = float(getattr(mf, "Gamma", 0.0))
            except Exception:
                gam = 0.0
            # Do not overwrite if caller already provided these
            if "mem_Theta" not in m:
                m["mem_Theta"] = theta
            if "mem_Da" not in m:
                m["mem_Da"] = da
            if "mem_Lambda" not in m:
                m["mem_Lambda"] = lam
            if "mem_Gamma" not in m:
                m["mem_Gamma"] = gam
    except Exception:
        pass

    # 3) Apply B1 detector via provided seam (preserves detector parameters and gating)
    try:
        if apply_b1 is not None:
            m = apply_b1(nx, m, int(step))
    except Exception:
        pass

    return m, void_topic_symbols

__all__ = ["macro_why_base", "status_payload", "tick_fold"]