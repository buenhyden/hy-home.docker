---
status: active
---
<!-- Target: docs/05.operations/runbooks/09-tooling/performance-testing.md -->

# Performance Testing Runbook

## Performance Testing Recovery Procedure

> Locust 부하 테스트 인프라 장애 시 대응 및 복구 절차를 정의합니다.

---

### Overview (KR)

이 문서는 Locust 마스터/워커 노드의 연결 끊김, InfluxDB 지표 수집 장애 또는 성능 테스트로 인한 타 서비스 과부하 발생 시의 긴급 조치 방법을 안내합니다.

### Target Audience

- Operator
- Performance Engineer
- SRE

### Alerting & Monitoring

- **Locust UI Error**: 웹 인터페이스에서 `Worker disconnected` 경고 발생 시.
- **Metric Loss**: InfluxDB로의 데이터 전송 실패가 Locust 콘솔에 출력될 때.
- **Target Down**: 부하 테스트 시작 후 대상 서비스의 가용성 지표(SLI)가 급격히 하락할 때.

### Recovery Procedures

#### 1. 테스트 강제 중단 (Emergency Stop)

가장 우선적으로 부하 생성을 즉시 중단합니다.

- **Locust UI**: UI에서 `Stop` 버튼을 클릭합니다.
- **CLI**: `docker-compose -f infra/09-tooling/k6/docker-compose.yml stop` 명령을 실행합니다.

#### 2. 마스터-워커 연결 복구 (Master-Worker Sync)

워커 노드가 마스터를 찾지 못하는 경우:

1. 마스터 활성 상태 확인: `docker-compose ps locust-master`
2. 환경 변수 확인: 워커의 `LOCUST_MASTER_NODE_HOST`가 올바른지 확인합니다.
3. 서비스 재시작: `docker-compose restart locust-master locust-worker`

#### 3. InfluxDB 데이터 전송 오류 (Data Link Recovery)

1. InfluxDB 서비스 상태 확인: `docker-compose ps influxdb`
2. 네트워크 가시성 확인: `docker-compose exec locust-master ping influxdb`
3. Locust 설정 확인: `locustfile.py` 내의 InfluxDB 엔드포인트 설정을 점검합니다.

#### 4. 타 서비스 영향 복구 (Cascading Failure Clean-up)

부하 테스트로 인해 다른 서비스가 마비된 경우:

- Gateway 캐시를 플러시하거나 서비스를 재시작하여 정상 상태로 돌려놓습니다.
- 테스트 결과 데이터를 분석하여 어느 지점에서 연쇄 장애가 시작되었는지 파악합니다.

### Post-Mortem Tasks

- 장애 원인이 테스트 시나리오 설계 오류인지, 인프라 용량 부족인지 분석하여 보고서를 작성합니다.
- 재발 방지를 위해 테스트 스케일링 정책을 조정합니다.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Steps

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
- [Usage guide](../../guides/09-tooling/performance-testing.md)
- [Operations policy](../../policies/09-tooling/performance-testing.md)
- [Operations template](../../../99.templates/operation.template.md)
