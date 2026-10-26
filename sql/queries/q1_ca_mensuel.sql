-- Q1 — Chiffre d'affaires mensuel (agrégat + fonction de date)
-- Question métier : comment évolue le CA mois par mois ? (Direction)
-- Le CA est la somme des prix des articles des commandes livrées ou expédiées.
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS mois,
    COUNT(DISTINCT o.order_id)                      AS nb_commandes,
    ROUND(SUM(oi.price), 2)                         AS chiffre_affaires,
    ROUND(SUM(oi.freight_value), 2)                 AS frais_port
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY 1
ORDER BY 1;
