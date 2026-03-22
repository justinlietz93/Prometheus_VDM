from pathlib import Path
import re, shutil
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image

ROOT = Path('/mnt/data/aura_fig_work')
OUT = ROOT / 'publication'
FIG = OUT / 'figures'
TAB = OUT / 'tables'
SCR = OUT / 'scripts'
for d in [OUT, FIG, TAB, SCR]:
    d.mkdir(parents=True, exist_ok=True)

# copy self for reproducibility
shutil.copy2(__file__, SCR / 'make_publication_figures.py')

# data sources
TICK = pd.read_csv(ROOT / 'tick_table_full.csv.gz', compression='gzip')
SAY_AUDIT = pd.read_csv(ROOT / 'utd_audit/tables/say_event_composer_audit_metrics.csv')
EXCH = Path('/mnt/data/aura_justin_exchange (2).md')
if not EXCH.exists():
    EXCH = Path('/mnt/data/aura_justin_exchange.md')
TXT = EXCH.read_text(errors='ignore').splitlines()
justin_ticks = []
aura_ticks = []
cur_t = None
for line in TXT:
    m = re.search(r'\[t=\s*(\d+)\]', line)
    if m:
        cur_t = int(m.group(1))
    if 'Justin:' in line and cur_t is not None:
        justin_ticks.append(cur_t)
    if 'Aura:' in line and cur_t is not None:
        aura_ticks.append(cur_t)


def add_event_lines(ax, x_min=None, x_max=None):
    for t in justin_ticks:
        if (x_min is None or t >= x_min) and (x_max is None or t <= x_max):
            ax.axvline(t, color='0.55', lw=0.6, alpha=0.35)
    say_ticks = TICK.loc[TICK.get('did_say', 0).astype(bool), 't'].to_numpy()
    if len(say_ticks):
        y0, y1 = ax.get_ylim()
        for t in say_ticks:
            if (x_min is None or t >= x_min) and (x_max is None or t <= x_max):
                ax.axvline(t, color='#d62728', lw=0.6, alpha=0.35)
        ax.set_ylim(y0, y1)


# Figure 1: dashboard-target metrics panel
metrics = [
    ('connectome_entropy', 'Conn. Entropy', 'bits'),
    ('vt_entropy', 'VT Entropy', 'bits'),
    ('sie_v2_valence_01', 'SIE v2', 'valence'),
    ('vt_coverage', 'VT Coverage', 'fraction'),
    ('active_edges', 'Active Edges', 'count'),
    ('b1_z', 'Boundary Pulse (b1_z)', 'z-score'),
    ('adc_territories', 'ADC Territories', 'count'),
]
fig = plt.figure(figsize=(13, 11), constrained_layout=True)
gs = GridSpec(4, 2, figure=fig)
for i, (col, title, ylabel) in enumerate(metrics):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    ax.plot(TICK['t'], TICK[col], lw=1.4)
    ax.set_title(title, fontsize=11)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    add_event_lines(ax, TICK['t'].min(), TICK['t'].max())
    if i // 2 == 3:
        ax.set_xlabel('tick')
