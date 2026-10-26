-- Q4 — Satisfaction moyenne par catégorie (jointure multiple + agrégat)
-- Question métier : quelles catégories génèrent les meilleurs/pires avis ? (Service client)
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name, 'inconnue') AS categorie,
    COUNT(DISTINCT r.review_id)        AS nb_avis,
    ROUND(AVG(r.review_score), 2)      AS note_moyenne,
    ROUND(100.0 * AVG(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END), 2) AS pct_avis_negatifs
FROM order_reviews r
JOIN orders o      ON o.order_id = r.order_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p    ON p.product_id = oi.product_id
LEFT JOIN category_translation ct ON ct.product_category_name = p.product_category_name
GROUP BY 1
HAVING COUNT(DISTINCT r.review_id) >= 30
ORDER BY note_moyenne ASC;
