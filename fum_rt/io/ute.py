
import sys, time, queue, threading, os, json

class UTE:
    """Universal Temporal Encoder.
    Feeds inbound messages into a queue the Nexus can poll every tick.
    Sources implemented: stdin (lines) and synthetic 'tick' generator.
    """
    def __init__(self, use_stdin=True, inbox_path=None):
        self.q = queue.Queue(maxsize=1024)
        self._stop = threading.Event()
        self.use_stdin = use_stdin
        self._threads = []
        # Optional run-local chat inbox (JSONL), e.g. runs/<ts>/chat_inbox.jsonl
        self.inbox_path = inbox_path
        self._inbox_size = 0

    def start(self):
        if self.use_stdin:
            t = threading.Thread(target=self._stdin_reader, daemon=True)
            t.start()
            self._threads.append(t)
        # Optional chat inbox tailer
        if self.inbox_path:
            t3 = threading.Thread(target=self._inbox_reader, daemon=True)
            t3.start()
            self._threads.append(t3)
        # Always run a synthetic ticker as a heartbeat
        t2 = threading.Thread(target=self._ticker, daemon=True)
        t2.start()
        self._threads.append(t2)

    def stop(self):
        self._stop.set()

    def _stdin_reader(self):
        for line in sys.stdin:
            if self._stop.is_set(): break
            line = line.strip()
            if line:
                self.q.put({'type': 'text', 'msg': line})

    def _inbox_reader(self):
        # Tail a JSONL chat inbox file (appended by dashboard/chat UI)
        while not self._stop.is_set():
            try:
                path = self.inbox_path
                if not path or not os.path.exists(path):
                    time.sleep(0.5)
                    continue
                size = os.path.getsize(path)
                # handle truncation/rotation
                if size < self._inbox_size:
                    self._inbox_size = 0
                if size == self._inbox_size:
                    time.sleep(0.5)
                    continue
                with open(path, "rb") as f:
                    f.seek(self._inbox_size)
                    data = f.read(size - self._inbox_size)
                self._inbox_size = size
                text = data.decode("utf-8", errors="ignore")
                for line in text.splitlines():
                    s = line.strip()
                    if not s:
                        continue
                    try:
                        rec = json.loads(s)
                    except Exception:
                        rec = {"type": "text", "msg": s}
                    if isinstance(rec, dict):
                        if rec.get("type") == "text" and "msg" in rec:
                            self.q.put({"type": "text", "msg": str(rec.get("msg"))})
                        else:
                            # Allow passthrough of structured events if provided
                            self.q.put(rec)
            except Exception:
                # Keep runtime alive on any error
                time.sleep(0.5)

    def _ticker(self):
        # 1 Hz ticker (used as heartbeat input)
        while not self._stop.is_set():
            self.q.put({'type':'tick', 'msg':'tick'})
            time.sleep(1.0)

    def poll(self, max_items=32):
        out = []
        while len(out) < max_items:
            try:
                out.append(self.q.get_nowait())
            except queue.Empty:
                break
        return out
