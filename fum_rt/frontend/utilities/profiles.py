"""
Profile utilities for FUM Live Dashboard.
Centralizes default profile defaults and assembly helpers to avoid duplication.
"""

from typing import Any, Dict, List


def safe_int(x, default=None):
    try:
        return int(x)
    except Exception:
        return default


def safe_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default


def bool_from_checklist(val) -> bool:
    """
    Dash checklist returns a list of selected values.
    We treat presence of 'on' as True for single-toggle checklists.
    """
    if isinstance(val, list):
        return "on" in val
    return bool(val)


def checklist_from_bool(b: bool) -> List[str]:
    """Inverse of bool_from_checklist for initial Dash values."""
    return ["on"] if bool(b) else []


def get_default_profile() -> Dict[str, Any]:
    """
    Default profile used by the dashboard UI for initial values.
    Mirrors the legacy dashboard defaults exactly.
    """
    return {
        "neurons": 1000,
        "k": 12,
        "hz": 10,
        "domain": "math_physics",
        "use_time_dynamics": True,
        "sparse_mode": False,
        "threshold": 0.15,
        "lambda_omega": 0.10,
        "candidates": 64,
        "walkers": 256,
        "hops": 3,
        "bundle_size": 3,
        "prune_factor": 0.10,
        "status_interval": 1,
        "viz_every": 0,
        "log_every": 1,
        "speak_auto": True,
        "speak_z": 3.0,
        "speak_hysteresis": 0.5,
        "speak_cooldown_ticks": 10,
        "speak_valence_thresh": 0.55,
        "b1_half_life_ticks": 50,
        "stim_group_size": 8,
        "stim_amp": 0.08,
        "stim_decay": 0.92,
        "stim_max_symbols": 128,
        "checkpoint_every": 60,
        "checkpoint_keep": 5,
        "duration": None,
    }


def assemble_profile(
    neurons,
    k,
    hz,
    domain,
    use_td,
    sparse_mode,
    threshold,
    lambda_omega,
    candidates,
    walkers,
    hops,
    status_interval,
    bundle_size,
    prune_factor,
    stim_group_size,
    stim_amp,
    stim_decay,
    stim_max_symbols,
    speak_auto,
    speak_z,
    speak_hyst,
    speak_cd,
    speak_val,
    b1_hl,
    viz_every,
    log_every,
    checkpoint_every,
    checkpoint_keep,
    duration,
    default_profile: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build a normalized runtime profile dict from UI inputs with robust typing.
    All conversions mirror the legacy dashboard behavior to avoid surprises.
    """
    return {
        "neurons": int(safe_int(neurons, default_profile["neurons"])),
        "k": int(safe_int(k, default_profile["k"])),
        "hz": int(safe_int(hz, default_profile["hz"])),
        "domain": str(domain or default_profile["domain"]),
        "use_time_dynamics": bool_from_checklist(use_td) if use_td is not None else default_profile["use_time_dynamics"],
        "sparse_mode": bool_from_checklist(sparse_mode) if sparse_mode is not None else default_profile["sparse_mode"],
        "threshold": float(safe_float(threshold, default_profile["threshold"])),
        "lambda_omega": float(safe_float(lambda_omega, default_profile["lambda_omega"])),
        "candidates": int(safe_int(candidates, default_profile["candidates"])),
        "walkers": int(safe_int(walkers, default_profile["walkers"])),
        "hops": int(safe_int(hops, default_profile["hops"])),
        "status_interval": int(safe_int(status_interval, default_profile["status_interval"])),
        "bundle_size": int(safe_int(bundle_size, default_profile["bundle_size"])),
        "prune_factor": float(safe_float(prune_factor, default_profile["prune_factor"])),
        "stim_group_size": int(safe_int(stim_group_size, default_profile["stim_group_size"])),
        "stim_amp": float(safe_float(stim_amp, default_profile["stim_amp"])),
        "stim_decay": float(safe_float(stim_decay, default_profile["stim_decay"])),
        "stim_max_symbols": int(safe_int(stim_max_symbols, default_profile["stim_max_symbols"])),
        "speak_auto": bool_from_checklist(speak_auto) if speak_auto is not None else default_profile["speak_auto"],
        "speak_z": float(safe_float(speak_z, default_profile["speak_z"])),
        "speak_hysteresis": float(safe_float(speak_hyst, default_profile["speak_hysteresis"])),
        "speak_cooldown_ticks": int(safe_int(speak_cd, default_profile["speak_cooldown_ticks"])),
        "speak_valence_thresh": float(safe_float(speak_val, default_profile["speak_valence_thresh"])),
        "b1_half_life_ticks": int(safe_int(b1_hl, default_profile["b1_half_life_ticks"])),
        "viz_every": int(safe_int(viz_every, default_profile["viz_every"])),
        "log_every": int(safe_int(log_every, default_profile["log_every"])),
        "checkpoint_every": int(safe_int(checkpoint_every, default_profile["checkpoint_every"])),
        "checkpoint_keep": int(safe_int(checkpoint_keep, default_profile["checkpoint_keep"])),
        "duration": None if duration in (None, "", "None") else int(safe_int(duration, 0)),
    }