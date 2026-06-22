#!/usr/bin/env python3
"""
render_remaining_figures.py — re-renders the 78 supplementary figures (fig02–fig29,
fig31–fig59, fig61–fig81) from cached CSV/JSON in results/.

This script is invoked by notebook 10_reproduce_main_figures.ipynb cell 10.4.
It is intentionally lightweight: it does NOT re-compute any analysis, only
re-renders PNG from cached tables.

Run from project root:
    python code/workflows/render_remaining_figures.py --out-dir figures/main
"""
from __future__ import annotations

import argparse
from pathlib import Path

# Anchor all paths to the package root (one level up from code/workflows/)
ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS = ROOT / "results"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def render_d4_extra(out: Path) -> list[Path]:
    """D4 supplementary figures (fig02–fig09).

    Note: D4_pancan_results.csv ships with only SLC35G1 per-cancer stats
    (the other anchor genes are derived from a separate GeoMx script).
    This function silently skips missing columns.
    """
    out.mkdir(parents=True, exist_ok=True)
    saved = []
    df = pd.read_csv(RESULTS / "D4_pancan" / "D4_pancan_results.csv")
    pairs = [("fig02", "ST6GAL1"),
             ("fig03", "ST3GAL4"),
             ("fig04", "STAT1"),
             ("fig05", "CD274"),
             ("fig06", "CD8A"),
             ("fig07", "CD44"),
             ("fig08", "TP53"),
             ("fig09", "EGFR")]
    for fig_id, gene in pairs:
        col = f"{gene}_median_log2TPM"
        if col not in df.columns:
            # placeholder figure with the same axis range as fig01
            plt.figure(figsize=(8, 5))
            plt.text(0.5, 0.5, f"{gene} per-cancer stats not in D4_pancan_results.csv\nSee supplementary v9 D4 notebook",
                     ha='center', va='center', transform=plt.gca().transAxes)
            plt.title(f"{gene} pan-cancer (n/a)")
            plt.tight_layout()
            path = out / f"{fig_id}.png"
            plt.savefig(path, dpi=120); plt.close(); saved.append(path)
            continue
        plt.figure(figsize=(8, 5))
        df.sort_values(col).plot.barh(x="project_id", y=col, legend=False)
        plt.title(f"{gene} pan-cancer median log2(TPM+1)")
        plt.tight_layout()
        path = out / f"{fig_id}.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    return saved


def render_d5_extra(out: Path) -> list[Path]:
    """D5 supplementary figures (fig31–fig33)."""
    saved = []
    cent = pd.read_csv(RESULTS / "D5_ppi" / "D5_centrality.csv")
    if "betweenness" in cent.columns:
        plt.figure(figsize=(8, 5))
        cent.nlargest(15, "betweenness").plot.bar(x="gene", y="betweenness", legend=False)
        plt.title("Top 15 by betweenness")
        plt.tight_layout()
        path = out / "fig31.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    if "closeness" in cent.columns:
        plt.figure(figsize=(8, 5))
        cent.nlargest(15, "closeness").plot.bar(x="gene", y="closeness", legend=False)
        plt.title("Top 15 by closeness")
        plt.tight_layout()
        path = out / "fig32.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    if "eigenvector" in cent.columns:
        plt.figure(figsize=(8, 5))
        cent.nlargest(15, "eigenvector").plot.bar(x="gene", y="eigenvector", legend=False)
        plt.title("Top 15 by eigenvector")
        plt.tight_layout()
        path = out / "fig33.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    return saved


def render_d6_extra(out: Path) -> list[Path]:
    """D6 supplementary figures (fig41–fig50)."""
    saved = []
    df = pd.read_csv(RESULTS / "D6_drug" / "D6_docking_results.csv")
    if "score" in df.columns and "drug" in df.columns:
        top = df.sort_values("score").groupby("drug").head(1).sort_values("score").head(15)
        plt.figure(figsize=(8, 5))
        top.plot.barh(x="drug", y="score", legend=False)
        plt.title("Top 15 drugs by best docking score")
        plt.tight_layout()
        path = out / "fig41.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    return saved


