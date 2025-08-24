#!/usr/bin/env python3
from __future__ import annotations

"""
Golden-run parity harness.

Purpose:
- Compare two completed runs for behavioral parity without re-running the model.
- Validate that macro emissions and selected 'why' metrics are identical (or within tolerance).
- Provide basic distribution checks (P50/P99 deltas and two-sample KS statistic) on tick metrics.

What it checks:
1) Macro parity (default: first 200 'say' macros)
   - Text equality per position
   - Optional 'why' keys equality per position (strict or tolerant numeric compare)

2) Tick metrics parity from runs/<ts>/events.jsonl
   - P50/P99 delta within tolerance for selected metrics
   - KS statistic below tolerance (non-parametric)

Exit codes:
- 0 on parity pass
- 1 on any check failure

Notes:
- This script does not launch runs. Use it to compare existing run directories (e.g., A: IDF k=0.0 vs B: k=0.2).
- Does not require SciPy; uses simple robust implementations.

Usage examples:
  python tools/golden_run_parity.py --run-a runs/2025-08-10_21-00-00 --run-b runs/2025-08-10_22-15-00
  python tools/golden_run_parity.py --run-a A --run-b B --macros 200 --why-keys vt_entropy vt_coverage b1_z sie_valence_01 sie_v2_valence_01

"""

