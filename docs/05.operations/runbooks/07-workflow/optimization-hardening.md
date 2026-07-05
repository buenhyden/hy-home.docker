---
status: active
---
<!-- Target: docs/05.operations/runbooks/07-workflow/optimization-hardening.md -->

# 07-Workflow Optimization Hardening Runbook

## Overview

이 런북은 `07-workflow` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health dependency 회귀, n8n image/entrypoint drift, CI 게이트 실패를 중심으로 점검/복구한다.

## 07-Workflow Optimization Hardening Procedure

### Purpose

- workflow 관리 경로 보안과 startup 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

### Canonical References

- [Spec](../../../03.specs/008-workflow/spec.md)
- [Operations Policy](../../policies/07-workflow/optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)

## When to Use

- `infrastructure-hardening` CI가 실패할 때
- Airflow/Flower/n8n 경로 접근 정책이 비정상일 때
- Airflow worker/scheduler startup이 불안정할 때
- n8n worker/task-runner 재시작 루프가 발생할 때

## Procedure

### Checklist

- [ ] 실패 항목(middleware, healthcheck, depends_on, image, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(스케줄링, 자동화, 큐 지연) 평가

### Steps

1. 정적 구성 점검
   - `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
   - `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
   - service-local compose 파일은 root network/secrets context 없이 단독 `config` 대상으로 쓰지 않는다.
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
3. 증상별 복구
   - middleware 회귀:
     - Airflow/Flower/n8n 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - Airflow startup race:
     - service-local compose에서는 핵심 서비스의 `airflow-valkey` `service_healthy` dependency 복원
     - root-included dev compose에서는 `mng-valkey` broker 경계와 validation evidence 확인
   - n8n worker/task-runner 이상:
     - healthcheck/depends_on 계약 복원
   - n8n image drift:
     - compose custom image 설정 복원
     - Dockerfile `USER node`, entrypoint secret guard 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

### Verification Steps

- [ ] workflow compose static validation 통과
- [ ] workflow hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening`, container health, queue lag, scheduler heartbeat
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/Dockerfile/docs diff

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/07-workflow/airflow/docker-compose.yml`
  - `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
  - `scripts/hardening/check-all-hardening.sh 07-workflow`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: workflow 자동 변경 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-all-hardening.sh 07-workflow`
  - `check-template-security-baseline`
  - `check-doc-traceability`
- **Trace Capture**: CI logs + compose config + health 상태

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
- [Usage guide](../../guides/07-workflow/optimization-hardening.md)
- [Operations policy](../../policies/07-workflow/optimization-hardening.md)
