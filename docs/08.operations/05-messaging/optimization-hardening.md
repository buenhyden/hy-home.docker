# 05-Messaging Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `05-messaging` 계층의 최적화/하드닝 운영 정책을 정의한다. 게이트웨이 경계 제어, 관리 경로 보호, 이미지 태그 통제, CI 기준선 검증, 카탈로그 확장 승인 조건을 필수 통제로 규정한다.

## Policy Scope

- `infra/05-messaging/kafka/docker-compose.yml`
- `infra/05-messaging/kafka/docker-compose.dev.yml`
- `infra/05-messaging/rabbitmq/docker-compose.yml`
- `scripts/check-messaging-hardening.sh`

## Applies To

- **Systems**: Kafka/Kafbat/Schema Registry/Kafka Connect/Kafka REST/RabbitMQ
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 외부 노출 라우터는 `gateway-standard-chain@file`를 적용해야 한다.
  - 관리 UI 라우터(`kafka-ui`, `kafbat-ui-dev`, `rabbitmq`)는 SSO 체인을 포함해야 한다.
  - Kafka UI 이미지는 고정 태그를 사용해야 하며 부동 태그를 금지한다.
  - 메시징 변경은 `messaging-hardening` CI 게이트를 통과해야 한다.
  - 문서(PRD~Runbook)는 optimization-hardening 링크를 유지해야 한다.
- **Allowed**:
  - `messaging-option` 프로필 기반 RabbitMQ 선택 활성화
  - 카탈로그 확장 항목의 단계적 도입(DLQ/재처리/quorum queue)
- **Disallowed**:
  - 무검증 라우터 middleware 변경
  - 부동 태그 이미지 도입
  - 카탈로그/정책 미연계 확장 실행

## Exceptions

- 긴급 장애 대응 시 일시적으로 middleware 완화가 필요할 수 있다.
- 단, 조치 후 동일 릴리스 내 원상 복구 및 검증 증적 확보가 필수다.

## Verification

- `bash scripts/check-messaging-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`
- `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
- `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`

## Review Cadence

- 월 1회 정기 검토
- 메시징 컴포넌트 주요 버전 변경/보안 이슈 발생 시 수시 검토

## Catalog Expansion Approval Gates

- **Kafka 확장 승인 조건**:
  - 토픽 거버넌스(보존/compaction/파티션 기준) 문서화
  - DLQ + 재처리 파이프라인 표준 운영 절차 확보
- **RabbitMQ 확장 승인 조건**:
  - quorum queue 적용 범위 및 예외 명시
  - dead-letter/retry 정책 + 소비자 재시도 기준 합의
- **Gateway 연계 승인 조건**:
  - 보안 헤더/접근 정책 템플릿 적용 계획 수립
  - 운영 자동화 경로의 접근 제어 영향 평가 완료

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: `messaging-hardening` + 공통 기준선 통과 필수
- **Log / Trace Retention**: `06-observability` 정책 준수
- **Safety Incident Thresholds**: 장기 healthcheck fail, 관리경로 인증 실패 급증, 메시지 지연 급증 시 runbook 즉시 전환

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-05-messaging-optimization-hardening.md](../../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../../02.ard/0020-messaging-optimization-hardening-architecture.md](../../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md](../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/05-messaging/spec.md](../../04.specs/05-messaging/spec.md)
- **Plan**: [../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/05-messaging/optimization-hardening.md](../../07.guides/05-messaging/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/05-messaging/optimization-hardening.md](../../09.runbooks/05-messaging/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
