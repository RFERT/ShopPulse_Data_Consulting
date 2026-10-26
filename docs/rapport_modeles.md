# Rapport des modèles — ShopPulse

## 1. Modèle de retard de livraison

- Observations : **96470** commandes livrées — taux de retard **8.1 %** (classes déséquilibrées).

### Validation croisée (5 plis)

| modele        |   roc_auc |   average_precision |     f1 |   recall |   precision |
|:--------------|----------:|--------------------:|-------:|---------:|------------:|
| baseline      |    0.5009 |              0.0813 | 0.083  |   0.0832 |      0.0828 |
| logreg        |    0.6939 |              0.1641 | 0.2252 |   0.6274 |      0.1372 |
| random_forest |    0.719  |              0.1917 | 0.2539 |   0.5659 |      0.1637 |


### Modèle retenu (Random Forest)
- ROC-AUC : **0.717** · PR-AUC : **0.1993**
- Rappel classe « retard » : **0.551** · F1 : **0.253**

> **Interprétation** : la Random Forest offre le meilleur pouvoir de classement (ROC-AUC/PR-AUC), tandis que la régression logistique équilibrée maximise le rappel (~0,63). Au seuil par défaut de 0,5 le rappel est faible : en production, **le seuil de décision doit être abaissé** pour privilégier le rappel (anticiper un maximum de retards), au prix de la précision. L'API expose la **probabilité** afin de laisser le métier fixer ce seuil.


### Importance des variables

| feature                                |   importance |
|:---------------------------------------|-------------:|
| num__delai_estime_jours                |   0.303919   |
| num__distance_km                       |   0.134089   |
| num__fret_total                        |   0.0701477  |
| cat__customer_state_RJ                 |   0.0673638  |
| num__seller_order_count                |   0.0578289  |
| cat__customer_state_SP                 |   0.0569585  |
| num__volume_moy                        |   0.054458   |
| num__prix_total                        |   0.05406    |
| num__poids_total                       |   0.0489691  |
| cat__seller_state_SP                   |   0.0239468  |
| cat__customer_state_MG                 |   0.0222524  |
| cat__customer_state_infrequent_sklearn |   0.0154525  |
| cat__customer_state_PR                 |   0.0142949  |
| cat__customer_state_BA                 |   0.0107674  |
| cat__seller_state_MG                   |   0.00956909 |


### Audit d'équité par région

Écart de rappel inter-régions : **0.8626** · écart de taux de faux positifs : **0.6774**.

| region   |   effectif |   taux_retard_reel |   taux_retard_prevu |   rappel |   taux_faux_positifs |
|:---------|-----------:|-------------------:|--------------------:|---------:|---------------------:|
| MA       |        154 |             0.2078 |              0.7468 |   0.9375 |               0.6967 |
| CE       |        239 |             0.1548 |              0.6695 |   0.8108 |               0.6436 |
| BA       |        657 |             0.1385 |              0.6621 |   0.7912 |               0.6413 |
| PE       |        338 |             0.1361 |              0.5266 |   0.6087 |               0.5137 |
| MS       |        152 |             0.1316 |              0.6316 |   0.85   |               0.5985 |
| RJ       |       2496 |             0.131  |              0.7095 |   0.9083 |               0.6796 |
| RN       |        101 |             0.1287 |              0.6139 |   0.6923 |               0.6023 |
| PA       |        199 |             0.1005 |              0.3568 |   0.5    |               0.3408 |
| ES       |        391 |             0.0946 |              0.6317 |   0.9459 |               0.5989 |
| RS       |       1006 |             0.0875 |              0.1372 |   0.3295 |               0.1187 |


## 2. Modèle de sentiment (avis en portugais)

- Observations : **40950** avis textuels — part d'avis positifs **64.7 %**.
- **Baseline TF-IDF + régression logistique** : F1 = **0.9148**
- **Réseau de neurones PyTorch** : F1 = **0.8988**


### Courbes d'apprentissage (réseau de neurones)

|   epoch |   train_loss |   val_loss |
|--------:|-------------:|-----------:|
|       1 |       0.6006 |     0.5677 |
|       2 |       0.5199 |     0.4805 |
|       3 |       0.444  |     0.4152 |
|       4 |       0.3878 |     0.3789 |
|       5 |       0.3518 |     0.3524 |
|       6 |       0.3262 |     0.3376 |


### Analyse d'erreurs (baseline) — exemples mal classés

| texte                                                                                                                         |   review_score |   label |
|:------------------------------------------------------------------------------------------------------------------------------|---------------:|--------:|
| Já comprei muitos produtos das Lojas lannister. Contudo, não sei o motivo de não receber e-mais com ofertas de seus produtos. |              5 |       1 |
| Atenciosamente.                                                                                                               |                |         |
| Comprei 2 produtos no pedido 03-49282XXXX! Para um dos produtos, a cadeira, o processo transcorreu super bem!                 |              4 |       1 |
| Porém, o outro produto, até agora só informa que está com atraso no envio!                                                    |                |         |
| Pinhão não serve na fazer 2008                                                                                                |              5 |       1 |
| Excelente produto, correto, bem embalado mas com entrega excessivamente demorada, considerando que o mesmo é um medicamento.  |              3 |       0 |
| Muito rápido na entrega                                                                                                       |              3 |       0 |