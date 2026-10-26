"""Audit d'équité du modèle de retard par région (état client).

Mesure, par région, l'écart de performance et de taux de prédiction positive afin
de détecter un biais géographique (exigence éthique du Lot 4).
"""

from __future__ import annotations

import pandas as pd

from shoppulse.features.engineering import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET


def audit_by_region(pipe, df_test: pd.DataFrame, min_count: int = 100) -> pd.DataFrame:
    """Calcule par état client : effectif, taux réel/prévu de retard, rappel, taux de faux positifs."""
    x = df_test[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    data = df_test.copy()
    data["pred"] = pipe.predict(x)
    rows = []
    for region, g in data.groupby("customer_state"):
        if len(g) < min_count:
            continue
        pos = g[TARGET] == 1
        neg = g[TARGET] == 0
        tp = int(((g["pred"] == 1) & pos).sum())
        fn = int(((g["pred"] == 0) & pos).sum())
        fp = int(((g["pred"] == 1) & neg).sum())
        recall = tp / (tp + fn) if (tp + fn) else float("nan")
        fpr = fp / neg.sum() if neg.sum() else float("nan")
        rows.append(
            {
                "region": region,
                "effectif": len(g),
                "taux_retard_reel": round(pos.mean(), 4),
                "taux_retard_prevu": round((g["pred"] == 1).mean(), 4),
                "rappel": round(recall, 4),
                "taux_faux_positifs": round(fpr, 4),
            }
        )
    out = pd.DataFrame(rows).sort_values("taux_retard_reel", ascending=False).reset_index(drop=True)
    return out


def equity_gap(audit: pd.DataFrame) -> dict[str, float]:
    """Résume l'écart d'équité (max-min) sur le rappel et le taux de faux positifs."""
    return {
        "ecart_rappel": round(audit["rappel"].max() - audit["rappel"].min(), 4),
        "ecart_fpr": round(
            audit["taux_faux_positifs"].max() - audit["taux_faux_positifs"].min(), 4
        ),
    }
