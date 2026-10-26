"""Tests des endpoints de prédiction de l'API (modèles versionnés requis)."""

from fastapi.testclient import TestClient

from shoppulse.api.main import app

client = TestClient(app)

DELAY_PAYLOAD = {
    "distance_km": 450.0,
    "delai_estime_jours": 15,
    "poids_total": 1800,
    "volume_moy": 12000,
    "fret_total": 25.0,
    "prix_total": 180.0,
    "n_items": 1,
    "seller_order_count": 120,
    "customer_state": "RJ",
    "seller_state": "SP",
}


def test_predict_retard_ok() -> None:
    resp = client.post("/predict/retard", json=DELAY_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert 0.0 <= body["probabilite_retard"] <= 1.0
    assert isinstance(body["risque_eleve"], bool)
    assert body["seuil"] == 0.30


def test_predict_retard_validation_error() -> None:
    bad = dict(DELAY_PAYLOAD, n_items=0)  # viole ge=1
    resp = client.post("/predict/retard", json=bad)
    assert resp.status_code == 422


def test_predict_sentiment_positive() -> None:
    resp = client.post("/predict/sentiment", json={"texte": "produto excelente, entrega rápida"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["sentiment"] in {"positif", "négatif"}
    assert 0.0 <= body["probabilite_positif"] <= 1.0


def test_predict_sentiment_empty_text_rejected() -> None:
    resp = client.post("/predict/sentiment", json={"texte": ""})
    assert resp.status_code == 422


def test_openapi_lists_prediction_endpoints() -> None:
    spec = client.get("/openapi.json").json()
    assert "/predict/retard" in spec["paths"]
    assert "/predict/sentiment" in spec["paths"]
