# Tempo Recovery Runbook

> Troubleshooting and recovery procedures for distributed tracing.

---

## Overview (KR)

이 문서는 Tempo 서비스 장애 발생 시 복구 절차를 정의한다. 트레이스 인입 안 됨, MinIO 연결 실패, WAL 손상, 쿼리 엔진 지연 등의 일반적인 시나리오를 다룬다.

## Runbook Type

`recovery-runbook`

## Potential Issues & Symptoms

### 1. Broken Trace Ingestion (트레이스 누락)
- **Symptom**: Grafana에서 최근 트레이스가 검색되지 않음.
- **Check**: `infra-tempo` 로그 및 `distributor` 지표 확인.
- **Resolution**:
  ```bash
  docker compose restart tempo- [Tempo](./tempo.md)
  ```
  Alloy와 Tempo 간의 OTLP 엔드포인트(4317/4318) 도달 가능성 확인.

### 2. Backend Storage Connection (MinIO 오류)
- **Symptom**: `Failed to write blocks to storage`, `S3 bucket access denied` 오류 로그 발생.
- **Check**: MinIO 버킷 권한 및 네트워크 연결 상태.
- **Resolution**:
  - `MINIO_APP_USERNAME` 및 비밀번호 환경 변수 재확인.
  - MinIO 인터페이스에서 `tempo-bucket` 존재 여부 확인.

### 3. WAL Corruption (쓰기 버퍼 손상)
- **Symptom**: Tempo 재시작 시 `corrupt WAL` 오류와 함께 기동 실패.
- **Check**: `/var/tempo/wal` 디렉토리 파일 상태.
- **Resolution**:
  - WAL 파일 백업 후 해당 디렉토리 정리 (데이터 유실 주의).

### 4. Metrics Generator Failure
- **Symptom**: 서비스 그래프나 Span Metrics가 대시보드에서 보이지 않음.
- **Check**: `tempo.yaml` 내 `remote_write` 설정 및 Prometheus 상태.
- **Resolution**:
  - Prometheus 엔드포인트 헬스체크.
  - Tempo 재시작 후 메트릭 생성 로그 모니터링.

## Recovery Steps

### Emergency Full Restart
```bash
# Move to infra directory
cd infra/06-observability

# Restart all related services
docker compose restart minio tempo alloy
```

### Manual Bucket Check
MinIO 클라이언트(`mc`)를 사용하여 스토리지 상태를 점검한다.

## Post-Mortem Guidelines

- 트레이스 유실 범위 및 시간을 기록한다.
- `alloy`에서 `tempo`로의 데이터 전달 병목이었는지, `tempo` 내부 압축기(Compactor) 문제였는지 분석한다.
- 재발 방지를 위해 저장소 모니터링 알림 임계값을 조정한다.

## Related Documents

- **Infrastructure**: `[infra/06-observability/tempo/README.md](../../../infra/06-observability/tempo/README.md)`
- **Guide**: `[../../07.guides/06-observability/tempo.md](../../07.guides/06-observability/tempo.md)`
- **Operation**: `[../../08.operations/06-observability/tempo.md](../../08.operations/06-observability/tempo.md)`
