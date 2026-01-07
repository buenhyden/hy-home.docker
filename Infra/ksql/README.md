# ksqlDB

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: Apache Kafka 위에 구축된 이벤트 스트리밍 데이터베이스입니다.  
표준 SQL과 유사한 구문을 사용하여 실시간 데이터 스트림을 필터링, 변환, 조인 및 집계할 수 있습니다.

## 2. 주요 기능 (Key Features)
- **Stream Processing with SQL**: SQL 쿼리로 복잡한 스트림 처리 로직 구현 (CREATE STREAM, CREATE TABLE).
- **Push Queries**: 데이터가 변경될 때마다 실시간으로 클라이언트에 업데이트를 푸시.
- **Pull Queries**: 현재 상태(State)를 조회하는 전통적인 DB 스타일의 쿼리 지원.
- **Connect Integration**: Kafka Connect와 연동하여 외부 소스/싱크 처리.

## 3. 기술 스택 (Tech Stack)
- **Image**: `bitnami/ksql:latest` (Note: Confluent 이미지가 아닌 Bitnami 이미지를 사용 중)
- **Dependency**: Apache Kafka Cluster

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 데이터 흐름
1.  **Ingest**: Kafka Topic으로 데이터 유입.
2.  **Process**: ksqlDB Server가 스트림/테이블 쿼리를 실행하여 실시간 처리.
3.  **Sink**: 처리 결과를 다시 Kafka Topic으로 저장하거나, Connect를 통해 외부 DB로 전송.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **주의**: `KSQL_BOOTSTRAP_SERVERS` 환경변수가 가리키는 Kafka 브로커(`kafka-0`)가 정상적으로 실행 중이어야 합니다. 현재 Kafka 설정과 불일치할 경우 수정이 필요합니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 CLI 접속 (ksqlDB CLI)
ksqlDB Server 컨테이너 내부 또는 별도의 CLI 컨테이너를 통해 접속할 수 있습니다.

```bash
# ksqlDB CLI 실행 (이미지에 포함된 경우)
docker exec -it ksqldb-node1 ksql http://localhost:8088
```

**기본 쿼리 예제**:
```sql
-- 모든 토픽 확인
SHOW TOPICS;

-- 스트림 생성
CREATE STREAM user_clicks (
    user_id VARCHAR,
    url VARCHAR,
    timestamp VARCHAR
) WITH (
    KAFKA_TOPIC = 'clicks',
    VALUE_FORMAT = 'JSON'
);

-- 실시간 조회 (Push Query)
SELECT * FROM user_clicks EMIT CHANGES;
```

### 6.2 REST API
HTTP 요청으로 쿼리를 실행할 수 있습니다.
- **Endpoint**: `http://localhost:8088/ksql`
- **Method**: POST
- **Body**: `{"ksql": "SHOW STREAMS;", "streamsProperties": {}}`

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `KSQL_BOOTSTRAP_SERVERS`: Kafka 브로커 리스트 (예: `kafka-1:19092,kafka-2:19092`). 현재 설정은 `kafka-0`을 참조하고 있어 확인이 필요합니다.
- `KSQL_LISTENERS`: 리스너 주소 (기본 `:8088`).

### 볼륨 마운트 (Volumes)
- `ksqldb-node-1-data-volume`: `/bitnami/ksql` (서버 상태 및 로그 저장).

### 네트워크 포트 (Ports)
- **8088**: ksqlDB Server API 포트.

## 8. 통합 및 API 가이드 (Integration Guide)
**API Endpoint**:
- Base URL: `http://localhost:8088` (또는 외부 도메인 설정 시 해당 주소)
- Info: `GET /info`
- Query: `POST /query` (HTTP/2 지원 권장)

## 9. 가용성 및 관측성 (Availability & Observability)
**상태 확인**:
- `/healthcheck` 엔드포인트를 통해 서버 상태를 확인할 수 있습니다.
- 로그 확인: `docker logs ksqldb-node1`

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**Command Topic**:
- ksqlDB의 모든 쿼리 정의(DDL)는 Kafka 내부의 `_confluent-ksql-..._command_topic`에 저장됩니다. Kafka 데이터가 보존되면 ksqlDB 서버를 재시작해도 쿼리 상태가 복구됩니다.

## 11. 보안 및 강화 (Security Hardening)
- **Network**: 현재 HTTP(8088)를 사용 중이므로, 프로덕션 환경에서는 SSL/TLS 설정(`ksql.listeners=https://...`)을 적용하거나 Traefik과 같은 Reverse Proxy 뒤에 배치하여 보호해야 합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Broker Connection Fail**: "Could not connect to broker" 에러 발생 시 `KSQL_BOOTSTRAP_SERVERS` 설정이 실제 서비스 실행명(`kafka-1` 등) 및 포트(`19092`)와 일치하는지 확인하십시오.
- **Topic Not Found**: 쿼리하려는 Kafka Topic이 실제로 존재하는지 `SHOW TOPICS;`로 확인하십시오.

---
**공식 문서**: [https://docs.ksqldb.io/](https://docs.ksqldb.io/)
