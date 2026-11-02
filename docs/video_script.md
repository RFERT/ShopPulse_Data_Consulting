# Support & script de la vidéo de soutenance (10 min max)

> Vidéo **face caméra**, l'auteur visible tout au long. Support (slides) rendu avec la
> vidéo. La trame des 7 points est **imposée** par l'énoncé ; les bonus sont glissés au
> fil de l'eau. Minutage indicatif (cible : **9 min 30**, marge de sécurité).
>
> Ce document contient **deux versions** du même déroulé :
> - **Version A — texte complet** : à lire/répéter, formulations prêtes à l'emploi.
> - **Version B — notes rapides** : puces type prompteur, à garder sous les yeux pendant le tournage.

---

## 🎬 Idées de présentation (créatives · pro · un peu drôles)

Choisis-en 2-3, n'en abuse pas — l'énoncé évalue le fond.

- **Fil rouge narratif** : suis **une seule commande** du début à la fin — « Victor commande un casque audio à São Paulo ». Elle sert d'exemple pour l'ETL, le dashboard, la prédiction de retard et le sentiment de son avis. Fil conducteur mémorable.
- **Hook d'ouverture (5 s)** : *« Vous offrez un cadeau d'anniversaire. Il arrive 3 jours trop tard. Vous mettez 1 étoile. Maintenant, multipliez par des milliers de commandes : voilà le problème de ShopPulse. »* Puis on enchaîne.
- **Tagline récurrente** : répète une courte phrase à 2-3 moments → *« De la donnée brute à la décision. »* Donne un rythme et une signature.
- **Structure Avant / Après** : slide coupée en deux (données éparpillées & décisions au doigt mouillé → base consolidée & décisions chiffrées).
- **Touche d'humilité drôle (point 5)** : *« Mon réseau de neurones PyTorch s'est fait battre par une régression logistique des années 50. Leçon : commencer simple, et laisser l'ego au vestiaire. »* (la baseline TF-IDF F1 0,91 > NN F1 0,90). Sincère et pro.
- **Démo live dramatisée** : tape un avis en portugais *en direct* (« produto excelente, entrega rápida ») → sentiment positif à l'écran. L'effet « ça marche vraiment » est fort.
- **Prop physique (optionnel)** : un petit colis en carton posé à côté de toi ; tu le montres quand tu parles de retard de livraison. Visuel, un peu décalé, pro.
- **Chiffre-choc affiché en grand** : « **733 000 R$** de CA incrémental estimé » seul sur une slide, laissé 2 secondes en silence.
- **Clin d'œil bonus** : *« L'énoncé proposait 4 bonus. Je les ai tous pris — mais rangés dans des tiroirs optionnels pour que le projet reste clonable en moins de 30 minutes. »*
- **Punchline de fin** : *« ShopPulse a commencé avec des données éparpillées et des retards subis. Il repart avec une plateforme, des réponses chiffrées et un modèle qui anticipe. Merci. »*

**Conseils de forme** : regarde l'objectif (pas l'écran), souris à l'intro/outro, change de plan toutes les ~90 s (slide ↔ visage ↔ démo), montre la **CI verte** et le **repo** au moins une fois.

---
---

# VERSION A — Texte complet (à lire / répéter)

## 1. Le problème de ShopPulse et la valeur apportée — 1 min
> *Slide : logo + « 3 irritants → 3 leviers ».*

« Bonjour, je suis RFERT, consultant data pour ShopPulse, une marketplace fictive de
3 000 vendeurs et 100 000 clients.

Imaginez : vous offrez un cadeau, il arrive trois jours trop tard, vous mettez une
étoile. Multipliez par des milliers de commandes — c'est, en résumé, le problème de
ShopPulse. Concrètement, trois irritants : des **données éparpillées**, un **marketing
non ciblé**, et des **retards de livraison subis** qui génèrent des avis négatifs.

