-- Q6 — Classement des vendeurs par CA (FONCTION DE FENÊTRE : RANK)
-- Question métier : qui sont nos meilleurs vendeurs et leur poids relatif ? (Direction)
WITH ventes_vendeur AS (
    SELECT
        s.seller_id,
        s.seller_state,
        SUM(oi.price)              AS ca,
        COUNT(DISTINCT oi.order_id) AS nb_commandes
    FROM order_items oi
    JOIN sellers s ON s.seller_id = oi.seller_id
    JOIN orders o  ON o.order_id = oi.order_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY s.seller_id, s.seller_state
)
SELECT
    seller_id,
    seller_state,
    ROUND(ca, 2)                                              AS chiffre_affaires,
    nb_commandes,
    RANK()       OVER (ORDER BY ca DESC)                      AS rang_global,
    RANK()       OVER (PARTITION BY seller_state ORDER BY ca DESC) AS rang_dans_etat,
    ROUND(100.0 * ca / SUM(ca) OVER (), 2)                    AS part_ca_pct
FROM ventes_vendeur
ORDER BY chiffre_affaires DESC
LIMIT 20;
