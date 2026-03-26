<!-- Target: docs/09.runbooks/04-data/analytics/influxdb.md -->

# InfluxDB Recovery Runbook

: InfluxDB Data Persistence Layer

---

## Overview (KR)

이 런북은 InfluxDB 서비스 장애 시의 복구 절차를 정의한다. 데이터 유실, 토큰 만료, 스토리지 부족 등 주요 장애 상황에서 운영자가 즉시 따라 할 수 있는 가이드를 제공한다.

## Purpose

Restore metrics ingestion and analytical querying capabilities during service outages.

## Canonical References

- `[../../02.ard/04-data/01-analytics-tier.md]`
- `../../../infra/04-data/analytics/influxdb/docker-compose.yml`

## When to Use

- InfluxDB health check returns non-200.
- Telegraf/k6 logs show `401 Unauthorized` or `503 Service Unavailable`.
- Disk usage alert for InfluxDB volume.

## Procedure or Checklist

### Checklist

- [ ] Check container status: `docker compose ps influxdb`
- [ ] Check disk availability: `df -h ${DEFAULT_DATA_DIR}`
- [ ] Verify Docker Secrets are mounted: `docker exec influxdb ls /run/secrets/`

### Procedure 1: Token Rotation (Unauthorized)

1. Generate new token via InfluxDB UI or CLI.
2. Update the secret file: `echo "NEW_TOKEN" > secrets/influxdb_api_token`
3. Restart service: `docker compose up -d influxdb`

### Procedure 2: Storage Cleanup

If the disk is full and service fails to start:
1. Temporarily move stale Parquet/data files to backup.
2. Start service.
3. Lower retention periods on non-critical buckets.
4. Run manual compaction if supported.

### Procedure 3: Full Reset (Data Loss Acceptable)

1. Stop services: `docker compose down`
2. Wipe data: `sudo rm -rf ${DEFAULT_DATA_DIR}/influxdb/data/*`
3. Restart: `docker compose up -d`

## Verification Steps

- [ ] `curl -sL -D - http://influxdb:8181/health -o /dev/null | grep 200`
- [ ] Log in to Grafana and verify InfluxDB datasource "Test Connection" passes.

## Safe Rollback

- Always snapshot the `${DEFAULT_DATA_DIR}/influxdb/data` volume before performing manual deletions or reset procedures.

## Related Operational Documents

- **Operations**: `[../../../08.operations/04-data/analytics/influxdb.md]`
