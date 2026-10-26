"""Tests des modules d'analyse : RFM, clustering, tests statistiques."""

import numpy as np
import pandas as pd

from shoppulse.analysis import stats
from shoppulse.features.rfm import score_rfm
from shoppulse.features.segmentation import cluster_rfm


def _fake_rfm(n: int = 400) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "customer_unique_id": [f"c{i}" for i in range(n)],
            "recence": rng.integers(1, 700, n),
            "frequence": rng.integers(1, 6, n),
            "montant": rng.gamma(2.0, 80, n).round(2),
        }
    )


def test_score_rfm_ranges_and_columns() -> None:
    scored = score_rfm(_fake_rfm())
    for col in ("R", "F", "M"):
        assert scored[col].between(1, 5).all()
    assert scored["rfm_score"].between(3, 15).all()
    assert scored["segment"].notna().all()


def test_recency_scoring_is_inverted() -> None:
    # Récence faible (achat récent) => score R élevé.
    df = pd.DataFrame(
        {
            "customer_unique_id": list("abcde"),
            "recence": [1, 50, 100, 300, 600],
            "frequence": [1, 1, 1, 1, 1],
            "montant": [10, 20, 30, 40, 50],
        }
    )
    scored = score_rfm(df)
    assert scored.loc[0, "R"] >= scored.loc[4, "R"]


def test_cluster_rfm_assigns_all_and_profiles() -> None:
    scored = score_rfm(_fake_rfm())
    data, profiles = cluster_rfm(scored, k=4)
    assert data["cluster"].nunique() == 4
    assert len(data) == len(scored)
    assert set(profiles.columns) >= {"cluster", "taille", "montant_moy", "part_pct"}
    assert abs(profiles["part_pct"].sum() - 100) < 0.1


def test_stats_detects_late_penalty() -> None:
    # Construit un jeu où les commandes en retard ont des notes plus basses.
    on_time = pd.DataFrame({"delai_jours": [5] * 100, "en_retard": 0, "review_score": [5] * 100})
    late = pd.DataFrame({"delai_jours": [30] * 100, "en_retard": 1, "review_score": [2] * 100})
    df = pd.concat([on_time, late], ignore_index=True)
    r1 = stats.test_late_vs_score(df)
    assert r1.p_value < 0.05
    r2 = stats.test_duration_score_correlation(df)
    assert r2.statistic < 0  # plus long => note plus basse
