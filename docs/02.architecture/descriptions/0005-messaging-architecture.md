---
title: "Messaging Architecture Description"
version: "1.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "architecture"
artifact_id: "AD-0005"
parent_ids:
- "REQ-0006"
created: "2026-03-26"
---
# Messaging Architecture Description

## Context and Stakeholders

이 문서는 메시징 계층(`05-messaging`)의 참조 아키텍처와 품질 속성을 정의한다. 고가용성 Apache Kafka (KRaft mode) 클러스터와 경량 RabbitMQ 브로커가 결합된 폴리글랏 메시징 구조를 다룬다.

### Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`hy-home.docker`의 메시징 계층은 시스템의 이벤트 중심 아키텍처(EDA)를 뒷받침한다. Kafka는 대용량 스트리밍 및 이벤트 로그 저장을 담당하며, RabbitMQ는 저지연 작업 큐잉 및 마이크로서비스 간의 단발성 비동기 통신을 담당한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - Kafka Broker Cluster & Metadata (KRaft)
  - Schema Registry & Connect
  - RabbitMQ Server
- **Consumes**:
  - `infra_net` 네트워크 리소스
  - `${DEFAULT_MESSAGE_BROKER_DIR}` 영구 저장소
- **Does Not Own**:
  - 서비스별 비즈니스 토픽 네이밍 규약 (Spec 담당)
  - 메트릭 시각화 (06-observability 담당)
  - ksqlDB stream processing engine (`04-data/analytics/ksql` 담당)
- **Non-goals**:
  - 메시징 계층에서 대용량 BLOB 데이터 직접 저장.

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: service-local full Kafka compose는 3 broker 병렬 쓰기 모델을 제공하고, root-included dev compose는 단일 broker 개발 모델을 제공한다.
- **Security**: 내부망 기반 격리 통신, Traefik 관리 경로 보호, Docker Secrets 기반 Kafbat/RabbitMQ secret 주입을 사용한다.
- **Reliability**: KRaft 쿼럼 기반 고가용성 메타데이터 서비스.
- **Scalability**: 브로커 및 파티션 추가를 통한 수평 확장 지원.
- **Observability**: Kafka broker JMX exporter agent, Kafka Exporter, RabbitMQ healthcheck 및 Prometheus 기반 지표 모니터링.
- **Operability**: Kafbat UI 및 RabbitMQ Management 플러그인 제공.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

메시징 계층은 Kafka REST Proxy를 통해 RESTful 접근도 지원하며, Schema Registry를 통해 Avro/JSON 기반의 데이터 정합성 보장을 가능하게 한다. ksqlDB는 현재 `04-data/analytics/ksql`의 downstream analytics component로 운영한다.

### AI Agent Architecture

- **Model/Provider Strategy**: N/A (인프라 계층 특성).
- **Tooling Boundary**: Topic Manager Tool, Queue Monitor Tool.
- **Memory & Context Strategy**: 최근 메시지 오프셋 저장 및 추적.
- **Guardrail Boundary**: 대기열 소비율 임계치 기반 알림 호출.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - `infra-events`: 시스템 통합 이벤트 스트림.
  - `application-logs`: 애플리케이션 로그 스트림.
  - RabbitMQ `default` VHost 기반 작업 큐.
- **Storage Strategy**: Local SSD 바인딩 기반 고성능 디바이스 사용.
- **Data Boundaries**: 메시징 계층은 current compose가 선언한 토픽과 broker storage 경계를 제공한다. 전역 Kafka retention 값은 현재 compose에 고정 선언되어 있지 않으며, 장기 분석/보관은 `04-data` 계층 책임이다.

## Deployment View

- **Runtime / Platform**: Docker Containers / Linux Host.
- **Deployment Model**: root include path는 Kafka dev single broker + RabbitMQ 1 node를 렌더링한다. `infra/05-messaging/kafka/docker-compose.yml`은 service-local full 3 broker compose이며 root network/secret context가 필요하다.
- **Operational Evidence**: `docker-compose.yml` 기반의 스테이트풀 서비스 관리.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../../01.requirements/0006-messaging.md](../../01.requirements/0006-messaging.md)
- **Spec**: [../../03.specs/006-messaging/spec.md](0005-messaging-architecture.md)
- **ADR**: [../decisions/0005-kafka-vs-rabbitmq-selection.md](../decisions/0005-kafka-vs-rabbitmq-selection.md)
