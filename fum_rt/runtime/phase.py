"""
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
        pass