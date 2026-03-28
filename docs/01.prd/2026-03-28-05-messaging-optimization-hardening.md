# 05-Messaging Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/05-messaging` 계층(Kafka, RabbitMQ)의 최적화/하드닝 요구사항을 정의한다. 게이트웨이 경계에서의 트래픽 제어, 관리 경로 보호, 이미지 버전 고정, 구성 정합성, CI 기반 회귀 차단을 목표로 한다.

## Vision

메시징 계층을 "기본적으로 안전하고(secure-by-default), 회귀를 자동 차단하며, 단계적 확장(HA/재처리/DLQ)이 가능한 운영 기반"으로 전환한다.

## Problem Statement

- 일부 메시징 UI/관리 경로는 게이트웨이 표준 체인이 누락되어 트래픽 급증과 순간 장애에 취약하다.
- Kafka UI 이미지에 부동 태그(`:main`)가 사용되어 예측 불가능한 변경 위험이 존재한다.
- 개발 Compose 경로 정합성 이슈로 환경 재현성이 낮다.
- 메시징 전용 하드닝 기준선 검증이 CI에 없어 PR 단계에서 회귀가 누락될 수 있다.
- 기존 05-messaging 문서는 optimization-hardening 문맥의 추적성이 약하다.

## Personas

- **Messaging Operator**: Kafka/RabbitMQ의 가용성과 복구 가능성을 유지해야 한다.
- **DevOps Engineer**: 구성 하드닝과 CI 게이트를 운영해야 한다.
- **Platform Developer**: 안정적인 이벤트/큐 기반 통합을 위해 일관된 운영 계약이 필요하다.

## Key Use Cases

- **STORY-01**: 운영자는 메시징 라우터가 게이트웨이 표준 체인과 SSO 정책을 준수하는지 검증한다.
- **STORY-02**: 엔지니어는 이미지 태그/구성 경로 회귀를 CI에서 사전에 차단한다.
- **STORY-03**: 장애 대응자는 runbook 절차로 관리 경로 접근/브로커 헬스 문제를 빠르게 복구한다.

## Functional Requirements

- **REQ-PRD-MSG-FUN-01**: Kafka/RabbitMQ 외부 노출 라우터는 `gateway-standard-chain@file`를 적용해야 한다.
- **REQ-PRD-MSG-FUN-02**: Kafka UI/RabbitMQ 관리 라우터는 SSO 미들웨어 체인을 강제해야 한다.
- **REQ-PRD-MSG-FUN-03**: Kafka UI 이미지는 부동 태그를 금지하고 고정 버전을 사용해야 한다.
- **REQ-PRD-MSG-FUN-04**: `docker-compose.dev.yml` 경로 정합성을 보장해야 한다.
- **REQ-PRD-MSG-FUN-05**: `scripts/check-messaging-hardening.sh`와 CI `messaging-hardening` job을 제공해야 한다.
- **REQ-PRD-MSG-FUN-06**: 01~09 문서 계층에서 메시징 최적화/하드닝 문서 상호 링크를 유지해야 한다.

## Success Criteria

- **REQ-PRD-MSG-MET-01**: `bash scripts/check-messaging-hardening.sh` 실패 0건
- **REQ-PRD-MSG-MET-02**: Kafka/RabbitMQ compose 정적 검증 명령 통과
- **REQ-PRD-MSG-MET-03**: 메시징 노출 라우터의 middleware 계약 충족
- **REQ-PRD-MSG-MET-04**: 05-messaging optimization-hardening 문서의 양방향 링크 정합성 확보

## Scope and Non-goals

- **In Scope**:
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
  - `scripts/check-messaging-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` 메시징 optimization-hardening 문서
- **Out of Scope**:
  - 애플리케이션 Producer/Consumer 코드
  - Kafka/RabbitMQ 토폴로지의 즉시 대규모 재구성
  - 클라우드 매니지드 메시징 이전
- **Non-goals**:
  - 모든 카탈로그 확장 항목의 즉시 구현
  - 비메시징 티어의 직접 변경

## Risks, Dependencies, and Assumptions

- SSO 정책 강화는 일부 운영 자동화 경로에 영향이 있을 수 있어 절차 기반 예외 정책이 필요하다.
- 카탈로그 확장 항목(DLQ/재처리/quorum queue)은 단계별 승인과 운영 검증이 필요하다.
- 로컬 런타임 검증은 호스트의 Docker 네트워크/시크릿 상태에 의존한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: 메시징 compose/script/docs/ci 변경 및 정적 검증 실행
- **Disallowed Actions**: 부동 태그 재도입, 무근거 포트 노출 확대, 무검증 라우팅 정책 변경
- **Human-in-the-loop Requirement**: 운영 접근 정책 완화, 대규모 HA 확장은 승인 후 수행
- **Evaluation Expectation**: `messaging-hardening`, `template-security-baseline`, `doc-traceability` 통과

## Related Documents

- **ARD**: [../02.ard/0020-messaging-optimization-hardening-architecture.md](../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/05-messaging/spec.md](../04.specs/05-messaging/spec.md)
- **Plan**: [../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md](../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/05-messaging/optimization-hardening.md](../07.guides/05-messaging/optimization-hardening.md)
- **Operation**: [../08.operations/05-messaging/optimization-hardening.md](../08.operations/05-messaging/optimization-hardening.md)
- **Runbook**: [../09.runbooks/05-messaging/optimization-hardening.md](../09.runbooks/05-messaging/optimization-hardening.md)
