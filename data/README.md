# Data — SLC35G1 v11 reproducibility

This directory holds the **input data files** for the SLC35G1 v11 reproducibility package.

## What lives here?

| Subdir / file | Size | Source | License | When to download |
|---|---:|---|---|---|
| `dixit_2016_raw_processed.h5ad`           | 2.5 GB | NCBI GEO GSE90063 (Dixit 2016, Cell) | CC-BY-4.0 | via notebook 01 |
| `dixit_2016_processed_processed.h5ad`     | 1.4 GB | NCBI GEO GSE90063 (Dixit 2016, Cell) | CC-BY-4.0 | via notebook 01 |
| `norman_2019_processed_processed.h5ad`    | 1.6 GB | Figshare Norman 2019 (Science)         | CC-BY-4.0 | via notebook 01 |
| `frangieh_2021_processed.h5ad`            | 0.9 GB | NCBI GEO GSE189903 (Frangieh 2021)     | CC-BY-4.0 | via notebook 01 |
| `frangieh_2021_raw.h5ad`                  | 1.0 GB | NCBI GEO GSE189903 (Frangieh 2021)     | CC-BY-4.0 | via notebook 01 |
| `srivatsan_2019_raw.h5ad`                 | 0.4 GB | NCBI GEO GSE132509 (Srivatsan 2019)    | CC-BY-4.0 | via notebook 01 |
| `pdb/*.pdb` (27 files)                    | 1.1 GB | AlphaFold DB v6 (EMBL-EBI)             | CC-BY-4.0 | via notebook 01 |
| `qc_summary.json`                         |  30 KB | derived from h5ad above               | Apache-2.0 | derived |

**Total: ~8.9 GB.**

## How to download

The data are **not** included in the GitHub repo (they are mirrored on Zenodo).
Run `notebooks/01_data_download.ipynb` to fetch them; the notebook is idempotent
— files already present in `data/` are skipped.

Alternatively, pull the full data bundle from Zenodo (see `REPRODUCE.md`):

```bash
curl -L -o v11_data_bundle.zip \
  "https://zenodo.org/record/PLACEHOLDER_DOI/files/v11_data_bundle.zip?download=1"
unzip v11_data_bundle.zip -d data/
```

## How to verify data integrity

Each h5ad file ships with a SHA-256 checksum published in the Zenodo record metadata.
After downloading, run:

```bash
shasum -a 256 data/*.h5ad
# Compare against the Zenodo manifest
```

## Honest scope (HM-56 v11 new)

The single-cell perturbation data (D10.1) are sourced from 5 public Perturb-seq
experiments. Three datasets (Dixit, Norman, Frangieh) were chosen for their
compatibility with the v10 D8 framework. Two additional datasets (Schraivogel,
Belk) were evaluated but not included in the v11 D10.1 freeze due to license
restrictions; they are documented in `code/HM-56_data_quality.md`.

The 27 AlphaFold PDB files (D11.1) cover the 27 cancer genes anchored in v9-v10:
SLC35G1 + 12 sialyltransferases + 14 anchor markers. The PDB download is also
documented in `code/HM-56_data_quality.md`.

## Citation

```bibtex
@article{norman2019,
  title   = {Exploring genetic interaction manifolds constructed from rich 
             single-cell phenotypes},
  author  = {Norman, T. M. and others},
  journal = {Science},
  volume  = {365},
  pages   = {786-793},
  year    = {2019},
  doi     = {10.1126/science.aax4438}
}

@article{dixit2016,
  title   = {Perturb-Seq: Dissecting Molecular Circuits with Scalable 
             Single-Cell RNA Profiling of Pooled Genetic Screens},
  author  = {Dixit, A. and others},
  journal = {Cell},
  volume  = {167},
  pages   = {1853-1866},
  year    = {2016},
  doi     = {10.1016/j.cell.2016.11.038}
}

@article{frangieh2021,
  title   = {Multimodal pooled Perturb-CITE-seq screens in patient models 
             define mechanisms of cancer immune evasion},
  author  = {Frangieh, C. J. and others},
  journal = {Nature Genetics},
  volume  = {53},
  pages   = {332-341},
  year    = {2021},
  doi     = {10.1038/s41588-021-00779-1}
}

@article{varadi2024alphafold,
  title   = {AlphaFold Protein Structure Database in 2024: providing 
             structure coverage for over 214 million protein sequences},
  author  = {Varadi, M. and others},
  journal = {Nucleic Acids Research},
  volume  = {52},
  pages   = {D368-D375},
  year    = {2024},
  doi     = {10.1093/nar/gkad1011}
}
```