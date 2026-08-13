---
status: active
artifact_id: ad-0020
artifact_type: architecture-description
parent_ids:
  - prd-0017
created: 2026-03-28
updated: 2026-08-10
---
# 05-Messaging Optimization Hardening Architecture Description

## Overview and Context

이 문서는 `05-messaging` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. Kafka/RabbitMQ의 관리 트래픽 경로를 게이트웨이 표준 체인과 SSO 경계로 정렬하고, 운영 회귀를 CI 기준선 검증으로 차단하는 구조를 설명한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

메시징 계층은 데이터 평면(Kafka broker, RabbitMQ AMQP)과 관리 평면(UI/API)을 분리해 운영한다. 관리 평면은 Traefik TLS 종료 지점에서 표준 미들웨어를 적용하고, 데이터 평면은 `infra_net` 내부 경계에서 서비스 헬스 기반 의존 관계를 유지한다.

## Boundaries and Constraints

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - 메시징 관리 경로 라우팅/미들웨어 계약
  - Kafka UI 이미지 버전 고정 정책
  - 메시징 하드닝 기준선 검증(CI + script)
  - optimization-hardening 문서 추적성
- **Consumes**:
  - `01-gateway` Traefik 미들웨어 체인
  - `02-auth` SSO 체계
  - `06-observability` 지표/알림
- **Does Not Own**:
  - Producer/Consumer 애플리케이션 구현
  - 비메시징 티어 인프라 구성
- **Non-goals**:
  - 즉시 멀티리전/멀티클러스터 전환
  - 앱 레벨 재처리 코드 구현

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: 게이트웨이 표준 체인으로 burst 트래픽 제어 및 일시적 장애 흡수
- **Security**: TLS 종료 + SSO 보호 + 부동 태그 금지
- **Reliability**: healthcheck 의존성과 롤링 복구 절차로 가용성 유지
- **Scalability**: 카탈로그 기반으로 DLQ/재처리/quorum queue 확장 준비
- **Observability**: compose health + exporter 지표 + CI 증적 연계
- **Operability**: 표준 스크립트 + runbook + 정책 문서로 운영 단일 계약 유지

## Architecture Views

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

- Kafka:
  - Root include: `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`
  - Service-local full compose: `kafka-1/2/3`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`
- RabbitMQ:
  - `rabbitmq` (AMQP + Management)
- Gateway Path:
  - Client -> Traefik(`websecure`) -> middleware chain -> management endpoints
- Internal Path:
  - service-to-service traffic over `infra_net`

## Data and Infrastructure

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - Kafka topics (event/log streams)
  - RabbitMQ queues (task/retry/dead-letter flows)
- **Storage Strategy**:
  - `${DEFAULT_MESSAGE_BROKER_DIR}` 기반 상태 데이터 분리
- **Data Boundaries**:
  - 장기 보관/분석은 `04-data` 계층으로 오프로딩

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - Root profile: Kafka dev single broker + RabbitMQ single-node
  - Service-local full compose: Kafka 3 broker model with root network/secret context
  - Traefik TLS termination + middleware policy
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 05-messaging`
  - `.github/workflows/ci-quality.yml`의 `infrastructure-hardening` job

## AI Agent Architecture Descriptions (If Applicable)

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: 메시징 변경은 하드닝/문서 추적성 검증 통과 필수
- **Memory & Context Strategy**: Spec/Plan/Runbook/Catalog 링크를 실행 컨텍스트로 고정
- **Guardrail Boundary**: 부동 태그, 무검증 middleware 변경, 무근거 노출 확대 금지
- **Latency / Cost Budget**: 운영 정책에서 관리

## Decision and Requirement Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/prd-0017-messaging-optimization-hardening.md](../../01.requirements/prd-0017-messaging-optimization-hardening.md)
- **Spec**: [../03.specs/006-messaging/spec.md](../../03.specs/spec-0006-messaging/spec.md)
- **Plan**: ../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md
- **ADR**: [../02.architecture/decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md](../decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Tasks**: ../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md
- **Guide**: [../../05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/05-messaging/ops-0037-optimization-hardening/guide.md)
- **Policy**: [../../05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/05-messaging/ops-0037-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md)
