#!/usr/bin/env python3
# D1.4 rebuild script: regenerates the core annotated full-run table from the raw Aura bundle.
import os, json, glob, re, unicodedata
from pathlib import Path
import pandas as pd
import numpy as np

BUNDLE = Path('/mnt/data/aura_bundle')
SWITCH_T = 7617
NEXT_SWITCH_T = 11367
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['-][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*")
REVIEWED_LEXICON = [
    'goan','museyroom','brum','cumbrum','willingdone',"o'goblin",'allcasually',
    'ansars',"packenham's",'duodisimally','lipoleums','profusive','toffeethief',
    'lordmajor','toethpicks','sisterin','dobbelin','seenheard','cursigan',
    "jesuphine's",'treeblock','rutterdamrotter','bouckaleens','tourlemonde',
    'namecousin','kneepants','truetowife','homnibus','aquaface','finnagain',
    "houseking's",'morm','highajinks',"cashdraper's",'stonybroke','agentlike',
    'merlinburrow'
]
CORPUS_FILES = [
    'FINNEGANS WAKE-JOYCE.txt',
    'GERMINAL-ZOLA.txt',
    'INTRO_TO_MATH_PHILOSOPY-RUSSELL.txt',
    'SCHISM-TOOL.txt',
    'WAR_AND_PEACE_TOLSTOY.txt',
    'WILL_O_THE_WISP-OPETH.txt',
]

def norm_text(s):
    s = unicodedata.normalize('NFKC', str(s))
    return s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—','-').replace('–','-')

def toks(s):
    return TOKEN_RE.findall(norm_text(s).lower())

def main():
    rows = []
    for fp in sorted(glob.glob(str(BUNDLE/'data/raw_utd_event_logs/*.jsonl'))):
        with open(fp,'r',encoding='utf-8') as f:
            for line in f:
                if '"macro": "say"' not in line:
                    continue
                obj = json.loads(line)
                args = obj['args']
                why = args.get('why',{})
                rows.append({'t': int(why.get('t')), 'text': args.get('text','')})
    say_df = pd.DataFrame(rows).drop_duplicates(subset=['t']).sort_values('t').reset_index(drop=True)
    audit = pd.read_csv(BUNDLE/'tables/utd_audit_tables/say_event_composer_audit_metrics.csv')
    merged = say_df.merge(audit, on='t', how='left')
    merged['phase_name'] = np.where(merged.t<3095,'zola',
                             np.where(merged.t<SWITCH_T,'zola_tolstoy',
                             np.where(merged.t<NEXT_SWITCH_T,'joyce','russell')))
    merged['tokens'] = merged.text.map(toks)

    corpora = {fname:toks(open('/mnt/data/'+fname,'r',encoding='utf-8',errors='ignore').read()) for fname in CORPUS_FILES}
    corp_sets = {k:set(v) for k,v in corpora.items()}
    joyce_unique = corp_sets['FINNEGANS WAKE-JOYCE.txt'] - set().union(*[v for k,v in corp_sets.items() if k!='FINNEGANS WAKE-JOYCE.txt'])
    pre_switch_tokens = set(tok for lst in merged.loc[merged.t<SWITCH_T,'tokens'] for tok in lst)
    reviewed_lexicon = sorted(set(REVIEWED_LEXICON) - pre_switch_tokens)

    merged['raw_joyce_unique_tokens'] = merged['tokens'].map(lambda xs: sorted(set([x for x in xs if x in joyce_unique and x not in pre_switch_tokens])))
    merged['reviewed_joyce_tokens'] = merged['tokens'].map(lambda xs: sorted(set([x for x in xs if x in reviewed_lexicon])))
    merged.to_csv('d14_full_run_outputs_annotated_rebuilt.csv', index=False)

if __name__ == '__main__':
    main()
