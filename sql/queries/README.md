# Requêtes SQL d'analyse

8 requêtes documentées répondant à des questions métier. Elles couvrent les
exigences du Lot 2 : **jointures multiples**, **agrégats** et **fonctions de fenêtre**.

| # | Fichier | Thème | Techniques clés |
|---|---------|-------|-----------------|
| 1 | [q1_ca_mensuel.sql](q1_ca_mensuel.sql) | CA mensuel | Agrégat, `DATE_TRUNC` |
| 2 | [q2_top_categories.sql](q2_top_categories.sql) | Top catégories | **Jointure multiple (4 tables)**, agrégat |
| 3 | [q3_retards_par_etat.sql](q3_retards_par_etat.sql) | Retards par état | Agrégat, `CASE`, `HAVING` |
| 4 | [q4_satisfaction_par_categorie.sql](q4_satisfaction_par_categorie.sql) | Satisfaction / catégorie | **Jointure multiple (5 tables)** |
| 5 | [q5_rfm_clients.sql](q5_rfm_clients.sql) | Indicateurs RFM | CTE, agrégat, `CROSS JOIN` |
| 6 | [q6_classement_vendeurs.sql](q6_classement_vendeurs.sql) | Classement vendeurs | **Fonction de fenêtre** `RANK() OVER (PARTITION BY …)` |
| 7 | [q7_ca_cumule.sql](q7_ca_cumule.sql) | CA cumulé & moyenne mobile | **Fonctions de fenêtre** `SUM/LAG/AVG OVER` |
| 8 | [q8_moyens_paiement.sql](q8_moyens_paiement.sql) | Moyens de paiement | Agrégat, fenêtre de ratio |

## Exécution

```bash
# via docker compose (PostgreSQL exposé sur 5432)
psql postgresql://shoppulse:shoppulse@localhost:5432/shoppulse -f sql/queries/q1_ca_mensuel.sql
```
