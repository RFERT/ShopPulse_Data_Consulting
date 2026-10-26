# Rapport de qualité des données (avant / après)

Généré automatiquement par le pipeline ETL ShopPulse.

| table                |   rows_before |   rows_after |   rows_removed |   null_cells_before |   null_cells_after |   duplicate_rows_before |   duplicate_rows_after |   rows_loaded |
|:---------------------|--------------:|-------------:|---------------:|--------------------:|-------------------:|------------------------:|-----------------------:|--------------:|
| category_translation |            71 |           71 |              0 |                   0 |                  0 |                       0 |                      0 |            71 |
| customers            |         99441 |        99441 |              0 |                   0 |                  0 |                       0 |                      0 |         99441 |
| geolocation          |       1000163 |      1000163 |              0 |                   0 |                  0 |                  261831 |                 261831 |       1000163 |
| order_items          |        112650 |       112650 |              0 |                   0 |                  0 |                       0 |                      0 |        112650 |
| order_payments       |        103886 |       103886 |              0 |                   0 |                  0 |                       0 |                      0 |        103886 |
| order_reviews        |         99224 |        99224 |              0 |              145903 |             145903 |                       0 |                      0 |         99224 |
| orders               |         99441 |        99441 |              0 |                4908 |               4908 |                       0 |                      0 |         99441 |
| products             |         32951 |        32951 |              0 |                2448 |               2461 |                       0 |                      0 |         32951 |
| sellers              |          3095 |         3095 |              0 |                   0 |                  0 |                       0 |                      0 |          3095 |


## Règles de nettoyage appliquées (traçabilité)

- products: 13 catégorie(s) inconnue(s) mises à NULL