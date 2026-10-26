"""Indicateurs clés (KPI) et agrégats pour le tableau de bord Direction."""

from __future__ import annotations

import pandas as pd

KPI_QUERY = """
WITH ventes AS (
    SELECT o.order_id,
           SUM(oi.price) AS montant
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY o.order_id
),
retards AS (
    SELECT
        AVG(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date
                 THEN 1.0 ELSE 0.0 END) AS taux_retard
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
)
SELECT
    (SELECT ROUND(SUM(montant), 2) FROM ventes)           AS chiffre_affaires,
    (SELECT COUNT(*) FROM ventes)                         AS nb_commandes,
    (SELECT ROUND(AVG(montant), 2) FROM ventes)           AS panier_moyen,
    (SELECT ROUND(AVG(review_score), 2) FROM order_reviews) AS note_moyenne,
    (SELECT ROUND(100 * taux_retard, 2) FROM retards)     AS taux_retard_pct
"""

MONTHLY_QUERY = """
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS mois,
    ROUND(SUM(oi.price), 2)                          AS chiffre_affaires,
    COUNT(DISTINCT o.order_id)                       AS nb_commandes
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status NOT IN ('canceled', 'unavailable')
  AND o.order_purchase_timestamp IS NOT NULL
GROUP BY 1
ORDER BY 1
"""

STATE_QUERY = """
SELECT c.customer_state AS etat,
       COUNT(DISTINCT o.order_id) AS nb_commandes,
       ROUND(AVG(r.review_score), 2) AS note_moyenne
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
LEFT JOIN order_reviews r ON r.order_id = o.order_id
WHERE o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY c.customer_state
ORDER BY nb_commandes DESC
"""


def get_kpis(engine=None) -> dict[str, float]:
    """Retourne les 5 indicateurs clés sous forme de dictionnaire."""
    from shoppulse.data.db import read_sql

    return read_sql(KPI_QUERY, engine).iloc[0].to_dict()


def get_monthly_revenue(engine=None) -> pd.DataFrame:
    from shoppulse.data.db import read_sql

    return read_sql(MONTHLY_QUERY, engine)


def get_state_breakdown(engine=None) -> pd.DataFrame:
    from shoppulse.data.db import read_sql

    return read_sql(STATE_QUERY, engine)
