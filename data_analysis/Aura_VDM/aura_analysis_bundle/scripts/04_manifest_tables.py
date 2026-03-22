from __future__ import annotations
import argparse, os
from pathlib import Path
import pandas as pd
from common import ensure_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aura_dir', required=True)
    ap.add_argument('--metric_inventory', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out = ensure_dir(args.out)
    aura_dir = Path(args.aura_dir)
    rows=[]
    for p in sorted(aura_dir.rglob('*')):
        if p.is_file():
            rel = p.relative_to(aura_dir)
            group = rel.parts[0] if len(rel.parts)>1 else 'root'
            rows.append({'group':group,'path':str(rel),'bytes':p.stat().st_size,'ext':p.suffix.lower()})
    inv = pd.DataFrame(rows)
    inv.to_csv(out/'artifact_inventory_by_group.csv', index=False)
    inv.groupby('group').agg(files=('path','count'), bytes=('bytes','sum')).reset_index().to_csv(out/'run_package_manifest_summary.csv', index=False)
    corpus = []
    corpus_dir = aura_dir/'corpus'
    if corpus_dir.exists():
        for p in sorted(corpus_dir.iterdir()):
            if p.is_file():
                corpus.append({'filename':p.name,'bytes':p.stat().st_size,'include_fulltext_public_package':'depends_on_rights_clearance'})
    pd.DataFrame(corpus).to_csv(out/'corpus_manifest.csv', index=False)
    mi = pd.read_csv(args.metric_inventory)
    keep = ['metric_name','category','present_in_events_jsonl','present_in_utd_events','present_in_h5_state','present_in_code','planned_addition','description','notes']
    mi[[c for c in keep if c in mi.columns]].to_csv(out/'metric_inventory_filtered.csv', index=False)

if __name__ == '__main__':
    main()
