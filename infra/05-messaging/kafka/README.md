# Kafka Event Streaming Cluster (05-messaging)

> High-performance, 3-node Kafka cluster in KRaft mode for hy-home.docker.

## Overview

The platform's primary event streaming backbone. This cluster utilizes the Zookeeper-less KRaft architecture for improved scalability and simpler management. It includes a full ecosystem of Schema Registry, Kafka Connect, REST Proxy, and a Management UI (Kafbat). It serves as the SSoT for asynchronous inter-service communication and log aggregation.

## Audience

이 README의 주요 독자:

- **Data Engineers**: 데이터 파이프라인 및 커넥터 구성.
- **Backend Developers**: 이벤트 기반 아키텍처 및 메시지 생산/소비.
- **Operators**: 클러스터 상태 모니터링 및 브로커 관리.
- **AI Agents**: 실시간 이벤트 분석 및 자동화된 토픽 관리.

## Scope

### In Scope

- **3-node Kafka Broker Cluster**: KRaft 기반의 고가용성 클러스터.
- **Confluent Schema Registry**: Avro/JSON 스키마 버전 관리.
- **Kafka Connect**: 외부 시스템 연동용 커넥터 실행 엔진.
- **Kafbat UI**: 웹 기반 관리 대시보드.
- **Observability**: JMX 및 Prometheus Exporter를 통한 지표 수집.

### Out of Scope

- 개별 마이크로서비스의 Consumer/Producer 로직.
- 커스텀 Kafka Connector 개발 (Java SDK 영역).
- 외부 클라우드 관리형 Kafka (MSK/Confluent Cloud) 연동.

## Structure

```text
kafka/
├── jmx-exporter/       # JMX to Prometheus metrics config
├── kafbat-ui/          # UI configuration
├── docker-compose.yml  # Kafka ecosystem orchestration
└── README.md          # This file
```

## How to Work in This Area

1. **Bootstrap**: [Kafka KRaft Guide](../../../docs/07.guides/05-messaging/kafka.md)를 읽고 클러스터 초기 구성 방식을 파악한다.
2. **Configuration**: `docker-compose.yml`의 Broker ID 및 포트 맵핑 설정을 확인한다.
3. **Execution**: 변경 사항 적용 후 `docker compose up -d`로 반영한다.
4. **Validation**: [Messaging Runbook](../../../docs/09.runbooks/05-messaging/kafka.md)의 점검 절차를 수행한다.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Engine     | Confluent CP-Kafka             | v8.1.1                    |
| Mode       | KRaft                          | Integrated Metadata log   |
| Registry   | CP-Schema-Registry             | v8.1.1                    |
| UI         | Kafbat (Kafka UI)              | Web-based management      |
| Exporter   | Kafka Exporter                 | Prometheus metrics        |

## Configuration

### Environment Variables

| Variable | Node 1 | Node 2 | Node 3 | Description |
| :--- | :--- | :--- | :--- | :--- |
| `KAFKA_EXTERNAL_PORT` | 9092 | 9094 | 9096 | 외부 클라이언트 접속 포트 |
| `KAFKA_NODE_ID` | 1 | 2 | 3 | 클러스터 내 고유 노드 ID |
| `CLUSTER_ID` | `${KAFKA_CLUSTER_ID}` | | | 클러스터 식별 UUID |

## Testing

```bash
# internal topic 목록 확인
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list

# schema registry 연결성 확인
curl -fsS http://schema-registry.localhost/subjects
```

## Change Impact

- **브로커 설정 변경**: 순차적 재시작(Rolling Restart)이 필요하며, 가용성 보장을 위해 쿼럼 상태를 확인해야 한다.
- **토픽 정책 변경**: `replication.factor` 축소는 데이터 가용성을 낮추며, `retention` 변경은 디스크 용량에 즉각 영향을 준다.

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. **Initialize Topics**: 새 토픽은 반드시 `docker-compose.yml`의 `kafka-init` 서비스를 통해 관리되도록 설정한다.
2. **Monitor Health**: 브로커 점검 시 `UnderReplicatedPartitions` 지표가 0인지 항상 확인한다.
3. **SSoT Linkage**: 토픽 스펙 변경 시 `docs/04.specs/05-messaging/spec.md`를 함께 갱신한다.

## Related References

- **PRD**: [05-messaging](../../../docs/01.prd/2026-03-26-05-messaging.md)
- **ARD**: [Messaging Architecture](../../../docs/02.ard/0005-messaging-architecture.md)
- **Guide**: [Kafka Guide](../../../docs/07.guides/05-messaging/kafka.md)
- **Ops**: [Messaging Ops](../../../docs/08.operations/05-messaging/kafka.md)
- **Runbook**: [Messaging Recovery](../../../docs/09.runbooks/05-messaging/kafka.md)
