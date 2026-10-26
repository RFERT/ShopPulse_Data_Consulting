"""Filtrage de l'intégrité référentielle avant chargement.

Écarte (ou neutralise) les lignes enfants dont la clé étrangère est absente de
la table parente, afin de garantir un chargement sans violation de contrainte.
"""

from __future__ import annotations

import pandas as pd


def _valid_set(df: pd.DataFrame, col: str) -> set:
    return set(df[col].dropna().unique())


def enforce_referential_integrity(
    frames: dict[str, pd.DataFrame], log: list[str]
) -> dict[str, pd.DataFrame]:
    """Aligne les tables enfants sur les clés présentes dans les tables parentes."""
    # products.category -> category_translation (sinon NULL, FK nullable)
    if "products" in frames and "category_translation" in frames:
        valid = _valid_set(frames["category_translation"], "product_category_name")
        prod = frames["products"]
        mask = prod["product_category_name"].notna() & ~prod["product_category_name"].isin(valid)
        n = int(mask.sum())
        if n:
            prod.loc[mask, "product_category_name"] = None
            log.append(f"products: {n} catégorie(s) inconnue(s) mises à NULL")

    customers_ids = (
        _valid_set(frames["customers"], "customer_id") if "customers" in frames else set()
    )
    product_ids = _valid_set(frames["products"], "product_id") if "products" in frames else set()
    seller_ids = _valid_set(frames["sellers"], "seller_id") if "sellers" in frames else set()

    if "orders" in frames and customers_ids:
        frames["orders"] = _filter(frames["orders"], "customer_id", customers_ids, "orders", log)

    order_ids = _valid_set(frames["orders"], "order_id") if "orders" in frames else set()

    for table, fks in {
        "order_items": [
            ("order_id", order_ids),
            ("product_id", product_ids),
            ("seller_id", seller_ids),
        ],
        "order_payments": [("order_id", order_ids)],
        "order_reviews": [("order_id", order_ids)],
    }.items():
        if table not in frames:
            continue
        for col, valid in fks:
            if valid:
                frames[table] = _filter(frames[table], col, valid, table, log)

    return frames


def _filter(df: pd.DataFrame, col: str, valid: set, table: str, log: list[str]) -> pd.DataFrame:
    before = len(df)
    df = df[df[col].isin(valid)]
    removed = before - len(df)
    if removed:
        log.append(f"{table}: {removed} ligne(s) orpheline(s) sur {col} écartée(s)")
    return df.reset_index(drop=True)
