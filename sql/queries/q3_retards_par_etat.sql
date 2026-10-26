-- Q3 — Taux de retard de livraison par état (agrégat + CASE)
-- Question métier : où les retards sont-ils les plus fréquents ? (Logistique)
-- Une commande est en retard si livrée après la date estimée.
SELECT
    c.customer_state                                       AS etat,
    COUNT(*)                                               AS nb_livrees,
    SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
             THEN 1 ELSE 0 END)                            AS nb_retards,
    ROUND(100.0 * AVG(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
             THEN 1 ELSE 0 END), 2)                        AS taux_retard_pct
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY c.customer_state
HAVING COUNT(*) >= 50
ORDER BY taux_retard_pct DESC;
