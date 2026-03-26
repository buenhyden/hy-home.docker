# Messaging Architecture Reference Document (ARD)

## Messaging Tier (05-messaging) Architecture Reference Document

## Overview (KR)

이 문서는 메시징 계층(`05-messaging`)의 참조 아키텍처와 품질 속성을 정의한다. 고가용성 Apache Kafka (KRaft mode) 클러스터와 경량 RabbitMQ 브로커가 결합된 폴리글랏 메시징 구조를 다룬다.

## Summary

`hy-home.docker`의 메시징 계층은 시스템의 이벤트 중심 아키텍처(EDA)를 뒷받침한다. Kafka는 대용량 스트리밍 및 이벤트 로그 저장을 담당하며, RabbitMQ는 저지연 작업 큐잉 및 마이크로서비스 간의 단발성 비동기 통신을 담당한다.

## Boundaries & Non-goals

- **Owns**:
  - Kafka Broker Cluster & Metadata (KRaft)
  - Schema Registry & Connect
  - RabbitMQ Server
  - ksqlDB Engine
- **Consumes**:
  - `infra_net` 네트워크 리소스
  - `${DEFAULT_MESSAGE_BROKER_DIR}` 영구 저장소
- **Does Not Own**:
  - 서비스별 비즈니스 토픽 네이밍 규약 (Spec 담당)
  - 메트릭 시각화 (06-observability 담당)
- **Non-goals**:
    - 메시징 계층에서 대용량 BLOB 데이터 직접 저장.

## Quality Attributes

- **Performance**: Kafka 3노드 클러스터로 고성능 병렬 쓰기 보장.
- **Security**: 내부망 기반 격리 통신 및 Vault 기반 시크릿 주입.
- **Reliability**: KRaft 쿼럼 기반 고가용성 메타데이터 서비스.
- **Scalability**: 브로커 및 파티션 추가를 통한 수평 확장 지원.
- **Observability**: JMX Exporter 및 Prometheus 기반 지표 모니터링.
- **Operability**: Kafbat UI 및 RabbitMQ Management 플러그인 제공.

## System Overview & Context

메시징 계층은 Kafka REST Proxy를 통해 RESTful 접근도 지원하며, Schema Registry를 통해 Avro 기반의 강력한 데이터 정합성 보장을 가능하게 한다. ksqlDB는 흐르는 데이터에 대해 실시간 SQL 쿼리를 실행하여 마이크로서비스 엔진의 복잡도를 낮춘다.

## Data Architecture

- **Key Entities / Flows**:
  - `infra-events`: 시스템 통합 이벤트 스트림.
  - `application-logs`: 애플리케이션 로그 스트림.
  - RabbitMQ `default` VHost 기반 작업 큐.
- **Storage Strategy**: Local SSD 바인딩 기반 고성능 디바이스 사용.
- **Data Boundaries**: 메시징 계층은 최대 7일간의 리텐션(Kafka 기준)을 원칙으로 함.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Containers / Linux Host.
- **Deployment Model**: Infrastructure Stack (Kafka 3 Nodes, RabbitMQ 1 Node).
- **Operational Evidence**: `docker-compose.yml` 기반의 스테이트풀 서비스 관리.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: N/A (인프라 계층 특성).
- **Tooling Boundary**: Topic Manager Tool, Queue Monitor Tool.
- **Memory & Context Strategy**: 최근 메시지 오프셋 저장 및 추적.
- **Guardrail Boundary**: 대기열 소비율 임계치 기반 알림 호출.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-05-messaging.md]`
- **Spec**: `[../04.specs/05-messaging/spec.md]`
- **Plan**: `[../05.plans/2026-03-26-05-messaging-standardization.md]`
- **ADR**: `[../03.adr/0005-kafka-vs-rabbitmq-selection.md]`
