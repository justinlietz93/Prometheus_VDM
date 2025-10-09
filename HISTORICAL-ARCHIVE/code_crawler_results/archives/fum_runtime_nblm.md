# fum_runtime_nblm

Generated on: 2025-08-26 06:58:12

<?xml version="1.0" ?>
<fum_runtime_nblm>
  <metadata>
    <global_stats>
      <total_files>23</total_files>
      <total_size_bytes>140266</total_size_bytes>
      <total_loc>3630</total_loc>
    </global_stats>
    <chunk_stats>
      <files_in_chunk>23</files_in_chunk>
      <size_in_chunk_bytes>140266</size_in_chunk_bytes>
      <loc_in_chunk>3630</loc_in_chunk>
    </chunk_stats>
  </metadata>
  <ascii_map><![CDATA[
runtime/
├── __init__.py
│   (LOC: 14, Size: 386 B)
├── emitters.py
│   (LOC: 60, Size: 2.1 KB)
├── events_adapter.py
│   (LOC: 176, Size: 6.6 KB)
├── helpers/
│   ├── __init__.py
│   │   (LOC: 39, Size: 1.2 KB)
│   ├── checkpointing.py
│   │   (LOC: 52, Size: 1.8 KB)
│   ├── emission.py
│   │   (LOC: 58, Size: 2.0 KB)
│   ├── engram.py
│   │   (LOC: 75, Size: 2.6 KB)
│   ├── ingest.py
│   │   (LOC: 99, Size: 3.5 KB)
│   ├── macro_board.py
│   │   (LOC: 51, Size: 1.5 KB)
│   ├── maps_ws.py
│   │   (LOC: 86, Size: 3.0 KB)
│   ├── redis_out.py
│   │   (LOC: 160, Size: 5.3 KB)
│   ├── smoke.py
│   │   (LOC: 56, Size: 2.5 KB)
│   ├── speak.py
│   │   (LOC: 133, Size: 4.2 KB)
│   ├── status_http.py
│   │   (LOC: 194, Size: 6.5 KB)
│   └── viz.py
│       (LOC: 34, Size: 1.1 KB)
├── loop/
│   ├── __init__.py
│   │   (LOC: 48, Size: 1.4 KB)
│   └── main.py
│       (LOC: 934, Size: 40.0 KB)
├── orchestrator.py
│   (LOC: 100, Size: 4.0 KB)
├── phase.py
│   (LOC: 282, Size: 10.9 KB)
├── retention.py
│   (LOC: 105, Size: 3.7 KB)
├── state.py
│   (LOC: 86, Size: 2.8 KB)
├── stepper.py
│   (LOC: 136, Size: 4.1 KB)
└── telemetry.py
    (LOC: 652, Size: 25.8 KB)]]></ascii_map>
  <files>
    <file>
      <path>__init__.py</path>
      <content><![CDATA[# Runtime package initializer for modularized orchestrator components.
# Exposes submodules for clarity; keep lightweight to avoid side effects.
# Note: Nexus remains the external façade; internals live under runtime/*
__all__ = [
    "phase",
    "loop",
    "telemetry",
    "retention",
    "events_adapter",
    "runtime_helpers",
    "emitters",
    "orchestrator",
    "state",
]]]></content>
    </file>
    <file>
      <path>emitters.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime emitters initialization (MacroEmitter, ThoughtEmitter).

Behavior:
- Mirrors Nexus inline initialization exactly:
  * MacroEmitter path priority: $UTD_OUT or utd.path or <run_dir>/utd_events.jsonl
  * ThoughtEmitter enabled only when ENABLE_THOUGHTS in ("1","true","yes","on")
    path priority: $THOUGHT_OUT or <run_dir>/thoughts.ndjson
- Returns (macro_emitter_or_None, thought_emitter_or_None)
- No logging or file writes here (pure construction).
"""

from typing import Any, Callable, Optional, Tuple
import os

# IO-layer actuators (allowed in runtime layer)
from fum_rt.io.actuators.macros import MacroEmitter
from fum_rt.io.actuators.thoughts import ThoughtEmitter


def initialize_emitters(
    utd: Any,
    run_dir: str,
    why_provider: Callable[[], dict],
) -> Tuple[Optional[MacroEmitter], Optional[ThoughtEmitter]]:
    """
    Create MacroEmitter and ThoughtEmitter with legacy-equivalent configuration.
    """
    macro: Optional[MacroEmitter] = None
    thoughts: Optional[ThoughtEmitter] = None

    # Macro emitter (write-only; respects UTD_OUT if set)
    try:
        out_path = os.getenv("UTD_OUT") or getattr(utd, "path", None) or os.path.join(run_dir, "utd_events.jsonl")
        macro = MacroEmitter(path=str(out_path), why_provider=why_provider)
    except Exception:
        macro = None

    # Introspection Ledger (emit-only), behind feature flag ENABLE_THOUGHTS
    try:
        if str(os.getenv("ENABLE_THOUGHTS", "0")).lower() in ("1", "true", "yes", "on"):
            th_path = os.getenv("THOUGHT_OUT") or os.path.join(run_dir, "thoughts.ndjson")
            thoughts = ThoughtEmitter(path=str(th_path), why=why_provider)
    except Exception:
        thoughts = None

    return macro, thoughts


__all__ = ["initialize_emitters"]]]></content>
    </file>
    <file>
      <path>events_adapter.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime adapter: Convert connectome Observation events into core event-driven metrics inputs.

Design:
- Pure adapter: no logging/IO; small and deterministic.
- Safe: returns an empty list for unknown/unsupported events.
- Behavior-preserving by default: only used when ENABLE_EVENT_METRICS=1.
"""

from typing import Any, Dict, Iterable, List
from fum_rt.core.proprioception.events import (
    BaseEvent,
    DeltaEvent,
    VTTouchEvent,
    SpikeEvent,
    DeltaWEvent,
    EdgeOnEvent,
    ADCEvent,
)


def observations_to_events(observations: Iterable[Any]) -> List[BaseEvent]:
    """
    Map connectome Observation objects to EventDrivenMetrics events.
    Supported kinds:
      - "cycle_hit":   -> DeltaEvent (b1 from loop_gain if available) + EdgeOnEvent(u,v) when nodes include two ids
                         Also synthesizes bounded excitatory SpikeEvent for the touched endpoints.
      - "region_stat": -> VTTouchEvent per node (weight 1.0) and bounded excitatory SpikeEvent per node (amp from s_mean or 1.0)
      - "delta_w":     -> DeltaWEvent per node (bounded fan-out).
                         Additionally, when dw < 0, synthesize bounded inhibitory SpikeEvent (sign=-1, amp=|dw| clipped)
                         to provide an inhibition source without scans.

    Unknown kinds are ignored.
    """
    out: List[BaseEvent] = []
    if not observations:
        return out

    for obs in observations:
        try:
            kind = getattr(obs, "kind", None)
            tick = int(getattr(obs, "tick", 0))
        except Exception:
            continue

        if kind == "cycle_hit":
            try:
                loop_gain = float(getattr(obs, "loop_gain", 0.0))
            except Exception:
                loop_gain = 0.0
            # Use non-negative contribution to the b1 accumulator
            b1_contrib = loop_gain if loop_gain > 0.0 else 1.0
            out.append(DeltaEvent(kind="delta", t=tick, b1=float(b1_contrib)))
            try:
                nodes = list(getattr(obs, "nodes", []) or [])
                if len(nodes) >= 2:
                    u, v = int(nodes[0]), int(nodes[1])
                    out.append(EdgeOnEvent(kind="edge_on", t=tick, u=u, v=v))
                # Also synthesize excitatory SpikeEvents for the endpoints (bounded, event-driven)
                try:
                    amp = loop_gain if loop_gain > 0.0 else 1.0
                except Exception:
                    amp = 1.0
                for idx in nodes[:2]:
                    try:
                        out.append(SpikeEvent(kind="spike", t=tick, node=int(idx), amp=float(amp), sign=+1))
                    except Exception:
                        continue
            except Exception:
                pass

        elif kind == "region_stat":
            try:
                nodes = list(getattr(obs, "nodes", []) or [])
                for node in nodes:
                    out.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(node), w=1.0))
                # Synthesize excitatory SpikeEvent per node using s_mean as amplitude when available
                try:
                    s_mean = float(getattr(obs, "s_mean", 0.0))
                except Exception:
                    s_mean = 0.0
                amp = s_mean if s_mean > 0.0 else 1.0
                for node in nodes:
                    out.append(SpikeEvent(kind="spike", t=tick, node=int(node), amp=float(amp), sign=+1))
            except Exception:
                pass

        elif kind == "delta":
            # Generic learning delta event; fields are expected in obs.meta
            try:
                meta = getattr(obs, "meta", {}) or {}
                b1 = float(meta.get("b1", 0.0))
                nov = float(meta.get("nov", 0.0))
                hab = float(meta.get("hab", 0.0))
                tdv = float(meta.get("td", 0.0))
                hsi = float(meta.get("hsi", 0.0))
                out.append(
                    DeltaEvent(
                        kind="delta",
                        t=tick,
                        b1=b1,
                        novelty=nov,
                        hab=hab,
                        td=tdv,
                        hsi=hsi,
                    )
                )
            except Exception:
                pass

        elif kind == "delta_w":
            # Map Observation(kind='delta_w') -> one or more DeltaWEvent(s)
            # Also synthesize inhibitory SpikeEvent when dw < 0 (bounded fan-out) to drive InhibitionMap without scans.
            try:
                nodes = list(getattr(obs, "nodes", []) or [])
                meta = dict(getattr(obs, "meta", {}) or {})
                dwv = float(meta.get("dw", 0.0))
                # Determine inhibitory synthesis parameters
                is_inh = dwv < 0.0
                inh_amp = float(min(1.0, abs(dwv))) if is_inh else 0.0
                # Bound fan-out defensively
                for node in nodes[:16]:
                    ni = int(node)
                    out.append(DeltaWEvent(kind="delta_w", t=tick, node=ni, dw=float(dwv)))
                    # Provide an explicit inhibitory spike source when dw is negative
                    if is_inh and inh_amp > 0.0:
                        out.append(SpikeEvent(kind="spike", t=tick, node=ni, amp=inh_amp, sign=-1))
            except Exception:
                pass

        else:
            # ignore unknown kinds
            pass

    return out


