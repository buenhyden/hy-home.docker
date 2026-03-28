# 05-Messaging Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/05-messaging` 최적화/하드닝 실행 계획서다. 게이트웨이 경계 제어 강화, 이미지 태그/경로 정합성 보강, CI 하드닝 게이트 도입, 문서 계층 동기화를 단계적으로 수행한다.

## Context

- 기준 카탈로그: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 대상 구성: `kafka`, `rabbitmq` compose + 관련 docs/ci/scripts

## Goals & In-Scope

- **Goals**:
  - 메시징 관리 경로를 게이트웨이 표준 체인 및 SSO 정책에 정렬한다.
  - 부동 태그/경로 정합성 리스크를 제거한다.
  - 메시징 전용 하드닝 게이트를 CI에 추가한다.
  - PRD~Runbook 문서를 optimization-hardening 기준으로 동기화한다.
- **In Scope**:
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
  - `scripts/check-messaging-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` 메시징 optimization-hardening 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Kafka/RabbitMQ 신규 토폴로지 구축
  - 애플리케이션 재처리 코드 구현
- **Out of Scope**:
  - 비메시징 티어 구성 변경
  - 클라우드 managed messaging 도입

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-MSG-001 | Kafka UI 이미지 태그 고정 및 gateway chain 적용 | `infra/05-messaging/kafka/docker-compose.yml` | REQ-PRD-MSG-FUN-01,03 | compose config + grep 체크 |
| PLN-MSG-002 | Kafka dev compose 경로 정합성 및 chain 적용 | `infra/05-messaging/kafka/docker-compose.dev.yml` | REQ-PRD-MSG-FUN-01,04 | compose config 통과 |
| PLN-MSG-003 | RabbitMQ 관리 경로 middleware chain 강화 | `infra/05-messaging/rabbitmq/docker-compose.yml` | REQ-PRD-MSG-FUN-01,02 | router label 확인 |
| PLN-MSG-004 | 메시징 하드닝 기준선 스크립트 작성 | `scripts/check-messaging-hardening.sh` | REQ-PRD-MSG-FUN-05 | script pass/fail 동작 |
| PLN-MSG-005 | CI `messaging-hardening` job 추가 | `.github/workflows/ci-quality.yml` | REQ-PRD-MSG-FUN-05 | workflow 정의 확인 |
| PLN-MSG-006 | scripts 인덱스 갱신 | `scripts/README.md` | REQ-PRD-MSG-FUN-05 | README 항목/예시 반영 |
| PLN-MSG-007 | PRD~Runbook optimization 문서 세트 생성/갱신 | `docs/01~09/**` | REQ-PRD-MSG-FUN-06 | 상호 링크/README 반영 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-MSG-001 | Structural | Kafka compose 정적 검증 | `docker compose -f infra/05-messaging/kafka/docker-compose.yml config` | 오류 없음 |
| VAL-MSG-002 | Structural | Kafka dev compose 정적 검증 | `docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config` | 오류 없음 |
| VAL-MSG-003 | Structural | RabbitMQ compose 정적 검증 | `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config` | 오류 없음 |
| VAL-MSG-004 | Compliance | 메시징 하드닝 기준선 검증 | `bash scripts/check-messaging-hardening.sh` | 실패 0건 |
| VAL-MSG-005 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-MSG-006 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO 체인 강화로 운영 자동화 API 접근 영향 | Medium | 내부 포트 기반 운영 경로와 예외 절차를 runbook에 명시 |
| 라우터 미들웨어 오적용으로 관리 UI 장애 | High | 변경 즉시 compose 정적 검증 + 롤백 절차 제공 |
| 카탈로그 확장 미완료 | Medium | 운영 정책/가이드/태스크에 단계 확장 로드맵 명시 |
| 문서 인덱스 누락 | Medium | 수정 폴더 README를 동일 변경 세트에서 동기화 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-messaging-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Sandbox / Canary Rollout**: 메시징 프로필 단위 단계 기동 후 헬스 확인
- **Human Approval Gate**: 외부 노출 정책/SSO 우회/HA 토폴로지 확장 변경 시 승인 필수
- **Rollback Trigger**: 관리 UI 접근 실패, compose 검증 오류, CI 게이트 실패
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] 메시징 compose 하드닝 항목 반영
- [x] messaging-hardening 스크립트 및 CI 게이트 반영
- [x] 01~09 optimization-hardening 문서 및 README 인덱스 동기화
- [ ] runtime 검증 증적 확보(환경 가능 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-05-messaging-optimization-hardening.md](../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../02.ard/0020-messaging-optimization-hardening-architecture.md](../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md](../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/05-messaging/spec.md](../04.specs/05-messaging/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/05-messaging/optimization-hardening.md](../07.guides/05-messaging/optimization-hardening.md)
- **Operations**: [../08.operations/05-messaging/optimization-hardening.md](../08.operations/05-messaging/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/05-messaging/optimization-hardening.md](../09.runbooks/05-messaging/optimization-hardening.md)
