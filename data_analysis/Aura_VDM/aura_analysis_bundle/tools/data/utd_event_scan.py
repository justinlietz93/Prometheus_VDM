#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import os
import sys
import json
import argparse
import csv
import re
from typing import Iterable, List, Dict, Any, Tuple

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def _iter_event_files(paths: List[str], include_nexus: bool) -> Iterable[Tuple[str, str]]:
    """
    Yield (kind, path) where kind in {'utd','nexus'}.
    Scans directories recursively; if a file is passed, uses it directly.
    """
    for p in paths:
        p = os.path.abspath(p)
        if os.path.isfile(p):
            base = os.path.basename(p)
            if base == 'utd_events.jsonl':
                yield ('utd', p)
            elif include_nexus and base == 'events.jsonl':
                yield ('nexus', p)
            continue
        for root, dirs, files in os.walk(p):
            for fn in files:
                if fn == 'utd_events.jsonl':
                    yield ('utd', os.path.join(root, fn))
                elif include_nexus and fn == 'events.jsonl':
                    yield ('nexus', os.path.join(root, fn))

def _parse_json(line: str) -> Any:
    try:
        return json.loads(line)
    except Exception:
        return None

def _extract_from_utd(rec: Dict[str, Any], file_path: str) -> Dict[str, Any]:
    out = {}
    t = None
    val = None
    why = {}
    if isinstance(rec, dict) and rec.get('type') == 'macro':
        out['source'] = 'utd'
        out['kind'] = 'macro'
        out['macro'] = rec.get('macro')
        args = rec.get('args', {}) or {}
        out['text'] = args.get('text')
        why = args.get('why', {}) or {}
        t = why.get('t')
        val = why.get('sie_v2_valence_01', why.get('sie_valence_01'))
        out['score'] = rec.get('score')
    elif isinstance(rec, dict) and rec.get('type') == 'text':
        out['source'] = 'utd'
        out['kind'] = 'text'
        payload = rec.get('payload')
        out['payload'] = payload
        if isinstance(payload, dict):
            t = payload.get('t', None)
    else:
        return {}
    out['t'] = t
    out['valence'] = val
    out['file'] = file_path
    if isinstance(why, dict):
        for k in ('phase','b1_z','cohesion_components','vt_coverage','vt_entropy','connectome_entropy'):
            if k in why:
                out[k] = why[k]
    return out

def _extract_from_nexus(rec: Dict[str, Any], file_path: str) -> Dict[str, Any]:
    if not isinstance(rec, dict):
        return {}
    # structured logs may store event name in 'message' or 'event'
    msg = rec.get('message') or rec.get('event') or rec.get('name')
    extra = rec.get('extra') or rec.get('data') or {}
    if isinstance(extra, dict):
        extra = extra.get('extra', extra)
    out = {}
    if msg == 'speak_suppressed':
        out['source'] = 'nexus'
        out['kind'] = 'speak_suppressed'
        out['reason'] = (extra or {}).get('reason', 'unknown')
        out['valence'] = (extra or {}).get('val')
        out['threshold'] = (extra or {}).get('thresh')
        out['b1_z'] = (extra or {}).get('b1_z')
        out['t'] = (extra or {}).get('t')
        out['file'] = file_path
        return out
    return {}

def scan(paths: List[str], macro_names: List[str], include_text: bool, include_nexus: bool) -> List[Dict[str, Any]]:
    macro_set = set(macro_names or [])
    rows: List[Dict[str, Any]] = []
    for kind, fp in _iter_event_files(paths, include_nexus):
        try:
            with open(fp, 'r', encoding='utf-8') as fh:
                for line in fh:
                    rec = _parse_json(line)
                    if not rec:
                        continue
                    if kind == 'utd':
                        row = _extract_from_utd(rec, fp)
                        if not row:
                            continue
                        if row.get('kind') == 'macro':
                            if macro_set and row.get('macro') not in macro_set:
                                continue
                            rows.append(row)
                        elif row.get('kind') == 'text' and include_text:
                            rows.append(row)
                    elif kind == 'nexus':
                        row = _extract_from_nexus(rec, fp)
                        if row:
                            rows.append(row)
        except Exception as e:
            eprint(f"warn: failed to read {fp}: {e}")
    return rows

