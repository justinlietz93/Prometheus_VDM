#!/usr/bin/env python3
"""
FUM Live Dashboard (external, void-faithful)
- Tails a run's events.jsonl and utd_events.jsonl
- Live charts (sparsity, avg W, cohesion, complexity, B1 z, valence)
- Real-time control via runs/<ts>/phase.json (phase + speak + traversal/homeostasis)
- Start/Stop FUM runs with JSON profiles (no changes to fum_rt internals)

Usage:
  pip install dash plotly
  python fum_live_dashboard.py --runs-root runs

This app spawns 'python -m fum_rt.run_nexus ...' with the given profile.
It writes runs/<ts>/phase.json so Nexus applies gates live.
"""
import argparse
import json
import os
import sys
import time
import threading
import subprocess
from typing import Any, Dict, List, Tuple

import plotly.graph_objs as go
import dash
from dash import Dash, dcc, html, Input, Output, State, no_update

# ---------------- CLI ----------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--runs-root", default="runs")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8050)
    p.add_argument("--debug", action="store_true")
    return p.parse_args()

# -------------- FS utils -------------
def list_runs(root: str) -> List[str]:
    if not os.path.exists(root):
        return []
    items = []
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            try:
                mt = os.path.getmtime(path)
            except Exception:
                mt = 0.0
            items.append((mt, path))
    items.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in items]

def read_json_file(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def write_json_file(path: str, data: Any) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        return True
    except Exception:
        return False

# ------- Tailing JSONL with offsets -------
def _parse_jsonl_line(line: str) -> Any:
    try:
        return json.loads(line)
    except Exception:
        return None

def tail_jsonl_bytes(path: str, last_size: int) -> Tuple[List[Any], int]:
    if not os.path.exists(path):
        return [], 0
    try:
        size = os.path.getsize(path)
    except Exception:
        return [], last_size
    start = last_size if 0 <= last_size <= size else 0
    if size == start:
        return [], size
    try:
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(size - start)
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return [], size
    recs = []
    buf = []
    for ch in text:
        if ch == "\n":
            s = "".join(buf).strip()
            if s:
                obj = _parse_jsonl_line(s)
                if obj is not None:
                    recs.append(obj)
            buf = []
        else:
            buf.append(ch)
    return recs, size

# --------- Streaming z-score offline -------
import math
class StreamingZEMA:
    def __init__(self, half_life_ticks: int = 120):
        self.alpha = 1.0 - math.exp(math.log(0.5) / float(max(1, int(half_life_ticks))))
        self.mu = 0.0
        self.var = 1e-6
        self.prev = None
    def update(self, v: float) -> float:
        v = float(v)
        if self.prev is None:
            self.prev = v
            return 0.0
        d = v - self.prev
        self.prev = v
        a = self.alpha
        self.mu = (1.0 - a) * self.mu + a * d
        diff = d - self.mu
        self.var = (1.0 - a) * self.var + a * (diff * diff)
        sigma = (self.var if self.var > 1e-24 else 1e-24) ** 0.5
        return float(diff / sigma)

# --------- Process manager (start/stop) -----
class ProcessManager:
    def __init__(self, runs_root: str):
        self.runs_root = runs_root
        # Ensure runs_root exists and store repo root for module resolution
        try:
            os.makedirs(self.runs_root, exist_ok=True)
        except Exception:
            pass
        self.repo_root = os.path.dirname(os.path.abspath(__file__))
        # Launch logging (so you can inspect startup failures)
        self.launch_log = os.path.join(self.runs_root, "launcher_last.log")
        self._logf = None
        self.last_cmd: list[str] | None = None

        self.proc: subprocess.Popen | None = None
        self.proc_lock = threading.Lock()
        self.current_run_dir: str | None = None
        self._stdin_lock = threading.Lock()
        self._feed_thread: threading.Thread | None = None
        self._feed_stop = threading.Event()

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
        # optional: load existing engram
        if profile.get("load_engram"):
            cmd.extend(["--load-engram", str(profile["load_engram"])])
        return cmd

    def start(self, profile: Dict[str, Any]) -> Tuple[bool, str]:
        with self.proc_lock:
            if self.proc and self.proc.poll() is None:
                return False, "Already running"
            # Ensure runs_root exists before diffing
            try:
                os.makedirs(self.runs_root, exist_ok=True)
            except Exception:
                pass
            before = set(os.listdir(self.runs_root)) if os.path.exists(self.runs_root) else set()
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
            try:
                self.proc = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=self._logf or subprocess.DEVNULL,
                    stderr=self._logf or subprocess.DEVNULL,
                    cwd=repo_root,   # run from repo root so fum_rt is importable
                    env=env
                )
            except Exception as e:
                self.proc = None
                return False, f"Failed to start: {e}"
            # detect new run dir
            time.sleep(1.5)
            after = set(os.listdir(self.runs_root)) if os.path.exists(self.runs_root) else set()
            new_dirs = list(after - before)
            run_dir = None
            if new_dirs:
                # pick the newest by mtime
                run_dir = max(
                    (os.path.join(self.runs_root, d) for d in new_dirs),
                    key=lambda p: os.path.getmtime(p)
                )
            else:
                # fallback: latest by mtime under runs_root
                runs = list_runs(self.runs_root)
                run_dir = runs[0] if runs else None
            # if the process died immediately, surface the log
            if self.proc and self.proc.poll() is not None:
                # process exited early; read log and return error
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

# ------------- Live series state -------------
class SeriesState:
    def __init__(self, run_dir: str):
        self.run_dir = run_dir
        self.events_path = os.path.join(run_dir, "events.jsonl")
        self.utd_path = os.path.join(run_dir, "utd_events.jsonl")
        self.events_size = 0
        self.utd_size = 0
        self.b1_ema = StreamingZEMA(half_life_ticks=120)
        self.t: List[int] = []
        self.active = []
        self.avgw = []
        self.coh = []
        self.comp = []
        self.b1z = []
        self.val = []
        self.val2 = []
        self.entro = []
        self.speak_ticks: List[int] = []

def extract_tick(rec: Dict[str, Any]) -> int | None:
    for k in ("t", "tick"):
        if k in rec:
            try:
                return int(rec[k])
            except Exception:
                pass
    ex = rec.get("extra", {})
    for k in ("t", "tick"):
        if k in ex:
            try:
                return int(ex[k])
            except Exception:
                pass
    return None

