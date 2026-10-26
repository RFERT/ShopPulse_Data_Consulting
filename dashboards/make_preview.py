"""Génère une capture statique du dashboard (aperçu PNG) depuis la base."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shoppulse.analysis.kpis import get_kpis, get_monthly_revenue, get_state_breakdown

kpis = get_kpis()
monthly = get_monthly_revenue()
states = get_state_breakdown().head(10)

fig = plt.figure(figsize=(14, 8))
fig.suptitle("ShopPulse — Tableau de bord Direction", fontsize=18, fontweight="bold")

# Bandeau KPI
labels = ["Chiffre d'affaires", "Commandes", "Panier moyen", "Note moyenne", "Taux de retard"]
values = [
    f"R$ {kpis['chiffre_affaires']:,.0f}",
    f"{int(kpis['nb_commandes']):,}",
    f"R$ {kpis['panier_moyen']:.2f}",
    f"{kpis['note_moyenne']:.2f} / 5",
    f"{kpis['taux_retard_pct']:.1f} %",
]
for i, (lab, val) in enumerate(zip(labels, values, strict=True)):
    ax = fig.add_axes([0.02 + i * 0.196, 0.78, 0.18, 0.12])
    ax.axis("off")
    ax.text(0.5, 0.7, val, ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.5, 0.2, lab, ha="center", va="center", fontsize=10, color="gray")

# CA mensuel
ax1 = fig.add_axes([0.06, 0.40, 0.4, 0.3])
ax1.fill_between(monthly["mois"], monthly["chiffre_affaires"], color="#4C78A8", alpha=0.6)
ax1.set_title("Chiffre d'affaires mensuel")
ax1.tick_params(axis="x", rotation=45)

# Commandes mensuelles
ax2 = fig.add_axes([0.56, 0.40, 0.4, 0.3])
ax2.bar(monthly["mois"], monthly["nb_commandes"], width=20, color="#72B7B2")
ax2.set_title("Commandes par mois")
ax2.tick_params(axis="x", rotation=45)

# Top états
ax3 = fig.add_axes([0.06, 0.06, 0.9, 0.24])
ax3.bar(states["etat"], states["nb_commandes"], color="#E45756")
ax3.set_title("Top 10 des états par volume de commandes")

fig.savefig("dashboards/apercu_dashboard.png", dpi=90, bbox_inches="tight")
print("capture écrite: dashboards/apercu_dashboard.png")
