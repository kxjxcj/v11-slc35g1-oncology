#!/usr/bin/env python3
"""
D10.1 QC Pipeline - 5 scRNA-seq datasets
- 标准化 QC (min_genes, min_cells, mito_pct, doublet)
- scanpy standard workflow
- 输出 _processed.h5ad + QC stats
"""
import os
import sys
import json
import time
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad

# optional - check if available
try:
    import scrublet as scr
    HAS_SCRUBLET = True
except ImportError:
    HAS_SCRUBLET = False
    print("WARN: scrublet not available, skipping doublet detection")

import warnings
warnings.filterwarnings('ignore')

sc.settings.verbosity = 1

RAW_DIR = Path("/Users/chen/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/50_paper_v11_D10_scGen/D10.1_data")
OUT_DIR = RAW_DIR  # processed goes in same root dir

QC_STATS = {}

def load_h5ad(path):
    """Load h5ad, handle the case where X is already raw counts vs normalized"""
    adata = sc.read_h5ad(path)
    print(f"  Loaded: {adata.shape[0]} cells x {adata.shape[1]} genes")
    print(f"  obs columns: {list(adata.obs.columns)[:8]}")
    print(f"  var columns: {list(adata.var.columns)[:8]}")
    if 'X' in dir(adata):
        x = adata.X
        if hasattr(x, 'toarray'):
            sample = x[:5, :5].toarray()
        else:
            sample = x[:5, :5]
        print(f"  X sample (5x5): {sample}")
        # Detect if log-normalized
        if np.allclose(sample, np.round(sample)):
            print("  X appears to be raw counts (integers)")
        elif sample.max() < 20:
            print("  X appears to be log-normalized (small values)")
        else:
            print("  X scale: unknown")
    return adata


def qc_filter(adata, name, min_genes=200, min_cells=3, mito_max=0.20):
    """
    Standard scanpy QC:
    - Add mito percent
    - Filter cells (min_genes, mito < 20%)
    - Filter genes (min_cells)
    - Optional doublet detection (scrublet)
    """
    stats = {"name": name, "n_raw_cells": int(adata.shape[0]), "n_raw_genes": int(adata.shape[1])}

    # 1. Mark mito genes
    adata.var['mt'] = adata.var_names.str.startswith('MT-')
    n_mt = int(adata.var['mt'].sum())
    stats['n_mito_genes'] = n_mt
    print(f"  Mito genes: {n_mt}")

    # 2. Compute QC metrics
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    if 'pct_counts_mt' in adata.obs.columns:
        stats['mito_pct_median'] = float(adata.obs['pct_counts_mt'].median())
        stats['mito_pct_max'] = float(adata.obs['pct_counts_mt'].max())

    # 3. Filter
    n0 = adata.shape[0]
    sc.pp.filter_cells(adata, min_genes=min_genes)
    n1 = adata.shape[0]
    sc.pp.filter_genes(adata, min_cells=min_cells)
    n2 = adata.shape[0]
    adata = adata[adata.obs['pct_counts_mt'] < mito_max * 100].copy()
    n3 = adata.shape[0]

    stats['after_min_genes'] = n1
    stats['after_min_cells_genes'] = n2
    stats['after_mito_filter'] = n3
    print(f"  Cells: {n0} -> min_genes {n1} -> min_cells {n2} -> mito<{mito_max*100}% {n3}")
    print(f"  Genes after filter: {adata.shape[1]}")

    # 4. Doublet detection (scrublet)
    if HAS_SCRUBLET and adata.shape[0] > 50:
        try:
            scrub = scr.Scrublet(adata.X, random_state=0)
            adata.obs['doublet_score'], predicted = scrub.scrub_doublets(verbose=False)
            n_doublet = int(predicted.sum())
            stats['n_doublet_predicted'] = n_doublet
            stats['doublet_rate'] = round(n_doublet / adata.shape[0], 4)
            print(f"  Doublets predicted: {n_doublet} ({n_doublet/adata.shape[0]*100:.1f}%)")
            # Filter doublets if score available
            if 'doublet_score' in adata.obs.columns:
                # Use threshold 0.25 (conservative)
                adata = adata[adata.obs['doublet_score'] < 0.25].copy()
                stats['after_doublet_filter'] = int(adata.shape[0])
                print(f"  Cells after doublet filter: {adata.shape[0]}")
        except Exception as e:
            print(f"  Doublet detection failed: {e}")
            stats['doublet_error'] = str(e)

    return adata, stats


