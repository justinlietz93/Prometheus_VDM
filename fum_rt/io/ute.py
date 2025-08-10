
import sys, time, queue, threading

class UTE:
    """Universal Temporal Encoder.
    Feeds inbound messages into a queue the Nexus can poll every tick.
    Sources implemented: stdin (lines) and synthetic 'tick' generator.
    """
    def __init__(self, use_stdin=True):
        self.q = queue.Queue(maxsize=1024)
        self._stop = threading.Event()
        self.use_stdin = use_stdin
        self._threads = []

    def start(self):
        if self.use_stdin:
            t = threading.Thread(target=self._stdin_reader, daemon=True)
            t.start()
            self._threads.append(t)
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