Ma mission : transformer ça en décisions. J'ai livré une **plateforme data & IA** qui
répond à **quatre questions métier** par quatre réponses actionnables — de la donnée
brute à la décision. C'est le fil de cette présentation. »

## 2. Architecture et arbitrages techniques — 1 min 30
> *Slide : diagramme `docs/architecture.md` + petit tableau d'arbitrage.*

« Voici la chaîne de bout en bout : les données Olist passent par un **ETL orchestré
avec Airflow**, atterrissent dans **PostgreSQL**, sont exploitées par les analyses et
les modèles, puis servies par une **API FastAPI** et un **dashboard Streamlit**. Le tout
est **conteneurisé** avec Docker et validé par une **CI GitHub Actions**.

Deux arbitrages que j'assume. **Airflow plutôt que Prefect** : c'est le standard du
marché, avec une interface de supervision et une compétence directement transférable en
entreprise. **Streamlit plutôt que Metabase** : je garde une stack Python unifiée, donc
un déploiement cohérent et moins de pièces mobiles. Chaque choix est documenté dans la
note d'arbitrage. »

## 3. Les données : pipeline et qualité — 1 min 30
> *Slide : `docs/mld.md` + extrait `docs/rapport_qualite.md`.*

« Les données reposent sur un **modèle relationnel de 9 tables**. Le pipeline de
chargement est **idempotent et rejouable** : je peux le relancer autant de fois que je
veux, j'obtiens le même état, sans doublon. À chaque exécution, des **contrôles qualité**
produisent un **rapport avant/après** — valeurs manquantes, dates incohérentes,
référentiels.

Point important sur la rigueur : seuls des **échantillons de moins d'un méga-octet** sont
versionnés ; les données complètes ne sont **jamais** poussées sur le dépôt. Toute donnée
dérivée sort du pipeline, jamais d'une manipulation manuelle. »

## 4. Les réponses métier : dashboard, segmentation, recommandations — 2 min 30
> *Slide : `dashboards/apercu_dashboard.png` puis `docs/marketing.md`.*

« Première livraison métier : un **tableau de bord à 5 indicateurs** branché sur
PostgreSQL. Les chiffres clés : un **chiffre d'affaires de 13,5 millions de réais**, une
**note moyenne de 4,09 sur 5**, et **8,1 % de commandes en retard**.

Ensuite, la **segmentation**. Sur près de **95 000 clients**, j'ai calculé un score
**RFM** — Récence, Fréquence, Montant — puis un **clustering KMeans** qui fait émerger
trois personas. **Victor**, le nouvel acheteur à fort potentiel qui ne réachète pas.
**Lucia**, la cliente dormante depuis plus d'un an. Et **Marco**, le fidèle premium, petit
effectif mais plus gros panier par tête.

À chaque persona, une **campagne chiffrée** avec des hypothèses prudentes : relance
cross-sell pour Victor, réactivation win-back pour Lucia, programme VIP pour Marco. Au
total, une estimation de **733 000 réais de chiffre d'affaires incrémental**.

Enfin, deux **tests statistiques** pour valider une intuition métier : un test de
Mann-Whitney confirme que les commandes en retard **dégradent significativement** la
note — environ **2,6 sur 5 contre 4,3** pour les commandes à l'heure, avec une p-value
quasi nulle. Le retard n'est pas un détail logistique : c'est un sujet de satisfaction. »

## 5. Les modèles : performances, interprétation, limites et biais — 2 min
> *Slide : `docs/rapport_modeles.md` + `docs/ethique.md`.*

« Deux modèles. Le premier **prédit le risque de retard**. J'ai comparé une **baseline**,
une **régression logistique** et une **random forest**, avec des métriques adaptées au
**déséquilibre de classes** — les retards sont minoritaires. La forêt obtient un
**ROC-AUC de 0,72**, les variables les plus importantes étant la **distance** et le
**délai estimé**. Comme le rappel au seuil 0,5 est faible, l'**API expose la probabilité**
et j'abaisse le seuil de décision à 0,30 : mieux vaut anticiper un retard et se tromper
parfois, que de le rater.

