# Suivi d'expériences — MLflow (bonus)

Le suivi d'expériences trace les **paramètres**, **métriques** et **artefacts** de
chaque entraînement, pour comparer les runs et garantir la reproductibilité.

## Principe

L'intégration est **optionnelle et non bloquante** : si `mlflow` n'est pas installé
(ou si `SHOPPULSE_MLFLOW=0`), le suivi devient un *no-op* et l'entraînement se
déroule normalement. Le code vit dans [`tracking.py`](../src/shoppulse/models/tracking.py)
et est appelé par [`train.py`](../src/shoppulse/models/train.py).

Ce qui est journalisé :

| Run | Paramètres | Métriques |
|-----|-----------|-----------|
| `delay_random_forest` | modèle, nb d'observations | ROC-AUC, PR-AUC, rappel/F1 classe « retard », écarts d'équité |
| `sentiment_baseline_vs_nn` | nb d'observations, epochs | F1 baseline, F1 réseau de neurones |

L'artefact du modèle de retard (`delay_model.joblib`) est également attaché au run.

## Installation

```bash
pip install -e ".[mlflow]"
```

## Utilisation

**Suivi local (fichier)** — aucun service requis, les runs sont écrits dans une base
SQLite locale `mlflow.db` :

```bash
python -m shoppulse.models.train             # journalise automatiquement
mlflow ui --backend-store-uri sqlite:///mlflow.db   # http://localhost:5000
```

**Serveur MLflow (docker-compose, profil optionnel)** :

```bash
docker compose -f infra/docker-compose.yml --profile tracking up -d mlflow
# puis pointer l'entraînement vers le serveur :
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"   # PowerShell
python -m shoppulse.models.train
```

## Variables d'environnement

| Variable | Rôle | Défaut |
|----------|------|--------|
| `MLFLOW_TRACKING_URI` | Destination du suivi | SQLite local `mlflow.db` |
| `SHOPPULSE_MLFLOW` | `0` désactive le suivi | `1` (actif si installé) |
