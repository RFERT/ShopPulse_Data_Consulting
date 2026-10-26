"""Tableau de bord ShopPulse (Streamlit) — 5 indicateurs clés pour la Direction.

Lancement :
    streamlit run dashboards/app.py
Nécessite une base PostgreSQL alimentée (voir docker-compose).
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from shoppulse.analysis.kpis import get_kpis, get_monthly_revenue, get_state_breakdown

st.set_page_config(page_title="ShopPulse — Dashboard", page_icon="📊", layout="wide")

st.title("📊 ShopPulse — Tableau de bord Direction")
st.caption("Vision consolidée de l'activité — données Olist.")


@st.cache_data(ttl=300)
def load():
    return get_kpis(), get_monthly_revenue(), get_state_breakdown()


try:
    kpis, monthly, states = load()
except Exception as exc:  # pragma: no cover - dépend de la base
    st.error(f"Impossible de charger les données depuis PostgreSQL : {exc}")
    st.stop()

# --- 5 indicateurs clés ---
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chiffre d'affaires", f"R$ {kpis['chiffre_affaires']:,.0f}")
c2.metric("Commandes", f"{int(kpis['nb_commandes']):,}")
c3.metric("Panier moyen", f"R$ {kpis['panier_moyen']:,.2f}")
c4.metric("Note moyenne", f"{kpis['note_moyenne']:.2f} / 5")
c5.metric("Taux de retard", f"{kpis['taux_retard_pct']:.1f} %")

st.divider()

# --- Évolution du chiffre d'affaires ---
left, right = st.columns(2)
with left:
    st.subheader("Chiffre d'affaires mensuel")
    fig = px.area(monthly, x="mois", y="chiffre_affaires", labels={"chiffre_affaires": "CA (R$)"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Commandes par mois")
    fig2 = px.bar(monthly, x="mois", y="nb_commandes", labels={"nb_commandes": "Commandes"})
    st.plotly_chart(fig2, use_container_width=True)

# --- Répartition géographique ---
st.subheader("Top 10 des états par volume de commandes")
top_states = states.head(10)
fig3 = px.bar(
    top_states,
    x="etat",
    y="nb_commandes",
    color="note_moyenne",
    color_continuous_scale="RdYlGn",
    labels={"nb_commandes": "Commandes", "note_moyenne": "Note moy."},
)
st.plotly_chart(fig3, use_container_width=True)

st.caption("Source : base PostgreSQL ShopPulse (pipeline ETL Olist).")
