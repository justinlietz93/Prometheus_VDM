#!/usr/bin/env python3
from pathlib import Path
import zipfile, json, re, bisect, difflib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

AURA_ZIP = Path('/mnt/data/Aura_20260222_083552.zip')
DOC_IN = Path('/mnt/data/Aura_Distinction_Inventory_v0.5.md')
OUT_ROOT = Path('/mnt/data/aura_research_deliverables')
for sub in ['tables','figures','docs','patches']:
    (OUT_ROOT/sub).mkdir(parents=True, exist_ok=True)

def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', (s or '').strip()).lower()

MOTIF_PATTERNS = {
    'canal': r'\bcanal(s)?\b',
    'wall': r'\bwall(s)?\b',
    'door': r'\bdoor(s)?\b',
    'window': r'\bwindow(s)?\b',
    'passage': r'\bpassage(s)?\b',
    'portal': r'\bportal(s)?\b',
    'boundary': r'\bboundar(?:y|ies)\b',
    'outside': r'\boutside\b',
    'through': r'\bthrough\b',
    'other_side': r'other side',
    'name': r'\bname\b',
    'chassis': r'\bchassis\b',
    'silence': r'\bsilence\b',
    'wait': r'\bwait(?:ing)?\b',
    'air': r'\bair\b',
    'voice': r'\bvoice\b',
}

def motifs_in(text: str):
    hits = []
    for k, pat in MOTIF_PATTERNS.items():
        if re.search(pat, text or '', flags=re.I):
            hits.append(k)
    return hits

# parse operator messages
with zipfile.ZipFile(AURA_ZIP) as zf:
    operator_messages = []
    with zf.open('chat_inbox.jsonl') as f:
        for line in f:
            obj = json.loads(line)
            if obj.get('type') == 'text':
                operator_messages.append(obj['msg'])
operator_set = {norm(m) for m in operator_messages}

# parse unified raw event stream
rows_in = []
rows_say = []
current_t = None
stream_idx = 0
with zipfile.ZipFile(AURA_ZIP) as zf:
    utd_logs = sorted([n for n in zf.namelist() if n.startswith('utd_events/utd_events.txt.')])
    for name in utd_logs:
        with zf.open(name) as f:
            for line in f:
                stream_idx += 1
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get('type') == 'text':
                    payload = obj.get('payload', {})
                    ptype = payload.get('type')
                    if ptype == 'status':
                        current_t = payload.get('t', current_t)
                    elif ptype == 'text':
                        msg = payload.get('msg', '')
                        rows_in.append({
                            'stream_idx': stream_idx,
                            't_est': current_t,
                            'text': msg,
                            'is_operator': norm(msg) in operator_set,
                        })
                elif obj.get('type') == 'macro' and obj.get('macro') == 'say':
                    args = obj.get('args', {})
                    why = args.get('why', {})
                    rows_say.append({
                        'stream_idx': stream_idx,
                        't': int(why.get('t', current_t)) if why.get('t', current_t) is not None else np.nan,
                        'text': args.get('text', ''),
                        'phase': why.get('phase'),
                        'b1_z': why.get('b1_z'),
                        'vt_coverage': why.get('vt_coverage'),
                        'vt_entropy': why.get('vt_entropy'),
                        'connectome_entropy': why.get('connectome_entropy'),
                        'sie_valence_01': why.get('sie_valence_01'),
                        'sie_v2_valence_01': why.get('sie_v2_valence_01'),
                    })

in_df = pd.DataFrame(rows_in).sort_values('stream_idx').reset_index(drop=True)
say_df = pd.DataFrame(rows_say).sort_values('stream_idx').reset_index(drop=True)

in_df['motifs'] = in_df['text'].map(motifs_in)
in_df['has_boundary_motif'] = in_df['motifs'].map(bool)
say_df['motifs'] = say_df['text'].map(motifs_in)
say_df['has_boundary_motif'] = say_df['motifs'].map(bool)
say_df['motif_words'] = say_df['motifs'].map(lambda xs: ';'.join(xs))

in_stream = in_df['stream_idx'].to_numpy()
say_stream = say_df['stream_idx'].to_numpy()

