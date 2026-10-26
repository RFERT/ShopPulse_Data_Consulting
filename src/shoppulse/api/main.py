"""API REST ShopPulse — point d'entrée FastAPI.

Les endpoints de prédiction (retard de livraison, sentiment) sont ajoutés au Lot 5.
Ce module expose dès à présent la racine et le health-check.
"""

from __future__ import annotations

from fastapi import FastAPI

from shoppulse import __version__

app = FastAPI(
    title="ShopPulse API",
    description="API de la plateforme Data & IA ShopPulse (dataset Olist).",
    version=__version__,
)


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    """Message d'accueil de l'API."""
    return {"service": "shoppulse-api", "version": __version__, "docs": "/docs"}


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    """Health-check utilisé par la CI et l'orchestrateur."""
    return {"status": "ok"}
