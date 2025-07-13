# Backend Production Dockerfile
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN addgroup --gid 1001 --system python && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group python

# Change ownership of the app directory
RUN chown -R python:python /app

USER python

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]