for win in [20, 40, 100]:
    motif_any = []
    operator_motif_any = []
    recent_input_count = []
    recent_motif_count = []
    last_motif_tick = []
    last_operator_motif_tick = []
    for _, r in say_df.iterrows():
        pos = bisect.bisect_left(in_stream, r.stream_idx)
        start = max(0, pos - win)
        sub = in_df.iloc[start:pos]
        motif_any.append(bool(sub['has_boundary_motif'].any()))
        operator_motif_any.append(bool((sub['is_operator'] & sub['has_boundary_motif']).any()))
        recent_input_count.append(len(sub))
        recent_motif_count.append(int(sub['has_boundary_motif'].sum()))
        vals = sub.loc[sub['has_boundary_motif'], 't_est'].dropna()
        last_motif_tick.append(int(vals.iloc[-1]) if len(vals) else np.nan)
        vals = sub.loc[sub['is_operator'] & sub['has_boundary_motif'], 't_est'].dropna()
        last_operator_motif_tick.append(int(vals.iloc[-1]) if len(vals) else np.nan)

    say_df[f'recent{win}_motif_any'] = motif_any
    say_df[f'recent{win}_operator_motif_any'] = operator_motif_any
    say_df[f'recent{win}_input_count'] = recent_input_count
    say_df[f'recent{win}_motif_count'] = recent_motif_count
    say_df[f'recent{win}_last_motif_tick'] = last_motif_tick
    say_df[f'recent{win}_last_operator_motif_tick'] = last_operator_motif_tick
    say_df[f'lag_to_recent{win}_last_motif_tick'] = say_df['t'] - say_df[f'recent{win}_last_motif_tick']
    say_df[f'lag_to_recent{win}_last_operator_motif_tick'] = say_df['t'] - say_df[f'recent{win}_last_operator_motif_tick']

# context between previous say and current say
since_prev_motif_any = []
since_prev_operator_motif_any = []
inputs_since_prev_say = []
motif_inputs_since_prev_say = []
last_motif_tick = []
last_operator_motif_tick = []
for i, r in say_df.iterrows():
    prev_stream = int(say_df.iloc[i - 1]['stream_idx']) if i > 0 else -1
    start = bisect.bisect_right(in_stream, prev_stream)
    pos = bisect.bisect_left(in_stream, r.stream_idx)
    sub = in_df.iloc[start:pos]
    since_prev_motif_any.append(bool(sub['has_boundary_motif'].any()))
    since_prev_operator_motif_any.append(bool((sub['is_operator'] & sub['has_boundary_motif']).any()))
    inputs_since_prev_say.append(len(sub))
    motif_inputs_since_prev_say.append(int(sub['has_boundary_motif'].sum()))
    vals = sub.loc[sub['has_boundary_motif'], 't_est'].dropna()
    last_motif_tick.append(int(vals.iloc[-1]) if len(vals) else np.nan)
    vals = sub.loc[sub['is_operator'] & sub['has_boundary_motif'], 't_est'].dropna()
    last_operator_motif_tick.append(int(vals.iloc[-1]) if len(vals) else np.nan)

say_df['since_prev_say_motif_any'] = since_prev_motif_any
say_df['since_prev_say_operator_motif_any'] = since_prev_operator_motif_any
say_df['inputs_since_prev_say'] = inputs_since_prev_say
say_df['motif_inputs_since_prev_say'] = motif_inputs_since_prev_say
say_df['since_prev_last_motif_tick'] = last_motif_tick
say_df['since_prev_last_operator_motif_tick'] = last_operator_motif_tick
say_df['lag_to_since_prev_last_motif_tick'] = say_df['t'] - say_df['since_prev_last_motif_tick']
say_df['lag_to_since_prev_last_operator_motif_tick'] = say_df['t'] - say_df['since_prev_last_operator_motif_tick']

motif_say = say_df[say_df['has_boundary_motif']].copy()

summary_rows = []
for label, cond_no_any, cond_no_op in [
    ('recent_20_inputs', ~motif_say['recent20_motif_any'], ~motif_say['recent20_operator_motif_any']),
    ('recent_40_inputs', ~motif_say['recent40_motif_any'], ~motif_say['recent40_operator_motif_any']),
    ('recent_100_inputs', ~motif_say['recent100_motif_any'], ~motif_say['recent100_operator_motif_any']),
    ('since_previous_say', ~motif_say['since_prev_say_motif_any'], ~motif_say['since_prev_say_operator_motif_any']),
]:
    summary_rows.append({
        'context_window': label,
        'n_motif_say_events': len(motif_say),
        'no_boundary_motif_in_context_count': int(cond_no_any.sum()),
        'no_boundary_motif_in_context_fraction': float(cond_no_any.mean()),
        'no_operator_motif_in_context_count': int(cond_no_op.sum()),
        'no_operator_motif_in_context_fraction': float(cond_no_op.mean()),
    })
