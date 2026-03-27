<!-- Target: docs/08.operations/04-data/analytics/warehouses.md -->

# StarRocks Operations Policy

> Operational policy for OLAP data warehousing and resource management.

---

## Overview (KR)

이 문서는 StarRocks 데이터 웨어하우스 운영 정책을 정의한다. 대규모 분석 쿼리에 대한 동시성 제어, BE 노드의 데이터 분산 정책, 그리고 쿼리 타임아웃 및 자원 격리 기준을 규정한다.

## Policy Scope

이 정책은 StarRocks Frontend(FE) 메타데이터 노드와 Backend(BE) 컴퓨팅 노드 클러스터를 관리한다.

## Applies To

- **Systems**: StarRocks (FE/BE), Stream Load Jobs, Export Tasks
- **Agents**: SQL Query Optimizers, Data Ingestion Automators
- **Environments**: Production (Distributed Cluster), Staging

## Controls

- **Required**:
  - 모든 테이블은 명확한 파티션(Partition) 및 버킷(Bucket) 전략을 가져야 함.
  - 고성능 처리를 위해 BE 노드의 CPU 및 메모리 사용량을 85% 이하로 유지.
  - 데이터 로드 작업 시 레이블(Label)을 사용하여 멱등성(Idempotency)을 보장함.
- **Allowed**:
  - `Resource Group` 설정을 통한 분석 쿼리와 서비스 쿼리의 자원 격리.
  - 외부 카탈로그(MySQL, Iceberg 등) 연동을 통한 연합 쿼리 수행.
- **Disallowed**:
  - `SELECT *`와 같은 무분별한 대량 데이터 스캔 쿼리 제안 금지 (최소 필터 조건 포함 필수).
  - FE 노드 메타데이터 수동 수정을 통한 스키마 변경 시도 방지.

## Exceptions

- 긴급 데이터 복구 시, 일시적으로 동시 쿼리 수 제한을 상향 조정 가능.

## Verification

- `SHOW BACKENDS;` 및 `SHOW FRONTENDS;`를 통한 노드 생존 확인.
- `information_schema.queries_history`를 통한 롱-러닝 쿼리 모니터링.

## Review Cadence

- Monthly (월별)

## AI Agent Policy Section

- **Model Rollback**: 쿼리 생성 에이전트의 로직 변경 후 재시도 실패율 5% 초과 시 즉시 롤백.
- **Eval / Guardrail Threshold**: 스캔 데이터량이 1TB를 초과하는 쿼리는 실행 전 관리자 승인 필요.

## Related Documents

- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **Runbook**: [warehouses.md](../../../09.runbooks/04-data/analytics/warehouses.md)
