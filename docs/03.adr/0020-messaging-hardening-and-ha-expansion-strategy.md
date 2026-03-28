# ADR-0020: Messaging Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `05-messaging` 계층에 대해 즉시 적용 가능한 하드닝(게이트웨이 체인, 이미지 태그 고정, 구성 정합성, CI 게이트)을 우선 도입하고, 카탈로그 확장 항목(DLQ/재처리/quorum queue/HA 확장)은 단계적으로 진행하는 결정을 기록한다.

## Context

메시징 계층은 운영상 민감한 관리 경로를 외부에 노출하며, 트래픽 급증/일시 장애에 취약할 수 있다. 또한 부동 태그 이미지와 개발 구성 정합성 문제는 재현성과 안정성을 낮춘다. 운영 회귀를 PR 단계에서 차단할 자동화된 기준선 검증이 필요하다.

## Decision

- 즉시 하드닝 항목을 우선 반영한다.
  - 관리 라우터에 `gateway-standard-chain@file` 적용
  - `kafka-ui` 계열 이미지 태그를 고정 버전으로 핀
  - `docker-compose.dev.yml` 경로 정합성 수정
  - 메시징 하드닝 전용 검사 스크립트 + CI job 추가
  - optimization-hardening 문서 세트(01~09) 생성 및 링크 동기화
- RabbitMQ는 현행 `messaging-option` 운영 모델(선택 활성화)을 유지한다.
- 카탈로그 확장 항목은 정책/가이드/런북 기반 승인 절차로 단계 적용한다.

## Explicit Non-goals

- 이번 변경에서 메시징 토폴로지 자체를 즉시 재구성하는 작업
- 애플리케이션 로직 기반 재처리 파이프라인 구현
- 클라우드 메시징 서비스 전환

## Consequences

- **Positive**:
  - 게이트웨이 경계 품질(트래픽 제어/장애 흡수)이 향상된다.
  - 이미지 회귀 위험을 줄이고, 구성 재현성을 높인다.
  - CI에서 메시징 하드닝 회귀를 조기 차단한다.
- **Trade-offs**:
  - SSO 체인 적용으로 운영 자동화 스크립트 일부 조정이 필요할 수 있다.
  - 카탈로그 확장은 단계 이행이므로 단기 효과는 하드닝 중심으로 제한된다.

## Alternatives

### 카탈로그 확장 항목을 즉시 전면 구현

- Good:
  - 단기간에 많은 기능적 개선 가능
- Bad:
  - 변경 반경이 커져 장애 원인 분리와 롤백이 어려움

### 문서만 갱신하고 compose/CI 변경은 보류

- Good:
  - 단기 구현 부담 감소
- Bad:
  - 실제 운영 회귀를 자동 차단하지 못함

## Agent-related Example Decisions (If Applicable)

- Tool gating: `check-messaging-hardening.sh`를 CI 게이트로 강제
- Guardrail strategy: 부동 태그 금지, middleware 표준 체인 강제, 문서 링크 무결성 유지

## Related Documents

- **PRD**: [../01.prd/2026-03-28-05-messaging-optimization-hardening.md](../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../02.ard/0020-messaging-optimization-hardening-architecture.md](../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/05-messaging/spec.md](../04.specs/05-messaging/spec.md)
- **Plan**: [../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Related ADR**: [./0005-kafka-vs-rabbitmq-selection.md](./0005-kafka-vs-rabbitmq-selection.md)
