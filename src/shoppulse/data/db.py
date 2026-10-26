"""Connexion à la base PostgreSQL via SQLAlchemy."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import Engine, create_engine, text

from shoppulse.config import get_settings


def get_engine() -> Engine:
    """Retourne un moteur SQLAlchemy configuré depuis l'environnement."""
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def ping(engine: Engine | None = None) -> bool:
    """Teste la connexion ; renvoie True si la base répond."""
    engine = engine or get_engine()
    with engine.connect() as conn:
        return conn.execute(text("SELECT 1")).scalar_one() == 1


def read_sql(query: str, engine: Engine | None = None) -> pd.DataFrame:
    """Exécute une requête SQL et renvoie un DataFrame."""
    engine = engine or get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
