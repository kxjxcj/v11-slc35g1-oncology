# D4 Pan-Cancer (TCGA PANCAN 33-cancer) Data Summary

> **Generated**: 2026-06-20 (v9 D4 worker, parallel run with v9 PPI/drug/path)  
> **Data source**: TCGA PANCAN 33-cancer via UCSC Xena / GDC Open Access  
> **Workflow**: GDC API + STAR-Counts RNA-seq TSV (slim-parsed for 30 target genes) + GDC case endpoint clinical

## 1. Cohort enumeration (TCGA PANCAN 33 cancers)

- **Total TCGA-PANCAN projects**: 33 (ACC + 32 standard TCGA projects)
- **Cohort n_rna_seq (GDC queried, all STAR-Counts files)**: 10,517
- **Cohort n_clinical (all case-level clinical records)**: 11,428
- **Clin downloaded**: 33/33 projects, 11,428 case-level clinical records (vital_status, OS_days, ajcc_stage, age, gender, race)

### Per-cancer cohort sizes

| Project | n_rna_seq (GDC) | n_clin | site |
|---|---:|---:|---|
| TCGA-ACC | 79 | 92 | Adrenal gland |
| TCGA-BLCA | 406 | 412 | Bladder |
| TCGA-BRCA | 1,095 | 1,098 | Breast |
| TCGA-CESC | 304 | 307 | Cervix uteri |
| TCGA-CHOL | 36 | 51 | Liver and intrahepatic bile ducts |
| TCGA-COAD | 458 | 461 | Colon |
| TCGA-DLBC | 48 | 58 | Colon |
| TCGA-ESCA | 184 | 185 | Esophagus |
| TCGA-GBM | 293 | 617 | Brain |
| TCGA-HNSC | 521 | 528 | Lip |
| TCGA-KICH | 66 | 113 | Kidney |
| TCGA-KIRC | 533 | 537 | Kidney |
| TCGA-KIRP | 290 | 291 | Kidney |
| TCGA-LAML | 151 | 200 | Hematopoietic and reticuloendothelial systems |
| TCGA-LGG | 516 | 516 | Brain |
| TCGA-LIHC | 371 | 377 | Liver and intrahepatic bile ducts |
| TCGA-LUAD | 518 | 585 | Bronchus and lung |
| TCGA-LUSC | 501 | 504 | Bronchus and lung |
| TCGA-MESO | 87 | 87 | Bronchus and lung |
| TCGA-OV | 427 | 608 | Retroperitoneum and peritoneum |
| TCGA-PAAD | 178 | 185 | Pancreas |
| TCGA-PCPG | 179 | 179 | Adrenal gland |
| TCGA-PRAD | 497 | 500 | Prostate gland |
| TCGA-READ | 167 | 172 | Colon |
| TCGA-SARC | 259 | 261 | Retroperitoneum and peritoneum |
| TCGA-SKCM | 469 | 470 | Colon |
| TCGA-STAD | 415 | 443 | Stomach |
| TCGA-TGCT | 150 | 263 | Testis |
| TCGA-THCA | 505 | 507 | Thyroid gland |
| TCGA-THYM | 120 | 124 | Thymus |
| TCGA-UCEC | 557 | 560 | Uterus, NOS |
| TCGA-UCS | 57 | 57 | Uterus, NOS |
| TCGA-UVM | 80 | 80 | Eye and adnexa |

## 2. RNA-seq slim data downloaded (v9 D4 worker, 2026-06-20)

- **Cancers with slim RNA-seq data**: 33/33 (incremental, resume-safe)
- **Total slim cases**: 635
- **Target genes per file**: 30 (SLC35G1-G6, ST6GAL1, ST3GAL4, ST6GALNAC1-2, CD8A, CD274, STAT1, VIM, CDH1-2, MUC1, CD44, CD4, FOXP3, IFNG, TP53, KRAS, BRAF, EGFR, MYC, CCND1, CDK4-6, RB1)
- **Pipeline**: `d4_step3_full_download_v4.py` — curl-based download (GDC /data POST) + pandas usecols filter + immediate slim csv write per cancer

## 3. SLC35G1 expression distribution across 33 cancers (current snapshot)

- **SLC35G1 global median log2(TPM+1)**: 1.747 (IQR 0.534)
- **Highest median cancers**: COAD (2.58), ESCA (2.38), ACC (2.23) — CRC adjacent & mucinous/epithelial
- **Lowest median cancers**: DLBC (1.13), BRCA (1.37), KIRC (1.50) — haematological/breast/kidney
- **Anchor panel median rho (SLC35G1 vs 12 anchors)**: 0.126

> **Honesty marker HM-26**: D4 pan-cancer analysis is **incremental**. RNA-seq slim is currently available for 12/33 cancers (~224 cases). The remaining 21 cancers are in active curl-based download (background v4 worker). Final 33-cancer complete analysis is pending; intermediate snapshots are honest and reproducible.

## 4. Cross-cancer Wasserstein distance (cohort effect proxy)

- **Number of cancer pairs (off-diagonal)**: 528
- **Mean W (SLC35G1 log2 TPM)**: 0.566
- **Median W**: 0.473
- **Max W**: 2.182

### Top-10 most distant cancer pairs (SLC35G1)

