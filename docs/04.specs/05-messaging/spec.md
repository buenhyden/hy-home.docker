# 05-Messaging Optimization Hardening Specification

## Overview (KR)

이 문서는 `infra/05-messaging` 계층의 최적화/하드닝 구현 계약을 정의한다. Kafka/RabbitMQ 관리 경로의 게이트웨이 제어(레이트리밋/재시도/회로차단), 이미지 태그 고정, 개발 Compose 정합성, CI 기준선 검증을 핵심 범위로 다룬다.

## Strategic Boundaries & Non-goals

- 본 Spec은 메시징 인프라 구성 하드닝과 운영/문서 추적성 계약을 소유한다.
- Kafka/RabbitMQ 애플리케이션 레벨 Producer/Consumer 로직 변경은 범위 밖이다.

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-05-messaging-optimization-hardening.md](../../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../../02.ard/0020-messaging-optimization-hardening-architecture.md](../../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0005-kafka-vs-rabbitmq-selection.md](../../03.adr/0005-kafka-vs-rabbitmq-selection.md)
  - [../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md](../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - `kafbat-ui` 이미지는 부동 태그(`:main`)를 금지하고 고정 버전을 사용한다.
  - 외부 노출 라우터는 `gateway-standard-chain@file`를 적용한다.
  - 관리 UI 라우터(`kafka-ui`, `kafbat-ui-dev`, `rabbitmq`)는 SSO 미들웨어 체인을 유지한다.
  - `docker-compose.dev.yml`의 로컬 볼륨 경로는 서비스 디렉터리 기준 상대 경로를 사용한다.
- **Data / Interface Contract**:
  - Kafka/KRaft 3노드 및 RabbitMQ 단일 노드 운영 모델을 유지한다.
  - TLS 종료는 Traefik에서 수행하고 내부 `infra_net` 통신은 서비스 내부 프로토콜을 사용한다.
- **Governance Contract**:
  - `scripts/check-messaging-hardening.sh`를 CI `messaging-hardening` job으로 강제한다.
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
  - Kafka (Confluent CP 8.1.1)
  - RabbitMQ 4.2.x
  - Kafbat/Provectus UI
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
  - 토픽 거버넌스(보존/compaction/파티션 기준) 표준화
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
docker compose -f infra/05-messaging/kafka/docker-compose.yml config
docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config
docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config
bash scripts/check-messaging-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

가능 환경에서 runtime 검증:

```bash
docker compose -f infra/05-messaging/kafka/docker-compose.yml --profile messaging up -d
docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml --profile messaging-option up -d
docker inspect --format '{{json .State.Health}}' kafka-1
docker inspect --format '{{json .State.Health}}' rabbitmq
```

## Success Criteria & Verification Plan

- **VAL-SPC-MSG-001**: `check-messaging-hardening` 실패 0건
- **VAL-SPC-MSG-002**: Kafka/RabbitMQ compose 정적 검증 통과
- **VAL-SPC-MSG-003**: 외부 노출 라우터의 middleware 체인 계약 충족
- **VAL-SPC-MSG-004**: 01~09 optimization-hardening 문서 상호 링크 동기화

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/05-messaging/optimization-hardening.md](../../07.guides/05-messaging/optimization-hardening.md)
- **Operations**: [../../08.operations/05-messaging/optimization-hardening.md](../../08.operations/05-messaging/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/05-messaging/optimization-hardening.md](../../09.runbooks/05-messaging/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
