"""Tests du socle : configuration et API."""

from fastapi.testclient import TestClient

from shoppulse.api.main import app
from shoppulse.config import get_settings

client = TestClient(app)


def test_database_url_is_postgres() -> None:
    url = get_settings().database_url
    assert url.startswith("postgresql+psycopg2://")
    assert "shoppulse" in url


def test_root_endpoint() -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "shoppulse-api"
    assert "version" in body


def test_health_endpoint() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
