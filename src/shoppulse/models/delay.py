"""Modèle de prédiction du retard de livraison.

Compare une **baseline** à deux algorithmes, avec validation croisée et des
métriques **adaptées au déséquilibre de classes** (les retards sont minoritaires).
Sauvegarde le meilleur pipeline pour l'API.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from shoppulse.config import MODELS_DIR
from shoppulse.features.engineering import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
)

SCORING = ["roc_auc", "average_precision", "f1", "recall", "precision"]
DELAY_MODEL_PATH = MODELS_DIR / "delay_model.joblib"


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=0.01)),
        ]
    )
    return ColumnTransformer(
        [
            ("num", numeric, NUMERIC_FEATURES),
            ("cat", categorical, CATEGORICAL_FEATURES),
        ]
    )


def candidate_models() -> dict[str, object]:
    return {
        "baseline": DummyClassifier(strategy="stratified", random_state=42),
        "logreg": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=120,
            max_depth=12,
            min_samples_leaf=50,
            max_features="sqrt",
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=42,
        ),
    }


def _pipeline(model) -> Pipeline:
    return Pipeline([("prep", build_preprocessor()), ("clf", model)])


def cross_validate_models(df: pd.DataFrame) -> pd.DataFrame:
    """Validation croisée stratifiée des 3 modèles sur les métriques déséquilibre."""
    x = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    rows = []
    for name, model in candidate_models().items():
        scores = cross_validate(_pipeline(model), x, y, cv=cv, scoring=SCORING, n_jobs=-1)
        row = {"modele": name}
        row.update({m: round(scores[f"test_{m}"].mean(), 4) for m in SCORING})
        rows.append(row)
    return pd.DataFrame(rows)


def train_best(
    df: pd.DataFrame, model_name: str = "random_forest"
) -> tuple[Pipeline, dict, pd.DataFrame]:
    """Entraîne le modèle retenu sur un split train/test.

    Renvoie (pipeline, métriques, jeu de test) ; le jeu de test sert à l'audit d'équité.
    """
    from sklearn.metrics import (
        average_precision_score,
        classification_report,
        roc_auc_score,
    )

    x = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)
    pipe = _pipeline(candidate_models()[model_name])
    pipe.fit(x_tr, y_tr)
    proba = pipe.predict_proba(x_te)[:, 1]
    pred = pipe.predict(x_te)
    metrics = {
        "roc_auc": round(roc_auc_score(y_te, proba), 4),
        "pr_auc": round(average_precision_score(y_te, proba), 4),
        "report": classification_report(y_te, pred, output_dict=True),
    }
    test_df = x_te.copy()
    test_df[TARGET] = y_te
    return pipe, metrics, test_df


def feature_importances(pipe: Pipeline, top: int = 15) -> pd.DataFrame:
    """Importance des variables du modèle d'arbres (après one-hot)."""
    prep = pipe.named_steps["prep"]
    names = prep.get_feature_names_out()
    importances = pipe.named_steps["clf"].feature_importances_
    return (
        pd.DataFrame({"feature": names, "importance": importances})
        .sort_values("importance", ascending=False)
        .head(top)
        .reset_index(drop=True)
    )


def save_model(pipe: Pipeline, path: Path = DELAY_MODEL_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, path, compress=3)
    return path


def load_model(path: Path = DELAY_MODEL_PATH) -> Pipeline:
    return joblib.load(path)
