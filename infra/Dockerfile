# Image de l'API ShopPulse (FastAPI + modèles)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    SHOPPULSE_MODELS_DIR=/app/artifacts/models

WORKDIR /app

# Dépendances système minimales (psycopg2, build)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation du package (couche cache sur pyproject)
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

# Artefacts de modèles (compacts, versionnés via git add -f) pour une API autonome.
COPY artifacts ./artifacts
RUN mkdir -p artifacts/models

EXPOSE 8000

CMD ["uvicorn", "shoppulse.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
