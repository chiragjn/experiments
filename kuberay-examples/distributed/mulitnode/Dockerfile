FROM --platform=linux/amd64 python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
