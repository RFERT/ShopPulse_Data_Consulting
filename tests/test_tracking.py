"""Tests du suivi d'expériences MLflow (bonus)."""

from __future__ import annotations

import pytest

from shoppulse.models import tracking


def test_tracking_disabled_is_noop(monkeypatch) -> None:
    monkeypatch.setenv("SHOPPULSE_MLFLOW", "0")
    assert tracking.is_enabled() is False
    with tracking.start_run("test") as run:
        run.log_params({"a": 1})
        run.log_metrics({"m": 0.5})
        run.log_artifact("inexistant.txt")


def test_tracking_logs_to_local_dir(tmp_path, monkeypatch) -> None:
    pytest.importorskip("mlflow")
    monkeypatch.delenv("SHOPPULSE_MLFLOW", raising=False)
    tracking_uri = f"sqlite:///{(tmp_path / 'mlflow.db').as_posix()}"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", tracking_uri)
    assert tracking.is_enabled() is True

    with tracking.start_run("test_run") as run:
        run.log_params({"model": "unit_test"})
        run.log_metrics({"score": 0.9})

    import mlflow

    mlflow.set_tracking_uri(tracking_uri)
    exp = mlflow.get_experiment_by_name(tracking.EXPERIMENT_NAME)
    assert exp is not None
    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
    assert len(runs) >= 1
