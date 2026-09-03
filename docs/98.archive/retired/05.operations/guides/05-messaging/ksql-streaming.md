---
status: active
---

<!-- Target: docs/05.operations/guides/05-messaging/ksql-streaming.md -->

# ksqlDB Streaming Operations

## Usage

### Overview (KR)

이 가이드는 Kafka 스트림 데이터에 대해 SQL 질의가 가능한 ksqlDB(05-messaging)의 활용 방법을 설명한다. 실시간 데이터 정제, 조인(Join), 그리고 구체화된 뷰(Materialized View) 생성을 다룬다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Operators
- Developers
- Contributors
- AI Agents

### Purpose

- ksqlDB Streaming Operations의 운영 사용 맥락을 빠르게 파악한다.
- 반복 실행 절차와 장애 대응은 연결된 runbook으로 넘긴다.
- 통제 기준은 연결된 policy 문서와 분리해 유지한다.

### Prerequisites

- Repository checkout 접근 가능
- 관련 `docs/03.specs/` 또는 operations 문서 확인 가능
- 필요한 경우 Docker/Docker Compose 명령 실행 권한

### Step-by-step Instructions

1. 이 문서의 overview와 usage context를 확인한다.
2. 관련 service, configuration, 또는 documentation target을 식별한다.
3. `## Common Checks`의 검증 항목을 실행하거나 검토한다.
4. 반복 절차, 장애 대응, rollback, escalation이 필요하면 `## Runbook Handoff`의 runbook으로 이동한다.

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

### ksqlDB Usage (05-messaging)

> Real-time Streaming SQL and Data Transformation for Kafka.

#### Service Components

- **ksqlDB Server**: 실시간 SQL 처리 엔진 (`8088`).
- **ksqlDB CLI**: 대화형 질의 인터페이스.
- **Datagen**: 테스트 데이터 생성을 위한 유틸리티 컨테이너.

#### Streaming Patterns

##### 1. Simple Stream Creation

```sql
CREATE STREAM orders (id INT, product STRING, price DOUBLE)
  WITH (KAFKA_TOPIC='orders_topic', VALUE_FORMAT='AVRO');
```

##### 2. Materialized Views

```sql
CREATE TABLE total_sales AS
  SELECT product, SUM(price) FROM orders GROUP BY product;
```

#### Maintenance Tasks

- **CLI Access**: `docker compose run --rm ksql-cli ksql http://ksqldb-server:8088`
- **Resource Limit**: ksqlDB는 대규모 스테이트(State)를 로컬 디스크에 저장하므로, 호스트 볼륨 공간을 상시 확인한다.

#### Troubleshooting

- **State Store Corruption**: 서버 비정상 종료 시 RocksDB 상태가 깨질 수 있다. `05.operations`를 참조하여 상태 리셋을 수행한다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없습니다.

## Related Documents

- [Operations index](../../README.md)
