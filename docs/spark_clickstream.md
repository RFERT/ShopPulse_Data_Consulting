# Traitement Spark du clickstream REES46 (bonus)

Démonstration d'un traitement **distribuable** (PySpark) du flux de navigation,
en complément des données transactionnelles Olist.

## Contexte

Le jeu **REES46** (comportement de navigation e-commerce) est hors périmètre et
volumineux. On fournit ici un **échantillon déterministe < 1 Mo**
([`clickstream_sample.csv`](../data/samples/clickstream_sample.csv)) respectant son
schéma, pour démontrer un traitement Spark qui **passerait à l'échelle sans
changement de code** sur le jeu complet.

Schéma : `event_time, event_type (view|cart|purchase), product_id, category_id,
category_code, price, user_id, user_session`.

## Traitement

[`clickstream_job.py`](../pipelines/spark/clickstream_job.py) calcule :

- **Entonnoir view → cart → purchase** et taux de conversion ;
- **Top catégories** par nombre de vues ;
- **Chiffre d'affaires par catégorie** (événements d'achat).

Les résultats sont écrits en CSV dans `artifacts/spark/`.

## Lancement

```bash
pip install -e ".[spark]"            # nécessite un JDK (Java 8/11/17)
python -m spark.make_sample_clickstream   # génère l'échantillon
python -m spark.clickstream_job           # lance le traitement
```

Exemple de sortie (entonnoir) :

```
view       2500  taux=1.0
cart        864  taux=0.3456
purchase    379  taux=0.1516
```

## Notes

- **Windows** : si le chemin du projet contient des accents, `get_session()`
  bascule automatiquement `SPARK_HOME` sur le nom court 8.3 (le lanceur Spark ne
  supporte pas les chemins non-ASCII). L'écriture de fichiers requiert `winutils.exe`
  (Hadoop) ; en conteneur Linux ce point ne se pose pas.
- Dépendance **optionnelle** (`[spark]`), non installée en CI : le test associé
  s'auto-skippe en l'absence de PySpark.
