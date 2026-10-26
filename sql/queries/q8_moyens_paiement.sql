-- Q8 — Répartition des moyens de paiement et usage du paiement échelonné (agrégat)
-- Question métier : comment les clients paient-ils ? (Direction / Finance)
SELECT
    payment_type                                        AS moyen_paiement,
    COUNT(*)                                            AS nb_paiements,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)  AS part_pct,
    ROUND(AVG(payment_value), 2)                        AS montant_moyen,
    ROUND(AVG(payment_installments), 2)                 AS mensualites_moyennes
FROM order_payments
WHERE payment_type IS NOT NULL
GROUP BY payment_type
ORDER BY nb_paiements DESC;
