---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/pyroscope.md -->

# Pyroscope Runbook

## Pyroscope Recovery Procedure

> Troubleshooting and recovery procedures for continuous profiling.

---

### Overview (KR)

이 문서는 Pyroscope 서비스 장애 발생 시 복구 절차를 정의한다. 프로파일 데이터 인입 중단, 저장소 공간 부족, 쿼리 성능 저하 등의 일반적인 데브옵스 시나리오를 다룬다.

### Procedure Type

`recovery-runbook`

### Potential Issues & Symptoms

#### 1. Ingestion Gaps (데이터 수집 중단)

- **Symptom**: Grafana 플레임그래프에 데이터가 표시되지 않음.
- **Check**: `infra-pyroscope` 컨테이너 로그 및 `infra-alloy` 송신 로그 확인.
- **Resolution**:

  ```bash
  docker compose restart pyroscope
  docker compose restart alloy
  ```

#### 2. Disk Space Pressure (저장소 부족)

- **Symptom**: 컨테이너가 `Read-only` 모드로 전환되거나 비정상 종료됨.
- **Check**: `df -h`로 `/var/lib/pyroscope` 마운트 지점 확인.
- **Resolution**:
  - `pyroscope.yaml`에서 retention 설정 축소.
  - 오래된 데이터 수동 삭제 (주의: 서비스 중단 후 수행 권장).

#### 3. High CPU Usage (수집 부하)

- **Symptom**: 호스트 시스템 CPU 사용률 급증.
- **Check**: `docker stats pyroscope`.
- **Resolution**:
  - `pyroscope.yaml`의 `ingestion_rate_limit` 조정.
  - Alloy에서 수집 대상 서비스 필터링 강화.

### Recovery Steps

#### Emergency Restart

```bash
## Move to infra directory
cd infra/06-observability

## Restart Pyroscope
docker compose restart pyroscope

## Verify Health
curl -f http://localhost:4040/health
```

#### Configuration Rollback

설정 변경 후 장애 발생 시 `infra/06-observability/pyroscope/config/pyroscope.yaml`을 이전 버전으로 복구하고 재시작한다.

### Post-Mortem Usagelines

- 장애 발생 시간과 복구 시간을 기록한다.
- `alloy` 레이블 매핑 오류였는지, `pyroscope` 자체 저장소 문제였는지 원인을 규명한다.
- 재발 방지를 위해 알림 임계값(Alert Threshold) 조정을 검토한다.

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
- [Usage guide](../../guides/06-observability/pyroscope.md)
- [Operations policy](../../policies/06-observability/pyroscope.md)
- [Operations template](../../../99.templates/operation.template.md)
