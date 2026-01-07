# Confluent Kafka Platform

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 고성능 분산 이벤트 스트리밍 플랫폼입니다.  
실시간 데이터 파이프라인 구축, 마이크로서비스 간 비동기 통신, 스트림 프로세싱을 위한 핵심 인프라를 제공합니다.

## 2. 주요 기능 (Key Features)
- **KRaft Mode**: ZooKeeper에 대한 의존성을 제거하고 자체 Raft 쿼럼 기반의 컨트롤러를 사용하여 관리 복잡성을 줄이고 안정성을 높였습니다.
- **Schema Registry**: Avro, Protobuf 등의 스키마를 중앙에서 관리하고 호환성을 검증합니다.
- **Kafka Connect**: 다양한 데이터 소스(DB, 파일 등)와 카프카 간의 데이터 이동을 코드 없이 설정만으로 수행합니다.
- **Kafka UI**: 클러스터 상태, 토픽 데이터, 컨슈머 그룹 등을 웹 브라우저에서 직관적으로 모니터링하고 관리합니다.

## 3. 기술 스택 (Tech Stack)
- **Broker**: Confluent Kafka 7.7.7 (KRaft)
- **Components**: Schema Registry, Kafka Connect, REST Proxy
- **Monitoring**: Provectus Kafka UI (`v0.7.2`), Kafka Exporter

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 클러스터 구조
- **3-Node Brokers**: `kafka-1`, `kafka-2`, `kafka-3` 3개의 노드가 데이터를 분산 저장하고 복제합니다.
- **Controller Quorum**: 3개 노드 모두 컨트롤러 역할(투표권 보유)을 겸임하여 고가용성을 보장합니다.
- **Tools**: Schema Registry, Connect, REST Proxy가 브로커와 내부망을 통해 긴밀하게 연동됩니다.

### 워크플로우
1.  **Producer**: 데이터 생성 -> Schema Registry(스키마 검증) -> Kafka Broker(저장).
2.  **Broker**: 내부적으로 설정된 복제 계수(RF=3)에 따라 다른 브로커로 데이터 복제.
3.  **Consumer**: Kafka Broker -> 데이터 읽기 -> 로직 처리.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **주의**: 3개의 브로커가 서로 통신하며 쿼럼을 형성해야 하므로, "Started" 상태가 되어도 서비스 준비까지 약간의 시간(1~2분)이 소요될 수 있습니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Kafka UI 사용
1.  **접속**: `https://kafka-ui.${DEFAULT_URL}`
2.  **기능**:
    - **Topics**: 토픽 생성, 설정 변경, 메시지 샘플링.
    - **Consumers**: 컨슈머 그룹의 Lag(지연) 모니터링.
    - **Schema Registry**: 스키마 등록 및 버전 관리.
    - **Kafka Connect**: 커넥터 생성 및 상태 확인.

### 6.2 CLI 사용법 (Inside Container)
컨테이너 내부에서 Kafka CLI 도구를 직접 사용할 수 있습니다.

**토픽 생성**:
```bash
docker exec -it kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic my-topic --partitions 3 --replication-factor 3
```

**메시지 전송 (Producer)**:
```bash
docker exec -it kafka-1 kafka-console-producer --bootstrap-server localhost:19092 \
  --topic my-topic
> Hello Kafka
```

**메시지 수신 (Consumer)**:
```bash
docker exec -it kafka-1 kafka-console-consumer --bootstrap-server localhost:19092 \
  --topic my-topic --from-beginning
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `KAFKA_NODE_ID`: 각 브로커의 고유 ID (1, 2, 3).
- `KAFKA_CONTROLLER_QUORUM_VOTERS`: 쿼럼 투표 멤버 목록 (`1@kafka-1...`).
- `KAFKA_AUTO_CREATE_TOPICS_ENABLE`: `true` (개발 편의를 위해 존재하지 않는 토픽 자동 생성).
- `KAFKA_MIN_INSYNC_REPLICAS`: `2` (최소 2개 이상의 복제본이 확인되어야 쓰기 성공).

### 네트워크 포트 (Ports)
- **Broker (External)**: 각 노드별 외부 포트 매핑 (Host -> Container).
- **Broker (Internal)**: 19092 (PLAINTEXT), 9093 (CONTROLLER).
- **Schema Registry**: 8081
- **UI**: 8080 (`https://kafka-ui.${DEFAULT_URL}`)

## 8. 통합 및 API 가이드 (Integration Guide)
**Bootstrap Servers (Internal)**:
- `kafka-1:19092,kafka-2:19092,kafka-3:19092`

**Schema Registry URL**:
- `http://schema-registry:8081`

**REST Proxy URL**:
- `http://kafka-rest-proxy:8082`

## 9. 가용성 및 관측성 (Availability & Observability)
**고가용성 (HA)**:
- 3개 노드 중 1개 노드가 다운되어도 정상적인 읽기/쓰기가 가능합니다 (`min.insync.replicas=2` 충족 시).

**모니터링**:
- `kafka-exporter` 컨테이너가 `/metrics` 엔드포인트를 제공하며, Prometheus가 이를 수집합니다.
- Kafka UI에서 대시보드 형태의 시각적 모니터링을 제공합니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- **Volume**: 각 브로커의 `kafka-X-data` 볼륨이 중요합니다.
- **DR**: 재해 복구를 위해 MirrorMaker2를 사용하여 이기종/원격지 클러스터로 실시간 미러링을 구성하는 것이 표준입니다.

## 11. 보안 및 강화 (Security Hardening)
- **Network Isolation**: 현재 내부 통신은 암호화되지 않은 `PLAINTEXT`를 사용하므로, 신뢰할 수 있는 Docker Network 내부에서만 접근하도록 제한해야 합니다.
- **Authentication**: 외부 노출되는 Kafka UI는 Traefik 미들웨어(SSO 등)를 통해 보호되고 있는지 확인하세요.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Cluster ID Mismatch**: 볼륨을 초기화하지 않고 컨테이너를 재생성할 때 `CLUSTER_ID`가 변경되면 발생합니다. 볼륨을 함께 삭제(`docker compose down -v`)하고 재시작하세요.
- **Not Enough Replicas**: 활성 브로커 수가 `min.insync.replicas`보다 적으면 쓰기 요청이 거부됩니다.

**진단 명령어**:
```bash
# 브로커 API 버전 및 연결 상태 확인
docker exec -it kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092
```

---
**공식 문서**: [https://docs.confluent.io/](https://docs.confluent.io/)
