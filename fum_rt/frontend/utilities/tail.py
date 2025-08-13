import os
import json
from typing import Any, Tuple, List


def _parse_jsonl_line(line: str) -> Any:
    try:
        return json.loads(line)
    except Exception:
        return None


def tail_jsonl_bytes(path: str, last_size: int) -> Tuple[List[Any], int]:
    """
    Tail a JSONL file by byte offset.

    Inputs:
    - path: file path to JSONL
    - last_size: previous file size (bytes) to resume from

    Returns:
    - (records, new_size)
      records: list of parsed JSON objects appended since last_size
      new_size: new file size to store for the next call
    """
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
    recs: List[Any] = []
    buf: List[str] = []
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