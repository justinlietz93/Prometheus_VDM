from __future__ import annotations

import os
from typing import Tuple, Optional
import plotly.graph_objs as go

from fum_rt.frontend.utilities.tail import tail_jsonl_bytes
from fum_rt.frontend.models.series import SeriesState, append_event, append_say, ffill, extract_tick


def compute_dashboard_figures(run_dir: str, state: Optional[SeriesState]) -> Tuple[go.Figure, go.Figure, SeriesState]:
    """
    Pure controller for figure construction.
    - Stateless inputs: run_dir, prior state (SeriesState or None)
    - Returns: (fig_dashboard, fig_discovery, new_state)

    This isolates all business logic away from Dash callbacks so other callers
    (e.g., CLI previewers, batch exporters) can reuse the same computation.
    """
    if state is None or getattr(state, "run_dir", None) != run_dir:
        state = SeriesState(run_dir)

    # Stream append events; detect truncation/rotation or run restart to avoid overlay
    prev_es = getattr(state, "events_size", 0)
    new_events, esize = tail_jsonl_bytes(state.events_path, prev_es)
    prev_us = getattr(state, "utd_size", 0)
    new_utd, usize = tail_jsonl_bytes(state.utd_path, prev_us)

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

    # Bound buffers
    MAXP = 2000
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
    if len(state.speak_ticks) > 800:
        state.speak_ticks = state.speak_ticks[-800:]

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

    # Palette
    C = {
        "synapses": "#7aa2c7",
        "avgw": "#9ab8d1",
        "valence": "#c39b70",
        "valence2": "#8bb995",
        "components": "#b68484",
        "cycles": "#a08878",
        "b1z": "#76b0a7",
        "entropy": "#a495c7",
        "speak_line": "rgba(120,180,120,0.45)",
    }

    # fig1
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t, y=active, name="Active synapses", line=dict(width=1, color=C["synapses"])))
    fig1.add_trace(go.Scatter(x=t, y=avgw, name="Avg W", yaxis="y2", line=dict(width=1, color=C["avgw"])))
    if any(v is not None for v in val):
        fig1.add_trace(go.Scatter(x=t, y=val, name="SIE valence", yaxis="y2", line=dict(width=1, dash="dot", color=C["valence"])))
    if any(v is not None for v in val2):
        fig1.add_trace(go.Scatter(x=t, y=val2, name="SIE v2 valence", yaxis="y2", line=dict(width=1, dash="dash", color=C["valence2"])))
    fig1.add_trace(go.Scatter(x=t, y=coh, name="Components", yaxis="y3", line=dict(width=1, color=C["components"])))
    fig1.add_trace(go.Scatter(x=t, y=comp, name="Cycles", yaxis="y4", line=dict(width=1, color=C["cycles"])))
    fig1.add_trace(go.Scatter(x=t, y=b1z, name="B1 z", yaxis="y5", line=dict(width=1, color=C["b1z"])))
    if any(v is not None for v in entro):
        fig1.add_trace(go.Scatter(x=t, y=entro, name="Connectome entropy", yaxis="y6", line=dict(width=1, color=C["entropy"])))
    fig1.update_layout(
        title=f"Dashboard — {os.path.basename(run_dir)}",
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
    fig2.add_trace(go.Scatter(x=t, y=comp, name="Cycle hits", line=dict(width=1, color=C["cycles"])))
    for tk in state.speak_ticks[-200:]:
        fig2.add_vline(x=tk, line_width=1, line_dash="dash", line_color=C["speak_line"])
    fig2.add_trace(go.Scatter(x=t, y=b1z, name="B1 z", yaxis="y2", line=dict(width=1, color=C["b1z"])))
    fig2.update_layout(
        title="Discovery & Self‑Speak",
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