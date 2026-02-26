# Chapter 13: Containers — Dockerfile for Horizon
FROM python:3.12-slim

LABEL maintainer="asembereng"
LABEL description="Horizon Task Manager — Companion Code"

# Set working directory
WORKDIR /app

# Copy dependency file first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY horizon/ ./horizon/

# Expose the API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the API server
CMD ["python", "-m", "horizon.api"]
