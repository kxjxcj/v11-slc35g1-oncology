#!/usr/bin/env bash
# Codespaces post-create setup
# Target: SLC35G1 v11 reproducibility — minimal install for figure + result verification
#
# Why minimal: full stack (scvi-tools/openmm/geopandas) is 4-5GB and 30+ min.
# Codespaces reviewer use case = verify figures match + check JSON/CSV truth values.
# Full re-run = use the existing ghcr.io image (Option A in REPRODUCE.md).
set -e

echo "==> [postCreate] $(date) — SLC35G1 v11 minimal Codespaces setup"
cd /workspaces/v11-slc35g1-oncology || cd "$(dirname "$0")/.."

# 1. Create conda env (Codespaces miniconda image ships with /opt/conda)
ENV_NAME="slc35g1-cs"
echo "==> [1/4] creating conda env ${ENV_NAME} (Python 3.11)"
conda create -n "${ENV_NAME}" python=3.11 -y -q

# shellcheck disable=SC1091
source /opt/conda/etc/profile.d/conda.sh
conda activate "${ENV_NAME}"

# 2. Install MINIMAL stack (figure + results verification)
echo "==> [2/4] pip install minimal stack (numpy/pandas/sklearn/lifelines/jupyter)"
pip install --quiet --no-cache-dir \
  numpy==1.26.4 \
  pandas==2.1.4 \
  scipy==1.11.4 \
  scikit-learn==1.4.1.post1 \
  matplotlib==3.8.3 \
  seaborn==0.13.2 \
  statsmodels==0.14.1 \
  lifelines==0.27.7 \
  jupyter==1.0.0 \
  jupyterlab==4.1.5 \
  notebook==7.1.1 \
  nbconvert==7.16.0 \
  ipykernel==6.29.2 \
  tqdm==4.66.2 \
  pyyaml==6.0.1

# 3. Register Jupyter kernel
echo "==> [3/4] register Jupyter kernel"
python -m ipykernel install --user --name="${ENV_NAME}" --display-name="SLC35G1 v11 (${ENV_NAME})"

# 4. Smoke test — verify the minimal pipeline loads
echo "==> [4/4] smoke test"
python -c "
import sys, numpy as np, pandas as pd, scipy, sklearn, matplotlib, seaborn, statsmodels, lifelines
print(f'  Python:    {sys.version.split()[0]}')
print(f'  numpy:     {np.__version__}')
print(f'  pandas:    {pd.__version__}')
print(f'  scipy:     {scipy.__version__}')
print(f'  sklearn:   {sklearn.__version__}')
print(f'  lifelines: {lifelines.__version__}')
print(f'  statsmodels: {statsmodels.__version__}')
print('  minimal env: OK')
"

# 5. Print next steps
cat <<'NOTE'
========================================
SLC35G1 v11 — Codespaces ready
========================================

Quick start:
  conda activate slc35g1-cs
  jupyter lab --ip 0.0.0.0 --port 8888 --no-browser

Verify figures (no recompute, just visual sanity):
  python -c "import matplotlib.image as mpimg; img = mpimg.imread('figures/fig01_pancan_slc35g1.png'); print('fig01 OK', img.shape)"

Re-run smoke analysis (Cox + KM on cached results):
  cd notebooks && jupyter nbconvert --to notebook --execute 00_environment_check.ipynb

For full re-run (D4–D11, ~8h, needs heavy deps):
  bash docker/install_full_stack.sh

NOTE

echo "==> [postCreate] done. Welcome to SLC35G1 v11 reproducibility."