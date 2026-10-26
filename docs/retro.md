# Rétrospective — ShopPulse

## Ce qui a bien fonctionné
- **Socle conteneurisé dès le départ** : docker-compose (PostgreSQL + Airflow + API +
  Streamlit) a permis un développement cohérent et un « clone & run » fluide.
- **Pipeline ETL découplé de l'orchestrateur** : exécutable en CLI *et* via Airflow,
  ce qui a facilité les tests et l'itération.
- **Code testé en continu** : 28 tests, couverture ~76 %, CI verte — les régressions
  ont été détectées tôt.
- **Modèles compacts** : contrainte de taille sur la Random Forest (288 Mo → 2,4 Mo)
  pour permettre une API autonome versionnée.

## Écarts avec la feuille de route
- Le modèle de retard a un **rappel modéré au seuil 0,5** : le signal (distance, délai
  estimé) est réel mais partiel. Contourné en exposant la **probabilité** et un seuil
  métier abaissé, plutôt qu'une décision binaire rigide.
- **Bonus non traités** (conformément au périmètre) : Spark/REES46, ELK, déploiement
  cloud, MLflow.

## Ce que je referais autrement
- **Enrichir les features** du modèle de retard (historique de délais réels par
  vendeur/transporteur, jours fériés) pour améliorer le rappel.
- **Tuning du seuil** et calibration par région dès l'entraînement.
- Mettre en place **MLflow** tôt pour tracer les expérimentations (gain de temps sur la
  comparaison de modèles).
- Ajouter un **cache applicatif** côté dashboard pour les très gros agrégats.

## Usage de l'IA
Le projet a été mené avec un **agent IA (Copilot)** comme pair-programmeur :
génération de code, structuration, rédaction documentaire et accélération des tâches
répétitives. Les **décisions** (architecture, arbitrages d'outils, choix de modèles,
interprétation métier) et la **validation** (tests, revue, exécution) sont restées sous
la responsabilité de l'auteur. Chaque livrable a été exécuté et vérifié (pipeline,
requêtes SQL, modèles, API conteneurisée).

## Preuves de travail continu
- Historique Git par **branches de fonctionnalité** mergées dans `main` (commits
  conventionnels).
- Deux **points d'étape** (socle données, modèles & industrialisation) — voir
  [backlog.md](backlog.md).
- **CI au vert** sur `main`.