def append_event(ss: SeriesState, rec: Dict[str, Any]):
    t = extract_tick(rec)
    if t is None:
        return
    ex = rec.get("extra", rec)
    ss.t.append(int(t))
    ss.active.append(ex.get("active_synapses"))
    ss.avgw.append(ex.get("avg_weight"))
    ss.coh.append(ex.get("cohesion_components"))
    cc = ex.get("complexity_cycles")
    ss.comp.append(cc)
    bz = ex.get("b1_z")
    if bz is None:
        v = 0.0 if cc is None else float(cc)
        bz = ss.b1_ema.update(v)
    ss.b1z.append(float(bz))
    # Robust SIE valence extraction with fallbacks (handles various field names and ranges)
    val = ex.get("sie_valence_01")
    if val is None:
        for k in ("sie_valence", "valence"):
            v = ex.get(k)
            if v is not None:
                try:
                    fv = float(v)
                    # Normalize [-1,1] -> [0,1] if appropriate
                    val = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                except Exception:
                    val = v
                break
        if val is None:
            sie = ex.get("sie") or {}
            if isinstance(sie, dict):
                if "valence_01" in sie:
                    val = sie.get("valence_01")
                elif "valence" in sie:
                    try:
                        fv = float(sie.get("valence"))
                        val = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                    except Exception:
                        val = sie.get("valence")
    ss.val.append(val)
    val2 = ex.get("sie_v2_valence_01")
    if val2 is None:
        for k in ("sie_v2_valence", "sie_v2"):
            v = ex.get(k)
            if v is not None:
                try:
                    fv = float(v)
                    val2 = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                except Exception:
                    val2 = v
                break
        if val2 is None:
            sie2 = ex.get("sie_v2") or {}
            if isinstance(sie2, dict):
                if "valence_01" in sie2:
                    val2 = sie2.get("valence_01")
                elif "valence" in sie2:
                    try:
                        fv = float(sie2.get("valence"))
                        val2 = (fv + 1.0) / 2.0 if -1.001 <= fv <= 1.001 else fv
                    except Exception:
                        val2 = sie2.get("valence")
    ss.val2.append(val2)
    ss.entro.append(ex.get("connectome_entropy"))

def append_say(ss: SeriesState, rec: Dict[str, Any]):
    name = (rec.get("macro") or rec.get("name") or rec.get("kind") or "").lower()
    if name != "say":
        return
    t = rec.get("t") or rec.get("tick") or rec.get("meta", {}).get("t") or rec.get("meta", {}).get("tick")
    if t is None:
        return
    try:
        ss.speak_ticks.append(int(t))
    except Exception:
        pass

def ffill(arr: List[Any]) -> List[float | None]:
    out = []
    last = None
    for x in arr:
        if x is None:
            out.append(last)
        else:
            try:
                v = float(x)
            except Exception:
                v = last
            out.append(v)
            last = v
    return out

