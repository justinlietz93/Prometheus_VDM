"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import os
import sys
import time
import threading
import subprocess
from typing import Any, Dict, List, Tuple


class ProcessManager:
    """
    Extracted from the dashboard without behavior changes.
    Launches python -m fum_rt.run_nexus with a profile, manages stdin feeding, and exposes launcher log.
    """

    def __init__(self, runs_root: str):
        # Persist UI-configured runs root and normalize to absolute path
        self.runs_root = runs_root
        self.runs_root_abs = os.path.abspath(runs_root)
        # Ensure runs_root exists and store repo root for module resolution
        try:
            os.makedirs(self.runs_root_abs, exist_ok=True)
        except Exception:
            pass
        # Resolve repository root (directory that contains the 'fum_rt' package)
        # so 'python -m fum_rt.run_nexus' works even when runs_root is outside repo.
        # services -> frontend -> fum_rt -> REPO_ROOT
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        # Launch logging (so you can inspect startup failures)
        self.launch_log = os.path.join(self.runs_root_abs, "launcher_last.log")
        self._logf = None
        self.last_cmd: List[str] | None = None

        self.proc: subprocess.Popen | None = None
        self.proc_lock = threading.Lock()
        self.current_run_dir: str | None = None
        self._stdin_lock = threading.Lock()
        self._feed_thread: threading.Thread | None = None
        self._feed_stop = threading.Event()
        # Instrumentation for run-dir detection
        self.last_detect_ms: float = 0.0
        self.last_detect_method: str = "init"
        self.last_cwd: str | None = None

    def set_runs_root(self, root: str):
        """Update runs root to match UI selection and rotate launch log path."""
        try:
            self.runs_root = root
            self.runs_root_abs = os.path.abspath(root)
            os.makedirs(self.runs_root_abs, exist_ok=True)
        except Exception:
            pass
        try:
            self.launch_log = os.path.join(self.runs_root_abs, "launcher_last.log")
        except Exception:
            pass

    def _build_cmd(self, profile: Dict[str, Any]) -> List[str]:
        py = sys.executable or "python"
        cmd = [py, "-m", "fum_rt.run_nexus"]

        def add(flag: str, val: Any, cast=str):
            if val is None:
                return
            cmd.extend([flag, cast(val)])

        # basic
        add("--neurons", profile.get("neurons"), str)
        add("--k", profile.get("k"), str)
        add("--hz", profile.get("hz"), str)
        add("--domain", profile.get("domain"), str)
        if profile.get("use_time_dynamics", True):
            cmd.append("--use-time-dynamics")
        else:
            cmd.append("--no-time-dynamics")
        # sparse / structure
        if profile.get("sparse_mode", False):
            cmd.append("--sparse-mode")
        add("--threshold", profile.get("threshold"), str)
        add("--lambda-omega", profile.get("lambda_omega"), str)
        add("--candidates", profile.get("candidates"), str)
        add("--walkers", profile.get("walkers"), str)
        add("--hops", profile.get("hops"), str)
        add("--status-interval", profile.get("status_interval"), str)
        add("--bundle-size", profile.get("bundle_size"), str)
        add("--prune-factor", profile.get("prune_factor"), str)
        # stim
        add("--stim-group-size", profile.get("stim_group_size"), str)
        add("--stim-amp", profile.get("stim_amp"), str)
        add("--stim-decay", profile.get("stim_decay"), str)
        add("--stim-max-symbols", profile.get("stim_max_symbols"), str)
        # speak
        if profile.get("speak_auto", True):
            cmd.append("--speak-auto")
        else:
            cmd.append("--no-speak-auto")
        add("--speak-z", profile.get("speak_z"), str)
        add("--speak-hysteresis", profile.get("speak_hysteresis"), str)
        add("--speak-cooldown-ticks", profile.get("speak_cooldown_ticks"), str)
        add("--speak-valence-thresh", profile.get("speak_valence_thresh"), str)
        add("--b1-half-life-ticks", profile.get("b1_half_life_ticks"), str)
        # viz/log
        add("--viz-every", profile.get("viz_every"), str)
        add("--log-every", profile.get("log_every"), str)
        # checkpoints
        add("--checkpoint-every", profile.get("checkpoint_every"), str)
        add("--checkpoint-keep", profile.get("checkpoint_keep"), str)
        add("--duration", profile.get("duration"), str)
        # explicit run dir (resume)
        add("--run-dir", profile.get("run_dir"), str)
        # optional: load existing engram (folder or file path; runtime normalizes)
        if profile.get("load_engram"):
            cmd.extend(["--load-engram", str(profile["load_engram"])])
        return cmd

    def start(self, profile: Dict[str, Any]) -> Tuple[bool, str]:
        with self.proc_lock:
            if self.proc and self.proc.poll() is None:
                return False, "Already running"

            # Normalize runs root and ensure it exists
            rr = getattr(self, "runs_root_abs", None) or os.path.abspath(self.runs_root)
            try:
                os.makedirs(rr, exist_ok=True)
            except Exception:
                pass
            before = set(os.listdir(rr)) if os.path.exists(rr) else set()
            detection_t0 = time.time()

            # Ensure explicit run_dir honors UI-selected runs_root on fresh starts.
            # If the profile does not specify run_dir (i.e., Start New Run without adoption),
            # synthesize runs_root/<timestamp> to avoid defaulting to 'runs/<ts>' regardless of UI choice.
            if not profile.get("run_dir"):
                try:
                    ts = time.strftime('%Y%m%d_%H%M%S')
                    profile["run_dir"] = os.path.join(rr, ts)
                except Exception:
                    pass

            cmd = self._build_cmd(profile)
            self.last_cmd = cmd[:]

            # Prepare environment so 'python -m fum_rt.run_nexus' resolves even if GUI was launched elsewhere
            env = os.environ.copy()
            try:
                repo_root = self.repo_root
            except Exception:
                repo_root = os.path.dirname(os.path.abspath(__file__))
            env["PYTHONPATH"] = f"{repo_root}:{env.get('PYTHONPATH','')}"
            env.setdefault("PYTHONUNBUFFERED", "1")

            # open launch log so we can surface failures
            try:
                if self._logf:
                    try:
                        self._logf.close()
                    except Exception:
                        pass
                self._logf = open(self.launch_log, "wb")
            except Exception:
                self._logf = None

            # Run from parent dir of runs_root so runtime writes to rr = <parent>/runs
            cwd_dir = os.path.dirname(rr)
            try:
                self.proc = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=self._logf or subprocess.DEVNULL,
                    stderr=self._logf or subprocess.DEVNULL,
                    cwd=cwd_dir,
                    env=env
                )
            except Exception as e:
                self.proc = None
                return False, f"Failed to start: {e}"

            # If the process died immediately, surface the log
            time.sleep(0.5)
            if self.proc and self.proc.poll() is not None:
                try:
                    if self._logf:
                        self._logf.flush()
                        self._logf.close()
                        self._logf = None
                    with open(self.launch_log, "rb") as fh:
                        tail = fh.read()[-4096:]
                    return False, f"Process exited during start.\nCommand: {' '.join(cmd)}\nLog({self.launch_log}):\n{tail.decode('utf-8','ignore')}"
                except Exception:
                    return False, f"Process exited during start.\nCommand: {' '.join(cmd)}\nNo launch log available."

            # Resolve run dir with instrumentation
            run_dir = None
            detect_method = None
            specified = profile.get("run_dir")
            if specified:
                run_dir = str(specified)
                detect_method = "explicit"
            else:
                # Detect new run dir (robust loop)
                for _ in range(20):  # ~5s total
                    try:
                        after = set(os.listdir(rr)) if os.path.exists(rr) else set()
                        new_dirs = list(after - before)
                        if new_dirs:
                            run_dir = max(
                                (os.path.join(rr, d) for d in new_dirs),
                                key=lambda p: os.path.getmtime(p)
                            )
                            detect_method = "create_watch"
                            break
                    except Exception:
                        pass
                    time.sleep(0.25)

                if not run_dir:
                    # fallback: latest by mtime under runs_root
                    runs = sorted(
                        [os.path.join(rr, d) for d in os.listdir(rr) if os.path.isdir(os.path.join(rr, d))],
                        key=lambda p: os.path.getmtime(p),
                        reverse=True
                    ) if os.path.exists(rr) else []
                    run_dir = runs[0] if runs else None
                    detect_method = "fallback_latest" if run_dir else "none"

            # Record detection diagnostics and surface to launcher log
            try:
                self.last_detect_ms = float((time.time() - detection_t0) * 1000.0)
            except Exception:
                self.last_detect_ms = 0.0
            self.last_detect_method = detect_method or "unknown"
            try:
                self.last_cwd = cwd_dir
            except Exception:
                self.last_cwd = None
            try:
                if self._logf:
                    line = f"[UI] run_dir_detected method={self.last_detect_method} ms={int(self.last_detect_ms)} rd={run_dir or ''} rr={rr} cwd={cwd_dir}\n"
                    self._logf.write(line.encode("utf-8", "ignore"))
                    self._logf.flush()
            except Exception:
                pass

            self.current_run_dir = run_dir
            return True, run_dir or ""

    def stop(self) -> Tuple[bool, str]:
        with self.proc_lock:
            if not self.proc:
                return False, "Not running"
            try:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
            except Exception as e:
                return False, f"Stop error: {e}"
            finally:
                self.proc = None
                self.current_run_dir = None
                try:
                    if self._logf:
                        self._logf.close()
                        self._logf = None
                except Exception:
                    pass
            return True, "Stopped"

    def send_line(self, text: str) -> bool:
        with self.proc_lock:
            if not self.proc or self.proc.stdin is None:
                return False
            try:
                with self._stdin_lock:
                    self.proc.stdin.write((text.rstrip("\n") + "\n").encode("utf-8"))
                    self.proc.stdin.flush()
                return True
            except Exception:
                return False

    def feed_file(self, path: str, rate_lps: float = 20.0):
        if not os.path.exists(path):
            return False
        if not self.proc or self.proc.stdin is None:
            return False
        if self._feed_thread and self._feed_thread.is_alive():
            return False
        self._feed_stop.clear()

        def _runner():
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    for line in fh:
                        if self._feed_stop.is_set():
                            break
                        ok = self.send_line(line)
                        if not ok:
                            break
                        time.sleep(1.0 / max(1e-3, rate_lps))
            except Exception:
                pass

        self._feed_thread = threading.Thread(target=_runner, daemon=True)
        self._feed_thread.start()
        return True

    def stop_feed(self):
        self._feed_stop.set()