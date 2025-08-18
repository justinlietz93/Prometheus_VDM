from __future__ import annotations

import os

from .app import build_app


def main() -> None:
    rr = os.getenv("RUNS_ROOT", "").strip() or os.path.abspath("runs")
    app = build_app(rr)
    host = os.getenv("DASH_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("DASH_PORT", "8050"))
    except Exception:
        port = 8050
    # Avoid debug reloader to prevent duplicate callbacks
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()