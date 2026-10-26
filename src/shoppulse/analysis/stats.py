"""Deux tests statistiques motivés par une question métier.

Question : « Les retards de livraison dégradent-ils la satisfaction ? »
- Test 1 : la note des avis diffère-t-elle entre commandes à l'heure et en retard ?
  (Mann-Whitney U — notes ordinales, distributions non normales)
- Test 2 : la durée de livraison est-elle corrélée à la note ? (Spearman)
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from scipy import stats

DELIVERY_QUERY = """
SELECT
    DATE_PART('day', o.order_delivered_customer_date - o.order_purchase_timestamp) AS delai_jours,
    CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
         THEN 1 ELSE 0 END AS en_retard,
    r.review_score
FROM orders o
JOIN order_reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
"""


@dataclass
class TestResult:
    name: str
    statistic: float
    p_value: float
    effect: float
    conclusion: str


def load_delivery_satisfaction(engine=None) -> pd.DataFrame:
    """Charge le jeu délai / retard / note depuis la base."""
    from shoppulse.data.db import read_sql

    return read_sql(DELIVERY_QUERY, engine)


def test_late_vs_score(df: pd.DataFrame, alpha: float = 0.05) -> TestResult:
    """Mann-Whitney U : note des avis selon le retard de livraison."""
    on_time = df.loc[df["en_retard"] == 0, "review_score"].dropna()
    late = df.loc[df["en_retard"] == 1, "review_score"].dropna()
    u, p = stats.mannwhitneyu(on_time, late, alternative="greater")
    # Taille d'effet : corrélation rang-bisériale (positive si "à l'heure" mieux noté).
    effect = (2 * u) / (len(on_time) * len(late)) - 1
    sig = "significatif" if p < alpha else "non significatif"
    return TestResult(
        name="Mann-Whitney U — note (à l'heure vs en retard)",
        statistic=float(u),
        p_value=float(p),
        effect=round(float(effect), 4),
        conclusion=(
            f"Les commandes à l'heure obtiennent de meilleures notes ({sig}, p={p:.2e}). "
            f"Écart moyen : {on_time.mean():.2f} vs {late.mean():.2f}."
        ),
    )


def test_duration_score_correlation(df: pd.DataFrame, alpha: float = 0.05) -> TestResult:
    """Spearman : corrélation entre durée de livraison et note."""
    sub = df[["delai_jours", "review_score"]].dropna()
    rho, p = stats.spearmanr(sub["delai_jours"], sub["review_score"])
    sig = "significative" if p < alpha else "non significative"
    return TestResult(
        name="Spearman — durée de livraison vs note",
        statistic=round(float(rho), 4),
        p_value=float(p),
        effect=round(float(rho), 4),
        conclusion=(
            f"Corrélation {sig} (rho={rho:.3f}, p={p:.2e}) : plus la livraison est "
            "longue, plus la note baisse."
        ),
    )
