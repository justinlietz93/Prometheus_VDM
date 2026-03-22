
from pathlib import Path
import json, glob, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

BASE = Path("/mnt/data/aura_analysis_extracted/aura_analysis_bundle")
OUT = Path("/mnt/data/aura_research_deliverables")
TABLES = OUT / "tables"
FIGS = OUT / "figures"
DOCS = OUT / "docs"
for p in [TABLES, FIGS, DOCS]:
    p.mkdir(parents=True, exist_ok=True)

def extract_territories():
    rows = []
    for p in sorted((BASE / "json").glob("state_*_dashboard.json")):
        state_t = int(p.name.split("_")[1])
        data = json.load(open(p))
        for terr in data["state"]["territories"]:
            rows.append({
                "state_t": state_t,
                "id": terr["id"],
                "mass": terr["mass"],
                "ttl": terr["ttl"],
                "w_mean": terr["w_mean"],
                "w_var": terr["w_var"],
                "s_mean": terr["s_mean"],
                "s_var": terr["s_var"],
                "conf": terr.get("conf", np.nan),
            })
    terr = pd.DataFrame(rows).sort_values(["id", "state_t"])
    terr.to_csv(TABLES / "f3_territory_timeseries_late.csv", index=False)

    growth = terr.groupby("id").agg(
        mass_start=("mass", "first"),
        mass_end=("mass", "last"),
        mass_delta=("mass", lambda x: x.iloc[-1] - x.iloc[0]),
        ttl_mean=("ttl", "mean"),
        ttl_min=("ttl", "min"),
        ttl_max=("ttl", "max"),
        s_mean_mean=("s_mean", "mean"),
        s_mean_std=("s_mean", "std"),
        s_var_mean=("s_var", "mean"),
        w_mean_mean=("w_mean", "mean"),
        w_var_mean=("w_var", "mean"),
    ).reset_index()
    total_delta = growth["mass_delta"].sum()
    growth["growth_share_of_total_delta"] = np.where(
        total_delta != 0, growth["mass_delta"] / total_delta, 0.0
    )

    feat = growth[["mass_end", "mass_delta", "ttl_mean", "s_mean_mean", "s_var_mean"]].copy()
    X = StandardScaler().fit_transform(feat)
    labels = AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(X)
    growth["phenotype_cluster"] = labels

    # Stable names by sorted feature signature
    cluster_sig = growth.groupby("phenotype_cluster").agg(
        mean_mass=("mass_end", "mean"),
        mean_delta=("mass_delta", "mean"),
        mean_ttl=("ttl_mean", "mean"),
        mean_s=("s_mean_mean", "mean"),
        mean_svar=("s_var_mean", "mean"),
    ).reset_index()
    # deterministic naming
    name_map = {}
    for _, r in cluster_sig.sort_values(["mean_delta", "mean_s", "mean_mass"]).iterrows():
        cid = int(r["phenotype_cluster"])
        if r["mean_delta"] > 0:
            name_map[cid] = "frontier_growth"
        elif r["mean_s"] > 0.55:
            name_map[cid] = "high_signal_fixed"
        elif r["mean_s"] > 0.10:
            name_map[cid] = "mid_signal_fixed"
        else:
            name_map[cid] = "low_signal_fixed"
    growth["phenotype_name"] = growth["phenotype_cluster"].map(name_map)
    growth = growth.sort_values("id")
    growth.to_csv(TABLES / "f3_territory_growth_clusters.csv", index=False)

    cluster_summary = growth.groupby(["phenotype_cluster", "phenotype_name"]).agg(
        territory_ids=("id", lambda x: ",".join(map(str, x))),
        n_territories=("id", "size"),
        mean_mass_end=("mass_end", "mean"),
        total_mass_end=("mass_end", "sum"),
        total_mass_delta=("mass_delta", "sum"),
        mean_ttl=("ttl_mean", "mean"),
        mean_s_mean=("s_mean_mean", "mean"),
        mean_s_var=("s_var_mean", "mean"),
    ).reset_index().sort_values(["phenotype_name", "phenotype_cluster"])
    cluster_summary.to_csv(TABLES / "f3_territory_cluster_summary.csv", index=False)

    return terr, growth, cluster_summary

def extract_community_effects():
    rows = []
    toplines = []
    for p in sorted((BASE / "connectome_geom" / "results").glob("node_embedding_metrics_state_*.csv")):
        state_t = int(p.stem.split("_")[-1])
        df = pd.read_csv(p)
        ncom = int(df["community"].nunique())
        for metric in ["out_degree", "participation", "pagerank", "convergence_score", "row_weight_param"]:
            overall = df[metric].mean()
            groups = [g[metric].to_numpy() for _, g in df.groupby("community")]
            ss_between = sum(len(g) * (g.mean() - overall) ** 2 for g in groups)
            ss_total = ((df[metric] - overall) ** 2).sum()
            eta_sq = float(ss_between / ss_total) if ss_total else np.nan
            rows.append({
                "state_t": state_t,
                "metric": metric,
                "eta_sq": eta_sq,
                "n_communities": ncom,
            })
        top = (
            df.groupby("community")
              .agg(
                  n=("node", "size"),
                  out_degree_mean=("out_degree", "mean"),
                  participation_mean=("participation", "mean"),
                  pagerank_mean=("pagerank", "mean"),
                  convergence_mean=("convergence_score", "mean"),
                  row_weight_mean=("row_weight_param", "mean"),
              )
              .reset_index()
        )
        top["state_t"] = state_t
        toplines.append(top)
    effect_df = pd.DataFrame(rows).sort_values(["state_t", "metric"])
    top_df = pd.concat(toplines, ignore_index=True).sort_values(["state_t", "n"], ascending=[True, False])

    effect_df.to_csv(TABLES / "f3_community_metric_effect_sizes.csv", index=False)
    top_df.to_csv(TABLES / "f3_community_phenotype_summary_by_snapshot.csv", index=False)
    return effect_df, top_df

