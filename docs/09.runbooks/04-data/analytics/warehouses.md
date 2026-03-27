<!-- Target: docs/09.runbooks/04-data/analytics/warehouses.md -->

# StarRocks Recovery Runbook

: StarRocks Cluster & Load Job Recovery

---

## Overview (KR)

이 런북은 StarRocks FE/BE 노드 장애, 데이터 로드 실패 및 분석 쿼리 타임아웃 상황에 대한 대응 절차를 정의한다. 분산 분석 엔진의 가용성을 복원하고 일관성 있는 쿼리 환경을 유지하기 위한 단계를 제공한다.

## Purpose

OLAP 워크로드의 가동 중단을 방지하고, 대규모 데이터 세트의 수집 및 쿼리 무결성을 복구하는 것을 목적으로 한다.

## Canonical References

- `[../../02.ard/0012-data-analytics-architecture.md]`
- `[../../07.guides/04-data/analytics/warehouses.md]`
- `[../../08.operations/04-data/analytics/warehouses.md]`

## When to Use

- `SHOW BACKENDS;` 결과 BE 노드 상태가 `Alive: false`인 경우.
- `Stream Load` 작업이 `CANCELLED` 상태로 종료되거나 멱등성 에러 발생 시.
- FE 노드(9030 포트)에 접속이 불가능할 때.

## Procedure or Checklist

### Checklist

- [ ] FE 노드와 BE 노드 프로세스 생존 확인
- [ ] BE 노드의 `storage_root_path` 디스크 용량 확인
- [ ] FE 노드 메타데이터(`fe/meta`)의 정합성 확인

### Procedure

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

## Verification Steps

- [ ] `SELECT 1;` 또는 샘플 테이블 조회를 통해 쿼리 가능 여부 확인.
- [ ] `SHOW BACKENDS;`에서 모든 BE 노드가 `Alive: true`인지 확인.

## Observability and Evidence Sources

- **Signals**: StarRocks `be_healthy`, `fe_healthy`, `query_latency`.
- **Evidence to Capture**: BE 노드 `be.INFO` 로그, FE 노드 `fe.log`.

## Safe Rollback or Recovery Procedure

- [ ] 메타데이터 변경 전 `meta` 디렉터리 압축 백업.
- [ ] BE 노드 추가/삭제 전 반드시 `ALTER SYSTEM DROP BACKEND` 등 정식 절차 준수.

## Related Operational Documents

- **Operations**: [docs/08.operations/04-data/analytics/warehouses.md](../../08.operations/04-data/analytics/warehouses.md)
