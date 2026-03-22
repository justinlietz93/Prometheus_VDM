from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from common import ensure_dir, load_utd_events, flatten_macro_events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--utd_dir', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out = ensure_dir(args.out)
    utd_dir = Path(args.utd_dir)
    files = sorted([p for p in utd_dir.iterdir() if p.is_file()])
    df = load_utd_events(files)
    df['type'] = df['type'].astype(str)
    df['payload_type'] = df['payload'].apply(lambda x: x.get('type') if isinstance(x, dict) else None)
    df['macro_name'] = df['macro'].astype(str) if 'macro' in df.columns else None
    df.groupby('type').size().reset_index(name='count').to_csv(out/'utd_event_type_counts.csv', index=False)
    flat = flatten_macro_events(df[df['type']=='macro'])
    flat.to_csv(out/'utd_macro_events_flat.csv', index=False)
    say = flat[flat['macro']=='say'].copy()
    if len(say):
        pd.DataFrame(say[['why_phase']].value_counts().reset_index(name='count')).rename(columns={'why_phase':'phase'}).to_csv(out/'utd_say_phase_counts.csv', index=False)
        say.describe(include='all').to_csv(out/'utd_say_macro_summary.csv', index=True)
    else:
        pd.DataFrame(columns=['phase','count']).to_csv(out/'utd_say_phase_counts.csv', index=False)
        pd.DataFrame().to_csv(out/'utd_say_macro_summary.csv', index=False)

if __name__ == '__main__':
    main()
