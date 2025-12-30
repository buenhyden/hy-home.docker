# KSQL (KsqlDB) Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 Kafka 스트림 처리를 위한 KsqlDB 구성을 담고 있습니다. 현재는 단일 노드(`ksqldb-node1`) 구성이 활성화되어 있으며, Server/CLI 모드는 주석 처리되어 있습니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **ksqldb-node1** | Stream Processing Node| Kafka 클러스터와 연동하여 실시간 스트림 처리를 수행하는 KsqlDB 노드입니다. |

## 3. 구성 및 설정 (Configuration)

### 연결
- **Kafka**: `kafka-0` 브로커를 부트스트랩 서버로 사용하도록 설정되어 있습니다 (`KSQL_BOOTSTRAP_SERVERS`). (참고: 실제 Kafka 클러스터 서비스명은 `kafka-1` 등이므로 연결 테스트가 필요할 수 있습니다.)

### 데이터 볼륨
- `ksqldb-node-1-data-volume`: 호스트의 `${DEFAULT_DATABASE_DIR}/ksqldb/node1` 경로에 바인드 마운트되어 데이터를 저장합니다.

### 참고 사항
- 현재 `docker-compose.yml`에는 `ksqldb-server`와 `ksqldb-cli` 서비스가 정의되어 있으나 주석 처리된 상태입니다. 필요 시 활성화하여 사용할 수 있습니다.
