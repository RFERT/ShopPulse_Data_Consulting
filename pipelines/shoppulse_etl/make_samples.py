"""Génère des échantillons cohérents (< 1 Mo) des CSV Olist pour le dépôt.

Les données complètes ne sont jamais versionnées. Ces échantillons permettent à
un tiers de rejouer le pipeline sur un volume réduit. On part de N commandes
tirées aléatoirement puis on conserve toutes les lignes liées (cohérence FK).

Usage : python -m shoppulse_etl.make_samples --source data/olist --out data/samples --orders 1500
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

SEED = 42
GEO_SAMPLE = 3000


def make_samples(source: Path, out: Path, n_orders: int = 1500) -> dict[str, int]:
    out.mkdir(parents=True, exist_ok=True)

    orders = pd.read_csv(source / "olist_orders_dataset.csv")
    sample_orders = orders.sample(n=min(n_orders, len(orders)), random_state=SEED)
    order_ids = set(sample_orders["order_id"])
    customer_ids = set(sample_orders["customer_id"])

    items = pd.read_csv(source / "olist_order_items_dataset.csv")
    items = items[items["order_id"].isin(order_ids)]
    product_ids = set(items["product_id"])
    seller_ids = set(items["seller_id"])

    payments = pd.read_csv(source / "olist_order_payments_dataset.csv")
    payments = payments[payments["order_id"].isin(order_ids)]

    reviews = pd.read_csv(source / "olist_order_reviews_dataset.csv")
    reviews = reviews[reviews["order_id"].isin(order_ids)]

    customers = pd.read_csv(source / "olist_customers_dataset.csv")
    customers = customers[customers["customer_id"].isin(customer_ids)]

    products = pd.read_csv(source / "olist_products_dataset.csv")
    products = products[products["product_id"].isin(product_ids)]

    sellers = pd.read_csv(source / "olist_sellers_dataset.csv")
    sellers = sellers[sellers["seller_id"].isin(seller_ids)]

    category = pd.read_csv(source / "product_category_name_translation.csv")

    geo = pd.read_csv(source / "olist_geolocation_dataset.csv")
    geo = geo.sample(n=min(GEO_SAMPLE, len(geo)), random_state=SEED)

    frames = {
        "olist_orders_dataset.csv": sample_orders,
        "olist_order_items_dataset.csv": items,
        "olist_order_payments_dataset.csv": payments,
        "olist_order_reviews_dataset.csv": reviews,
        "olist_customers_dataset.csv": customers,
        "olist_products_dataset.csv": products,
        "olist_sellers_dataset.csv": sellers,
        "product_category_name_translation.csv": category,
        "olist_geolocation_dataset.csv": geo,
    }

    sizes: dict[str, int] = {}
    for name, df in frames.items():
        path = out / name
        df.to_csv(path, index=False, encoding="utf-8")
        sizes[name] = path.stat().st_size
    return sizes


def main() -> None:
    parser = argparse.ArgumentParser(description="Génère des échantillons Olist < 1 Mo")
    parser.add_argument("--source", type=Path, default=Path("data/olist"))
    parser.add_argument("--out", type=Path, default=Path("data/samples"))
    parser.add_argument("--orders", type=int, default=1500)
    args = parser.parse_args()
    sizes = make_samples(args.source, args.out, args.orders)
    for name, size in sizes.items():
        print(f"{name:45s} {size / 1024:8.1f} Ko")
    biggest = max(sizes.values())
    print(f"\nPlus gros échantillon : {biggest / 1024:.1f} Ko (limite 1024 Ko)")


if __name__ == "__main__":
    main()
