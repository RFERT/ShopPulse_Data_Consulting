# Note éthique — ShopPulse

Cette note couvre trois exigences : **biais possibles** des modèles (notamment par
région), **conformité RGPD** des données clients, et **limites d'usage** des prédictions.

## 1. Biais des modèles

### Biais géographique (régional)
Le modèle de retard est audité **par région** (état du client) : on compare le rappel
et le taux de faux positifs d'une région à l'autre (voir `audit d'équité` dans
[rapport_modeles.md](rapport_modeles.md)). Un écart important signifierait que le
modèle sert **moins bien certaines régions** (ex. le Nord, plus éloigné des centres
logistiques du Sud-Est). Risque : sur-signaler les commandes de régions éloignées et
créer un cercle vicieux (dé-priorisation commerciale). **Mesure prise** : suivi de
l'écart inter-régions de rappel/FPR ; si l'écart dépasse un seuil, rééquilibrage
(pondération, calibration par groupe) avant mise en production.

### Biais de déséquilibre de classes
Les retards sont minoritaires (~8 %). Un modèle optimisant l'exactitude ignorerait la
classe utile. **Mesure** : métriques adaptées (PR-AUC, rappel, F1) et `class_weight`
équilibré.

### Biais linguistique (sentiment)
Les avis sont en **portugais** ; le modèle est entraîné directement sur cette langue.
Il ne doit pas être appliqué tel quel à d'autres langues. Les avis très courts ou
ironiques restent mal captés (voir analyse d'erreurs).

## 2. Conformité RGPD

- **Minimisation** : aucune donnée personnelle directe (nom, e-mail) n'est utilisée ;
  les identifiants Olist sont déjà **pseudonymisés** (hachés).
- **Non-versionnement** : les données complètes ne sont **jamais** poussées dans Git ;
  seuls des échantillons < 1 Mo le sont. Aucun secret n'est versionné.
- **Finalité** : les données servent uniquement à l'analyse et à la prédiction décrites
  ici ; pas de revente ni de profilage individuel intrusif.
- **Géolocalisation** : utilisée de façon **agrégée** (préfixe de code postal), pas pour
  localiser un individu.
- **Droit à l'oubli / sécurité** : en production, prévoir purge sur demande, chiffrement
  au repos et accès restreint par variables d'environnement (jamais en clair dans le code).

## 3. Limites d'usage des prédictions

- **Aide à la décision, non automatisation aveugle** : le score de retard doit
  **déclencher une vérification humaine** (relance transporteur), pas une pénalité
  automatique d'un vendeur ou d'une région.
- **Pas de décision individuelle défavorable** fondée uniquement sur le modèle (ni pour
  un client, ni pour un vendeur) — conforme à l'esprit de l'article 22 RGPD.
- **Validité temporelle** : modèles entraînés sur l'historique Olist (2016-2018) ;
  ré-entraînement nécessaire en cas de dérive (nouveaux transporteurs, saisonnalité).
- **Sentiment** : indicatif pour **prioriser** le traitement des avis, pas pour répondre
  automatiquement au client.
- **Transparence** : l'importance des variables et l'audit d'équité sont documentés pour
  permettre une relecture métier.
