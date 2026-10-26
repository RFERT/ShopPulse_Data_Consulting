"""Feature engineering pour le modèle de prédiction de retard de livraison.

Construit une table au niveau commande à partir de PostgreSQL :
- distance client-vendeur (haversine via géolocalisation),
- délai de livraison estimé,
- poids et dimensions produit, fret, prix,
- historique du vendeur (volume de commandes).
Cible : ``en_retard`` (livraison après la date estimée).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

FEATURE_QUERY = """
WITH geo AS (
    SELECT geolocation_zip_code_prefix AS zip,
           AVG(geolocation_lat) AS lat,
           AVG(geolocation_lng) AS lng
    FROM geolocation
    GROUP BY geolocation_zip_code_prefix
),
seller_hist AS (
    SELECT oi.seller_id, COUNT(DISTINCT oi.order_id) AS seller_order_count
    FROM order_items oi
    GROUP BY oi.seller_id
),
order_feat AS (
    SELECT
        o.order_id,
        o.customer_id,
        c.customer_zip_code_prefix AS cust_zip,
        c.customer_state,
        COUNT(oi.*)                 AS n_items,
        SUM(oi.price)               AS prix_total,
        SUM(oi.freight_value)       AS fret_total,
        SUM(p.product_weight_g)     AS poids_total,
        AVG(p.product_length_cm * p.product_height_cm * p.product_width_cm) AS volume_moy,
        MAX(sh.seller_order_count)  AS seller_order_count,
        -- vendeur principal = celui de l'article le plus cher
        (ARRAY_AGG(s.seller_zip_code_prefix ORDER BY oi.price DESC))[1] AS seller_zip,
        (ARRAY_AGG(s.seller_state ORDER BY oi.price DESC))[1]           AS seller_state,
        DATE_PART('day', o.order_estimated_delivery_date - o.order_purchase_timestamp) AS delai_estime_jours,
        CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
             THEN 1 ELSE 0 END AS en_retard
    FROM orders o
    JOIN customers c    ON c.customer_id = o.customer_id
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products p     ON p.product_id = oi.product_id
    JOIN sellers s      ON s.seller_id = oi.seller_id
    JOIN seller_hist sh ON sh.seller_id = oi.seller_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
      AND o.order_purchase_timestamp IS NOT NULL
    GROUP BY o.order_id, o.customer_id, c.customer_zip_code_prefix, c.customer_state,
             o.order_estimated_delivery_date, o.order_purchase_timestamp,
             o.order_delivered_customer_date
)
SELECT f.*,
       gc.lat AS cust_lat, gc.lng AS cust_lng,
       gs.lat AS seller_lat, gs.lng AS seller_lng
FROM order_feat f
LEFT JOIN geo gc ON gc.zip = f.cust_zip
LEFT JOIN geo gs ON gs.zip = f.seller_zip
"""

NUMERIC_FEATURES = [
    "distance_km",
    "delai_estime_jours",
    "poids_total",
    "volume_moy",
    "fret_total",
    "prix_total",
    "n_items",
    "seller_order_count",
]
CATEGORICAL_FEATURES = ["customer_state", "seller_state"]
TARGET = "en_retard"


def _haversine(lat1, lon1, lat2, lon2):
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return r * 2 * np.arcsin(np.sqrt(a))


def add_distance(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la distance haversine client-vendeur (km)."""
    out = df.copy()
    out["distance_km"] = _haversine(
        out["cust_lat"], out["cust_lng"], out["seller_lat"], out["seller_lng"]
    )
    return out


def build_delay_features(engine=None) -> pd.DataFrame:
    """Charge et construit la table de features du modèle de retard."""
    from shoppulse.data.db import read_sql

    df = read_sql(FEATURE_QUERY, engine)
    df = add_distance(df)
    cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET]
    return df[cols]
