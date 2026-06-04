---
status: active
---
<!-- Target: docs/03.specs/05-messaging/spec.md -->

# 05-Messaging Optimization Hardening Specification

## Overview (KR)

이 문서는 `infra/05-messaging` 계층의 최적화/하드닝 구현 계약을 정의한다. Kafka/RabbitMQ 관리 경로의 게이트웨이 제어(레이트리밋/재시도/회로차단), 이미지 태그 고정, 개발 Compose 정합성, CI 기준선 검증을 핵심 범위로 다룬다.

## Strategic Boundaries & Non-goals

- 본 Spec은 메시징 인프라 구성 하드닝과 운영/문서 추적성 계약을 소유한다.
- Kafka/RabbitMQ 애플리케이션 레벨 Producer/Consumer 로직 변경은 범위 밖이다.

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md](../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md](../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md](../../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md)
  - [../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - `kafbat-ui` 이미지는 부동 태그(`:main`)를 금지하고 고정 버전을 사용한다.
  - 외부 노출 라우터는 `gateway-standard-chain@file`를 적용한다.
  - 관리 UI 라우터(`kafka-ui`, `rabbitmq`)는 SSO 미들웨어 체인을 유지한다. 현재 compose에 dev 전용 Kafbat router는 별도로 선언되어 있지 않다.
  - `docker-compose.dev.yml`의 로컬 볼륨 경로는 서비스 디렉터리 기준 상대 경로를 사용한다.
- **Data / Interface Contract**:
  - Root-included 메시징 profile은 `docker-compose.dev.yml`의 Kafka 단일 broker와 RabbitMQ 단일 노드를 렌더링한다. `infra/05-messaging/kafka/docker-compose.yml`은 root context 밖의 full 3 broker compose로 유지한다.
  - TLS 종료는 Traefik에서 수행하고 내부 `infra_net` 통신은 서비스 내부 프로토콜을 사용한다.
- **Governance Contract**:
  - `scripts/hardening/check-all-hardening.sh 05-messaging`를 CI `infrastructure-hardening` job으로 강제한다.
  - 문서 계층(01~09)은 optimization-hardening 문서 세트로 상호 링크를 유지한다.

## Core Design

- **Component Boundary**:
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
- **Key Dependencies**:
  - `infra/common-optimizations.yml` 공통 템플릿
  - `01-gateway` Traefik 동적 미들웨어(`gateway-standard-chain`, `sso-*`)
  - `02-auth` SSO 정책
- **Tech Stack**:
  - Kafka (Confluent CP 8.2.1)
  - RabbitMQ 4.3.1
  - Kafbat UI
  - Traefik TLS termination

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Kafka 토픽은 카탈로그 권장안 기준으로 보존/파티션/compaction 정책을 운영 문서에 명시한다.
  - RabbitMQ 큐는 dead-letter/retry/quorum queue 전략을 운영 정책으로 관리한다.
- **Migration / Transition Plan**:
  - Phase 1: 게이트웨이 경로 제어 + 이미지 핀 + compose 정합성 + CI 게이트
  - Phase 2: DLQ/재처리/quorum queue 표준 적용
  - Phase 3: 메시징 계층 확장(다중 AZ, mTLS, 리전 분산) 검토

## Interfaces & Data Structures

### Core Interfaces

```yaml
messaging_gateway_contract:
  routers:
    - schema-registry
    - kafka-connect
    - kafka-rest
    - kafka-ui
    - rabbitmq
  required_middlewares:
    - gateway-standard-chain@file
  privileged_routers:
    - kafka-ui
    - rabbitmq
  required_auth_middlewares:
    - sso-errors@file
    - sso-auth@file
```

## Catalog-aligned Expansion Targets

- Kafka:
  - 토픽 거버넌스(보존/compaction/파티션 기준) 표준화. 단, 전역 `retention.ms` 값은 현재 compose에 고정 선언되어 있지 않다.
  - DLQ + 재처리 파이프라인 표준화
- RabbitMQ:
  - quorum queue 적용 범위 확정
  - dead-letter + retry 정책 표준화
- Gateway 연계:
  - 관리 경로 보안 헤더 템플릿화
  - 서비스별 라우터 접근 제어 정책(SSO/IP allowlist) 고도화

## Edge Cases & Error Handling

- `gateway-standard-chain` 미적용 시 관리 API burst 트래픽에서 오류 전파 가능성이 높아진다.
- 부동 태그 이미지 사용 시 예기치 않은 런타임 회귀가 발생할 수 있다.
- 잘못된 상대 경로 볼륨 마운트는 개발 환경에서 부트 실패를 유발한다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Traefik 미들웨어 적용 후 관리 UI 접근 실패
- **Fallback**: 관련 라우터 middleware label을 직전 안정 버전으로 롤백
- **Human Escalation**: Messaging Operator + Gateway Operator 공동 승인 후 정책 조정

## Verification

```bash
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh
docker compose --env-file .env.example --profile messaging config --services
bash scripts/hardening/check-all-hardening.sh 05-messaging
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-doc-traceability.sh
```

Service-local compose 검증 경계:

- `infra/05-messaging/kafka/docker-compose.yml`, `infra/05-messaging/kafka/docker-compose.dev.yml`, `infra/05-messaging/rabbitmq/docker-compose.yml`는 root `infra_net` 및 root-managed secrets context 없이 `--profile messaging config`를 실행하면 `undefined network infra_net`로 실패한다.
- Full 3 broker Kafka compose 검증은 root network/secret context 또는 명시적인 임시 validation overlay가 있는 로컬 환경에서만 service-local로 실행한다.

가능 환경에서 runtime 검증:

```bash
docker compose --profile messaging up -d kafka-1 schema-registry kafka-connect kafka-rest-proxy kafbat-ui kafka-exporter kafka-init rabbitmq
docker inspect --format '{{json .State.Health}}' kafka-1
docker inspect --format '{{json .State.Health}}' rabbitmq
```

## Success Criteria & Verification Plan

- **VAL-SPC-MSG-001**: `check-all-hardening.sh 05-messaging` 실패 0건
- **VAL-SPC-MSG-002**: root profile 메시징 compose 정적 검증 통과 및 service-local compose context boundary 기록
- **VAL-SPC-MSG-003**: 외부 노출 라우터의 middleware 체인 계약 충족
- **VAL-SPC-MSG-004**: 01~09 optimization-hardening 문서 상호 링크 동기화

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/05-messaging/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/05-messaging/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/runbooks/05-messaging/optimization-hardening.md)
- **Catalog**: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
