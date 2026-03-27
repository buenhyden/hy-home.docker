# Relational Databases Runbook

: PostgreSQL HA Cluster Recovery Procedures

---

## Overview (KR)

이 런북은 PostgreSQL HA 클러스터(`relational`)에서 발생할 수 있는 장애 상황에 대한 긴급 대응 및 복구 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

This runbook defines emergency response and recovery procedures for potential failure scenarios in the PostgreSQL HA cluster (`relational`). it provides step-by-step instructions and verification criteria for immediate operational action.

## Purpose

데이터베이스 노드 장애, etcd 정족수 상실, 또는 하이퍼바이저 장애 발생 시 서비스 가용성을 복구하고 데이터를 보존한다.

## Canonical References

- `[../../02.ard/0004-data-architecture.md]`
- `[../../03.adr/0004-postgresql-ha-patroni.md]`
- `[../../08.operations/04-data/relational.md]`
- `[../../04.specs/04-data/postgresql-cluster/spec.md]`

## When to Use

- PostgreSQL 리더(Leader) 노드 다운 및 페일오버 실패 시
- etcd 클러스터 가용성 상실 시
- 노드 데이터 오염 또는 저장 공간 부족 시

## Procedure or Checklist

### Checklist

- [ ] 현재 리더 노드 식별: `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list`
- [ ] etcd 엔드포인트 헬스 체크: `docker exec -it etcd-1 etcdctl endpoint health`
- [ ] 호스트 디스크 여유 공간 확인: `df -h`

### Procedure

#### 1. 노드 재시작 (Minor Failure)

1. 장애 노드 확인: `docker compose ps`
2. 컨테이너 재시작: `docker compose restart [node-name]`
3. 상태 복구 대기: `patronictl list`로 리플리케이션 상태 확인

#### 2. etcd 정족수 복구
1. 모든 etcd 노드 상태 확인: `etcdctl endpoint health --cluster`
2. 과반수 미만 가동 시 클러스터 재구성 (스냅샷/백업 활용)

#### 3. 수동 페일오버 (Switchover)
1. 리더 교체가 필요한 경우: `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml switchover`
2. 대상 노드 선택 및 실행 컨펌

## Verification Steps

- [ ] `patronictl list`에서 모든 노드가 `running` 상태이고 `Leader`가 존재하는지 확인
- [ ] `pg-router` 트래픽 라우팅 확인 (Write on 15432, Read on 15433)
- [ ] 애플리케이션 로그에서 DB 연결 오류(`Connection refused`) 해소 확인

## Safe Rollback or Recovery Procedure

- [ ] 장애 이전 시점의 백업 스냅샷 확인
- [ ] 볼륨 복구: `${DEFAULT_DATA_DIR}/pg/` 데이터 복원 및 컨테이너 재생성

## Related Operational Documents

- **Operation**: `[../../08.operations/04-data/relational.md]`
- **Guide**: `[../../07.guides/04-data/relational.md]`
- **Incident examples**: `[../../10.incidents/]`
