"""Tests des modules modèles : feature engineering, retard, sentiment, équité."""

import numpy as np
import pandas as pd

from shoppulse.features.engineering import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    add_distance,
)
from shoppulse.models import delay, equity, sentiment


def test_haversine_distance_reasonable() -> None:
    # São Paulo -> Rio de Janeiro ~ 360 km
    df = pd.DataFrame(
        {
            "cust_lat": [-23.55],
            "cust_lng": [-46.63],
            "seller_lat": [-22.91],
            "seller_lng": [-43.17],
        }
    )
    out = add_distance(df)
    assert 300 < out["distance_km"].iloc[0] < 450


def _synthetic_delay(n: int = 300) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "distance_km": rng.uniform(0, 2000, n),
            "delai_estime_jours": rng.integers(5, 40, n),
            "poids_total": rng.uniform(100, 5000, n),
            "volume_moy": rng.uniform(100, 50000, n),
            "fret_total": rng.uniform(5, 100, n),
            "prix_total": rng.uniform(10, 500, n),
            "n_items": rng.integers(1, 4, n),
            "seller_order_count": rng.integers(1, 500, n),
            "customer_state": rng.choice(["SP", "RJ", "MG"], n),
            "seller_state": rng.choice(["SP", "RJ"], n),
        }
    )
    # Retard corrélé à la distance (signal apprenable).
    df[TARGET] = (df["distance_km"] + rng.normal(0, 300, n) > 1200).astype(int)
    return df


def test_delay_pipeline_trains_and_importances() -> None:
    df = _synthetic_delay()
    pipe, metrics, test_df = delay.train_best(df, "random_forest")
    assert 0.0 <= metrics["roc_auc"] <= 1.0
    imp = delay.feature_importances(pipe, top=5)
    assert len(imp) == 5
    assert {"feature", "importance"} <= set(imp.columns)
    assert set(test_df.columns) >= set(NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET])


def test_equity_audit_by_region() -> None:
    df = _synthetic_delay(600)
    pipe, _, test_df = delay.train_best(df, "logreg")
    audit = equity.audit_by_region(pipe, test_df, min_count=10)
    assert "region" in audit.columns
    gap = equity.equity_gap(audit)
    assert "ecart_rappel" in gap


def test_sentiment_tokenize_and_vocab() -> None:
    toks = sentiment.tokenize("Produto ótimo, entrega rápida!")
    assert "produto" in toks and "rápida" in toks
    vocab = sentiment.build_vocab(["bom produto", "produto ruim", "bom bom"], min_freq=1)
    assert "<pad>" in vocab and "produto" in vocab


def test_sentiment_baseline_learns() -> None:
    texts = ["produto excelente otimo"] * 20 + ["produto pessimo ruim horrivel"] * 20
    labels = [1] * 20 + [0] * 20
    pipe = sentiment.build_baseline()
    pipe.fit(texts, labels)
    assert pipe.predict(["produto excelente"])[0] == 1
    assert pipe.predict(["pessimo horrivel"])[0] == 0


def test_sentiment_nn_trains_and_predicts() -> None:
    import pytest

    pytest.importorskip("torch", reason="PyTorch requis (extra 'train')")
    texts = ["bom otimo excelente"] * 30 + ["ruim pessimo horrivel"] * 30
    labels = [1] * 30 + [0] * 30
    vocab = sentiment.build_vocab(texts, min_freq=1)
    model, history = sentiment.train_nn(texts, labels, vocab, epochs=3, batch_size=16)
    assert len(history["train_loss"]) == 3
    preds = sentiment.nn_predict(model, ["bom otimo", "ruim pessimo"], vocab)
    assert set(preds).issubset({0, 1})