# ------------- Build Dash app ---------------
def build_app(runs_root: str) -> Dash:
    app = Dash(__name__)
    app.title = "FUM Live Dashboard"

    runs = list_runs(runs_root)
    default_run = runs[0] if runs else ""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    PROFILES_DIR = os.path.join(repo_root, "run_profiles")
    os.makedirs(PROFILES_DIR, exist_ok=True)
    manager = ProcessManager(runs_root)

    default_profile = {
        "neurons": 1000, "k": 12, "hz": 10, "domain": "math_physics",
        "use_time_dynamics": True,
        "sparse_mode": False, "threshold": 0.15, "lambda_omega": 0.10, "candidates": 64,
        "walkers": 256, "hops": 3, "bundle_size": 3, "prune_factor": 0.10, "status_interval": 1,
        "viz_every": 0, "log_every": 1,
        "speak_auto": True, "speak_z": 3.0, "speak_hysteresis": 0.5, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.55,
        "b1_half_life_ticks": 50,
        "stim_group_size": 8, "stim_amp": 0.08, "stim_decay": 0.92, "stim_max_symbols": 128,
        "checkpoint_every": 60, "checkpoint_keep": 5, "duration": None
    }

    def list_profiles() -> List[str]:
        return sorted([os.path.join(PROFILES_DIR, f) for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])

    def _bool_from_checklist(val) -> bool:
        if isinstance(val, list):
            return 'on' in val
        return bool(val)

    def _checklist_from_bool(b: bool):
        return ['on'] if bool(b) else []

    def _safe_int(x, default=None):
        try:
            return int(x)
        except Exception:
            return default

    def _safe_float(x, default=None):
        try:
            return float(x)
        except Exception:
            return default

    domain_options = [
        {"label": n, "value": n}
        for n in ["math_physics", "quantum", "standard_model", "dark_matter", "biology_consciousness", "cosmogenesis", "higgs"]
    ]

    app.layout = html.Div([
        html.H3("FUM Live Dashboard (external control)"),
        html.Div([
            html.Div([
                html.Label("Runs root"),
                dcc.Input(id="runs-root", type="text", value=runs_root, style={"width":"100%"}),
                html.Button("Refresh Runs", id="refresh-runs", n_clicks=0, style={"marginTop":"6px"}),
                html.Label("Run directory"),
                dcc.Dropdown(id="run-dir", options=[{"label": p, "value": p} for p in runs], value=default_run),
                html.Div([
                    html.Button("Use Current Run", id="use-current-run", n_clicks=0),
                    html.Button("Use Latest Run", id="use-latest-run", n_clicks=0, style={"marginLeft":"8px"})
                ], style={"marginTop":"6px"}),
                html.Hr(),
                html.Label("Runtime Controls (phase + gates)"),
                dcc.Slider(id="phase", min=0, max=4, step=1, value=0, marks={i:str(i) for i in range(5)}),
                html.Div([
                    html.Div([
                        html.Label("Speak z"),
                        dcc.Input(id="rc-speak-z", type="number", value=default_profile["speak_z"], step=0.1, min=0)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Hysteresis"),
                        dcc.Input(id="rc-speak-hysteresis", type="number", value=default_profile["speak_hysteresis"], step=0.1, min=0)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Cooldown (ticks)"),
                        dcc.Input(id="rc-speak-cooldown", type="number", value=default_profile["speak_cooldown_ticks"], step=1, min=1)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Valence thresh"),
                        dcc.Input(id="rc-speak-valence", type="number", value=default_profile["speak_valence_thresh"], step=0.01, min=0, max=1)
                    ], style={"flex":"1"})
                ], style={"display":"flex","gap":"6px","marginTop":"6px"}),
                html.Div([
                    html.Div([
                        html.Label("Walkers"),
                        dcc.Input(id="rc-walkers", type="number", value=default_profile["walkers"], step=1, min=1)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Hops"),
                        dcc.Input(id="rc-hops", type="number", value=default_profile["hops"], step=1, min=1)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Bundle size"),
                        dcc.Input(id="rc-bundle-size", type="number", value=default_profile["bundle_size"], step=1, min=1)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Prune factor"),
                        dcc.Input(id="rc-prune-factor", type="number", value=default_profile["prune_factor"], step=0.01, min=0, max=1)
                    ], style={"flex":"1"})
                ], style={"display":"flex","gap":"6px","marginTop":"6px"}),
                html.Div([
                    html.Div([
                        html.Label("Threshold"),
                        dcc.Input(id="rc-threshold", type="number", value=default_profile.get("threshold", 0.15), step=0.01, min=0)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Lambda omega"),
                        dcc.Input(id="rc-lambda-omega", type="number", value=default_profile.get("lambda_omega", 0.10), step=0.01, min=0)
                    ], style={"flex":"1","paddingRight":"6px"}),
                    html.Div([
                        html.Label("Candidates"),
                        dcc.Input(id="rc-candidates", type="number", value=default_profile.get("candidates", 64), step=1, min=1)
                    ], style={"flex":"1"})
                ], style={"display":"flex","gap":"6px","marginTop":"6px"}),
                html.Button("Apply Runtime Settings", id="apply-phase", n_clicks=0, style={"marginTop":"6px"}),
                html.Pre(id="phase-status", style={"fontSize":"12px"}),
                html.Label("Load Engram (runtime)", style={"display":"none"}),
                dcc.Input(id="rc-load-engram-path", type="text", placeholder="runs/<ts>/state_XXXXX.h5 or .npz", style={"width":"100%", "display":"none"}),
                html.Button("Load Engram Now", id="rc-load-engram-btn", n_clicks=0, style={"marginTop":"6px","display":"none"}),
                html.Hr(),
                html.Label("Feed file to stdin (optional)"),
                dcc.Input(id="feed-path", type="text", placeholder="relative to fum_rt/data or absolute path", style={"width":"100%"}),
                dcc.Input(id="feed-rate", type="number", value=20, step=1, style={"width":"120px", "marginTop":"6px"}),
                html.Div([
                    html.Button("Start Feed", id="feed-start", n_clicks=0),
                    html.Button("Stop Feed", id="feed-stop", n_clicks=0, style={"marginLeft":"8px"}),
                ], style={"marginTop":"6px"}),
                html.Hr(),
                html.Pre(id="send-status", style={"fontSize":"12px"}),
            ], style={"flex":"0 0 360px", "minWidth":"320px", "maxWidth":"420px", "paddingRight":"10px", "borderRight":"1px solid #ccc"}),
            html.Div([
                html.H4("Run configuration and process control"),
                html.Div([
                    # Core
                    html.Div([
                        html.Div([
                            html.Label("Neurons"),
                            dcc.Input(id="cfg-neurons", type="number", value=default_profile["neurons"], step=1, min=1),
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("k"),
                            dcc.Input(id="cfg-k", type="number", value=default_profile["k"], step=1, min=1),
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Hz"),
                            dcc.Input(id="cfg-hz", type="number", value=default_profile["hz"], step=1, min=1),
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Domain"),
                            dcc.Dropdown(id="cfg-domain", options=domain_options, value=default_profile["domain"]),
                        ], style={"flex":"2"})
                    ], style={"display":"flex","gap":"6px"}),

                    html.Div([
                        html.Div([
                            html.Label("Use time dynamics"),
                            dcc.Checklist(id="cfg-use-time-dynamics", options=[{"label":" On","value":"on"}],
                                          value=['on'] if default_profile["use_time_dynamics"] else [])
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Sparse mode"),
                            dcc.Checklist(id="cfg-sparse-mode", options=[{"label":" On","value":"on"}],
                                          value=['on'] if default_profile["sparse_mode"] else [])
                        ], style={"flex":"1"}),
                    ], style={"display":"flex","gap":"6px","marginTop":"4px"}),

                    html.Hr(),
                    html.Label("Structure and traversal"),
                    html.Div([
                        html.Div([
                            html.Label("Threshold"),
                            dcc.Input(id="cfg-threshold", type="number", value=default_profile["threshold"], step=0.01, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Lambda omega"),
                            dcc.Input(id="cfg-lambda-omega", type="number", value=default_profile["lambda_omega"], step=0.01, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Candidates"),
                            dcc.Input(id="cfg-candidates", type="number", value=default_profile["candidates"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Walkers"),
                            dcc.Input(id="cfg-walkers", type="number", value=default_profile["walkers"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Hops"),
                            dcc.Input(id="cfg-hops", type="number", value=default_profile["hops"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Bundle size"),
                            dcc.Input(id="cfg-bundle-size", type="number", value=default_profile["bundle_size"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Prune factor"),
                            dcc.Input(id="cfg-prune-factor", type="number", value=default_profile["prune_factor"], step=0.01, min=0, max=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Status interval"),
                            dcc.Input(id="cfg-status-interval", type="number", value=default_profile["status_interval"], step=1, min=1)
                        ], style={"flex":"1"}),
                    ], style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"6px"}),

                    html.Hr(),
                    html.Label("Stimulus"),
                    html.Div([
                        html.Div([
                            html.Label("Group size"),
                            dcc.Input(id="cfg-stim-group-size", type="number", value=default_profile["stim_group_size"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Amp"),
                            dcc.Input(id="cfg-stim-amp", type="number", value=default_profile["stim_amp"], step=0.01, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Decay"),
                            dcc.Input(id="cfg-stim-decay", type="number", value=default_profile["stim_decay"], step=0.01, min=0, max=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Max symbols"),
                            dcc.Input(id="cfg-stim-max-symbols", type="number", value=default_profile["stim_max_symbols"], step=1, min=1)
                        ], style={"flex":"1"}),
                    ], style={"display":"flex","gap":"6px"}),

                    html.Hr(),
                    html.Label("Speak / B1 spike detector"),
                    html.Div([
                        html.Div([
                            html.Label("Speak auto"),
                            dcc.Checklist(id="cfg-speak-auto", options=[{"label":" On","value":"on"}],
                                          value=['on'] if default_profile["speak_auto"] else [])
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Speak z"),
                            dcc.Input(id="cfg-speak-z", type="number", value=default_profile["speak_z"], step=0.1, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Hysteresis"),
                            dcc.Input(id="cfg-speak-hysteresis", type="number", value=default_profile["speak_hysteresis"], step=0.1, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Cooldown (ticks)"),
                            dcc.Input(id="cfg-speak-cooldown-ticks", type="number", value=default_profile["speak_cooldown_ticks"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("Valence thresh"),
                            dcc.Input(id="cfg-speak-valence-thresh", type="number", value=default_profile["speak_valence_thresh"], step=0.01, min=0, max=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("B1 half-life (ticks)"),
                            dcc.Input(id="cfg-b1-half-life-ticks", type="number", value=default_profile["b1_half_life_ticks"], step=1, min=1)
                        ], style={"flex":"1"}),
                    ], style={"display":"grid","gridTemplateColumns":"repeat(6,1fr)","gap":"6px"}),

                    html.Hr(),
                    html.Label("Viz / Logs / Checkpoints"),
                    html.Div([
                        html.Div([
                            html.Label("viz_every"),
                            dcc.Input(id="cfg-viz-every", type="number", value=default_profile["viz_every"], step=1, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("log_every"),
                            dcc.Input(id="cfg-log-every", type="number", value=default_profile["log_every"], step=1, min=1)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("checkpoint_every"),
                            dcc.Input(id="cfg-checkpoint-every", type="number", value=default_profile["checkpoint_every"], step=1, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("checkpoint_keep"),
                            dcc.Input(id="cfg-checkpoint-keep", type="number", value=default_profile["checkpoint_keep"], step=1, min=0)
                        ], style={"flex":"1","paddingRight":"6px"}),
                        html.Div([
                            html.Label("duration (s)"),
                            dcc.Input(id="cfg-duration", type="number", value=default_profile["duration"], step=1, min=0)
                        ], style={"flex":"1"}),
                    ], style={"display":"flex","gap":"6px"}),

                    html.Div([
                        html.Label("Load engram path (optional)"),
                        dcc.Input(id="cfg-load-engram", type="text", value="", style={"width":"100%"}),
                    ], style={"marginTop":"6px","display":"none"}),

                    html.Div([
                        dcc.Input(id="profile-name", type="text", placeholder="profile name", style={"width":"200px"}),
                        html.Button("Save Profile", id="save-profile", n_clicks=0, style={"marginLeft":"6px"}),
                        dcc.Dropdown(id="profile-path", options=[{"label": p, "value": p} for p in list_profiles()], placeholder="load profile", style={"width":"60%","marginLeft":"8px"}),
                        html.Button("Load", id="load-profile", n_clicks=0, style={"marginLeft":"6px"}),
                    ], style={"display":"flex","alignItems":"center","marginTop":"6px"}),
                    html.Pre(id="profile-save-status", style={"fontSize":"12px","whiteSpace":"pre-wrap","marginTop":"6px"}),

                    html.Div([
                        html.Button("Start Run", id="start-run", n_clicks=0, style={"backgroundColor":"#28a745","color":"white"}),
                        html.Button("Stop Run", id="stop-run", n_clicks=0, style={"marginLeft":"8px","backgroundColor":"#dc3545","color":"white"}),
                    ], style={"marginTop":"8px"}),
                    html.Pre(id="proc-status", style={"fontSize":"12px","whiteSpace":"pre-wrap"}),
                    html.Button("Show Launcher Log", id="show-log", n_clicks=0, style={"marginTop":"6px"}),
                    html.Pre(id="launch-log", style={"fontSize":"12px","whiteSpace":"pre-wrap","maxHeight":"240px","overflowY":"auto"}),
                ]),
                dcc.Graph(id="fig-dashboard", style={"height":"420px"}),
                dcc.Graph(id="fig-discovery", style={"height":"320px"}),
                html.H4("Chat"),
                html.Pre(
                    id="chat-view",
                    style={
                        "height":"220px","overflowY":"auto","backgroundColor":"#111",
                        "color":"#eee","padding":"8px","whiteSpace":"pre-wrap","border":"1px solid #333"
                    }
                ),
                html.Div([
                    html.Label("Chat filter"),
                    dcc.RadioItems(
                        id="chat-filter",
                        options=[
                            {"label": "All (user + model)", "value": "all"},
                            {"label": "Model only", "value": "model"},
                            {"label": "Model (spike‑gated only)", "value": "spike"}
                        ],
                        value="all",
                        labelStyle={"display":"inline-block","marginRight":"10px"}
                    ),
                ], style={"marginTop":"6px"}),
                html.Div([
                    dcc.Input(
                        id="chat-input",
                        type="text",
                        placeholder="Type a message and click Send",
                        style={"width":"80%"}
                    ),
                    html.Button("Send", id="chat-send", n_clicks=0, style={"marginLeft":"8px"}),
                ], style={"marginTop":"6px"}),
                html.Pre(id="chat-status", style={"fontSize":"12px"}),
            ], style={"flex":"1","paddingLeft":"10px"}),
        ], style={"display":"flex","flexWrap":"wrap"}),
        dcc.Interval(id="poll", interval=1500, n_intervals=0),
        dcc.Store(id="chat-state"),
        dcc.Store(id="ui-state")
    ], style={"padding":"10px"})

    # ---------- Callbacks ----------
    @app.callback(
        Output("run-dir","options"),
        Output("run-dir","value", allow_duplicate=True),
        Input("refresh-runs","n_clicks"),
        State("runs-root","value"),
        prevent_initial_call=True
    )
    def on_refresh_runs(_n, root):
        root = root or runs_root
        opts = [{"label": p, "value": p} for p in list_runs(root)]
        val = opts[0]["value"] if opts else ""
        return opts, val

    @app.callback(
        Output("phase-status","children"),
        Input("apply-phase","n_clicks"),
        State("run-dir","value"),
        State("phase","value"),
        State("rc-speak-z","value"),
        State("rc-speak-hysteresis","value"),
        State("rc-speak-cooldown","value"),
        State("rc-speak-valence","value"),
        State("rc-walkers","value"),
        State("rc-hops","value"),
        State("rc-bundle-size","value"),
        State("rc-prune-factor","value"),
        State("rc-threshold","value"),
        State("rc-lambda-omega","value"),
        State("rc-candidates","value"),
        prevent_initial_call=True
    )
    def on_apply_phase(_n, run_dir, phase,
                       s_z, s_h, s_cd, s_vt,
                       c_w, c_h, c_b, c_pf, c_thr, c_lw, c_cand):
        if not run_dir:
            return "Select a run directory."
        # Helpers for safe casting with defaults
        def _sint(x, dv):
            try: return int(x)
            except Exception: return dv
        def _sfloat(x, dv):
            try: return float(x)
            except Exception: return dv
        prof = {
            "phase": int(_sint(phase, 0)),
            "speak": {
                "speak_z": float(_sfloat(s_z, default_profile["speak_z"])),
                "speak_hysteresis": float(_sfloat(s_h, default_profile["speak_hysteresis"])),
                "speak_cooldown_ticks": int(_sint(s_cd, default_profile["speak_cooldown_ticks"])),
                "speak_valence_thresh": float(_sfloat(s_vt, default_profile["speak_valence_thresh"])),
            },
            "connectome": {
                "walkers": int(_sint(c_w, default_profile["walkers"])),
                "hops": int(_sint(c_h, default_profile["hops"])),
                "bundle_size": int(_sint(c_b, default_profile["bundle_size"])),
                "prune_factor": float(_sfloat(c_pf, default_profile["prune_factor"])),
                "threshold": float(_sfloat(c_thr, default_profile.get("threshold", 0.15))),
                "lambda_omega": float(_sfloat(c_lw, default_profile.get("lambda_omega", 0.10))),
                "candidates": int(_sint(c_cand, default_profile.get("candidates", 64))),
            }
        }
        ok = write_json_file(os.path.join(run_dir,"phase.json"), prof)
        return "Applied" if ok else "Error writing phase.json"


    @app.callback(
        Output("phase-status","children", allow_duplicate=True),
        Input("rc-load-engram-btn","n_clicks"),
        State("run-dir","value"),
        State("rc-load-engram-path","value"),
        prevent_initial_call=True
    )
    def on_load_engram_now(_n, run_dir, path):
        rd = (run_dir or "").strip()
        if not rd:
            return "Select a run directory."
        p = (path or "").strip()
        if not p:
            return "Enter engram path."
        try:
            obj = read_json_file(os.path.join(rd, "phase.json")) or {}
            if not isinstance(obj, dict):
                obj = {}
            obj["load_engram"] = p
            ok = write_json_file(os.path.join(rd, "phase.json"), obj)
            return f"Queued load_engram: {p}" if ok else "Error writing phase.json"
        except Exception as e:
            return f"Error: {e}"

    @app.callback(
        Output("proc-status","children"),
        Output("run-dir","value", allow_duplicate=True),
        Input("start-run","n_clicks"),
        Input("stop-run","n_clicks"),
        State("runs-root","value"),
        # Profile States (validated UI)
        State("cfg-neurons","value"),
        State("cfg-k","value"),
        State("cfg-hz","value"),
        State("cfg-domain","value"),
        State("cfg-use-time-dynamics","value"),
        State("cfg-sparse-mode","value"),
        State("cfg-threshold","value"),
        State("cfg-lambda-omega","value"),
        State("cfg-candidates","value"),
        State("cfg-walkers","value"),
        State("cfg-hops","value"),
        State("cfg-status-interval","value"),
        State("cfg-bundle-size","value"),
        State("cfg-prune-factor","value"),
        State("cfg-stim-group-size","value"),
        State("cfg-stim-amp","value"),
        State("cfg-stim-decay","value"),
        State("cfg-stim-max-symbols","value"),
        State("cfg-speak-auto","value"),
        State("cfg-speak-z","value"),
        State("cfg-speak-hysteresis","value"),
        State("cfg-speak-cooldown-ticks","value"),
        State("cfg-speak-valence-thresh","value"),
        State("cfg-b1-half-life-ticks","value"),
        State("cfg-viz-every","value"),
        State("cfg-log-every","value"),
        State("cfg-checkpoint-every","value"),
        State("cfg-checkpoint-keep","value"),
        State("cfg-duration","value"),
        prevent_initial_call=True
    )
    def on_proc_actions(n_start, n_stop, root,
                        neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
                        walkers, hops, status_interval, bundle_size, prune_factor,
                        stim_group_size, stim_amp, stim_decay, stim_max_symbols,
                        speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
                        viz_every, log_every, checkpoint_every, checkpoint_keep, duration):
        # Determine which control triggered this callback
        try:
            trig = dash.callback_context.triggered[0]["prop_id"].split(".")[0] if dash.callback_context.triggered else None
        except Exception:
            trig = None

        if trig == "start-run":
            profile = {
                "neurons": int(_safe_int(neurons, default_profile["neurons"])),
                "k": int(_safe_int(k, default_profile["k"])),
                "hz": int(_safe_int(hz, default_profile["hz"])),
                "domain": str(domain or default_profile["domain"]),
                "use_time_dynamics": _bool_from_checklist(use_td) if use_td is not None else default_profile["use_time_dynamics"],
                "sparse_mode": _bool_from_checklist(sparse_mode) if sparse_mode is not None else default_profile["sparse_mode"],
                "threshold": float(_safe_float(threshold, default_profile["threshold"])),
                "lambda_omega": float(_safe_float(lambda_omega, default_profile["lambda_omega"])),
                "candidates": int(_safe_int(candidates, default_profile["candidates"])),
                "walkers": int(_safe_int(walkers, default_profile["walkers"])),
                "hops": int(_safe_int(hops, default_profile["hops"])),
                "status_interval": int(_safe_int(status_interval, default_profile["status_interval"])),
                "bundle_size": int(_safe_int(bundle_size, default_profile["bundle_size"])),
                "prune_factor": float(_safe_float(prune_factor, default_profile["prune_factor"])),
                "stim_group_size": int(_safe_int(stim_group_size, default_profile["stim_group_size"])),
                "stim_amp": float(_safe_float(stim_amp, default_profile["stim_amp"])),
                "stim_decay": float(_safe_float(stim_decay, default_profile["stim_decay"])),
                "stim_max_symbols": int(_safe_int(stim_max_symbols, default_profile["stim_max_symbols"])),
                "speak_auto": _bool_from_checklist(speak_auto) if speak_auto is not None else default_profile["speak_auto"],
                "speak_z": float(_safe_float(speak_z, default_profile["speak_z"])),
                "speak_hysteresis": float(_safe_float(speak_hyst, default_profile["speak_hysteresis"])),
                "speak_cooldown_ticks": int(_safe_int(speak_cd, default_profile["speak_cooldown_ticks"])),
                "speak_valence_thresh": float(_safe_float(speak_val, default_profile["speak_valence_thresh"])),
                "b1_half_life_ticks": int(_safe_int(b1_hl, default_profile["b1_half_life_ticks"])),
                "viz_every": int(_safe_int(viz_every, default_profile["viz_every"])),
                "log_every": int(_safe_int(log_every, default_profile["log_every"])),
                "checkpoint_every": int(_safe_int(checkpoint_every, default_profile["checkpoint_every"])),
                "checkpoint_keep": int(_safe_int(checkpoint_keep, default_profile["checkpoint_keep"])),
                "duration": None if duration in (None, "", "None") else int(_safe_int(duration, 0)),
            }
            ok, msg = manager.start(profile)
            if not ok:
                # msg contains error and possibly launch log; surface it
                return f"Start failed:\n{msg}", no_update
            run_dir = msg
            cmd_echo = " ".join(manager.last_cmd or [])
            return (f"Started.\nrun_dir={run_dir}\n"
                    f"checkpoint_every={profile.get('checkpoint_every')} keep={profile.get('checkpoint_keep')}\n"
                    f"cmd: {cmd_echo}\n"
                    f"launch_log: {manager.launch_log}"), run_dir or no_update

        if trig == "stop-run":
            ok, msg = manager.stop()
            return ("Stopped." if ok else msg), no_update

        # (send one line removed; use Chat input instead)

        return no_update, no_update



    @app.callback(
        Output("send-status","children", allow_duplicate=True),
        Input("feed-start","n_clicks"),
        State("feed-path","value"),
        State("feed-rate","value"),
        prevent_initial_call=True
    )
    def on_feed_start(_n, path, rate):
        # Resolve relative paths against fum_rt/data by default
        p = (path or "").strip()
        if not p:
            return "Provide a feed path (relative to fum_rt/data or absolute)."
        chosen = p
        try:
            if (not os.path.isabs(chosen)) or (not os.path.exists(chosen)):
                data_dir = os.path.join(repo_root, "fum_rt", "data")
                cand = os.path.join(data_dir, p)
                if os.path.exists(cand):
                    chosen = cand
        except Exception:
            pass
        ok = manager.feed_file(chosen, float(rate or 20.0))
        return (f"Feeding from {chosen}." if ok else "Feed failed (check process running and path).")

    @app.callback(
        Output("send-status","children", allow_duplicate=True),
        Input("feed-stop","n_clicks"),
        prevent_initial_call=True
    )
    def on_feed_stop(_n):
        manager.stop_feed()
        return "Feed stopped."

    @app.callback(
        Output("profile-path","options"),
        Output("profile-save-status","children"),
        Input("save-profile","n_clicks"),
        State("profile-name","value"),
        # All config fields as state for assembling the JSON
        State("cfg-neurons","value"),
        State("cfg-k","value"),
        State("cfg-hz","value"),
        State("cfg-domain","value"),
        State("cfg-use-time-dynamics","value"),
        State("cfg-sparse-mode","value"),
        State("cfg-threshold","value"),
        State("cfg-lambda-omega","value"),
        State("cfg-candidates","value"),
        State("cfg-walkers","value"),
        State("cfg-hops","value"),
        State("cfg-status-interval","value"),
        State("cfg-bundle-size","value"),
        State("cfg-prune-factor","value"),
        State("cfg-stim-group-size","value"),
        State("cfg-stim-amp","value"),
        State("cfg-stim-decay","value"),
        State("cfg-stim-max-symbols","value"),
        State("cfg-speak-auto","value"),
        State("cfg-speak-z","value"),
        State("cfg-speak-hysteresis","value"),
        State("cfg-speak-cooldown-ticks","value"),
        State("cfg-speak-valence-thresh","value"),
        State("cfg-b1-half-life-ticks","value"),
        State("cfg-viz-every","value"),
        State("cfg-log-every","value"),
        State("cfg-checkpoint-every","value"),
        State("cfg-checkpoint-keep","value"),
        State("cfg-duration","value"),
        prevent_initial_call=True
    )
    def on_save_profile(_n, name,
                        neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
                        walkers, hops, status_interval, bundle_size, prune_factor,
                        stim_group_size, stim_amp, stim_decay, stim_max_symbols,
                        speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
                        viz_every, log_every, checkpoint_every, checkpoint_keep, duration):
        name = (name or "").strip()
        if not name:
            return [{"label": p, "value": p} for p in list_profiles()], "Provide a profile name."
        # Assemble current form into JSON
        data = {
            "neurons": int(_safe_int(neurons, default_profile["neurons"])),
            "k": int(_safe_int(k, default_profile["k"])),
            "hz": int(_safe_int(hz, default_profile["hz"])),
            "domain": str(domain or default_profile["domain"]),
            "use_time_dynamics": _bool_from_checklist(use_td) if use_td is not None else default_profile["use_time_dynamics"],
            "sparse_mode": _bool_from_checklist(sparse_mode) if sparse_mode is not None else default_profile["sparse_mode"],
            "threshold": float(_safe_float(threshold, default_profile["threshold"])),
            "lambda_omega": float(_safe_float(lambda_omega, default_profile["lambda_omega"])),
            "candidates": int(_safe_int(candidates, default_profile["candidates"])),
            "walkers": int(_safe_int(walkers, default_profile["walkers"])),
            "hops": int(_safe_int(hops, default_profile["hops"])),
            "status_interval": int(_safe_int(status_interval, default_profile["status_interval"])),
            "bundle_size": int(_safe_int(bundle_size, default_profile["bundle_size"])),
            "prune_factor": float(_safe_float(prune_factor, default_profile["prune_factor"])),
            "stim_group_size": int(_safe_int(stim_group_size, default_profile["stim_group_size"])),
            "stim_amp": float(_safe_float(stim_amp, default_profile["stim_amp"])),
            "stim_decay": float(_safe_float(stim_decay, default_profile["stim_decay"])),
            "stim_max_symbols": int(_safe_int(stim_max_symbols, default_profile["stim_max_symbols"])),
            "speak_auto": _bool_from_checklist(speak_auto) if speak_auto is not None else default_profile["speak_auto"],
            "speak_z": float(_safe_float(speak_z, default_profile["speak_z"])),
            "speak_hysteresis": float(_safe_float(speak_hyst, default_profile["speak_hysteresis"])),
            "speak_cooldown_ticks": int(_safe_int(speak_cd, default_profile["speak_cooldown_ticks"])),
            "speak_valence_thresh": float(_safe_float(speak_val, default_profile["speak_valence_thresh"])),
            "b1_half_life_ticks": int(_safe_int(b1_hl, default_profile["b1_half_life_ticks"])),
            "viz_every": int(_safe_int(viz_every, default_profile["viz_every"])),
            "log_every": int(_safe_int(log_every, default_profile["log_every"])),
            "checkpoint_every": int(_safe_int(checkpoint_every, default_profile["checkpoint_every"])),
            "checkpoint_keep": int(_safe_int(checkpoint_keep, default_profile["checkpoint_keep"])),
            "duration": None if duration in (None, "", "None") else int(_safe_int(duration, 0)),
        }
        path = os.path.join(PROFILES_DIR, f"{name}.json")
        ok = write_json_file(path, data)
        status = f"Saved profile to {path}" if ok else f"Error writing {path}"
        return [{"label": p, "value": p} for p in list_profiles()], status

    # Multi-output load: populate all UI fields from a selected profile JSON
    @app.callback(
        Output("cfg-neurons","value"),
        Output("cfg-k","value"),
        Output("cfg-hz","value"),
        Output("cfg-domain","value"),
        Output("cfg-use-time-dynamics","value"),
        Output("cfg-sparse-mode","value"),
        Output("cfg-threshold","value"),
        Output("cfg-lambda-omega","value"),
        Output("cfg-candidates","value"),
        Output("cfg-walkers","value"),
        Output("cfg-hops","value"),
        Output("cfg-status-interval","value"),
        Output("cfg-bundle-size","value"),
        Output("cfg-prune-factor","value"),
        Output("cfg-stim-group-size","value"),
        Output("cfg-stim-amp","value"),
        Output("cfg-stim-decay","value"),
        Output("cfg-stim-max-symbols","value"),
        Output("cfg-speak-auto","value"),
        Output("cfg-speak-z","value"),
        Output("cfg-speak-hysteresis","value"),
        Output("cfg-speak-cooldown-ticks","value"),
        Output("cfg-speak-valence-thresh","value"),
        Output("cfg-b1-half-life-ticks","value"),
        Output("cfg-viz-every","value"),
        Output("cfg-log-every","value"),
        Output("cfg-checkpoint-every","value"),
        Output("cfg-checkpoint-keep","value"),
        Output("cfg-duration","value"),
        Output("cfg-load-engram","value"),
        Input("load-profile","n_clicks"),
        State("profile-path","value"),
        prevent_initial_call=True
    )
    def on_load_profile(_n, path):
        if not path:
            raise dash.exceptions.PreventUpdate
        data = read_json_file(path) or {}
        # Provide defaults for any missing fields
        def g(k, dv):
            v = data.get(k, dv)
            return v if v is not None else dv
        return (
            g("neurons", default_profile["neurons"]),
            g("k", default_profile["k"]),
            g("hz", default_profile["hz"]),
            g("domain", default_profile["domain"]),
            _checklist_from_bool(bool(g("use_time_dynamics", default_profile["use_time_dynamics"]))),
            _checklist_from_bool(bool(g("sparse_mode", default_profile["sparse_mode"]))),
            g("threshold", default_profile["threshold"]),
            g("lambda_omega", default_profile["lambda_omega"]),
            g("candidates", default_profile["candidates"]),
            g("walkers", default_profile["walkers"]),
            g("hops", default_profile["hops"]),
            g("status_interval", default_profile["status_interval"]),
            g("bundle_size", default_profile["bundle_size"]),
            g("prune_factor", default_profile["prune_factor"]),
            g("stim_group_size", default_profile["stim_group_size"]),
            g("stim_amp", default_profile["stim_amp"]),
            g("stim_decay", default_profile["stim_decay"]),
            g("stim_max_symbols", default_profile["stim_max_symbols"]),
            _checklist_from_bool(bool(g("speak_auto", default_profile["speak_auto"]))),
            g("speak_z", default_profile["speak_z"]),
            g("speak_hysteresis", default_profile["speak_hysteresis"]),
            g("speak_cooldown_ticks", default_profile["speak_cooldown_ticks"]),
            g("speak_valence_thresh", default_profile["speak_valence_thresh"]),
            g("b1_half_life_ticks", default_profile["b1_half_life_ticks"]),
            g("viz_every", default_profile["viz_every"]),
            g("log_every", default_profile["log_every"]),
            g("checkpoint_every", default_profile["checkpoint_every"]),
            g("checkpoint_keep", default_profile["checkpoint_keep"]),
            g("duration", default_profile["duration"]),
            g("load_engram", ""),
        )

    @app.callback(
        Output("run-dir","value", allow_duplicate=True),
        Input("use-current-run","n_clicks"),
        prevent_initial_call=True
    )
    def on_use_current(_n):
        return (manager.current_run_dir or no_update)

    @app.callback(
        Output("run-dir","value", allow_duplicate=True),
        Input("use-latest-run","n_clicks"),
        State("runs-root","value"),
        prevent_initial_call=True
    )
    def on_use_latest(_n, root):
        r = (root or runs_root)
        rs = list_runs(r)
        return (rs[0] if rs else no_update)

    @app.callback(
        Output("fig-dashboard","figure"),
        Output("fig-discovery","figure"),
        Input("poll","n_intervals"),
        Input("run-dir","value"),
        prevent_initial_call=False
    )
    def update_figs(_n, run_dir):
        if not run_dir:
            return go.Figure(), go.Figure()
        state = getattr(update_figs, "_state", None)
        if state is None or state.run_dir != run_dir:
            state = SeriesState(run_dir)
            setattr(update_figs, "_state", state)
        # tail events
        new_events, esize = tail_jsonl_bytes(state.events_path, state.events_size)
        state.events_size = esize
        for rec in new_events:
            append_event(state, rec)
        new_utd, usize = tail_jsonl_bytes(state.utd_path, state.utd_size)
        state.utd_size = usize
        for rec in new_utd:
            append_say(state, rec)
        # Trim series to a sliding window for responsiveness
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
        t = state.t
        active = ffill(state.active)
        avgw = ffill(state.avgw)
        coh = ffill(state.coh)
        comp = ffill(state.comp)
        b1z = ffill(state.b1z)
        val = ffill(state.val)
        val2 = ffill(state.val2)
        entro = ffill(state.entro)
        # fig1
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t, y=active, name="Active synapses", line=dict(width=1)))
        fig1.add_trace(go.Scatter(x=t, y=avgw, name="Avg W", yaxis="y2", line=dict(width=1,color="#1f77b4")))
        if any(v is not None for v in val):
            fig1.add_trace(go.Scatter(x=t, y=val, name="SIE valence", yaxis="y2", line=dict(width=1, dash="dot", color="#ff7f0e")))
        if any(v is not None for v in val2):
            fig1.add_trace(go.Scatter(x=t, y=val2, name="SIE v2 valence", yaxis="y2", line=dict(width=1, dash="dash", color="#2ca02c")))
        fig1.add_trace(go.Scatter(x=t, y=coh, name="Components", yaxis="y3", line=dict(width=1, color="#d62728")))
        fig1.add_trace(go.Scatter(x=t, y=comp, name="Cycles", yaxis="y4", line=dict(width=1, color="#8c564b")))
        fig1.add_trace(go.Scatter(x=t, y=b1z, name="B1 z", yaxis="y5", line=dict(width=1, color="#17becf")))
        if any(v is not None for v in entro):
            fig1.add_trace(go.Scatter(x=t, y=entro, name="Connectome entropy", yaxis="y6", line=dict(width=1, color="#9467bd")))
        fig1.update_layout(
            title=f"Dashboard — {os.path.basename(run_dir)}",
            xaxis=dict(domain=[0.05,0.95], title="Tick"),
            yaxis=dict(title="Active synapses", side="left"),
            yaxis2=dict(overlaying="y", side="right", title="Avg W / Valence", showgrid=False),
            yaxis3=dict(overlaying="y", side="left", position=0.02, showticklabels=False, showgrid=False),
            yaxis4=dict(overlaying="y", side="right", position=0.98, showticklabels=False, showgrid=False),
            yaxis5=dict(overlaying="y", side="right", position=0.96, showticklabels=False, showgrid=False),
            yaxis6=dict(overlaying="y", side="left", position=0.04, showticklabels=False, showgrid=False),
            legend=dict(orientation="h"),
            margin=dict(l=40,r=20,t=40,b=40),
        )
        # fig2
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=t, y=comp, name="Cycle hits", line=dict(width=1, color="#8c564b")))
        for tk in state.speak_ticks[-200:]:
            fig2.add_vline(x=tk, line_width=1, line_dash="dash", line_color="green")
        fig2.add_trace(go.Scatter(x=t, y=b1z, name="B1 z", yaxis="y2", line=dict(width=1, color="#17becf")))
        fig2.update_layout(
            title="Discovery & Self‑Speak",
            xaxis=dict(title="Tick"),
            yaxis=dict(title="Cycle hits"),
            yaxis2=dict(overlaying="y", side="right", title="B1 z", showgrid=False),
            legend=dict(orientation="h"),
            margin=dict(l=40,r=20,t=40,b=40),
        )
        return fig1, fig2

    # Auto-refresh launcher log every poll tick

    # Manual refresh still available; marked as duplicate output
    @app.callback(
        Output("launch-log","children", allow_duplicate=True),
        Input("show-log","n_clicks"),
        prevent_initial_call=True,
    )
    def on_show_log(_n):
        try:
            path = manager.launch_log
            if not path or not os.path.exists(path):
                return "No launcher log yet."
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                data = fh.read()
            return data[-4000:]
        except Exception as e:
            return f"Error reading launcher log: {e}"


    # --- Chat: send input to run-local inbox (consumed by UTE) ---
    @app.callback(
        Output("chat-status","children"),
        Output("chat-input","value"),
        Input("chat-send","n_clicks"),
        State("run-dir","value"),
        State("chat-input","value"),
        prevent_initial_call=True
    )
    def on_chat_send(_n, run_dir, text):
        rd = (run_dir or "").strip()
        msg = (text or "").strip()
        if not rd:
            return "Select a run directory.", no_update
        if not msg:
            return "Type a message.", no_update
        try:
            inbox = os.path.join(rd, "chat_inbox.jsonl")
            os.makedirs(os.path.dirname(inbox), exist_ok=True)
            with open(inbox, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"type":"text","msg": msg}, ensure_ascii=False) + "\n")
            return "Sent.", ""
        except Exception as e:
            return f"Error writing chat_inbox.jsonl: {e}", no_update

    # --- Chat: tail UTD 'say' macros and render as replies ---
    @app.callback(
        Output("chat-view","children"),
        Output("chat-state","data"),
        Input("poll","n_intervals"),
        Input("chat-filter","value"),
        State("run-dir","value"),
        State("chat-state","data"),
        prevent_initial_call=False
    )
    def on_chat_update(_n, filt, run_dir, data):
        rd = (run_dir or "").strip()
        if not rd:
            return "", {"run_dir":"", "utd_size":0, "inbox_size":0, "items":[]}

        state = data or {}
        items = list(state.get("items", []))
        last_run = state.get("run_dir")
        utd_size = int(state.get("utd_size", 0)) if isinstance(state.get("utd_size"), int) else 0
        inbox_size = int(state.get("inbox_size", 0)) if isinstance(state.get("inbox_size"), int) else 0

        # Reset if run changed
        if last_run != rd:
            items = []
            utd_size = 0
            inbox_size = 0

        # Tail model "say" outputs (from UTD)
        utd_path = os.path.join(rd, "utd_events.jsonl")
        new_utd_recs, new_utd_size = tail_jsonl_bytes(utd_path, utd_size)
        for rec in new_utd_recs:
            try:
                if isinstance(rec, dict) and (rec.get("type") == "macro") and (str(rec.get("macro","")).lower() == "say"):
                    args = rec.get("args") or {}
                    text = args.get("text") or ""
                    why = args.get("why") or rec.get("why") or {}
                    t = None
                    try:
                        t = int((why or {}).get("t"))
                    except Exception:
                        t = None
                    if text:
                        spike = False
                        if isinstance(why, dict):
                            try:
                                speak_ok = why.get("speak_ok")
                                top_spike = why.get("topology_spike")
                                b1z = why.get("b1_z")
                                spike = bool(speak_ok) or bool((why or {}).get('spike'))
                            except Exception:
                                spike = False
                        items.append({"kind":"model", "text": str(text), "t": t, "spike": bool(spike)})
            except Exception:
                pass

        # Tail user messages (from chat_inbox.jsonl)
        inbox_path = os.path.join(rd, "chat_inbox.jsonl")
        new_inbox_recs, new_inbox_size = tail_jsonl_bytes(inbox_path, inbox_size)
        for rec in new_inbox_recs:
            try:
                if isinstance(rec, dict):
                    mtype = (rec.get("type") or "").lower()
                    if mtype == "text":
                        msg = rec.get("msg") or rec.get("text") or ""
                        if msg:
                            items.append({"kind":"user", "text": str(msg), "t": None, "spike": False})
            except Exception:
                pass

        # keep last 200 items
        if len(items) > 200:
            items = items[-200:]

        # Render with filter
        filt = (filt or "all").lower()
        view_lines = []
        for it in items:
            if filt == "model":
                if it.get("kind") != "model":
                    continue
            elif filt == "spike":
                if it.get("kind") != "model" or not it.get("spike", False):
                    continue
            # Compose single-line display: user lines labeled; model lines are unlabeled text (optionally prefixed with t)
            t = it.get("t")
            text = it.get("text") or ""
            if it.get("kind") == "user":
                view_lines.append(f"You: {text}")
            else:
                if t is not None:
                    view_lines.append(f"[t={t}] {text}")
                else:
                    view_lines.append(f"{text}")

        view = "\n".join(view_lines)
        return view, {
            "run_dir": rd,
            "utd_size": int(new_utd_size),
            "inbox_size": int(new_inbox_size),
            "items": items
        }

    return app

def main():
    args = parse_args()
    app = build_app(args.runs_root)
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()