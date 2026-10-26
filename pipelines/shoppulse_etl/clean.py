"""Étape de nettoyage : fonctions pures et traçables sur les DataFrames.

Chaque règle est consignée dans un journal (liste de chaînes) pour produire le
rapport de qualité avant/après.
"""

from __future__ import annotations

import pandas as pd

from shoppulse_etl.datasets import DatasetSpec

# Bornes de cohérence métier appliquées au nettoyage.
MAX_REVIEW_SCORE = 5
MIN_REVIEW_SCORE = 1


def drop_duplicates_on_keys(df: pd.DataFrame, spec: DatasetSpec, log: list[str]) -> pd.DataFrame:
    """Supprime les doublons sur les colonnes clés de la spec."""
    if not spec.keys:
        return df
    keys = [k for k in spec.keys if k in df.columns]
    if not keys:
        return df
    before = len(df)
    df = df.drop_duplicates(subset=keys, keep="first")
    removed = before - len(df)
    if removed:
        log.append(f"{spec.table}: {removed} doublon(s) supprimé(s) sur {keys}")
    return df


def strip_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les espaces superflus des colonnes textuelles."""
    obj_cols = df.select_dtypes(include="object").columns
    for col in obj_cols:
        df[col] = df[col].str.strip()
    return df


def clip_review_scores(df: pd.DataFrame, log: list[str]) -> pd.DataFrame:
    """Écarte les notes d'avis hors de l'intervalle [1, 5]."""
    if "review_score" not in df.columns:
        return df
    before = len(df)
    df = df[df["review_score"].between(MIN_REVIEW_SCORE, MAX_REVIEW_SCORE)]
    removed = before - len(df)
    if removed:
        log.append(f"order_reviews: {removed} note(s) hors [1,5] écartée(s)")
    return df


def clean(df: pd.DataFrame, spec: DatasetSpec, log: list[str]) -> pd.DataFrame:
    """Applique l'ensemble des règles de nettoyage traçables à un dataset."""
    df = strip_text_columns(df)
    df = drop_duplicates_on_keys(df, spec, log)
    df = clip_review_scores(df, log)
    return df.reset_index(drop=True)
