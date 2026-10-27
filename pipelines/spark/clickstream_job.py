"""Traitement Spark du clickstream REES46 (bonus).

Démontre un traitement distribuable (PySpark) du flux de navigation : entonnoir
**view → cart → purchase**, taux de conversion et top catégories. Fonctionne sur
l'échantillon généré ; passerait à l'échelle sur le jeu REES46 complet sans
changement de code.

Usage :
    python -m spark.make_sample_clickstream   # génère l'échantillon
    python -m spark.clickstream_job           # lance le traitement
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F  # noqa: N812

from shoppulse.config import ROOT_DIR, SAMPLES_DIR

OUTPUT_DIR = ROOT_DIR / "artifacts" / "spark"


def _configure_windows_spark_home() -> None:
    """Sous Windows, fixe SPARK_HOME au nom court 8.3.

    Le lanceur Spark échoue si le chemin d'installation contient des caractères
    accentués ; le nom court (ex. ``DEUXIM~1``) contourne le problème.
    """
    if sys.platform != "win32" or os.environ.get("SPARK_HOME"):
        return
    import ctypes
    from ctypes import wintypes

    import pyspark

    get_short = ctypes.windll.kernel32.GetShortPathNameW
    get_short.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    buffer = ctypes.create_unicode_buffer(600)
    if get_short(os.path.dirname(pyspark.__file__), buffer, 600):
        os.environ["SPARK_HOME"] = buffer.value
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)


def get_session() -> SparkSession:
    _configure_windows_spark_home()
    return (
        SparkSession.builder.appName("shoppulse-clickstream")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )


def load_events(spark: SparkSession, path: Path) -> DataFrame:
    """Charge le clickstream CSV en DataFrame Spark."""
    return spark.read.csv(str(path), header=True, inferSchema=True)


def funnel(events: DataFrame) -> DataFrame:
    """Compte les événements par étape et calcule les taux de conversion."""
    counts = {
        row["event_type"]: row["n"]
        for row in events.groupBy("event_type").agg(F.count("*").alias("n")).collect()
    }
    views = counts.get("view", 0)
    carts = counts.get("cart", 0)
    purchases = counts.get("purchase", 0)
    spark = events.sparkSession
    data = [
        ("view", views, 1.0),
        ("cart", carts, round(carts / views, 4) if views else 0.0),
        ("purchase", purchases, round(purchases / views, 4) if views else 0.0),
    ]
    return spark.createDataFrame(data, ["stage", "events", "rate_from_view"])


def top_categories(events: DataFrame, limit: int = 5) -> DataFrame:
    """Top catégories par nombre de vues."""
    return (
        events.filter(F.col("event_type") == "view")
        .groupBy("category_code")
        .agg(F.count("*").alias("views"))
        .orderBy(F.desc("views"))
        .limit(limit)
    )


def revenue_by_category(events: DataFrame) -> DataFrame:
    """Chiffre d'affaires simulé par catégorie (événements d'achat)."""
    return (
        events.filter(F.col("event_type") == "purchase")
        .groupBy("category_code")
        .agg(
            F.count("*").alias("purchases"),
            F.round(F.sum("price"), 2).alias("revenue"),
        )
        .orderBy(F.desc("revenue"))
    )


def run(input_path: Path | None = None, output_dir: Path | None = None) -> dict:
    """Exécute le traitement complet et écrit les résultats en CSV."""
    input_path = input_path or (SAMPLES_DIR / "clickstream_sample.csv")
    output_dir = output_dir or OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    spark = get_session()
    try:
        events = load_events(spark, input_path).cache()
        results = {
            "funnel": funnel(events),
            "top_categories": top_categories(events),
            "revenue_by_category": revenue_by_category(events),
        }
        summary = {}
        for name, df in results.items():
            df.coalesce(1).write.mode("overwrite").option("header", True).csv(
                str(output_dir / name)
            )
            summary[name] = df.collect()
        return summary
    finally:
        spark.stop()


def main() -> None:
    summary = run()
    print("Entonnoir :")
    for row in summary["funnel"]:
        print(f"  {row['stage']:<9} {row['events']:>6}  taux={row['rate_from_view']}")
    print("Résultats écrits dans", OUTPUT_DIR)


if __name__ == "__main__":
    main()
