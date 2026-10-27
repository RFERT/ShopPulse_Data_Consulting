"""Tests du logging JSON structuré (bonus ELK)."""

from __future__ import annotations

import json
import logging

from shoppulse.observability.logging import JsonFormatter, configure_logging


def test_json_formatter_produces_valid_json() -> None:
    record = logging.LogRecord(
        name="shoppulse",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="http_request",
        args=(),
        exc_info=None,
    )
    record.extra_fields = {"method": "GET", "path": "/health", "status_code": 200}
    line = JsonFormatter().format(record)

    data = json.loads(line)
    assert data["message"] == "http_request"
    assert data["service"] == "shoppulse-api"
    assert data["level"] == "INFO"
    assert data["method"] == "GET"
    assert data["status_code"] == 200
    assert "timestamp" in data


def test_configure_logging_returns_json_logger() -> None:
    logger = configure_logging()
    assert logger.name == "shoppulse"
    assert logger.handlers
    assert isinstance(logger.handlers[0].formatter, JsonFormatter)
