"""Suivi d'expériences MLflow (bonus).

Enveloppe légère autour de MLflow. Si ``mlflow`` n'est pas installé ou si
``SHOPPULSE_MLFLOW=0``, toutes les opérations deviennent des **no-op** : le code
d'entraînement fonctionne à l'identique sans la dépendance.

URI de suivi : ``MLFLOW_TRACKING_URI`` si défini, sinon un dossier local ``mlruns/``.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from shoppulse.config import ROOT_DIR

EXPERIMENT_NAME = "shoppulse"


def is_enabled() -> bool:
    """Vrai si MLflow est installé et non désactivé via l'environnement."""
    if os.getenv("SHOPPULSE_MLFLOW", "1") == "0":
        return False
    try:
        import mlflow  # noqa: F401
    except ImportError:
        return False
    return True


def _tracking_uri() -> str:
    uri = os.getenv("MLFLOW_TRACKING_URI")
    if uri:
        return uri
    # Backend SQLite local (le store fichier est déprécié depuis MLflow 3).
    return f"sqlite:///{(ROOT_DIR / 'mlflow.db').as_posix()}"


class _Run:
    """Interface minimale de journalisation ; no-op si MLflow est absent."""

    def __init__(self, active: bool) -> None:
        self._active = active

    def log_params(self, params: dict[str, Any]) -> None:
        if not self._active:
            return
        import mlflow

        mlflow.log_params(params)

    def log_metrics(self, metrics: dict[str, float]) -> None:
        if not self._active:
            return
        import mlflow

        clean = {k: float(v) for k, v in metrics.items() if v is not None}
        mlflow.log_metrics(clean)

    def log_artifact(self, path: str | Path) -> None:
        if not self._active or not Path(path).exists():
            return
        import mlflow

        mlflow.log_artifact(str(path))


@contextmanager
def start_run(run_name: str):
    """Ouvre un run MLflow nommé ; cède un ``_Run`` no-op si le suivi est désactivé."""
    if not is_enabled():
        yield _Run(active=False)
        return

    import mlflow

    mlflow.set_tracking_uri(_tracking_uri())
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run(run_name=run_name):
        yield _Run(active=True)
