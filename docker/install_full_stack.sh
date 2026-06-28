#!/usr/bin/env bash
# Install FULL scientific stack on top of the minimal Codespaces env
# Adds: scanpy/scvi-tools/openmm/geopandas — adds ~4 GB / ~30 min on 4-core.
# Only needed if you want to re-run D4-D11 from scratch.
set -e

ENV_NAME="${ENV_NAME:-slc35g1-cs}"
# shellcheck disable=SC1091
source /opt/conda/etc/profile.d/conda.sh
conda activate "${ENV_NAME}"

echo "==> installing heavy deps (scanpy/scvi-tools/openmm/geopandas) — expect ~30 min"
pip install --quiet --no-cache-dir \
  scanpy==1.9.6 \
  anndata==0.10.7 \
  scvi-tools==1.0.4 \
  scgen==2.1.0 \
  muon==0.1.5 \
  networkx==3.2.1 \
  python-igraph==0.11.4 \
  rdkit==2024.3.3 \
  mdtraj==1.9.9 \
  prolif==2.0.3 \
  openmm==8.1.1 \
  parmed==4.2.2 \
  pybiomart==0.2.0 \
  gseapy==1.1.3 \
  pydeseq2==0.4.4 \
  scrublet==0.2.3 \
  doubletdetection==4.3 \
  bbknn==1.6.0 \
  magic-impute==3.0.0 \
  scvelo==0.2.5 \
  cellrank==2.0.4 \
  pertpy==0.8.0 \
  geopandas==0.14.3 \
  shapely==2.0.2 \
  pyproj==3.6.1 \
  dowhy==0.10 \
  econml==0.16 \
  causal-learn==0.1.3.8

echo "==> full stack installed. To re-run the pipeline:"
echo "    cd code/workflows && snakemake --cores 4 --use-conda"