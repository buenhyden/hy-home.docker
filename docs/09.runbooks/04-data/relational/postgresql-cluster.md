# postgresql-cluster Runbook

: PostgreSQL Cluster High-Availability Recovery

---

## Overview (KR)

이 런북은 `postgresql-cluster` 장애 시 신속한 복구 및 유지보수 작업을 위한 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공하여 서비스 중단을 최소화하는 것을 목적으로 한다.

## Purpose

- etcd 쿼럼 소실 시 클러스터 복구
- PostgreSQL 마스터 장애 시 수동 페일오버 및 상태 복구
- `pg-cluster-init`을 이용한 데이터베이스 초기화 재수행

## Canonical References

- **ARD**: `docs/02.ard/0004-data-architecture.md`
- **Spec**: `docs/04.specs/04-data/spec.md`
- **Operation**: `docs/08.operations/04-data/relational/postgresql-cluster.md`

## When to Use

- `patronictl list` 결과에서 리더가 없거나 쿼럼이 깨진 경우
- 계획된 점검을 위해 리더 노드를 변경(Switchover)해야 하는 경우
- `pg-router`를 통한 DB 접속이 불가능한 경우

## Procedure or Checklist

### Checklist

- [ ] `docker compose ps`로 etcd 및 pg 노드 컨테이너 생존 확인
- [ ] `docker compose logs`로 에러 메시지 확인
- [ ] 데이터 볼륨(`DEFAULT_DATA_DIR`)의 디스크 여유 공간 확인

### Procedure

#### 1. 클러스터 수동 리더 변경 (Switchover)
```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml switchover
```

#### 2. etcd 쿼럼 복구 (전체 장애 시)
1. 모든 PostgreSQL 노드 정지: `docker compose stop pg-0 pg-1 pg-2`
2. etcd 데이터 초기화 (필요시): `rm -rf ${DEFAULT_DATA_DIR}/etcd/*`
3. etcd 서비스 재시작: `docker compose up -d etcd-1 etcd-2 etcd-3`
4. PostgreSQL 노드 순차 가동: `docker compose up -d pg-0` (이후 순차)

#### 3. 초기화 작업(pg-cluster-init) 재실행
```bash
docker compose rm -f pg-cluster-init
docker compose up pg-cluster-init
```

## Verification Steps

- [ ] `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list` 실행 후 `Leader` 존재 확인
- [ ] `pg_isready -h localhost -p 15432 -U postgres` 명령으로 쓰기 포트 가용성 확인

## Observability and Evidence Sources

- **Signals**: Grafana PostgreSQL Dashboard, `pg-router` HAProxy Stats
- **Evidence to Capture**: `patronictl list` 출력 결과, `docker compose logs`

## Related Operational Documents

- **Incident examples**: `docs/10.incidents/`
- **Postmortem examples**: `docs/11.postmortems/`

