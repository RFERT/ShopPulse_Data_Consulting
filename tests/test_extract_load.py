"""Tests d'extraction (sur échantillons) et d'intégration ETL (si Postgres dispo)."""

from pathlib import Path

import pytest
from shoppulse_etl.datasets import datasets_in_order
from shoppulse_etl.extract import extract

from shoppulse.config import ROOT_DIR

SAMPLES_DIR = ROOT_DIR / "data" / "samples"
pytestmark = pytest.mark.skipif(
    not (SAMPLES_DIR / "olist_orders_dataset.csv").exists(),
    reason="Échantillons absents (data/samples)",
)


def test_extract_renames_product_columns() -> None:
    spec = next(s for s in datasets_in_order() if s.table == "products")
    df = extract(spec, SAMPLES_DIR)
    assert "product_name_length" in df.columns
    assert "product_name_lenght" not in df.columns


def test_extract_parses_order_dates() -> None:
    spec = next(s for s in datasets_in_order() if s.table == "orders")
    df = extract(spec, SAMPLES_DIR)
    assert str(df["order_purchase_timestamp"].dtype).startswith("datetime64")


def test_extract_missing_file_raises() -> None:
    spec = next(s for s in datasets_in_order() if s.table == "orders")
    with pytest.raises(FileNotFoundError):
        extract(spec, Path("chemin/inexistant"))


# --- Intégration : exécute le flux complet sur les échantillons si Postgres répond ---


def _db_available() -> bool:
    try:
        from shoppulse.data.db import ping

        return ping()
    except Exception:
        return False


@pytest.mark.skipif(not _db_available(), reason="PostgreSQL indisponible")
def test_full_etl_on_samples(tmp_path) -> None:
    from shoppulse_etl.flow import run_etl

    from shoppulse.data.db import read_sql

    report = run_etl(SAMPLES_DIR, report_path=tmp_path / "rapport.md")
    assert report["rows_loaded"].sum() > 0
    # Idempotence : relancer ne change pas les comptages
    orders_1 = read_sql("SELECT COUNT(*) AS n FROM orders")["n"].iloc[0]
    run_etl(SAMPLES_DIR, report_path=tmp_path / "rapport2.md")
    orders_2 = read_sql("SELECT COUNT(*) AS n FROM orders")["n"].iloc[0]
    assert orders_1 == orders_2
