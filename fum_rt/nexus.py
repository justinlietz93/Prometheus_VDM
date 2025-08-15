"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import time, os, argparse, json, re, random, sys
from collections import deque
from .utils.logging_setup import get_logger
from .io.ute import UTE
from .io.utd import UTD
from .io.actuators.macros import MacroEmitter
from .io.actuators.thoughts import ThoughtEmitter
from .core import text_utils
from .core.connectome import Connectome
from .core.sparse_connectome import SparseConnectome
from .core.metrics import compute_metrics, StreamingZEMA
from .core.visualizer import Visualizer
from .core.memory import save_checkpoint, load_engram as _load_engram_state
from .core.void_dynamics_adapter import get_domain_modulation
from .core.fum_sie import SelfImprovementEngine
from .core.bus import AnnounceBus
from .core.adc import ADC
from .core.void_b1 import update_void_b1 as _update_void_b1
# Modularized lexicon/phrase store (behavior-preserving)
from .io.lexicon.store import (
    load_phrase_templates as _lxn_load_phrases,
    load_lexicon as _lxn_load,
    save_lexicon as _lxn_save,
)
from .runtime.telemetry import macro_why_base as _telemetry_why_base, status_payload as _telemetry_status
# Event-driven metrics seam (feature-flagged; pure core + adapter)
from .core.proprioception.events import EventDrivenMetrics as _EvtMetrics
from .runtime.events_adapter import observations_to_events as _obs_to_events, adc_metrics_to_event as _adc_event
from .runtime.retention import prune_checkpoints as _prune_ckpt
# Cognition seams (Phase 3 move-only; behavior-preserving)
from .io.cognition.stimulus import symbols_to_indices as _stim_symbols_to_indices
from .io.cognition.composer import compose_say_text as _compose_say_text_impl
from .io.cognition.speaker import should_speak as _speak_gate, novelty_and_score as _novelty_and_score
try:
    from .core.control_server import ControlServer  # optional UI
except Exception:
    ControlServer = None
