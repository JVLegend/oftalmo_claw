FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/uploads

# Non-root user for security
RUN useradd -m -r oftalmo && chown -R oftalmo:oftalmo /app
USER oftalmo

EXPOSE ${PORT:-8000}

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

CMD ["python", "main.py"]
