"""Clustering des clients à partir des indicateurs RFM (KMeans).

Fonctions pures (hors I/O) : prennent une table RFM scorée et renvoient les
affectations de clusters et leurs profils, directement exploitables pour écrire
des personas.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

FEATURES = ["recence", "frequence", "montant"]


def cluster_rfm(
    rfm: pd.DataFrame, k: int = 4, random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Segmente les clients par KMeans sur R/F/M (log + standardisation).

    Retourne (table enrichie d'une colonne ``cluster``, profils par cluster).
    """
    data = rfm.copy()
    # Log sur fréquence/montant (distributions très asymétriques).
    x = data[FEATURES].astype(float).copy()
    x["frequence"] = np.log1p(x["frequence"])
    x["montant"] = np.log1p(x["montant"])
    scaled = StandardScaler().fit_transform(x)

    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    data["cluster"] = km.fit_predict(scaled)

    profiles = cluster_profiles(data)
    return data, profiles


def cluster_profiles(data: pd.DataFrame) -> pd.DataFrame:
    """Calcule le profil moyen de chaque cluster (taille, R/F/M, score)."""
    agg = (
        data.groupby("cluster")
        .agg(
            taille=("customer_unique_id", "count"),
            recence_moy=("recence", "mean"),
            frequence_moy=("frequence", "mean"),
            montant_moy=("montant", "mean"),
            rfm_score_moy=("rfm_score", "mean"),
        )
        .round(2)
        .reset_index()
    )
    agg["part_pct"] = (100 * agg["taille"] / agg["taille"].sum()).round(2)
    return agg.sort_values("montant_moy", ascending=False).reset_index(drop=True)
