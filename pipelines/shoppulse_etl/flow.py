"""Orchestration du flux ETL ShopPulse.

Peut être exécuté :
- en ligne de commande : ``python -m shoppulse_etl.flow --source data/olist``
- depuis Airflow (voir ``pipelines/dags/shoppulse_etl_dag.py``).

Le flux est **rejouable** et **idempotent** : relancer produit le même état.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from shoppulse.config import DATA_DIR, ROOT_DIR
from shoppulse.data.db import get_engine
from shoppulse_etl.clean import clean
from shoppulse_etl.datasets import datasets_in_order
from shoppulse_etl.extract import extract
from shoppulse_etl.load import load_all
from shoppulse_etl.quality import profile, quality_report
from shoppulse_etl.referential import enforce_referential_integrity


def run_etl(source_dir: Path, engine=None, report_path: Path | None = None) -> pd.DataFrame:
    """Exécute le flux complet et retourne le rapport qualité avant/après."""
    specs = datasets_in_order()
    before: dict[str, dict] = {}
    after: dict[str, dict] = {}
    frames: dict[str, pd.DataFrame] = {}
    log: list[str] = []

    # 1. Extraction + 2. Nettoyage + profilage avant/après
    for spec in specs:
        raw = extract(spec, source_dir)
        before[spec.table] = profile(raw)
        cleaned = clean(raw, spec, log)
        frames[spec.table] = cleaned

    # 3. Intégrité référentielle
    frames = enforce_referential_integrity(frames, log)
    for spec in specs:
        after[spec.table] = profile(frames[spec.table])

    # 4. Chargement idempotent
    engine = engine or get_engine()
    ordered_tables = [s.table for s in specs]
    counts = load_all(frames, ordered_tables, engine)

    report = quality_report(before, after)
    report["rows_loaded"] = report["table"].map(counts)

    report_path = report_path or (ROOT_DIR / "docs" / "rapport_qualite.md")
    _write_report(report, log, report_path)
    return report


def _write_report(report: pd.DataFrame, log: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Rapport de qualité des données (avant / après)\n"]
    lines.append("Généré automatiquement par le pipeline ETL ShopPulse.\n")
    lines.append(report.to_markdown(index=False))
    lines.append("\n\n## Règles de nettoyage appliquées (traçabilité)\n")
    if log:
        lines.extend(f"- {entry}" for entry in log)
    else:
        lines.append("- Aucune anomalie détectée sur ce lot.")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Flux ETL ShopPulse (Olist → PostgreSQL)")
    parser.add_argument(
        "--source",
        type=Path,
        default=DATA_DIR / "olist",
        help="Répertoire contenant les 9 CSV Olist",
    )
    args = parser.parse_args()
    report = run_etl(args.source)
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
