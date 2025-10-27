"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Rolling JSONL writer with bounded main file and archival segments.

- Maintains a capped "active" JSONL file (e.g., events.jsonl, utd_events.jsonl).
- When the active file exceeds the configured size or line cap, the oldest lines
  are streamed into an archive segment and the active file is rewritten to keep
  only the newest tail (rolling buffer).
- Archive segments live under: <run_dir>/archived/<YYYYMMDD_HHMMSS>/<base_name>
  Example: runs/<ts>/archived/20250815_120828/events.jsonl
- When the current archive segment exceeds its cap, a new timestamped segment
  directory is created and subsequent archival lines are appended there.

Configuration (env):
- For events.jsonl (category="EVENTS"):
    FUM_EVENTS_MAX_MB                  (default: 256)
    FUM_EVENTS_MAX_LINES               (default: unset; bytes cap used)
    FUM_EVENTS_ARCHIVE_SEGMENT_MB      (default: 512)
    FUM_EVENTS_ARCHIVE_SEGMENT_LINES   (default: unset; bytes cap used)
- For utd_events.jsonl (category="UTD"):
    FUM_UTD_MAX_MB                     (default: 256)
    FUM_UTD_MAX_LINES                  (default: unset; bytes cap used)
    FUM_UTD_ARCHIVE_SEGMENT_MB         (default: 512)
    FUM_UTD_ARCHIVE_SEGMENT_LINES      (default: unset; bytes cap used)
- Global:
    FUM_LOG_ROLL_CHECK_EVERY           (default: 200)  # enforce cadence (per write)

