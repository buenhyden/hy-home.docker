<!-- Target: docs/05.operations/guides/04-data/analytics/ksqldb.md -->

# ksqlDB Operations Policy

> Operational policy for real-time stream processing and lifecycle.

---

## Overview (KR)

이 문서는 ksqlDB 운영 정책을 정의한다. 스트림 및 테이블의 생성 주명 주기, Kafka 컨슈머 오프셋 관리, 그리고 스트림 프로세싱 자원 할당 기준을 규정한다.

## Policy Scope

이 정책은 ksqlDB 서버 클러스터, 스트림 처리 쿼리, 그리고 연관된 Kafka 브로커 인터페이스를 관리한다.

## Applies To

- **Systems**: ksqlDB Server, ksqlDB CLI
- **Agents**: Stream Logic Optimizers, Event-driven Workflow Agents
- **Environments**: Production, Staging

## Controls

- **Required**:
  - 모든 스트림 처리는 `AUTO_OFFSET_RESET='earliest'`를 기본값으로 하되, 비즈니스 로직에 따라 명시적으로 설정해야 함.
  - 복잡한 조인(Join) 쿼리는 실행 전 성능 영향을 검토해야 함.
  - 모든 쿼리는 `EMIT CHANGES`를 사용하여 스트리밍 결과의 무결성을 보장해야 함.
- **Allowed**:
  - 임시 디버깅용 스트림 및 테이블 생성 (24시간 이내 삭제 권고).
  - Schema Registry를 통한 스키마 진화(Evolution).
- **Disallowed**:
  - 무한 루프를 유발할 수 있는 자기 참조 쿼리 금지.
  - 가용한 JVM 메모리의 90%를 초과하는 대규모 쿼리 실행 제안 금지.

## Exceptions

- 재해 복구 또는 데이터 재처리(Reprocessing) 시, 기존 오프셋을 무시하고 특정 시점부터의 재처리를 승인 하에 허용.

## Verification

- `LIST QUERIES;`를 통한 실행 중인 쿼리 목록 모니터링.
- Kafka 컨슈머 그룹 지연(Lag) 상태 실시간 감지.

## Review Cadence

- Per release (변경 시마다)

## AI Agent Policy Section

- **Eval / Guardrail Threshold**: 쿼리 복잡도 지수가 임계치를 초과할 경우 실행 전 경고 발생.
- **Trace Retention**: ksqlDB 처리 로그는 30일간 보관.

## Related Documents

- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **Procedure**: [ksqldb.md](./ksqldb.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/04-data/analytics/ksqldb.md` during the 2026-05-10 operations taxonomy consolidation.

### ksqlDB System Usage

> Usage for real-time stream processing with ksqlDB in the hy-home.docker ecosystem.

---

#### Overview (KR)

이 문서는 ksqlDB 스트리밍 SQL 엔진에 대한 가이드다. Kafka 스트림과 테이블의 개념, CLI 사용법, 그리고 데이터 생성 패턴을 설명한다. 실시간 데이터 분석 및 변환을 위한 스트림 처리 애플리케이션 구축의 핵심 지침을 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Architect

#### Purpose

이 가이드는 사용자가 SQL을 사용하여 Kafka 스트림 위에 실시간 분석 애플리케이션을 구축하도록 돕는다.

#### Prerequisites

- 정상 작동하는 Kafka 클러스터 (`kafka-1:19092` 접근 가능).
- 정상 작동하는 Schema Registry (`schema-registry:8081` 접근 가능).
- Docker Compose의 `data` 프로필 활성화.

#### Step-by-step Instructions

##### 1. ksqlDB CLI 연결 (Connecting to ksqlDB CLI)

대화형 CLI를 사용하여 스트림 프로세서에 대해 SQL 쿼리를 실행한다.

```bash
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

##### 2. 스트림 생성 (Creating a Stream)

기존 Kafka 토픽에 대해 스키마를 정의한다.

```sql
CREATE STREAM events (
  id VARCHAR,
  val INT,
  timestamp BIGINT
) WITH (
  KAFKA_TOPIC='events',
  VALUE_FORMAT='JSON',
  TIMESTAMP='timestamp'
);
```

##### 3. 실체화된 테이블 생성 (Creating a Materialized Table)

스트림 데이터를 상태가 있는 쿼리 가능한 테이블로 집계한다.

```sql
CREATE TABLE event_counts AS
  SELECT id, COUNT(*) AS total
  FROM events
  GROUP BY id
  EMIT CHANGES;
```

#### Common Pitfalls

- **직렬화 불일치 (Serialization Mismatch)**: `VALUE_FORMAT`이 Kafka의 실제 데이터와 일치하는지 확인한다.
- **컨슈머 그룹 지연 (Consumer Group Lag)**: 에러 확인을 위해 `KSQL_KSQL_LOGGING_PROCESSING_TOPIC`을 모니터링한다.
- **자원 고갈 (Resource Exhaustion)**: ksqlDB는 상당한 메모리를 소비하므로 JVM Heap을 면밀히 모니터링한다.

#### Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../../01.requirements/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../../02.architecture/decisions/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../../03.specs/04-data-analytics/spec.md)
- **Operation**: [ksqldb.md](./ksqldb.md)
- **Procedure**: [ksqldb.md](./ksqldb.md)

## Procedure

> Migrated from `docs/05.operations/04-data/analytics/ksqldb.md` during the 2026-05-10 operations taxonomy consolidation.

### ksqlDB Recovery Procedure

: ksqlDB Stream Processing Recovery

---

#### Overview (KR)

이 런북은 ksqlDB 스트림 처리 지연, 쿼리 실패 및 서버 연결 이슈 상황에 대한 실행 절차를 정의한다. Kafka와의 연결성을 복원하고 처리 무결성을 유지하기 위한 단계를 제공한다.

#### Purpose

실시간 스트림 처리 파이프라인의 중단을 최소화하고, 잘못된 상태를 가진 쿼리를 안전하게 재시작하는 것을 목적으로 한다.

#### Canonical References

- `[../../02.architecture/requirements/0012-data-analytics-architecture.md]`
- `[../../05.operations/04-data/analytics/ksqldb.md]`
- `[../../05.operations/04-data/analytics/ksqldb.md]`

#### When to Use

- ksqlDB 서버가 Kafka 브로커에 연결하지 못할 때.
- `ksql-cli`에서 특정 쿼리의 상태가 `RUNNING`이 아닐 때.
- 컨슈머 래그(Lag)가 급격히 증가하여 실시간성이 훼손될 때.

#### Procedure or Checklist

##### Checklist

- [ ] Kafka 브로커 가용성 확인 (`kafka-1:19092`)
- [ ] Schema Registry 가용성 확인 (`schema-registry:8081`)
- [ ] ksqlDB 서버 로그의 `KafkaException` 발생 여부 확인

##### Procedure

1. **쿼리 상태 점검**:
   CLI에 접속하여 비정상 쿼리를 식별한다.

   ```sql
   SHOW QUERIES;
   DESCRIBE <QUERY_ID>;
   ```

2. **서버 상태 확인**:

   ```bash
   docker compose logs ksqldb-server --tail 50
   ```

3. **실패한 쿼리 재시작**:
   문제 있는 쿼리를 종료하고 다시 등록한다. (상태 보존 주의)

   ```sql
   TERMINATE <QUERY_ID>;
   -- 기존 CREATE 문 실행
   ```

4. **연결성 강제 갱신**:
   Kafka 브로커와의 메타데이터 갱신을 위해 서버를 재시작한다.

   ```bash
   docker compose restart ksqldb-server
   ```

#### Verification Steps

- [ ] `SHOW QUERIES;` 결과 모든 핵심 쿼리가 `RUNNING` 상태인지 확인.
- [ ] 샘플 데이터를 Kafka에 전송하여 결과 테이블이 즉시 업데이트되는지 확인.

#### Observability and Evidence Sources

- **Signals**: Kafka Consumer Lag metrics, ksqlDB `error_rate`.
- **Evidence to Capture**: `EXPLAIN <QUERY>;` 결과물, ksqlDB 서버 에러 스택트레이스.

#### Safe Rollback or Recovery Procedure

- [ ] 쿼리 종료 전 `DESCRIBE EXTENDED <SINK_TOPIC>;`를 통해 현재 오프셋 기록.
- [ ] 데이터 정합성 이슈 시, 오프셋을 특정 시점으로 되돌려 재처리 수행.

#### Related Operational Documents

- **Operations**: [docs/05.operations/04-data/analytics/ksqldb.md](./ksqldb.md)

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