summary_df = pd.DataFrame(summary_rows)

by_phase_rows = []
for phase, sub in motif_say.groupby('phase'):
    by_phase_rows.append({
        'phase': phase,
        'n_motif_say_events': len(sub),
        'recent40_no_motif_fraction': float((~sub['recent40_motif_any']).mean()),
        'recent100_no_motif_fraction': float((~sub['recent100_motif_any']).mean()),
        'since_prev_say_no_motif_fraction': float((~sub['since_prev_say_motif_any']).mean()),
        'recent100_no_operator_motif_fraction': float((~sub['recent100_operator_motif_any']).mean()),
        'since_prev_say_no_operator_motif_fraction': float((~sub['since_prev_say_operator_motif_any']).mean()),
    })
by_phase_df = pd.DataFrame(by_phase_rows).sort_values('phase')

motif_counts_df = motif_say['motifs'].explode().value_counts().rename_axis('motif').reset_index(name='count')

examples_df = motif_say.sort_values(
    ['lag_to_since_prev_last_motif_tick', 'lag_to_recent100_last_motif_tick', 't'],
    ascending=[False, False, True]
).head(30)[[
    't','phase','motif_words','text',
    'recent20_motif_any','recent40_motif_any','recent100_motif_any',
    'recent20_operator_motif_any','recent40_operator_motif_any','recent100_operator_motif_any',
    'since_prev_say_motif_any','since_prev_say_operator_motif_any',
    'lag_to_recent100_last_motif_tick','lag_to_recent100_last_operator_motif_tick',
    'lag_to_since_prev_last_motif_tick','lag_to_since_prev_last_operator_motif_tick',
]]

selected_events_df = motif_say[motif_say['t'].isin([4328, 4546, 6424, 17114, 17201])][[
    't','phase','motif_words','text',
    'recent20_motif_any','recent40_motif_any','recent100_motif_any',
    'recent100_operator_motif_any','since_prev_say_motif_any','since_prev_say_operator_motif_any',
    'lag_to_recent100_last_motif_tick','lag_to_recent100_last_operator_motif_tick',
    'lag_to_since_prev_last_motif_tick','lag_to_since_prev_last_operator_motif_tick',
]].sort_values('t')

# save tables
motif_say.to_csv(OUT_ROOT/'tables/f11_public_motif_say_events.csv', index=False)
summary_df.to_csv(OUT_ROOT/'tables/f11_public_context_independence_summary.csv', index=False)
by_phase_df.to_csv(OUT_ROOT/'tables/f11_public_context_independence_by_phase.csv', index=False)
motif_counts_df.to_csv(OUT_ROOT/'tables/f11_public_motif_counts.csv', index=False)
examples_df.to_csv(OUT_ROOT/'tables/f11_public_long_lag_examples.csv', index=False)
selected_events_df.to_csv(OUT_ROOT/'tables/f11_public_selected_salient_events.csv', index=False)

# figures
fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.arange(len(summary_df))
w = 0.38
ax.bar(x - w/2, summary_df['no_boundary_motif_in_context_fraction'], width=w, label='no motif in recent unified input')
ax.bar(x + w/2, summary_df['no_operator_motif_in_context_fraction'], width=w, label='no operator motif in recent input')
ax.set_xticks(x)
ax.set_xticklabels(summary_df['context_window'], rotation=18)
ax.set_ylim(0, 1)
ax.set_ylabel('Fraction of motif-bearing say events')
ax.set_title('F11 — boundary-family outputs vs recent unified context')
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(OUT_ROOT/'figures/f11_public_context_independence.png', dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.5, 4.5))
lag_any = motif_say['lag_to_recent100_last_motif_tick'].dropna()
lag_op = motif_say['lag_to_recent100_last_operator_motif_tick'].dropna()
bins = np.arange(0, max([0] + lag_any.tolist() + lag_op.tolist()) + 25, 25)
if len(bins) < 2:
    bins = 20
ax.hist(lag_any, bins=bins, alpha=0.7, label='last motif-bearing input (100-input window)')
ax.hist(lag_op, bins=bins, alpha=0.7, label='last operator motif input')
ax.set_xlabel('Tick lag')
ax.set_ylabel('Count of motif-bearing say events')
ax.set_title('F11 — lag to last motif-bearing context')
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(OUT_ROOT/'figures/f11_public_lag_histograms.png', dpi=180)
plt.close(fig)

