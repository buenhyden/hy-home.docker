# Pyroscope Recovery Runbook

> Troubleshooting and recovery procedures for continuous profiling.

---

## Overview (KR)

이 문서는 Pyroscope 서비스 장애 발생 시 복구 절차를 정의한다. 프로파일 데이터 인입 중단, 저장소 공간 부족, 쿼리 성능 저하 등의 일반적인 데브옵스 시나리오를 다룬다.

## Runbook Type

`recovery-runbook`

## Potential Issues & Symptoms

### 1. Ingestion Gaps (데이터 수집 중단)
- **Symptom**: Grafana 플레임그래프에 데이터가 표시되지 않음.
- **Check**: `infra-pyroscope` 컨테이너 로그 및 `infra-alloy` 송신 로그 확인.
- **Resolution**:
  ```bash
  docker compose restart pyroscope
  docker compose restart alloy
  ```

### 2. Disk Space Pressure (저장소 부족)
- **Symptom**: 컨테이너가 `Read-only` 모드로 전환되거나 비정상 종료됨.
- **Check**: `df -h`로 `/var/lib/pyroscope` 마운트 지점 확인.
- **Resolution**:
  - `pyroscope.yaml`에서 retention 설정 축소.
  - 오래된 데이터 수동 삭제 (주의: 서비스 중단 후 수행 권장).

### 3. High CPU Usage (수집 부하)
- **Symptom**: 호스트 시스템 CPU 사용률 급증.
- **Check**: `docker stats pyroscope`. 
- **Resolution**:
  - `pyroscope.yaml`의 `ingestion_rate_limit` 조정.
  - Alloy에서 수집 대상 서비스 필터링 강화.

## Recovery Steps

### Emergency Restart
```bash
# Move to infra directory
cd infra/06-observability

# Restart Pyroscope
docker compose restart pyroscope

# Verify Health
curl -f http://localhost:4040/health
```

### Configuration Rollback
설정 변경 후 장애 발생 시 `infra/06-observability/pyroscope/config/pyroscope.yaml`을 이전 버전으로 복구하고 재시작한다.

## Post-Mortem Guidelines

- 장애 발생 시간과 복구 시간을 기록한다.
- `alloy` 레이블 매핑 오류였는지, `pyroscope` 자체 저장소 문제였는지 원인을 규명한다.
- 재발 방지를 위해 알림 임계값(Alert Threshold) 조정을 검토한다.

## Related Documents

- **Infrastructure**: `[infra/06-observability/pyroscope/README.md](../../../infra/06-observability/pyroscope/README.md)`
- **Guide**: `[../../07.guides/06-observability/pyroscope.md](../../07.guides/06-observability/pyroscope.md)`
- **Operation**: `[../../08.operations/06-observability/pyroscope.md](../../08.operations/06-observability/pyroscope.md)`