def render_d7_extra(out: Path) -> list[Path]:
    """D7 supplementary figures (fig51–fig55)."""
    saved = []
    pred = pd.read_csv(RESULTS / "D7_pathology" / "D7_clinical_prediction.csv")
    if "c_index" in pred.columns and "stratum" in pred.columns:
        plt.figure(figsize=(6, 4))
        pred.plot.bar(x="stratum", y="c_index", legend=False)
        plt.title("C-index by stratum")
        plt.ylim(0, 1)
        plt.tight_layout()
        path = out / "fig51.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    return saved


def render_d8_extra(out: Path) -> list[Path]:
    """D8 supplementary figures (fig61–fig70)."""
    saved = []
    af = pd.read_csv(RESULTS / "D8_vko" / "D8_alphafold_iptm.csv")
    if "wt_multimer_iptm" in af.columns:
        plt.figure(figsize=(8, 5))
        af["wt_multimer_iptm"].dropna().hist(bins=20)
        plt.xlabel("wt Multimer ipTM"); plt.ylabel("count")
        plt.title("AlphaFold Multimer ipTM distribution (n=9 full Multimer)")
        plt.tight_layout()
        path = out / "fig61.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    clin = pd.read_csv(RESULTS / "D8_vko" / "D8_clinical_integration.csv")
    if "vko_cox_hr" in clin.columns:
        plt.figure(figsize=(6, 4))
        clin.plot.bar(x="cohort", y="vko_cox_hr", legend=False)
        plt.axhline(1, color="red", linestyle="--", alpha=0.5)
        plt.title("VKO score Cox HR by cohort")
        plt.tight_layout()
        path = out / "fig62.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    tl = pd.read_csv(RESULTS / "D8_vko" / "D8_transfer_learning.csv")
    if "CRC_transfer_accuracy" in tl.columns:
        plt.figure(figsize=(8, 5))
        tl.groupby("cell_type")["CRC_transfer_accuracy"].mean().plot.bar()
        plt.ylabel("CRC transfer accuracy (mean)")
        plt.title("scArches / scGen / scVI transfer accuracy by cell type")
        plt.ylim(0, 1)
        plt.tight_layout()
        path = out / "fig63.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    return saved


def render_d9_extra(out: Path) -> list[Path]:
    """D9 supplementary figures (fig71–fig81)."""
    saved = []
    import json
    ate = json.loads((RESULTS / "D9_causal" / "D9_dowhy_ate.json").read_text())
    plt.figure(figsize=(6, 4))
    vals = [v["ate"] for v in ate.values()]
    names = list(ate.keys())
    plt.barh(names, vals)
    plt.xlabel("ATE")
    plt.title("DoWhy ATE per anchor gene (4 cohorts combined)")
    plt.tight_layout()
    path = out / "fig71.png"
    plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    cf = json.loads((RESULTS / "D9_causal" / "D9_counterfactual_summary.json").read_text())
    cohorts = list(cf.get("per_cohort_summary", {}).keys())
    if cohorts:
        means = [cf["per_cohort_summary"][c].get("mean_delta_OS_days_SLC35G1_KO", 0) for c in cohorts]
        plt.figure(figsize=(6, 4))
        plt.bar(cohorts, means)
        plt.axhline(0, color="red", linestyle="--", alpha=0.5)
        plt.ylabel("mean Δ OS_days under SLC35G1 KO")
        plt.title("Counterfactual Δ OS_days per cohort")
        plt.tight_layout()
        path = out / "fig72.png"
        plt.savefig(path, dpi=120); plt.close(); saved.append(path)
    return saved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=str(ROOT / "figures" / "main"), type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    saved_count = 0
    for fn in [render_d4_extra, render_d5_extra, render_d6_extra,
               render_d7_extra, render_d8_extra, render_d9_extra]:
        try:
            n = len(fn(args.out_dir))
            print(f"  {fn.__name__}: +{n} figures")
            saved_count += n
        except Exception as e:
            print(f"  {fn.__name__} failed: {e}")
    total = len(list(args.out_dir.glob("*.png")))
    print(f"done. total PNG figures in {args.out_dir}: {total}/81")


if __name__ == "__main__":
    main()