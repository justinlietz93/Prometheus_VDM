#!/usr/bin/env python3
"""
Compact VS Code state rows that contain a large `taskHistory` array.
- Caps by count AND by bytes.
- Scrubs very long strings and message-like arrays inside each task.
- Backs up DB automatically; archives pruned tasks to JSONL.

Examples:
  python3 roo_compact_state.py --scan-only \
    --db "$HOME/.config/Code/User/globalStorage/state.vscdb" \
    --ext-substr RooVeterinaryInc.roo-cline,saoudrizwan.claude-dev

  python3 roo_compact_state.py --db "$HOME/.config/Code/User/globalStorage/state.vscdb" \
    --keep 20 --max-bytes 200000 --messages-keep 15 --max-str 6000 \
    --ext-substr RooVeterinaryInc.roo-cline,saoudrizwan.claude-dev --verbose
"""
import argparse, json, os, sqlite3, sys, time, shutil
from pathlib import Path
from typing import List, Tuple, Any

def backup_db(db: Path) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    bak = db.with_name(f"{db.name}.bak.{ts}")
    shutil.copy2(db, bak)
    return bak

def decode(b):
    if isinstance(b, (bytes, bytearray)): return b.decode("utf-8", "ignore")
    return "" if b is None else str(b)

def bsize(obj: Any) -> int:
    try:
        return len(json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    except Exception:
        return 0

def find_taskhistory_nodes(root: Any):
    out = []
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == 'taskHistory' and isinstance(v, list):
                    out.append((node, k))
                walk(v)
        elif isinstance(node, list):
            for v in node: walk(v)
    walk(root)
    return out

def truncate_str(s: str, max_chars: int) -> str:
    if not isinstance(s, str) or len(s) <= max_chars: return s
    head = max_chars // 2 - 10
    tail = max_chars - head - 10
    return s[:max(0,head)] + " …[trimmed]… " + s[-max(0,tail):]

def scrub_large_fields(obj: Any, max_str_chars: int, messages_keep: int) -> None:
    def walk(node):
        if isinstance(node, dict):
            for k, v in list(node.items()):
                if isinstance(v, str):
                    node[k] = truncate_str(v, max_str_chars)
                elif isinstance(v, list):
                    if k in ('messages','chunks','diffs','edits','logs','history'):
                        if len(v) > messages_keep:
                            node[k] = v[-messages_keep:]
                    for i in range(len(node[k])): walk(node[k][i])
                elif isinstance(v, dict):
                    walk(v)
        elif isinstance(node, list):
            for i in range(len(node)): walk(node[i])
    walk(obj)

def shrink_taskhistory(parent: dict, key: str, keep: int, max_bytes: int, max_str_chars: int, messages_keep: int):
    changed = False
    pruned = []
    arr = parent.get(key, [])
    if not isinstance(arr, list): return False, []
    # Cap by count
    if len(arr) > keep:
        pruned.extend(arr[:-keep])
        parent[key] = arr[-keep:]
        arr = parent[key]
        changed = True
    # Scrub heavy fields first (cheaper than dropping more tasks)
    scrub_large_fields(arr, max_str_chars, messages_keep)
    # Then enforce byte budget on the whole JSON fragment
    while bsize(parent) > max_bytes and len(arr) > 1:
        pruned.append(arr.pop(0))
        changed = True
    # Final scrub
    scrub_large_fields(arr, max_str_chars, messages_keep)
    return changed, pruned

def process_db(db: Path, keep: int, max_bytes: int, max_str_chars: int, messages_keep: int,
               ext_filters: List[str], scan_only: bool, verbose: bool):
    con = sqlite3.connect(str(db))
    con.text_factory = bytes
    cur = con.cursor()
    try:
        rows = cur.execute("SELECT key, value FROM ItemTable").fetchall()
    except sqlite3.OperationalError:
        con.close(); return (0,0,0,0)
    changed_rows = archived = candidates = bytes_saved = 0
    archive_path = db.with_name("roo-taskHistory-archive.jsonl")
    did_backup = False
    for key_b, val_b in rows:
        key = decode(key_b); val = decode(val_b)
        if ext_filters:
            if not any(f.lower() in key.lower() for f in ext_filters) and '"taskHistory"' not in val:
                continue
        else:
            if '"taskHistory"' not in val:
                continue
        # Parse JSON value
        try:
            obj = json.loads(val)
        except Exception:
            continue
        nodes = find_taskhistory_nodes(obj)
        if not nodes: continue
        candidates += 1
        before = bsize(obj)
        total_pruned = []
        changed = False
        for parent, k in nodes:
            ch, pruned = shrink_taskhistory(parent, k, keep, max_bytes, max_str_chars, messages_keep)
            if ch: changed = True; total_pruned.extend(pruned)
        after = bsize(obj)
        if changed and after <= before:
            changed_rows += 1
            bytes_saved += (before - after)
            archived += len(total_pruned)
            if verbose:
                print(f"[+] {db}  key={key}  pruned_tasks={len(total_pruned)}  bytes_saved={before-after}")
            if not scan_only:
                if not did_backup:
                    backup_db(db); did_backup = True
                cur.execute("UPDATE ItemTable SET value=? WHERE key=?",
                            (json.dumps(obj, ensure_ascii=False, separators=(',',':')).encode('utf-8'), key.encode('utf-8')))
                with open(archive_path, "ab") as f:
                    for item in total_pruned:
                        f.write((json.dumps(item, ensure_ascii=False) + "\n").encode('utf-8'))
    if not scan_only and changed_rows:
        con.commit()
        try: cur.execute("VACUUM")
        except Exception: pass
    con.close()
    return (candidates, changed_rows, archived, bytes_saved)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=str, required=True, help="Path to state.vscdb to compact")
    ap.add_argument("--keep", type=int, default=50, help="Keep last N tasks (per taskHistory)")
    ap.add_argument("--max-bytes", type=int, default=300000, help="Target max bytes per row after compact")
    ap.add_argument("--max-str", type=int, default=8000, help="Max characters for any string field")
    ap.add_argument("--messages-keep", type=int, default=20, help="Keep last K items in message-like arrays per task")
    ap.add_argument("--ext-substr", type=str, default="", help="Comma-separated substrings to filter keys by (optional)")
    ap.add_argument("--scan-only", action="store_true", help="Scan/report only; no writes")
    ap.add_argument("--verbose", action="store_true", help="Verbose output")
    args = ap.parse_args()
    ext_filters = [s.strip() for s in args.ext_substr.split(",") if s.strip()]
    cand, changed, arch, saved = process_db(Path(args.db).expanduser(),
                                            args.keep, args.max_bytes, args.max_str, args.messages_keep,
                                            ext_filters, args.scan_only, args.verbose)
    mode = "SCAN" if args.scan_only else "COMPACT"
    print(f"[{mode}] candidates={cand} rows_changed={changed} items_archived={arch} bytes_saved={saved}")

if __name__ == "__main__":
    main()