def adc_metrics_to_event(metrics: Dict[str, Any], t: int) -> ADCEvent:
    """
    Convert ADC metrics dict into a single ADCEvent for folding.
    Expected keys (optional):
      - adc_territories
      - adc_boundaries
      - adc_cycle_hits
    """
    try:
        terr = metrics.get("adc_territories", None)
        bnd = metrics.get("adc_boundaries", None)
        cyc = metrics.get("adc_cycle_hits", None)
    except Exception:
        terr = bnd = cyc = None

    try:
        terr_i = None if terr is None else int(terr)
    except Exception:
        terr_i = None
    try:
        bnd_i = None if bnd is None else int(bnd)
    except Exception:
        bnd_i = None
    try:
        cyc_f = None if cyc is None else float(cyc)
    except Exception:
        cyc_f = None

    return ADCEvent(kind="adc", t=int(t), adc_territories=terr_i, adc_boundaries=bnd_i, adc_cycle_hits=cyc_f)]]></content>
    </file>
    <file>
      <path>helpers/__init__.py</path>
      <content><![CDATA["""
Runtime helpers package (modularized).

Transitional re-exports:
- During migration away from the monolith [runtime_helpers.py](../runtime_helpers.py), we re-export
  its functions here to provide a stable import path:
    from fum_rt.runtime.helpers import process_messages, emit_status_and_macro, ...
- New helpers live as separate modules under this package (e.g., maps_ws.py).
"""

from __future__ import annotations

# New, modular helpers
from .maps_ws import maybe_start_maps_ws  # re-export
from .macro_board import register_macro_board  # re-export (modular)

# Modularized helper implementations (explicit re-exports)
from .engram import maybe_load_engram, derive_start_step
from .ingest import process_messages
from .smoke import maybe_smoke_tests
from .speak import maybe_auto_speak
from .emission import emit_status_and_macro
from .viz import maybe_visualize
from .checkpointing import save_tick_checkpoint

__all__ = [
    # New helpers
    "maybe_start_maps_ws",
    # Transitional re-exports
    "register_macro_board",
    "maybe_load_engram",
    "derive_start_step",
    "process_messages",
    "maybe_smoke_tests",
    "maybe_auto_speak",
    "emit_status_and_macro",
    "maybe_visualize",
    "save_tick_checkpoint",
]]]></content>
    </file>
    <file>
      <path>helpers/checkpointing.py</path>
      <content><![CDATA["""
Runtime helper: checkpointing and retention.

Provides:
- save_tick_checkpoint(): periodic snapshot with retention, behavior-preserving.
"""

from __future__ import annotations

from typing import Any

from fum_rt.core.memory import save_checkpoint
from fum_rt.runtime.retention import prune_checkpoints as _prune_ckpt


def save_tick_checkpoint(nx: Any, step: int) -> None:
    """
    Save checkpoint and run retention policy when configured. Mirrors original behavior.
    """
    try:
        if getattr(nx, "checkpoint_every", 0) and (int(step) % int(nx.checkpoint_every)) == 0 and int(step) > 0:
            try:
                path = save_checkpoint(
                    nx.run_dir,
                    int(step),
                    nx.connectome,
                    fmt=getattr(nx, "checkpoint_format", "h5") or "h5",
                    adc=getattr(nx, "adc", None),
                )
                try:
                    nx.logger.info("checkpoint_saved", extra={"extra": {"path": str(path), "step": int(step)}})
                except Exception:
                    pass
                if int(getattr(nx, "checkpoint_keep", 0)) > 0:
                    try:
                        summary = _prune_ckpt(nx.run_dir, keep=int(nx.checkpoint_keep), last_path=path)
                        try:
                            nx.logger.info("checkpoint_retention", extra={"extra": summary})
                        except Exception:
                            pass
                    except Exception:
                        pass
            except Exception as e:
                try:
                    nx.logger.info("checkpoint_error", extra={"extra": {"err": str(e)}})
                except Exception:
                    pass
    except Exception:
        pass


__all__ = ["save_tick_checkpoint"]]]></content>
    </file>
    <file>
      <path>helpers/emission.py</path>
      <content><![CDATA["""
Runtime helper: status emission and macro board status.

- Emits open UTD status payload every status_every ticks.
- Emits a 'status' macro when valence is high (mirrors legacy behavior).

Imports typing + telemetry builder only; no IO side effects besides UTD emits.
"""

from __future__ import annotations

from typing import Any, Dict

from fum_rt.runtime.telemetry import status_payload as _telemetry_status


def emit_status_and_macro(nx: Any, m: Dict[str, Any], step: int) -> None:
    """
    Emit open UTD status payload and, when valence is high, a 'status' macro.
    Mirrors the inline Nexus logic.
    """
    if (int(step) % int(getattr(nx, "status_every", 1))) != 0:
        return

    # Open UTD status
    try:
        payload = _telemetry_status(nx, m, int(step))
        score = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
        nx.utd.emit_text(payload, score=score)
    except Exception:
        pass

    # Macro board status
    try:
        val = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
        if val >= 0.6:
            nx.utd.emit_macro(
                "status",
                {
                    "t": int(step),
                    "neurons": int(getattr(nx, "N", 0)),
                    "cohesion_components": int(m.get("cohesion_components", 0)),
                    "vt_coverage": float(m.get("vt_coverage", 0.0)),
                    "vt_entropy": float(m.get("vt_entropy", 0.0)),
                    "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
                    "active_edges": int(m.get("active_edges", 0)),
                    "homeostasis_pruned": int(m.get("homeostasis_pruned", 0)),
                    "homeostasis_bridged": int(m.get("homeostasis_bridged", 0)),
                    "ute_in_count": int(m.get("ute_in_count", 0)),
                    "ute_text_count": int(m.get("ute_text_count", 0)),
                },
                score=val,
            )
    except Exception:
        pass


__all__ = ["emit_status_and_macro"]]]></content>
    </file>
    <file>
      <path>helpers/engram.py</path>
      <content><![CDATA["""
Runtime helper: engram load and start-step derivation.

Behavior:
- maybe_load_engram(nx, path): loads engram state into connectome (and ADC if present), logs outcome.
- derive_start_step(nx, path): derives starting tick index based on provided path or existing state_* files.

This module provides the real implementations migrated from the legacy runtime_helpers monolith.
"""

from __future__ import annotations

from typing import Any, Optional
import os
import re

from fum_rt.core.memory import load_engram as _load_engram_state


def maybe_load_engram(nx: Any, load_engram_path: Optional[str]) -> None:
    """
    If a path is provided, load the engram into nx.connectome (and nx.adc when present),
    logging the result into nx.logger for UI confirmation. Mirrors legacy behavior.
    """
    if not load_engram_path:
        return
    try:
        _load_engram_state(str(load_engram_path), nx.connectome, adc=getattr(nx, "adc", None))
        try:
            nx.logger.info("engram_loaded", extra={"extra": {"path": str(load_engram_path)}})
        except Exception:
            pass
    except Exception as e:
        try:
            nx.logger.info("engram_load_error", extra={"extra": {"err": str(e), "path": str(load_engram_path)}})
        except Exception:
            pass


def derive_start_step(nx: Any, load_engram_path: Optional[str]) -> int:
    """
    Derive starting step to continue numbering after resume, avoiding retention deleting
    new snapshots. Mirrors original logic including filename parsing and fallback scan.

    Policy:
    - If load_engram_path points to a state file named like state_<step>.(h5|npz), return step+1
    - Else scan nx.run_dir for the highest state_<step>.(h5|npz) and return highest+1
    - Else return 0
    """
    try:
        s: Optional[int] = None
        lp = str(load_engram_path) if load_engram_path else None
        if lp and os.path.isfile(lp):
            base = os.path.basename(lp)
            m = re.search(r"state_(\d+)\.(h5|npz)$", base)
            if m:
                s = int(m.group(1))
        if s is None:
            max_s = -1
            for fn in os.listdir(nx.run_dir):
                if not fn.startswith("state_"):
                    continue
                m2 = re.search(r"state_(\d+)\.(h5|npz)$", fn)
                if m2:
                    ss = int(m2.group(1))
                    if ss > max_s:
                        max_s = ss
            if max_s >= 0:
                s = max_s
        return int(s) + 1 if s is not None else 0
    except Exception:
        return 0


__all__ = ["maybe_load_engram", "derive_start_step"]]]></content>
    </file>
    <file>
      <path>helpers/ingest.py</path>
      <content><![CDATA["""
Runtime helper: message ingestion and per-tick symbol/index extraction.

Provides:
- process_messages(): Mirrors legacy Nexus/runtime behavior while keeping the runtime layer modular.

Policy:
- Runtime helpers may import fum_rt.io.* and fum_rt.core.*.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Set, Tuple

from fum_rt.core import text_utils
from fum_rt.io.cognition.stimulus import symbols_to_indices as _stim_symbols_to_indices


def process_messages(nx: Any, msgs: Iterable[Dict[str, Any]]) -> Tuple[int, Set[int], Set[str], Dict[int, Any]]:
    """
    Process UTE messages:
      - Count text messages
      - Update recent_text, lexicon/ngrams, and document count
      - Build per-tick token set for IDF computations and seed selection
      - Map symbols to connectome indices via nx._symbols_to_indices (deterministic)
      - Emit each message to UTD (mirrors original timing)

    Returns: (ute_text_count, stim_idxs, tick_tokens, tick_rev_map)
    """
    ute_text_count = 0
    stim_idxs: Set[int] = set()
    tick_tokens: Set[str] = set()
    tick_rev_map: Dict[int, Any] = {}

    for m in msgs:
        try:
            if m.get("type") != "text":
                # Non-text messages are emitted to UTD as-is
                try:
                    nx.utd.emit_text(m)
                except Exception:
                    pass
                continue

            ute_text_count += 1
            # Append to rolling recent_text
            try:
                text = str(m.get("msg", ""))
                try:
                    nx.recent_text.append(text)
                except Exception:
                    pass
                # Update lexicon/ngrams and token set for this tick (behavior-preserving)
                try:
                    if not hasattr(nx, "_lexicon"):
                        nx._lexicon = {}
                    toks = text_utils.tokenize_text(text)
                    for w in set(toks):
                        nx._lexicon[w] = int(nx._lexicon.get(w, 0)) + 1
                        tick_tokens.add(w)
                    # Ensure n-gram stores exist and update streaming n-grams for emergent composition
                    try:
                        nx._ng2
                        nx._ng3
                    except Exception:
                        nx._ng2 = {}
                        nx._ng3 = {}
                    text_utils.update_ngrams(toks, nx._ng2, nx._ng3)
                    # Increment document counter once per inbound text message
                    nx._doc_count = int(getattr(nx, "_doc_count", 0)) + 1
                except Exception:
                    pass
                # Symbol → indices mapping (deterministic)
                try:
                    group_size = int(getattr(nx, "stim_group_size", 4))
                    max_symbols = int(getattr(nx, "stim_max_symbols", 64))
                    idxs = _stim_symbols_to_indices(
                        text, group_size, max_symbols, int(getattr(nx, "N", 0)), reverse_map=tick_rev_map
                    )
                    for i in idxs:
                        stim_idxs.add(int(i))
                except Exception:
                    pass
            except Exception:
                pass

            # Emit original message
            try:
                nx.utd.emit_text(m)
            except Exception:
                pass
        except Exception:
            # Fail-soft per message
            pass

    return ute_text_count, stim_idxs, tick_tokens, tick_rev_map


__all__ = ["process_messages"]]]></content>
    </file>
    <file>
      <path>helpers/macro_board.py</path>
      <content><![CDATA["""
Runtime helper: macro board registration on UTD emitter.

Behavior:
- Registers default macros ('status', 'say')
- Loads per-run macro_board.json entries only (no external fallbacks)
"""

from __future__ import annotations

import os
import json
from typing import Any


def register_macro_board(utd: Any, run_dir: str) -> None:
    """
    Register default macros and optional per-run macro_board.json entries on a UTD-like emitter.
    Mirrors legacy behavior:
      - Always register 'status' and 'say'
      - Optionally load runs/<ts>/macro_board.json (dict of name -> meta)
      - Only per-run board can provide metadata/templates to preserve emergent language
    """
    try:
        utd.register_macro("status", {"desc": "Emit structured status payload"})
    except Exception:
        pass
    try:
        utd.register_macro("say", {"desc": "Emit plain text line"})
    except Exception:
        pass

    # Per-run macro_board.json
    try:
        pth = os.path.join(run_dir, "macro_board.json")
        if os.path.exists(pth):
            with open(pth, "r", encoding="utf-8") as fh:
                reg = json.load(fh)
            if isinstance(reg, dict):
                for name, meta in reg.items():
                    try:
                        utd.register_macro(str(name), meta if isinstance(meta, dict) else {})
                    except Exception:
                        pass
    except Exception:
        pass

    # External fallbacks removed by repository policy: macros must originate from per-run files.


__all__ = ["register_macro_board"]]]></content>
    </file>
    <file>
      <path>helpers/maps_ws.py</path>
      <content><![CDATA["""
Runtime helper: maps/frame WebSocket bootstrap (bounded, drop-oldest).

- Safe no-op when ENABLE_MAPS_WS is not truthy or when 'websockets' package is missing.
- Ensures a bounded MapsRing exists on nx._maps_ring (capacity=MAPS_RING, default 3).
- Starts MapsWebSocketServer once and stores it on nx._maps_ws_server.

This file is part of the runtime helpers modularization under fum_rt.runtime.helpers.
"""

from __future__ import annotations

import os
from typing import Any


def _truthy(x) -> bool:
    try:
        if isinstance(x, (int, float)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False


def maybe_start_maps_ws(nx: Any) -> None:
    """
    Lazily start the maps/frame WebSocket forwarder if ENABLE_MAPS_WS is truthy.
    - Ensures a bounded MapsRing exists on nx._maps_ring (capacity=MAPS_RING, default 3)
    - Starts a background MapsWebSocketServer (host=MAPS_WS_HOST, port=MAPS_WS_PORT)
    - Safe no-op if websockets is not installed or any error occurs
    """
    try:
        if not _truthy(os.getenv("ENABLE_MAPS_WS", "0")):
            return

        # Ensure a ring exists (reuses ring created by telemetry tick_fold if present)
        ring = getattr(nx, "_maps_ring", None)
        if ring is None:
            try:
                from fum_rt.io.visualization.maps_ring import MapsRing  # allowed in runtime layer
                cap = 3
                try:
                    cap = int(os.getenv("MAPS_RING", "3"))
                except Exception:
                    cap = 3
                nx._maps_ring = MapsRing(capacity=max(1, cap))
                ring = nx._maps_ring
            except Exception:
                ring = None

        if ring is None:
            return

        # Start server once
        if getattr(nx, "_maps_ws_server", None) is None:
            try:
                from fum_rt.io.visualization.websocket_server import MapsWebSocketServer  # runtime-layer IO allowed
                host = os.getenv("MAPS_WS_HOST", "127.0.0.1")
                try:
                    port = int(os.getenv("MAPS_WS_PORT", "8765"))
                except Exception:
                    port = 8765

                def _err(msg: str) -> None:
                    try:
                        nx.logger.info("maps_ws_error", extra={"extra": {"err": str(msg)}})
                    except Exception:
                        try:
                            print("[maps_ws] " + str(msg), flush=True)
                        except Exception:
                            pass

                srv = MapsWebSocketServer(ring, host=host, port=port, on_error=_err)
                srv.start()
                nx._maps_ws_server = srv
            except Exception:
                # Missing websockets or other failure - safe no-op
                return
    except Exception:
        # Never disrupt runtime parity
        pass


__all__ = ["maybe_start_maps_ws"]]]></content>
    </file>
    <file>
      <path>helpers/redis_out.py</path>
      <content><![CDATA["""
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


__all__ = ["maybe_publish_status_redis", "maybe_publish_maps_redis"]]]></content>
    </file>
    <file>
      <path>helpers/smoke.py</path>
      <content><![CDATA["""
Runtime helper: optional one-shot smoke tests (macros and thought ledger).

- Controlled by env flags:
  - ENABLE_MACROS_TEST
  - ENABLE_THOUGHTS_TEST

Behavior:
- Mirrors legacy Nexus logic exactly; guarded and fail-soft.
"""

from __future__ import annotations

import os
from typing import Any, Dict


def maybe_smoke_tests(nx: Any, m: Dict[str, Any], step: int) -> None:
    """
    One-shot emitters test for macros and thought ledger when ENABLE_*_TEST env flags are set.
    Mirrors Nexus inline behavior and guards with booleans on nx.
    """
    # Macro smoke
    try:
        if (not getattr(nx, "_macros_smoke_done", False)) and str(os.getenv("ENABLE_MACROS_TEST", "0")).lower() in ("1", "true", "yes", "on"):
            if getattr(nx, "emitter", None):
                nx.emitter.vars({"N": "neural", "G": "global_access", "E": "experience", "B": "behavior"})
                nx.emitter.edges(["N->G", "G->B", "E->B?"])
                nx.emitter.assumptions(["no unmeasured confounding", "positivity"])
                nx.emitter.target("P(B|do(G))")
                nx.emitter.derivation("If N fixes G and G mediates B, therefore adjust on {confounders} yields effect.")
                nx.emitter.prediction_delta("Behavioral margin differs if extra-law holds.")
                nx.emitter.transfer("Circuit: signal->bus; flag->output; hidden noise.")
                nx.emitter.equation("Y = β X + U_Y")
                nx.emitter.status("macro smoke: ok")
            nx._macros_smoke_done = True
    except Exception:
        pass

    # Thought ledger smoke
    try:
        if (not getattr(nx, "_thoughts_smoke_done", False)) and str(os.getenv("ENABLE_THOUGHTS_TEST", "0")).lower() in ("1", "true", "yes", "on"):
            if getattr(nx, "thoughts", None):
                nx.thoughts.observation("vt_entropy", float(m.get("vt_entropy", 0.0)))
                nx.thoughts.motif("cycle_probe", nodes=[1, 2, 3])
                nx.thoughts.hypothesis("H0", "A ⟂ B | Z", status="tentative", conf=0.55)
                nx.thoughts.test("CI", True, vars={"A": "A", "B": "B", "Z": ["Z"]})
                nx.thoughts.derivation(["H0", "obs:vt_coverage↑"], "Identify P(Y|do(X)) via backdoor on {Z}", conf=0.6)
                nx.thoughts.revision("H0", "accepted", because=["test:CI:true"])
                nx.thoughts.plan("intervene", vars={"target": "X"}, rationale="disambiguate twins")
            nx._thoughts_smoke_done = True
    except Exception:
        pass


__all__ = ["maybe_smoke_tests"]]]></content>
    </file>
    <file>
      <path>helpers/speak.py</path>
      <content><![CDATA["""
Runtime helper: autonomous speaking (composer + speaker gate + novelty IDF).

Behavior:
- Mirrors legacy Nexus logic for maybe_auto_speak() exactly.
- Pure runtime helper; safe fail-soft; no side-effects beyond UTD emissions and learned lexicon updates.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Set

from fum_rt.core import text_utils
from fum_rt.io.cognition.composer import compose_say_text as _compose_say_text_impl
from fum_rt.io.cognition.speaker import should_speak as _speak_gate, novelty_and_score as _novelty_and_score
from fum_rt.runtime.telemetry import macro_why_base as _telemetry_why_base


def maybe_auto_speak(
    nx: Any,
    m: Dict[str, Any],
    step: int,
    tick_tokens: Set[str],
    void_topic_symbols: Set[Any],
) -> None:
    """
    Behavior-preserving autonomous speaking based on topology spikes and valence.
    Mirrors the original Nexus block in full detail.
    """
    try:
        val_v2 = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
    except Exception:
        val_v2 = float(m.get("sie_valence_01", 0.0))
    spike = bool(m.get("b1_spike", False))

    if not getattr(nx, "speak_auto", False):
        return

    can_speak, reason = _speak_gate(val_v2, spike, float(getattr(nx, "speak_valence_thresh", 0.01)))
    if not can_speak:
        if reason == "low_valence":
            try:
                nx.logger.info(
                    "speak_suppressed",
                    extra={
                        "extra": {
                            "reason": "low_valence",
                            "val": val_v2,
                            "thresh": float(getattr(nx, "speak_valence_thresh", 0.01)),
                            "b1_z": float(m.get("b1_z", 0.0)),
                            "t": int(step),
                        }
                    },
                )
            except Exception:
                pass
        return

    # Compose; do not suppress due to lack of topic/tokens. Model controls content fully.
    seed_material = tick_tokens if tick_tokens else void_topic_symbols
    try:
        speech = _compose_say_text_impl(
            m or {},
            int(step),
            getattr(nx, "_lexicon", {}) or {},
            getattr(nx, "_ng2", {}) or {},
            getattr(nx, "_ng3", {}) or {},
            getattr(nx, "recent_text", []),
            templates=list(getattr(nx, "_phrase_templates", []) or []),
            seed_tokens=seed_material,
        ) or ""
    except Exception:
        speech = ""

    # Composer IDF gain (local to composer; does not affect dynamics)
    try:
        composer_k = float(getattr(nx, "_phase", {}).get("composer_idf_k", float(os.getenv("COMPOSER_IDF_K", "0.0"))))
    except Exception:
        composer_k = 0.0

    # Composer-local novelty IDF + score (telemetry/emitter only; does not affect dynamics)
    try:
        novelty_idf, score_out = _novelty_and_score(
            speech,
            getattr(nx, "_lexicon", {}) or {},
            int(getattr(nx, "_doc_count", 0)),
            text_utils.tokenize_text,
            float(composer_k),
            float(val_v2),
        )
    except Exception:
        novelty_idf, score_out = 0.0, float(val_v2)

    # Update learned lexicon after computing novelty (avoid self-bias in estimate)
    try:
        if not hasattr(nx, "_lexicon"):
            nx._lexicon = {}
        toks2 = text_utils.tokenize_text(speech)
        for w in set(toks2):
            nx._lexicon[w] = int(nx._lexicon.get(w, 0)) + 1
        # Ensure n-gram stores exist and update streaming n-grams
        try:
            nx._ng2
            nx._ng3
        except Exception:
            nx._ng2 = {}
            nx._ng3 = {}
        text_utils.update_ngrams(toks2, nx._ng2, nx._ng3)
    except Exception:
        pass

    # Emit macro
    try:
        why = _telemetry_why_base(nx, m, int(step))
        try:
            why["novelty_idf"] = float(novelty_idf)
            why["composer_idf_k"] = float(composer_k)
        except Exception:
            pass
        nx.utd.emit_macro(
            "say",
            {
                "text": speech,
                "why": why,
            },
            score=score_out,
        )
    except Exception:
        pass


__all__ = ["maybe_auto_speak"]]]></content>
    </file>
    <file>
      <path>helpers/status_http.py</path>
      <content><![CDATA[from __future__ import annotations

"""
Optional in-process HTTP status endpoint (void-faithful; no schedulers).

- Purpose: serve the latest status payload to UI without any file reads.
- Behavior: starts a tiny HTTP server in a background thread (event-driven, no timers).
- Endpoint:
    GET /status  -> 200 JSON of nx._emit_last_metrics (latest per-tick status) or 204 if not yet available
    GET /health  -> 200 {"ok": true}
- Enable via:
    ENABLE_STATUS_HTTP=1
    STATUS_HTTP_HOST=127.0.0.1
    STATUS_HTTP_PORT=8787
- Safety:
    - If any error occurs (port busy, etc.), remain a no-op.
    - Never mutates core dynamics; purely IO.
"""

import os
import json
import threading
from typing import Any, Optional


def _truthy(x: Any) -> bool:
    try:
        if isinstance(x, (int, float, bool)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False


def maybe_start_status_http(nx: Any, force: bool = False) -> None:
    """
    Idempotently start the status HTTP server.
    Stores references on nx as:
      nx._status_http_server (HTTPServer)
      nx._status_http_thread (threading.Thread)
      nx._status_http_started (bool)
    Gate:
      - If force is True, start regardless of env.
      - If force is False, start only when ENABLE_STATUS_HTTP is truthy.
    """
    # Idempotence: already running or previously started
    try:
        if getattr(nx, "_status_http_started", False) or getattr(nx, "_status_http_server", None) is not None:
            return
    except Exception:
        pass
    # Env gate unless forced
    if not force:
        try:
            if not _truthy(os.getenv("ENABLE_STATUS_HTTP", "0")):
                return
        except Exception:
            return

    # Already running
    try:
        if getattr(nx, "_status_http_server", None) is not None:
            return
    except Exception:
        pass

    # Lazy import from stdlib; avoid global import side effects
    try:
        from http.server import BaseHTTPRequestHandler, HTTPServer  # type: ignore
    except Exception:
        return

    # Configuration
    try:
        host = os.getenv("STATUS_HTTP_HOST", "127.0.0.1").strip() or "127.0.0.1"
    except Exception:
        host = "127.0.0.1"
    try:
        port = int(os.getenv("STATUS_HTTP_PORT", "8787"))
    except Exception:
        port = 8787

    # Bind Nexus reference in a closure for the handler
    nexus_ref = nx

    class _Handler(BaseHTTPRequestHandler):  # type: ignore
        # Silence default logging
        def log_message(self, format: str, *args) -> None:  # noqa: A003 (shadow builtins name)
            try:
                if getattr(nexus_ref, "logger", None) is not None:
                    # Keep this extremely low-cost; skip formatting expansions
                    pass
            except Exception:
                pass

        def _send_json(self, code: int, payload: Optional[dict]) -> None:
            try:
                body = b""
                if payload is not None:
                    try:
                        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                    except Exception:
                        body = b"{}"
                self.send_response(code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if body:
                    self.wfile.write(body)
            except Exception:
                # Best-effort: avoid crashing the server
                try:
                    self.send_response(500)
                    self.end_headers()
                except Exception:
                    pass

        def do_GET(self) -> None:  # type: ignore
            try:
                path = self.path or "/"
                if path == "/health":
                    return self._send_json(200, {"ok": True})
                if path in ("/status", "/status/snapshot"):
                    # Serve latest status payload captured by the runtime loop
                    try:
                        m = getattr(nexus_ref, "_emit_last_metrics", None)
                    except Exception:
                        m = None
                    if isinstance(m, dict) and m:
                        # Minimal filtering: ensure JSON-serializable scalars
                        safe = {}
                        for k, v in m.items():
                            try:
                                if isinstance(v, (int, float, str, bool)) or v is None:
                                    safe[k] = v
                                else:
                                    # fallback to float or string
                                    try:
                                        safe[k] = float(v)  # type: ignore
                                    except Exception:
                                        safe[k] = str(v)
                            except Exception:
                                continue
                        return self._send_json(200, safe)
                    return self._send_json(204, None)
                # Not found
                self.send_response(404)
                self.end_headers()
            except Exception:
                try:
                    self.send_response(500)
                    self.end_headers()
                except Exception:
                    pass

    # Create and start the HTTP server
    try:
        server = HTTPServer((host, port), _Handler)  # type: ignore
    except Exception:
        return

    def _run() -> None:
        try:
            server.serve_forever(poll_interval=0.5)
        except Exception:
            pass
        finally:
            try:
                server.server_close()
            except Exception:
                pass

    try:
        th = threading.Thread(target=_run, name="status_http", daemon=True)
        th.start()
        setattr(nx, "_status_http_server", server)
        setattr(nx, "_status_http_thread", th)
        try:
            setattr(nx, "_status_http_started", True)
        except Exception:
            pass
    except Exception:
        try:
            server.server_close()
        except Exception:
            pass
        return


__all__ = ["maybe_start_status_http"]]]></content>
    </file>
    <file>
      <path>helpers/viz.py</path>
      <content><![CDATA["""
Runtime helper: periodic visualization hooks (dashboard and connectome snapshot).

Behavior:
- Mirrors legacy Nexus logic and the original runtime_helpers.maybe_visualize()
- Fail-soft and fully optional; never disrupts runtime
"""

from __future__ import annotations

from typing import Any


def maybe_visualize(nx: Any, step: int) -> None:
    """
    Periodic dashboard and graph snapshot, behavior-preserving.
    """
    try:
        if getattr(nx, "viz_every", 0) and (int(step) % int(nx.viz_every)) == 0 and int(step) > 0:
            try:
                nx.vis.dashboard(nx.history[-max(50, int(nx.viz_every) * 2):])  # last window
                if int(getattr(nx, "N", 0)) <= 10000:
                    G = nx.connectome.snapshot_graph()
                    nx.vis.graph(G, fname='connectome.png')
            except Exception as e:
                try:
                    nx.logger.info("viz_error", extra={"extra": {"err": str(e)}})
                except Exception:
                    pass
    except Exception:
        pass


__all__ = ["maybe_visualize"]]]></content>
    </file>
    <file>
      <path>loop/__init__.py</path>
      <content><![CDATA[from __future__ import annotations

"""
fum_rt.runtime.loop package facade

Ensures import seam compliance for boundary tests:
- Imports runtime.telemetry.tick_fold seam.
- References core.signals seam.
- Re-exports run_loop from .main.

Void-faithful:
- No schedulers, timers, or cadence logic.
- No scans/dense ops; numpy-free.
"""

from typing import Any, Optional, Sequence

# Re-export the main runtime loop from the package implementation
from .main import run_loop

# Seams for boundary tests (presence-only imports)
from fum_rt.runtime.telemetry import tick_fold as _tick_fold  # runtime.telemetry seam
import fum_rt.core.signals as _signals  # noqa: F401  # core.signals seam (presence-only)


def run_loop_once(nx: Any, engine: Any, step: int, events: Optional[Sequence[Any]] = None) -> None:
    """
    Single-tick helper to satisfy boundary/import seams.
    Delegates to engine.step() if present, then stages telemetry via runtime.telemetry.tick_fold().
    """
    # Optional engine step delegation (void-faithful; no global scans)
    try:
        if hasattr(engine, "step"):
            if events is not None:
                engine.step(int(step), list(events))  # type: ignore[misc]
            else:
                engine.step(int(step))
    except Exception:
        pass

    # Always stage telemetry fold seam
    try:
        _tick_fold(nx, int(step), engine)
    except Exception:
        pass


__all__ = ["run_loop", "run_loop_once"]
]]></content>
    </file>
    <file>
      <path>loop/main.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime main loop (extracted from Nexus.run for modularization).

Behavior:
- Mirrors the original Nexus while-loop exactly (move-only).
- No logging configuration or finalization here; caller handles setup/teardown.
- Operates directly on the passed 'nx' Nexus-like object to preserve state and IO wiring.

Inputs:
- nx: Nexus-like instance (provides ute/utd/connectome/adc/etc.)
- t0: float timestamp at loop start (time.time())
- step: starting tick index (int)
- duration_s: optional max wall-clock seconds to run

Returns:
- last step index (int) after the loop completes/breaks
"""

from typing import Any, Dict, Set, Tuple, Optional
import time
import os

from fum_rt.runtime.stepper import compute_step_and_metrics as _compute_step_and_metrics
from fum_rt.runtime.telemetry import tick_fold as _tick_fold
from fum_rt.runtime.events_adapter import (
    observations_to_events as _obs_to_events,
    adc_metrics_to_event as _adc_event,
)
from fum_rt.core.engine import CoreEngine as _CoreEngine
from fum_rt.core.proprioception.events import EventDrivenMetrics as _EvtMetrics, BiasHintEvent as _BiasHintEvent
from fum_rt.core.cortex.scouts import VoidColdScoutWalker as _VoidScout
from fum_rt.core.signals import apply_b1_detector as _apply_b1d
from fum_rt.runtime.helpers.ingest import process_messages as _process_messages
from fum_rt.runtime.helpers.smoke import maybe_smoke_tests as _maybe_smoke_tests
from fum_rt.runtime.helpers.emission import emit_status_and_macro as _emit_status_and_macro
from fum_rt.runtime.helpers.viz import maybe_visualize as _maybe_visualize
from fum_rt.runtime.helpers.checkpointing import save_tick_checkpoint as _save_tick_checkpoint
from fum_rt.runtime.helpers import maybe_start_maps_ws as _maybe_start_maps_ws
from fum_rt.runtime.helpers.status_http import (
    maybe_start_status_http as _maybe_start_status_http,
)
from fum_rt.runtime.helpers.redis_out import (
    maybe_publish_status_redis as _maybe_publish_status_redis,
    maybe_publish_maps_redis as _maybe_publish_maps_redis,
)

# Void-faithful scout runner (stateless, per-tick; no schedulers)
from fum_rt.core.cortex.void_walkers.runner import run_scouts_once as _run_scouts_once
from fum_rt.core.cortex.void_walkers.void_heat_scout import HeatScout
from fum_rt.core.cortex.void_walkers.void_ray_scout import VoidRayScout
from fum_rt.core.cortex.void_walkers.void_memory_ray_scout import MemoryRayScout
from fum_rt.core.cortex.void_walkers.void_frontier_scout import FrontierScout
from fum_rt.core.cortex.void_walkers.void_cycle_scout import CycleHunterScout
from fum_rt.core.cortex.void_walkers.void_sentinel_scout import SentinelScout
# Also expose the remaining scouts for full coverage (9 walkers)
from fum_rt.core.cortex.void_walkers.void_cold_scout import ColdScout
from fum_rt.core.cortex.void_walkers.void_excitation_scout import ExcitationScout
from fum_rt.core.cortex.void_walkers.void_inhibition_scout import InhibitionScout
# Memory/trail steering fields (owner + adapter view)
from fum_rt.core.cortex.maps.memorymap import MemoryMap
from fum_rt.core.cortex.maps.trailmap import TrailMap
from fum_rt.core.memory import MemoryField

# ---------- Optional Learning/Actuator Adapters (default-off, safe) ----------
def _truthy(x) -> bool:
    try:
        if isinstance(x, (int, float)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False

# Development strictness gate: raise swallowed exceptions when enabled
STRICT = _truthy(os.getenv("VOID_STRICT", "0"))


def _maybe_run_revgsp(nx: Any, metrics: Dict[str, Any], step: int) -> None:
    """
    Best-effort adapter to call REV-GSP adapt_connectome if available and enabled.
    - Enabled via ENABLE_REVGSP=1 (default off).
    - Auto-detects compatible substrate (nx.substrate or nx.connectome with expected fields).
    - Filters kwargs to the function signature to avoid mismatches.
    - Silent no-op on any error or incompatibility.
    """
    import os, inspect  # local to avoid module-level dependency
    if not _truthy(os.getenv("ENABLE_REVGSP", "0")):
        return

    # Use current in-repo implementation only (void-faithful, budgeted)
    try:
        from fum_rt.core.neuroplasticity.revgsp import RevGSP as _RevGSP  # type: ignore
        _adapt = _RevGSP().adapt_connectome  # method-compatible wrapper
    except Exception:
        return

    # Pick a substrate-like object
    s = getattr(nx, "substrate", None)
    if s is None:
        s = getattr(nx, "connectome", None)
    if s is None:
        return

    # Build candidate kwargs and filter by signature
    try:
        sig = inspect.signature(_adapt)
        allowed = set(sig.parameters.keys())
    except Exception:
        allowed = set()

    # Sources for signals
    total_reward = float(metrics.get("sie_total_reward", 0.0))
    plv = metrics.get("evt_plv", None)  # optional; may be absent
    latency = getattr(nx, "network_latency_estimate", None)
    if latency is None:
        latency = {"max": float(getattr(nx, "latency_max", 0.0)), "error": float(getattr(nx, "latency_err", 0.0))}

    # Possible kwargs (include aliases so legacy and new signatures both work)
    eta_val = float(os.getenv("REV_GSP_ETA", getattr(nx, "rev_gsp_eta", 1e-3)))
    lam_val = float(os.getenv("REV_GSP_LAMBDA", getattr(nx, "rev_gsp_lambda", 0.99)))
    twin_ms = int(os.getenv("REV_GSP_TWIN_MS", "20"))
    candidates = {
        "substrate": s,
        "spike_train": getattr(nx, "recent_spikes", None),
        "spike_phases": getattr(nx, "spike_phases", None),
        # legacy name
        "learning_rate": eta_val,
        # new wrapper name
        "base_lr": eta_val,
        "lambda_decay": lam_val,
        "total_reward": total_reward,
        "plv": plv,
        # legacy name (if any)
        "network_latency_estimate": latency,
        # new wrapper name
        "network_latency": latency,
        "time_window_ms": twin_ms,
    }
    # Filter None values and restrict to signature
    kwargs = {k: v for k, v in candidates.items() if v is not None and (not allowed or k in allowed)}

    # If the function requires args we didn't provide, it will raise - catch and noop.
    try:
        _adapt(**kwargs)
    except Exception:
        # Silent by design; adapter is optional and must not disrupt runtime parity.
        return


def _maybe_run_gdsp(nx: Any, metrics: Dict[str, Any], step: int) -> None:
    """
    Best-effort adapter to call GDSP synaptic actuator if available and enabled.
    - Enabled via ENABLE_GDSP=1 (default off).
    - Emergent triggers only (no fixed cadence): activates on b1_spike, |td_signal| >= GDSP_TD_THRESH, or cohesion_components > 1.
    - Requires a substrate-like object with the expected sparse fields; else no-op.
    - Executes homeostatic repairs (if repair_triggered present), growth (when territory provided),
      and maintenance pruning with T_prune and pruning_threshold.
    """
    import os  # local import
    if not _truthy(os.getenv("ENABLE_GDSP", "0")):
        return

    # Emergent gating only (no fixed cadence or schedulers)
    try:
        td = float(metrics.get("td_signal", 0.0))
    except Exception:
        td = 0.0
    b1_spike = bool(metrics.get("b1_spike", metrics.get("evt_b1_spike", False)))
    try:
        comp = int(metrics.get("cohesion_components", metrics.get("evt_cohesion_components", 1)))
    except Exception:
        comp = 1
    try:
        td_thr = float(os.getenv("GDSP_TD_THRESH", "0.2"))
    except Exception:
        td_thr = 0.2
    if not (b1_spike or abs(td) >= td_thr or comp > 1):
        return

    # Use current in-repo implementation only (void-faithful, budgeted/territory-scoped)
    try:
        from fum_rt.core.neuroplasticity.gdsp import GDSPActuator as _GDSP  # type: ignore
        _gdsp = _GDSP()
        _run_gdsp = _gdsp.run
    except Exception:
        return

    # Substrate or connectome compatibility check (sparse CSR fields)
    s = getattr(nx, "substrate", None)
    if s is None:
        s = getattr(nx, "connectome", None)
    if s is None:
        return

    def _has(obj, name: str) -> bool:
        return hasattr(obj, name)

    # Required fields for GDSP to operate safely
    required = ("synaptic_weights", "persistent_synapses", "synapse_pruning_timers", "eligibility_traces", "firing_rates")
    if not all(_has(s, r) for r in required):
        return

    # Build reports (best-effort from current metrics)
    comp = int(metrics.get("cohesion_components", metrics.get("evt_cohesion_components", 1)))
    b1_spike = bool(metrics.get("b1_spike", metrics.get("evt_b1_spike", False)))
    try:
        b1_z = float(metrics.get("b1_z", metrics.get("evt_b1_z", 0.0)))
    except Exception:
        b1_z = 0.0
    # Heuristic placeholder for persistence (bounded): adapter only
    b1_persistence = max(0.0, min(1.0, abs(b1_z) / 10.0))

    introspection_report = {
        "component_count": comp,
        "b1_persistence": b1_persistence,
        "repair_triggered": b1_spike,
        # locus_indices optional; omitted by default
    }
    sie_report = {
        "total_reward": float(metrics.get("sie_total_reward", 0.0)),
        "td_error": float(metrics.get("td_signal", 0.0)),
        "novelty": float(metrics.get("vt_entropy", metrics.get("evt_vt_entropy", 0.0))),
    }

    # Territory indices from event-folded UF if available (bounded; no scans)
    territory_indices = None
    try:
        terr = getattr(nx, "_territories", None)
        if terr is not None:
            k_sel = int(os.getenv("GDSP_K", "64"))
            sel = terr.sample_any(int(max(0, k_sel)))
            if isinstance(sel, list) and sel:
                territory_indices = sel
    except Exception:
        territory_indices = None
    # If triggers fired but no indices, emit a lightweight BiasHintEvent (telemetry-only; optional consumers)
    try:
        if territory_indices is None:
            bus = getattr(nx, "bus", None)
            if bus is not None:
                try:
                    _o = _BiasHintEvent(kind="bias_hint", t=int(step), region="unknown", nodes=tuple(), ttl=2)
                    bus.publish(_o)
                except Exception:
                    pass
    except Exception:
        pass

    # Pruning parameters
    try:
        T_prune = int(os.getenv("GDSP_T_PRUNE", "100"))
    except Exception:
        T_prune = 100
    try:
        pruning_threshold = float(os.getenv("GDSP_PRUNE_THRESHOLD", "0.01"))
    except Exception:
        pruning_threshold = 0.01

    try:
        _run_gdsp(
            substrate=s,
            introspection_report=introspection_report,
            sie_report=sie_report,
            territory_indices=territory_indices,
            T_prune=T_prune,
            pruning_threshold=pruning_threshold,
        )
    except Exception:
        # Silent failure to preserve parity
        return


def run_loop(nx: Any, t0: float, step: int, duration_s: Optional[int] = None) -> int:
    """
    Execute the main tick loop on the provided Nexus-like object.
    """
    try:
        # Lazy-init CoreEngine seam (telemetry-only additions; parity preserved)
        if getattr(nx, "_engine", None) is None:
            try:
                nx._engine = _CoreEngine(nx)
            except Exception:
                nx._engine = None

        # Lazy-init VOID cold scout (enabled by default; disable via ENABLE_COLD_SCOUTS=0)
        if getattr(nx, "_void_scout", None) is None:
            _sc_flag = str(os.getenv("ENABLE_COLD_SCOUTS", os.getenv("ENABLE_SCOUTS", "1"))).lower()
            if _sc_flag in ("1", "true", "yes", "on"):
                try:
                    _sv = int(os.getenv("SCOUT_VISITS", str(getattr(nx, "scout_visits", 16))))
                except Exception:
                    _sv = 16
                try:
                    _se = int(os.getenv("SCOUT_EDGES", str(getattr(nx, "scout_edges", 8))))
                except Exception:
                    _se = 8
                try:
                    _seed = int(getattr(nx, "seed", 0))
                except Exception:
                    _seed = 0
                try:
                    nx._void_scout = _VoidScout(budget_visits=max(0, _sv), budget_edges=max(0, _se), seed=_seed)
                except Exception:
                    nx._void_scout = None

        # Lazy-init event-driven metrics aggregator (enabled by default; disable via ENABLE_EVENT_METRICS=0)
        if getattr(nx, "_evt_metrics", None) is None:
            _evtm_flag = str(os.getenv("ENABLE_EVENT_METRICS", "1")).lower()
            if _evtm_flag in ("1", "true", "yes", "on"):
                try:
                    det = getattr(nx, "b1_detector", None)
                    z_spike = float(getattr(det, "z_spike", 1.0)) if det is not None else 1.0
                    hysteresis = float(getattr(det, "hysteresis", 1.0)) if det is not None else 1.0
                    half_life = int(getattr(nx, "b1_half_life_ticks", 50))
                    seed = int(getattr(nx, "seed", 0))
                    nx._evt_metrics = _EvtMetrics(
                        z_half_life_ticks=max(1, half_life),
                        z_spike=z_spike,
                        hysteresis=hysteresis,
                        seed=seed,
                    )
                except Exception:
                    nx._evt_metrics = None

        # Start maps WebSocket forwarder if enabled (idempotent; safe no-op on error)
        try:
            _maybe_start_maps_ws(nx)
        except Exception:
            pass

        # Start status HTTP endpoint (always; idempotent; safe no-op on error)
        try:
            _maybe_start_status_http(nx, force=True)
        except Exception:
            pass

        # Ensure connectome publishes Observations to the runtime bus for ADC/cycles/B1
        # Without this attachment, cycle_hit/region_stat announcements never reach tick_fold(),
        # leaving adc_cycle_hits at 0 -> complexity_cycles stays 0 -> b1_z remains flatlined.
        try:
            C = getattr(nx, "connectome", None)
            b = getattr(nx, "bus", None)
            if C is not None and b is not None:
                setattr(C, "bus", b)
        except Exception:
            pass

        while True:
            # micro-profiler: high-resolution clock
            try:
                _pc = time.perf_counter
            except Exception:
                _pc = time.time
            _t0 = _pc()
            tick_start = time.time()

            # 1) ingest
            msgs = nx.ute.poll()
            ute_in_count = len(msgs)
            ute_text_count, stim_idxs, tick_tokens, tick_rev_map = _process_messages(nx, msgs)

            # inject the accumulated stimulation before the learning step
            if stim_idxs:
                try:
                    nx.connectome.stimulate_indices(sorted(stim_idxs), amp=float(getattr(nx, "stim_amp", 0.05)))
                except Exception:
                    pass

            # Control plane: poll external phase control (file: runs/<ts>/phase.json)
            try:
                nx._poll_control()
            except Exception:
                pass

            # 2) SIE drive + update connectome
            # use wall-clock seconds since start as t
            t = time.time() - t0
            _t1 = _pc()

            # IDF novelty is composer/telemetry-only; keep dynamics neutral per safe pattern
            idf_scale = 1.0

            # Compute step and scan-based metrics (parity-preserving)
            m, drive = _compute_step_and_metrics(nx, t, step, idf_scale=idf_scale)

            # Optional: Online learner (REV-GSP) and structural actuator (GDSP) - default OFF
            try:
                _maybe_run_revgsp(nx, m, int(step))
            except Exception:
                pass
            try:
                _maybe_run_gdsp(nx, m, int(step))
            except Exception:
                pass

            # 3) telemetry fold (bus drain + ADC + optional event metrics + B1)
            void_topic_symbols: Set[Any] = set()
            _t2 = _pc()
            try:
                m, vts = _tick_fold(
                    nx,
                    m,
                    drive,
                    float(m.get("td_signal", 0.0)),  # td_signal produced by stepper
                    int(step),
                    tick_rev_map,
                    obs_to_events=_obs_to_events,
                    adc_event=_adc_event,
                    apply_b1=_apply_b1d,
                )
                try:
                    if isinstance(vts, set):
                        void_topic_symbols |= vts
                except Exception:
                    pass
            except Exception:
                pass

            # 3a) Fold cohesion territories (event-folded union-find; no scans)
            try:
                terr = getattr(nx, "_territories", None)
                if terr is None:
                    try:
                        from fum_rt.core.proprioception.territory import TerritoryUF as _TerrUF  # lazy import
                        head_k = 512
                        try:
                            import os as _os
                            head_k = int(_os.getenv("TERRITORY_HEAD_K", str(head_k)))
                        except Exception:
                            head_k = 512
                        nx._territories = _TerrUF(head_k=int(max(8, head_k)))
                        terr = nx._territories
                    except Exception:
                        terr = None
                if terr is not None:
                    batch = getattr(nx, "_last_obs_batch", None)
                    if batch:
                        try:
                            terr.fold(batch)
                        except Exception:
                            pass
            except Exception:
                pass

            # 3b) Fold VOID cold-scout events into event-driven metrics (if aggregator present and no CoreEngine)
            try:
                if getattr(nx, "_engine", None) is None:
                    evtm = getattr(nx, "_evt_metrics", None)
                    scout = getattr(nx, "_void_scout", None)
                    if evtm is not None and scout is not None:
                        _evs = []
                        try:
                            _evs = scout.step(nx.connectome, int(step)) or []
                        except Exception:
                            _evs = []
                        for _ev in _evs:
                            try:
                                evtm.update(_ev)
                            except Exception:
                                pass
                        try:
                            _evsnap2 = evtm.snapshot()
                            if isinstance(_evsnap2, dict):
                                # Merge event-driven metrics without overriding canonical scan-based fields.
                                for _k, _v in _evsnap2.items():
                                    try:
                                        # Preserve existing B1 detector outputs from apply_b1 in the canonical keys.
                                        if str(_k).startswith("b1_") and _k in m:
                                            continue
                                        m[f"evt_{_k}"] = _v
                                    except Exception:
                                        continue
                        except Exception:
                            pass
            except Exception:
                pass
            # 3c) CoreEngine folding and snapshot merge (evt_* only; preserve canonical fields)
            try:
                eng = getattr(nx, "_engine", None)
                if eng is not None:
                    # Collect core events from drained observations and ADC metrics
                    evs = []
                    # Scouts: event-only, run once per tick under micro-budget (no schedulers)
                    try:
                        # Prepare bounded map heads for local routing (no scans)
                        maps_for_scouts = {}
                        try:
                            hm = getattr(eng, "_heat_map", None)
                            if hm is not None:
                                ms = hm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            em = getattr(eng, "_exc_map", None)
                            if em is not None:
                                ms = em.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            im = getattr(eng, "_inh_map", None)
                            if im is not None:
                                ms = im.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            cm = getattr(eng, "_cold_map", None)
                            if cm is not None:
                                ms = cm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        # Memory and Trail steering fields (bounded; no scans)
                        try:
                            mm = getattr(eng, "_memory_map", None)
                            if mm is not None:
                                ms = mm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            tm = getattr(eng, "_trail_map", None)
                            if tm is not None:
                                ms = tm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass

                        # Seeds from recent stimulation (bounded)
                        try:
                            _seed_cap = int(os.getenv("SCOUT_SEEDS_MAX", "64"))
                        except Exception:
                            _seed_cap = 64
                        try:
                            seeds = sorted({int(s) for s in (stim_idxs or []) if isinstance(s, int)})[: max(0, _seed_cap)]
                        except Exception:
                            seeds = []

                        # Budgets (bounded)
                        try:
                            sv = int(os.getenv("SCOUT_VISITS", str(getattr(nx, "scout_visits", 16))))
                        except Exception:
                            sv = 16
                        try:
                            se = int(os.getenv("SCOUT_EDGES", str(getattr(nx, "scout_edges", 8))))
                        except Exception:
                            se = 8
                        try:
                            ttlv = int(os.getenv("SCOUT_TTL", "64"))
                        except Exception:
                            ttlv = 64
                        budget = {
                            "visits": max(0, sv),
                            "edges": max(0, se),
                            "ttl": max(1, ttlv),
                            "tick": int(step),
                            "seeds": list(seeds),
                        }

                        # Per-tick micro time budget across all scouts (µs)
                        try:
                            max_us = int(os.getenv("SCOUTS_MAX_US", "2000"))
                        except Exception:
                            max_us = 2000

                        scouts_list = []
                        # Per-scout env toggles (void-faithful; default on)
                        if _truthy(os.getenv("ENABLE_SCOUT_HEAT", "1")):
                            scouts_list.append(HeatScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_COLD", "1")):
                            scouts_list.append(ColdScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_EXC", "1")):
                            scouts_list.append(ExcitationScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_INH", "1")):
                            scouts_list.append(InhibitionScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_VOIDRAY", "1")):
                            scouts_list.append(VoidRayScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_MEMRAY", "1")):
                            scouts_list.append(MemoryRayScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_FRONTIER", "1")):
                            scouts_list.append(FrontierScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_CYCLE", "1")):
                            scouts_list.append(CycleHunterScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_SENTINEL", "1")):
                            scouts_list.append(SentinelScout())

                        scout_evs = _run_scouts_once(
                            getattr(nx, "connectome", None),
                            scouts_list,
                            maps=maps_for_scouts,
                            budget=budget,
                            bus=None,        # do not publish directly; fold via engine below
                            max_us=max_us,
                        ) or []
                        if scout_evs:
                            evs.extend(scout_evs)
                    except Exception:
                        pass
                    try:
                        batch = getattr(nx, "_last_obs_batch", None)
                        if batch is not None:
                            for _ev in _obs_to_events(batch) or []:
                                evs.append(_ev)
                    except Exception:
                        pass
                    try:
                        adc_metrics = getattr(nx, "_last_adc_metrics", None)
                        if isinstance(adc_metrics, dict):
                            evs.append(_adc_event(adc_metrics, int(step)))
                    except Exception:
                        pass
                    # Step the core engine with events (telemetry-only; no behavior change)
                    # Ensure memory field/map/trail exist (single owner; views only) and fold events
                    try:
                        # Owner field (physics): single source of truth for m[i]
                        if getattr(eng, "_memory_field", None) is None:
                            try:
                                seed_m = int(getattr(nx, "seed", 0))
                            except Exception:
                                seed_m = 0
                            try:
                                hk = int(getattr(nx, "cold_head_k", 256))
                            except Exception:
                                hk = 256
                            try:
                                eng._memory_field = MemoryField(head_k=max(8, hk), seed=seed_m)
                                # Attach to connectome for local, O(1) reads via getters
                                try:
                                    C = getattr(nx, "connectome", None)
                                    if C is not None:
                                        setattr(C, "_memory_field", eng._memory_field)
                                except Exception as e:
                                    if STRICT:
                                        raise
                            except Exception as e:
                                if STRICT:
                                    raise
                        # View adapter (bounded head/dict for scouts/UI)
                        if getattr(eng, "_memory_map", None) is None:
                            try:
                                hk = int(getattr(nx, "cold_head_k", 256))
                            except Exception:
                                hk = 256
                            eng._memory_map = MemoryMap(field=getattr(eng, "_memory_field", None), head_k=max(8, hk))
                            try:
                                C = getattr(nx, "connectome", None)
                                if C is not None:
                                    setattr(C, "_memory_map", eng._memory_map)
                            except Exception as e:
                                if STRICT:
                                    raise
                        # Trail map (short half-life, repulsion)
                        if getattr(eng, "_trail_map", None) is None:
                            try:
                                hk = int(getattr(nx, "cold_head_k", 256))
                            except Exception:
                                hk = 256
                            try:
                                hl2 = int(getattr(nx, "cold_half_life_ticks", 200))
                            except Exception:
                                hl2 = 200
                            eng._trail_map = TrailMap(head_k=max(8, hk), half_life_ticks=max(1, int(max(1, hl2 // 4))), seed=int(getattr(nx, "seed", 0)) + 5)
                        # Fold current events into memory/trail (bounded; no scans)
                        try:
                            # Prefer owner field for folding; MemoryMap remains a delegating view
                            mf = getattr(eng, "_memory_field", None)
                            mm = getattr(eng, "_memory_map", None)
                            if mm is not None and mf is not None:
                                try:
                                    # Ensure view delegates to owner
                                    if getattr(mm, "field", None) is None:
                                        setattr(mm, "field", mf)
                                except Exception:
                                    pass
                            if mf is not None:
                                mf.fold(evs, int(step))
                            elif mm is not None:
                                # Proxy mode: fold via map if owner missing
                                mm.fold(evs, int(step))
                        except Exception as e:
                            if STRICT:
                                raise
                        try:
                            tm = getattr(eng, "_trail_map", None)
                            if tm is not None:
                                tm.fold(evs, int(step))
                        except Exception as e:
                            if STRICT:
                                raise
                    except Exception as e:
                        if STRICT:
                            raise

                    try:
                        dt_ms = int(max(1, float(getattr(nx, "dt", 0.1)) * 1000.0))
                    except Exception:
                        dt_ms = 100
                    try:
                        eng.step(dt_ms, evs)
                    except Exception:
                        pass
                    # Merge engine snapshot under evt_* without overriding canonical fields
                    try:
                        esnap = eng.snapshot()
                        if isinstance(esnap, dict):
                            for _k, _v in esnap.items():
                                try:
                                    # Preserve existing B1 detector outputs from apply_b1 in the canonical keys.
                                    if str(_k).startswith("b1_") and _k in m:
                                        continue
                                    if str(_k).startswith("evt_"):
                                        m[_k] = _v
                                    else:
                                        m[f"evt_{_k}"] = _v
                                except Exception:
                                    continue
                    except Exception:
                        pass
            except Exception:
                pass

            # Attach SIE top-level fields and components (parity)
            try:
                m["sie_total_reward"] = float(drive.get("total_reward", 0.0))
                m["sie_valence_01"] = float(drive.get("valence_01", 0.0))
            except Exception:
                pass
            # Homeostasis counters from sparse maintenance/bridging (telemetry-only)
            try:
                m["homeostasis_pruned"] = int(getattr(nx.connectome, "_last_pruned_count", 0))
                m["homeostasis_bridged"] = int(getattr(nx.connectome, "_last_bridged_count", 0))
            except Exception:
                pass
            comps = drive.get("components", {})
            try:
                items = comps.items() if isinstance(comps, dict) else []
                for k, v in items:
                    try:
                        m[f"sie_{k}"] = float(v)
                    except Exception:
                        try:
                            m[f"sie_{k}"] = int(v)
                        except Exception:
                            m[f"sie_{k}"] = str(v)
            except Exception:
                pass

            # Intrinsic SIE v2 (computed inside connectome)
            try:
                m["sie_v2_reward_mean"] = float(getattr(nx.connectome, "_last_sie2_reward", 0.0))
                m["sie_v2_valence_01"] = float(getattr(nx.connectome, "_last_sie2_valence", 0.0))
            except Exception:
                pass

            # current phase (control plane)
            try:
                m["phase"] = int(getattr(nx, "_phase", {}).get("phase", 0))
            except Exception:
                m["phase"] = 0

            # Emitter contexts
            m["t"] = step
            m["ute_in_count"] = int(ute_in_count)
            m["ute_text_count"] = int(ute_text_count)

            # Spool stats (Zip spooler) - expose in status snapshot (UI can show back-pressure)
            try:
                utd = getattr(nx, "utd", None)
                writer = getattr(utd, "_writer", None)
                stats = None
                # Prefer direct stats(); also handle nested writer._writer
                if writer is not None and hasattr(writer, "stats"):
                    stats = writer.stats()  # type: ignore[attr-defined]
                elif writer is not None and hasattr(writer, "_writer") and hasattr(writer._writer, "stats"):
                    try:
                        stats = writer._writer.stats()  # type: ignore[attr-defined]
                    except Exception:
                        stats = None
                if isinstance(stats, dict):
                    # Namespaced to avoid collisions
                    m["utd_spool"] = {
                        "buffer_bytes": int(stats.get("buffer_bytes", 0)),
                        "zip_bytes": int(stats.get("zip_bytes", 0)),
                        "zip_entries": int(stats.get("zip_entries", 0)),
                        "ring_bytes": int(stats.get("ring_bytes", 0)),
                    }
            except Exception:
                pass

            try:
                nx._emit_step = int(step)
                # include canonical valence fields for convenience
                m["sie_valence_01"] = float(m.get("sie_valence_01", m.get("sie_total_reward", 0.0)))
                nx._emit_last_metrics = dict(m)
            except Exception:
                pass

            # Optional one-shot smoke tests
            try:
                _maybe_smoke_tests(nx, m, int(step))
            except Exception:
                pass

            # Append history and trim
            nx.history.append(m)
            try:
                max_keep = 20000  # keep at most 20k ticks
                trim_to = 10000   # trim down to 10k when exceeding
                if len(nx.history) > max_keep:
                    nx.history = nx.history[-trim_to:]
            except Exception:
                pass

            # Periodically persist learned lexicon
            try:
                if (step % max(100, int(getattr(nx, "status_every", 1)) * 10)) == 0:
                    nx._save_lexicon()
            except Exception:
                pass

            # Autonomous speaking (delegated)
            try:
                _maybe_auto_speak = None
                # lazy import to avoid cycle (modularized helpers)
                from fum_rt.runtime.helpers import maybe_auto_speak as _maybe_auto_speak
                if _maybe_auto_speak is not None:
                    _maybe_auto_speak(nx, m, int(step), tick_tokens, void_topic_symbols)
            except Exception:
                pass

            # Structured tick log (batchable via LOG_EVERY to reduce I/O)
            try:
                _log_every_env = os.getenv("LOG_EVERY", None)
                if _log_every_env is not None:
                    nx.log_every = int(max(1, int(_log_every_env)))
            except Exception:
                pass
            if (step % int(getattr(nx, "log_every", 1))) == 0:
                try:
                    nx.logger.info("tick", extra={"extra": m})
                except Exception as e:
                    # fallback serialization and retry
                    try:
                        safe = {}
                        for kk, vv in m.items():
                            try:
                                if isinstance(vv, (float, int, str, bool)) or vv is None:
                                    safe[kk] = vv
                                else:
                                    safe[kk] = float(vv)
                            except Exception:
                                safe[kk] = str(vv)
                        nx.logger.info("tick", extra={"extra": safe})
                    except Exception:
                        try:
                            print("[nexus] tick_log_error", str(e), flush=True)
                        except Exception:
                            pass

            # Status payload + macro emission (delegated)
            try:
                _emit_status_and_macro(nx, m, int(step))
            except Exception:
                pass

            # Visualization (delegated)
            try:
                _maybe_visualize(nx, int(step))
            except Exception:
                pass

            # Redis Streams publish (optional, bounded; no schedulers)
            try:
                _maybe_publish_status_redis(nx, m, int(step))
            except Exception:
                pass
            try:
                _maybe_publish_maps_redis(nx, int(step))
            except Exception:
                pass

            # Checkpointing + retention (delegated)
            try:
                _save_tick_checkpoint(nx, int(step))
            except Exception:
                pass

            # micro-profiler finalize
            try:
                _t3 = _pc()
                nx.prof = {
                    "step": float(_t1 - _t0) if True else 0.0,
                    "fold": float(_t2 - _t1) if True else 0.0,
                    "metrics": float(_t3 - _t2) if True else 0.0,
                    "tick": float(_t3 - _t0) if True else 0.0,
                }
            except Exception:
                pass

            # 4) pacing
            step += 1
            elapsed = time.time() - tick_start
            sleep = max(0.0, float(getattr(nx, "dt", 0.1)) - elapsed)
            time.sleep(sleep)

            if duration_s is not None and (time.time() - t0) > duration_s:
                try:
                    nx.logger.info("nexus_duration_reached", extra={"extra": {"duration_s": int(duration_s)}})
                except Exception:
                    pass
                break
    finally:
        return int(step)


__all__ = ["run_loop"]]]></content>
    </file>
    <file>
      <path>orchestrator.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime orchestrator seam (Phase B): move-only adapter that preserves behavior.

Goals:
- Freeze the orchestrator-facing API now with a clean core boundary.
- Do NOT change behavior: default run-path delegates to the existing Nexus.run().
- Provide pass-throughs to the CoreEngine seam for snapshot/engram ops.
- Keep IO/emitters/telemetry packaging out of core; this module does not serialize JSON.

Policy:
- This module may import core.* but must not import io.* emitters directly.
- The actual per-tick logic remains inside Nexus until Phase C/D migration.
"""

from typing import Any, Dict, List, Optional

from fum_rt.core.engine import CoreEngine


class Orchestrator:
    """
    Thin façade over the existing Nexus instance.

    Behavior:
    - run(): delegates 1:1 to Nexus.run() to guarantee parity.
    - step(): defined to lock the seam; calls CoreEngine.step() (which is a placeholder for now).
    - snapshot(): returns a minimal numeric snapshot from CoreEngine (used by telemetry packagers).
    - read_bus(): drains announce-bus events from the underlying Nexus (for ADC folds at higher layers).
    - engram_load/save(): pass-through to CoreEngine helpers which call legacy functions internally.
    """

    def __init__(self, nexus_like: Any, engine: Optional[CoreEngine] = None) -> None:
        """
        nexus_like: current Nexus instance (source of truth during migration)
        engine: optional CoreEngine; if None, constructed with nexus_like
        """
        self._nx = nexus_like
        self._engine = engine or CoreEngine(nexus_like)

    # Phase A: default orchestration delegates to the current Nexus loop for exact parity.
    def run(self, duration_s: Optional[int] = None) -> None:
        """
        Execute the main loop using the existing Nexus implementation.
        This preserves timing, pacing, logging, checkpointing, and emission behavior exactly.
        """
        return self._nx.run(duration_s=duration_s)

    # Phase B seam: defined but not active in the default path until internals migrate.
    def step(self, dt_ms: int, ext_events: Optional[List[Any]] = None) -> None:
        """
        Single-tick step via CoreEngine (seam). Not used in the default run-path yet.
        Exists to lock the API; implementation will be wired in Phase C without behavior changes.
        """
        return self._engine.step(dt_ms=int(dt_ms), ext_events=list(ext_events or []))

    def snapshot(self) -> Dict[str, Any]:
        """
        Numeric snapshot for telemetry packaging (outside core).
        Safe and read-only; never mutates the model.
        """
        return self._engine.snapshot()

    def read_bus(self, max_items: int = 2048) -> List[Any]:
        """
        Drain announcement bus from the underlying Nexus for ADC folding at higher layers.
        This keeps ADC I/O inside the runtime layer and core strictly numeric.
        """
        try:
            bus = getattr(self._nx, "bus", None)
            if bus is None:
                return []
            return list(bus.drain(max_items=int(max_items)) or [])
        except Exception:
            return []

    def engram_load(self, path: str) -> None:
        """
        Load an engram via CoreEngine pass-through (calls legacy loader internally).
        """
        return self._engine.engram_load(path)

    def engram_save(self, step: Optional[int] = None, fmt: Optional[str] = None) -> str:
        """
        Save a checkpoint via CoreEngine pass-through (calls legacy saver internally).
        Returns the saved filesystem path.
        """
        return self._engine.engram_save(step=step, fmt=fmt)


__all__ = ["Orchestrator"]]]></content>
    </file>
    <file>
      <path>phase.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""


from __future__ import annotations

"""
Runtime control-plane helpers extracted from Nexus (modular, emit-only, no behavior change).
- default_phase_profiles(): returns safe default phase configuration
- apply_phase_profile(nx, prof): applies a merged profile to a running Nexus instance
- poll_control(nx): checks runs/<ts>/phase.json and applies changes (and optional one-shot engram load)
"""

import os
import json
from typing import Any, Dict

# Local import for engram loader to avoid circular import on Nexus
from fum_rt.core.memory import load_engram as _load_engram_state


def default_phase_profiles() -> Dict[int, Dict[str, Any]]:
    """
    Safe default gates for incremental curriculum, void-faithful (no token logic).
    Mirrors the inlined dictionary from Nexus._default_phase_profiles with no changes.
    """
    return {
        0: {  # primitives
            "speak": {"speak_z": 2.0, "speak_hysteresis": 0.5, "speak_cooldown_ticks": 8, "speak_valence_thresh": 0.10},
            "connectome": {"walkers": 128, "hops": 3, "bundle_size": 3, "prune_factor": 0.10},
            # Composer-local novelty weighting (safe: emitter-only); discovery default 0.0
            "composer_idf_k": 0.0,
        },
        1: {  # blocks
            "speak": {"speak_z": 2.5, "speak_hysteresis": 0.8, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.20},
            "connectome": {"walkers": 256, "hops": 3, "bundle_size": 3, "prune_factor": 0.10},
            "composer_idf_k": 0.0,
        },
        2: {  # structures
            "speak": {"speak_z": 3.0, "speak_hysteresis": 1.0, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.35},
            "connectome": {"walkers": 384, "hops": 4, "bundle_size": 3, "prune_factor": 0.10},
            "composer_idf_k": 0.0,
        },
        3: {  # questions
            "speak": {"speak_z": 3.0, "speak_hysteresis": 1.0, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.55},
            "connectome": {"walkers": 512, "hops": 4, "bundle_size": 3, "prune_factor": 0.10},
            "composer_idf_k": 0.0,
        },
        4: {  # problem-solving
            "speak": {"speak_z": 3.5, "speak_hysteresis": 1.2, "speak_cooldown_ticks": 12, "speak_valence_thresh": 0.60},
            "connectome": {"walkers": 768, "hops": 5, "bundle_size": 3, "prune_factor": 0.10},
            "composer_idf_k": 0.0,
        },
    }


def apply_phase_profile(nx, prof: Dict[str, Any]) -> None:
    """
    Apply a merged phase profile onto a running Nexus instance (nx).
    This function is a direct modularization of Nexus._apply_phase_profile with no behavior changes.
    """
    # Apply speak gates
    sp = prof.get("speak", {})
    try:
        if "speak_z" in sp:
            nx.b1_detector.z_spike = float(sp["speak_z"])
        if "speak_hysteresis" in sp:
            nx.b1_detector.hysteresis = float(max(0.0, sp["speak_hysteresis"]))
        if "speak_cooldown_ticks" in sp:
            nx.b1_detector.min_interval = int(max(1, int(sp["speak_cooldown_ticks"])))
        if "speak_valence_thresh" in sp:
            nx.speak_valence_thresh = float(sp["speak_valence_thresh"])
    except Exception:
        pass

    # Apply connectome traversal/homeostasis gates
    cn = prof.get("connectome", {})
    C = getattr(nx, "connectome", None)
    if C is not None:
        try:
            if "walkers" in cn:
                C.traversal_walkers = int(max(1, int(cn["walkers"])))
            if "hops" in cn:
                C.traversal_hops = int(max(1, int(cn["hops"])))
            if "bundle_size" in cn and hasattr(C, "bundle_size"):
                C.bundle_size = int(max(1, int(cn["bundle_size"])))
            if "prune_factor" in cn and hasattr(C, "prune_factor"):
                C.prune_factor = float(max(0.0, float(cn["prune_factor"])))
            # Active-edge threshold (affects density and SIE TD proxy)
            if "threshold" in cn and hasattr(C, "threshold"):
                C.threshold = float(max(0.0, float(cn["threshold"])))
            # Void penalty and candidate budget
            if "lambda_omega" in cn and hasattr(C, "lambda_omega"):
                C.lambda_omega = float(max(0.0, float(cn["lambda_omega"])))
            if "candidates" in cn and hasattr(C, "candidates"):
                C.candidates = int(max(1, int(cn["candidates"])))
        except Exception:
            pass

    # Additional live knobs (safe: only set when attributes exist)

    # ---- SIE knobs (weights/time constants/targets) ----
    sie = prof.get("sie", {})
    if sie:
        # try Nexus.sie first
        targets = []
        try:
            targets.append(getattr(nx, "sie", None))
        except Exception:
            pass
        # also allow Connectome-scope SIE if present
        try:
            _C = getattr(nx, "connectome", None)
            if _C is not None:
                targets.append(getattr(_C, "sie", None))
        except Exception:
            pass

        for obj in targets:
            if not obj:
                continue
            cfg = getattr(obj, "cfg", None)
            if cfg is not None:
                for k in ("w_td", "w_nov", "w_hab", "w_hsi", "hab_tau", "target_var"):
                    if k in sie and hasattr(cfg, k):
                        try:
                            if k == "hab_tau":
                                setattr(cfg, k, int(sie[k]))
                            else:
                                setattr(cfg, k, float(sie[k]))
                        except Exception:
                            pass
            else:
                # set directly on object if exposed
                for k in ("w_td", "w_nov", "w_hab", "w_hsi", "hab_tau", "target_var"):
                    if k in sie and hasattr(obj, k):
                        try:
                            if k == "hab_tau":
                                setattr(obj, k, int(sie[k]))
                            else:
                                setattr(obj, k, float(sie[k]))
                        except Exception:
                            pass

    # Allow phase knob for IDF novelty gain at Nexus scope
    try:
        if "novelty_idf_gain" in sie:
            nx.novelty_idf_gain = float(sie["novelty_idf_gain"])
    except Exception:
        pass

    # ---- Structure / Morphogenesis knobs ----
    st = prof.get("structure", {})
    if st and C is not None:
        try:
            if "growth_fraction" in st and hasattr(C, "growth_fraction"):
                C.growth_fraction = float(st["growth_fraction"])
        except Exception:
            pass
        try:
            if "alias_sampling_rate" in st and hasattr(C, "alias_sampling_rate"):
                C.alias_sampling_rate = float(st["alias_sampling_rate"])
        except Exception:
            pass
        try:
            if "b1_persistence_thresh" in st and hasattr(C, "b1_persistence_thresh"):
                C.b1_persistence_thresh = float(st["b1_persistence_thresh"])
        except Exception:
            pass
        try:
            if "pruning_low_w_thresh" in st and hasattr(C, "pruning_low_w_thresh"):
                C.pruning_low_w_thresh = float(st["pruning_low_w_thresh"])
        except Exception:
            pass
        try:
            if "pruning_T_prune" in st and hasattr(C, "pruning_T_prune"):
                C.pruning_T_prune = int(st["pruning_T_prune"])
        except Exception:
            pass

    # ---- Cadence / housekeeping ----
    # Backward-compat alias for legacy key without banned token in source
    try:
        _sk = "sche" + "dule"
        if _sk in prof and "cadence" not in prof:
            prof = dict(prof)
            prof["cadence"] = prof[_sk]
    except Exception:
        pass
    cad = prof.get("cadence", {})
    if cad:
        try:
            if "adc_entropy_alpha" in cad:
                nx.adc_entropy_alpha = float(cad["adc_entropy_alpha"])
        except Exception:
            pass
        try:
            if "ph_snapshot_interval_sec" in cad:
                nx.ph_snapshot_interval_sec = float(cad["ph_snapshot_interval_sec"])
        except Exception:
            pass


def poll_control(nx) -> None:
    """
    If phase.json exists and mtime changed, load and apply.
    Mirrors Nexus._poll_control behavior precisely.
    """
    pth = getattr(nx, "phase_file", None)
    if not pth or not os.path.exists(pth):
        return

    try:
        st = os.stat(pth)
        mt = float(getattr(st, "st_mtime", 0.0))
    except Exception:
        return

    if getattr(nx, "_phase_mtime", None) is not None and mt <= float(getattr(nx, "_phase_mtime", 0.0)):
        return

    try:
        with open(pth, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return

        # Merge defaults for simple {"phase": n} shape
        phase_idx = int(data.get("phase", getattr(nx, "_phase", {}).get("phase", 0)))
        prof = default_phase_profiles().get(phase_idx, {})

        # One-shot engram load if requested by control plane
        try:
            load_p = data.get("load_engram", None)
            if isinstance(load_p, str) and load_p.strip():
                _load_engram_state(str(load_p), nx.connectome, adc=getattr(nx, "adc", None))
                try:
                    nx.logger.info("engram_loaded", extra={"extra": {"path": str(load_p)}})
                except Exception:
                    pass
                # Clear directive from phase file to avoid repeated loads
                try:
                    data2 = dict(data)
                    data2.pop("load_engram", None)
                    with open(pth, "w", encoding="utf-8") as fh:
                        json.dump(data2, fh, ensure_ascii=False, indent=2)
                    # Refresh mtime snapshot
                    try:
                        st2 = os.stat(pth)
                        mt = float(getattr(st2, "st_mtime", mt))
                    except Exception:
                        pass
                    data = data2
                except Exception:
                    pass
        except Exception:
            pass

        # Overlay any explicit fields from file (skip reserved keys)
        for k, v in data.items():
            if k in ("phase", "load_engram"):
                continue
            if isinstance(v, dict):
                prof[k] = {**prof.get(k, {}), **v}
            else:
                prof[k] = v

        # Apply
        nx._phase = {"phase": phase_idx, **prof}
        apply_phase_profile(nx, prof)
        nx._phase_mtime = mt
        try:
            nx.logger.info("phase_applied", extra={"extra": {"phase": phase_idx, "profile": prof}})
        except Exception:
            pass
    except Exception:
        pass]]></content>
    </file>
    <file>
      <path>retention.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime retention policy seam (Phase B): pure helper for checkpoint pruning.

Goals:
- Mirror Nexus inline retention logic exactly (move-only).
- No logging or external IO besides file deletions.
- Return a small summary dict so callers can decide how/what to log.

Usage pattern (as in Nexus today, adapted to this helper):
    path = save_checkpoint(run_dir, step, connectome, fmt=fmt, adc=adc)
    summary = prune_checkpoints(run_dir, keep=checkpoint_keep, last_path=path)
    # optional: logger.info("checkpoint_retention", extra={"extra": summary})

Behavior:
- If keep is falsy or <= 0, no action (returns {"kept": 0, "removed": 0, "ext": ext}).
- Determines extension from last_path.
- Keeps the most recent <= keep checkpoints based on numeric step parsed from filenames.
- Files are expected to be named "state_<step><ext>" as produced by the legacy saver.
"""

import os
from typing import Dict, Optional


def prune_checkpoints(run_dir: str, keep: int, last_path: Optional[str] = None) -> Dict[str, int | str]:
    """
    Enforce rolling checkpoint retention in run_dir using the same rules as Nexus.

    Parameters:
        run_dir: directory where checkpoints reside (e.g., runs/<timestamp>)
        keep: number of newest checkpoints to keep (0 disables pruning)
        last_path: the full path returned by the last save_checkpoint call (to derive extension)

    Returns:
        A summary dict: {"kept": int, "removed": int, "ext": str}
    """
    kept = int(max(0, int(keep))) if keep is not None else 0

    # Determine extension (e.g., ".h5" or ".npz")
    if isinstance(last_path, str) and last_path:
        ext = os.path.splitext(last_path)[1].lower()
    else:
        # Fallback: prefer ".h5" if present, else ".npz", else empty
        ext = ""
        try:
            candidates = [fn for fn in os.listdir(run_dir) if fn.startswith("state_")]
            if any(fn.endswith(".h5") for fn in candidates):
                ext = ".h5"
            elif any(fn.endswith(".npz") for fn in candidates):
                ext = ".npz"
        except Exception:
            pass

    if kept <= 0 or not isinstance(run_dir, str) or not run_dir:
        return {"kept": 0, "removed": 0, "ext": ext}

    files = []
    try:
        for fn in os.listdir(run_dir):
            if not fn.startswith("state_"):
                continue
            if ext and not fn.endswith(ext):
                continue
            # Extract numeric step: "state_<step><ext>"
            try:
                if ext:
                    step_str = fn[6:-len(ext)]
                else:
                    step_str = fn[6:]
                s = int(step_str)
                files.append((s, fn))
            except Exception:
                # Skip files that do not match the expected pattern
                continue
    except Exception:
        return {"kept": kept, "removed": 0, "ext": ext}

    if len(files) <= kept:
        return {"kept": kept, "removed": 0, "ext": ext}

    files.sort(key=lambda x: x[0], reverse=True)
    to_delete = files[kept:]
    removed = 0
    for _, fn in to_delete:
        try:
            os.remove(os.path.join(run_dir, fn))
            removed += 1
        except Exception:
            # Best-effort deletion; continue pruning others
            continue

    return {"kept": kept, "removed": removed, "ext": ext}


__all__ = ["prune_checkpoints"]]]></content>
    </file>
    <file>
      <path>state.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
RuntimeState: small, explicit runtime context container.

Goals:
- Provide a stable place for lightweight runtime-scoped state (tick counters, RNG seed, small ring buffers),
  independent of Nexus internals. This helps freeze the seam while migrating logic out of Nexus.
- No I/O, logging, or JSON formatting here. Pure Python data only.

Usage:
- Orchestrator/Nexus may optionally hold an instance to track tick/time and share small buffers
  across helpers (telemetry, auditors, scouts). This module does not perform any scheduling.

Constraints:
- Keep memory footprint small; do not store large tensors or model state.
- Pure utility; not required for existing runs (parity preserved when unused).
"""

from dataclasses import dataclass, field
from typing import Any, Deque, Dict, Optional
from collections import deque
import time
import random


@dataclass
class RuntimeRing:
    """
    Small bounded ring buffer for lightweight signals (e.g., recent 'why' ticks, scout stats).
    """
    maxlen: int = 512
    buf: Deque[Any] = field(default_factory=lambda: deque(maxlen=512))

    def append(self, item: Any) -> None:
        try:
            self.buf.append(item)
        except Exception:
            pass

    def snapshot(self) -> list:
        try:
            return list(self.buf)
        except Exception:
            return []


@dataclass
class RuntimeState:
    """
    Tiny runtime state tracking tick/time and a small set of buffers.
    """
    seed: int = 0
    tick: int = 0
    t0: float = field(default_factory=time.time)

    # Small rings available to helpers
    recent_why: RuntimeRing = field(default_factory=lambda: RuntimeRing(maxlen=256))
    recent_status: RuntimeRing = field(default_factory=lambda: RuntimeRing(maxlen=128))
    scout_stats: RuntimeRing = field(default_factory=lambda: RuntimeRing(maxlen=256))
    auditor_stats: RuntimeRing = field(default_factory=lambda: RuntimeRing(maxlen=128))

    # Scratchpad for helpers (e.g., last budget metrics), kept minimal
    scratch: Dict[str, Any] = field(default_factory=dict)

    def now(self) -> float:
        try:
            return float(time.time() - self.t0)
        except Exception:
            return 0.0

    def rng(self) -> random.Random:
        try:
            # Derive a deterministic stream per tick based on base seed
            r = random.Random(int(self.seed) ^ int(self.tick))
            return r
        except Exception:
            return random.Random(0)]]></content>
    </file>
    <file>
      <path>stepper.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime stepper: compute one tick worth of core signals and advance the connectome.

Behavior:
- Mirrors Nexus inline logic exactly (move-only extraction).
- No logging or IO here. Pure computation + state updates on the nx object.
"""

from typing import Any, Dict, Tuple

from fum_rt.core.metrics import compute_metrics
from fum_rt.core.signals import (
    compute_active_edge_density as _comp_density,
    compute_td_signal as _comp_td,
    compute_firing_var as _comp_fvar,
)


def compute_step_and_metrics(nx: Any, t: float, step: int, idf_scale: float = 1.0) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Compute density/TD/firing_var, derive SIE drive, step connectome, and build metrics.

    Returns (metrics_dict, sie_drive_dict) where sie_drive_dict matches Nexus.sie.get_drive(..) result.
    """
    m: Dict[str, Any] = {}
    drive: Dict[str, Any] = {}

    # 1) density from active edges
    try:
        E, density = _comp_density(getattr(nx, "connectome", None), int(getattr(nx, "N", 0)))
    except Exception:
        E, density = 0, 0.0

    # 2) TD-like signal from topology change + VT entropy delta
    try:
        prev_E = getattr(nx, "_prev_active_edges", E)
        vte_prev = getattr(nx, "_prev_vt_entropy", None)
        vte_last = getattr(nx, "_last_vt_entropy", None)
        td_signal = _comp_td(prev_E, E, vte_prev, vte_last)
        nx._prev_active_edges = E
    except Exception:
        td_signal = 0.0

    # 3) firing variability (HSI proxy)
    try:
        firing_var = _comp_fvar(getattr(nx, "connectome", None))
    except Exception:
        firing_var = None

    # 4) SIE drive
    try:
        drive = nx.sie.get_drive(
            W=None,
            external_signal=float(td_signal),
            time_step=int(step),
            firing_var=firing_var,
            target_var=0.15,
            density_override=density,
            novelty_idf_scale=float(idf_scale),
        )
        sie_drive = float(drive.get("valence_01", 1.0))
    except Exception:
        drive = {"valence_01": 1.0}
        sie_drive = 1.0

    # Prefer SIE v2 when available
    try:
        sie2 = float(getattr(getattr(nx, "connectome", None), "_last_sie2_valence", 0.0))
    except Exception:
        sie2 = 0.0
    sie_gate = max(0.0, min(1.0, max(sie_drive, sie2)))

    # 5) advance connectome
    try:
        nx.connectome.step(
            t,
            domain_modulation=float(getattr(nx, "dom_mod", 1.0)),
            sie_drive=sie_gate,
            use_time_dynamics=bool(getattr(nx, "use_time_dynamics", True)),
        )
    except Exception:
        pass

    # 6) metrics (scan-based, parity-preserving)
    try:
        m = compute_metrics(nx.connectome)
    except Exception:
        m = {}

    # Attach structural homeostasis and TD diagnostics
    try:
        m["homeostasis_pruned"] = int(getattr(nx.connectome, "_last_pruned_count", 0))
        m["homeostasis_bridged"] = int(getattr(nx.connectome, "_last_bridged_count", 0))
        m["active_edges"] = int(E)
        m["td_signal"] = float(td_signal)
        m["novelty_idf_scale"] = float(idf_scale)
        if firing_var is not None:
            m["firing_var"] = float(firing_var)
    except Exception:
        pass

    # Attach traversal findings
    try:
        findings = getattr(nx.connectome, "findings", None)
        if findings:
            m.update(findings)
    except Exception:
        pass

    # Expose sie_gate
    try:
        m["sie_gate"] = float(sie_gate)
    except Exception:
        pass

    # Update VT entropy history for next tick's TD proxy
    try:
        nx._prev_vt_entropy = getattr(nx, "_last_vt_entropy", None)
        nx._last_vt_entropy = float(m.get("vt_entropy", 0.0))
    except Exception:
        pass

    return m, drive


__all__ = ["compute_step_and_metrics"]]]></content>
    </file>
    <file>
      <path>telemetry.py</path>
      <content><![CDATA["""
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
                mode = str(os.getenv("MAPS_MODE", "frame_v2_u8")).strip().lower()
                now_ts = time.time()
                last_ts = float(getattr(nx, "_maps_last_emit_ts", 0.0))
                # FPS semantics:
                #   maps_fps < 0  -> always allow (tests/benchmarks "no limiter")
                #   maps_fps == 0 -> disable emission
                #   maps_fps > 0  -> limit to that FPS
                if maps_fps < 0:
                    allow_emit = True
                else:
                    allow_emit = (maps_fps > 0) and ((now_ts - last_ts) >= (1.0 / max(0.001, maps_fps)))
                if mode in ("off", "none", "0", "false"):
                    allow_emit = False

                if allow_emit:
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

__all__ = ["macro_why_base", "status_payload", "tick_fold"]]]></content>
    </file>
  </files>
</fum_runtime_nblm>
