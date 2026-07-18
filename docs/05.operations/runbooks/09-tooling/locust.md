---
status: active
---
<!-- Target: docs/05.operations/runbooks/09-tooling/locust.md -->

# Locust Recovery Runbook

<!-- [ID:09-tooling:locust] -->

## Locust Recovery Procedure

> Scope: recover or stop `locust-master` and `locust-worker` under `infra/09-tooling/locust`.

### Overview

이 런북은 Locust master/worker 연결 끊김, 요청 통계 이상, 또는 테스트 부하로 인한 target service 영향이 발생했을 때 사용한다.

### Purpose

부하 생성을 즉시 통제하고 master/worker 연결과 Locust 결과를 확인한 뒤 안전하게 재시작 또는 escalation한다.

### Canonical References

- **Spec**: [09-tooling spec](../../../03.specs/010-tooling/spec.md)
- **Policy**: [Locust policy](../../policies/09-tooling/locust.md)
- **Guide**: [Locust guide](../../guides/09-tooling/locust.md)

## When to Use

- Locust UI나 로그에 worker disconnect가 나타난다.
- `locust-worker` healthcheck가 실패하거나 restart loop에 들어간다.
- Locust request error 또는 통계 수집 이상이 발생한다.
- target service SLI가 테스트 중 급격히 저하된다.

## Procedure

### Checklist

- [ ] 테스트 owner와 target service owner에게 현재 상태를 공유한다.
- [ ] root compose + Locust leaf compose를 함께 사용하는 실행 context인지 확인한다.
- [ ] 현재 users, spawn rate, target host, 시나리오 파일을 기록한다.

### Steps

1. Compose context 변수를 설정한다.

   ```bash
   LOCUST_COMPOSE_FILES="-f docker-compose.yml -f infra/09-tooling/locust/docker-compose.yml"
   ```

2. 부하를 먼저 중단한다.

   ```bash
   docker compose $LOCUST_COMPOSE_FILES --profile tooling --profile testing stop locust-worker locust-master
   ```

3. master/worker 상태와 최근 로그를 확인한다.

   ```bash
   docker compose $LOCUST_COMPOSE_FILES --profile tooling --profile testing ps locust-master locust-worker
   docker compose $LOCUST_COMPOSE_FILES --profile tooling --profile testing logs --tail=100 locust-master locust-worker
   ```

4. worker 재동기화가 필요한 경우 master health를 먼저 확인한 뒤 worker만 재생성한다.

   ```bash
   docker compose $LOCUST_COMPOSE_FILES --profile tooling --profile testing up -d --force-recreate locust-worker
   ```

5. 정적 기준선을 재검증한다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 09-tooling
   bash scripts/validation/check-repo-contracts.sh
   ```

### Verification Steps

- `locust-master`와 `locust-worker` 상태가 stopped 또는 healthy로 명확히 확인된다.
- target service SLI가 정상 범위로 회복된다.
- `locust-worker` logs에서 master 연결 실패가 반복되지 않는다.

### Observability and Evidence Sources

- **Logs**: `locust-master`, `locust-worker`, target service logs
- **Metrics**: target SLI, request error rate, worker count, Locust request statistics
- **Evidence to Capture**: 실행 명령, 중단 시각, users/spawn rate, target, worker count, 오류 요약

### Safe Rollback or Recovery Procedure

1. 부하 발생을 중단한 상태를 유지한다.
2. worker만 문제가 있으면 master health 확인 후 `locust-worker`만 재생성한다.
3. `locustfile.py` 변경이 원인이면 마지막 정상 commit과 현재 diff를 evidence로 남기고 review 후 재실행한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: `check-all-hardening.sh 09-tooling`, `check-repo-contracts.sh`

## Evidence

- Capture command output, timestamps, worker count, scenario file path, and final stopped/healthy state.
- Record failed checks, suspected script changes, and target SLI recovery state in the related task or incident evidence.

## Rollback or Recovery

Use the stop, inspect, and worker-only recreate procedure above. No broader verified rollback procedure is documented for target services or host networking from this runbook.

## Escalation

Escalate to the performance tooling owner when workers cannot reconnect after master health is restored, target SLI does not recover after stopping load, secret exposure risk appears, or root compose context cannot render required dependencies.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/locust.md)
- [Operations policy](../../policies/09-tooling/locust.md)
