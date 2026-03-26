<!-- [ID:09-tooling:sonarqube] -->
# Runbook: SonarQube Service Recovery (P2)

> Procedures for recovering from SonarQube service failures and index corruption.

## Symptoms

- Web UI returning 500 or 503 errors.
- Authentication failures (SonarQube uses its own user DB stored in Postgres).
- ElasticSearch initialization loops or "Search index is corrupted" in logs.
- Scan tasks (Background Tasks) stuck in "Pending".

## Diagnostic Steps

### 1. Check Service Status

```bash
cd ${DEFAULT_TOOLING_DIR}/sonarqube
docker compose ps
docker compose logs --tail=100 -f sonarqube
```

### 2. Verify Database Connectivity

SonarQube depends on the shared `mng-db`. Check if the container can reach the DB.

```bash
docker exec -it sonarqube \
  psql -h ${POSTGRES_MNG_HOSTNAME} -U ${SONARQUBE_DB_USER} -d ${SONARQUBE_DBNAME}
```

## Recovery Procedures

### 1. Elasticsearch Index Reconstruction

If ES fails to start or search results are inconsistent, clear the data directory to trigger a full re-analysis.

```bash
# 1. Stop the service
docker compose stop sonarqube

# 2. Clear ES data (Requires root to delete ES lock files)
sudo rm -rf ${DEFAULT_TOOLING_DIR}/sonarqube/data/es7

# 3. Restart service
docker compose start sonarqube
```

> [!NOTE]
> This will trigger a full re-analysis on the next scan for all projects. This is normal and expected.

### 2. JVM Memory Adjustment

If logs show `OutOfMemoryError`, increase the JVM heap in `docker-compose.yml`.

```yaml
# Update these values in docker-compose.yml
- SONAR_WEB_JAVAOPTS=-Xmx1024m -Xms1024m
- SONAR_SEARCH_JAVAOPTS=-Xmx1024m -Xms1024m
```

### 3. Log Inspection

Monitor these files for specific error patterns:

- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/web.log`: Web server and API issues.
- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/ce.log`: Compute Engine (scan task) issues.
- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/es.log`: ElasticSearch internal issues.

## Escalation Policy

- **P1**: Total UI outage affecting all PR merges -> Notify SRE Team.
- **P2**: Intermittent scan failures -> Investigate Compute Engine limits.

## Related References

- **Infrastructure**: [SonarQube Service](../../../infra/09-tooling/sonarqube/README.md)
- **Guide**: [SonarQube System Guide](../../07.guides/09-tooling/sonarqube.md)
- **Operation**: [SonarQube Operations Policy](../../08.operations/09-tooling/sonarqube.md)
