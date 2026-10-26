"""Chargement et mise en cache des modèles servis par l'API."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from shoppulse.features.engineering import CATEGORICAL_FEATURES, NUMERIC_FEATURES

# Seuil métier abaissé pour privilégier le rappel (anticiper les retards).
DELAY_THRESHOLD = 0.30


@lru_cache
def get_delay_model():
    from shoppulse.models.delay import load_model

    return load_model()


@lru_cache
def get_sentiment_model():
    from shoppulse.models.sentiment import load_baseline

    return load_baseline()


def predict_delay(payload: dict) -> dict:
    """Prédit la probabilité de retard à partir des features d'une commande."""
    model = get_delay_model()
    row = pd.DataFrame([{c: payload[c] for c in NUMERIC_FEATURES + CATEGORICAL_FEATURES}])
    proba = float(model.predict_proba(row)[0, 1])
    return {
        "probabilite_retard": round(proba, 4),
        "risque_eleve": proba >= DELAY_THRESHOLD,
        "seuil": DELAY_THRESHOLD,
    }


def predict_sentiment(texte: str) -> dict:
    """Prédit le sentiment (positif/négatif) d'un avis en portugais."""
    model = get_sentiment_model()
    proba_pos = float(model.predict_proba([texte])[0, 1])
    return {
        "sentiment": "positif" if proba_pos >= 0.5 else "négatif",
        "probabilite_positif": round(proba_pos, 4),
    }