Le second analyse le **sentiment des avis**, directement **en portugais**. Et là, un
aveu d'humilité : mon **réseau de neurones PyTorch s'est fait battre par une régression
logistique sur TF-IDF** — F1 de 0,91 contre 0,90. La leçon : commencer simple, et garder
la baseline comme juge de paix.

Côté **éthique et biais** : j'ai mené un **audit d'équité par région**. Le modèle de
retard n'est pas uniforme — l'écart de rappel entre régions atteint 0,22. Je le
documente, avec les contraintes RGPD et les limites d'usage, parce qu'un modèle qu'on
déploie sans en connaître les angles morts est un risque, pas un atout. »

## 6. Démonstration de l'API conteneurisée — 1 min
> *À MONTRER EN DIRECT. Slide de repli : capture de `localhost:8000/docs`.*

« Place à la démo. Je lance toute la plateforme avec une seule commande Docker Compose,
puis j'interroge l'API.

Je teste d'abord le sentiment, avec un vrai avis en portugais. »

```bash
docker compose -f infra/docker-compose.yml up -d
curl -X POST localhost:8000/predict/sentiment -H "Content-Type: application/json" \
     -d '{"texte":"produto excelente, entrega rápida"}'
# -> {"sentiment":"positif","probabilite_positif":0.97}
```

« Positif à 97 %. Et maintenant une commande à risque — longue distance, délai estimé
large : »

```bash
curl -X POST localhost:8000/predict/retard -H "Content-Type: application/json" \
     -d '{"distance_km":450,"delai_estime_jours":15,"poids_total":1800,"volume_moy":12000,
          "fret_total":25,"prix_total":180,"n_items":1,"seller_order_count":120,
          "customer_state":"RJ","seller_state":"SP"}'
# -> {"probabilite_retard":0.73,"risque_eleve":true,"seuil":0.3}
```

« Risque élevé, 73 %. L'API renvoie la probabilité et laisse le métier fixer le seuil.
Tout ça documenté automatiquement en OpenAPI. »

## 7. Bilan : écarts, bonus et ce que je referais — 30 s
> *Slide : `docs/retro.md` + CI verte affichée.*

« Pour conclure : les **cinq lots sont livrés, la CI est verte**. J'ai aussi traité les
**quatre bonus** de l'énoncé — suivi d'expériences MLflow, supervision ELK, traitement
Spark du clickstream, et déploiement cloud AWS chiffré — rangés dans des **profils
optionnels** pour que le projet reste clonable en moins de 30 minutes.

Mon principal **axe d'amélioration** : le rappel du modèle de retard, en enrichissant les
features — historique réel par vendeur, jours fériés — et en calibrant le seuil par
région.

ShopPulse est parti de données éparpillées et de retards subis. Il repart avec une
plateforme, des réponses chiffrées et un modèle qui anticipe. Merci de votre attention. »

---
---

# VERSION B — Notes rapides (prompteur / tournage)

> Puces télégraphiques. Garde-les à hauteur d'objectif. Un bloc = ~une respiration.

## 1. Problème & valeur — 1 min
- Moi : RFERT, consultant data. ShopPulse = marketplace, **3 000 vendeurs / 100 000 clients**.
- Hook : *cadeau en retard → 1 étoile → ×1000*.
- **3 irritants** : données éparpillées · marketing non ciblé · retards subis.
- Livré : plateforme data & IA → **4 questions métier = 4 réponses**.
- Tagline : *« de la donnée brute à la décision »*.

## 2. Archi & arbitrages — 1 min 30
- Chaîne : **Olist → ETL Airflow → PostgreSQL → analyse/ML → API FastAPI + dashboard Streamlit**.
- Conteneurisé **Docker** + **CI GitHub Actions**.
- **Airflow vs Prefect** : standard, UI supervision, compétence transférable.
- **Streamlit vs Metabase** : stack Python unifiée, déploiement cohérent.
- → montrer le **diagramme**.

