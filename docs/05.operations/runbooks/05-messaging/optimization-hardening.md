---
status: active
---
<!-- Target: docs/05.operations/runbooks/05-messaging/optimization-hardening.md -->

# 05-Messaging Optimization Hardening Runbook

## Overview (KR)

이 런북은 05-messaging 하드닝 항목에서 발생할 수 있는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. 관리 경로 middleware/SSO 누락, 이미지 태그 회귀, dev 경로 오류, CI 하드닝 실패를 중심으로 점검/복구 절차를 정의한다.

## 05-Messaging Optimization Hardening Procedure

> Scope: Messaging Gateway/Compose Baseline Recovery

### Purpose

- 메시징 관리 경로의 보안/안정성 기준을 신속히 복구한다.
- compose 정합성과 CI 기준선 회귀를 빠르게 차단한다.

### Canonical References

- [Spec](../../../03.specs/05-messaging/spec.md)
- [Operations Policy](../../policies/05-messaging/optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)

## When to Use

- `messaging-hardening` CI가 실패할 때
- Kafka/RabbitMQ 관리 UI가 Traefik 경유로 비정상 응답할 때
- Kafka dev compose가 경로/네트워크 오류로 기동 실패할 때
- 부동 태그 이미지 회귀가 발견될 때

## Procedure

### Checklist

- [ ] 실패 항목(이미지/라우터/경로/문서 링크) 식별
- [ ] 최근 변경 커밋과 영향 범위 확인
- [ ] 운영 영향도(관리 경로/데이터 평면) 평가

### Steps

1. 정적 구성 점검
   - `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
   - `docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config`
   - `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
3. 증상별 복구
   - middleware 누락:
     - 대상 라우터에 `gateway-standard-chain@file` 재적용
   - 관리 UI 접근 제어 누락:
     - `kafka-ui`, `kafbat-ui-dev`, `rabbitmq` 라우터에 `sso-errors@file,sso-auth@file` 재적용
   - 이미지 회귀:
     - `kafka-ui` 이미지를 고정 태그로 복원
   - dev 경로 오류:
     - `./jmx-exporter`, `./kafbat-ui/dynamic_config.yaml` 경로로 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

### Verification Steps

- [ ] 3개 compose `config` 검증 통과
- [ ] `check-messaging-hardening` 실패 0건
- [ ] optimization-hardening 문서 링크와 README 인덱스 최신화 확인

### Observability and Evidence Sources

- **Signals**: CI `messaging-hardening` job 상태, Traefik 라우터 상태, 컨테이너 health
- **Evidence to Capture**:
  - 변경 전후 `check-messaging-hardening.sh` 출력
  - `docker compose config` 결과
  - 관련 compose/docs diff

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 05-messaging`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 링크 재확인

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: 메시징 관리 자동화 작업 일시 중지(승인 필요)
- **Eval Re-run**: `check-messaging-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output + health 상태 스냅샷

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
- [Usage guide](../../guides/05-messaging/optimization-hardening.md)
- [Operations policy](../../policies/05-messaging/optimization-hardening.md)
- [Operations template](../../../99.templates/operation.template.md)
