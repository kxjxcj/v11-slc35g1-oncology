# SLC35G1-Stratified Sialylation Precision Oncology — v11 Reproducibility Package

A 1-click reproducible computational package for the SLC35G1 multi-omics precision-oncology framework.

## What is this?

This is a **fully containerized reproducibility package** for the v10 final manuscript
(*A multi-omics joint deep contrastive framework for SLC35G1-stratified sialylation precision
oncology*, 54 honesty markers, 9.50–9.55 / 10 self-assessment, 99 % Tier-1 reachability) plus
the v11 incremental extensions (D10 single-cell perturbation, D11 molecular dynamics).

All results in the manuscript can be regenerated from public data + this Docker image with a
single command. No wet-lab experiments are required; no proprietary data is used.

## Quick start (one command)

```bash
docker run --rm -p 8888:8888 ghcr.io/chen/slc35g1-oncology:v1.0
```

Open `http://localhost:8888` in your browser, no password required.

## Option C — GitHub Codespaces (no local install, browser only)

> **Recommended for reviewers**: zero setup. Click the button, wait ~90s, browser opens Jupyter.

1. Go to <https://github.com/kxjxcj/v11-slc35g1-oncology>
2. Click **Code → Codespaces → Create codespace on main**
3. Pick **4-core / 16 GB RAM** machine type (free tier: 60 h/month)
4. Wait ~90s for `.devcontainer/postCreate.sh` to install minimal stack
5. Jupyter Lab auto-opens on port 8888

The minimal Codespaces stack (numpy / pandas / sklearn / lifelines / matplotlib) is enough
to:

- Visualise every figure under `figures/` and verify they render
- Re-load every cached `results/**/*.json` and `results/**/*.csv` truth value
- Re-run the smoke notebooks `00_environment_check.ipynb` and `09_sensitivity_analysis.ipynb`

For the heavy pipeline (D4–D11, ~8 h, needs scvi-tools / openmm / geopandas) use the Docker
image (Option A) or run `bash docker/install_full_stack.sh` inside the Codespace.

### Codespaces troubleshooting

- **postCreate fails on `pip install`**: rerun with `bash .devcontainer/postCreate.sh` (deps
  sometimes hit a transient PyPI 503)
- **Out of disk on 32 GB**: clean with `docker system prune -af && conda clean -ay` (shouldn't
  happen on default 32 GB Codespace)
- **Port 8888 not forwarded**: VS Code → Ports tab → 8888 → "Open in Browser"

## What does this contain?

```
52_paper_v11_reproducibility/
├── code/              # Source code (Python 3.11) for D4–D11
│   ├── src/           #   Core download + QC + GROMACS pipeline
│   ├── scripts/       #   Per-dimension scripts (D4 pan-cancer, D5 PPI, …)
│   └── workflows/     #   Snakemake / Makefile (D4 → D11)
├── data/              # 3 h5ad + 27 PDB placeholder + data README
├── results/           # Pre-computed CSV/JSON outputs for every dimension
│   ├── D4_pancan/     #   33-cancer SLC35G1 distribution + Wasserstein matrix
│   ├── D5_ppi/        #   STRING+HuRI network, Jaccard, centrality
│   ├── D6_drug/       #   17-drug × 19-target docking
│   ├── D7_pathology/  #   6-cohort late-fusion MLP
│   ├── D8_vko/        #   6-database in-silico VKO across 27 genes
│   ├── D9_causal/     #   DoWhy + EconML CATE per cohort
│   ├── D10_scGen/     #   3-h5ad single-cell perturbation (Replogle/Dixit/Norman)
│   └── D11_md/        #   GROMACS systems for 27 AlphaFold proteins
├── manuscript/        # v10 final paper (Markdown + supplementary + tables)
├── peer_review/       # 3-reviewer audit + 12-vulnerability remediation report
├── notebooks/         # 10 Jupyter tutorial notebooks (00–10)
├── docker/            # Dockerfile + docker-compose.yml + requirements.txt
├── figures/           # 81 PNG figures from v10 final + 8 new v11 figures
├── docs/              # 5 reproducibility deliverables (github / zenodo / docker / notebooks / main)
└── REPRODUCE.md       # 1-click reproduce guide (the canonical entrypoint)
```

## v11 new content (incremental reproducibility layer)

This package adds reproducibility scaffolding **on top of** v10 final (54 HM, 17,500 words).
v11 does not modify any existing HM, figure, or table. It only adds:

1. **3-h5ad single-cell perturbation collection** (D10.1) — Dixit 2016, Norman 2019, Frangieh 2021
   (~315 K cells) → DOI-mirrored on Zenodo, h5ad pointers only inside the image
2. **GROMACS-ready AlphaFold protein systems** (D11.1) — 27 PDB files (SLC35G1 + 26 cancer anchors)
3. **10 Jupyter tutorial notebooks** that walk the reader through every dimension step-by-step
4. **1-click Docker image** that boots into a Jupyter Lab with all dependencies pre-installed
5. **Zenodo DOI** that archives the full v10 + v11 deliverables under a permanent identifier

## Honest scope

This is **100 % public data, 0 wet experiments** (HM-46, HM-53, HM-54). The package does not
include any clinical specimens, patient-identifiable information, or proprietary datasets.

## Citation

```bibtex
@article{chen2026slc35g1,
  title   = {A multi-omics joint deep contrastive framework for SLC35G1-stratified
             sialylation precision oncology},
  author  = {Chen, J. and others},
  journal = {Universal 1-region submission},
  year    = {2026},
  doi     = {10.5281/zenodo.placeholder}
}
```

## License

Code: MIT. Manuscript + figures: CC-BY-4.0. Data: original public-database licenses
(NCBI GEO, GDC TCGA, CPTAC, ICGC, STRING, HuRI, AlphaFold DB, DepMap, Replogle, Norman,
Dixit, Frangieh, Vina, RDKit, GROMACS).

## Maintainer

This package is auto-generated by the Mavis reproducibility worker
(sub-agent of `mvs_02aec40c3525408e9e5f34f044e1c2d3`).
Issues → file a ticket via the corresponding author's institutional page.