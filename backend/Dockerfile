# Backend Dockerfile - FastAPI app served by uvicorn.
# Multi-stage: builder installs deps, runtime runs the app as a non-root user.

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Install build deps for any source distributions, then wheel-install
# requirements into an isolated prefix we copy into the runtime image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ---- runtime ----
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create a non-root user for the app process.
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

WORKDIR /app

# Copy installed dependencies from the builder stage.
COPY --from=builder /install /usr/local

# Copy application source.
COPY . .

# Ensure the SQLite DB lives in a writable data dir.
RUN mkdir -p /app/data && chown -R app:app /app
ENV SQLITE_DB_PATH=/app/data/sql_app.db

USER app

EXPOSE 8000

# Healthcheck hits the /health endpoint; gives the container a startup grace period.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5); sys.exit(0)" || exit 1

# Run migrations (create_all) is implicit on import; seed is optional via env.
CMD ["sh", "-c", "python -c \"import models, database; models.Base.metadata.create_all(bind=database.engine)\" && uvicorn main:app --host 0.0.0.0 --port 8000"]
