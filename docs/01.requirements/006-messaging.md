---
status: active
---
<!-- Target: docs/01.requirements/006-messaging.md -->

# Messaging Tier (05-messaging) Product Requirements

## Overview

이 문서는 `hy-home.docker` 아키텍처의 메시징 계층(`05-messaging`)에 대한 제품 요구사항을 정의한다. 고성능 이벤트 스트리밍(Kafka)과 경량 작업 큐(RabbitMQ)를 통해 시스템 전반의 비동기 통신을 지원한다. 스트리밍 SQL 처리(ksqlDB)는 현재 `04-data/analytics` 구현과 운영 문서가 소유한다.

## Vision

시스템 컴포넌트 간의 결합도를 낮추고, 실시간 이벤트 처리 및 신뢰성 있는 메시지 전달을 가능하게 하는 견고한 전용 메시징 인프라를 제공한다.

## Problem Statement

현재 복잡한 마이크로서비스 및 인프라 환경에서 컴포넌트 간의 직접 통신은 확산성이 떨어지고, 데이터 손실 위험과 시스템 가용성 저하를 초래할 수 있다. 다양한 트래픽 특성(고처리량 vs 단순 큐잉)에 대응할 수 있는 계층화된 메시징 솔루션이 필요하다.

## Personas

- **Backend Developers**: 비동기 패턴 및 이벤트 소싱 구현을 위해 메시징 인프라 사용.
- **Data Engineers**: Kafka 토픽, Schema Registry, Kafka Connect를 통해 데이터 파이프라인 입력 경계를 사용.
- **SREs**: 클러스터 가용성, 보존 정책, 복구 절차 관리.
- **AI Agents**: 실시간 이벤트 감지 및 자동화된 반응 처리를 위해 사용.

## Key Use Cases

- **STORY-01**: 시스템 로그 및 이벤트를 Kafka로 수집하여 실시간 분석 및 보관.
- **STORY-02**: 시간이 오래 걸리는 작업을 RabbitMQ 큐에 넣고 비동기 워커가 처리.
- **STORY-03**: Schema Registry와 Kafka Connect를 사용해 이벤트 형식과 커넥터 경계를 검증한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: Apache Kafka (KRaft mode)를 제공한다. `infra/05-messaging/kafka/docker-compose.yml`은 3 broker full compose이며, root `docker-compose.yml`은 dev compose(`docker-compose.dev.yml`)를 include해 단일 broker로 렌더링한다.
- **REQ-PRD-FUN-02**: RabbitMQ를 통한 표준 AMQP 0-9-1 프로토콜 지원.
- **REQ-PRD-FUN-03**: Avro/JSON 스키마 관리를 위한 Schema Registry 제공.
- **REQ-PRD-FUN-04**: 웹 기반 관리 UI(Kafbat, RabbitMQ Management) 제공.
- **REQ-PRD-FUN-05**: Kafka REST Proxy와 Kafka Exporter를 통해 운영 API와 지표 수집 경계를 제공한다.

## Success Criteria

- **REQ-PRD-MET-01**: `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`가 root-included 메시징 구성에서 실패 0건으로 통과한다.
- **REQ-PRD-MET-02**: `bash scripts/hardening/check-all-hardening.sh 05-messaging`가 이미지 핀, 라우터 middleware, SSO, 경로 기준선 회귀를 차단한다.

## Scope and Non-goals

- **In Scope**:
  - Kafka Cluster (KRaft)
  - Schema Registry & Kafka Connect
  - RabbitMQ Broker
  - Kafka REST Proxy
  - Kafka Exporter 및 broker JMX exporter agent
- **Out of Scope**:
  - 개별 서비스 내의 Consumer/Producer 애플리케이션 로직.
  - 외부 클라우드 메시징 서비스(AWS SQS 등).
- **Non-goals**:
  - 메시징 계층에서 데이터를 영구 보관하는 것 (Data 계층의 책임).

## Risks, Dependencies, and Assumptions

- **Risks**: Kafka 노드 장애 시 파티션 리밸런싱 지연 가능성. 스키마 변경 시 하위 호환성 위반 위험.
- **Dependencies**: 인증 및 권한 관리를 위해 `02-auth` 계층에 의존한다. ksqlDB consumer/processing boundary는 `04-data/analytics/ksql`에 의존한다.
- **Assumptions**: 모든 노드는 `infra_net` 내에서 통신하며 전용 볼륨에 데이터를 저장한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: `kafka-init` 기준 토픽 선언 검토, 스키마 등록 상태 조회, 컨슈머 그룹 상태 조회.
- **Disallowed Actions**: 클러스터 전체 리셋, 메시지 보존 주기(Retention) 임의 변경.

## Related Documents

- **ARD**: [Messaging architecture requirements](../02.architecture/requirements/0005-messaging-architecture.md)
- **Spec**: [Messaging technical specification](../03.specs/05-messaging/spec.md)
- **Plan**: [Messaging standardization plan](../04.execution/plans/2026-03-26-05-messaging-standardization.md)
- **ADR**: [Kafka vs RabbitMQ selection decision](../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md)
