"""Étape de contrôle qualité : métriques avant/après et rapport."""

from __future__ import annotations

import pandas as pd


def profile(df: pd.DataFrame) -> dict[str, int]:
    """Retourne un profil simple d'un DataFrame (lignes, cellules nulles, doublons)."""
    return {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "null_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def quality_report(before: dict[str, dict], after: dict[str, dict]) -> pd.DataFrame:
    """Construit un rapport qualité avant/après par table."""
    rows = []
    for table in before:
        b, a = before[table], after[table]
        rows.append(
            {
                "table": table,
                "rows_before": b["rows"],
                "rows_after": a["rows"],
                "rows_removed": b["rows"] - a["rows"],
                "null_cells_before": b["null_cells"],
                "null_cells_after": a["null_cells"],
                "duplicate_rows_before": b["duplicate_rows"],
                "duplicate_rows_after": a["duplicate_rows"],
            }
        )
    return pd.DataFrame(rows).sort_values("table").reset_index(drop=True)
