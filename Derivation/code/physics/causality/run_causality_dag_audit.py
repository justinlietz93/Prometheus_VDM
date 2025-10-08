#!/usr/bin/env python3
"""
Order-only Causal DAG Audit Runner

Ingests JSONL event streams, constructs an order-only DAG, samples Alexandrov
intervals, estimates an effective dimension from ordering fraction, and fits
diamond scaling |I| vs Δt on a log–log plot.

Artifacts are written via common.io_paths with policy-aware quarantine routing.
Approval is enforced via common.authorization.approval.check_tag_approval.

Inputs
- --events: path to events.jsonl or a directory of shards (scans for *.jsonl, *.jsonl.gz)
- --utd-events: optional path to utd_events.jsonl (model outputs) or a directory
- --tag: approval tag (default: v1)
- --allow-unapproved: bypass approval for engineering-only smoke (artifacts quarantined)

Notes
- JSONL rows may contain fields: {id|event_id}, {t|time|timestamp}, parents (list), stream/kind
- We accept gzip-compressed files with .gz; zstd is not yet supported.
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import os
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Set, Any, TYPE_CHECKING
from dataclasses import dataclass
import sys

# Ensure common helpers on path (Derivation/code)
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
	sys.path.insert(0, str(CODE_ROOT))

from common.authorization.approval import (
	check_tag_approval,
)
from common.io_paths import (
	build_slug,
	log_path_by_tag,
	write_log,
)
from common.data.results_db import (
	begin_run,
	add_artifacts,
	log_metrics,
	end_run_success,
	end_run_failed,
)
from common.causality.event_dag import (
	build_event_dag,
	is_acyclic,
	transitive_reduction,
)
from common.causality.intervals import (
	sample_intervals,
	dim_from_order_fraction,
	fit_diamond_scaling,
)

from common.plotting.core import (
	apply_style,
	get_fig_ax,
	sanitize_for_log,
	save_figure,
)


DOMAIN = "causality"
SCRIPT_NAME = "run_causality_dag_audit"

if TYPE_CHECKING:
	import pandas as pd  # type: ignore


def _iter_jsonl(path: Path) -> Iterator[dict]:
	"""Stream JSON objects from a .jsonl or .jsonl.gz file.

	Skips malformed lines with a small warning for robustness.
	"""
	opener: Any
	if str(path).endswith(".gz"):
		opener = gzip.open  # type: ignore
		mode = "rt"
	else:
		opener = open  # type: ignore
		mode = "r"
	try:
		with opener(path, mode, encoding="utf-8", errors="ignore") as f:  # type: ignore[arg-type]
			for i, line in enumerate(f, start=1):
				s = line.strip()
				if not s:
					continue
				obj: Optional[dict]
				try:
					obj = json.loads(s)
				except Exception as e:
					print(f"[causality] Warning: JSON parse error in {path} line {i}: {e}")
					obj = None
				if obj is not None:
					yield obj
	except FileNotFoundError:
		print(f"[causality] Warning: file not found: {path}")


def _discover_files(p: Path) -> List[Path]:
	if p.is_file():
		return [p]
	files: List[Path] = []
	if p.is_dir():
		for ext in ("*.jsonl", "*.jsonl.gz"):
			files.extend(sorted(p.glob(ext)))
	return files


@dataclass
class AuditSpec:
	events: Path
	utd_events: Optional[Path]
	tag: str = "v1"
	name: str = "dag_audit"
	infer_by_time: bool = False
	max_successors: int = 0
	time_tol: float = 0.0
	k: int = 256
	min_dt: float = 0.0
	max_dt: Optional[float] = None
	reach_budget: int = 8192
	streams: Optional[Set[str]] = None
	max_events: Optional[int] = None
	# Flexible key handling
	id_key: Optional[str] = None        # dot-path, e.g., "meta.id"
	time_key: Optional[str] = None      # dot-path, e.g., "meta.ts_ns"
	time_scale: str = "auto"           # one of {auto,1,1e-3,1e-6,1e-9}
	step_key: Optional[str] = None      # if no time, use integer step index
	step_dt: Optional[float] = None     # seconds per step (requires step_key)
	# Neuron head expansion: expand evt_*_head arrays into per-neuron events
	expand_heads: Optional[Set[str]] = None  # subset of {"heat","exc","inh"}; None or empty disables
	# Trail chaining (within-tick): optionally add edges along the trail ranking to emulate walker path
	trail_chain: bool = False
	trail_topk: Optional[int] = None
	trail_minval: Optional[float] = None
	# Macro DAG controls
	macro_dag: bool = True
	macro_lags: int = 2
	macro_alpha: float = 0.01


def _get_nested(obj: dict, path: str) -> Any:
	cur: Any = obj
	for part in path.split('.'):
		if isinstance(cur, dict) and part in cur:
			cur = cur[part]
		else:
			return None
	return cur


def _normalize_event_id(obj: dict, *, id_key: Optional[str] = None) -> Optional[str]:
	if id_key:
		v = _get_nested(obj, id_key)
		if v is not None:
			try:
				return str(v)
			except Exception:
				return None
	# Heuristic: common composite keys for neuron events (e.g., neuron + event index)
	neuron_like = None
	for nk in ("neuron", "neuron_id", "neuron_idx", "neuron_index"):
		v = obj.get(nk)
		if v is not None:
			neuron_like = str(v)
			break
	if neuron_like is not None:
		for ik in ("i", "event_index", "idx", "index"):
			iv = obj.get(ik)
			if iv is not None:
				return f"{neuron_like}:{iv}"
	# Single-key aliases
	for k in ("id", "event_id", "eid", "i", "event_index", "idx", "index", "neuron", "neuron_id", "neuron_idx", "neuron_index", "t"):
		if k in obj and obj[k] is not None:
			try:
				return str(obj[k])
			except Exception:
				return None
	# Fallback: nested payload (e.g., UTD records {type, payload:{t,...}})
	try:
		payload = obj.get("payload")
		if isinstance(payload, dict):
			# Repeat alias search within payload
			for k in ("id", "event_id", "eid", "i", "event_index", "idx", "index", "neuron", "neuron_id", "neuron_idx", "neuron_index", "t"):
				if k in payload and payload[k] is not None:
					try:
						return str(payload[k])
					except Exception:
						return None
			# Composite within payload
			neuron_like = None
			for nk in ("neuron", "neuron_id", "neuron_idx", "neuron_index"):
				v = payload.get(nk)
				if v is not None:
					neuron_like = str(v)
					break
			if neuron_like is not None:
				for ik in ("i", "event_index", "idx", "index"):
					iv = payload.get(ik)
					if iv is not None:
						return f"{neuron_like}:{iv}"
	except Exception as _e:
		# Fallback path failed; leave ID unresolved
		_ = _e
	return None


def _normalize_time(obj: dict, *, time_key: Optional[str] = None, time_scale: str = "auto") -> Optional[float]:
	def _scale(v: float) -> float:
		if time_scale == "1":
			return v
		if time_scale == "1e-3":
			return v * 1e-3
		if time_scale == "1e-6":
			return v * 1e-6
		if time_scale == "1e-9":
			return v * 1e-9
		# auto: detect by magnitude for ints
		if isinstance(orig, int):
			if orig > 1e14:
				return v * 1e-9  # ns -> s
			if orig > 1e11:
				return v * 1e-6  # us -> s
			if orig > 1e9:
				return v * 1e-3  # ms -> s
		return v

	# Custom path first
	if time_key:
		orig = _get_nested(obj, time_key)
		if orig is not None:
			if isinstance(orig, (int, float)):
				val = float(orig)
				return _scale(val)
			if isinstance(orig, str):
				# try float then ISO
				try:
					return float(orig)
				except ValueError:
					try:
						from datetime import datetime
						return datetime.fromisoformat(orig).timestamp()
					except Exception:
						return None
	for k in ("t", "time", "timestamp", "ts"):
		if k in obj and obj[k] is not None:
			orig = obj[k]
			# Attempt conversion; if it fails for this key, try next alias
			if isinstance(orig, (int, float)):
				return _scale(float(orig))
			if isinstance(orig, str):
				try:
					return float(orig)
				except ValueError:
					# try next alias key
					continue
	# Additional typical time keys
	for k in ("time_s", "t_s", "ts_s", "timestamp_s", "ts_ms", "timestamp_ms", "ts_us", "ts_ns"):
		if k in obj and obj[k] is not None:
			orig = obj[k]
			if isinstance(orig, (int, float)):
				v = float(orig)
				# direct scale by suffix
				if k.endswith("_ms"):
					return v * 1e-3
				if k.endswith("_us"):
					return v * 1e-6
				if k.endswith("_ns"):
					return v * 1e-9
				return v
	# Fallback: nested payload (e.g., UTD {payload:{t,...}})
	try:
		payload = obj.get("payload")
		if isinstance(payload, dict):
			# direct time_key inside payload
			if time_key:
				orig = _get_nested(payload, time_key) if "." in str(time_key) else payload.get(time_key)
				if orig is not None:
					if isinstance(orig, (int, float)):
						return _scale(float(orig))
					if isinstance(orig, str):
						try:
							return float(orig)
						except ValueError:
							try:
								from datetime import datetime
								return datetime.fromisoformat(orig).timestamp()
							except Exception as _e:
								_ = _e
								return None
			# alias scan within payload
			for k in ("t", "time", "timestamp", "ts", "time_s", "t_s", "ts_s", "timestamp_s", "ts_ms", "timestamp_ms", "ts_us", "ts_ns"):
				if k in payload and payload[k] is not None:
					orig = payload[k]
					if isinstance(orig, (int, float)):
						v = float(orig)
						if k.endswith("_ms"):
							return v * 1e-3
						if k.endswith("_us"):
							return v * 1e-6
						if k.endswith("_ns"):
							return v * 1e-9
						return _scale(v)
					if isinstance(orig, str):
						try:
							return float(orig)
						except ValueError:
							try:
								from datetime import datetime
								return datetime.fromisoformat(orig).timestamp()
							except Exception as _e:
								# Try next alias in payload on parse failure
								_ = _e
								continue
	except Exception as _e:
		_ = _e
	return None


def _extract_parents(obj: dict) -> Sequence[str]:
	v = obj.get("parents") or obj.get("parent_ids") or obj.get("sources")
	if isinstance(v, (list, tuple)):
		out: List[str] = []
		for x in v:
			s: Optional[str] = None
			try:
				s = str(x)
			except Exception:
				s = None
			if s is not None:
				out.append(s)
		return out
	return []


def _ingest_events(
	files: Sequence[Path],
	*,
	include_streams: Optional[Set[str]] = None,
	max_events: Optional[int] = None,
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, str]], int, Dict[str, int]]:
	"""Return (events, edges, total_seen). Edges inferred from 'parents' if present."""
	events: List[Tuple[str, float]] = []
	edges: List[Tuple[str, str]] = []
	seen = 0
	skipped: Dict[str, int] = {"filtered_stream": 0, "missing_id": 0, "missing_time": 0}
	# Pull flexible keys from outer scope via default values (set by caller)
	_id_key = getattr(_ingest_events, "_id_key", None)
	_time_key = getattr(_ingest_events, "_time_key", None)
	_time_scale = getattr(_ingest_events, "_time_scale", "auto")
	_step_key = getattr(_ingest_events, "_step_key", None)
	_step_dt = getattr(_ingest_events, "_step_dt", None)
	_expand_heads: Optional[Set[str]] = getattr(_ingest_events, "_expand_heads", None)
	_trail_chain: bool = bool(getattr(_ingest_events, "_trail_chain", False))
	_trail_topk: Optional[int] = getattr(_ingest_events, "_trail_topk", None)
	_trail_minval: Optional[float] = getattr(_ingest_events, "_trail_minval", None)
	# State for head chaining: last event id per (kind, neuron)
	_last_head: Dict[Tuple[str, int], str] = {}

	def _progress(i_seen: int) -> None:
		if i_seen % 50000 == 0 and i_seen > 0:
			try:
				print(f"[causality] ingest progress: seen={i_seen} events={len(events)} edges={len(edges)}", flush=True)
			except Exception as _e:
				_ = _e
	for fp in files:
		for obj in _iter_jsonl(fp):
			seen += 1
			if _expand_heads:
				# Expand neuron head arrays into per-neuron events; prefer explicit tick/time
				# Tick index (int) for stable per-tick IDs
				_tick = None
				try:
					if "t" in obj and isinstance(obj["t"], (int, float)):
						_tick = int(obj["t"])
					elif "evt_t" in obj and isinstance(obj["evt_t"], (int, float)):
						_tick = int(obj["evt_t"])
				except Exception as _e:
					_ = _e
					_tick = None
				# Event time: prefer explicit time_key, else ts, else step*dt, else tick as seconds
				t = _normalize_time(obj, time_key=_time_key, time_scale=_time_scale)
				if t is None and _step_key and _step_dt:
					step_val = _get_nested(obj, _step_key)
					if isinstance(step_val, (int, float)):
						t = float(step_val) * float(_step_dt)
				if t is None and isinstance(_tick, int):
					t = float(_tick)
				if t is None:
					skipped["missing_time"] += 1
					_progress(seen)
					continue

				# For each requested head kind, create events and chain edges from previous tick
				created = 0
				per_kind_created: Dict[str, List[Tuple[str, float]]] = {}
				for kind in list(_expand_heads or set()):
					key = f"evt_{kind}_head"
					arr = obj.get(key)
					if not isinstance(arr, list):
						continue
					for pair in arr:
						try:
							nidx, val = int(pair[0]), pair[1]
						except Exception as _e:
							_ = _e
							# skip malformed pair
							continue
						# Build event id; include tick to ensure uniqueness
						eid = f"{kind}:{nidx}:{int(_tick) if isinstance(_tick, int) else 0}"
						events.append((eid, float(t)))
						created += 1
						# Track created for possible within-tick chaining (e.g., trail)
						try:
							per_kind_created.setdefault(kind, []).append((eid, float(val)))
						except Exception:
							per_kind_created.setdefault(kind, []).append((eid, float('nan')))
						# Chain edge from previous head event for the same node/kind
						prev = _last_head.get((kind, nidx))
						if prev is not None:
							edges.append((prev, eid))
						_last_head[(kind, nidx)] = eid
				# Within-tick chaining along trail ranking (emulate walker path)
				if _trail_chain and ("trail" in (per_kind_created.keys())):
					lst = per_kind_created.get("trail", [])
					# Filter by min value if provided
					if _trail_minval is not None:
						lst = [(e, v) for (e, v) in lst if (isinstance(v, (int, float)) and (not (v != v)) and v >= float(_trail_minval))]  # v!=v checks NaN
					# Sort by value descending (fallback: keep insertion order)
					try:
						lst.sort(key=lambda ev: (float('-inf') if not isinstance(ev[1], (int, float)) or (ev[1] != ev[1]) else float(ev[1])), reverse=True)
					except Exception:
						lst = lst  # keep as is
					# Apply top-k if provided
					if isinstance(_trail_topk, int) and _trail_topk > 0:
						lst = lst[: _trail_topk]
					# Add linear edges along the sorted list
					if len(lst) > 1:
						for i in range(len(lst) - 1):
							u = lst[i][0]
							v = lst[i + 1][0]
							if u != v:
								edges.append((u, v))
				# If nothing created for this row, count as missing_id
				if created == 0:
					skipped["missing_id"] += 1
				_progress(seen)
				# Respect max_events cap on created events rather than rows
				if max_events is not None and len(events) >= max_events:
					return events, edges, seen, skipped
				continue
			if include_streams is not None:
				stream = str(obj.get("stream") or obj.get("source") or "").lower()
				if stream and stream not in include_streams:
					skipped["filtered_stream"] += 1
					continue
			eid = _normalize_event_id(obj, id_key=_id_key)
			t = _normalize_time(obj, time_key=_time_key, time_scale=_time_scale)
			if t is None and _step_key and _step_dt:
				step_val = _get_nested(obj, _step_key)
				if isinstance(step_val, (int, float)):
					t = float(step_val) * float(_step_dt)
			if eid is None:
				skipped["missing_id"] += 1
				continue
			if t is None:
				skipped["missing_time"] += 1
				continue
			events.append((eid, t))
			# explicit edges if present
			for p in _extract_parents(obj):
				edges.append((p, eid))
			if max_events is not None and len(events) >= max_events:
				return events, edges, seen, skipped
			_progress(seen)
	return events, edges, seen, skipped


def _render_plot(samples, slope: float, intercept: float, *, diag: Optional[Dict[str, Any]] = None):
	"""Create a log–log scaling subplot figure for intervals.

	Returns (fig, warning). If matplotlib is unavailable, returns (None, warn).
	"""
	try:
		apply_style("light")
		fig, ax = get_fig_ax(size=(6.5, 4.0))
	except Exception as e:
		return None, f"matplotlib not available: {e}"

	xs: List[float] = []
	ys: List[float] = []
	for _p, _q, dt, size, _r in samples:
		if dt > 0 and size > 0:
			xs.append(float(dt))
			ys.append(float(size))

	if not xs or not ys:
		# No intervals: return an empty figure; caller may compose with DAG viz
		ax.axis('off')
		ax.text(0.5, 0.5, "No interval samples", ha='center', va='center')
		fig.tight_layout()
		return fig, "no interval samples"

	# Log-log scatter with fit line
	try:
		import numpy as np
		lxs = np.log(sanitize_for_log(xs))
		lys = np.log(sanitize_for_log(ys))
	except Exception:
		# Fallback without numpy (shouldn't happen given sanitize_for_log uses numpy)
		import math
		lxs = [math.log(max(x, 1e-30)) for x in xs]
		lys = [math.log(max(y, 1e-30)) for y in ys]

	ax.scatter(lxs, lys, s=12, alpha=0.5, label="samples")
	xmin, xmax = (min(lxs), max(lxs))
	xr = [xmin, xmax]
	yr = [intercept + slope * xmin, intercept + slope * xmax]
	ax.plot(xr, yr, color="crimson", lw=2, label=f"fit slope={slope:.3f}")
	ax.set_xlabel("log Δt")
	ax.set_ylabel("log |I|")
	ax.set_title("Causal interval scaling")
	ax.legend()
	fig.tight_layout()
	return fig, None


def _render_dag(times: Dict[str, float], adj: Dict[str, List[str]], *, max_nodes: int = 400, max_edges: int = 1200):
	"""Render a simple DAG visualization (transitive reduction) using a layered layout by time.

	Returns (fig, warn) where warn is None on success.
	"""
	try:
		import numpy as np
		import matplotlib.pyplot as plt
		apply_style("light")
	except Exception as e:
		return None, f"matplotlib not available: {e}"

	n = len(times)
	if n == 0:
		fig, ax = get_fig_ax(size=(6.5, 4.0))
		ax.axis('off')
		ax.text(0.5, 0.5, "No events recognized", ha='center', va='center')
		fig.tight_layout()
		return fig, "no events"

	# Select subset if too large
	nodes = list(times.keys())
	nodes.sort(key=lambda u: times[u])
	if n > max_nodes:
		step = max(1, n // max_nodes)
		sel = set(nodes[::step])
	else:
		sel = set(nodes)

	# Build filtered edges
	edges = []
	for u, nbrs in adj.items():
		if u not in sel:
			continue
		for v in nbrs:
			if v in sel:
				edges.append((u, v))
				if len(edges) >= max_edges:
					break
		if len(edges) >= max_edges:
			break

	# Layered layout: y by normalized time, x by index bucket to reduce overlap
	sel_nodes = [u for u in nodes if u in sel]
	ts = np.array([times[u] for u in sel_nodes], dtype=float)
	tmin, tmax = float(ts.min()), float(ts.max())
	td = (tmax - tmin) if (tmax > tmin) else 1.0
	ys = (ts - tmin) / td
	cols = 24 if len(sel_nodes) > 150 else 12 if len(sel_nodes) > 60 else 8
	xs = np.array([ (i % cols) / max(cols - 1, 1) for i, _ in enumerate(sel_nodes)], dtype=float)

	pos = {u: (xs[i], ys[i]) for i, u in enumerate(sel_nodes)}

	fig, ax = plt.subplots(figsize=(7.2, 5.2))
	ax.set_title("Causal DAG (transitive reduction)")
	# Draw edges
	for (u, v) in edges:
		if u in pos and v in pos:
			x0, y0 = pos[u]
			x1, y1 = pos[v]
			ax.plot([x0, x1], [y0, y1], color="#555", alpha=0.35, lw=0.8)
	# Draw nodes
	ax.scatter([pos[u][0] for u in sel_nodes], [pos[u][1] for u in sel_nodes], s=12, c="#1f77b4", alpha=0.85)
	ax.set_xlabel("layer index (bucketed)")
	ax.set_ylabel("normalized time")
	ax.set_xlim(-0.05, 1.05)
	ax.set_ylim(-0.05, 1.05)
	ax.grid(True, alpha=0.2)
	fig.tight_layout()
	return fig, None


# ----------------------------- Macro DAG (system metrics) -----------------------------
def _bh_fdr(pvals: List[Tuple[Tuple[str, str], float]], alpha: float = 0.01) -> List[Tuple[str, str]]:
	"""Benjamini–Hochberg FDR control over a list of ((u,v), pval).

	Returns edges with p <= p_star where p_star is the largest p meeting BH criterion.
	"""
	m = len(pvals)
	if m == 0:
		return []
	ps = sorted([(p, e) for (e, p) in pvals], key=lambda x: x[0])
	keep_k = 0
	for i, (p, _e) in enumerate(ps, start=1):
		if p <= (alpha * i) / m:
			keep_k = i
	return [ps[i - 1][1] for i in range(1, keep_k + 1)]


def _extract_macro_table(files: Sequence[Path], *, default_vars: Optional[List[str]] = None) -> Optional["pd.DataFrame"]:
	"""Build a per-tick DataFrame of macro/system metrics.

	- Uses top-level fields if present; computes counts from evt_*_head if not found.
	- Returns None if insufficient data.
	"""
	try:
		import pandas as pd  # type: ignore
		import numpy as np  # type: ignore
	except Exception:
		return None

	rows: List[dict] = []
	for fp in files:
		for obj in _iter_jsonl(fp):
			tick = None
			if isinstance(obj.get("t"), (int, float)):
				tick = int(obj.get("t"))
			elif isinstance(obj.get("evt_t"), (int, float)):
				tick = int(obj.get("evt_t"))
			if tick is None:
				continue
			row: Dict[str, Any] = {"tick": tick}
			# Candidate variables (present in logs; robust to missing)
			candidates = set(default_vars or [
				"vt_walkers", "vt_coverage", "td_signal", "sie_valence_01", "b1_spike", "speak_suppressed",
				"evt_exc_count", "evt_inh_count", "evt_heat_count", "evt_trail_count",
			])
			# Direct copy if present
			for k in list(candidates):
				v = obj.get(k)
				if isinstance(v, (int, float)):
					row[k] = float(v)
				elif isinstance(v, bool):
					row[k] = float(1 if v else 0)
			# Compute counts from *_head arrays if missing
			if "evt_exc_count" in candidates and "evt_exc_count" not in row:
				arr = obj.get("evt_exc_head")
				if isinstance(arr, list):
					row["evt_exc_count"] = float(len(arr))
			if "evt_inh_count" in candidates and "evt_inh_count" not in row:
				arr = obj.get("evt_inh_head")
				if isinstance(arr, list):
					row["evt_inh_count"] = float(len(arr))
			if "evt_heat_count" in candidates and "evt_heat_count" not in row:
				arr = obj.get("evt_heat_head")
				if isinstance(arr, list):
					row["evt_heat_count"] = float(len(arr))
			if "evt_trail_count" in candidates and "evt_trail_count" not in row:
				v = obj.get("evt_trail_count")
				if isinstance(v, (int, float)):
					row["evt_trail_count"] = float(v)
				else:
					arr = obj.get("evt_trail_head")
					if isinstance(arr, list):
						row["evt_trail_count"] = float(len(arr))
			# Only keep row if at least 3 metrics present (besides tick)
			if len(row) > 3:
				rows.append(row)
	if not rows:
		return None
	df = pd.DataFrame(rows).sort_values("tick").drop_duplicates(subset=["tick"])  # noqa: F841
	return df


def _macro_granger_edges(df: "pd.DataFrame", *, lags: int = 2, alpha: float = 0.01, fdr: bool = True) -> Tuple[List[Tuple[str, str]], Dict[Tuple[str, str], float]]:
	"""Fit a VAR(lags) and test pairwise Granger causality; return significant edges and p-values.

	Uses BH-FDR if fdr=True.
	"""
	import numpy as np  # type: ignore
	from statsmodels.tsa.api import VAR  # type: ignore

	cols = [c for c in df.columns if c != "tick"]
	if len(cols) < 3:
		return [], {}
	X = df[cols].astype(float).replace([np.inf, -np.inf], np.nan).fillna(0.0)
	if len(X) < (lags + 8):
		return [], {}
	try:
		model = VAR(X)
		res = model.fit(lags)
	except Exception:
		return [], {}
	pvals: List[Tuple[Tuple[str, str], float]] = []
	pmap: Dict[Tuple[str, str], float] = {}
	for j in cols:
		for i in cols:
			if i == j:
				continue
			try:
				test = res.test_causality(j, [i], kind='f')
				p = float(getattr(test, 'pvalue', 1.0))
			except Exception:
				p = 1.0
			pmap[(i, j)] = p
			pvals.append(((i, j), p))
	if fdr:
		edges = _bh_fdr(pvals, alpha=alpha)
	else:
		edges = [e for (e, p) in pvals if p <= alpha]
	return edges, pmap


def _render_macro_dag(vars: List[str], edges: List[Tuple[str, str]]):
	"""Render a simple directed graph of macro variables; allow cycles; layout in a circle.

	Returns (fig, warn)
	"""
	try:
		import numpy as np  # noqa: F401
		import matplotlib.pyplot as plt
		apply_style("light")
	except Exception as e:
		return None, f"matplotlib not available: {e}"

	n = len(vars)
	if n == 0:
		fig, ax = get_fig_ax(size=(6.5, 4.0))
		ax.axis('off')
		ax.text(0.5, 0.5, "No macro variables", ha='center', va='center')
		fig.tight_layout()
		return fig, "no macro vars"

	# Circle layout
	angles = [2.0 * 3.1415926535 * k / n for k in range(n)]
	pos = {v: (0.5 + 0.42 * __import__('math').cos(a), 0.5 + 0.42 * __import__('math').sin(a)) for v, a in zip(vars, angles)}
	fig, ax = plt.subplots(figsize=(7.4, 7.0))
	ax.set_title("Macro VAR Granger DAG (FDR-controlled)")
	# Draw nodes
	for v in vars:
		x, y = pos[v]
		ax.scatter([x], [y], s=160, c="#1f77b4", alpha=0.9)
		ax.text(x, y, v, ha='center', va='center', color='white', fontsize=9, weight='bold')
	# Draw edges with arrows
	for (u, v) in edges:
		if (u in pos) and (v in pos):
			x0, y0 = pos[u]
			x1, y1 = pos[v]
			ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color="#555", lw=1.4, alpha=0.85))
	ax.axis('off')
	fig.tight_layout()
	return fig, None


def run_audit(spec: AuditSpec, *, approved: bool, engineering_only: bool, proposal: Optional[str]) -> Tuple[str, str, dict]:
	# Discover files
	files: List[Path] = _discover_files(spec.events)
	if spec.utd_events is not None:
		files += _discover_files(spec.utd_events)
	if not files:
		raise FileNotFoundError("No input files found")

	# Ingest
	# Configure flexible keying for this call (attach to function for simplicity)
	_ingest_events._id_key = spec.id_key
	_ingest_events._time_key = spec.time_key
	_ingest_events._time_scale = spec.time_scale
	_ingest_events._step_key = spec.step_key
	_ingest_events._step_dt = spec.step_dt
	_ingest_events._expand_heads = set(spec.expand_heads or set()) or None
	_ingest_events._trail_chain = bool(spec.trail_chain)
	_ingest_events._trail_topk = (int(spec.trail_topk) if spec.trail_topk is not None else None)
	_ingest_events._trail_minval = (float(spec.trail_minval) if spec.trail_minval is not None else None)
	events, edges, total_seen, skipped = _ingest_events(files, include_streams=spec.streams, max_events=spec.max_events)

	# Build DAG
	times, adj = build_event_dag(
		events,
		edges=edges if edges else None,
		infer_by_time=bool(spec.infer_by_time),
		max_successors=(max(0, int(spec.max_successors))),
		time_tolerance=float(spec.time_tol),
	)
	# If no edges resulted and no parents were present, enable minimal time inference fallback
	if sum(len(vs) for vs in adj.values()) == 0 and not edges:
		times, adj = build_event_dag(
			events,
			edges=None,
			infer_by_time=True,
			max_successors=8 if spec.max_successors == 0 else spec.max_successors,
			time_tolerance=max(0.0, float(spec.time_tol)),
		)
	adj_red = transitive_reduction(adj, max_edges=200_000)
	dag_ok = is_acyclic(adj_red)

	# Sample intervals and fit scaling
	samples = sample_intervals(
		times,
		adj_red,
		k=int(spec.k),
		min_dt=float(spec.min_dt),
		max_dt=float(spec.max_dt) if spec.max_dt is not None else None,
		reach_budget=int(spec.reach_budget),
	)
	slope, intercept = fit_diamond_scaling(samples)
	rs: List[float] = [r for (_p, _q, _dt, _sz, r) in samples]
	ds: List[float] = [dim_from_order_fraction(r) for r in rs]
	import statistics as stats
	r_mean = float(stats.mean(rs)) if rs else 1.0
	r_median = float(stats.median(rs)) if rs else 1.0
	d_mean = float(stats.mean(ds)) if ds else 1.0
	d_median = float(stats.median(ds)) if ds else 1.0

	# Compute diagnostics and gates before artifact routing
	diag_info = {
		"nodes": len(times),
		"edges": sum(len(vs) for vs in adj_red.values()),
		"samples": len(samples),
		"seen": total_seen,
		"skipped_filtered_stream": skipped.get("filtered_stream", 0),
		"skipped_missing_id": skipped.get("missing_id", 0),
		"skipped_missing_time": skipped.get("missing_time", 0),
	}
	gate_reasons: List[str] = []
	if len(events) == 0:
		gate_reasons.append("no_events_recognized")
	if len(times) == 0:
		gate_reasons.append("no_nodes_in_dag")
	if diag_info["edges"] == 0:
		gate_reasons.append("no_edges_in_dag")
	# Note: samples can be 0 for sparse data; keep as a soft signal
	if len(samples) == 0:
		gate_reasons.append("no_intervals_sampled")
	gate_failed = any(r in {"no_events_recognized", "no_nodes_in_dag", "no_edges_in_dag"} for r in gate_reasons)
	# Route artifacts to failed_runs if gate fails (independent of approval quarantine)
	route_failed = (not approved) or gate_failed
	# Prefer a DAG graph; if intervals exist, add a separate scaling figure later if needed.
	dag_fig, dag_warn = _render_dag(times, adj_red)
	warn = dag_warn
	slug = build_slug(spec.name, spec.tag)
	fig_path: Optional[Path] = None
	if dag_fig is not None:
		try:
			fig_path = save_figure(DOMAIN, slug, dag_fig, failed=route_failed)
		except Exception as e:
			warn = f"figure save failed: {e}"

	# Optionally also save the scaling plot if samples exist
	if len(samples) > 0:
		scaling_fig, _w = _render_plot(samples, slope, intercept, diag=diag_info)
		try:
			_ = save_figure(DOMAIN, slug + "_scaling", scaling_fig, failed=route_failed)
		except Exception as e:
			warn = (warn or "") + f"; scaling figure save failed: {e}"

	# Optional Macro DAG path (system metrics Granger graph)
	macro_edges: List[Tuple[str, str]] = []
	macro_vars: List[str] = []
	macro_fig_path: Optional[Path] = None
	macro_pvals: Dict[Tuple[str, str], float] = {}
	if spec.macro_dag:
		try:
			macro_df = _extract_macro_table(files)
			if macro_df is not None:
				macro_vars = [c for c in macro_df.columns if c != "tick"]
				macro_edges, macro_pvals = _macro_granger_edges(macro_df, lags=int(spec.macro_lags), alpha=float(spec.macro_alpha), fdr=True)
				macro_fig, _mw = _render_macro_dag(macro_vars, macro_edges)
				if macro_fig is not None:
					macro_fig_path = save_figure(DOMAIN, slug + "_macro", macro_fig, failed=route_failed)
		except Exception as _e:
			_ = _e

	logp = log_path_by_tag(DOMAIN, spec.name, spec.tag, failed=route_failed, type="json")
	log = {
		"timestamp": __import__("datetime").datetime.now().isoformat(),
		"domain": DOMAIN,
		"script": SCRIPT_NAME,
		"proposal": proposal,
		"tag": spec.tag,
		"params": {
			"infer_by_time": bool(spec.infer_by_time),
			"max_successors": int(spec.max_successors),
			"time_tolerance": float(spec.time_tol),
			"k": int(spec.k),
			"min_dt": float(spec.min_dt),
			"max_dt": (float(spec.max_dt) if spec.max_dt is not None else None),
			"reach_budget": int(spec.reach_budget),
			"streams": sorted(list(spec.streams)) if spec.streams else None,
			"max_events": int(spec.max_events) if spec.max_events is not None else None,
			"expand_heads": (sorted(list(spec.expand_heads)) if spec.expand_heads else None),
			"trail_chain": bool(spec.trail_chain),
			"trail_topk": (int(spec.trail_topk) if spec.trail_topk is not None else None),
			"trail_minval": (float(spec.trail_minval) if spec.trail_minval is not None else None),
		},
		"ingest": {
			"input_files": [str(p) for p in files],
			"total_seen": int(total_seen),
			"events": int(len(events)),
			"edges": int(len(edges)),
			"skipped": skipped,
		},
		"dag": {
			"nodes": int(len(times)),
			"edges": int(sum(len(vs) for vs in adj_red.values())),
			"acyclic": bool(dag_ok),
		},
		"macro": {
			"enabled": bool(spec.macro_dag),
			"vars": macro_vars,
			"edges": [(u, v) for (u, v) in macro_edges],
			"pvals": {f"{i}->{j}": float(p) for ((i, j), p) in macro_pvals.items()},
		},
		"metrics": {
			"samples": int(len(samples)),
			"diamond_slope": float(slope),
			"diamond_intercept": float(intercept),
			"r_mean": float(r_mean),
			"r_median": float(r_median),
			"d_hat_mean": float(d_mean),
			"d_hat_median": float(d_median),
		},
		"gates": {
			"failed": bool(gate_failed),
			"reasons": gate_reasons,
		},
		"artifacts": {
			"figure": (str(fig_path) if fig_path is not None else None),
			"macro_figure": (str(macro_fig_path) if macro_fig_path is not None else None),
			"figure_warning": warn,
			"log": str(logp),
		},
		"policy": {
			"approved": os.getenv("VDM_POLICY_APPROVED") == "1",
			"engineering_only": os.getenv("VDM_POLICY_ENGINEERING") == "1",
			"proposal": os.getenv("VDM_POLICY_PROPOSAL"),
			"schema": os.getenv("VDM_POLICY_SCHEMA"),
			"approved_by": os.getenv("VDM_POLICY_APPROVED_BY"),
			"approved_at": os.getenv("VDM_POLICY_APPROVED_AT"),
		},
		"status": ("failed" if gate_failed else "success"),
	}
	write_log(logp, log)

	# Results DB logging (per-domain DB, table per script)
	try:
		handle = begin_run(
			domain=DOMAIN,
			experiment=str(Path(__file__).resolve()),
			tag=spec.tag,
			params={
				"infer_by_time": bool(spec.infer_by_time),
				"max_successors": int(spec.max_successors),
				"time_tolerance": float(spec.time_tol),
				"k": int(spec.k),
				"min_dt": float(spec.min_dt),
				"max_dt": (float(spec.max_dt) if spec.max_dt is not None else None),
				"reach_budget": int(spec.reach_budget),
				"streams": sorted(list(spec.streams)) if spec.streams else None,
				"max_events": int(spec.max_events) if spec.max_events is not None else None,
				"expand_heads": (sorted(list(spec.expand_heads)) if spec.expand_heads else None),
				"trail_chain": bool(spec.trail_chain),
				"trail_topk": (int(spec.trail_topk) if spec.trail_topk is not None else None),
				"trail_minval": (float(spec.trail_minval) if spec.trail_minval is not None else None),
			},
			engineering_only=bool(os.getenv("VDM_POLICY_ENGINEERING") == "1" or os.getenv("VDM_POLICY_APPROVED") != "1"),
		)
		add_artifacts(handle, {"figure": (str(fig_path) if fig_path is not None else None), "log": str(logp)})
		log_metrics(
			handle,
			{
				"samples": int(len(samples)),
				"diamond_slope": float(slope),
				"diamond_intercept": float(intercept),
				"r_mean": float(r_mean),
				"r_median": float(r_median),
				"d_hat_mean": float(d_mean),
				"d_hat_median": float(d_median),
				"dag_nodes": int(len(times)),
				"dag_edges": int(sum(len(vs) for vs in adj_red.values())),
				"acyclic": bool(dag_ok),
			},
		)
		if gate_failed:
			end_run_failed(handle, reason=";".join(gate_reasons) or "gate_failed")
		else:
			end_run_success(handle)
	except Exception as _e:
		_ = _e

	return str(fig_path), str(logp), log


def main(argv: Optional[Sequence[str]] = None) -> int:
	parser = argparse.ArgumentParser(description="Causal DAG audit over JSONL event logs")
	parser.add_argument("--events", type=str, required=True, help="Path to events.jsonl or directory of shards")
	parser.add_argument("--utd-events", type=str, default=None, help="Optional path to utd_events.jsonl or directory")
	parser.add_argument("--tag", type=str, default="v1", help="Approval tag to use (default: v1)")
	parser.add_argument("--allow-unapproved", action="store_true", help="Allow unapproved run; artifacts quarantined")
	parser.add_argument("--name", type=str, default="dag_audit", help="Base slug for artifacts (default: dag_audit)")
	parser.add_argument("--infer-by-time", action="store_true", help="Infer edges by time ordering when parents missing")
	parser.add_argument("--max-successors", type=int, default=0, help="Max successors per node when inferring (0=unbounded)")
	parser.add_argument("--time-tol", type=float, default=0.0, help="Time tolerance for zero-lag grouping (seconds)")
	parser.add_argument("--k", type=int, default=256, help="Number of intervals to sample")
	parser.add_argument("--min-dt", type=float, default=0.0, help="Minimum Δt for intervals")
	parser.add_argument("--max-dt", type=float, default=None, help="Maximum Δt for intervals")
	parser.add_argument("--reach-budget", type=int, default=8192, help="Reachability budget for bounded searches")
	parser.add_argument("--streams", type=str, default="", help="Comma list of streams to include (default: all)")
	parser.add_argument("--max-events", type=int, default=None, help="Cap on number of events to ingest (per run)")
	# Flexible keying
	parser.add_argument("--id-key", type=str, default=None, help="Dot-path for event id (e.g., 'neuron:i' not required; aliases auto-detected)")
	parser.add_argument("--time-key", type=str, default=None, help="Dot-path for event time (e.g., 'meta.ts_ns')")
	parser.add_argument(
		"--time-scale",
		type=str,
		default="auto",
		choices=["auto", "1", "1e-3", "1e-6", "1e-9"],
		help="Scale for time-key to seconds (auto|1|1e-3|1e-6|1e-9)",
	)
	parser.add_argument("--step-key", type=str, default=None, help="Integer step field to use when no time-key present")
	parser.add_argument("--step-dt", type=float, default=None, help="Seconds per step for --step-key time fallback")
	parser.add_argument(
		"--expand-heads",
		type=str,
		default="",
		help="Comma list among {heat,exc,inh} to expand evt_*_head arrays into per-neuron events and chain across ticks (default: off)",
	)
	parser.add_argument("--trail-chain", action="store_true", help="Within-tick: add edges along evt_trail_head ranking (after expansion)")
	parser.add_argument("--trail-topk", type=int, default=None, help="Limit number of trail-ranked nodes chained per tick (default: all)")
	parser.add_argument("--trail-minval", type=float, default=None, help="Minimum value to include in trail chaining (filters low-valued entries)")
	# Macro DAG options
	parser.add_argument("--macro-dag", action="store_true", help="Enable system-level macro DAG via VAR Granger (default on)")
	parser.add_argument("--no-macro-dag", action="store_true", help="Disable system-level macro DAG")
	parser.add_argument("--macro-lags", type=int, default=2, help="VAR lag order for macro DAG (default: 2)")
	parser.add_argument("--macro-alpha", type=float, default=0.01, help="Significance level for macro DAG FDR (default: 0.01)")
	args = parser.parse_args(argv)

	# Make the run script name visible to approval policy (domain:script:tag)
	# Use the actual script filename (with extension) to match script-scoped approvals
	os.environ.setdefault("VDM_RUN_SCRIPT", Path(__file__).name)

	code_root = Path(__file__).resolve().parents[2]  # Derivation/code
	approved, engineering_only, proposal = check_tag_approval(
		DOMAIN, args.tag, args.allow_unapproved, code_root
	)

	# If streams is empty or 'all', include all streams (no filtering)
	include_streams: Optional[Set[str]]
	if not args.streams or args.streams.strip().lower() in {"all", "*"}:
		include_streams = None
	else:
		include_streams = {s.strip().lower() for s in args.streams.split(",") if s.strip()}
	spec = AuditSpec(
		events=Path(args.events),
		utd_events=(Path(args.utd_events) if args.utd_events else None),
		tag=args.tag,
		name=args.name,
		infer_by_time=bool(args.infer_by_time),
		max_successors=int(args.max_successors),
		time_tol=float(args.time_tol),
		k=int(args.k),
		min_dt=float(args.min_dt),
		max_dt=(float(args.max_dt) if args.max_dt is not None else None),
		reach_budget=int(args.reach_budget),
		streams=include_streams,
		max_events=(int(args.max_events) if args.max_events is not None else None),
		id_key=(str(args.id_key) if args.id_key else None),
		time_key=(str(args.time_key) if args.time_key else None),
		time_scale=str(args.time_scale),
		step_key=(str(args.step_key) if args.step_key else None),
		step_dt=(float(args.step_dt) if args.step_dt is not None else None),
		expand_heads=({s.strip() for s in str(args.expand_heads).split(',') if s.strip()} if args.expand_heads else None),
		trail_chain=bool(args.trail_chain),
		trail_topk=(int(args.trail_topk) if args.trail_topk is not None else None),
		trail_minval=(float(args.trail_minval) if args.trail_minval is not None else None),
		macro_dag=(False if args.no_macro_dag else True),
		macro_lags=int(args.macro_lags),
		macro_alpha=float(args.macro_alpha),
	)

	figp, logp, log = run_audit(spec, approved=approved, engineering_only=engineering_only, proposal=proposal)
	print(json.dumps({"figure": figp, "log": logp, "approved": bool(approved), "samples": log["metrics"]["samples"], "slope": log["metrics"]["diamond_slope"], "d_hat_median": log["metrics"]["d_hat_median"]}, indent=2))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