## 3. Données : pipeline & qualité — 1 min 30
- MLD **9 tables**.
- Chargement **idempotent & rejouable** (relance = même état, pas de doublon).
- **Contrôles qualité** → rapport **avant/après**.
- **Échantillons < 1 Mo** versionnés ; **données complètes jamais poussées** ; dérivé = pipeline only.

## 4. Réponses métier — 2 min 30
- Dashboard **5 KPI** : **CA 13,5 M R$** · note **4,09/5** · **8,1 %** retard.
- Segmentation : **~95 000 clients**, **RFM** + **KMeans** → 3 personas.
  - **Victor** = nouveau fort potentiel, ne réachète pas.
  - **Lucia** = dormante > 1 an.
  - **Marco** = fidèle premium, gros panier/tête.
- 3 campagnes chiffrées → **total ≈ 733 000 R$** (chiffre-choc, pause 2 s).
- 2 tests stats : **Mann-Whitney**, retard **2,6 vs 4,3**, p ≈ 0. Retard = sujet satisfaction.

## 5. Modèles : perfs, limites, biais — 2 min
- **Retard** : baseline + logreg + random forest ; métriques déséquilibre.
  - **ROC-AUC 0,72** ; variables clés **distance + délai estimé**.
  - Rappel faible à 0,5 → **API expose la proba**, **seuil 0,30**.
- **Sentiment** (portugais, direct) : **TF-IDF F1 0,91 > NN PyTorch 0,90**.
  - Punchline humilité : *« le deep learning battu par une régression des années 50 »*.
- **Éthique** : **audit d'équité par région** (écart rappel 0,22) + RGPD + limites.

## 6. Démo API — 1 min  ⚠️ EN DIRECT
- `docker compose -f infra/docker-compose.yml up -d`
- **Sentiment** : `curl .../predict/sentiment` → *produto excelente* → **positif 0,97**.
- **Retard** : `curl .../predict/retard` (450 km, 15 j) → **risque élevé 0,73, seuil 0,3**.
- Souligner : **proba renvoyée**, seuil au métier, **OpenAPI auto** (`/docs`).
- Repli si bug : capture `localhost:8000/docs`.

## 7. Bilan + bonus — 30 s
- **5 lots livrés, CI verte** (la montrer).
- **4 bonus** : MLflow · ELK · Spark clickstream · cloud AWS chiffré → **profils optionnels**, clone < 30 min.
- Axe d'amélioration : **rappel retard** (features + calibration par région).
- Punchline fin : *« données éparpillées & retards subis → plateforme, réponses chiffrées, modèle qui anticipe. Merci. »*

---

### ⏱️ Récap minutage
| # | Séquence | Durée | Cumul |
|---|----------|-------|-------|
| 1 | Problème & valeur | 1:00 | 1:00 |
| 2 | Archi & arbitrages | 1:30 | 2:30 |
| 3 | Données & qualité | 1:30 | 4:00 |
| 4 | Réponses métier | 2:30 | 6:30 |
| 5 | Modèles & biais | 2:00 | 8:30 |
| 6 | Démo API | 1:00 | 9:30 |
| 7 | Bilan & bonus | 0:30 | 10:00 |

### ✅ Checklist avant enregistrement
- [ ] `docker compose up` fonctionne (API + dashboard + Airflow), **API déjà `up` avant de filmer** (évite le temps de build en direct).
- [ ] Commandes `curl` **copiées-collées prêtes** dans le terminal.
- [ ] Caméra + micro OK, **visage visible**, regard vers l'objectif, bon éclairage.
- [ ] Support (slides) partagé à l'écran, **CI verte** affichée au moins une fois.
- [ ] Durée **≤ 10 min** — chrono visible pendant la répétition.
- [ ] Repo ouvert dans un onglet (preuve technique) ; `/docs` OpenAPI accessible.
