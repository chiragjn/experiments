# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Install curl and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Kustomize v5.2.1
RUN KUSTOMIZE_OS=$(uname -s | tr '[:upper:]' '[:lower:]') && \
    KUSTOMIZE_ARCH=$(case $(uname -m) in x86_64) echo "amd64" ;; aarch64) echo "arm64" ;; *) echo "amd64" ;; esac) && \
    curl -L -s "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.2.1/kustomize_v5.2.1_${KUSTOMIZE_OS}_${KUSTOMIZE_ARCH}.tar.gz" | tar xz \
    && mv kustomize /usr/local/bin/ \
    && chmod +x /usr/local/bin/kustomize \
    && kustomize version

# Set working directory
WORKDIR /app

# Configure UV environment
ENV UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install UV and base dependencies
RUN python -m pip install --no-cache-dir -U pip setuptools wheel
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/usr/local/bin/uv uv sync --locked --no-dev --no-install-project

# Copy the rest of the application
COPY ./ ./

# Set up virtual environment path
ENV PATH=/app/.venv/bin:$PATH

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
