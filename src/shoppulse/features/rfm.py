"""Calcul et scoring RFM (Récence, Fréquence, Montant) des clients ShopPulse.

``compute_rfm`` interroge PostgreSQL ; ``score_rfm`` est une fonction pure (testable
sans base) qui attribue des scores R/F/M par quintiles et un segment lisible.
"""

from __future__ import annotations

import pandas as pd

RFM_QUERY = """
WITH bornes AS (
    SELECT MAX(order_purchase_timestamp) AS date_ref FROM orders
)
SELECT
    c.customer_unique_id,
    DATE_PART('day', b.date_ref - MAX(o.order_purchase_timestamp))::INT AS recence,
    COUNT(DISTINCT o.order_id)                                          AS frequence,
    SUM(oi.price)                                                       AS montant
FROM orders o
JOIN customers c    ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
CROSS JOIN bornes b
WHERE o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY c.customer_unique_id, b.date_ref
"""


def compute_rfm(engine=None) -> pd.DataFrame:
    """Calcule la table RFM brute depuis la base."""
    from shoppulse.data.db import read_sql

    df = read_sql(RFM_QUERY, engine)
    return score_rfm(df)


def _quintile_score(series: pd.Series, ascending: bool) -> pd.Series:
    """Attribue un score 1..5 par quintiles ; ``ascending=False`` inverse l'échelle."""
    ranks = series.rank(method="first", pct=True)
    scores = ranks.mul(5).apply(lambda x: min(int(x) + 1, 5))
    return scores if ascending else (6 - scores)


def score_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les scores R, F, M (1..5), le score agrégé et un segment lisible."""
    out = df.copy()
    # Récence : plus c'est récent (valeur faible), meilleur est le score.
    out["R"] = _quintile_score(out["recence"], ascending=False)
    out["F"] = _quintile_score(out["frequence"], ascending=True)
    out["M"] = _quintile_score(out["montant"], ascending=True)
    out["rfm_score"] = out["R"] + out["F"] + out["M"]
    out["segment"] = out.apply(_segment_label, axis=1)
    return out


def _segment_label(row: pd.Series) -> str:
    """Traduit les scores RFM en segment marketing lisible."""
    r, f, m = row["R"], row["F"], row["M"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    if r >= 4 and m >= 3:
        return "Clients fidèles"
    if r >= 4:
        return "Nouveaux / prometteurs"
    if r <= 2 and f >= 3:
        return "À risque"
    if r <= 2:
        return "Perdus / dormants"
    return "À développer"
