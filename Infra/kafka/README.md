# Kafka Ecosystem Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 Confluent Platform 기반의 Kafka 생태계를 정의합니다. ZooKeeper를 제거하고 KRaft 모드로 동작하는 3-Node Kafka 클러스터를 중심으로, 스키마 레지스트리, 커넥트, REST 프록시, UI 및 모니터링 도구를 포함하고 있습니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **kafka-1, 2, 3** | Event Broker | KRaft 모드로 동작하는 Kafka 브로커 및 컨트롤러 노드입니다. |
| **schema-registry** | Schema Registry | Avro, JSON Schema 등을 관리하고 유효성을 검증하는 중앙 레지스트리입니다. |
| **kafka-connect** | Integration | 데이터 소스와 싱크를 연결하는 분산 모드 Kafka Connect입니다. |
| **kafka-rest-proxy**| REST API | HTTP REST 클라이언트가 Kafka 클러스터에 접근할 수 있도록 하는 프록시입니다. |
| **kafka-ui** | Web UI (Provectus)| Kafka 클러스터, 토픽, 커넥터 등을 시각적으로 관리하고 모니터링하는 인터페이스입니다. |
| **kafka-exporter** | Metrics Exporter | Kafka 클러스터의 메트릭(Lag 등)을 수집하여 Prometheus에 제공합니다. |

## 3. 구성 및 설정 (Configuration)

### Kafka Cluster (KRaft)
- **Node ID**: 1, 2, 3
- **Roles**: 각 노드가 Broker와 Controller 역할을 겸임합니다.
- **Replication**: 오프셋 및 상태 로그의 복제 계수는 3으로 설정되어 고가용성을 보장합니다.

### Listeners
- `PLAINTEXT`: 브로커 간 내부 통신 (19092)
- `CONTROLLER`: 컨트롤러 간 통신 (9093)
- `EXTERNAL`: 외부 클라이언트 접속용 (호스트 포트 매핑)

### 주요 환경 변수
- `CLUSTER_ID`: 클러스터 식별자
- `KAFKA_HEAP_OPTS`: JVM 메모리 설정
- `CONNECT_BOOTSTRAP_SERVERS`: Connect가 접속할 브로커 목록

### 로드밸런싱 (Traefik)
- **Kafka UI**: `https://kafka-ui.${DEFAULT_URL}`
- **Schema Registry**: `https://schema-registry.${DEFAULT_URL}`
- **Kafka Connect**: `https://kafka-connect.${DEFAULT_URL}`
- **Kafka REST Proxy**: `https://kafka-rest.${DEFAULT_URL}`

### 데이터 볼륨
각 브로커 및 Connect는 별도의 Docker 볼륨을 사용하여 데이터를 영구 저장합니다.
- `kafka-1-data`, `kafka-2-data`, `kafka-3-data`
- `kafka-connect-data`
