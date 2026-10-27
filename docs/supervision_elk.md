# Supervision des logs — ELK (bonus)

Stack **Elasticsearch + Logstash + Kibana** pour centraliser, indexer et visualiser
les logs de l'API.

## Flux de logs

```
API FastAPI ──(logs JSON)──> fichier partagé ──> Logstash ──> Elasticsearch ──> Kibana
  middleware                api.jsonl            pipeline       index            dashboards
```

- L'API émet **une ligne JSON par événement** (voir
  [`observability/logging.py`](../src/shoppulse/observability/logging.py)).
- Un middleware journalise chaque requête HTTP : `method`, `path`, `status_code`,
  `latency_ms`, `timestamp`, `level`, `service`.
- En conteneur, `SHOPPULSE_LOG_FILE` redirige ces logs vers un volume partagé lu par
  Logstash ([`pipeline.conf`](../infra/elk/logstash/pipeline.conf)).

## Lancement

```bash
# socle + API
docker compose -f infra/docker-compose.yml up -d api
# stack d'observabilité (profil optionnel)
docker compose -f infra/docker-compose.yml --profile observability up -d
```

Puis générer du trafic (`curl http://localhost:8000/health`) et ouvrir **Kibana** sur
<http://localhost:5601> : créer une *data view* sur l'index `shoppulse-api-*` pour
explorer latences, taux d'erreurs et volume de requêtes.

## Exemple de ligne de log

```json
{"timestamp":"2026-10-27T18:00:00","level":"INFO","logger":"shoppulse",
 "service":"shoppulse-api","message":"http_request","method":"POST",
 "path":"/predict/retard","status_code":200,"latency_ms":12.4}
```

## Note

Le profil `observability` est **optionnel** : il n'est pas lancé par défaut pour
préserver le « clone & run » et rester léger. Elasticsearch requiert ~1 Go de RAM.
