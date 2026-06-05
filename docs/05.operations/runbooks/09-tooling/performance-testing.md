---
status: active
---
<!-- Target: docs/05.operations/runbooks/09-tooling/performance-testing.md -->

# Performance Testing Incident Runbook

## Performance Testing Incident Procedure

> Scope: stop and triage Locust/k6-wrapper performance tests that affect shared services.

### Overview (KR)

이 런북은 성능 테스트 실행 중 target service 또는 shared gateway/auth/data tier에 영향이 발생했을 때 사용하는 공통 절차다.

### Purpose

테스트 부하를 우선 중단하고, 어떤 leaf(`locust` 또는 `k6`)가 실행 중인지 확인한 뒤, target 회복과 evidence capture를 완료한다.

### Canonical References

- **Spec**: [09-tooling spec](../../../03.specs/09-tooling/spec.md)
- **Policy**: [Performance testing policy](../../policies/09-tooling/performance-testing.md)
- **Guide**: [Performance testing guide](../../guides/09-tooling/performance-testing.md)

## When to Use

- 테스트 중 target SLI가 승인된 한계 아래로 떨어진다.
- Gateway/Auth/Data tier가 부하 테스트 영향으로 degraded 상태가 된다.
- InfluxDB 지표 전송 실패로 테스트 결과 신뢰도가 떨어진다.
- 실행 leaf가 `locust`인지 `k6` wrapper인지 불명확하다.

## Procedure

### Checklist

- [ ] 테스트 owner, target service owner, platform operator에게 중단 결정을 알린다.
- [ ] 실행 중인 leaf와 service name을 확인한다.
- [ ] users, spawn rate, target, scenario file, 시작 시각을 기록한다.

### Steps

1. 실행 중인 performance service를 확인한다.

   ```bash
   docker ps --format '{{.Names}}\t{{.Status}}' | rg '^(locust-master|locust-worker|k6-master)\b'
   ```

2. Locust leaf가 실행 중이면 Locust runbook의 stop 절차를 따른다.

3. k6 wrapper leaf가 실행 중이면 k6 runbook의 stop 절차를 따른다.

4. target service 회복 상태를 확인한다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 09-tooling
   bash scripts/validation/check-repo-contracts.sh
   ```

5. target SLI, error rate, latency, affected time window를 evidence에 기록한다.

### Verification Steps

- 실행 중이던 load generator가 stopped 또는 healthy-idle 상태다.
- target SLI와 shared tier health가 정상 범위로 회복됐다.
- 관련 guide/policy/runbook이 현재 service names와 root optional boundary를 유지한다.

### Observability and Evidence Sources

- **Logs**: load generator logs, target logs, gateway/auth/data tier logs
- **Metrics**: target SLI, request error rate, response latency, InfluxDB write status
- **Evidence to Capture**: service names, test parameters, stop time, recovery time, failed checks

### Safe Rollback or Recovery Procedure

1. load generator를 중단한 상태로 유지한다.
2. target service recovery는 해당 target의 runbook으로 전환한다.
3. 재실행은 target owner 승인과 conservative ramp-up plan이 있을 때만 수행한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: `check-all-hardening.sh 09-tooling`, `check-repo-contracts.sh`

## Evidence

- Capture command output, timestamps, service names, test parameters, target SLI summary, and final recovery state.
- Record whether Locust or k6 wrapper procedures were used.

## Rollback or Recovery

Use the leaf-specific stop procedure and target-specific recovery runbook. No verified procedure is documented here for restarting target services or mutating InfluxDB data.

## Escalation

Escalate to the platform operator and target service owner when stopping load does not restore service health, root compose context is broken, or secret exposure risk appears.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/performance-testing.md)
- [Operations policy](../../policies/09-tooling/performance-testing.md)
- [Locust runbook](./locust.md)
- [k6 runbook](./k6.md)
