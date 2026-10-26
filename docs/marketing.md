# Segmentation marketing — personas & recommandations

Analyse issue de la **segmentation RFM** (94 983 clients) puis d'un **clustering
KMeans (k=4)** sur les variables Récence / Fréquence / Montant (log-transformées et
standardisées). Trois personas actionnables en sont dérivés, chacun assorti d'une
**recommandation de campagne chiffrée**.

> Chiffres issus du pipeline sur le jeu Olist complet (CA total ≈ **R$ 13,5 M**,
> note moyenne **4,09/5**, taux de retard **8,1 %**). Hypothèses de conversion
> explicitées et volontairement prudentes.

## Profils des clusters

| Cluster | Part | Récence moy. (j) | Fréquence moy. | Montant moy. (R$) | Lecture |
|---|---|---|---|---|---|
| 1 | 35,0 % | 212 | 1,0 | 251 | Récents, achat unique, **panier élevé** |
| 0 | 28,9 % | 476 | 1,0 | 109 | **Dormants**, anciens, panier moyen |
| 3 | 33,0 % | 202 | 1,0 | 44 | Récents, **petit panier** |
| 2 | 3,0 % | 270 | 2,1 | 260 | **Multi-achats**, valeur élevée |

## Persona 1 — « Victor, le nouvel acheteur à fort potentiel » (cluster 1, 35 %)
- **Qui** : ~33 200 clients, un seul achat récent, panier élevé (R$ 251).
- **Irritant** : ne réachète pas (fréquence = 1), aucun lien de fidélité créé.
- 🎯 **Recommandation chiffrée** : séquence de **relance cross-sell J+30** (e-mail
  personnalisé sur catégories complémentaires). Hypothèse prudente : **5 %** de
  seconde commande au panier moyen → `0,05 × 33 200 × 251 ≈ **R$ 417 000** de CA
  incrémental`.

## Persona 2 — « Lucia, la cliente dormante » (cluster 0, 29 %)
- **Qui** : ~27 500 clients, dernier achat il y a ~476 jours, panier moyen (R$ 109).
- **Irritant** : risque de perte définitive, aucune interaction récente.
- 🎯 **Recommandation chiffrée** : **campagne de réactivation (win-back)** avec offre
  limitée (-15 %). Hypothèse : **3 %** de réactivation → `0,03 × 27 500 × 109 ≈
  **R$ 90 000** de CA récupéré`, et réduction du taux d'attrition.

## Persona 3 — « Marco, le client fidèle premium » (cluster 2, 3 %)
- **Qui** : ~2 900 clients, multi-achats (2,1 commandes), forte valeur (R$ 260).
- **Irritant** : petit effectif mais **CA par tête le plus élevé** → à protéger.
- 🎯 **Recommandation chiffrée** : **programme de fidélité VIP** (accès anticipé,
  livraison prioritaire). Hypothèse : **+0,3 commande/an** sur le segment →
  `2 900 × 0,3 × 260 ≈ **R$ 226 000** de CA incrémental`, avec un fort effet de
  rétention.

## Synthèse

| Campagne | Cible | CA incrémental estimé |
|---|---|---|
| Relance cross-sell J+30 | Nouveaux à fort panier | ~R$ 417 000 |
| Réactivation win-back | Dormants | ~R$ 90 000 |
| Fidélité VIP | Fidèles premium | ~R$ 226 000 |
| **Total** | | **~R$ 733 000** |

> Les campagnes priorisent le **réachat** (principal irritant marketing de ShopPulse).
> Un **audit d'équité** et les limites d'usage figurent dans [ethique.md](ethique.md).