Notes:
- Uses a cross-process advisory lock via <base_path>.lock to serialize trimming with writers.
- Writers should not hold persistent file handles; always append per call (MacroEmitter, UTD updated).
"""

from __future__ import annotations

import io
import os
import time
import threading
from typing import Optional, Tuple

try:
    import fcntl as _fcntl
except Exception:  # non-posix fallback (no-op locks)
    _fcntl = None


def _now_ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _is_ts_dir(name: str) -> bool:
    # YYYYMMDD_HHMMSS
    if len(name) != 15:
        return False
    d, u = name.split("_", 1) if "_" in name else ("", "")
    return d.isdigit() and u.isdigit() and len(d) == 8 and len(u) == 6


class RollingJsonlWriter:
    """
    Append-only JSONL writer with rolling buffer and archival segments.

    Usage:
        w = RollingJsonlWriter("/path/to/events.jsonl")
        w.write_line('{"msg":"hello"}')
    """

    def __init__(
        self,
        base_path: str,
        *,
        max_main_bytes: Optional[int] = None,
        max_main_lines: Optional[int] = None,
        archive_dir: Optional[str] = None,
        archive_segment_max_bytes: Optional[int] = None,
        archive_segment_max_lines: Optional[int] = None,
        check_every: Optional[int] = None,
    ) -> None:
        self.base_path = os.path.abspath(base_path)
        _ensure_dir(os.path.dirname(self.base_path))
        self.lock_path = self.base_path + ".lock"
        self._local_lock = threading.Lock()

        base_name = os.path.basename(self.base_path).lower()
        if base_name == "events.jsonl":
            cat = "EVENTS"
        elif "utd" in base_name:
            cat = "UTD"
        else:
            cat = "LOG"

        # Defaults via env (prefer bytes caps unless specific line caps are set)
        def _env_int(name: str, default: Optional[int]) -> Optional[int]:
            v = os.environ.get(name, None)
            if v is None or str(v).strip() == "":
                return default
            try:
                return int(v)
            except Exception:
                return default

        if max_main_bytes is None:
            if cat == "EVENTS":
                max_main_bytes = _env_int("FUM_EVENTS_MAX_MB", 256)
            elif cat == "UTD":
                max_main_bytes = _env_int("FUM_UTD_MAX_MB", 256)
            else:
                max_main_bytes = _env_int("FUM_LOG_MAX_MB", 128)
            max_main_bytes = int(max_main_bytes) * 1024 * 1024 if max_main_bytes else None

        if max_main_lines is None:
            if cat == "EVENTS":
                max_main_lines = _env_int("FUM_EVENTS_MAX_LINES", None)
            elif cat == "UTD":
                max_main_lines = _env_int("FUM_UTD_MAX_LINES", None)
            else:
                max_main_lines = _env_int("FUM_LOG_MAX_LINES", None)

        if archive_dir is None:
            archive_dir = os.path.join(os.path.dirname(self.base_path), "archived")
        self.archive_dir = archive_dir

        if archive_segment_max_bytes is None:
            if cat == "EVENTS":
                archive_segment_max_bytes = _env_int("FUM_EVENTS_ARCHIVE_SEGMENT_MB", 512)
            elif cat == "UTD":
                archive_segment_max_bytes = _env_int("FUM_UTD_ARCHIVE_SEGMENT_MB", 512)
            else:
                archive_segment_max_bytes = _env_int("FUM_LOG_ARCHIVE_SEGMENT_MB", 256)
            archive_segment_max_bytes = (
                int(archive_segment_max_bytes) * 1024 * 1024 if archive_segment_max_bytes else None
            )

        if archive_segment_max_lines is None:
            if cat == "EVENTS":
                archive_segment_max_lines = _env_int("FUM_EVENTS_ARCHIVE_SEGMENT_LINES", None)
            elif cat == "UTD":
                archive_segment_max_lines = _env_int("FUM_UTD_ARCHIVE_SEGMENT_LINES", None)
            else:
                archive_segment_max_lines = _env_int("FUM_LOG_ARCHIVE_SEGMENT_LINES", None)

        self.max_main_bytes = max_main_bytes
        self.max_main_lines = max_main_lines
        self.archive_segment_max_bytes = archive_segment_max_bytes
        self.archive_segment_max_lines = archive_segment_max_lines

        if check_every is None:
            check_every = _env_int("FUM_LOG_ROLL_CHECK_EVERY", 200) or 200
        self._check_every = int(check_every)
        self._ops = 0

    # ------------- public -------------
    def write_line(self, line: str) -> None:
        data = (line.rstrip("\n") + "\n").encode("utf-8", errors="ignore")
        with self._local_lock:
            with self._acquire_lock():
                # append
                with open(self.base_path, "ab") as fh:
                    fh.write(data)
                self._ops += 1
                if (self._ops % self._check_every) == 0:
                    self._enforce()

    # ------------- internals -------------
    def _acquire_lock(self):
        class _Locker:
            def __init__(self, p: str) -> None:
                self.p = p
                self.fh = None

            def __enter__(self):
                _ensure_dir(os.path.dirname(self.p))
                self.fh = open(self.p, "a+")
                if _fcntl is not None:
                    _fcntl.flock(self.fh.fileno(), _fcntl.LOCK_EX)
                return self

            def __exit__(self, exc_type, exc, tb):
                try:
                    if _fcntl is not None and self.fh is not None:
                        _fcntl.flock(self.fh.fileno(), _fcntl.LOCK_UN)
                finally:
                    try:
                        if self.fh:
                            self.fh.close()
                    except Exception:
                        pass

        return _Locker(self.lock_path)

    def _enforce(self) -> None:
        """Trim oldest lines to keep main file under configured cap and move trimmed lines to archive."""
        try:
            size = os.path.getsize(self.base_path)
        except Exception:
            return

        # Prefer bytes cap unless a line cap is explicitly configured
        if self.max_main_lines and self.max_main_lines > 0:
            self._enforce_by_lines(self.max_main_lines)
        elif self.max_main_bytes and size > self.max_main_bytes:
            to_remove = size - self.max_main_bytes
            self._trim_oldest_bytes_to_archive(to_remove)

    def _enforce_by_lines(self, keep_last_lines: int) -> None:
        try:
            # Count lines
            total = 0
            with open(self.base_path, "rb") as fh:
                for _ in fh:
                    total += 1
            if total <= keep_last_lines:
                return
            to_remove = total - keep_last_lines

            # Stream: first 'to_remove' lines -> archive; remainder -> temp; then replace
            self._stream_archive_and_tail(to_remove_lines=to_remove)
        except Exception:
            return

    def _trim_oldest_bytes_to_archive(self, remove_bytes: int) -> None:
        if remove_bytes <= 0:
            return
        # Best-effort: move enough whole lines to cover remove_bytes
        moved = 0
        try:
            seg_fh, _ = self._open_archive_for_append()
            try:
                tmp_path = self.base_path + ".tmp"
                with open(self.base_path, "rb") as src, open(tmp_path, "wb") as dst:
                    for line in src:
                        if moved < remove_bytes:
                            # ensure we rotate segment if needed
                            self._seg_write(seg_fh, line)
                            moved += len(line)
                        else:
                            dst.write(line)
                # Replace atomically
                os.replace(tmp_path, self.base_path)
            finally:
                try:
                    if seg_fh:
                        seg_fh.close()
                except Exception:
                    pass
        except Exception:
            return

    def _stream_archive_and_tail(self, to_remove_lines: int) -> None:
        if to_remove_lines <= 0:
            return
        removed = 0
        try:
            seg_fh, _ = self._open_archive_for_append()
            try:
                tmp_path = self.base_path + ".tmp"
                with open(self.base_path, "rb") as src, open(tmp_path, "wb") as dst:
                    for line in src:
                        if removed < to_remove_lines:
                            self._seg_write(seg_fh, line)
                            removed += 1
                        else:
                            dst.write(line)
                os.replace(tmp_path, self.base_path)
            finally:
                try:
                    if seg_fh:
                        seg_fh.close()
                except Exception:
                    pass
        except Exception:
            return

    # ----- archive segment helpers -----
    def _open_archive_for_append(self) -> Tuple[io.BufferedWriter, str]:
        """
        Return a file handle opened for appending to the current archive segment and the segment dir.
        Creates archive dir/segment as needed.
        """
        _ensure_dir(self.archive_dir)
        # Select latest timestamp directory or create new
        try:
            dirs = [d for d in os.listdir(self.archive_dir) if _is_ts_dir(d)]
        except Exception:
            dirs = []
        if dirs:
            dirs.sort()
            seg_dir = os.path.join(self.archive_dir, dirs[-1])
        else:
            seg_dir = os.path.join(self.archive_dir, _now_ts())
            _ensure_dir(seg_dir)

        # Archive filename mirrors base filename inside the segment directory
        arch_file = os.path.join(seg_dir, os.path.basename(self.base_path))
        _ensure_dir(os.path.dirname(arch_file))

        # If current segment overflows max, rotate to a new segment directory
        if self._segment_full(arch_file):
            seg_dir = os.path.join(self.archive_dir, _now_ts())
            _ensure_dir(seg_dir)
            arch_file = os.path.join(seg_dir, os.path.basename(self.base_path))

        fh = open(arch_file, "ab")
        return fh, seg_dir

    def _segment_full(self, arch_file: str) -> bool:
        try:
            size = os.path.getsize(arch_file)
        except Exception:
            size = 0
        # bytes-based check first
        if self.archive_segment_max_bytes and self.archive_segment_max_bytes > 0:
            if size >= self.archive_segment_max_bytes:
                return True
        # optional lines-based check
        if self.archive_segment_max_lines and self.archive_segment_max_lines > 0:
            try:
                cnt = 0
                with open(arch_file, "rb") as fh:
                    for _ in fh:
                        cnt += 1
                if cnt >= self.archive_segment_max_lines:
                    return True
            except Exception:
                return False
        return False

    def _seg_write(self, seg_fh: io.BufferedWriter, line: bytes) -> None:
        # Append line to current segment, rotate if segment crosses cap
        try:
            seg_fh.write(line)
            seg_fh.flush()
        except Exception:
            return
        # If segment now full, open a new one for subsequent writes
        try:
            if self._segment_full(seg_fh.name):  # type: ignore[attr-defined]
                seg_fh.close()
                new_fh, _ = self._open_archive_for_append()
                seg_fh.__dict__.update(new_fh.__dict__)  # swap internals (best-effort)
        except Exception:
            pass


# ---------- Logging handler integration ----------

import logging


class RollingJsonlHandler(logging.Handler):
    """
    logging.Handler that writes formatted JSON lines to a bounded rolling JSONL file.
    """
    def __init__(self, path: str) -> None:
        super().__init__(level=logging.INFO)
        self._writer = RollingJsonlWriter(path)
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._writer.write_line(msg)
        except Exception:
            # Avoid crashing logging subsystem
            pass

class RollingZipJsonlHandler(logging.Handler):
    """
    logging.Handler that writes formatted JSON lines to a zip-spooled JSONL buffer.
    The buffer is truncated when it exceeds the configured threshold and compressed
    into a .zip archive adjacent to the buffer file (e.g., events.jsonl -> events.zip).
    """
    def __init__(self, path: str) -> None:
        super().__init__(level=logging.INFO)
        # Prefer zip spooler for bounded disk pressure
        self._writer = RollingZipJsonlWriter(path)  # type: ignore[name-defined]
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._writer.write_line(msg)
        except Exception:
            # Avoid crashing logging subsystem
            pass

__all__ = ["RollingJsonlWriter", "RollingJsonlHandler", "RollingZipJsonlWriter", "RollingZipJsonlHandler"]
# ---------- Zip spool writer (optional) ----------
# Lightweight, void-faithful spooler that compresses the active JSONL buffer into a growing .zip
# once it exceeds a bounded threshold, then truncates the buffer. Keeps a tiny in-process ring
# for quick peeks. Uses RollingJsonlWriter's advisory lock to coordinate with other writers.
import zipfile as _zipfile  # stdlib

class RollingZipJsonlWriter:
    """
    Zip spooler for JSONL:
    - Appends lines to a small active buffer file (base_path)
    - When buffer exceeds max_buffer_bytes, compresses it into <base_name>.zip (append mode)
      under the same directory and truncates the buffer to zero
    - Tracks coarse stats for UI/status reporting (entries, sizes)
    - Thread-safe; coordinates with other processes via RollingJsonlWriter's lock
    """

    def __init__(
        self,
        base_path: str,
        *,
        max_buffer_bytes: int | None = None,
        ring_bytes: int | None = None,
        zip_path: str | None = None,
    ) -> None:
        self.base_path = os.path.abspath(base_path)
        _ensure_dir(os.path.dirname(self.base_path))
        # Defaults (env-overridable)
        try:
            if max_buffer_bytes is None:
                max_buffer_bytes = int(os.getenv("FUM_ZIP_BUFFER_BYTES", "1048576"))  # 1 MiB
        except Exception:
            max_buffer_bytes = 1_048_576
        try:
            if ring_bytes is None:
                ring_bytes = int(os.getenv("FUM_ZIP_RING_BYTES", "65536"))  # 64 KiB
        except Exception:
            ring_bytes = 65_536
        self.max_buffer_bytes = int(max(32 * 1024, max_buffer_bytes or 1_048_576))
        self._ring_cap = int(max(1024, ring_bytes or 65_536))
        self._ring = bytearray()
        # Zip path next to base_path (events.jsonl -> events.zip)
        if not zip_path:
            stem = os.path.splitext(os.path.basename(self.base_path))[0]
            zip_path = os.path.join(os.path.dirname(self.base_path), f"{stem}.zip")
        self.zip_path = os.path.abspath(zip_path)

        # Use RollingJsonlWriter with huge caps to avoid its archival path interfering
        # (we rely on the zip spool rotation below)
        self._writer = RollingJsonlWriter(
            self.base_path,
            max_main_bytes=10**12,              # effectively disable
            max_main_lines=None,
            archive_dir=os.path.join(os.path.dirname(self.base_path), "archived"),
            archive_segment_max_bytes=None,
            archive_segment_max_lines=None,
            check_every=2_147_483_647,          # effectively disable
        )
        self._zip_entries_cache: int | None = None
        self._local_lock = threading.Lock()

    def write_line(self, line: str) -> None:
        # Append line (delegates to rolling writer for atomic append)
        self._writer.write_line(line)
        # Update in-process ring
        try:
            data = (line.rstrip("\n") + "\n").encode("utf-8", errors="ignore")
            self._ring.extend(data)
            if len(self._ring) > self._ring_cap:
                # keep last _ring_cap bytes
                self._ring[:] = self._ring[-self._ring_cap:]
        except Exception:
            pass

        # Rotate to zip if buffer exceeds threshold (guarded by advisory lock)
        try:
            with self._writer._acquire_lock():  # type: ignore[attr-defined]
                try:
                    size = os.path.getsize(self.base_path)
                except Exception:
                    size = 0
                if size >= self.max_buffer_bytes:
                    # Read buffer
                    try:
                        with open(self.base_path, "rb") as fh:
                            buf = fh.read()
                    except Exception:
                        buf = b""
                    if buf:
                        arcname = f"{os.path.basename(self.base_path)}.{_now_ts()}.jsonl"
                        try:
                            with _zipfile.ZipFile(self.zip_path, mode="a", compression=_zipfile.ZIP_DEFLATED) as zf:
                                zf.writestr(arcname, buf)
                                # Seed entries cache if unknown
                                try:
                                    if self._zip_entries_cache is None:
                                        self._zip_entries_cache = 0
                                    self._zip_entries_cache += 1
                                except Exception:
                                    pass
                        except Exception:
                            # best-effort: do not abort rotation
                            pass
                        # Truncate buffer
                        try:
                            with open(self.base_path, "wb") as fh2:
                                fh2.write(b"")
                        except Exception:
                            pass
        except Exception:
            # best-effort; avoid throwing on contentions
            pass

    def stats(self) -> dict:
        """
        Return coarse spool statistics for status reporting:
          - buffer_bytes: size of active JSONL buffer
          - zip_bytes: size of the zip archive file
          - zip_entries: count of archived segments (approximate)
          - ring_bytes: size of in-process ring buffer
        """
        try:
            buffer_bytes = os.path.getsize(self.base_path)
        except Exception:
            buffer_bytes = 0
        try:
            zip_bytes = os.path.getsize(self.zip_path)
        except Exception:
            zip_bytes = 0
        # If entries unknown, estimate by inspecting the zip once
        if self._zip_entries_cache is None:
            try:
                if os.path.exists(self.zip_path):
                    with _zipfile.ZipFile(self.zip_path, mode="r") as zf:
                        self._zip_entries_cache = len(zf.namelist())
                else:
                    self._zip_entries_cache = 0
            except Exception:
                self._zip_entries_cache = 0
        return {
            "buffer_bytes": int(buffer_bytes),
            "zip_bytes": int(zip_bytes),
            "zip_entries": int(self._zip_entries_cache or 0),
            "ring_bytes": int(len(self._ring)),
        }

# expose in module exports
try:
    __all__.append("RollingZipJsonlWriter")  # type: ignore[name-defined]
except Exception:
    __all__ = ["RollingJsonlWriter", "RollingJsonlHandler", "RollingZipJsonlWriter"]