"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime helper functions extracted from Nexus to reduce file size and improve separation
of concerns. All helpers are behavior-preserving and mirror the original inline logic.

This module may import fum_rt.io.* and fum_rt.core.* (runtime-layer policy). No CLI or
long-running orchestrator loop logic lives here—only small, focused helpers.
"""

from typing import Any, Dict, Iterable, Optional, Set, Tuple
import os
import re

# Core/IO imports allowed at runtime layer
from fum_rt.core.memory import save_checkpoint, load_engram as _load_engram_state
from fum_rt.core import text_utils
from fum_rt.runtime.retention import prune_checkpoints as _prune_ckpt
from fum_rt.runtime.telemetry import status_payload as _telemetry_status, macro_why_base as _telemetry_why_base
from fum_rt.io.cognition.stimulus import symbols_to_indices as _stim_symbols_to_indices
from fum_rt.io.cognition.composer import compose_say_text as _compose_say_text_impl
from fum_rt.io.cognition.speaker import should_speak as _speak_gate, novelty_and_score as _novelty_and_score


# --- Macro board helpers --------------------------------------------------------

def register_macro_board(utd: Any, run_dir: str) -> None:
    """
    Register default macros and optional per-run macro_board.json entries on a UTD-like emitter.
    Mirrors Nexus inline behavior:
      - Always register 'status' and 'say'
      - Optionally load runs/<ts>/macro_board.json (dict of name -> meta)
      - Only per-run board can provide metadata/templates to preserve emergent language
    """
    try:
        utd.register_macro('status', {'desc': 'Emit structured status payload'})
    except Exception:
        pass
    try:
        utd.register_macro('say', {'desc': 'Emit plain text line'})
    except Exception:
        pass

    try:
        pth = os.path.join(run_dir, 'macro_board.json')
        if os.path.exists(pth):
            import json
            with open(pth, 'r', encoding='utf-8') as fh:
                reg = json.load(fh)
            if isinstance(reg, dict):
                for name, meta in reg.items():
                    try:
                        utd.register_macro(str(name), meta if isinstance(meta, dict) else {})
                    except Exception:
                        pass
    except Exception:
        pass

    # Fallback: from_physicist_agent/macro_board_min.json (do not override per-run entries)
    try:
        # Discover repository root by walking up from this file: .../fum_rt/runtime -> repo root
        _here = os.path.abspath(__file__)
        _fum_rt_dir = os.path.dirname(os.path.dirname(_here))
        _repo_root = os.path.dirname(_fum_rt_dir)
        fb = os.path.join(_repo_root, 'from_physicist_agent', 'macro_board_min.json')
        if os.path.exists(fb):
            import json
            with open(fb, 'r', encoding='utf-8') as fh:
                reg2 = json.load(fh)
            current = set()
            try:
                current = set(utd.list_macros() or [])
            except Exception:
                current = set()
            if isinstance(reg2, dict):
                for name, meta in reg2.items():
                    try:
                        if str(name) not in current:
                            utd.register_macro(str(name), meta if isinstance(meta, dict) else {})
                    except Exception:
                        pass
    except Exception:
        pass


# --- Engram load and start-step derivation -------------------------------------

def maybe_load_engram(nx: Any, load_engram_path: Optional[str]) -> None:
    """
    If a path is provided, load the engram into nx.connectome (and nx.adc when present),
    logging the result into nx.logger for UI confirmation. Mirrors Nexus inline behavior.
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
    new snapshots. Mirrors Nexus inline logic including filename parsing and fallback scan.
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


# --- Ingest helpers -------------------------------------------------------------

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
            if m.get('type') != 'text':
                # Non-text messages are emitted to UTD as-is
                try:
                    nx.utd.emit_text(m)
                except Exception:
                    pass
                continue

            ute_text_count += 1
            # Append to rolling recent_text
            try:
                text = str(m.get('msg', ''))
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
                    idxs = _stim_symbols_to_indices(text, group_size, max_symbols, int(getattr(nx, "N", 0)), reverse_map=tick_rev_map)
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


# --- Diagnostics (optional smoke tests) -----------------------------------------

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


# --- Speaking (auto) ------------------------------------------------------------

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


# --- Status emission ------------------------------------------------------------

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
                score=val
            )
    except Exception:
        pass


# --- Visualization --------------------------------------------------------------

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


# --- Checkpointing --------------------------------------------------------------

def save_tick_checkpoint(nx: Any, step: int) -> None:
    """
    Save checkpoint and run retention policy when configured. Mirrors original behavior.
    """
    try:
        if getattr(nx, "checkpoint_every", 0) and (int(step) % int(nx.checkpoint_every)) == 0 and int(step) > 0:
            try:
                path = save_checkpoint(nx.run_dir, int(step), nx.connectome, fmt=getattr(nx, "checkpoint_format", "h5") or "h5", adc=getattr(nx, "adc", None))
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


__all__ = [
    "register_macro_board",
    "maybe_load_engram",
    "derive_start_step",
    "process_messages",
    "maybe_smoke_tests",
    "maybe_auto_speak",
    "emit_status_and_macro",
    "maybe_visualize",
    "save_tick_checkpoint",
]