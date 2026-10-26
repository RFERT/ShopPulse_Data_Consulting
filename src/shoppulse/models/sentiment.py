"""Analyse de sentiment des avis (texte **portugais**, entraînement direct).

Deux approches comparées :
- **Baseline** : TF-IDF + régression logistique (scikit-learn),
- **Réseau de neurones** : embeddings + moyenne + couche dense (PyTorch),
  avec courbes d'apprentissage et analyse d'erreurs.

Label binaire : avis positif (note >= 4) vs négatif (note <= 3).
"""

from __future__ import annotations

import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from shoppulse.config import MODELS_DIR

REVIEWS_QUERY = """
SELECT review_comment_message AS texte, review_score
FROM order_reviews
WHERE review_comment_message IS NOT NULL
  AND LENGTH(TRIM(review_comment_message)) > 0
"""

SENTIMENT_BASELINE_PATH = MODELS_DIR / "sentiment_baseline.joblib"
POSITIVE_THRESHOLD = 4
_TOKEN_RE = re.compile(r"[a-zà-ú]+")


def load_reviews(engine=None) -> pd.DataFrame:
    """Charge les avis textuels non vides et construit le label binaire."""
    from shoppulse.data.db import read_sql

    df = read_sql(REVIEWS_QUERY, engine)
    df["label"] = (df["review_score"] >= POSITIVE_THRESHOLD).astype(int)
    return df


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(str(text).lower())


# --------------------------------------------------------------------------- #
# Baseline TF-IDF + régression logistique
# --------------------------------------------------------------------------- #
def build_baseline() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=3)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )


def save_baseline(pipe: Pipeline, path: Path = SENTIMENT_BASELINE_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, path)
    return path


def load_baseline(path: Path = SENTIMENT_BASELINE_PATH) -> Pipeline:
    return joblib.load(path)


# --------------------------------------------------------------------------- #
# Réseau de neurones PyTorch (embeddings + moyenne + dense)
# --------------------------------------------------------------------------- #
def build_vocab(texts: list[str], max_size: int = 10000, min_freq: int = 2) -> dict[str, int]:
    from collections import Counter

    counter: Counter = Counter()
    for t in texts:
        counter.update(tokenize(t))
    vocab = {"<pad>": 0, "<unk>": 1}
    for word, freq in counter.most_common(max_size):
        if freq >= min_freq:
            vocab[word] = len(vocab)
    return vocab


def encode(text: str, vocab: dict[str, int], max_len: int = 40) -> list[int]:
    ids = [vocab.get(tok, 1) for tok in tokenize(text)][:max_len]
    if not ids:
        ids = [0]
    return ids + [0] * (max_len - len(ids))


def make_nn(vocab_size: int, embed_dim: int = 32):
    """Construit le réseau de neurones (importé paresseusement : torch requis)."""
    import torch
    from torch import nn

    class SentimentNN(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.embed = nn.EmbeddingBag(vocab_size, embed_dim, mode="mean")
            self.fc = nn.Sequential(
                nn.Linear(embed_dim, 32), nn.ReLU(), nn.Dropout(0.3), nn.Linear(32, 2)
            )

        def forward(self, x):
            return self.fc(self.embed(x))

    _ = torch  # garde la dépendance explicite
    return SentimentNN()


def train_nn(
    texts: list[str],
    labels: list[int],
    vocab: dict[str, int],
    epochs: int = 6,
    batch_size: int = 256,
    lr: float = 1e-3,
    seed: int = 42,
):
    """Entraîne le réseau et renvoie (modèle, historique des pertes train/val)."""
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset

    torch.manual_seed(seed)
    x = torch.tensor([encode(t, vocab) for t in texts], dtype=torch.long)
    y = torch.tensor(labels, dtype=torch.long)
    n_val = max(1, int(0.2 * len(x)))
    perm = torch.randperm(len(x))
    val_idx, tr_idx = perm[:n_val], perm[n_val:]
    train_dl = DataLoader(TensorDataset(x[tr_idx], y[tr_idx]), batch_size=batch_size, shuffle=True)

    model = make_nn(len(vocab))
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = {"train_loss": [], "val_loss": []}

    for _ in range(epochs):
        model.train()
        tot = 0.0
        for xb, yb in train_dl:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            tot += loss.item() * len(xb)
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(x[val_idx]), y[val_idx]).item()
        history["train_loss"].append(round(tot / len(tr_idx), 4))
        history["val_loss"].append(round(val_loss, 4))
    return model, history


def nn_predict(model, texts: list[str], vocab: dict[str, int]) -> np.ndarray:
    import torch

    x = torch.tensor([encode(t, vocab) for t in texts], dtype=torch.long)
    model.eval()
    with torch.no_grad():
        return model(x).argmax(1).numpy()
