"""Étape de chargement idempotent vers PostgreSQL.

Le chargement se fait dans une transaction unique : toutes les tables sont
vidées puis rechargées dans l'ordre des clés étrangères. Rejouable sans effet
de bord : relancer le flux produit exactement le même état.
"""

from __future__ import annotations

import pandas as pd
from sqlalchemy import Engine, text

# Colonnes réellement présentes dans le schéma cible (exclut les colonnes
# générées comme les identifiants de substitution).
TABLE_COLUMNS: dict[str, list[str]] = {
    "category_translation": ["product_category_name", "product_category_name_english"],
    "geolocation": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state",
    ],
    "customers": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "sellers": ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"],
    "products": [
        "product_id",
        "product_category_name",
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "order_payments": [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ],
    "order_reviews": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
}


def load_table(df: pd.DataFrame, table: str, conn) -> int:
    """Vide puis recharge une table dans la connexion/transaction fournie."""
    cols = [c for c in TABLE_COLUMNS[table] if c in df.columns]
    subset = df[cols].where(pd.notna(df[cols]), None)
    conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
    subset.to_sql(table, conn, if_exists="append", index=False, method="multi", chunksize=1000)
    return len(subset)


def load_all(
    frames: dict[str, pd.DataFrame], ordered_tables: list[str], engine: Engine
) -> dict[str, int]:
    """Charge toutes les tables de façon idempotente dans une transaction unique."""
    counts: dict[str, int] = {}
    with engine.begin() as conn:
        # Désactive temporairement les contraintes pour l'ordre de TRUNCATE.
        conn.execute(text("SET session_replication_role = 'replica'"))
        for table in ordered_tables:
            counts[table] = load_table(frames[table], table, conn)
        conn.execute(text("SET session_replication_role = 'origin'"))
    return counts