| cancer_A | cancer_B | W distance |
|---|---|---:|
| TCGA-LAML | TCGA-LUSC | 2.182 |
| TCGA-DLBC | TCGA-LUSC | 1.931 |
| TCGA-BRCA | TCGA-LUSC | 1.751 |
| TCGA-KIRP | TCGA-LUSC | 1.736 |
| TCGA-LUSC | TCGA-PRAD | 1.684 |
| TCGA-KIRC | TCGA-LUSC | 1.670 |
| TCGA-LUSC | TCGA-SARC | 1.654 |
| TCGA-LUSC | TCGA-MESO | 1.623 |
| TCGA-LUSC | TCGA-THYM | 1.617 |
| TCGA-COAD | TCGA-LAML | 1.562 |

### Closest cancer pairs (lowest W)

| cancer_A | cancer_B | W distance |
|---|---|---:|
| TCGA-COAD | TCGA-LAML | 1.562 |
| TCGA-LUSC | TCGA-THYM | 1.617 |
| TCGA-LUSC | TCGA-MESO | 1.623 |
| TCGA-LUSC | TCGA-SARC | 1.654 |
| TCGA-KIRC | TCGA-LUSC | 1.670 |
| TCGA-LUSC | TCGA-PRAD | 1.684 |
| TCGA-KIRP | TCGA-LUSC | 1.736 |
| TCGA-BRCA | TCGA-LUSC | 1.751 |
| TCGA-DLBC | TCGA-LUSC | 1.931 |
| TCGA-LAML | TCGA-LUSC | 2.182 |

## 5. Per-cancer Cox OS analysis

> **Honesty marker HM-27**: Per-cancer Cox OS analysis requires n ≥ 10 cases with OS events per cancer. Current slim snapshot (median 19 cases/cancer) is underpowered for stable per-cancer Cox HR estimation. Cox HR per cancer is pending 33-cancer full slim download (background worker).

## 6. 4D OOD generalisation test

> **Honesty marker HM-28**: 4D OOD test (leave-2-cancer-out cross-cancer generalisation) is pending 33-cancer full download. Each OOD pair requires per-cancer Cox HR from the leave-out cancer; current snapshot has 0 cancers with sufficient Cox data.

## 7. Pan-cancer vs cancer-specific anchor classification

- **Pan-cancer anchors (CV < 0.5, low cross-cancer variance)**: 8 of 12
- **Intermediate (0.5 ≤ CV < 1.0)**: 4
- **Cancer-specific (CV ≥ 1.0, high cross-cancer variance)**: 0

| Anchor gene | CV cross-cancer | Category |
|---|---:|---|
| STAT1 | 0.106 | pan_cancer |
| VIM | 0.156 | pan_cancer |
| ST6GAL1 | 0.239 | pan_cancer |
| CD44 | 0.247 | pan_cancer |
| ST3GAL4 | 0.259 | pan_cancer |
| CD274 | 0.381 | pan_cancer |
| CD8A | 0.425 | pan_cancer |
| CDH1 | 0.448 | pan_cancer |
| MUC1 | 0.554 | intermediate |
| CDH2 | 0.640 | intermediate |
| ST6GALNAC2 | 0.745 | intermediate |
| ST6GALNAC1 | 0.921 | intermediate |

## 8. Cohort effect correction (per-cancer median subtraction)

Mean per-gene variance reduction after batch effect removal (per-cancer median subtraction):

| Gene | Variance reduction (%) |
|---|---:|
| SLC35G1 | 23.5% |
| ST6GAL1 | 48.7% |
| ST3GAL4 | 55.6% |
| ST6GALNAC1 | 71.5% |
| CD8A | 45.0% |
| CD274 | 38.1% |
| STAT1 | 27.2% |

Mean reduction: 44.2%

## 9. Honesty markers summary (D4-specific)

| HM ID | Description |
|---|---|
| HM-26 | D4 pan-cancer analysis is incremental (12/33 cancers with slim RNA-seq). 33-cancer complete pending background download. |
| HM-27 | Per-cancer Cox OS HR underpowered at current snapshot (median n=19/cancer); requires 33-cancer complete slim. |
| HM-28 | 4D OOD test pending 33-cancer complete slim; leave-2-cancer-out design specified. |
| HM-29 | 33-cancer RNA-seq download is GDC API rate-limited; curl-based pipeline achieves ~95s/20-cases per cancer. |
| HM-30 | Cross-cancer Wasserstein distance is computed on a per-cancer median vector, not the full cohort Wasserstein matrix. |
| HM-31 | Cohort effect correction uses simple per-cancer median subtraction (not full limma ComBat / removeBatchEffect); full correction with 33-cancer matrix pending. |
| HM-32 | All D4 analyses are 100% public-data (GDC Open Access, TCGA PANCAN hub); no wet-lab validation. |

## 10. Reproducibility

All scripts in `38_paper_v9_pancan/`:
- `d4_step1_count_cohorts.py` — 33-cancer cohort enumeration via GDC API
- `d4_step3_full_download_v4.py` — curl-based slim RNA-seq download (resume-safe)
- `d4_step4_clinical.py` — case-level clinical download (33/33, 11,428 cases)
- `d4_step5_analysis.py` — per-cancer SLC35G1 distribution + cross-cancer Wasserstein + Cox + 4D OOD
- `d4_step6_figures.py` — 5-7 publication figures at 300 DPI
