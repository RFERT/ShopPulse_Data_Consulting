"""API REST ShopPulse — point d'entrée FastAPI.

Expose la racine, le health-check et un endpoint de prédiction par modèle :
- ``/predict/retard``   : risque de retard de livraison,
- ``/predict/sentiment``: sentiment d'un avis client (portugais).
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from shoppulse import __version__
from shoppulse.api.predictor import predict_delay, predict_sentiment
from shoppulse.api.schemas import (
    DelayRequest,
    DelayResponse,
    SentimentRequest,
    SentimentResponse,
)

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


@app.post("/predict/retard", response_model=DelayResponse, tags=["predictions"])
def delay_endpoint(payload: DelayRequest) -> DelayResponse:
    """Prédit le risque de retard de livraison d'une commande."""
    try:
        result = predict_delay(payload.model_dump())
    except FileNotFoundError as exc:  # pragma: no cover - modèle absent
        raise HTTPException(status_code=503, detail="Modèle de retard indisponible") from exc
    return DelayResponse(**result)


@app.post("/predict/sentiment", response_model=SentimentResponse, tags=["predictions"])
def predict_sentiment_route(payload: SentimentRequest) -> SentimentResponse:
    """Analyse le sentiment d'un avis client (texte en portugais)."""
    try:
        result = predict_sentiment(payload.texte)
    except FileNotFoundError as exc:  # pragma: no cover - modèle absent
        raise HTTPException(status_code=503, detail="Modèle de sentiment indisponible") from exc
    return SentimentResponse(**result)