def process_dataset(name, raw_path, output_path):
    """Process a single dataset: load, QC, save"""
    print(f"\n{'='*60}")
    print(f"Processing: {name}")
    print(f"  Raw: {raw_path}")
    print(f"  Output: {output_path}")
    print(f"{'='*60}")

    if not raw_path.exists():
        print(f"  ERROR: {raw_path} does not exist, skipping")
        return None

    try:
        adata = load_h5ad(raw_path)
    except Exception as e:
        print(f"  ERROR loading: {e}")
        return {"name": name, "error": str(e)}

    adata_proc, stats = qc_filter(adata, name)
    stats['processed_path'] = str(output_path)
    stats['n_processed_cells'] = int(adata_proc.shape[0])
    stats['n_processed_genes'] = int(adata_proc.shape[1])

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    adata_proc.write_h5ad(output_path)
    size_mb = output_path.stat().st_size / 1e6
    print(f"  Saved: {output_path} ({size_mb:.1f} MB)")

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datasets', nargs='*', help='specific datasets to process')
    args = parser.parse_args()

    # All 7 raw files we downloaded
    dataset_names = [
        "dixit_2016_raw",
        "dixit_2016_processed",
        "norman_2019_raw",
        "norman_2019_processed",
        "frangieh_2021_raw",
        "frangieh_2021_processed",
        "srivatsan_2019_raw",
    ]

    if args.datasets:
        dataset_names = [d for d in dataset_names if d in args.datasets]

    all_stats = {}
    for name in dataset_names:
        raw_path = RAW_DIR / "raw" / f"{name}.h5ad"
        # processed version: same name, in parent dir
        output_path = RAW_DIR / f"{name}_processed.h5ad"

        if not raw_path.exists():
            print(f"SKIP {name}: {raw_path} not found")
            all_stats[name] = {"name": name, "skipped": "no raw file"}
            continue

        # Don't QC an already-processed file
        if "processed" in name and name.replace("_processed", "") not in name:
            # This is a separate "processed" download, just verify it
            print(f"Verify pre-processed: {name}")
            try:
                adata = sc.read_h5ad(raw_path)
                print(f"  Already processed: {adata.shape[0]} cells x {adata.shape[1]} genes")
                # Copy to output
                import shutil
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(raw_path, output_path)
                all_stats[name] = {
                    "name": name,
                    "source": "figshare pre-processed",
                    "n_processed_cells": int(adata.shape[0]),
                    "n_processed_genes": int(adata.shape[1]),
                    "n_raw_cells": int(adata.shape[0]),
                    "n_raw_genes": int(adata.shape[1]),
                    "qc_skipped": "already processed",
                }
            except Exception as e:
                print(f"  ERROR: {e}")
                all_stats[name] = {"name": name, "error": str(e)}
            continue

        stats = process_dataset(name, raw_path, output_path)
        if stats:
            all_stats[name] = stats

    # Save QC summary
    qc_path = RAW_DIR / "qc_summary.json"
    with open(qc_path, "w") as f:
        json.dump(all_stats, f, indent=2, default=str)
    print(f"\nQC summary saved: {qc_path}")

    # Print summary
    print(f"\n{'='*60}")
    print("QC Summary")
    print(f"{'='*60}")
    for name, stats in all_stats.items():
        if 'error' in stats:
            print(f"  {name}: ERROR {stats['error'][:80]}")
        elif 'skipped' in stats:
            print(f"  {name}: SKIPPED ({stats['skipped']})")
        else:
            print(f"  {name}: {stats.get('n_raw_cells', '?')} -> {stats.get('n_processed_cells', '?')} cells, "
                  f"{stats.get('n_raw_genes', '?')} -> {stats.get('n_processed_genes', '?')} genes")


if __name__ == "__main__":
    main()
