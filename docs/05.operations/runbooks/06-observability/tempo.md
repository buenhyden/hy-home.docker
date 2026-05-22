---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/tempo.md -->

# Tempo Runbook

## Tempo Recovery Procedure

> Troubleshooting and recovery procedures for distributed tracing.

---

### Overview (KR)

이 문서는 Tempo 서비스 장애 발생 시 복구 절차를 정의한다. 트레이스 인입 안 됨, MinIO 연결 실패, WAL 손상, 쿼리 엔진 지연 등의 일반적인 시나리오를 다룬다.

### Procedure Type

`recovery-runbook`

### Potential Issues & Symptoms

#### 1. Broken Trace Ingestion (트레이스 누락)

- **Symptom**: Grafana에서 최근 트레이스가 검색되지 않음.
- **Check**: `infra-tempo` 로그 및 `distributor` 지표 확인.
- **Resolution**:

  ```bash
  docker compose restart tempo- [Tempo](./tempo.md)
  ```

  Alloy와 Tempo 간의 OTLP 엔드포인트(4317/4318) 도달 가능성 확인.

#### 2. Backend Storage Connection (MinIO 오류)

- **Symptom**: `Failed to write blocks to storage`, `S3 bucket access denied` 오류 로그 발생.
- **Check**: MinIO 버킷 권한 및 네트워크 연결 상태.
- **Resolution**:
  - `MINIO_APP_USERNAME` 및 비밀번호 환경 변수 재확인.
  - MinIO 인터페이스에서 `tempo-bucket` 존재 여부 확인.

#### 3. WAL Corruption (쓰기 버퍼 손상)

- **Symptom**: Tempo 재시작 시 `corrupt WAL` 오류와 함께 기동 실패.
- **Check**: `/var/tempo/wal` 디렉토리 파일 상태.
- **Resolution**:
  - WAL 파일 백업 후 해당 디렉토리 정리 (데이터 유실 주의).

#### 4. Metrics Generator Failure

- **Symptom**: 서비스 그래프나 Span Metrics가 대시보드에서 보이지 않음.
- **Check**: `tempo.yaml` 내 `remote_write` 설정 및 Prometheus 상태.
- **Resolution**:
  - Prometheus 엔드포인트 헬스체크.
  - Tempo 재시작 후 메트릭 생성 로그 모니터링.

### Recovery Steps

#### Emergency Full Restart

```bash
## Move to infra directory
cd infra/06-observability

## Restart all related services
docker compose restart minio tempo alloy
```

#### Manual Bucket Check

MinIO 클라이언트(`mc`)를 사용하여 스토리지 상태를 점검한다.

### Post-Mortem Usagelines

- 트레이스 유실 범위 및 시간을 기록한다.
- `alloy`에서 `tempo`로의 데이터 전달 병목이었는지, `tempo` 내부 압축기(Compactor) 문제였는지 분석한다.
- 재발 방지를 위해 저장소 모니터링 알림 임계값을 조정한다.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

### Procedure or Checklist

#### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

#### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/tempo.md)
- [Operations policy](../../policies/06-observability/tempo.md)
- [Operations template](../../../99.templates/operation.template.md)
