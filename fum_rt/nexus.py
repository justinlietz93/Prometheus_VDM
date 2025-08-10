
import time, os, argparse, json, re
from collections import deque
from .utils.logging_setup import get_logger
from .io.ute import UTE
from .io.utd import UTD
from .core.connectome import Connectome
from .core.sparse_connectome import SparseConnectome
from .core.metrics import compute_metrics, StreamingZEMA
from .core.visualizer import Visualizer
from .core.memory import save_checkpoint, load_engram as _load_engram_state
from .core.void_dynamics_adapter import get_domain_modulation
from .core.fum_sie import SelfImprovementEngine
from .core.bus import AnnounceBus
from .core.adc import ADC

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
                 checkpoint_format:str="h5", checkpoint_keep:int=5, load_engram_path:str=None):
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

        os.makedirs(self.run_dir, exist_ok=True)
        self.logger = get_logger("nexus", os.path.join(self.run_dir, "events.jsonl"))
        self.ute = UTE(use_stdin=True)
        self.utd = UTD(self.run_dir)
        # Macro board: minimal defaults + optional JSON registry
        try:
            self.utd.register_macro('status', {'desc': 'Emit structured status payload'})
            self.utd.register_macro('say', {'desc': 'Emit plain text line'})
            macro_candidates = [
                os.path.join(self.run_dir, 'macro_board.json'),
                os.path.join('from_physicist_agent', 'macro_board_min.json'),
            ]
            for pth in macro_candidates:
                if os.path.exists(pth):
                    with open(pth, 'r', encoding='utf-8') as fh:
                        reg = json.load(fh)
                        if isinstance(reg, dict):
                            for name, meta in reg.items():
                                try:
                                    self.utd.register_macro(str(name), meta if isinstance(meta, dict) else {})
                                except Exception:
                                    pass
                    break
        except Exception:
            pass
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
        if load_engram_path:
            try:
                _load_engram_state(str(load_engram_path), self.connectome)
                try:
                    self.logger.info("engram_loaded", extra={"extra": {"path": str(load_engram_path)}})
                except Exception:
                    pass
            except Exception as e:
                try:
                    self.logger.info("engram_load_error", extra={"extra": {"err": str(e), "path": str(load_engram_path)}})
                except Exception:
                    pass
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
        self.b1_detector = StreamingZEMA(
            half_life_ticks=int(max(1, b1_half_life_ticks)),
            z_spike=float(speak_z),
            hysteresis=float(speak_hysteresis),
            min_interval_ticks=int(max(1, speak_cooldown_ticks)),
        )
        # External control plane: phase file and cache (void-faithful: gates only)
        self.phase_file = os.path.join(self.run_dir, "phase.json")
        self._phase = {"phase": 0}
        self._phase_mtime = None

        # Announcement bus + ADC (void-walker observations -> incremental map)
        self.bus = AnnounceBus(capacity=int(max(1, bus_capacity)))
        self.bus_drain = int(max(1, bus_drain))
        self.adc = ADC(r_attach=float(r_attach), ttl_init=int(ttl_init), split_patience=int(split_patience))
        # Attach bus to connectome so walkers can publish Observation events
        try:
            self.connectome.bus = self.bus
        except Exception:
            pass

        self.dom_mod = float(get_domain_modulation(self.domain))
        self.history = []
        # Rolling buffer of recent inbound text for composing human-friendly “say” content
        self.recent_text = deque(maxlen=256)

    def _symbols_to_indices(self, text):
        """
        Deterministic, stateless symbol→group mapping.
        Each unique symbol maps to 'stim_group_size' neuron indices via a stable arithmetic hash.
        """
        try:
            g = int(max(1, getattr(self, "stim_group_size", 4)))
            max_syms = int(max(1, getattr(self, "stim_max_symbols", 64)))
            N = int(self.N)
            out = []
            seen = set()
            for ch in str(text):
                if ch in seen:
                    continue
                seen.add(ch)
                code = ord(ch)
                base = (code * 1315423911) % N
                for j in range(g):
                    idx = int((base + j * 2654435761) % N)
                    out.append(idx)
                if len(seen) >= max_syms:
                    break
            return out
        except Exception:
            return []

    def _keyword_summary(self, k: int = 4) -> str:
        """
        Deterministic, lightweight keyword extractor from recent_text buffer.
        Boundary-only helper (does not affect core learning).
        """
        try:
            if not self.recent_text:
                return ""
            txt = " ".join(list(self.recent_text)[-32:])
            words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_+\-]*", txt)]
            STOP = {
                "the","a","an","and","or","for","with","into","of","to","from","in","on","at","by","is",
                "are","was","were","be","been","being","it","this","that","as","if","then","than","so",
                "thus","such","not","no","nor","but","over","under","up","down","out","you","your",
                "yours","me","my","mine","we","our","ours","they","their","theirs","he","him","his",
                "she","her","hers","i","am","do","does","did","done","have","has","had","will","would",
                "can","could","should","shall","may","might"
            }
            words = [w for w in words if (w not in STOP and len(w) > 2)]
            if not words:
                return ""
            freq = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
            top = [w for w,_ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:max(1,int(k))]]
            return ", ".join(top)
        except Exception:
            return ""

    # --- Phase control plane (file-driven) ---------------------------------
    def _default_phase_profiles(self):
        # Safe default gates for incremental curriculum, void-faithful (no token logic)
        # You can override any field via runs/<ts>/phase.json
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
            except Exception:
                pass

    def _poll_control(self):
        # If phase.json exists and mtime changed, load and apply
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
        try:
            with open(pth, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                return
            # Merge defaults for simple {"phase": n} shape
            phase_idx = int(data.get("phase", self._phase.get("phase", 0)))
            prof = self._default_phase_profiles().get(phase_idx, {})
            # Overlay any explicit fields from file
            for k, v in data.items():
                if k == "phase":
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
        t0 = time.time()
        step = 0
        try:
            while True:
                tick_start = time.time()
                # 1) ingest
                msgs = self.ute.poll()
                ute_in_count = len(msgs)
                ute_text_count = 0
                stim_idxs = set()
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
                            idxs = self._symbols_to_indices(text)
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

                # TD-like signal from topology change (normalized delta in active edges)
                try:
                    prev_E = getattr(self, "_prev_active_edges", E)
                    delta_e = float(E - prev_E) / float(max(1, E))
                    # Emphasize meaningful structural changes; clip to [-2, 2]
                    td_signal = max(-2.0, min(2.0, 4.0 * delta_e))
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
                    density_override=density
                )
                sie_drive = float(drive.get("valence_01", 1.0))

                # Update connectome, gating universal void dynamics by sie_drive
                self.connectome.step(
                    t,
                    domain_modulation=self.dom_mod,
                    sie_drive=sie_drive,
                    use_time_dynamics=self.use_time_dynamics
                )

                # 3) metrics & logs (merge SIE components + traversal findings)
                m = compute_metrics(self.connectome)
                # attach traversal findings
                if getattr(self.connectome, "findings", None):
                    m.update(self.connectome.findings)
                # Drain announcement bus and update ADC
                try:
                    obs_batch = self.bus.drain(max_items=self.bus_drain)
                    if obs_batch:
                        self.adc.update_from(obs_batch)
                        adc_metrics = self.adc.get_metrics()
                        # fold ADC metrics in; also add cycle hits to the cycle proxy so b1_z sees them
                        m.update(adc_metrics)
                        m["complexity_cycles"] = float(m.get("complexity_cycles", 0.0)) + float(adc_metrics.get("adc_cycle_hits", 0.0))
                except Exception:
                    pass
                # attach SIE top-level fields and components
                m["sie_total_reward"] = float(drive.get("total_reward", 0.0))
                m["sie_valence_01"]  = float(drive.get("valence_01", 0.0))
                comps = drive.get("components", {})
                for k, v in comps.items():
                    m[f"sie_{k}"] = v
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
                self.history.append(m)

                # Autonomous speaking based on topology spikes and valence
                try:
                    val = float(m.get("sie_valence_01", 0.0))
                    spike = bool(m.get("b1_spike", False))
                    if self.speak_auto and spike:
                        if val >= self.speak_valence_thresh:
                            # Compose a brief English snippet from recent input to demonstrate symbol/word grounding
                            summary = ""
                            try:
                                summary = self._keyword_summary(4)
                            except Exception:
                                summary = ""
                            speech = "Topology discovery: salient loop detected."
                            if summary:
                                speech = f"Topology discovery: {summary}"
                            self.utd.emit_macro(
                                "say",
                                {
                                    "text": speech,
                                    "why": {
                                        "t": int(step),
                                        "phase": int(getattr(self, "_phase", {}).get("phase", 0)),
                                        "b1_z": float(m.get("b1_z", 0.0)),
                                        "cohesion_components": int(m.get("cohesion_components", 0)),
                                        "vt_coverage": float(m.get("vt_coverage", 0.0)),
                                        "vt_entropy": float(m.get("vt_entropy", 0.0)),
                                        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
                                        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0))),
                                    },
                                },
                                score=val,
                            )
                        else:
                            try:
                                self.logger.info(
                                    "speak_suppressed",
                                    extra={
                                        "extra": {
                                            "reason": "low_valence",
                                            "val": val,
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
                    self.logger.info("tick", extra={"extra": m})

                if (step % self.status_every) == 0:
                    # Open UTD: emit a status text payload at configured interval (void-faithful score via valence)
                    try:
                        payload = {
                            "type": "status",
                            "t": int(step),
                            "neurons": int(self.N),
                            "phase": int(m.get("phase", int(getattr(self, "_phase", {}).get("phase", 0)))),
                            "cohesion_components": int(m.get("cohesion_components", 0)),
                            "vt_coverage": float(m.get("vt_coverage", 0.0)),
                            "vt_entropy": float(m.get("vt_entropy", 0.0)),
                            "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
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
                        score = float(m.get("sie_valence_01", 0.0))
                        self.utd.emit_text(payload, score=score)
                    except Exception:
                        pass
                    # Macro board: emit a status macro when valence is high
                    try:
                        val = float(m.get("sie_valence_01", 0.0))
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
                        G = self.connectome.snapshot_graph()
                        self.vis.graph(G, fname='connectome.png')
                    except Exception as e:
                        self.logger.info("viz_error", extra={"extra": {"err": str(e)}})

                if self.checkpoint_every and (step % self.checkpoint_every) == 0 and step > 0:
                    # Save engram as HDF5 (falls back to .npz only if h5py is unavailable)
                    try:
                        path = save_checkpoint(self.run_dir, step, self.connectome, fmt=self.checkpoint_format or "h5")
                        # Rolling retention: keep last K checkpoints of the actual format we just saved (0 disables)
                        if getattr(self, "checkpoint_keep", 0) and int(self.checkpoint_keep) > 0:
                            try:
                                ext = os.path.splitext(path)[1].lower()
                                files = []
                                for fn in os.listdir(self.run_dir):
                                    if not fn.startswith("state_") or not fn.endswith(ext):
                                        continue
                                    # "state_<step><ext>"
                                    step_str = fn[6:-len(ext)] if len(ext) > 0 else fn[6:]
                                    try:
                                        s = int(step_str)
                                        files.append((s, fn))
                                    except Exception:
                                        pass
                                if len(files) > int(self.checkpoint_keep):
                                    files.sort(key=lambda x: x[0], reverse=True)
                                    to_delete = files[int(self.checkpoint_keep):]
                                    removed = 0
                                    for _, fn in to_delete:
                                        try:
                                            os.remove(os.path.join(self.run_dir, fn))
                                            removed += 1
                                        except Exception:
                                            pass
                                    try:
                                        self.logger.info("checkpoint_retention", extra={"extra": {"kept": int(self.checkpoint_keep), "removed": int(removed), "ext": ext}})
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
                    break
        finally:
            self.utd.close()

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
    p.set_defaults(sparse_mode=False)
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
    return p
