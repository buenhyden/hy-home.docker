<!-- Target: docs/07.operations/04-data/analytics/warehouses.md -->

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
- **Procedure**: [warehouses.md](../../../07.operations/04-data/analytics/warehouses.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/04-data/analytics/warehouses.md` during the 2026-05-10 operations taxonomy consolidation.

### Warehouse (StarRocks) System Usage

> High-performance analytical database for real-time analytics.

---

#### Overview (KR)

이 문서는 StarRocks 데이터 웨어하우스 시스템에 대한 가이드다. OLAP 엔진의 구조(FE/BE), SQL 인터페이스 사용법, 대규모 데이터 세트의 실시간 분석 및 시각화 도구 연동 방법을 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Data Engineer
- Analytics Developer
- AI Agents

#### Purpose

StarRocks의 분산 분석 아키텍처를 이해하고, 대규모 데이터를 초 단위로 분석할 수 있는 SQL 환경을 구축 및 활용하는 것을 돕는다.

#### Prerequisites

- `hy-home.docker` 인프라 네트워크 (`infra_net`) 지식.
- MySQL 프로토콜 및 SQL 문법 이해.
- `DEFAULT_DATA_DIR` 환경 변수 설정 확인.

#### Step-by-step Instructions

##### 1. Connection via MySQL Client

StarRocks는 MySQL 프로토콜과 호환된다.

```bash
### FE 노드 접속 (기본 포트 9030)
mysql -u root -h starrocks-fe -P 9030
```

##### 2. Creating Tables

StarRocks는 여러 데이터 모델(Duplicate, Aggregate, Primary Key)을 지원한다.

```sql
CREATE DATABASE demo;
USE demo;

CREATE TABLE sales (
    sale_date DATE,
    product_id INT,
    amount DECIMAL(10, 2)
)
ENGINE=OLAP
DUPLICATE KEY(sale_date, product_id)
DISTRIBUTED BY HASH(product_id) BUCKETS 3;

```

##### 3. Data Ingestion (Stream Load)

HTTP API를 사용하여 대량의 데이터를 빠르게 로드한다.

```bash
curl --location-trusted -u root: \
    -H "label:sales_load_1" \
    -H "column_separator:," \
    -T sales_data.csv \
    -XPUT http://starrocks-fe:8030/api/demo/sales/_stream_load
```

#### Common Pitfalls

- **BE Node Alive Status**: BE 노드가 FE에 정상적으로 추가되지 않으면 쿼리가 수행되지 않는다. `SHOW BACKENDS;` 명령어로 상태를 확인해야 한다.
- **Ulimit Restrictions**: BE 노드는 고성능 처리를 위해 높은 `ulimit` 설정을 요구한다. 컨테이너 내부 또는 호스트에서 조정이 필요하다.

#### Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [warehouses.md](../../../07.operations/04-data/analytics/warehouses.md)
- **Procedure**: [warehouses.md](../../../07.operations/04-data/analytics/warehouses.md)

## Procedure

> Migrated from `docs/07.operations/04-data/analytics/warehouses.md` during the 2026-05-10 operations taxonomy consolidation.

### StarRocks Recovery Procedure

: StarRocks Cluster & Load Job Recovery

---

#### Overview (KR)

이 런북은 StarRocks FE/BE 노드 장애, 데이터 로드 실패 및 분석 쿼리 타임아웃 상황에 대한 대응 절차를 정의한다. 분산 분석 엔진의 가용성을 복원하고 일관성 있는 쿼리 환경을 유지하기 위한 단계를 제공한다.

#### Purpose

OLAP 워크로드의 가동 중단을 방지하고, 대규모 데이터 세트의 수집 및 쿼리 무결성을 복구하는 것을 목적으로 한다.

#### Canonical References

- `[../../02.ard/0012-data-analytics-architecture.md]`
- `[../../07.operations/04-data/analytics/warehouses.md]`
- `[../../07.operations/04-data/analytics/warehouses.md]`

#### When to Use

- `SHOW BACKENDS;` 결과 BE 노드 상태가 `Alive: false`인 경우.
- `Stream Load` 작업이 `CANCELLED` 상태로 종료되거나 멱등성 에러 발생 시.
- FE 노드(9030 포트)에 접속이 불가능할 때.

#### Procedure or Checklist

##### Checklist

- [ ] FE 노드와 BE 노드 프로세스 생존 확인
- [ ] BE 노드의 `storage_root_path` 디스크 용량 확인
- [ ] FE 노드 메타데이터(`fe/meta`)의 정합성 확인

##### Procedure

1. **클러스터 상태 확인 (MySQL 접속)**:

   ```sql
   SHOW FRONTENDS;
   SHOW BACKENDS;
   ```

2. **BE 노드 재활성화**:
   BE 노드가 중단되었다면 재시작 후 상태를 확인한다.

   ```bash
   docker compose restart starrocks-be
   -- MySQL에서 확인
   SHOW BACKENDS;
   ```

3. **데이터 로드 작업 재시도**:
   실패한 로드를 새 레이블로 다시 시도하거나 원인을 분석한다.

   ```sql
   SHOW LOAD FROM demo WHERE label = 'my_failed_label';
   ```

4. **FE 메타데이터 복구 (임계 상황)**:
   FE 노드가 시작되지 않을 경우 백업된 메타데이터를 사용하여 복구 모드로 시작한다.

#### Verification Steps

- [ ] `SELECT 1;` 또는 샘플 테이블 조회를 통해 쿼리 가능 여부 확인.
- [ ] `SHOW BACKENDS;`에서 모든 BE 노드가 `Alive: true`인지 확인.

#### Observability and Evidence Sources

- **Signals**: StarRocks `be_healthy`, `fe_healthy`, `query_latency`.
- **Evidence to Capture**: BE 노드 `be.INFO` 로그, FE 노드 `fe.log`.

#### Safe Rollback or Recovery Procedure

- [ ] 메타데이터 변경 전 `meta` 디렉터리 압축 백업.
- [ ] BE 노드 추가/삭제 전 반드시 `ALTER SYSTEM DROP BACKEND` 등 정식 절차 준수.

#### Related Operational Documents

- **Operations**: [docs/07.operations/04-data/analytics/warehouses.md](../../../07.operations/04-data/analytics/warehouses.md)

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
