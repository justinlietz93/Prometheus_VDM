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
    ss.val.append(ex.get("sie_valence_01"))
    ss.val2.append(ex.get("sie_v2_valence_01"))
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
        "sparse_mode": False, "walkers": 256, "hops": 3, "bundle_size": 3, "prune_factor": 0.10,
        "viz_every": 0, "log_every": 1,
        "speak_auto": True, "speak_z": 3.0, "speak_hysteresis": 0.5, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.55,
        "b1_half_life_ticks": 50,
        "stim_group_size": 8, "stim_amp": 0.08, "stim_decay": 0.92, "stim_max_symbols": 128,
        "checkpoint_every": 60, "checkpoint_keep": 5, "duration": None
    }

    def list_profiles() -> List[str]:
        return sorted([os.path.join(PROFILES_DIR, f) for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])

    app.layout = html.Div([
        html.H3("FUM Live Dashboard (external control)"),
        html.Div([
            html.Div([
                html.Label("Runs root"),
                dcc.Input(id="runs-root", type="text", value=runs_root, style={"width":"100%"}),
                html.Button("Refresh Runs", id="refresh-runs", n_clicks=0, style={"marginTop":"6px"}),
                html.Label("Run directory"),
                dcc.Dropdown(id="run-dir", options=[{"label": p, "value": p} for p in runs], value=default_run),
                html.Button("Use Current Run", id="use-current-run", n_clicks=0, style={"marginTop":"6px"}),
                html.Hr(),
                html.Label("Phase control"),
                dcc.Slider(id="phase", min=0, max=4, step=1, value=0, marks={i:str(i) for i in range(5)}),
                html.Button("Apply Phase", id="apply-phase", n_clicks=0, style={"marginTop":"6px"}),
                html.Pre(id="phase-status", style={"fontSize":"12px"}),
                html.Hr(),
                html.Label("Feed file to stdin (optional)"),
                dcc.Input(id="feed-path", type="text", placeholder="path/to/text.txt", style={"width":"100%"}),
                dcc.Input(id="feed-rate", type="number", value=20, step=1, style={"width":"120px", "marginTop":"6px"}),
                html.Div([
                    html.Button("Start Feed", id="feed-start", n_clicks=0),
                    html.Button("Stop Feed", id="feed-stop", n_clicks=0, style={"marginLeft":"8px"}),
                ], style={"marginTop":"6px"}),
                html.Hr(),
                html.Label("Send one line"),
                dcc.Input(id="send-line", type="text", placeholder="type and Enter", style={"width":"100%"}),
                html.Button("Send", id="send-btn", n_clicks=0, style={"marginTop":"6px"}),
                html.Pre(id="send-status", style={"fontSize":"12px"}),
            ], style={"flex":"1", "paddingRight":"10px", "borderRight":"1px solid #ccc"}),
            html.Div([
                html.H4("Run profiles (JSON) and process control"),
                html.Div([
                    html.Label("Profile JSON"),
                    dcc.Textarea(id="profile-json", value=json.dumps(default_profile, indent=2), style={"width":"100%","height":"260px","fontFamily":"monospace","fontSize":"12px"}),
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
            ], style={"flex":"2","paddingLeft":"10px"}),
        ], style={"display":"flex"}),
        dcc.Interval(id="poll", interval=1000, n_intervals=0),
        dcc.Store(id="ui-state")
    ], style={"padding":"10px"})

    # ---------- Callbacks ----------
    @app.callback(
        Output("run-dir","options"),
        Output("run-dir","value"),
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
        prevent_initial_call=True
    )
    def on_apply_phase(_n, run_dir, phase):
        if not run_dir:
            return "Select a run directory."
        prof = {"phase": int(phase or 0)}
        ok = write_json_file(os.path.join(run_dir,"phase.json"), prof)
        return "Applied" if ok else "Error writing phase.json"

    @app.callback(
        Output("proc-status","children"),
        Output("run-dir","value"),
        Input("start-run","n_clicks"),
        State("profile-json","value"),
        State("runs-root","value"),
        prevent_initial_call=True
    )
    def on_start(_n, profile_json, root):
        try:
            profile = json.loads(profile_json or "{}")
        except Exception as e:
            return f"Invalid profile JSON: {e}", no_update
        ok, msg = manager.start(profile)
        if not ok:
            # msg contains error and possibly launch log; surface it
            return f"Start failed:\n{msg}", no_update
        # msg is run_dir on success
        run_dir = msg
        cmd_echo = " ".join(manager.last_cmd or [])
        return (f"Started.\nrun_dir={run_dir}\n"
                f"checkpoint_every={profile.get('checkpoint_every')} keep={profile.get('checkpoint_keep')}\n"
                f"cmd: {cmd_echo}\n"
                f"launch_log: {manager.launch_log}"), run_dir or no_update

    @app.callback(
        Output("proc-status","children", allow_duplicate=True),
        Input("stop-run","n_clicks"),
        prevent_initial_call=True
    )
    def on_stop(_n):
        ok, msg = manager.stop()
        return "Stopped." if ok else msg

    @app.callback(
        Output("proc-status","children", allow_duplicate=True),
        Input("send-btn","n_clicks"),
        State("send-line","value"),
        prevent_initial_call=True
    )
    def on_send(_n, line):
        if not line:
            return no_update
        ok = manager.send_line(line)
        return "Sent." if ok else "Not running."

    @app.callback(
        Output("send-status","children"),
        Input("feed-start","n_clicks"),
        State("feed-path","value"),
        State("feed-rate","value"),
        prevent_initial_call=True
    )
    def on_feed_start(_n, path, rate):
        if not path:
            return "Provide a feed path."
        ok = manager.feed_file(path, float(rate or 20.0))
        return "Feeding." if ok else "Feed failed (check process running and path)."

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
        State("profile-json","value"),
        prevent_initial_call=True
    )
    def on_save_profile(_n, name, text):
        name = (name or "").strip()
        if not name:
            return [{"label": p, "value": p} for p in list_profiles()], "Provide a profile name."
        try:
            data = json.loads(text or "{}")
        except Exception as e:
            return [{"label": p, "value": p} for p in list_profiles()], f"Invalid profile JSON: {e}"
        path = os.path.join(PROFILES_DIR, f"{name}.json")
        ok = write_json_file(path, data)
        status = f"Saved profile to {path}" if ok else f"Error writing {path}"
        return [{"label": p, "value": p} for p in list_profiles()], status

    @app.callback(
        Output("profile-json","value"),
        Input("load-profile","n_clicks"),
        State("profile-path","value"),
        prevent_initial_call=True
    )
    def on_load_profile(_n, path):
        if not path:
            return no_update
        data = read_json_file(path)
        if data is None:
            return no_update
        return json.dumps(data, indent=2)

    @app.callback(
        Output("use-current-run","n_clicks"),
        Output("run-dir","value", allow_duplicate=True),
        Input("use-current-run","n_clicks"),
        prevent_initial_call=True
    )
    def on_use_current(_n):
        return 0, (manager.current_run_dir or no_update)

    @app.callback(
        Output("fig-dashboard","figure"),
        Output("fig-discovery","figure"),
        Input("poll","n_intervals"),
        State("run-dir","value"),
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

    @app.callback(
        Output("launch-log","children"),
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


    return app

def main():
    args = parse_args()
    app = build_app(args.runs_root)
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()