from __future__ import annotations

import os
import math
from typing import Tuple, Optional
import plotly.graph_objs as go

from fum_rt.frontend.utilities.tail import tail_jsonl_bytes
from fum_rt.frontend.models.series import SeriesState, append_event, append_say, ffill, extract_tick
from fum_rt.frontend.services.status_client import get_status_snapshot as _get_status


def compute_dashboard_figures(run_dir: str, state: Optional[SeriesState], ui: Optional[dict] = None) -> Tuple[go.Figure, go.Figure, SeriesState]:
    """
    Pure controller for figure construction.
    - Stateless inputs: run_dir, prior state (SeriesState or None)
    - UI dict: optional caps and toggles from in-app controls (no env needed)
    - Returns: (fig_dashboard, fig_discovery, new_state)
    """
    if state is None or getattr(state, "run_dir", None) != run_dir:
        state = SeriesState(run_dir)
    ui = ui or {}

    # Prefer HTTP status snapshot; fallback to cheap file tails if unavailable.
    # Detect truncation/rotation or run restart remains supported via tick/time regression.
    prev_es = getattr(state, "events_size", 0)
    prev_us = getattr(state, "utd_size", 0)
    new_events, esize = [], prev_es
    new_utd, usize = [], prev_us

    snap = None
    try:
        url = None
        timeout_s = None
        try:
            _u = ui.get("status_url") if isinstance(ui, dict) else None
            if isinstance(_u, str) and _u:
                url = _u
        except Exception:
            pass
        try:
            _ts = ui.get("status_timeout") if isinstance(ui, dict) else None
            if _ts is not None:
                timeout_s = float(_ts)
        except Exception:
            pass
        snap = _get_status(url, timeout_s)
    except Exception:
        snap = None

    # Honor UI preference: use HTTP snapshot only when requested; otherwise allow bounded file tails.
    # Default: False (allow file tails) so graphs populate even before ui-state is ready.
    charts_http_only = False
    try:
        charts_http_only = bool(ui.get("charts_http_only", False))
    except Exception:
        charts_http_only = False

    if isinstance(snap, dict) and snap:
        # Use snapshot directly as an "event-like" record; append_event() reads from the dict.
        new_events = [snap]
    elif not charts_http_only:
        # Fallback: tail events.jsonl and utd_events.jsonl incrementally (bounded by last offsets).
        try:
            epath = os.path.join(run_dir, "events.jsonl")
            if os.path.exists(epath):
                new_events, esize = tail_jsonl_bytes(epath, prev_es)
        except Exception:
            new_events, esize = [], prev_es
        try:
            upath = os.path.join(run_dir, "utd_events.jsonl")
            if os.path.exists(upath):
                new_utd, usize = tail_jsonl_bytes(upath, prev_us)
        except Exception:
            new_utd, usize = [], prev_us
    else:
        # Keep empty tails; rely on HTTP to populate when available.
        new_events, new_utd = [], []
        esize, usize = prev_es, prev_us

    # Reset conditions:
    truncated = (prev_es > 0 and esize < prev_es) or (prev_us > 0 and usize < prev_us)

    # 1) Explicit run restart marker from backend (logged at nexus start)
    restart_marker = False
    try:
        for rec in new_events:
            name = str(
                rec.get("event_type")
                or rec.get("event")
                or rec.get("message")
                or rec.get("msg")
                or rec.get("name")
                or ""
            ).lower()
            if name in ("nexus_started", "engram_loaded"):
                restart_marker = True
                break
    except Exception:
        pass

    # 2) Tick regression (incoming ticks lower than last known)
    tick_regression = False
    try:
        last_t = state.t[-1] if state.t else None
        if last_t is not None:
            min_new_t = None
            for rec in new_events:
                tv = extract_tick(rec)
                if tv is None:
                    continue
                tv = int(tv)
                if min_new_t is None or tv < min_new_t:
                    min_new_t = tv
            if min_new_t is not None and min_new_t < last_t:
                tick_regression = True
    except Exception:
        pass

    if truncated or restart_marker or tick_regression:
        # Clear buffers while keeping run_dir; prevents graph overlay on resume/restart.
        # Also advance offsets to current EOF so we don't re-ingest old tail data.
        try:
            state.__post_init__()  # re-init SeriesState buffers and counters
            state.events_size = esize
            state.utd_size = usize
            new_events = []
            new_utd = []
        except Exception:
            pass

    # Apply tails after optional reset
    for rec in new_events:
        append_event(state, rec)
    for rec in new_utd:
        append_say(state, rec)
    state.events_size = esize
    state.utd_size = usize

    # Bound buffers (UI-tunable; no env)
    try:
        MAXP = int(ui.get("maxp", 1200))
    except Exception:
        MAXP = 1200
    if len(state.t) > MAXP:
        state.t = state.t[-MAXP:]
        state.active = state.active[-MAXP:]
        state.avgw = state.avgw[-MAXP:]
        state.coh = state.coh[-MAXP:]
        state.comp = state.comp[-MAXP:]
        state.b1z = state.b1z[-MAXP:]
        state.val = state.val[-MAXP:]
        state.val2 = state.val2[-MAXP:]
        state.entro = state.entro[-MAXP:]
    # Speak tick overlay window (fixed UI-default)
    MAX_SAY = 800
    if len(state.speak_ticks) > MAX_SAY:
        state.speak_ticks = state.speak_ticks[-MAX_SAY:]

    # Forward-fill holes
    t = state.t
    active = ffill(state.active)
    avgw = ffill(state.avgw)
    coh = ffill(state.coh)
    comp = ffill(state.comp)
    b1z = ffill(state.b1z)
    val = ffill(state.val)
    val2 = ffill(state.val2)
    entro = ffill(state.entro)

    # Optional decimation to bound plotting work (UI-only). Applied after MAXP slicing.
    # Env:
    #   DASH_DECIMATE_TO = 0 (off) or N (target max plotted points per series)
    try:
        DEC_TO = int(ui.get("decimate", 600))
    except Exception:
        DEC_TO = 600
    if DEC_TO > 0 and len(t) > DEC_TO:
        stride = max(1, int(math.ceil(len(t) / float(DEC_TO))))
        def _dec(seq):
            return seq[::stride] if stride > 1 else seq
        t = t[::stride]
        active = _dec(active)
        avgw = _dec(avgw)
        coh = _dec(coh)
        comp = _dec(comp)
        b1z = _dec(b1z)
        val = _dec(val)
        val2 = _dec(val2)
        entro = _dec(entro)

    # Palette (env-overridable)
    def _env_color(k: str, default: str) -> str:
        try:
            v = os.getenv(f"DASH_COLOR_{k.upper()}", "").strip()
            return v if v else default
        except Exception:
            return default

    C = {
        "synapses": _env_color("synapses", "#7aa2c7"),
        "avgw": _env_color("avgw", "#9ab8d1"),
        "valence": _env_color("valence", "#c39b70"),
        "valence2": _env_color("valence2", "#8bb995"),
        "components": _env_color("components", "#b68484"),
        "cycles": _env_color("cycles", "#a08878"),
        "b1z": _env_color("b1z", "#76b0a7"),
        "entropy": _env_color("entropy", "#a495c7"),
        "speak_line": _env_color("speak_line", "rgba(120,180,120,0.45)"),
    }

    # fig1
    fig1 = go.Figure()
    # Enforce series_cap (UI control; default 6). Prioritize essential series first.
    try:
        SERIES_CAP = int(ui.get("series_cap", 6))
    except Exception:
        SERIES_CAP = 6
    SERIES_CAP = max(1, min(8, SERIES_CAP))

    add_count = 0
    def _add_if(cond: bool, fn) -> None:
        nonlocal add_count
        if add_count >= SERIES_CAP:
            return
        if cond:
            fn()
            add_count += 1

    # Priority order: Active, Cycles, AvgW, B1z, Components, Valence, Valence2, Entropy
    _add_if(True, lambda: fig1.add_trace(
        go.Scattergl(x=t, y=active, name="Active synapses", line=dict(width=1, color=C["synapses"]))
    ))
    _add_if(True, lambda: fig1.add_trace(
        go.Scattergl(x=t, y=comp, name="Cycles", yaxis="y4", line=dict(width=1, color=C["cycles"]))
    ))
    _add_if(True, lambda: fig1.add_trace(
        go.Scattergl(x=t, y=avgw, name="Avg W", yaxis="y2", line=dict(width=1, color=C["avgw"]))
    ))
    _add_if(True, lambda: fig1.add_trace(
        go.Scattergl(x=t, y=b1z, name="B1 z", yaxis="y5", line=dict(width=1, color=C["b1z"]))
    ))
    _add_if(True, lambda: fig1.add_trace(
        go.Scattergl(x=t, y=coh, name="Components", yaxis="y3", line=dict(width=1, color=C["components"]))
    ))
    _add_if(any(v is not None for v in val), lambda: fig1.add_trace(
        go.Scattergl(x=t, y=val, name="SIE valence", yaxis="y2", line=dict(width=1, dash="dot", color=C["valence"]))
    ))
    _add_if(any(v is not None for v in val2), lambda: fig1.add_trace(
        go.Scattergl(x=t, y=val2, name="SIE v2 valence", yaxis="y2", line=dict(width=1, dash="dash", color=C["valence2"]))
    ))
    _add_if(any(v is not None for v in entro), lambda: fig1.add_trace(
        go.Scattergl(x=t, y=entro, name="Connectome entropy", yaxis="y6", line=dict(width=1, color=C["entropy"]))
    ))
    fig1.update_layout(
        title=f"Dashboard - {os.path.basename(run_dir)}",
        paper_bgcolor="#10151c",
        plot_bgcolor="#0f141a",
        font=dict(color="#cfd7e3"),
        xaxis=dict(domain=[0.05, 0.95], title="Tick", gridcolor="#233140", zerolinecolor="#233140"),
        yaxis=dict(title="Active synapses", side="left", gridcolor="#233140", zerolinecolor="#233140"),
        yaxis2=dict(overlaying="y", side="right", title="Avg W / Valence", showgrid=False, zeroline=False),
        yaxis3=dict(overlaying="y", side="left", position=0.02, showticklabels=False, showgrid=False, zeroline=False),
        yaxis4=dict(overlaying="y", side="right", position=0.98, showticklabels=False, showgrid=False, zeroline=False),
        yaxis5=dict(overlaying="y", side="right", position=0.96, showticklabels=False, showgrid=False, zeroline=False),
        yaxis6=dict(overlaying="y", side="left", position=0.04, showticklabels=False, showgrid=False, zeroline=False),
        legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=20, t=40, b=40),
    )

    # fig2
    fig2 = go.Figure()
    fig2.add_trace(go.Scattergl(x=t, y=comp, name="Cycle hits", line=dict(width=1, color=C["cycles"])))
    for tk in state.speak_ticks[-200:]:
        fig2.add_vline(x=tk, line_width=1, line_dash="dash", line_color=C["speak_line"])
    fig2.add_trace(go.Scattergl(x=t, y=b1z, name="B1 z", yaxis="y2", line=dict(width=1, color=C["b1z"])))
    fig2.update_layout(
        title="Cycle Hits & B1 z",
        paper_bgcolor="#10151c",
        plot_bgcolor="#0f141a",
        font=dict(color="#cfd7e3"),
        xaxis=dict(title="Tick", gridcolor="#233140", zerolinecolor="#233140"),
        yaxis=dict(title="Cycle hits", gridcolor="#233140", zerolinecolor="#233140"),
        yaxis2=dict(overlaying="y", side="right", title="B1 z", showgrid=False, zeroline=False),
        legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=20, t=40, b=40),
    )

    return fig1, fig2, state