# ksqlDB

**ksqlDB**는 Apache Kafka를 위한 이벤트 스트리밍 데이터베이스입니다.
SQL 구문을 사용하여 실시간 데이터 스트림을 필터링, 변환 및 집계할 수 있습니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **ksqldb-node1** | ksqlDB 서버 노드 | `8088` |

## 🛠 설정 및 환경 변수

- **이미지**: `bitnami/ksql:latest`
- **Kafka 연결**: `KSQL_BOOTSTRAP_SERVERS=kafka-0:...` (Kafka 서비스에 의존)

## 📦 볼륨 마운트

- `ksqldb-node-1-data-volume`: 데이터 저장소

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **의존성**: `Docker/Infra/kafka` 서비스가 먼저 실행되어 있어야 합니다.
