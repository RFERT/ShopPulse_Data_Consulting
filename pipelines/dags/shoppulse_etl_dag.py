"""DAG Airflow — pipeline ETL ShopPulse (Olist → PostgreSQL).

Orchestration rejouable : vérification des sources, exécution du flux ETL
(extraction, nettoyage, contrôles qualité, chargement idempotent), puis
validation du chargement.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Rend les packages du projet importables dans le conteneur Airflow.
for p in ("/opt/airflow", "/opt/airflow/src"):
    if p not in sys.path:
        sys.path.insert(0, p)

from airflow.decorators import dag, task  # noqa: E402

SOURCE_DIR = Path("/opt/airflow/data/olist")


@dag(
    dag_id="shoppulse_etl",
    description="Chargement idempotent des 9 CSV Olist dans PostgreSQL",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["shoppulse", "etl"],
)
def shoppulse_etl():
    @task
    def check_sources() -> str:
        from shoppulse_etl.datasets import datasets_in_order

        missing = [s.file for s in datasets_in_order() if not (SOURCE_DIR / s.file).exists()]
        if missing:
            raise FileNotFoundError(f"Fichiers Olist manquants : {missing}")
        return str(SOURCE_DIR)

    @task
    def run_pipeline(source: str) -> dict:
        from shoppulse_etl.flow import run_etl

        report = run_etl(Path(source))
        return {"tables": int(len(report)), "rows_loaded": int(report["rows_loaded"].sum())}

    @task
    def validate_load(summary: dict) -> None:
        from shoppulse.data.db import read_sql

        count = read_sql("SELECT COUNT(*) AS n FROM orders")["n"].iloc[0]
        if count == 0:
            raise ValueError("Chargement invalide : table orders vide.")
        print(f"Validation OK — {count} commandes chargées ; résumé={summary}")

    validate_load(run_pipeline(check_sources()))


shoppulse_etl()
