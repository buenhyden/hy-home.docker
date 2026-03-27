<!-- Target: docs/08.operations/04-data/analytics/ksqldb.md -->

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

- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **Runbook**: [ksqldb.md](../../../09.runbooks/04-data/analytics/ksqldb.md)