class Nexus:
    def __init__(self, run_dir: str, N:int=1000, k:int=12, hz:int=10,
                 domain:str='biology_consciousness', use_time_dynamics:bool=True,
                 viz_every:int=10, log_every:int=1, checkpoint_every:int=0, seed:int=0,
                 sparse_mode:bool=False, threshold:float=0.15, lambda_omega:float=0.1,
                 candidates:int=64, walkers:int=256, hops:int=3, status_interval:int=1,
                 bundle_size:int=3, prune_factor:float=0.10,
                 speak_auto:bool=True, speak_z:float=1.0, speak_hysteresis:float=1.0,
                 speak_cooldown_ticks:int=10, speak_valence_thresh:float=0.01,
                 b1_half_life_ticks:int=50,
                 bus_capacity:int=65536, bus_drain:int=2048,
                 r_attach:float=0.25, ttl_init:int=120, split_patience:int=6,
                 stim_group_size:int=4, stim_amp:float=0.05, stim_decay:float=0.90, stim_max_symbols:int=64,
                 checkpoint_format:str="h5", checkpoint_keep:int=5, load_engram_path:str=None,
                 start_control_server:bool=False, emergent_macros:bool=False):
        self.run_dir = run_dir
        self.N = N
        self.k = k
        self.hz = hz
        self.dt = 1.0 / max(1, hz)
        self.domain = domain
        self.use_time_dynamics = use_time_dynamics
        self.viz_every = viz_every
        self.log_every = log_every
        self.checkpoint_every = checkpoint_every
        self.seed = seed
        self.emergent_macros = bool(emergent_macros)

        os.makedirs(self.run_dir, exist_ok=True)
        self.logger = get_logger("nexus", os.path.join(self.run_dir, "events.jsonl"))
        inbox_path = os.path.join(self.run_dir, "chat_inbox.jsonl")
        self.ute = UTE(use_stdin=True, inbox_path=inbox_path)
        self.utd = UTD(self.run_dir)
        # Macro emitter (write-only; respects UTD_OUT if set)
        try:
            out_path = os.getenv("UTD_OUT") or getattr(self.utd, "path", os.path.join(self.run_dir, "utd_events.jsonl"))
            self.emitter = MacroEmitter(path=out_path, why_provider=lambda: self._emit_why())
        except Exception:
            self.emitter = None
        # Introspection Ledger (emit-only), behind feature flag ENABLE_THOUGHTS
        self.thoughts = None
        try:
            if str(os.getenv("ENABLE_THOUGHTS", "0")).lower() in ("1", "true", "yes", "on"):
                th_path = os.getenv("THOUGHT_OUT") or os.path.join(self.run_dir, "thoughts.ndjson")
                self.thoughts = ThoughtEmitter(path=th_path, why=lambda: self._emit_why())
        except Exception:
            self.thoughts = None
        # Start local control server only when requested (default: off)
        self._control_server = None
        if bool(start_control_server) and ControlServer is not None:
            try:
                self._control_server = ControlServer(self.run_dir)
                try:
                    self.logger.info("control_server_started", extra={"extra": {"url": getattr(self._control_server, "url", "")}})
                except Exception:
                    pass
            except Exception:
                self._control_server = None
        # Macro board: minimal defaults + optional JSON registry
        try:
            self.utd.register_macro('status', {'desc': 'Emit structured status payload'})
            self.utd.register_macro('say', {'desc': 'Emit plain text line'})
            macro_candidates = [
                os.path.join(self.run_dir, 'macro_board.json'),
            ]
            for pth in macro_candidates:
                if os.path.exists(pth):
                    with open(pth, 'r', encoding='utf-8') as fh:
                        reg = json.load(fh)
                    if isinstance(reg, dict):
                        for name, meta in reg.items():
                            try:
                                # Only per-run board can provide metadata/templates to preserve emergent language
                                self.utd.register_macro(str(name), meta if isinstance(meta, dict) else {})
                            except Exception:
                                pass
                    break
        except Exception:
            pass

        # Phrase templates for 'say' macro and persistent lexicon (for richer sentences)
        self._phrase_templates = []
        try:
            self._phrase_templates = list(_lxn_load_phrases(self.run_dir) or [])
        except Exception:
            # Fail-soft: keep empty; store mirrors legacy behavior
            pass
        # 3) Persistent lexicon (word -> count), learned from inbound text and emissions
        try:
            self._lexicon_path = os.path.join(self.run_dir, 'lexicon.json')
            lx, dc = _lxn_load(self.run_dir)
            self._lexicon = dict(lx or {})
            self._doc_count = int(dc or 0)
        except Exception:
            # Fail-soft: empty lexicon
            self._lexicon = {}
            self._doc_count = 0
            pass

        # N-gram stores for emergent sentence composition (learned from inputs/outputs)
        self._ng2 = {}  # bigram: w1 -> {w2: count}
        self._ng3 = {}  # trigram: (w1,w2) -> {w3: count}

        # Select connectome backend (dense vs sparse) with void-faithful parameters
        if sparse_mode:
            self.connectome = SparseConnectome(
                N=self.N, k=self.k, seed=self.seed,
                threshold=threshold, lambda_omega=lambda_omega,
                candidates=candidates, traversal_walkers=walkers, traversal_hops=hops,
                bundle_size=bundle_size
            )
        else:
            self.connectome = Connectome(
                N=self.N, k=self.k, seed=self.seed,
                threshold=threshold, lambda_omega=lambda_omega,
                candidates=candidates, traversal_walkers=walkers, traversal_hops=hops,
                bundle_size=bundle_size, prune_factor=prune_factor
            )
        # Load engram if provided (after backend selection)
        # Defer engram loading until after ADC is initialized to avoid spurious errors/logs.
        # The actual load (with logging) happens below after ADC is constructed.
        self.vis = Visualizer(run_dir=self.run_dir)
        # Status emission cadence for UTD
        self.status_every = max(1, int(status_interval))
        # Self-Improvement Engine (Rule 3): produces signed total_reward and legacy valence_01
        self.sie = SelfImprovementEngine(self.N)
        # Engram persistence config
        self.checkpoint_every = int(checkpoint_every)
        self.checkpoint_format = str(checkpoint_format).lower()
        self.checkpoint_keep = int(max(0, checkpoint_keep))
        # Text stimulus wiring for symbol→group activation
        self.stim_group_size = int(max(1, stim_group_size))
        self.stim_amp = float(stim_amp)
        self.stim_max_symbols = int(max(1, stim_max_symbols))
        try:
            if hasattr(self.connectome, "_stim_decay"):
                self.connectome._stim_decay = float(stim_decay)
        except Exception:
            pass

        # Self-speak configuration and topology spike detector (tick-based)
        self.speak_auto = bool(speak_auto)
        self.speak_valence_thresh = float(speak_valence_thresh)
        # Persist half-life for void_b1 meter to keep UX consistent with detector
        self.b1_half_life_ticks = int(max(1, b1_half_life_ticks))
        self.b1_detector = StreamingZEMA(
            half_life_ticks=self.b1_half_life_ticks,
            z_spike=float(speak_z),
            hysteresis=float(speak_hysteresis),
            min_interval_ticks=int(max(1, speak_cooldown_ticks)),
        )
        # Optional event-driven metrics aggregator (disabled by default; parity preserved)
        self._evt_metrics = None
        try:
            if str(os.getenv("ENABLE_EVENT_METRICS", "0")).lower() in ("1", "true", "yes", "on"):
                self._evt_metrics = _EvtMetrics(
                    z_half_life_ticks=self.b1_half_life_ticks,
                    z_spike=float(speak_z),
                    hysteresis=float(speak_hysteresis),
                    seed=int(self.seed),
                )
        except Exception:
            self._evt_metrics = None
        # External control plane: phase file and cache (void-faithful: gates only)
        self.phase_file = os.path.join(self.run_dir, "phase.json")
        self._phase = {"phase": 0}
        self._phase_mtime = None
        # Novelty rarity gain (tunable via phase.json under "sie": {"novelty_idf_gain": ...})
        self.novelty_idf_gain = 1.0

        # Announcement bus + ADC (void-walker observations -> incremental map)
        self.bus = AnnounceBus(capacity=int(max(1, bus_capacity)))
        self.bus_drain = int(max(1, bus_drain))
        self.adc = ADC(r_attach=float(r_attach), ttl_init=int(ttl_init), split_patience=int(split_patience))
        # Attach bus to connectome so walkers can publish Observation events
        try:
            self.connectome.bus = self.bus
        except Exception:
            pass

        # If an engram path was provided earlier and ADC is now available, reload including ADC
        # Load engram once ADC is available, with clear success/error logs for the UI
        if load_engram_path:
            try:
                _load_engram_state(str(load_engram_path), self.connectome, adc=self.adc)
                try:
                    self.logger.info("engram_loaded", extra={"extra": {"path": str(load_engram_path)}})
                except Exception:
                    pass
            except Exception as e:
                try:
                    self.logger.info("engram_load_error", extra={"extra": {"err": str(e), "path": str(load_engram_path)}})
                except Exception:
                    pass
        # Derive starting step to continue numbering after resume and avoid retention deleting new snapshots
        try:
            s = None
            lp = str(load_engram_path) if load_engram_path else None
            if lp and os.path.isfile(lp):
                base = os.path.basename(lp)
                m = re.search(r"state_(\d+)\.(h5|npz)$", base)
                if m:
                    s = int(m.group(1))
            if s is None:
                # Fallback: scan run_dir for highest step across known formats
                max_s = -1
                for fn in os.listdir(self.run_dir):
                    if not fn.startswith("state_"):
                        continue
                    m2 = re.search(r"state_(\d+)\.(h5|npz)$", fn)
                    if m2:
                        ss = int(m2.group(1))
                        if ss > max_s:
                            max_s = ss
                if max_s >= 0:
                    s = max_s
            self.start_step = int(s) + 1 if s is not None else 0
            try:
                self.logger.info("resume_step", extra={"extra": {"start_step": int(self.start_step)}})
            except Exception:
                pass
        except Exception:
            self.start_step = 0
        self.dom_mod = float(get_domain_modulation(self.domain))
        self.history = []
        # Emitter context (read-only snapshot for why providers)
        self._emit_step = 0
        self._emit_last_metrics = {}
        self._macros_smoke_done = False
        self._thoughts_smoke_done = False
        # Rolling buffer of recent inbound text for composing human-friendly “say” content
        self.recent_text = deque(maxlen=256)
        # Track vt_entropy over time for SIE TD proxy (void-native signal)
        self._prev_vt_entropy = None
        self._last_vt_entropy = None

    def _symbols_to_indices(self, text, reverse_map=None):
        """
        Deterministic, stateless symbol→group mapping.

        Delegates to io.cognition.stimulus.symbols_to_indices (behavior-preserving).
        """
        try:
            return _stim_symbols_to_indices(
                str(text),
                int(getattr(self, "stim_group_size", 4)),
                int(getattr(self, "stim_max_symbols", 64)),
                int(self.N),
                reverse_map=reverse_map,
            )
        except Exception:
            return []

    def _update_lexicon_and_ngrams(self, text: str):
        try:
            if not hasattr(self, "_lexicon"): self._lexicon = {}
            toks = text_utils.tokenize_text(text)
            # Document-frequency semantics: increment once per message per token
            for w in set(toks):
                self._lexicon[w] = int(self._lexicon.get(w, 0)) + 1
            # Update streaming n-grams for emergent composition
            text_utils.update_ngrams(toks, self._ng2, self._ng3)
        except Exception: pass

    def _save_lexicon(self):
        try:
            _lxn_save(self.run_dir, getattr(self, "_lexicon", {}) or {}, int(getattr(self, "_doc_count", 0)))
        except Exception:
            pass

    def _compose_say_text(self, metrics: dict, step: int, seed_tokens: set = None) -> str:
        """
        Compose a short sentence using emergent language or templates.

        Delegates to io.cognition.composer.compose_say_text (behavior-preserving).
        """
        try:
            return _compose_say_text_impl(
                metrics or {},
                int(step),
                getattr(self, "_lexicon", {}) or {},
                getattr(self, "_ng2", {}) or {},
                getattr(self, "_ng3", {}) or {},
                self.recent_text,
                templates=list(getattr(self, "_phrase_templates", []) or []),
                seed_tokens=seed_tokens,
            ) or ""
        except Exception:
            return ""

    def _emit_why(self):
        """
        Provide context for MacroEmitter / ThoughtEmitter from the last computed metrics.
        Read-only; never mutates model state.
        """
        try:
            m = getattr(self, "_emit_last_metrics", {}) or {}
            step = int(getattr(self, "_emit_step", 0))
            return _telemetry_why_base(self, m, step)
        except Exception:
            try:
                return {"t": int(getattr(self, "_emit_step", 0)), "phase": int(getattr(self, "_phase", {}).get("phase", 0))}
            except Exception:
                return {"t": 0, "phase": 0}

        # --- Phase control plane (file-driven) ---------------------------------
    def _default_phase_profiles(self):
        # Delegated to modular control-plane helper (no behavior change)
        try:
            from .runtime.phase import default_phase_profiles as _default_phase_profiles
            return _default_phase_profiles()
        except Exception:
            # Fallback to original inline defaults to preserve behavior if import fails unexpectedly
            return {
                0: {  # primitives
                    "speak": {"speak_z": 2.0, "speak_hysteresis": 0.5, "speak_cooldown_ticks": 8, "speak_valence_thresh": 0.10},
                    "connectome": {"walkers": 128, "hops": 3, "bundle_size": 3, "prune_factor": 0.10},
                },
                1: {  # blocks
                    "speak": {"speak_z": 2.5, "speak_hysteresis": 0.8, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.20},
                    "connectome": {"walkers": 256, "hops": 3, "bundle_size": 3, "prune_factor": 0.10},
                },
                2: {  # structures
                    "speak": {"speak_z": 3.0, "speak_hysteresis": 1.0, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.35},
                    "connectome": {"walkers": 384, "hops": 4, "bundle_size": 3, "prune_factor": 0.10},
                },
                3: {  # questions
                    "speak": {"speak_z": 3.0, "speak_hysteresis": 1.0, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.55},
                    "connectome": {"walkers": 512, "hops": 4, "bundle_size": 3, "prune_factor": 0.10},
                },
                4: {  # problem-solving
                    "speak": {"speak_z": 3.5, "speak_hysteresis": 1.2, "speak_cooldown_ticks": 12, "speak_valence_thresh": 0.60},
                    "connectome": {"walkers": 768, "hops": 5, "bundle_size": 3, "prune_factor": 0.10},
                },
            }

    def _apply_phase_profile(self, prof: dict):
        # Delegated to modular control-plane helper (no behavior change)
        try:
            from .runtime.phase import apply_phase_profile as _apply_phase_profile_impl
            return _apply_phase_profile_impl(self, prof)
        except Exception:
            # Inline fallback mirrors previous behavior to avoid any functional change
            # Apply speak gates
            sp = prof.get("speak", {})
            try:
                if "speak_z" in sp:
                    self.b1_detector.z_spike = float(sp["speak_z"])
                if "speak_hysteresis" in sp:
                    self.b1_detector.hysteresis = float(max(0.0, sp["speak_hysteresis"]))
                if "speak_cooldown_ticks" in sp:
                    self.b1_detector.min_interval = int(max(1, int(sp["speak_cooldown_ticks"])))
                if "speak_valence_thresh" in sp:
                    self.speak_valence_thresh = float(sp["speak_valence_thresh"])
            except Exception:
                pass
            # Apply connectome traversal/homeostasis gates
            cn = prof.get("connectome", {})
            C = getattr(self, "connectome", None)
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
                    # Allow live tuning of active-edge threshold (affects density and SIE TD proxy)
                    if "threshold" in cn and hasattr(C, "threshold"):
                        C.threshold = float(max(0.0, float(cn["threshold"])))
                    # Allow live tuning of void-penalty and candidate budget
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
                    targets.append(getattr(self, "sie", None))
                except Exception:
                    pass
                # also allow Connectome-scope SIE if present
                try:
                    _C = getattr(self, "connectome", None)
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
                    self.novelty_idf_gain = float(sie["novelty_idf_gain"])
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

            # ---- Schedules / housekeeping ----
            sched = prof.get("schedule", {})
            if sched:
                try:
                    if "adc_entropy_alpha" in sched:
                        self.adc_entropy_alpha = float(sched["adc_entropy_alpha"])
                except Exception:
                    pass
                try:
                    if "ph_snapshot_interval_sec" in sched:
                        self.ph_snapshot_interval_sec = float(sched["ph_snapshot_interval_sec"])
                except Exception:
                    pass
    def _poll_control(self):
        # Delegated to modular control-plane helper (no behavior change)
        try:
            from .runtime.phase import poll_control as _poll_control_impl
            return _poll_control_impl(self)
        except Exception:
            # Inline fallback mirrors previous behavior to avoid any functional change
            try:
                pth = getattr(self, "phase_file", None)
                if not pth or not os.path.exists(pth):
                    return
                try:
                    st = os.stat(pth)
                    mt = float(getattr(st, "st_mtime", 0.0))
                except Exception:
                    return
                if self._phase_mtime is not None and mt <= float(self._phase_mtime):
                    return
                with open(pth, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if not isinstance(data, dict):
                    return
                # Merge defaults for simple {"phase": n} shape
                phase_idx = int(data.get("phase", self._phase.get("phase", 0)))
                prof = self._default_phase_profiles().get(phase_idx, {})
                # One-shot engram load if requested by control plane
                try:
                    load_p = data.get("load_engram", None)
                    if isinstance(load_p, str) and load_p.strip():
                        _load_engram_state(str(load_p), self.connectome, adc=self.adc)
                        try:
                            self.logger.info("engram_loaded", extra={"extra": {"path": str(load_p)}})
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
                self._phase = {"phase": phase_idx, **prof}
                self._apply_phase_profile(prof)
                self._phase_mtime = mt
                try:
                    self.logger.info("phase_applied", extra={"extra": {"phase": phase_idx, "profile": prof}})
                except Exception:
                    pass
            except Exception:
                pass
    
    def run(self, duration_s:int=None):
        self.ute.start()
        self.logger.info("nexus_started", extra={"extra": {"N": self.N, "k": self.k, "hz": self.hz, "domain": self.domain, "dom_mod": self.dom_mod}})
        try:
            self.logger.info("checkpoint_config", extra={"extra": {"every": int(getattr(self, "checkpoint_every", 0)), "keep": int(getattr(self, "checkpoint_keep", 0)), "format": str(getattr(self, "checkpoint_format", ""))}})
        except Exception:
            pass
        t0 = time.time()
        step = int(getattr(self, "start_step", 0))
        try:
            while True:
                tick_start = time.time()
                # 1) ingest
                msgs = self.ute.poll()
                ute_in_count = len(msgs)
                ute_text_count = 0
                stim_idxs = set()
                tick_tokens = set()
                tick_rev_map = {}
                for m in msgs:
                    if m.get('type') == 'text':
                        ute_text_count += 1
                        # translate inbound text → deterministic neuron groups
                        try:
                            text = str(m.get('msg', ''))
                            try:
                                self.recent_text.append(text)
                            except Exception:
                                pass
                            try:
                                # Update rolling lexicon, n-grams, and get tokens for IDF
                                self._update_lexicon_and_ngrams(text)
                                toks = text_utils.tokenize_text(text)
                                for w in set(toks):
                                    tick_tokens.add(w)
                                # Increment document counter once per inbound text message
                                self._doc_count = int(getattr(self, "_doc_count", 0)) + 1
                            except Exception:
                                pass
                            idxs = self._symbols_to_indices(text, reverse_map=tick_rev_map)
                            for i in idxs:
                                stim_idxs.add(int(i))
                        except Exception:
                            pass
                        self.utd.emit_text(m)
                # inject the accumulated stimulation before the learning step
                if stim_idxs:
                    try:
                        self.connectome.stimulate_indices(sorted(stim_idxs), amp=float(self.stim_amp))
                    except Exception:
                        pass

                # Control plane: poll external phase control (file: runs/<ts>/phase.json)
                try:
                    self._poll_control()
                except Exception:
                    pass

                # 2) SIE drive + update connectome
                # use wall-clock seconds since start as t
                t = time.time() - t0

                # Compute undirected density cheaply from active edge count
                try:
                    E = max(0, int(self.connectome.active_edge_count()))
                    N = max(1, int(self.N))
                    denom = float(N * (N - 1))
                    density = (2.0 * E / denom) if denom > 0 else 0.0
                except Exception:
                    density = 0.0

                # IDF novelty is composer/telemetry-only; keep dynamics neutral per safe pattern
                idf_scale = 1.0

                # TD-like signal from topology change (normalized delta in active edges)
                try:
                    prev_E = getattr(self, "_prev_active_edges", E)
                    delta_e = float(E - prev_E) / float(max(1, E))
                    # Combine structural change and traversal entropy change as a void-native TD proxy
                    try:
                        vte_prev = getattr(self, "_prev_vt_entropy", None)
                        vte_last = getattr(self, "_last_vt_entropy", None)
                        vt_delta = 0.0 if (vte_prev is None or vte_last is None) else float(vte_last - vte_prev)
                    except Exception:
                        vt_delta = 0.0
                    td_raw = 4.0 * delta_e + 1.5 * vt_delta
                    td_signal = max(-2.0, min(2.0, td_raw))
                    self._prev_active_edges = E
                except Exception:
                    td_signal = 0.0
        
                # Firing variability proxy for HSI (variance of field W)
                try:
                    firing_var = float(self.connectome.W.var())
                except Exception:
                    firing_var = None
        
                # Get SIE drive (total_reward in [-1,1], valence_01 in [0,1])
                drive = self.sie.get_drive(
                    W=None,
                    external_signal=float(td_signal),
                    time_step=int(step),
                    firing_var=firing_var,
                    target_var=0.15,
                    density_override=density,
                    novelty_idf_scale=float(idf_scale)
                )
                sie_drive = float(drive.get("valence_01", 1.0))
                # Prefer SIE v2 valence (from W,dW) when available; fall back to legacy
                try:
                    sie2 = float(getattr(self.connectome, "_last_sie2_valence", 0.0))
                except Exception:
                    sie2 = 0.0
                sie_gate = max(0.0, min(1.0, max(sie_drive, sie2)))
 
                # Update connectome, gating universal void dynamics by sie_gate
                self.connectome.step(
                    t,
                    domain_modulation=self.dom_mod,
                    sie_drive=sie_gate,
                    use_time_dynamics=self.use_time_dynamics
                )

                # 3) metrics & logs (merge SIE components + traversal findings)
                m = compute_metrics(self.connectome)
                # attach structural homeostasis and TD diagnostics (void-native)
                try:
                    m["homeostasis_pruned"] = int(getattr(self.connectome, "_last_pruned_count", 0))
                    m["homeostasis_bridged"] = int(getattr(self.connectome, "_last_bridged_count", 0))
                    m["active_edges"] = int(E)
                    m["td_signal"] = float(td_signal)
                    # expose the IDF novelty scale used this tick
                    m["novelty_idf_scale"] = float(idf_scale)
                    if firing_var is not None:
                        m["firing_var"] = float(firing_var)
                except Exception:
                    pass
                # attach traversal findings
                if getattr(self.connectome, "findings", None):
                    m.update(self.connectome.findings)
                # expose sie_gate used this tick for diagnostics
                try:
                    m["sie_gate"] = float(sie_gate)
                except Exception:
                    pass
                # update vt_entropy history for next tick's TD proxy
                try:
                    self._prev_vt_entropy = getattr(self, "_last_vt_entropy", None)
                    self._last_vt_entropy = float(m.get("vt_entropy", 0.0))
                except Exception:
                    pass
                # Drain announcement bus, extract void-driven topic, then update ADC
                void_topic_symbols = set()
                try:
                    obs_batch = self.bus.drain(max_items=self.bus_drain)
                    if obs_batch:
                        # Map observed node indices back to symbols seen this tick
                        for obs in obs_batch:
                            nodes = getattr(obs, "nodes", None)
                            if nodes:
                                for idx in nodes:
                                    sym = tick_rev_map.get(int(idx)) if isinstance(tick_rev_map, dict) else None
                                    if sym is not None:
                                        void_topic_symbols.add(sym)
                        # Update ADC after extracting topic so we don't interfere with its internal logic
                        self.adc.update_from(obs_batch)
                        adc_metrics = self.adc.get_metrics()
                        # Optionally fold event-driven metrics (feature-flagged; telemetry-only)
                        try:
                            if getattr(self, "_evt_metrics", None) is not None:
                                evs = _obs_to_events(obs_batch)
                                for _ev in evs:
                                    try:
                                        self._evt_metrics.update(_ev)
                                    except Exception:
                                        pass
                                try:
                                    self._evt_metrics.update(_adc_event(adc_metrics, t=int(step)))
                                except Exception:
                                    pass
                                try:
                                    evsnap = self._evt_metrics.snapshot()
                                    m.update(evsnap)
                                except Exception:
                                    pass
                        except Exception:
                            pass
                        # fold ADC metrics in; also add cycle hits to the cycle proxy so b1_z sees them
                        m.update(adc_metrics)
                        m["complexity_cycles"] = float(m.get("complexity_cycles", 0.0)) + float(adc_metrics.get("adc_cycle_hits", 0.0))
                except Exception:
                    pass
                # attach SIE top-level fields and components
                m["sie_total_reward"] = float(drive.get("total_reward", 0.0))
                m["sie_valence_01"]  = float(drive.get("valence_01", 0.0))
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
                # intrinsic SIE v2 (computed from W and dW within the connectome)
                try:
                    m["sie_v2_reward_mean"] = float(getattr(self.connectome, "_last_sie2_reward", 0.0))
                    m["sie_v2_valence_01"] = float(getattr(self.connectome, "_last_sie2_valence", 0.0))
                except Exception:
                    pass
                # current phase (control plane)
                try:
                    m["phase"] = int(getattr(self, "_phase", {}).get("phase", 0))
                except Exception:
                    m["phase"] = 0
                # B1 proxy from active-subgraph cycles (void-native)
                b1_value = float(m.get("complexity_cycles", 0.0))
                b1s = self.b1_detector.update(b1_value, tick=int(step))
                m["b1_value"] = float(b1s.get("value", 0.0))
                m["b1_delta"] = float(b1s.get("delta", 0.0))
                m["b1_z"] = float(b1s.get("z", 0.0))
                m["b1_spike"] = bool(b1s.get("spike", False))
                m['t'] = step
                m['ute_in_count'] = int(ute_in_count)
                m['ute_text_count'] = int(ute_text_count)
                # Update emitter contexts (used by why providers)
                try:
                    self._emit_step = int(step)
                    # include canonical valence fields for convenience
                    m["sie_valence_01"] = float(m.get("sie_valence_01", m.get("sie_total_reward", 0.0)))
                    self._emit_last_metrics = dict(m)
                except Exception:
                    pass
                # Optional one-shot smoke tests (no behavior change)
                try:
                    # Macro smoke (VARS/EDGES/etc.) if enabled
                    if (not getattr(self, "_macros_smoke_done", False)) and str(os.getenv("ENABLE_MACROS_TEST", "0")).lower() in ("1", "true", "yes", "on"):
                        if getattr(self, "emitter", None):
                            self.emitter.vars({"N": "neural", "G": "global_access", "E": "experience", "B": "behavior"})
                            self.emitter.edges(["N->G", "G->B", "E->B?"])
                            self.emitter.assumptions(["no unmeasured confounding", "positivity"])
                            self.emitter.target("P(B|do(G))")
                            self.emitter.derivation("If N fixes G and G mediates B, therefore adjust on {confounders} yields effect.")
                            self.emitter.prediction_delta("Behavioral margin differs if extra-law holds.")
                            self.emitter.transfer("Circuit: signal->bus; flag->output; hidden noise.")
                            self.emitter.equation("Y = β X + U_Y")
                            self.emitter.status("macro smoke: ok")
                        self._macros_smoke_done = True
                    # Thought ledger smoke (emit once per kind) if enabled
                    if (not getattr(self, "_thoughts_smoke_done", False)) and str(os.getenv("ENABLE_THOUGHTS_TEST", "0")).lower() in ("1", "true", "yes", "on"):
                        if getattr(self, "thoughts", None):
                            self.thoughts.observation("vt_entropy", float(m.get("vt_entropy", 0.0)))
                            self.thoughts.motif("cycle_probe", nodes=[1, 2, 3])
                            self.thoughts.hypothesis("H0", "A ⟂ B | Z", status="tentative", conf=0.55)
                            self.thoughts.test("CI", True, vars={"A": "A", "B": "B", "Z": ["Z"]})
                            self.thoughts.derivation(["H0", "obs:vt_coverage↑"], "Identify P(Y|do(X)) via backdoor on {Z}", conf=0.6)
                            self.thoughts.revision("H0", "accepted", because=["test:CI:true"])
                            self.thoughts.plan("intervene", vars={"target": "X"}, rationale="disambiguate twins")
                        self._thoughts_smoke_done = True
                except Exception:
                    pass
                self.history.append(m)
                # Prevent unbounded memory growth of in‑process history buffer (can cause random stops/OOM)
                try:
                    max_keep = 20000   # keep at most 20k ticks of history
                    trim_to = 10000    # when trimming, retain the last 10k for continuity
                    if len(self.history) > max_keep:
                        self.history = self.history[-trim_to:]
                except Exception:
                    pass
 
                # Periodically persist learned lexicon
                try:
                    if (step % max(100, int(self.status_every) * 10)) == 0:
                        self._save_lexicon()
                except Exception:
                    pass

                # Autonomous speaking based on topology spikes and valence
                try:
                    val_v2 = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
                    spike = bool(m.get("b1_spike", False))
                    if self.speak_auto:
                        can_speak, reason = _speak_gate(val_v2, spike, float(self.speak_valence_thresh))
                        if can_speak:
                            # Compose; do not suppress due to lack of topic/tokens. Model controls content fully.
                            seed_material = tick_tokens if tick_tokens else void_topic_symbols
                            speech = self._compose_say_text(m, int(step), seed_tokens=seed_material)
                            # k from control-plane or env; discovery default 0.0
                            try:
                                composer_k = float(getattr(self, "_phase", {}).get("composer_idf_k", float(os.getenv("COMPOSER_IDF_K", "0.0"))))
                            except Exception:
                                composer_k = 0.0
                            # Composer-local novelty IDF + score (telemetry/emitter only; does not affect dynamics)
                            novelty_idf, score_out = _novelty_and_score(
                                speech,
                                getattr(self, "_lexicon", {}) or {},
                                int(getattr(self, "_doc_count", 0)),
                                text_utils.tokenize_text,
                                float(composer_k),
                                float(val_v2),
                            )
                            # Update learned lexicon after computing novelty (avoid self-bias in estimate)
                            self._update_lexicon_and_ngrams(speech)
                            why = _telemetry_why_base(self, m, int(step))
                            try:
                                why["novelty_idf"] = float(novelty_idf)
                                why["composer_idf_k"] = float(composer_k)
                            except Exception:
                                pass
                            self.utd.emit_macro(
                                "say",
                                {
                                    "text": speech,
                                    "why": why,
                                },
                                score=score_out,
                            )
                        else:
                            # Log suppression only for low valence (silent when no spike)
                            if reason == "low_valence":
                                try:
                                    self.logger.info(
                                        "speak_suppressed",
                                        extra={
                                            "extra": {
                                                "reason": "low_valence",
                                                "val": val_v2,
                                                "thresh": float(self.speak_valence_thresh),
                                                "b1_z": float(m.get("b1_z", 0.0)),
                                                "t": int(step),
                                            }
                                        },
                                    )
                                except Exception:
                                    pass
                except Exception:
                    pass

                if (step % self.log_every) == 0:
                    try:
                        self.logger.info("tick", extra={"extra": m})
                    except Exception as e:
                        # Attempt a safe fallback serialization and retry once
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
                            self.logger.info("tick", extra={"extra": safe})
                        except Exception:
                            # As last resort, write to stderr so supervisor can see the error
                            print("[nexus] tick_log_error", str(e), file=sys.stderr, flush=True)
 
                if (step % self.status_every) == 0:
                    # Open UTD: emit a status text payload at configured interval (void-faithful score via valence)
                    try:
                        payload = _telemetry_status(self, m, int(step))
                        score = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
                        self.utd.emit_text(payload, score=score)
                    except Exception:
                        pass
                    # Macro board: emit a status macro when valence is high
                    try:
                        val = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
                        if val >= 0.6:
                            self.utd.emit_macro(
                                "status",
                                {
                                    "t": int(step),
                                    "neurons": int(self.N),
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

                if self.viz_every and (step % self.viz_every) == 0 and step > 0:
                    try:
                        self.vis.dashboard(self.history[-max(50, self.viz_every*2):])  # last window
                        # Guard expensive graph snapshot at scale
                        if int(self.N) <= 10000:
                            G = self.connectome.snapshot_graph()
                            self.vis.graph(G, fname='connectome.png')
                    except Exception as e:
                        self.logger.info("viz_error", extra={"extra": {"err": str(e)}})

                if self.checkpoint_every and (step % self.checkpoint_every) == 0 and step > 0:
                    # Save engram as HDF5 (falls back to .npz only if h5py is unavailable)
                    try:
                        path = save_checkpoint(self.run_dir, step, self.connectome, fmt=self.checkpoint_format or "h5", adc=self.adc)
                        # Emit explicit event so UI/logs can confirm checkpointing activity
                        try:
                            self.logger.info("checkpoint_saved", extra={"extra": {"path": str(path), "step": int(step)}})
                        except Exception:
                            pass
                        # Rolling retention: keep last K checkpoints via helper (0 disables)
                        if getattr(self, "checkpoint_keep", 0) and int(self.checkpoint_keep) > 0:
                            try:
                                summary = _prune_ckpt(self.run_dir, keep=int(self.checkpoint_keep), last_path=path)
                                try:
                                    self.logger.info("checkpoint_retention", extra={"extra": summary})
                                except Exception:
                                    pass
                            except Exception:
                                pass
                    except Exception as e:
                        try:
                            self.logger.info("checkpoint_error", extra={"extra": {"err": str(e)}})
                        except Exception:
                            pass

                step += 1
                # 4) pacing
                elapsed = time.time() - tick_start
                sleep = max(0.0, self.dt - elapsed)
                time.sleep(sleep)

                if duration_s is not None and (time.time() - t0) > duration_s:
                    try:
                        self.logger.info("nexus_duration_reached", extra={"extra": {"duration_s": int(duration_s)}})
                    except Exception:
                        pass
                    break
        except Exception as e:
            try:
                self.logger.info("nexus_fatal", extra={"extra": {"err": str(e)}})
            except Exception:
                try:
                    print("[nexus] fatal", str(e), file=sys.stderr, flush=True)
                except Exception:
                    pass
        finally:
            self.utd.close()
            # Stop local control server on exit
            try:
                if getattr(self, "_control_server", None):
                    self._control_server.stop()
            except Exception:
                pass

def make_parser():
    p = argparse.ArgumentParser()
    p.add_argument('--neurons', type=int, default=1000)
    p.add_argument('--k', type=int, default=12)
    p.add_argument('--hz', type=int, default=10)
    p.add_argument('--domain', type=str, default='biology_consciousness')
    p.add_argument('--viz-every', type=int, default=10)
    p.add_argument('--log-every', type=int, default=1)
    p.add_argument('--checkpoint-every', type=int, default=0)
    p.add_argument('--checkpoint-keep', type=int, default=5)
    p.add_argument('--duration', type=int, default=None)
    p.add_argument('--use-time-dynamics', dest='use_time_dynamics', action='store_true')
    p.add_argument('--no-time-dynamics', dest='use_time_dynamics', action='store_false')
    p.set_defaults(use_time_dynamics=True)
    p.add_argument('--seed', type=int, default=0)

    # Ultra-scale/sparse flags
    p.add_argument('--sparse-mode', dest='sparse_mode', action='store_true')
    p.add_argument('--dense-mode', dest='sparse_mode', action='store_false')
    # Aliases
    p.add_argument('--sparse', dest='sparse_mode', action='store_true')
    p.add_argument('--dense', dest='sparse_mode', action='store_false')
    p.set_defaults(sparse_mode=None)
    p.add_argument('--threshold', type=float, default=0.15)
    p.add_argument('--lambda-omega', dest='lambda_omega', type=float, default=0.1)
    p.add_argument('--candidates', type=int, default=64)
    p.add_argument('--walkers', type=int, default=256)
    p.add_argument('--hops', type=int, default=3)
    p.add_argument('--status-interval', dest='status_interval', type=int, default=1)
    p.add_argument('--bundle-size', dest='bundle_size', type=int, default=3)
    p.add_argument('--prune-factor', dest='prune_factor', type=float, default=0.10)

    # Text→connectome stimulation (symbol→group)
    p.add_argument('--stim-group-size', dest='stim_group_size', type=int, default=4)
    p.add_argument('--stim-amp', dest='stim_amp', type=float, default=0.05)
    p.add_argument('--stim-decay', dest='stim_decay', type=float, default=0.90)
    p.add_argument('--stim-max-symbols', dest='stim_max_symbols', type=int, default=64)

    # Self-speak and topology-spike detection (void-native)
    p.add_argument('--speak-auto', dest='speak_auto', action='store_true')
    p.add_argument('--no-speak-auto', dest='speak_auto', action='store_false')
    p.set_defaults(speak_auto=True)
    p.add_argument('--speak-z', dest='speak_z', type=float, default=1.0)
    p.add_argument('--speak-hysteresis', dest='speak_hysteresis', type=float, default=1.0)
    p.add_argument('--speak-cooldown-ticks', dest='speak_cooldown_ticks', type=int, default=10)
    p.add_argument('--speak-valence-thresh', dest='speak_valence_thresh', type=float, default=0.01)
    p.add_argument('--b1-half-life-ticks', dest='b1_half_life_ticks', type=int, default=50)

    # Announcement bus / ADC tuning
    p.add_argument('--bus-capacity', dest='bus_capacity', type=int, default=65536)
    p.add_argument('--bus-drain', dest='bus_drain', type=int, default=2048)
    p.add_argument('--r-attach', dest='r_attach', type=float, default=0.25)
    p.add_argument('--ttl-init', dest='ttl_init', type=int, default=120)
    p.add_argument('--split-patience', dest='split_patience', type=int, default=6)

    # Engram loader (optional)
    p.add_argument('--load-engram', dest='load_engram', type=str, default=None)
    # Optional embedded control server (disabled by default to avoid duplicate UI)
    p.add_argument('--control-server', dest='control_server', action='store_true')
    p.add_argument('--no-control-server', dest='control_server', action='store_false')
    p.set_defaults(control_server=False)
    # Allow explicit reuse of an existing run directory (resume), otherwise a new timestamp dir is used
    p.add_argument('--run-dir', dest='run_dir', type=str, default=None)

    return p
