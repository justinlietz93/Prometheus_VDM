"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

# control_server.py
# Lightweight local control server to expose a "Load Engram" button/page.
# - Serves a minimal HTML UI at http://127.0.0.1:<port>/
# - Accepts POST /api/load_engram with JSON {"path": "<engram file path>"}
# - Writes/updates runs/<ts>/phase.json with {"load_engram": "<path>"} so Nexus control plane will pick it up.

import os
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from urllib.parse import urlparse

_HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FUM Control — Load Engram</title>
  <style>
    :root { --fg: #e6edf3; --bg: #0d1117; --muted: #8b949e; --accent: #2f81f7; --danger: #f85149; }
    body { background: var(--bg); color: var(--fg); font: 14px/1.4 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, sans-serif; margin: 0; padding: 0; }
    .wrap { max-width: 880px; margin: 32px auto; padding: 16px 20px; }
    h1 { margin: 0 0 16px 0; font-size: 20px; }
    p.note { color: var(--muted); }
    .card { border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin: 16px 0; background: #161b22; }
    label { display: block; margin-bottom: 6px; color: var(--muted); }
    input[type=text] {
      width: 100%; padding: 10px 12px; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: var(--fg);
    }
    .row { display: flex; gap: 8px; align-items: center; margin-top: 10px; }
    button {
      padding: 10px 16px; border-radius: 6px; border: 1px solid #30363d; background: var(--accent); color: white; cursor: pointer;
    }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    .status { margin-top: 12px; min-height: 20px; }
    .ok { color: #3fb950; }
    .err { color: var(--danger); }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace; }
    .footer { margin-top: 24px; color: var(--muted); font-size: 12px; }
    code { background: #0b1220; padding: 2px 6px; border-radius: 4px; border: 1px solid #30363d; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>FUM Control — Load Engram</h1>
    <p class="note">Run directory: <span class="mono" id="runDir"></span></p>

    <div class="card">
      <label for="engram">Engram path (.h5 or .npz)</label>
      <input id="engram" type="text" placeholder="e.g. runs/20250811_155023/state_23220.h5" />
      <div class="row">
        <button id="btnLoad">Load Engram</button>
        <span class="mono" id="busy" style="display:none">loading…</span>
      </div>
      <div class="status" id="status"></div>
    </div>

    <div class="footer">
      The button sets <code>load_engram</code> in your run's <code>phase.json</code>; Nexus will hot-load it on the next poll and then clear the field.
    </div>
  </div>

  <script>
    const runDirSpan = document.getElementById('runDir');
    fetch('/api/status').then(r => r.json()).then(js => {
      runDirSpan.textContent = js.run_dir || '(unknown)';
    }).catch(() => { runDirSpan.textContent = '(unknown)'; });

    const el = (id) => document.getElementById(id);
    el('btnLoad').addEventListener('click', async () => {
      const path = el('engram').value.trim();
      const btn = el('btnLoad');
      const busy = el('busy');
      const status = el('status');
      status.textContent = '';
      status.className = 'status';
      if (!path) {
        status.textContent = 'Please enter a file path.';
        status.classList.add('err');
        return;
      }
      btn.disabled = true; busy.style.display = 'inline';
      try {
        const res = await fetch('/api/load_engram', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path })
        });
        const js = await res.json().catch(() => ({}));
        if (res.ok && js.ok) {
          status.textContent = 'Queued load_engram: ' + (js.path || path);
          status.classList.add('ok');
        } else {
          status.textContent = 'Error: ' + (js.error || ('HTTP ' + res.status));
          status.classList.add('err');
        }
      } catch (err) {
        status.textContent = 'Request failed';
        status.classList.add('err');
      } finally {
        btn.disabled = false; busy.style.display = 'none';
      }
    });
  </script>
