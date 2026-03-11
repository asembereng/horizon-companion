# Chapter 13: Containers — Dockerfile for Horizon (Security-Hardened)
FROM python:3.12-slim

LABEL maintainer="asembereng"
LABEL description="Horizon Task Manager — Companion Code"

# (1) Install only what you need; clear the package cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# (2) Copy requirements first so Docker caches the layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# (3) Copy source code after dependencies
COPY horizon/ ./horizon/

# (4) Run as a non-root user
RUN useradd --no-create-home appuser
USER appuser

# Expose the API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the API server
CMD ["python", "-m", "horizon.api"]
