# Runbook: SonarQube Recovery (P2)

Procedures for recovering SonarQube service failures.

## Symptoms

- Web UI returning 500 or 503 errors.
- Authentication failures (SonarQube uses its own user DB stored in Postgres).
- ElasticSearch initialization loops.

## Recovery Steps

### 1. Check Database Connectivity

SonarQube depends on the shared `mng-db`.

```bash
docker exec -it sonarqube psql -h ${POSTGRES_MNG_HOSTNAME} -U ${SONARQUBE_DB_USER} -d ${SONARQUBE_DBNAME}
```

### 2. ElasticSearch Index Corruption

If ES fails to start, clear the data directory (Note: This will trigger a full re-analysis on next scan).

```bash
docker exec -u 0 -it sonarqube rm -rf /opt/sonarqube/data/es7
docker compose restart sonarqube
```

### 3. Log Inspection

```bash
tail -f ${DEFAULT_TOOLING_DIR}/sonarqube/logs/web.log
tail -f ${DEFAULT_TOOLING_DIR}/sonarqube/logs/ce.log
```