</body>
</html>
'''

class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class _Handler(BaseHTTPRequestHandler):
    # Server context attached at runtime: self.server.ctx = { 'run_dir': ..., 'phase_file': ... }

    def _json(self, code: int, obj: dict):
        try:
            payload = json.dumps(obj).encode("utf-8")
        except Exception:
            payload = b'{}'
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(payload)
        except Exception:
            pass

    def _text(self, code: int, html: str):
        try:
            data = html.encode("utf-8")
        except Exception:
            data = b""
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        try:
            self.wfile.write(data)
        except Exception:
            pass

    def do_GET(self):
        try:
            path = urlparse(self.path).path
        except Exception:
            path = "/"
        if path in ("/", "/index", "/index.html"):
            # Fill in run_dir client-side via /api/status
            return self._text(200, _HTML)
        if path == "/api/status":
            ctx = getattr(self.server, "ctx", {})
            run_dir = ctx.get("run_dir", "")
            return self._json(200, {"ok": True, "run_dir": run_dir})
        return self._json(404, {"ok": False, "error": "not_found"})

    def do_POST(self):
        try:
            path = urlparse(self.path).path
        except Exception:
            path = "/"
        if path != "/api/load_engram":
            return self._json(404, {"ok": False, "error": "not_found"})

        # parse JSON
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except Exception:
            length = 0
        try:
            body = self.rfile.read(length) if length > 0 else b"{}"
        except Exception:
            body = b"{}"
        try:
            data = json.loads(body.decode("utf-8"))
        except Exception:
            data = {}
        raw_path = data.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            return self._json(400, {"ok": False, "error": "path_missing"})

        # Normalize path
        p = raw_path.strip()
        try:
            p = os.path.expanduser(p)
        except Exception:
            pass
        # Allow relative paths; make them absolute relative to CWD
        try:
            if not os.path.isabs(p):
                p = os.path.abspath(p)
        except Exception:
            pass

        # Optional existence check to reduce confusion
        if not os.path.exists(p):
            return self._json(400, {"ok": False, "error": "path_not_found", "path": p})

        # Write/merge phase.json with load_engram directive
        ctx = getattr(self.server, "ctx", {})
        phase_file = ctx.get("phase_file")
        if not isinstance(phase_file, str) or not phase_file:
            return self._json(500, {"ok": False, "error": "phase_file_unavailable"})

        obj = {}
        try:
            if os.path.exists(phase_file):
                with open(phase_file, "r", encoding="utf-8") as fh:
                    obj = json.load(fh)
                    if not isinstance(obj, dict):
                        obj = {}
        except Exception:
            obj = {}

        obj["load_engram"] = p
        try:
            os.makedirs(os.path.dirname(phase_file), exist_ok=True)
        except Exception:
            pass

        try:
            with open(phase_file, "w", encoding="utf-8") as fh:
                json.dump(obj, fh, ensure_ascii=False, indent=2)
        except Exception as e:
            return self._json(500, {"ok": False, "error": "write_failed", "detail": str(e)})

        return self._json(200, {"ok": True, "path": p})

    # Quiet server logs
    def log_message(self, fmt, *args):
        try:
            # Suppress default stderr chatter
            return
        except Exception:
            pass


class ControlServer:
    """
    Spawn a local HTTP control server in a background thread.
    Exposes:
      - url: http://127.0.0.1:<port>/
      - stop(): shutdown server
    """
    def __init__(self, run_dir: str, host: str = "127.0.0.1", port: int = 8765):
        self.run_dir = run_dir
        self.phase_file = os.path.join(run_dir, "phase.json")
        self.host = host
        self.port = None
        self._server = None
        self._thread = None

        # Bind first available port in a small range
        last_err = None
        for p in range(int(port), int(port) + 16):
            try:
                server = ThreadingHTTPServer((host, p), _Handler)
                server.ctx = {"run_dir": self.run_dir, "phase_file": self.phase_file}
                self._server = server
                self.port = p
                break
            except OSError as e:
                last_err = e
                continue

        if self._server is None:
            raise RuntimeError(f"Failed to bind control server on {host}:{port} (+15) — last error: {last_err}")

        t = threading.Thread(target=self._server.serve_forever, name="fum-control-server", daemon=True)
        t.start()
        self._thread = t

        self.url = f"http://{host}:{self.port}/"

    def stop(self):
        try:
            if self._server:
                self._server.shutdown()
        except Exception:
            pass
        try:
            if self._server:
                self._server.server_close()
        except Exception:
            pass
        self._server = None