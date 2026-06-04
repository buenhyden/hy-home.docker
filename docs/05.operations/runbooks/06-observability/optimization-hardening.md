---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/optimization-hardening.md -->

# 06-Observability Optimization Hardening Runbook

## Overview (KR)

이 런북은 `06-observability` 하드닝 항목에서 발생할 수 있는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health 의존성 회귀, 커스텀 이미지 런타임 하드닝 누락, CI 기준선 실패를 중심으로 점검/복구한다.

## 06-Observability Optimization Hardening Procedure

> Scope: Observability Gateway/Compose Baseline Recovery

### Purpose

- 관측성 관리 경로의 보안/가용성 기준을 신속히 복구한다.
- compose/CI 회귀를 조기에 차단하고 안정 상태로 복원한다.

### Canonical References

- [Spec](../../../03.specs/06-observability/spec.md)
- [Operations Policy](../../policies/06-observability/optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)

## When to Use

- `infrastructure-hardening` CI가 실패할 때
- 관측성 UI/API가 Traefik 경유로 비정상 응답할 때
- 스택 부팅 시 Alloy/Grafana 의존성 대기로 장애가 반복될 때
- Loki/Tempo custom image 런타임 실패가 발생할 때

## Procedure

### Checklist

- [ ] 실패 항목(middleware/depends_on/healthcheck/image/script/doc) 식별
- [ ] 최근 변경 커밋과 영향 범위 확인
- [ ] 운영 영향도(수집/조회/알림 경로) 평가

### Steps

1. 정적 구성 점검
   - root context: `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
   - service-local context: root networks/secrets를 선언한 임시 validation overlay를 함께 사용한다.
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 06-observability`
3. 증상별 복구
   - middleware 누락:
     - 대상 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - 의존성 race:
     - Alloy/Grafana의 Loki/Tempo `depends_on`을 `service_healthy`로 복원
   - 호스트 수집기 신호 불량:
     - cAdvisor `/healthz` healthcheck 복원
     - cAdvisor labels가 `traefik.http.routers.cadvisor.*`와 `${CADVISOR_PORT:-8080}` service port를 사용하도록 복원
   - pyroscope route/availability 회귀:
     - root-included `docker-compose.dev.yml`과 local `docker-compose.yml` 모두 `pyroscope` service를 렌더하도록 복원
     - Pyroscope labels가 `traefik.http.routers.pyroscope.*`와 `${PYROSCOPE_PORT:-4040}` service port를 사용하도록 복원
   - custom image 회귀:
     - Loki/Tempo Dockerfile `USER 10001:10001` 복원
     - entrypoint secret guard 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 06-observability`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

### Verification Steps

- [ ] observability compose `config` 검증 통과
- [ ] `check-all-hardening.sh 06-observability` 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening` 상태, Traefik 라우터 상태, container health
- **Evidence to Capture**:
  - 변경 전후 `check-all-hardening.sh 06-observability` 출력
  - compose `config` 결과
  - 관련 compose/Dockerfile/docs diff

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
  - `scripts/hardening/check-all-hardening.sh 06-observability`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 링크 재확인

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: 관측성 자동화 변경 작업 일시 중지(승인 필요)
- **Eval Re-run**: `check-all-hardening.sh 06-observability`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output + health 상태

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
- [Usage guide](../../guides/06-observability/optimization-hardening.md)
- [Operations policy](../../policies/06-observability/optimization-hardening.md)
