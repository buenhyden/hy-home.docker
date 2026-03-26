<!-- Target: docs/09.runbooks/04-data/analytics/warehouses.md -->

# Warehouse (StarRocks) Recovery Runbook

: StarRocks Node Maintenance & Health Recovery

---

## Overview (KR)

이 런북은 StarRocks 클러스터 장애 발생 시 대응 절차를 정의한다. FE/BE 노드 상태 복구, 메타데이터 손상 해결, 디스크 부족에 따른 데이터 재배치 단계를 제공한다.

## Purpose

StarRocks 서비스 중단 또는 쿼리 실패 발생 시 운영자가 신속하게 노드 상태를 복구하고 데이터 무결성을 확보하도록 돕는다.

## Canonical References

- `[../../02.ard/0004-data-architecture.md]`
- `[../../../07.guides/04-data/analytics/warehouses.md]`
- `[../../../08.operations/04-data/analytics/warehouses.md]`

## When to Use

- `SHOW FRONTENDS;` 결과 `Alive: false` 일 때.
- `SHOW BACKENDS;` 결과 BE 노드가 정상적으로 등록되지 않거나 `Alive: false` 일 때.
- 쿼리 수행 시 `No alive backends` 에러가 발생할 때.

## Procedure or Checklist

### Checklist

- [ ] `mysql -u root -h starrocks-fe -P 9030 -e "SHOW FRONTENDS; SHOW BACKENDS;"` 확인.
- [ ] Docker logs (`docker compose logs starrocks-fe`) 확인.
- [ ] 디스크 공간 및 BE 스토리지 경로 (`/opt/starrocks/be/storage`) 읽기/쓰기 권한 확인.

### Procedure

#### 1. FE Cluster Metadata Recovery

FE 노드가 시작되지 않는 경우 메타데이터 디렉토리를 확인한다.

```bash
# FE 메타데이터 디렉토리 상태 확인
ls -la ${DEFAULT_DATA_DIR}/starrocks/fe/meta
# 비정상 종료 시 이미지 재생성 또는 볼륨 복구 수행
```

#### 2. BE Node Re-registration

BE 노드가 FE에 자동으로 연결되지 않는 경우 수동으로 추가한다.

```sql
-- FE 접속 후 수행
ALTER SYSTEM ADD BACKEND "starrocks-be:9050";
```

#### 3. Data Balancing and Disk Cleanup

BE 노드 디스크 잔량이 부족한 경우 불필요한 태블릿을 정리하거나 노드를 추가한다.

```sql
-- 데이터 재배치 상태 확인
SHOW PROC '/cluster_balance';
```

## Verification Steps

- [ ] `SHOW FRONTENDS;` 결과에 FE 노드가 `Alive: true`인가?
- [ ] `SHOW BACKENDS;` 결과에 모든 BE 노드가 `Alive: true`인가?
- [ ] 9030 포트를 통한 SQL 쿼리가 정상적으로 수행되는가?

## Related Operational Documents

- **Incident examples**: `[N/A]`
- **Postmortem examples**: `[N/A]`
