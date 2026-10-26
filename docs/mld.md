# Modèle Logique de Données (MLD) — ShopPulse / Olist

Le modèle consolide les **9 fichiers CSV Olist** en une base relationnelle PostgreSQL
normalisée. Il distingue les **tables de référence** (catalogue, géographie, acteurs)
des **tables transactionnelles** (commandes et leurs satellites).

## Diagramme entité-association

```mermaid
erDiagram
    customers ||--o{ orders : passe
    orders ||--o{ order_items : contient
    orders ||--o{ order_payments : regle
    orders ||--o{ order_reviews : recoit
    products ||--o{ order_items : reference
    sellers ||--o{ order_items : vend
    category_translation ||--o{ products : traduit

    customers {
        text customer_id PK
        text customer_unique_id
        int  customer_zip_code_prefix
        text customer_city
        char customer_state
    }
    orders {
        text order_id PK
        text customer_id FK
        text order_status
        timestamp order_purchase_timestamp
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }
    order_items {
        text order_id PK,FK
        int  order_item_id PK
        text product_id FK
        text seller_id FK
        numeric price
        numeric freight_value
    }
    order_payments {
        text order_id PK,FK
        int  payment_sequential PK
        text payment_type
        int  payment_installments
        numeric payment_value
    }
    order_reviews {
        bigint review_pk PK
        text review_id
        text order_id FK
        smallint review_score
        text review_comment_message
    }
    products {
        text product_id PK
        text product_category_name FK
        int  product_weight_g
    }
    sellers {
        text seller_id PK
        int  seller_zip_code_prefix
        char seller_state
    }
    category_translation {
        text product_category_name PK
        text product_category_name_english
    }
    geolocation {
        bigint geolocation_id PK
        int  geolocation_zip_code_prefix
        double geolocation_lat
        double geolocation_lng
    }
```

## Choix de modélisation

| Décision | Justification |
|---|---|
| **Clé de substitution** sur `geolocation` et `order_reviews` | Pas de clé naturelle : un préfixe de code postal a plusieurs coordonnées ; un `review_id` peut apparaître sur plusieurs commandes. |
| **Clés composites** `order_items(order_id, order_item_id)` et `order_payments(order_id, payment_sequential)` | Reflètent la granularité réelle (ligne d'article, séquence de paiement). |
| **FK `products.product_category_name` nullable** | Certaines catégories sont absentes de la table de traduction : mises à NULL par le pipeline plutôt que de rejeter la ligne. |
| **`review_score` contraint à [1,5]** | Garantit la cohérence métier dès la base. |
| **Index** sur FK et colonnes de filtre (`order_status`, `order_purchase_timestamp`, `review_score`) | Accélère les requêtes analytiques et le dashboard. |
| **`geolocation` non reliée par FK** | Table de référence géographique rattachée par préfixe de code postal applicatif (jointure analytique, pas contrainte). |

## Correctifs appliqués par le pipeline

- Renommage des colonnes mal orthographiées dans la source Olist :
  `product_name_lenght → product_name_length`, `product_description_lenght → product_description_length`.
- Déduplication sur les clés, nettoyage des espaces, filtrage des orphelins (intégrité référentielle).

Le schéma SQL exécutable est dans [../sql/schema.sql](../sql/schema.sql).
