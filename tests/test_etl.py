"""Tests unitaires et tests de données du pipeline ETL."""

import pandas as pd
from shoppulse_etl.clean import clean, clip_review_scores, drop_duplicates_on_keys
from shoppulse_etl.datasets import DatasetSpec, datasets_in_order
from shoppulse_etl.quality import profile, quality_report
from shoppulse_etl.referential import enforce_referential_integrity


def test_datasets_order_is_complete_and_sorted() -> None:
    specs = datasets_in_order()
    assert len(specs) == 9
    orders = [s.load_order for s in specs]
    assert orders == sorted(orders)
    # category_translation doit être chargée avant products (FK)
    tables = [s.table for s in specs]
    assert tables.index("category_translation") < tables.index("products")
    assert tables.index("orders") < tables.index("order_items")


def test_drop_duplicates_on_keys() -> None:
    spec = DatasetSpec(file="x.csv", table="customers", load_order=1, keys=["customer_id"])
    df = pd.DataFrame({"customer_id": ["a", "a", "b"], "customer_city": ["x", "x", "y"]})
    log: list[str] = []
    out = drop_duplicates_on_keys(df, spec, log)
    assert len(out) == 2
    assert log and "doublon" in log[0]


def test_clip_review_scores_removes_out_of_range() -> None:
    df = pd.DataFrame({"review_score": [1, 5, 0, 6, 3]})
    log: list[str] = []
    out = clip_review_scores(df, log)
    assert set(out["review_score"]) == {1, 5, 3}
    assert log


def test_clean_strips_text_and_dedupes() -> None:
    spec = DatasetSpec(file="x.csv", table="sellers", load_order=1, keys=["seller_id"])
    df = pd.DataFrame({"seller_id": [" s1 ", "s1", "s2"], "seller_city": [" sao ", "sao", "rio"]})
    log: list[str] = []
    out = clean(df, spec, log)
    # après strip, " s1 " et "s1" deviennent identiques → dédupliqués
    assert len(out) == 2
    assert out["seller_city"].iloc[0] == "sao"


def test_profile_and_report() -> None:
    before = {"t": profile(pd.DataFrame({"a": [1, 1, None]}))}
    after = {"t": profile(pd.DataFrame({"a": [1]}))}
    report = quality_report(before, after)
    assert report.loc[0, "rows_removed"] == 2
    assert report.loc[0, "table"] == "t"


def test_referential_integrity_filters_orphans() -> None:
    frames = {
        "category_translation": pd.DataFrame({"product_category_name": ["cat1"]}),
        "customers": pd.DataFrame({"customer_id": ["c1"]}),
        "sellers": pd.DataFrame({"seller_id": ["s1"]}),
        "products": pd.DataFrame(
            {"product_id": ["p1", "p2"], "product_category_name": ["cat1", "inconnue"]}
        ),
        "orders": pd.DataFrame({"order_id": ["o1", "o2"], "customer_id": ["c1", "orphan"]}),
        "order_items": pd.DataFrame(
            {"order_id": ["o1", "o1"], "product_id": ["p1", "p2"], "seller_id": ["s1", "s1"]}
        ),
        "order_payments": pd.DataFrame({"order_id": ["o1", "ghost"]}),
        "order_reviews": pd.DataFrame({"order_id": ["o1"]}),
    }
    log: list[str] = []
    out = enforce_referential_integrity(frames, log)
    # commande orpheline (customer inconnu) retirée
    assert set(out["orders"]["order_id"]) == {"o1"}
    # catégorie inconnue mise à NULL
    assert (
        out["products"]
        .loc[out["products"]["product_id"] == "p2", "product_category_name"]
        .isna()
        .all()
    )
    # paiement rattaché à une commande fantôme retiré
    assert set(out["order_payments"]["order_id"]) == {"o1"}
    assert log
