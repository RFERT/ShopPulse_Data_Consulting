"""Logs JSON structurés et middleware de requêtes (bonus ELK).

Produit une ligne JSON par événement, exploitable par Logstash puis
Elasticsearch/Kibana. Aucune dépendance externe : formateur basé sur ``logging``.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response

SERVICE_NAME = "shoppulse-api"


class JsonFormatter(logging.Formatter):
    """Formate chaque enregistrement de log en une ligne JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "service": SERVICE_NAME,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        extra = getattr(record, "extra_fields", None)
        if isinstance(extra, dict):
            payload.update(extra)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure un logger applicatif émettant du JSON sur la sortie standard."""
    logger = logging.getLogger("shoppulse")
    logger.setLevel(level)
    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.propagate = False

    log_file = os.getenv("SHOPPULSE_LOG_FILE")
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)

    return logger


async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Middleware : journalise méthode, route, statut et latence de chaque requête."""
    logger = logging.getLogger("shoppulse")
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "http_request",
        extra={
            "extra_fields": {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": elapsed_ms,
            }
        },
    )
    return response