import argparse
import json
import math
import os
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _read_ndjson(path: str) -> Iterable[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
    except Exception:
        return []


def _find_file(run_dir: str, filename: str) -> Optional[str]:
    p = os.path.join(run_dir, filename)
    return p if os.path.exists(p) else None


def _safe_num(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        if isinstance(x, (int, float)):
            return float(x)
        # Try cast strings
        return float(str(x))
    except Exception:
        return None


def _p50(values: List[float]) -> Optional[float]:
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    mid = n // 2
    if n % 2 == 1:
        return vs[mid]
    else:
        return (vs[mid - 1] + vs[mid]) / 2.0


def _p99(values: List[float]) -> Optional[float]:
    if not values:
        return None
    vs = sorted(values)
    idx = int(math.ceil(0.99 * (len(vs) - 1)))
    return vs[max(0, min(idx, len(vs) - 1))]


def _ks_statistic(a: List[float], b: List[float]) -> Optional[float]:
    """
    Two-sample KS statistic (D) without SciPy.
    """
    if not a or not b:
        return None
    sa = sorted(a)
    sb = sorted(b)
    ia = ib = 0
    na = len(sa)
    nb = len(sb)
    d = 0.0
    while ia < na and ib < nb:
        if sa[ia] <= sb[ib]:
            x = sa[ia]
            ia += 1
        else:
            x = sb[ib]
            ib += 1
        while ia < na and sa[ia] == x:
            ia += 1
        while ib < nb and sb[ib] == x:
            ib += 1
        fa = ia / na
        fb = ib / nb
        d = max(d, abs(fa - fb))
    return d


def _load_utd_macros(run_dir: str, macro_name: str = "say") -> List[Dict[str, Any]]:
    """
    Load macro records from utd_events.jsonl with given macro name.
    Returns list of {"text": str, "why": dict, "score": float|None}
    """
    p = _find_file(run_dir, "utd_events.jsonl")
    out: List[Dict[str, Any]] = []
    if not p:
        return out
    for rec in _read_ndjson(p):
        try:
            if rec.get("type") != "macro":
                continue
            if rec.get("macro") != macro_name:
                continue
            args = rec.get("args", {}) or {}
            out.append(
                {
                    "text": str(args.get("text", "")),
                    "why": dict(args.get("why") or {}),
                    "score": _safe_num(rec.get("score")),
                }
            )
        except Exception:
            continue
    return out


def _extract_tick_metrics(run_dir: str, metric_keys: List[str]) -> Dict[str, List[float]]:
    """
    Extract tick metrics from events.jsonl, robust to structure differences.
    Structured logger likely writes records with message/event 'tick' and metrics inside 'extra.extra'.
    """
    p = _find_file(run_dir, "events.jsonl")
    out: Dict[str, List[float]] = {k: [] for k in metric_keys}
    if not p:
        return out

    def _get_metrics(rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Try nested forms: 'extra' or 'data' with nested 'extra'
        extra = rec.get("extra") or rec.get("data")
        if isinstance(extra, dict):
            e2 = extra.get("extra", extra)
            if isinstance(e2, dict):
                return e2
        return None

    for rec in _read_ndjson(p):
        try:
            # Recognize 'tick' records
            msg = rec.get("message") or rec.get("event") or rec.get("name") or rec.get("type")
            if str(msg).lower() != "tick":
                continue
            m = _get_metrics(rec)
            if not isinstance(m, dict):
                continue
            for k in metric_keys:
                v = _safe_num(m.get(k))
                if v is not None:
                    out[k].append(v)
        except Exception:
            continue
    return out


def _rel_diff(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None or b is None:
        return None
    denom = max(1e-9, abs(a) + abs(b)) / 2.0
    return abs(a - b) / denom


def compare_macros(
    A: List[Dict[str, Any]],
    B: List[Dict[str, Any]],
    limit: int,
    why_keys: List[str],
    tol: float = 0.0,
) -> Tuple[bool, List[str]]:
    """
    Compare first N macros by text and selected 'why' keys.
    tol: numeric tolerance for comparing 'why' values (exact text equality always required).
    """
    n = min(limit, len(A), len(B))
    errs: List[str] = []
    ok = True
    for i in range(n):
        a = A[i]
        b = B[i]
        if a.get("text", "") != b.get("text", ""):
            errs.append(f"[macro#{i}] text mismatch: A='{a.get('text','')}' vs B='{b.get('text','')}'")
            ok = False
        aw = a.get("why", {}) or {}
        bw = b.get("why", {}) or {}
        for k in why_keys:
            av = aw.get(k)
            bv = bw.get(k)
            anv = _safe_num(av)
            bnv = _safe_num(bv)
            if anv is not None and bnv is not None:
                if abs(anv - bnv) > tol:
                    errs.append(f"[macro#{i}] why[{k}] mismatch: A={anv} vs B={bnv} (tol={tol})")
                    ok = False
            else:
                if av != bv:
                    errs.append(f"[macro#{i}] why[{k}] mismatch (non-numeric): A={av} vs B={bv}")
                    ok = False
    return ok, errs


def compare_tick_distributions(
    A: Dict[str, List[float]],
    B: Dict[str, List[float]],
    p_tol: float,
    ks_tol: float,
) -> Tuple[bool, List[str]]:
    """
    Compare P50/P99 and KS statistic for selected tick metrics.
    """
    errs: List[str] = []
    ok = True
    for k in sorted(set(list(A.keys()) + list(B.keys()))):
        va = A.get(k, [])
        vb = B.get(k, [])
        if not va or not vb:
            # If either missing, we skip strict check but report
            errs.append(f"[tick] metric '{k}' missing or empty in {'A' if not va else 'B'} (len A={len(va)}, B={len(vb)})")
            ok = False
            continue
        p50a, p50b = _p50(va), _p50(vb)
        p99a, p99b = _p99(va), _p99(vb)
        rd50 = _rel_diff(p50a, p50b)
        rd99 = _rel_diff(p99a, p99b)
        if rd50 is not None and rd50 > p_tol:
            errs.append(f"[tick:{k}] P50 rel-diff {rd50:.4f} exceeds tol {p_tol:.4f} (A={p50a}, B={p50b})")
            ok = False
        if rd99 is not None and rd99 > p_tol:
            errs.append(f"[tick:{k}] P99 rel-diff {rd99:.4f} exceeds tol {p_tol:.4f} (A={p99a}, B={p99b})")
            ok = False
        ks = _ks_statistic(va, vb)
        if ks is not None and ks > ks_tol:
            errs.append(f"[tick:{k}] KS={ks:.4f} exceeds tol {ks_tol:.4f}")
            ok = False
    return ok, errs


def main():
    ap = argparse.ArgumentParser(description="Golden-run parity harness (compare two runs).")
    ap.add_argument("--run-a", required=True, help="Path to run A (directory containing utd_events.jsonl/events.jsonl)")
    ap.add_argument("--run-b", required=True, help="Path to run B (directory containing utd_events.jsonl/events.jsonl)")
    ap.add_argument("--macro", default="say", help="Macro name to compare (default: say)")
    ap.add_argument("--macros", type=int, default=200, help="Compare first N macros (default: 200)")
    ap.add_argument(
        "--why-keys",
        nargs="*",
        default=["vt_entropy", "vt_coverage", "b1_z", "connectome_entropy", "sie_valence_01", "sie_v2_valence_01", "cohesion_components"],
        help="Why keys to compare per macro (exact or numeric within tol)",
    )
    ap.add_argument("--why-tol", type=float, default=0.0, help="Tolerance for numeric 'why' comparisons (default: 0.0 exact)")
    ap.add_argument(
        "--tick-keys",
        nargs="*",
        default=["vt_entropy", "vt_coverage", "b1_z", "cohesion_components", "active_edges"],
        help="Tick metrics to compare from events.jsonl",
    )
    ap.add_argument("--p-tol", type=float, default=0.02, help="Relative tolerance for P50/P99 (default: 0.02 = 2%)")
    ap.add_argument("--ks-tol", type=float, default=0.15, help="KS tolerance (default: 0.15)")
    args = ap.parse_args()

    # 1) Macro parity
    mac_a = _load_utd_macros(args.run_a, macro_name=args.macro)
    mac_b = _load_utd_macros(args.run_b, macro_name=args.macro)
    ok_mac, errs_mac = compare_macros(mac_a, mac_b, args.macros, why_keys=args.why_keys, tol=args.why_tol)

    # 2) Tick distributions
    ticks_a = _extract_tick_metrics(args.run_a, metric_keys=args.tick_keys)
    ticks_b = _extract_tick_metrics(args.run_b, metric_keys=args.tick_keys)
    ok_tick, errs_tick = compare_tick_distributions(ticks_a, ticks_b, p_tol=args.p_tol, ks_tol=args.ks_tol)

    # Report
    print("=== Golden Run Parity Report ===")
    print(f"Run A: {args.run_a}")
    print(f"Run B: {args.run_b}")
    print(f"Macros compared: {args.macro} (first {args.macros})")
    print(f"Why keys: {', '.join(args.why_keys)} (tol={args.why_tol})")
    print(f"Tick keys: {', '.join(args.tick_keys)}  P tol={args.p_tol}  KS tol={args.ks_tol}")
    print("--------------------------------")

    if ok_mac:
        print("[OK] Macro parity")
    else:
        print("[FAIL] Macro parity mismatches:")
        for e in errs_mac[:20]:
            print("  -", e)
        if len(errs_mac) > 20:
            print(f"  ... and {len(errs_mac)-20} more")

    if ok_tick:
        print("[OK] Tick distributions parity")
    else:
        print("[FAIL] Tick distributions differences:")
        for e in errs_tick[:20]:
            print("  -", e)
        if len(errs_tick) > 20:
            print(f"  ... and {len(errs_tick)-20} more")

    ok = ok_mac and ok_tick
    print("--------------------------------")
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()