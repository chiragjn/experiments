FROM nvcr.io/nvidia/pytorch:24.12-py3
ENV PATH=/virtualenvs/venv/bin:$PATH
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends git && \
    python -m venv /virtualenvs/venv/ && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN --mount=from=ghcr.io/astral-sh/uv:latest,source=/uv,target=/usr/local/bin/uv python -m pip install -U pip setuptools wheel && \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_INDEX_STRATEGY=unsafe-best-match \
    uv pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app
WORKDIR /app