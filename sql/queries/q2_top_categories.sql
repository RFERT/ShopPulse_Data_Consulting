-- Q2 — Top 10 des catégories par chiffre d'affaires (jointure multiple + agrégat)
-- Question métier : quelles catégories rapportent le plus ? (Marketing / Direction)
-- Jointure sur 4 tables : order_items -> products -> category_translation + orders.
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name, 'inconnue') AS categorie,
    COUNT(DISTINCT oi.order_id)  AS nb_commandes,
    ROUND(SUM(oi.price), 2)      AS chiffre_affaires,
    ROUND(AVG(oi.price), 2)      AS prix_moyen
FROM order_items oi
JOIN orders o   ON o.order_id = oi.order_id
JOIN products p ON p.product_id = oi.product_id
LEFT JOIN category_translation ct ON ct.product_category_name = p.product_category_name
WHERE o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY 1
ORDER BY chiffre_affaires DESC
LIMIT 10;
