<!-- Target: docs/09.runbooks/04-data/analytics/influxdb.md -->

# InfluxDB Recovery Runbook

: InfluxDB Performance & Ingestion Recovery

---

## Overview (KR)

이 런북은 InfluxDB의 수집 장애, 성능 저하 및 노드 중단 시의 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 복구 단계와 검증 기준을 제공한다.

## Purpose

지표 수집 누락을 최소화하고, InfluxDB 서비스의 가용성을 즉각적으로 복구하는 것을 목적으로 한다.

## Canonical References

- `[../../02.ard/0012-data-analytics-architecture.md]`
- `[../../07.guides/04-data/analytics/influxdb.md]`
- `[../../08.operations/04-data/analytics/influxdb.md]`

## When to Use

- InfluxDB 헬스 체크(`8181/health`) 실패 시.
- Telegraf 또는 애플리케이션에서 `401 Unauthorized` 또는 `503 Service Unavailable` 노출 시.
- 디스크 사용량 임계치(80%) 초과 경보 발생 시.

## Procedure or Checklist

### Checklist

- [ ] Docker 컨테이너 상태 확인 (`influxdb`)
- [ ] API Token 유효성 및 Secrets 마운트 확인
- [ ] 볼륨 마운트 지점의 디스크 잔여 용량 확인

### Procedure

1. **서비스 요상 확인**:

   ```bash
   docker compose ps influxdb
   docker logs influxdb --tail 100
   ```

2. **토큰 검증**:
   API 호출을 통해 토큰이 활성 상태인지 확인한다.

   ```bash
   curl -i http://influxdb:8181/health -H "Authorization: Token $(cat secrets/influxdb_api_token)"
   ```

3. **강제 재시작 (필요 시)**:

   ```bash
   docker compose restart influxdb
   ```

4. **데이터 정리 (디스크 고갈 시)**:
   보존 정책이 짧은 버킷의 데이터를 수동으로 삭제하거나 보존 기간을 조정한다.

## Verification Steps

- [ ] `curl -i http://influxdb:8181/health` 결과가 `200 OK`인지 확인.
- [ ] Grafana 대시보드에서 최신 데이터가 업데이트되는지 확인.

## Observability and Evidence Sources

- **Signals**: Prometheus `influxdb_up`, `influxdb_http_request_duration_seconds`.
- **Evidence to Capture**: `docker logs influxdb` 출력 결과, `influx bucket list` 결과.

## Safe Rollback or Recovery Procedure

- [ ] 설정 변경 전 `docker-compose.yml` 백업.
- [ ] 데이터 유실 우려 시, 기존 데이터를 다른 경로로 복사 후 작업 수행.

## Related Operational Documents

- **Operations**: [docs/08.operations/04-data/analytics/influxdb.md](../../../08.operations/04-data/analytics/influxdb.md)
