"""Définition des 9 jeux de données Olist et de leur mapping vers le schéma.

Chaque entrée décrit :
- ``file`` : nom du CSV source Olist,
- ``table`` : table cible PostgreSQL,
- ``rename`` : renommage de colonnes (corrige notamment les fautes de frappe Olist),
- ``keys`` : colonnes identifiantes servant à la déduplication,
- ``load_order`` : ordre de chargement (respect des clés étrangères).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DatasetSpec:
    file: str
    table: str
    load_order: int
    keys: list[str] = field(default_factory=list)
    rename: dict[str, str] = field(default_factory=dict)
    parse_dates: list[str] = field(default_factory=list)


DATASETS: list[DatasetSpec] = [
    DatasetSpec(
        file="product_category_name_translation.csv",
        table="category_translation",
        load_order=1,
        keys=["product_category_name"],
    ),
    DatasetSpec(
        file="olist_geolocation_dataset.csv",
        table="geolocation",
        load_order=2,
    ),
    DatasetSpec(
        file="olist_customers_dataset.csv",
        table="customers",
        load_order=3,
        keys=["customer_id"],
    ),
    DatasetSpec(
        file="olist_sellers_dataset.csv",
        table="sellers",
        load_order=4,
        keys=["seller_id"],
    ),
    DatasetSpec(
        file="olist_products_dataset.csv",
        table="products",
        load_order=5,
        keys=["product_id"],
        rename={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        },
    ),
    DatasetSpec(
        file="olist_orders_dataset.csv",
        table="orders",
        load_order=6,
        keys=["order_id"],
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    ),
    DatasetSpec(
        file="olist_order_items_dataset.csv",
        table="order_items",
        load_order=7,
        keys=["order_id", "order_item_id"],
        parse_dates=["shipping_limit_date"],
    ),
    DatasetSpec(
        file="olist_order_payments_dataset.csv",
        table="order_payments",
        load_order=8,
        keys=["order_id", "payment_sequential"],
    ),
    DatasetSpec(
        file="olist_order_reviews_dataset.csv",
        table="order_reviews",
        load_order=9,
        keys=["review_id", "order_id"],
        parse_dates=["review_creation_date", "review_answer_timestamp"],
    ),
]


def datasets_in_order() -> list[DatasetSpec]:
    """Retourne les specs triées par ordre de chargement (respect des FK)."""
    return sorted(DATASETS, key=lambda d: d.load_order)