def emit_macro_board(rows: List[Dict[str, Any]], out_path: str):
    names = sorted(set(r.get('macro') for r in rows if r.get('kind') == 'macro' and r.get('macro')))
    board: Dict[str, Any] = {}
    for name in names:
        board[name] = {}
    try:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    except Exception:
        pass
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(board, fh, ensure_ascii=False, indent=2)

def emit_lexicon(rows: List[Dict[str, Any]], out_path: str, macro_filter: List[str] | None = None):
    tok_re = re.compile(r"[A-Za-z][A-Za-z0-9_+\-]*")
    counts: Dict[str, int] = {}
    mset = set(macro_filter or [])
    for r in rows:
        if r.get('kind') != 'macro':
            continue
        if mset and r.get('macro') not in mset:
            continue
        txt = r.get('text') or ""
        for w in tok_re.findall(str(txt)):
            lw = w.lower()
            counts[lw] = counts.get(lw, 0) + 1
    obj = {"tokens": [{"token": k, "count": v} for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]}
    try:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    except Exception:
        pass
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)

def write_ndjson(rows: List[Dict[str, Any]], fh):
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

def write_csv(rows: List[Dict[str, Any]], fh):
    fields = ['source','kind','macro','text','payload','t','valence','score','phase','b1_z','cohesion_components','vt_coverage','vt_entropy','connectome_entropy','file']
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k) for k in fields})

def main(argv=None):
    p = argparse.ArgumentParser(description="Scan UTD/Nexus logs for macro/text emissions")
    p.add_argument('paths', nargs='*', default=['.'], help="Run dir(s) or files to scan (default: .)")
    p.add_argument('--macro', dest='macro', action='append', help="Macro name to include (can repeat). Default: say")
    p.add_argument('--include-text', action='store_true', help="Include UTD text events (status payloads).")
    p.add_argument('--include-nexus', action='store_true', help="Also scan Nexus events.jsonl for speak_suppressed.")
    p.add_argument('--out', dest='out', default='-', help="Output file path or '-' for stdout (default).")
    p.add_argument('--format', dest='fmt', choices=['ndjson','csv'], default='ndjson', help="Output format.")
    p.add_argument('--emit-macro-board', dest='macro_board', help="Write aggregated macro_board.json to this path.")
    p.add_argument('--emit-lexicon', dest='lexicon', help="Write aggregated vocabulary JSON to this path.")
    args = p.parse_args(argv)

    macros = args.macro or ['say']
    rows = scan(args.paths, macros, args.include_text, args.include_nexus)
    rows.sort(key=lambda r: (r.get('t') is None, r.get('t')))

    if args.macro_board:
        try:
            emit_macro_board(rows, args.macro_board)
            eprint(f"macro board written: {args.macro_board}")
        except Exception as e:
            eprint(f"warn: failed to write macro board: {e}")

    if args.lexicon:
        try:
            emit_lexicon(rows, args.lexicon, macro_filter=macros)
            eprint(f"lexicon written: {args.lexicon}")
        except Exception as e:
            eprint(f"warn: failed to write lexicon: {e}")

    if args.out == '-' or args.out is None:
        outfh = sys.stdout
        close_fh = False
    else:
        outfh = open(args.out, 'w', encoding='utf-8', newline='' if args.fmt=='csv' else None)
        close_fh = True
    try:
        if args.fmt == 'csv':
            write_csv(rows, outfh)
        else:
            write_ndjson(rows, outfh)
    finally:
        if close_fh:
            outfh.close()

if __name__ == '__main__':
    main()