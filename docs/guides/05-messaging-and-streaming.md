# 📨 Messaging & Streaming Guide (Kafka)

고가용성 메시지 스트리밍 플랫폼인 **Kafka (KRaft mode)** 운영 및 활용 가이드입니다.

## 1. Cluster Overview

이 프로젝트는 무거운 Zookeeper 없이 **KRaft (Kafka Raft)** 모드로 동작하는 3-노드 Kafka 클러스터를 제공합니다.

- **Brokers**: `kafka-1`, `kafka-2`, `kafka-3`
- **Internal Access**: `kafka-1:9092,kafka-2:9092,kafka-3:9092`
- **Controller Quorum**: 각 브로커가 컨트롤러 역할도 동시에 수행합니다.

## 2. Management & UI

### Redpanda Console (Kafka UI)

브라우저를 통해 토픽, 컨슈머 그룹, 메시지 내용을 시각적으로 확인할 수 있습니다.

- **접속 주소**: `https://kafka-ui.${DEFAULT_URL}`
- **주요 기능**: 토픽 생성, 메시지 검색 (Filter/JSON), 커넥터 상태 확인.

## 3. Kafka Ecosystem Components

| 컴포넌트 | 역할 | 접속 정보/UI |
| :--- | :--- | :--- |
| **Schema Registry** | Avro/JSON 스키마 관리 | `http://schema-registry:8081` |
| **Kafka Connect** | 외부 데이터 소스(DB) 연동 | `http://kafka-connect:8083` |
| **REST Proxy** | HTTP를 통한 Kafka 메시지 송수신 | `http://rest-proxy:8082` |

## 4. Operational Best Practices

### Topic Creation

자동 토픽 생성 옵션이 활성화되어 있을 수 있으나, 가급적 명시적으로 생성하는 것을 권장합니다:

- **Partitions**: 최소 3개 (처리량에 비례하여 증가)
- **Replication Factor**: 3 (고가용성 유지)

### Monitoring

`kafka-exporter`가 가동 중이며, Grafana의 "Kafka Dashboard"에서 실시간 지표를 확인할 수 있습니다.

- 주요 지표: `UnderReplicatedPartitions`, `OfflinePartitionsCount`, `Consumer Lag`.

## 5. Troubleshooting

- **Topic Not Reachable**: 컨테이너 내부에서 `kafka-net` 네트워크 연결을 확인하십시오.
- **Log Overflow**: 볼륨 용량이 부족할 경우 Retention 정책(`log.retention.hours`)을 조정해야 합니다.
- **Controller Quorum Loss**: 3개 노드 중 2개 이상이 다운되면 클러스터가 읽기 전용으로 전환되거나 중단될 수 있습니다.
