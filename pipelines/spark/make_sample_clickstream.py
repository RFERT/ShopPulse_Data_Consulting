"""Générateur d'un échantillon de clickstream type REES46 (bonus Spark).

Le jeu REES46 complet est hors périmètre et volumineux. On produit ici un
**échantillon déterministe < 1 Mo** respectant son schéma, avec un entonnoir
réaliste view → cart → purchase, pour démontrer le traitement Spark.

Sortie : ``data/samples/clickstream_sample.csv``.
Usage : ``python -m spark.make_sample_clickstream``
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta

from shoppulse.config import SAMPLES_DIR

CATEGORIES = [
    ("electronics.smartphone", 1001),
    ("electronics.audio.headphone", 1002),
    ("computers.notebook", 1003),
    ("apparel.shoes", 2001),
    ("furniture.living_room.sofa", 3001),
    ("appliances.kitchen.refrigerators", 4001),
    ("auto.accessories", 5001),
]
N_SESSIONS = 2500
SEED = 42


def generate(path=None):
    """Écrit l'échantillon de clickstream et renvoie le chemin produit."""
    path = path or (SAMPLES_DIR / "clickstream_sample.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    start = datetime(2024, 1, 1)

    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "event_time",
                "event_type",
                "product_id",
                "category_id",
                "category_code",
                "price",
                "user_id",
                "user_session",
            ]
        )
        for session in range(N_SESSIONS):
            user_id = 100000 + rng.randint(0, 1800)
            session_id = f"s{session:06d}"
            category_code, category_id = rng.choice(CATEGORIES)
            product_id = category_id * 1000 + rng.randint(0, 40)
            price = round(rng.uniform(20, 2500), 2)
            t = start + timedelta(minutes=session * 7)

            events = ["view"]
            if rng.random() < 0.35:  # ajout au panier
                events.append("cart")
                if rng.random() < 0.45:  # conversion
                    events.append("purchase")

            for step, event_type in enumerate(events):
                writer.writerow(
                    [
                        (t + timedelta(seconds=step * 40)).strftime("%Y-%m-%d %H:%M:%S"),
                        event_type,
                        product_id,
                        category_id,
                        category_code,
                        price,
                        user_id,
                        session_id,
                    ]
                )
    return path


if __name__ == "__main__":
    out = generate()
    print("Échantillon clickstream écrit :", out)
