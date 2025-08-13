from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Optional

from fum_rt.frontend.utilities.profiles import safe_int as _safe_int, safe_float as _safe_float
from fum_rt.frontend.utilities.fs_utils import read_json_file, write_json_file, latest_checkpoint


def build_phase_update(
    default_profile: Dict[str, Any],
    phase,
    s_z,
    s_h,
    s_cd,
    s_vt,
    c_w,
    c_h,
    c_b,
    c_pf,
    c_thr,
    c_lw,
    c_cand,
    s_idf,
) -> Dict[str, Any]:
    """
    Build a dict of runtime/phase settings, coercing types with defaults.
    This normalizes UI inputs into a consistent structure.
    """
    return {
        "phase": int(_safe_int(phase, 0)),
        "speak": {
            "speak_z": float(_safe_float(s_z, default_profile["speak_z"])),
            "speak_hysteresis": float(_safe_float(s_h, default_profile["speak_hysteresis"])),
            "speak_cooldown_ticks": int(_safe_int(s_cd, default_profile["speak_cooldown_ticks"])),
            "speak_valence_thresh": float(_safe_float(s_vt, default_profile["speak_valence_thresh"])),
        },
        "connectome": {
            "walkers": int(_safe_int(c_w, default_profile["walkers"])),
            "hops": int(_safe_int(c_h, default_profile["hops"])),
            "bundle_size": int(_safe_int(c_b, default_profile["bundle_size"])),
            "prune_factor": float(_safe_float(c_pf, default_profile["prune_factor"])),
            "threshold": float(_safe_float(c_thr, default_profile.get("threshold", 0.15))),
            "lambda_omega": float(_safe_float(c_lw, default_profile.get("lambda_omega", 0.10))),
            "candidates": int(_safe_int(c_cand, default_profile.get("candidates", 64))),
        },
        "sie": {"novelty_idf_gain": float(_safe_float(s_idf, 1.0))},
    }


def _merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Shallow-merge with one level of deep-merge for nested dicts 'speak' and 'connectome'.
    Preserves keys like 'load_engram' in existing phase.json while applying updates.
    """
    out = dict(a or {})
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            nv = dict(out[k])
            nv.update(v)
            out[k] = nv
        else:
            out[k] = v
    return out


def update_phase_json(run_dir: str, update: Dict[str, Any]) -> bool:
    """
    Merge-update run_dir/phase.json with the provided update dict.
    Ensures directory exists; returns True on successful write.
    """
    try:
        os.makedirs(run_dir, exist_ok=True)
        p = os.path.join(run_dir, "phase.json")
        current = read_json_file(p) or {}
        if not isinstance(current, dict):
            current = {}
        merged = _merge(current, update)
        return write_json_file(p, merged)
    except Exception:
        return False


def queue_load_engram(run_dir: str, path: str) -> tuple[bool, str]:
    """
    Add/overwrite 'load_engram' in phase.json, preserving other keys.
    Normalizes directories to the latest checkpoint file to prevent loader errors.
    Returns (ok, normalized_path) so the UI can echo the actual target.
    """
    try:
        os.makedirs(run_dir, exist_ok=True)
        p = os.path.join(run_dir, "phase.json")
        obj = read_json_file(p) or {}
        if not isinstance(obj, dict):
            obj = {}
        # Normalize provided path:
        target = (path or "").strip()
        if not target:
            return False, ""
        # If a directory was provided, resolve to latest checkpoint inside it
        if os.path.isdir(target):
            lp = latest_checkpoint(target)
            if not lp:
                return False, ""
            target = lp
        else:
            # If file doesn't exist, try resolving relative to run_dir
            if not os.path.exists(target):
                cand = os.path.join(run_dir, target)
                if os.path.isdir(cand):
                    lp = latest_checkpoint(cand)
                    if not lp:
                        return False, ""
                    target = lp
                elif os.path.exists(cand):
                    target = cand
                else:
                    return False, ""
        obj["load_engram"] = target
        ok = write_json_file(p, obj)
        return (True, target) if ok else (False, "")
    except Exception:
        return False, ""


def parse_engram_events_for_message(records: Iterable[Dict[str, Any]]) -> Optional[str]:
    """
    Scan a set of event dicts and derive a user-facing message summarizing an engram load result.
    Returns the last relevant message if multiple are present.
    """
    msg: Optional[str] = None
    for rec in (records or []):
        if not isinstance(rec, dict):
            continue
        name = str(
            rec.get("event_type")
            or rec.get("event")
            or rec.get("message")
            or rec.get("msg")
            or rec.get("name")
            or ""
        ).lower()
        extra = rec.get("extra") or rec.get("meta") or {}
        if name == "engram_loaded":
            engram_path = extra.get("path") or extra.get("engram") or rec.get("path")
            msg = f"Engram loaded: {engram_path}" if engram_path else "Engram loaded."
        elif name == "engram_load_error":
            err = extra.get("err") or extra.get("error") or rec.get("error")
            engram_path = extra.get("path") or extra.get("engram") or rec.get("path")
            if err and engram_path:
                msg = f"Engram load error: {err} ({engram_path})"
            elif err:
                msg = f"Engram load error: {err}"
            else:
                msg = "Engram load error."
    return msg