def make_figures(terr, growth, effect_df):
    # Territory mass / growth figure
    fig, ax = plt.subplots(figsize=(8, 5))
    for tid, g in terr.groupby("id"):
        ax.plot(g["state_t"], g["mass"], marker="o", label=f"T{tid}")
    ax.set_xlabel("Late snapshot tick")
    ax.set_ylabel("Territory mass")
    ax.set_title("Late territory mass trajectories")
    ax.legend(ncol=3, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "f3_territory_mass_trajectories_late.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 5))
    for _, r in growth.iterrows():
        ax.scatter(r["mass_end"], r["s_mean_mean"], s=40 + (r["mass_end"] / 8000.0), alpha=0.9)
        ax.text(r["mass_end"], r["s_mean_mean"], f"T{int(r['id'])}", fontsize=8, ha="left", va="bottom")
    ax.set_xlabel("Late mass (final snapshot)")
    ax.set_ylabel("Mean s_mean across late snapshots")
    ax.set_title("Late territory phenotype map")
    fig.tight_layout()
    fig.savefig(FIGS / "f3_territory_phenotype_map.png", dpi=180)
    plt.close(fig)

    piv = effect_df.pivot(index="state_t", columns="metric", values="eta_sq")
    fig, ax = plt.subplots(figsize=(8, 5))
    for metric in ["participation", "convergence_score", "row_weight_param", "out_degree", "pagerank"]:
        ax.plot(piv.index, piv[metric], marker="o", label=metric)
    ax.set_xlabel("Late snapshot tick")
    ax.set_ylabel("Eta-squared explained by community")
    ax.set_title("Community phenotype effect sizes across late snapshots")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "f3_community_effect_sizes_late.png", dpi=180)
    plt.close(fig)

def build_note(growth, effect_df):
    frontier = growth[growth["mass_delta"] > 0]
    fixed = growth[growth["mass_delta"] == 0]
    p = effect_df.pivot(index="state_t", columns="metric", values="eta_sq")
    note = f"""# F3 late territory and community phenotype analysis

## Scope
This pack analyzes the late-snapshot territory fields from `json/state_*_dashboard.json`
and the per-node community embeddings from `connectome_geom/results/node_embedding_metrics_state_*.csv`.

## Hard observations
- Exactly **2 of 9** late territories grow across the five late snapshots: territories {", ".join("T"+str(x) for x in frontier["id"].tolist())}.
- Those two territories carry **100% of net late mass growth**: total delta = {growth["mass_delta"].sum():.0f}; frontier deltas = {", ".join(f"T{int(r.id)}={int(r.mass_delta)}" for _, r in frontier.iterrows())}.
- The other **7 territories are mass-invariant** across all five late snapshots.
- Ward clustering on standardized late territory features (`mass_end`, `mass_delta`, `ttl_mean`, `s_mean_mean`, `s_var_mean`) yields four territory phenotype groups:
  - low-signal fixed: {growth.loc[growth.phenotype_name=='low_signal_fixed','id'].tolist()}
  - high-signal fixed: {growth.loc[growth.phenotype_name=='high_signal_fixed','id'].tolist()}
  - mid-signal fixed: {growth.loc[growth.phenotype_name=='mid_signal_fixed','id'].tolist()}
  - frontier_growth: {growth.loc[growth.phenotype_name=='frontier_growth','id'].tolist()}
- Community membership explains much more variance in **participation** than in raw degree during late snapshots.
  - participation eta²: {", ".join(f"{int(t)}={p.loc[t,'participation']:.3f}" for t in p.index)}
  - convergence eta²: {", ".join(f"{int(t)}={p.loc[t,'convergence_score']:.3f}" for t in p.index)}
  - out_degree eta²: {", ".join(f"{int(t)}={p.loc[t,'out_degree']:.3f}" for t in p.index)}

## Readable interpretation
The late structure is not just "9 territories exist." The territories separate into distinct phenotypes under unsupervised clustering,
and the community system differentiates routing/mixing behavior far more strongly than sheer degree.
That is a real specialization proxy, even without assigning semantic roles to specific territories.
"""
    (DOCS / "F3_late_territory_community_phenotypes_note.md").write_text(note)

def main():
    terr, growth, cluster_summary = extract_territories()
    effect_df, top_df = extract_community_effects()
    make_figures(terr, growth, effect_df)
    build_note(growth, effect_df)
    print("Wrote F3 late territory/community phenotype outputs.")

if __name__ == "__main__":
    main()
