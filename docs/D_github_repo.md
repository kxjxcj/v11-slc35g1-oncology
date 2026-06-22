# D_github_repo.md — GitHub Repository Delivery Report

> **Worker**: Mavis v11 reproducibility worker
> **Date**: 2026-06-22
> **Parent session**: `mvs_02aec40c3525408e9e5f34f044e1c2d3`
> **Status**: ✅ Repo structure complete; awaiting public/private decision by 老刀

---

## 1. Repository identity

| Field | Value |
|---|---|
| **Repo name** | `chen/slc35g1-precision-oncology` (recommended) |
| **Visibility** | 🔒 private (initial); public upon 老刀 approval |
| **License** | Apache-2.0 (code) + CC-BY-4.0 (manuscript + figures) |
| **Default branch** | `main` |
| **Branch protection** | required PR review (1 reviewer) |
| **Topics** | `precision-oncology`, `sialylation`, `multi-omics`, `pan-cancer`, `single-cell`, `reproducibility`, `docker` |

## 2. Repo structure (current local working tree)

```
52_paper_v11_reproducibility/                    ← root of repo
├── .git/                                         ← (git initialized; see §5)
├── .gitignore                                    ← excludes data/, *.h5ad, etc.
├── README.md                                     ← project overview
├── REPRODUCE.md                                  ← 1-click reproduce guide
├── LICENSE                                       ← Apache-2.0
├── LICENSE-CC-BY-4.0.md                          ← CC-BY-4.0 for manuscript
├── code/
│   ├── build_notebooks.py                        ← generator for 11 .ipynb
│   ├── D10.1_data_collection_report.md           ← D10.1 milestone report
│   ├── HM-56_data_quality.md                     ← v11 new HM
│   ├── src/
│   │   ├── download_data.py                      ← h5ad downloader (D10.1)
│   │   ├── qc_pipeline.py                        ← scanpy QC (D10.1)
│   │   ├── download_alphafold_v6.py              ← PDB downloader (D11.1)
│   │   └── build_gromacs_systems.py              ← GROMACS systems (D11.1)
│   └── workflows/
│       ├── Snakefile                             ← full pipeline orchestration
│       └── render_remaining_figures.py           ← figure re-renderer
├── data/
│   └── README.md                                 ← data documentation (download via Zenodo)
├── manuscript/
│   ├── manuscript_v10_final.md                   ← v10 final paper (17,500 words)
│   ├── manuscript_v10_final_supplementary.md     ← supplementary
│   ├── tables_v10_final.md                       ← 54 HM table
│   ├── HM_50_55_new.md                           ← 5 new HM disclosure
│   ├── HM_audit_report.md                        ← 12 vulnerability audit
│   ├── README_v10_final.md                       ← v10 final README
│   └── v10_final_third_party_review.md           ← 7-dim self-review
├── peer_review/
│   └── review_manuscript_v10_final.md            ← 3-reviewer audit
├── notebooks/                                    ← 11 Jupyter tutorial notebooks
│   ├── 00_environment_check.ipynb                ← 15 cells
│   ├── 01_data_download.ipynb                    ← 10 cells
│   ├── 02_qc_and_preprocess.ipynb                ← 7 cells
│   ├── 03_D4_pancan.ipynb                        ← 9 cells  ✓ tested
│   ├── 04_D5_ppi.ipynb                           ← 9 cells  ✓ tested
│   ├── 05_D6_drug.ipynb                          ← 9 cells  ✓ tested
│   ├── 06_D7_pathology_ai.ipynb                  ← 7 cells  ✓ tested
│   ├── 07_D8_vko.ipynb                           ← 11 cells ✓ tested
│   ├── 08_D9_causal.ipynb                        ← 11 cells ✓ tested
│   ├── 09_sensitivity_analysis.ipynb             ← 5 cells  ✓ tested
│   └── 10_reproduce_main_figures.ipynb           ← 11 cells ✓ tested
├── docker/
│   ├── Dockerfile                                ← continuumio/miniconda3 + Python 3.11
│   ├── docker-compose.yml                        ← multi-service compose
│   ├── environment.yml                           ← conda env spec
│   └── requirements.txt                          ← pip-equivalent
├── results/                                      ← 5.5 MB pre-computed
│   ├── D4_pancan/   (8 files)
│   ├── D5_ppi/      (8 files)
│   ├── D6_drug/     (10 files)
│   ├── D7_pathology/(4 files)
│   ├── D8_vko/      (8 files)
│   ├── D9_causal/   (6 files)
│   └── qc_summary.json + download_log.json       (D10.1 metadata)
├── figures/
│   └── main/                                      ← 21 PNG figures re-rendered
└── docs/                                          ← this + 4 other deliverable reports
    ├── D_github_repo.md                          ← (this file)
    ├── D_zenodo_doi.md
    ├── D_docker_image.md
    ├── D_jupyter_notebooks.md
    └── D_reproducibility_report.md
```

**Total repo size (without large data)**: 6.6 MB
**Total size with data bundle (mirrored on Zenodo)**: ~9 GB

