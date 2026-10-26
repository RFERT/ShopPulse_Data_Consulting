# ShopPulse — Plateforme Data & IA

> Mission Flash — consultant data pour **ShopPulse**, marketplace e-commerce fictive.
> Jeu de données : **Brazilian E-Commerce Public Dataset by Olist** (Kaggle).

Plateforme data & IA réduite mais complète : base consolidée PostgreSQL, pipeline ETL
rejouable (Airflow), analyses marketing (RFM + clustering), modèles de prédiction
(retard de livraison, sentiment des avis) servis par une **API FastAPI conteneurisée**,
le tout avec tests et CI.

## 🎯 Les 4 questions métier

| Question | Destinataire | Réponse livrée |
|---|---|---|
| Qui sont nos clients et comment les cibler ? | Marketing | Segmentation RFM + clustering, 3 personas, 3 actions chiffrées |
| Quelle commande risque d'arriver en retard ? | Logistique | Modèle de classification servi par l'API |
| Que disent les clients dans leurs avis ? | Service client | Sentiment : baseline TF-IDF vs réseau de neurones |
| Comment se porte l'activité ? | Direction | Tableau de bord Streamlit à 5 indicateurs |

## 🏗️ Architecture

Voir [docs/architecture.md](docs/architecture.md).

Stack : **PostgreSQL** · **Airflow** (ETL) · **scikit-learn / PyTorch** · **FastAPI** ·
**Streamlit** · **Docker** · **GitHub Actions**.

## 📂 Arborescence

```
shoppulse/
├── README.md            # pitch, architecture, installation, démo
├── docs/                # cadrage, arbitrage, architecture, éthique, rétro
├── data/samples/        # échantillons < 1 Mo (jamais les données complètes)
├── sql/                 # schéma et requêtes d'analyse
├── pipelines/           # flux ETL (DAGs Airflow + package ETL)
├── notebooks/           # EDA, statistiques, segmentation, expérimentations
├── src/shoppulse/       # package Python : features, modèles, API
├── tests/               # tests unitaires et tests de données
├── dashboards/          # tableau de bord Streamlit
├── infra/               # Dockerfile, docker-compose
└── .github/workflows/   # CI
```

## 🚀 Installation & lancement

### Prérequis
- Docker / Docker Desktop
- Python 3.11+ (pour le développement hors conteneurs)

### Démarrage complet (recommandé)
```bash
cp .env.example .env
docker compose -f infra/docker-compose.yml up -d
```

Services exposés :
- **API** : http://localhost:8000 — documentation OpenAPI sur http://localhost:8000/docs
- **Dashboard** : http://localhost:8501
- **Airflow** : http://localhost:8080 (admin / admin)
- **PostgreSQL** : localhost:5432

### Développement local
```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows :  .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
ruff check .
pytest
```

## 📊 Données

Les données complètes Olist **ne sont jamais versionnées**. Seuls des échantillons
< 1 Mo figurent dans [data/samples/](data/samples/). La procédure de récupération du
jeu complet (Kaggle) est décrite dans [docs/cadrage.md](docs/cadrage.md).

## 🧪 Qualité & CI

- Lint & format : **ruff**
- Tests : **pytest** (couverture ≥ 50 %)
- CI : **GitHub Actions** (lint → tests → build d'image) — voir [.github/workflows/ci.yml](.github/workflows/ci.yml)

## 🤖 Usage de l'IA

Ce projet a été réalisé avec l'assistance d'un agent IA (Copilot). Les décisions
d'architecture, les arbitrages d'outils et la validation des livrables restent sous
la responsabilité de l'auteur. Détail dans [docs/retro.md](docs/retro.md).

## 👤 Auteur

RFERT — HETIC, 2ᵉ année.
