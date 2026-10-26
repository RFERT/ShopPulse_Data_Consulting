# Support & script de la vidéo de soutenance (10 min max)

> Vidéo **face caméra**, l'auteur visible tout au long. Support (ces slides) rendu avec
> la vidéo. La trame ci-dessous est **imposée** par l'énoncé. Minutage indicatif.

---

## 1. Le problème de ShopPulse et la valeur apportée — 1 min
**À dire :**
- ShopPulse : marketplace (3 000 vendeurs, 100 000 clients). Trois irritants : données
  éparpillées, marketing non ciblé, retards subis générant des avis négatifs.
- Valeur livrée : base consolidée, réponses métier lisibles, modèle prédictif servi par
  API. **4 questions métier → 4 réponses actionnables.**
**Slide :** logo + 3 irritants → 3 leviers.

## 2. Architecture et arbitrages techniques — 1 min 30
**À dire :**
- Schéma : Olist → ETL Airflow → PostgreSQL → analyse/ML → API FastAPI + dashboard
  Streamlit, le tout conteneurisé + CI.
- Arbitrages : **Airflow vs Prefect** (standard, UI de supervision, compétence
  transférable) ; **Streamlit vs Metabase** (stack unifiée, déploiement cohérent).
**Slide :** `docs/architecture.md` (diagramme) + tableau d'arbitrage.

## 3. Les données : pipeline et qualité — 1 min 30
**À dire :**
- MLD 9 tables, chargement **idempotent et rejouable**, contrôles qualité, rapport
  avant/après. Échantillons < 1 Mo versionnés, données complètes jamais poussées.
- Démo rapide : `python -m shoppulse_etl.flow` → rapport qualité.
**Slide :** `docs/mld.md` + extrait `docs/rapport_qualite.md`.

## 4. Les réponses métier : dashboard, segmentation, recommandations — 2 min 30
**À dire :**
- Dashboard 5 KPI (CA 13,5 M R$, note 4,09, retard 8,1 %).
- Segmentation RFM + clustering → **3 personas** (nouveau à fort potentiel, dormant,
  fidèle premium) → **3 campagnes chiffrées** (~733 k R$ de CA incrémental estimé).
- 2 tests statistiques : les retards **dégradent significativement** la note.
**Slide :** `dashboards/apercu_dashboard.png` + `docs/marketing.md`.

## 5. Les modèles : performances, interprétation, limites et biais — 2 min
**À dire :**
- **Retard** : baseline + logreg + random forest, métriques déséquilibre (ROC-AUC 0,72,
  PR-AUC). Variables clés : distance, délai estimé. Seuil abaissé pour le rappel.
- **Sentiment** (portugais, entraînement direct) : TF-IDF+logreg (F1 0,91) vs réseau de
  neurones PyTorch (F1 0,90), courbes d'apprentissage, analyse d'erreurs.
- **Biais & éthique** : audit d'équité par région, RGPD, limites d'usage.
**Slide :** `docs/rapport_modeles.md` + `docs/ethique.md`.

## 6. Démonstration de l'API conteneurisée — 1 min
**À dire + montrer en direct :**
```bash
docker compose -f infra/docker-compose.yml up -d
curl -X POST localhost:8000/predict/sentiment -H "Content-Type: application/json" \
     -d '{"texte":"produto excelente, entrega rápida"}'
# -> {"sentiment":"positif","probabilite_positif":0.97}
curl -X POST localhost:8000/predict/retard -H "Content-Type: application/json" \
     -d '{"distance_km":450,"delai_estime_jours":15,"poids_total":1800,"volume_moy":12000,
          "fret_total":25,"prix_total":180,"n_items":1,"seller_order_count":120,
          "customer_state":"RJ","seller_state":"SP"}'
# -> {"probabilite_retard":0.73,"risque_eleve":true,"seuil":0.3}
```
**Slide :** capture de `http://localhost:8000/docs` (OpenAPI).

## 7. Bilan : écarts et ce que je referais — 30 s
**À dire :**
- 5 lots livrés, CI verte. Écart : rappel du modèle retard à améliorer (features).
- À refaire : enrichir les features, MLflow tôt, calibration par région.
**Slide :** `docs/retro.md`.

---

### Checklist avant enregistrement
- [ ] `docker compose up` fonctionne (API + dashboard + Airflow).
- [ ] Caméra + micro OK, visage visible.
- [ ] Durée ≤ 10 min, support partagé à l'écran.
- [ ] CI au vert affichée.
