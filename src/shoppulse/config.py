"""Configuration centralisée : chemins projet et connexion base de données."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Racine du projet (…/ShopPulse_Data_Consulting)
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
SAMPLES_DIR = DATA_DIR / "samples"
MODELS_DIR = ROOT_DIR / "artifacts" / "models"
SQL_DIR = ROOT_DIR / "sql"


class Settings:
    """Paramètres applicatifs lus depuis l'environnement."""

    def __init__(self) -> None:
        self.db_host = os.getenv("POSTGRES_HOST", "localhost")
        self.db_port = os.getenv("POSTGRES_PORT", "5432")
        self.db_name = os.getenv("POSTGRES_DB", "shoppulse")
        self.db_user = os.getenv("POSTGRES_USER", "shoppulse")
        self.db_password = os.getenv("POSTGRES_PASSWORD", "shoppulse")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
