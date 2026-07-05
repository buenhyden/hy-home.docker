---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/optimization-hardening.md -->

# 06-Observability Optimization Hardening Runbook

## 06-Observability Optimization Hardening Procedure

> Scope: observability gateway/SSO middleware, compose health dependency, custom image hardening, hardening checks, restart, and Git-managed rollback evidence.

### Overview

이 런북은 `06-observability` hardening regression을 복구하기 위한 실행 절차를 제공한다. Gateway/SSO middleware 누락, health dependency 회귀, custom image runtime hardening 누락, Pyroscope route availability 회귀, cAdvisor healthcheck 회귀, and CI hardening baseline failure를 중심으로 점검/복구한다.

### Purpose

운영자가 observability management route, compose dependency, healthcheck, custom image, and hardening validation boundary를 확인하고, runtime/security policy 변경이 필요한 경우 별도 승인으로 격리하도록 돕는다.

### Canonical References

- [Spec](../../../03.specs/007-observability/spec.md)
- [Operations Policy](../../policies/06-observability/optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)

## When to Use

- `infrastructure-hardening` CI가 실패할 때.
- 관측성 UI/API가 Traefik 경유로 비정상 응답할 때.
- 스택 부팅 시 Alloy/Grafana dependency 또는 service health race가 반복될 때.
- Loki/Tempo custom image runtime hardening이 깨졌을 때.
- Pyroscope or cAdvisor route/healthcheck availability가 회귀했을 때.
- hardening script, Compose, Dockerfile, or operations docs 변경 후 rollback 가능성을 확인해야 할 때.

## Procedure

### Checklist

- [ ] 실패 항목을 middleware, depends_on, healthcheck, image, script, workflow, or docs 중 하나로 분류한다.
- [ ] 최근 변경 커밋과 영향 범위를 확인한다.
- [ ] telemetry collection, query, alerting, profiling, and UI route 영향도를 평가한다.
- [ ] Secret value, token, or credential payload는 기록하지 않는다.
- [ ] Route/middleware, resource cap, secret reference, workflow gate, or runtime hardening rule을 변경해야 해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 정적 구성과 hardening baseline을 캡처한다.

   ```bash
   HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh
   bash scripts/hardening/check-all-hardening.sh 06-observability
   ```

2. Gateway/SSO middleware boundary를 확인한다.

   ```bash
   rg -n 'traefik.http.routers.(prometheus|alloy|grafana|alertmanager|pushgateway|loki|tempo|pyroscope|cadvisor).*middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

3. Health dependency and healthcheck boundary를 확인한다.

   ```bash
   rg -n 'condition: service_healthy|/healthz|/api/health|/-/healthy|/ready|/-/ready' infra/06-observability/docker-compose.yml
   ```

4. Custom image hardening boundary를 확인한다.

   ```bash
   rg -n 'USER 10001:10001|/run/secrets/minio_app_user_password|MINIO_APP_USER_PASSWORD|exec /usr/bin/(loki|tempo)' infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh infra/06-observability/tempo/Dockerfile infra/06-observability/tempo/docker-entrypoint.sh
   ```

5. Pyroscope and cAdvisor route availability boundary를 확인한다.

   ```bash
   rg -n 'pyroscope:|cadvisor:|traefik.http.routers.pyroscope|traefik.http.services.pyroscope.loadbalancer.server.port|traefik.http.routers.cadvisor|traefik.http.services.cadvisor.loadbalancer.server.port|PYROSCOPE_PORT|CADVISOR_PORT' infra/06-observability/docker-compose.yml infra/06-observability/docker-compose.dev.yml
   ```

6. 증상별 Git-managed rollback 후보를 확인한다.

   ```bash
   git diff -- infra/06-observability/docker-compose.yml infra/06-observability/docker-compose.dev.yml infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh infra/06-observability/tempo/Dockerfile infra/06-observability/tempo/docker-entrypoint.sh scripts/hardening/check-all-hardening.sh .github/workflows/ci-quality.yml
   ```

7. Hardening script, Compose, Dockerfile, or workflow 변경이 원인이면 직전 Git diff 단위로 되돌리고 재검증한다.

   ```bash
   HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh
   bash scripts/hardening/check-all-hardening.sh 06-observability
   bash scripts/validation/check-doc-traceability.sh
   ```

   이 런북은 route/middleware policy change, resource cap change, secret rotation, workflow gate redesign, or runtime security relaxation을 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`가 통과한다.
- [ ] `bash scripts/hardening/check-all-hardening.sh 06-observability` 실패가 0건이다.
- [ ] `bash scripts/validation/check-doc-traceability.sh`가 통과한다.
- [ ] Observability route middleware, health dependencies, custom image hardening, Pyroscope/cAdvisor availability checks가 현재 policy와 일치한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening` 상태, Traefik router labels, container health, hardening script output
- **Evidence to Capture**: before/after hardening output, compose validation result, affected router/service, relevant diff, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed Compose, Dockerfile, entrypoint, hardening script, workflow, or operations doc change가 원인이면 직전 Git diff 단위로 되돌린다.
- Runtime restart는 affected service의 documented runbook을 따른다.
- Route/middleware policy, resource cap, secret reference, workflow gate, or runtime security relaxation은 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: 관측성 자동화 변경 작업 일시 중지(승인 필요)
- **Eval Re-run**: `check-all-hardening.sh 06-observability`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output + health 상태

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, token, credential payload 원문은 기록하지 않는다.
- Hardening 장애는 failed check name, affected service/router, before/after command output, relevant redacted diff, and recovery/escalation state를 함께 기록한다.
- Route/resource/secret/workflow/security policy 변경 필요성이 보이면 approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, evidence capture, and Git-managed rollback만 사용한다. Route/middleware policy, resource cap, secret reference, workflow gate, runtime security relaxation, or external service 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, route/resource/secret/workflow/security 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/optimization-hardening.md)
- [Operations policy](../../policies/06-observability/optimization-hardening.md)
