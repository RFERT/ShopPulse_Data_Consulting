# Backlog — ShopPulse

Backlog organisé par **lot** (cycle de vie de la donnée). À reporter dans
**GitHub Projects** (vue Board, une colonne par statut). Les **deux points d'étape**
sont matérialisés par deux issues de jalon.

## Jalons (points d'étape)

- 🏁 **Point d'étape 1 — Socle données** : base consolidée + pipeline ETL rejouable +
  requêtes SQL (fin Lot 2).
- 🏁 **Point d'étape 2 — Modèles & industrialisation** : modèles servis par l'API
  conteneurisée, tests et CI au vert (fin Lot 5).

## Lot 1 — Cadrage
- [x] Note de cadrage (enjeux, objectifs économiques, utilisateurs, évolutions)
- [x] Arbitrages techniques (Airflow vs Prefect, Streamlit vs Metabase, stratégie avis)
- [x] Schéma d'architecture cible
- [x] Backlog initial dans GitHub Projects

## Lot 2 — Données fiables
- [x] Modèle relationnel (MLD) + schéma PostgreSQL (9 tables)
- [x] Pipeline ETL rejouable et idempotent (extraction, qualité, chargement)
- [x] Règles de nettoyage traçables + rapport qualité avant/après
- [x] 8 requêtes SQL d'analyse (jointures multiples, agrégats, fonctions de fenêtre)
- [x] Échantillons < 1 Mo versionnés

## Lot 3 — Analyse et marketing
- [x] EDA documentée (distributions, saisonnalité, géographie)
- [x] Deux tests statistiques motivés par une question métier
- [x] Segmentation RFM + clustering → 3 personas
- [x] 3 recommandations de campagnes chiffrées
- [x] Dashboard Streamlit (5 KPI) branché sur PostgreSQL

## Lot 4 — Modèles
- [x] Feature engineering (distance client-vendeur, délai estimé, poids, historique vendeur)
- [x] Prédiction de retard : baseline + 2 algorithmes, validation croisée, métriques déséquilibre
- [x] Sentiment : baseline TF-IDF vs réseau de neurones PyTorch, courbes, analyse d'erreurs
- [x] Audit d'équité du modèle de retard par région
- [x] Note éthique (1 page)

## Lot 5 — Industrialisation
- [x] API FastAPI (1 endpoint par modèle, validation, OpenAPI)
- [x] Package Python typé et linté (ruff)
- [x] Tests pytest (unitaires + données), couverture ≥ 50 %
- [x] Dockerfile + docker-compose fonctionnels
- [x] CI GitHub Actions (lint, tests, build) au vert

## Finalisation
- [x] README complet (archi, installation, lancement API, captures dashboard)
- [x] Rétrospective (docs/retro.md)
- [x] Support + script de la vidéo de soutenance (10 min)
- [x] Vérification « clone & run < 30 min », aucun secret
