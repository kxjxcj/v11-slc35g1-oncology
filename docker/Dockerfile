# Base image: miniconda3 with Python 3.11 (matches the dev environment)
FROM continuumio/miniconda3:23.11.0-1 AS base

LABEL maintainer="Mavis reproducibility worker <chen@silicon.com>"
LABEL description="SLC35G1-stratified sialylation precision oncology — v10 final + v11 reproducibility package"
LABEL version="1.0"
LABEL license="Apache-2.0 (code) / CC-BY-4.0 (manuscript)"

# Set shell and non-interactive frontend
SHELL ["/bin/bash", "-lc"]
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# System packages: gcc, git, curl, hdf5, libgomp (GROMACS deps), pandoc (nbconvert)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        git \
        curl \
        wget \
        ca-certificates \
        libhdf5-dev \
        libgomp1 \
        pandoc \
        texlive-xetex \
        texlive-fonts-recommended \
        texlive-plain-generic \
        zip \
        unzip \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user (jovyan is the Jupyter community convention)
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -m -s /bin/bash -u ${NB_UID} ${NB_USER}

WORKDIR /home/${NB_USER}

# --- Python 3.11 conda env ---
COPY docker/environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy && \
    rm -rf /opt/conda/pkgs

# Activate conda env in all subsequent RUN / CMD
ENV PATH="/opt/conda/envs/slc35g1/bin:${PATH}"
SHELL ["conda", "run", "-n", "slc35g1", "/bin/bash", "-lc"]

# --- Copy project files ---
COPY --chown=${NB_USER}:${NB_USER} code/          /home/${NB_USER}/code/
COPY --chown=${NB_USER}:${NB_USER} notebooks/     /home/${NB_USER}/notebooks/
COPY --chown=${NB_USER}:${NB_USER} results/       /home/${NB_USER}/results/
COPY --chown=${NB_USER}:${NB_USER} manuscript/    /home/${NB_USER}/manuscript/
COPY --chown=${NB_USER}:${NB_USER} peer_review/   /home/${NB_USER}/peer_review/
COPY --chown=${NB_USER}:${NB_USER} figures/       /home/${NB_USER}/figures/
COPY --chown=${NB_USER}:${NB_USER} data/          /home/${NB_USER}/data/
COPY --chown=${NB_USER}:${NB_USER} docker/        /home/${NB_USER}/docker/

# Pre-install Jupyter kernel into the conda env
RUN python -m ipykernel install --name slc35g1 --display-name "SLC35G1 (Python 3.11)"

# Make sure the data directory has a stub README so the image is self-describing
# (full data is downloaded at runtime via notebook 01)
RUN echo "Data files are downloaded by notebooks/01_data_download.ipynb." \
       > /home/${NB_USER}/data/README.md && \
    echo "See REPRODUCE.md for the Zenodo DOI." \
       >> /home/${NB_USER}/data/README.md

EXPOSE 8888

# Default entrypoint: Jupyter Lab
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "slc35g1"]
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--ServerApp.token=", \
     "--ServerApp.password=", \
     "--ServerApp.allow_origin='*'", \
     "--notebook-dir=/home/jovyan/notebooks"]

# Healthcheck: ping the Jupyter server
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8888/lab >/dev/null || exit 1