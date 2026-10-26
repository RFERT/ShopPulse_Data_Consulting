-- Q5 — Indicateurs RFM par client (agrégat + sous-requête)
-- Question métier : récence, fréquence et montant par client (Marketing).
-- Base de la segmentation RFM (Lot 3). La récence est en jours depuis le dernier achat.
WITH bornes AS (
    SELECT MAX(order_purchase_timestamp) AS date_ref FROM orders
)
SELECT
    c.customer_unique_id,
    DATE_PART('day', b.date_ref - MAX(o.order_purchase_timestamp))::INT AS recence_jours,
    COUNT(DISTINCT o.order_id)                                          AS frequence,
    ROUND(SUM(oi.price), 2)                                             AS montant_total
FROM orders o
JOIN customers c   ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
CROSS JOIN bornes b
WHERE o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY c.customer_unique_id, b.date_ref
ORDER BY montant_total DESC;
