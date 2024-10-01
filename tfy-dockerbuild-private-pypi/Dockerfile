FROM python:3.11-slim
ARG JFROG_PYPI_EXTRA_INDEX_URL
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --extra-index-url "$JFROG_PYPI_EXTRA_INDEX_URL"

