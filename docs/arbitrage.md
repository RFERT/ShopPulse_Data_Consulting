# Arbitrages techniques

Chaque choix d'outil est argumenté selon quatre critères : **coût**, **délai de mise
en œuvre**, **performance/adéquation** et **pérennité**. Deux arbitrages structurants
sont détaillés, suivis d'un récapitulatif de la stack.

## Arbitrage 1 — Orchestrateur ETL : **Airflow** vs Prefect

| Critère | Apache Airflow ✅ | Prefect |
|---|---|---|
| **Coût** | Open-source ; conteneur un peu plus lourd | Open-source ; Prefect Cloud payant au-delà du gratuit |
| **Délai** | Mise en place un peu plus longue (webserver + scheduler + DB) | Démarrage très rapide |
| **Performance / adéquation** | Standard de fait pour l'ETL batch planifié, UI riche, large écosystème d'opérateurs | Très bon en Python pur, plus moderne, mais écosystème plus restreint |
| **Pérennité** | Projet **Apache**, adoption massive en entreprise, compétence très recherchée | Croissance forte mais gouvernance d'éditeur unique |

**Décision : Airflow.** La mission valorise une **chaîne industrialisée standard** et
une **compétence directement transférable en entreprise**. Airflow offre une UI de
supervision claire (indispensable pour démontrer l'orchestration en soutenance) et un
modèle DAG explicite. Le surcoût d'installation est absorbé par **docker-compose**.
Le pipeline reste néanmoins **découplé de l'orchestrateur** (package `shoppulse_etl`
exécutable aussi en CLI), ce qui limite l'adhérence et préserve la réversibilité.

## Arbitrage 2 — Restitution : **Streamlit** vs Metabase

| Critère | Streamlit ✅ | Metabase |
|---|---|---|
| **Coût** | Open-source, aucun service additionnel | Open-source mais service séparé à héberger/maintenir |
| **Délai** | Immédiat, 100 % Python, réutilise le package `shoppulse` | Rapide pour des KPI simples, mais config connexion/UI à part |
| **Performance / adéquation** | Totale maîtrise des 5 KPI, graphiques sur mesure, narration métier | Excellent pour l'exploration ad hoc en libre-service |
| **Pérennité** | Même langage et mêmes dépendances que le reste du projet → un seul socle à maintenir | Outil en plus dans la stack, montée de version indépendante |

**Décision : Streamlit.** Le dashboard doit présenter **5 indicateurs précis** à la
Direction, avec une **narration maîtrisée** et un **déploiement cohérent** (même image
Docker, même connexion PostgreSQL que l'API). Streamlit **unifie la stack** et évite
d'exploiter un service supplémentaire, ce qui réduit le coût de maintenance et le délai
de livraison. Metabase resterait pertinent si le besoin évoluait vers de
l'exploration libre-service par des non-développeurs.

## Arbitrage 3 — Avis en portugais : **entraînement direct** vs traduction

Les avis Olist sont en **portugais**. Trois stratégies possibles : traduire vers
l'anglais, utiliser un modèle multilingue, ou **entraîner directement** sur le texte
portugais. **Décision : entraînement direct.** La baseline **TF-IDF** est agnostique à
la langue (elle apprend le vocabulaire du corpus), et le **réseau de neurones PyTorch**
apprend ses propres embeddings sur le portugais. On évite ainsi le **coût** et la
**perte d'information** de la traduction, tout en gardant un pipeline simple et rejouable.

## Récapitulatif de la stack

| Besoin | Choix | Alternative écartée |
|---|---|---|
| Base consolidée | **PostgreSQL** | — |
| Orchestration ETL | **Airflow** | Prefect |
| Analyse / ML classique | **scikit-learn** | — |
| Réseau de neurones | **PyTorch** | Keras/TensorFlow |
| Restitution | **Streamlit** | Metabase / Superset |
| API | **FastAPI** | Flask |
| Conteneurs | **Docker / docker-compose** | — |
| Qualité & CI | **ruff + pytest + GitHub Actions** | flake8 |