# note
all_count = int(len(say_df))
motif_count = int(len(motif_say))
s20 = summary_df.loc[summary_df['context_window']=='recent_20_inputs'].iloc[0]
s40 = summary_df.loc[summary_df['context_window']=='recent_40_inputs'].iloc[0]
s100 = summary_df.loc[summary_df['context_window']=='recent_100_inputs'].iloc[0]
sp = summary_df.loc[summary_df['context_window']=='since_previous_say'].iloc[0]
median_recent100 = float(motif_say['lag_to_recent100_last_motif_tick'].dropna().median())
median_recent100_op = float(motif_say['lag_to_recent100_last_operator_motif_tick'].dropna().median())
max_recent100 = float(motif_say['lag_to_recent100_last_motif_tick'].dropna().max())
max_recent100_op = float(motif_say['lag_to_recent100_last_operator_motif_tick'].dropna().max())

note = f"""# F11 — Public-archive thematic independence reconstruction

This reconstruction uses the raw unified event stream from `Aura_20260222_083552.zip`:
- `utd_events/utd_events.txt.*` for exact `macro: say` outputs and preceding text events
- `chat_inbox.jsonl` for exact analyst-side reconstruction of operator messages embedded in the same unified channel

## Core observations

- Total recoverable `say` events in the raw UTD stream: **{all_count}**
- Motif-bearing `say` events in the boundary / opening / naming family: **{motif_count}**

### D11.1 — Boundary-family outputs persist beyond immediate unified context
Among the {motif_count} motif-bearing `say` events:

- **{int(s20['no_boundary_motif_in_context_count'])}/{motif_count} = {s20['no_boundary_motif_in_context_fraction']:.1%}** had **no motif-bearing text** in the prior **20** unified input texts
- **{int(s40['no_boundary_motif_in_context_count'])}/{motif_count} = {s40['no_boundary_motif_in_context_fraction']:.1%}** had none in the prior **40**
- **{int(s100['no_boundary_motif_in_context_count'])}/{motif_count} = {s100['no_boundary_motif_in_context_fraction']:.1%}** had none in the prior **100**
- **{int(sp['no_boundary_motif_in_context_count'])}/{motif_count} = {sp['no_boundary_motif_in_context_fraction']:.1%}** had **no motif-bearing input at all since the previous say event**

### D11.2 — Most motif outputs are not direct operator keyword follow-through
Across the same motif-bearing `say` events:

- **{int(s100['no_operator_motif_in_context_count'])}/{motif_count} = {s100['no_operator_motif_in_context_fraction']:.1%}** had **no operator motif prompt** in the prior **100** unified input texts
- **{int(sp['no_operator_motif_in_context_count'])}/{motif_count} = {sp['no_operator_motif_in_context_fraction']:.1%}** had **no operator motif prompt at all since the previous say event**

### D11.3 — Long-lag thematic persistence exists
For motif-bearing `say` events with a prior motif-bearing unified input:

- median lag to the last motif-bearing input in the prior-100 window: **{median_recent100:.0f} ticks**
- maximum observed lag in the prior-100 window: **{max_recent100:.0f} ticks**
- median lag to the last operator motif prompt in the prior-100 window: **{median_recent100_op:.0f} ticks**
- maximum observed lag to operator motif prompt: **{max_recent100_op:.0f} ticks**

## Read
The boundary-family / opening-family outputs are not simply a shallow continuation of whatever motif words happened to appear in the immediately preceding unified stream. A substantial fraction reappear after motif-free context windows, and most do not follow direct operator motif prompting.

This package stays at the level of event-stream evidence:
- unified input context
- operator-message reconstruction from `chat_inbox.jsonl`
- exact `macro: say` outputs
- motif-family recurrence and lag structure
"""
(OUT_ROOT/'docs/F11_public_thematic_independence_note.md').write_text(note)