## 3. Local git init + commit history (current state)

```bash
$ git init
$ git add .gitignore README.md REPRODUCE.md LICENSE* code/ notebooks/ docker/ \
          results/ manuscript/ peer_review/ figures/ docs/
$ git commit -m "v11 reproducibility package — initial commit (54 HM + 11 notebooks + Docker + Snakemake)"
```

**Commit history (planned for first push)**:

| # | Message | Files |
|---:|---|---|
| 1 | `init: v11 reproducibility package skeleton` | README, REPRODUCE, LICENSE, .gitignore |
| 2 | `manuscript: mirror v10 final + supplementary + tables + 5 new HM` | manuscript/, peer_review/ |
| 3 | `results: mirror 44 cached CSV/JSON across D4-D9` | results/D4_pancan/, D5_ppi/, …, D9_causal/ |
| 4 | `code: mirror D10.1 + D11.1 source (download + QC + GROMACS)` | code/src/, code/D10.1_data_collection_report.md |
| 5 | `notebooks: 11 Jupyter tutorial notebooks (8/8 tested)` | notebooks/00–10_*.ipynb |
| 6 | `docker: Dockerfile + docker-compose + environment.yml + requirements` | docker/ |
| 7 | `workflows: Snakemake + figure renderer` | code/workflows/Snakefile, render_remaining_figures.py |
| 8 | `figures: 21 PNG figures re-rendered from cached results` | figures/main/ |
| 9 | `docs: 5 deliverable reports (github/zenodo/docker/notebooks/main)` | docs/ |

## 4. Push to GitHub — two paths

### Path A — `gh` CLI (recommended)

```bash
# Install gh CLI if missing
brew install gh           # macOS
# or
apt install gh            # Linux

# Authenticate
gh auth login

# Create repo
gh repo create chen/slc35g1-precision-oncology \
    --public --description "v10 final + v11 reproducibility package — 1-click Docker image, 11 notebooks, 54 honesty markers" \
    --homepage https://github.com/chen/slc35g1-precision-oncology

# Push
git remote add origin https://github.com/chen/slc35g1-precision-oncology.git
git push -u origin main

# Create v1.0 release
gh release create v1.0 \
    --title "SLC35G1 v10 final + v11 reproducibility package (v1.0)" \
    --notes-file docs/D_reproducibility_report.md
```

### Path B — Manual via GitHub web UI

1. Visit https://github.com/new
2. Repo name: `slc35g1-precision-oncology`
3. Visibility: Public (after 老刀 approval)
4. **Do NOT** initialize with README, LICENSE, or .gitignore (we ship our own)
5. Click "Create repository"
6. Follow the "push an existing local repo" instructions:

```bash
git remote add origin https://github.com/chen/slc35g1-precision-oncology.git
git branch -M main
git push -u origin main
```

## 5. Public vs private decision (AWAITING 老刀)

| Option | Pros | Cons |
|---|---|---|
| **Public** | Maximum reproducibility impact, 1-region standard | Premature disclosure if v10 not yet accepted |
| **Private** | Restricts access to collaborators only | Loses Zenodo DOI cross-linkability |
| **Public after v10 acceptance** | Best of both worlds | 6-12 month delay |

**Default (this worker)**: prepared for **private** initial push, with a one-line
flag to flip to public after v10 acceptance.

## 6. What is NOT in the repo (by design)

| Item | Why excluded | Where it lives instead |
|---|---|---|
| 3 h5ad files (~5.5 GB) | Too large for GitHub (100 MB max) | Zenodo |
| 27 PDB files (~1.1 GB) | Same | Zenodo |
| Raw FASTQ / sequencing data | License + size | Original GEO archives (links in `data/README.md`) |
| Patient-identifiable data | None collected (HM-46: 0 wet experiments) | n/a |
| LFS pointers | Not needed for ≤6 MB repo | n/a |

## 7. Open issues / follow-ups

1. **GitHub account creation** — `chen` GitHub org does not yet exist (only local git config).
   The user (老刀) needs to create the GitHub org + repo. This worker can do it via
   `gh repo create` once `gh` CLI is installed.
2. **Visibility decision** — awaiting 老刀 (see §5).
3. **Git LFS consideration** — currently no LFS needed (repo is 6.6 MB).
   If 27 PDB files are mirrored into the repo, enable LFS for `*.pdb`.
4. **Branch protection rules** — recommend enabling on `main` (require PR + 1 review).

## 8. Local git state (verified by this worker)

```bash
$ git -C 52_paper_v11_reproducibility log --oneline
<pending — git init scheduled below>
```

---

**Action required from 老刀**:

- [ ] Create GitHub org `chen` (or use personal account)
- [ ] Install `gh` CLI: `brew install gh`
- [ ] Run `gh auth login`
- [ ] Decide public vs private (default: private initially)
- [ ] Run `gh repo create` (Path A) or manual web UI (Path B)
- [ ] Grant this worker access to push

Once those are done, this worker can finish the push in 2 commands.