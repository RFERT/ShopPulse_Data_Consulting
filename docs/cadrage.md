# Note de cadrage — ShopPulse

> Mission Flash — plateforme Data & IA. Consultant data externe. Durée : 10 jours.

## 1. Contexte et enjeux métier

**ShopPulse** est une marketplace e-commerce de taille moyenne (~3 000 vendeurs,
~100 000 clients). Sa direction constate trois irritants :

1. **Données éparpillées** : aucune vision consolidée de l'activité.
2. **Marketing non ciblé** : absence de segmentation, taux de réachat stagnant.
3. **Retards de livraison** : avis négatifs découverts *après coup*, sans anticipation.

La mission consiste à livrer une **plateforme data & IA réduite mais complète** qui
transforme les données brutes Olist en **décisions actionnables** pour quatre
destinataires métier (Marketing, Logistique, Service client, Direction).

## 2. Objectifs économiques

| Irritant | Levier data livré | Impact économique visé |
|---|---|---|
| Pas de vision consolidée | Base PostgreSQL + dashboard 5 KPI | Pilotage factuel, décisions plus rapides |
| Marketing non ciblé | Segmentation RFM + personas + actions chiffrées | **Hausse du réachat**, meilleur ROI campagnes |
| Retards subis | Modèle prédictif de retard servi par API | **Réduction des avis négatifs**, actions logistiques préventives |
| Avis non exploités | Modèle de sentiment (NLP) | Détection précoce de l'insatisfaction |

La valeur se mesure sur trois axes : **CA** (ciblage et réachat), **satisfaction**
(NPS / note moyenne) et **coûts** (anticipation des retards, désengorgement du SAV).

## 3. Utilisateurs et usages

| Utilisateur | Besoin | Interface livrée |
|---|---|---|
| **Direction** | Suivre l'activité d'un coup d'œil | Dashboard Streamlit (5 KPI) |
| **Marketing** | Cibler les bons segments | Personas + recommandations chiffrées |
| **Logistique** | Anticiper les retards | Endpoint API `/predict/retard` |
| **Service client** | Prioriser les avis à risque | Endpoint API `/predict/sentiment` |
| **Équipe data** | Rejouer et fiabiliser les données | Pipeline ETL Airflow, tests, CI |

## 4. Périmètre

**Dans le périmètre** : consolidation PostgreSQL, pipeline ETL rejouable, 8 requêtes
d'analyse, EDA + tests statistiques, segmentation RFM + clustering, 2 modèles
(retard, sentiment), dashboard, API conteneurisée, tests + CI, volet éthique.

**Hors périmètre** (bonus éventuels) : Spark / clickstream REES46, supervision ELK,
déploiement cloud AWS, suivi MLflow.

## 5. Données

Jeu unique : **Brazilian E-Commerce Public Dataset by Olist** (Kaggle) — ~100 000
commandes, **9 fichiers CSV** (commandes, clients, vendeurs, produits, paiements,
avis, géolocalisation, catégories).

**Règles d'usage respectées** :
- Les **données complètes ne sont jamais versionnées** ; seuls des **échantillons
  < 1 Mo** figurent dans [`data/samples/`](../data/samples/).
- Les **avis sont en portugais** → stratégie retenue : **entraînement direct** sur le
  texte portugais (TF-IDF indépendant de la langue pour la baseline, embeddings
  entraînés sur le corpus pour le réseau de neurones). Pas de coût ni de perte de
  traduction. Justification détaillée dans [l'arbitrage](arbitrage.md).
- Toute donnée dérivée est produite par le **pipeline**, jamais à la main.

### Procédure de récupération du jeu complet
```bash
# via l'API Kaggle (nécessite ~/.kaggle/kaggle.json)
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/olist --unzip
# puis
python -m shoppulse_etl.flow --source data/olist
```

## 6. Évolutions probables

- **Industrialisation avancée** : orchestration planifiée, MLflow pour le suivi des
  expérimentations, registre de modèles.
- **Passage à l'échelle** : ingestion Spark du clickstream (REES46), stockage colonne.
- **Temps réel** : scoring des retards à la commande, alertes SAV automatiques.
- **Observabilité** : supervision ELK, monitoring de dérive des modèles.
- **Déploiement cloud** : conteneurs sur AWS (ECS/Fargate), estimation de coût.

## 7. Organisation et livrables

Projet découpé en **5 lots** suivant le cycle de vie de la donnée (cadrage → données
→ analyse → modèles → industrialisation). Suivi dans **GitHub Projects**, branches par
fonctionnalité, commits conventionnels, **deux points d'étape**. Livrables finaux :
dépôt GitHub exécutable (< 30 min) et vidéo de soutenance (10 min).