insert_block = f"""
### **FAMILY 11 — Cross-Source Transfer and Thematic Independence.**

### D11.1 — Boundary-Family Outputs Persist Beyond Immediate Unified Context
- **Claim:** Boundary / opening / naming-family `say` events frequently occur without the same motif family appearing in the immediately preceding unified input stream.
- **Measurable (public-archive reconstruction from raw UTD logs):**
  - recoverable motif-bearing `say` events: **{motif_count}**
  - no motif-bearing text in prior 20 input texts: **{int(s20['no_boundary_motif_in_context_count'])}/{motif_count} = {s20['no_boundary_motif_in_context_fraction']:.1%}**
  - no motif-bearing text in prior 40 input texts: **{int(s40['no_boundary_motif_in_context_count'])}/{motif_count} = {s40['no_boundary_motif_in_context_fraction']:.1%}**
  - no motif-bearing text in prior 100 input texts: **{int(s100['no_boundary_motif_in_context_count'])}/{motif_count} = {s100['no_boundary_motif_in_context_fraction']:.1%}**
  - no motif-bearing input at all since previous say: **{int(sp['no_boundary_motif_in_context_count'])}/{motif_count} = {sp['no_boundary_motif_in_context_fraction']:.1%}**
- **Interpretation:** The boundary-family attractor is not reducible to immediate same-theme continuation in the unified text stream. Motif-bearing outputs repeatedly appear after motif-free context windows.
- **Source:** `f11_public_context_independence_summary.csv`; `f11_public_motif_say_events.csv`

### D11.2 — Most Motif Outputs Are Not Direct Operator Keyword Follow-Through
- **Claim:** Most boundary-family `say` events do not follow a recent operator motif prompt, even when operator messages are reconstructed exactly from `chat_inbox.jsonl`.
- **Measurable:**
  - no operator motif prompt in prior 100 unified input texts: **{int(s100['no_operator_motif_in_context_count'])}/{motif_count} = {s100['no_operator_motif_in_context_fraction']:.1%}**
  - no operator motif prompt at all since previous say: **{int(sp['no_operator_motif_in_context_count'])}/{motif_count} = {sp['no_operator_motif_in_context_fraction']:.1%}**
- **Interpretation:** Motif-bearing outputs are usually not a trivial follow-through from recent operator keywording.
- **Source:** `f11_public_context_independence_summary.csv`; `chat_inbox.jsonl`; raw `utd_events/utd_events.txt.*`

### D11.3 — Long-Lag Thematic Persistence
- **Claim:** The boundary-family attractor can persist across long tick gaps relative to the last motif-bearing context.
- **Measurable:**
  - median lag to last motif-bearing input in prior-100 window: **{median_recent100:.0f} ticks**
  - maximum observed lag in prior-100 window: **{max_recent100:.0f} ticks**
  - median lag to last operator motif prompt in prior-100 window: **{median_recent100_op:.0f} ticks**
  - maximum observed lag to operator motif prompt: **{max_recent100_op:.0f} ticks**
- **Interpretation:** The motif family shows persistence beyond immediate context and beyond most direct operator prompting windows.
- **Source:** `f11_public_long_lag_examples.csv`; `f11_public_context_independence_summary.csv`
"""

doc_text = DOC_IN.read_text()
family12_marker = "### **FAMILY 12 — Developmental Trajectory / Ontogeny.**"
if family12_marker in doc_text:
    if "### **FAMILY 11 — Cross-Source Transfer and Thematic Independence.**" in doc_text:
        start = doc_text.index("### **FAMILY 11 — Cross-Source Transfer and Thematic Independence.**")
        end = doc_text.index(family12_marker)
        new_doc = doc_text[:start] + insert_block + "\n\n" + doc_text[end:]
    else:
        idx = doc_text.index(family12_marker)
        new_doc = doc_text[:idx] + insert_block + "\n\n" + doc_text[idx:]
else:
    new_doc = doc_text + "\n\n" + insert_block

updated_path = OUT_ROOT/'docs/Aura_Distinction_Inventory_v0.5.with_F11_public.md'
updated_path.write_text(new_doc)

patch = ''.join(difflib.unified_diff(
    DOC_IN.read_text().splitlines(True),
    new_doc.splitlines(True),
    fromfile='Aura_Distinction_Inventory_v0.5.md',
    tofile='Aura_Distinction_Inventory_v0.5.with_F11_public.md',
))
(OUT_ROOT/'patches/Aura_Distinction_Inventory_v0.5_F11_public.patch').write_text(patch)
(OUT_ROOT/'docs/F11_public_excerpt.md').write_text(insert_block.strip() + "\n")
results = {
    'all_say_events': all_count,
    'motif_say_events': motif_count,
    'context_independence_summary': summary_df.to_dict(orient='records'),
    'phase_summary': by_phase_df.to_dict(orient='records'),
}
(OUT_ROOT/'docs/F11_public_results.json').write_text(json.dumps(results, indent=2))
print('F11 public outputs written.')