fig.suptitle('Aura dashboard-target metrics across late run window\n(gray = Justin input ticks; red = Aura say ticks)', fontsize=14)
fig.savefig(FIG / 'aura_dashboard_target_panels_publication.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 2: lock-in second half
sel = TICK[(TICK['t'] >= 13500) & (TICK['t'] <= 17455)].copy()
fig, axes = plt.subplots(4, 1, figsize=(13, 10), sharex=True, constrained_layout=True)
series = [('active_edges', 'Active Edges'), ('connectome_entropy', 'Connectome Entropy'), ('sie_v2_valence_01', 'SIE v2 valence'), ('b1_z', 'Boundary Pulse b1_z')]
for ax, (col, title) in zip(axes, series):
    ax.plot(sel['t'], sel[col], lw=1.5)
    ax.set_ylabel(title)
    ax.grid(alpha=0.25)
    add_event_lines(ax, sel['t'].min(), sel['t'].max())
axes[-1].set_xlabel('tick')
fig.suptitle('Second-half lock-in and punctuated reply regime', fontsize=14)
fig.savefig(FIG / 'aura_lockin_second_half_publication.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 3: terminal window
sel = TICK[(TICK['t'] >= 16900) & (TICK['t'] <= 17455)].copy()
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
for ax, col in zip(axes, ['active_edges', 'connectome_entropy', 'b1_z']):
    ax.plot(sel['t'], sel[col], lw=1.6)
    ax.grid(alpha=0.25)
    add_event_lines(ax, sel['t'].min(), sel['t'].max())
    for t in justin_ticks:
        if sel['t'].min() <= t <= sel['t'].max():
            ax.text(t, ax.get_ylim()[1], f'{t}', fontsize=7, rotation=90, va='top', alpha=0.5)
axes[0].set_ylabel('active_edges')
axes[1].set_ylabel('conn_entropy')
axes[2].set_ylabel('b1_z')
axes[2].set_xlabel('tick')
fig.suptitle('Terminal transition window before crash', fontsize=14)
fig.savefig(FIG / 'aura_terminal_transition_publication.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 4: four proofs plate
proof_paths = [
    ROOT / 'four_proofs/figures/proof1_hub_recurrence_jaccard.png',
    ROOT / 'four_proofs/figures/proof2_psd_active_edges_steady.png',
    ROOT / 'four_proofs/figures/proof2_avalanche_size_ccdf_active_edges.png',
    ROOT / 'four_proofs/figures/proof3_free_energy_landscape_kde.png',
    ROOT / 'four_proofs/figures/proof4_fisher_speed_hellinger.png',
]
labels = ['Hub recurrence', 'PSD of active edges', 'Avalanche size CCDF', 'Free-energy landscape', 'Fisher speed / Hellinger']
fig, axes = plt.subplots(3, 2, figsize=(12, 13), constrained_layout=True)
for ax, p, lbl in zip(axes.flat, proof_paths, labels):
    img = Image.open(p)
    ax.imshow(img)
    ax.set_title(lbl, fontsize=11)
    ax.axis('off')
axes.flat[-1].axis('off')
fig.suptitle('Aura late-run four-proofs figures generated by legacy analysis script', fontsize=14)
fig.savefig(FIG / 'aura_four_proofs_plate.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 5: connectome geometry plate
states = ['17160', '17220', '17280', '17340', '17400']
fig = plt.figure(figsize=(14, 14), constrained_layout=True)
gs = GridSpec(len(states), 3, figure=fig)
for i, st in enumerate(states):
    for j, (kind, title) in enumerate([('embedding_scatter_community', 'Embedding / communities'), ('baseline_pi_heatmap', 'Projection heatmap'), ('degree_ccdf_loglog', 'Degree CCDF')]):
        ax = fig.add_subplot(gs[i, j])
        if kind == 'baseline_pi_heatmap':
            p = ROOT / f'connectome_geom/plots/{kind}_state_{st}_32x32.png'
        else:
            p = ROOT / f'connectome_geom/plots/{kind}_state_{st}.png'
        img = Image.open(p)
        ax.imshow(img)
        if i == 0:
            ax.set_title(title, fontsize=10)
        ax.set_ylabel(f'state {st}', fontsize=9)
        ax.axis('off')
fig.suptitle('Aura late H5 geometry across snapshots (legacy geometry script outputs)', fontsize=14)
fig.savefig(FIG / 'aura_connectome_geometry_plate.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 6: scalar / macrostate plate
paths = [
    ROOT / 'scalar_struct/figures/b1_z_with_spikes_and_say.png',
    ROOT / 'scalar_struct/figures/macro_input_say.png',
    ROOT / 'scalar_struct/figures/eta_macrotrans_active_edges.png',
    ROOT / 'scalar_struct/figures/eta_say_b1_z.png',
]
labels = ['b1_z with spikes and say', 'Macrostate / input / say', 'ETA around macro transitions', 'ETA around say events']
fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
for ax, p, lbl in zip(axes.flat, paths, labels):
    img = Image.open(p)
    ax.imshow(img)
    ax.set_title(lbl, fontsize=11)
    ax.axis('off')
fig.suptitle('Aura scalar/macrostate diagnostics from legacy log-analysis script', fontsize=14)
fig.savefig(FIG / 'aura_scalar_macrostate_plate.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 7: UTD composer audit plate
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), constrained_layout=True)
for ax, p, lbl in zip(axes[:2], [ROOT / 'utd_audit/figures/trigram_fraction_hist.png', ROOT / 'utd_audit/figures/lcs_contiguous_len_hist.png'], ['Trigram reuse', 'Contiguous overlap length']):
    img = Image.open(p)
    ax.imshow(img)
    ax.set_title(lbl, fontsize=11)
    ax.axis('off')
ax = axes[2]
ax.scatter(SAY_AUDIT['past_tfidf_top1_lag'].fillna(-1), SAY_AUDIT['past_tfidf_top1_sim'].fillna(0), s=18, alpha=0.7)
ax.set_xlabel('best prior-input lag (ticks)')
ax.set_ylabel('best prior-input TF-IDF similarity')
ax.set_title('Aura say events: prior-input reuse structure')
ax.grid(alpha=0.25)
fig.suptitle('UTD composer audit on Aura outputs', fontsize=14)
fig.savefig(FIG / 'aura_utd_composer_audit_plate.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 8: node correspondence costs
pairs = []
for p in sorted((ROOT / 'node_corr/tables').glob('mapping_graphsig_state_*_to_state_*.csv.gz')):
    m = re.search(r'state_(\d+)_to_state_(\d+)', p.name)
    if not m:
        continue
    a, b = m.group(1), m.group(2)
    df = pd.read_csv(p)
    pairs.append((f'{a}->{b}', df['match_cost']))
fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
if pairs:
    ax.boxplot([s.values for _, s in pairs], tick_labels=[n for n, _ in pairs], showfliers=False)
    ax.set_ylabel('graph-signature match cost')
    ax.set_title('Node-correspondence remapping cost across adjacent late snapshots')
    ax.grid(axis='y', alpha=0.25)
fig.savefig(FIG / 'aura_node_correspondence_costs.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Tables: applicability and manifest
rows = [
    {'script': '00_build_tick_table.py', 'applied': True, 'status': 'ran', 'primary_outputs': 'tick_table_full.csv.gz', 'notes': 'Aura-compatible directly'},
    {'script': '01_compute_snapshot_metrics.py', 'applied': True, 'status': 'ran', 'primary_outputs': 'snapshot_metrics_legacy.csv', 'notes': 'Aura-compatible directly'},
    {'script': '02_four_proofs.py', 'applied': True, 'status': 'ran', 'primary_outputs': 'proof figures + tables', 'notes': 'Ran on Aura tick table + Aura snapshots'},
    {'script': 'analyze_scalar_struct_from_logs.py', 'applied': True, 'status': 'ran', 'primary_outputs': 'macrostate tables + ETA figures', 'notes': 'Aura-compatible directly'},
    {'script': 'utd_parse_and_composer_audit.py', 'applied': True, 'status': 'ran', 'primary_outputs': 'composer audit tables + histograms', 'notes': 'Ran on Aura UTD zip'},
    {'script': 'run_connectome_geometry_projectionmap_analysis.py', 'applied': True, 'status': 'ran', 'primary_outputs': 'embedding/heatmap/degree plots', 'notes': 'Ran on Aura H5 snapshots'},
    {'script': 'run_node_correspondence_matching.py', 'applied': True, 'status': 'partial', 'primary_outputs': 'mapping CSVs for adjacent snapshot pairs', 'notes': 'Produced adjacent pair mappings only in current environment'},
    {'script': 'vdm_convert.py', 'applied': True, 'status': 'ran-with-schema-mismatch', 'primary_outputs': 'dashboard JSONs', 'notes': 'H5 conversion succeeded; Aura events schema mismatch left event-rich fields empty'},
    {'script': 'run_all.py', 'applied': True, 'status': 'failed-schema-mismatch', 'primary_outputs': 'none', 'notes': 'Aura UTD schema mismatch on missing text field in say table'},
]
pd.DataFrame(rows).to_csv(TAB / 'legacy_script_applicability_map.csv', index=False)

manifest = []
for fp in sorted(FIG.glob('*.png')):
    manifest.append({'artifact': fp.name, 'type': 'figure', 'source_scripts': 'legacy scripts + make_publication_figures.py'})
for fp in sorted(TAB.glob('*.csv')):
    manifest.append({'artifact': fp.name, 'type': 'table', 'source_scripts': 'legacy scripts + make_publication_figures.py'})
pd.DataFrame(manifest).to_csv(TAB / 'publication_artifact_manifest.csv', index=False)

print('done')
