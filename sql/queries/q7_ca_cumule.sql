-- Q7 — Chiffre d'affaires cumulé mensuel (FONCTION DE FENÊTRE : SUM glissant)
-- Question métier : quelle est la trajectoire cumulée du CA et sa croissance ? (Direction)
WITH ca_mensuel AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS mois,
        SUM(oi.price)                                   AS ca
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY 1
)
SELECT
    mois,
    ROUND(ca, 2)                                                       AS ca_mensuel,
    ROUND(SUM(ca) OVER (ORDER BY mois), 2)                             AS ca_cumule,
    ROUND(ca - LAG(ca) OVER (ORDER BY mois), 2)                        AS variation_mois,
    ROUND(AVG(ca) OVER (ORDER BY mois ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2)
                                                                       AS moyenne_mobile_3m
FROM ca_mensuel
ORDER BY mois;
