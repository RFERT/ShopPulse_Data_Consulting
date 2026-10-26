"""Étape d'extraction : lecture des CSV Olist en DataFrames."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from shoppulse_etl.datasets import DatasetSpec


def extract(spec: DatasetSpec, source_dir: Path) -> pd.DataFrame:
    """Lit le CSV correspondant à ``spec`` depuis ``source_dir``."""
    path = source_dir / spec.file
    if not path.exists():
        raise FileNotFoundError(
            f"Fichier source introuvable : {path}. "
            "Récupérez le dataset Olist (voir docs/cadrage.md)."
        )
    df = pd.read_csv(path)
    if spec.rename:
        df = df.rename(columns=spec.rename)
    for col in spec.parse_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df
