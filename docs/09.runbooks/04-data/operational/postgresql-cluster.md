# postgresql-cluster Runbook

## Overview (개요)

`postgresql-cluster` 런북은 클러스터 장애 시 신속한 복구 및 유지보수 작업을 위한 단계별 절차를 제공한다.

## Purpose

장애 상황에서의 중단 최소화 및 일관된 복구 프로세스 실행을 보장하는 데 목적이 있다.

## Prerequisites

- `docker compose` CLI 접근 권한
- `patronictl` 도구 사용법 숙지
- 관리자 권한 (sudo)

## Incident Scenarios

### 1. etcd 쿼럼 소실 (Cluster Read-Only)
- **증상**: Patroni가 리더를 선출하지 못하고 모든 노드가 Replica 모드 또는 대기 상태가 됨.
- **원인**: etcd 노드 2개 이상 장애.

### 2. PostgreSQL 마스터 노드 장애
- **증상**: 자동 페일오버 발생으로 잠시 쓰기 중단 후 복구됨.
- **원인**: 마스터 노드 컨테이너 또는 하드웨어 장애.

## Step-by-Step Procedures

### 1. 클러스터 수동 리더 변경 (Switchover)
유지보수를 위해 리더를 다른 노드로 안전하게 옮길 때 사용한다.

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml switchover
```

### 2. 초기화 작업(pg-cluster-init) 재실행
스키마 변경이나 DB 초기화가 다시 필요한 경우:

```bash
# 기존 작업 컨테이너 삭제 후 재가동
docker compose rm -f pg-cluster-init
docker compose up pg-cluster-init
```

### 3. etcd 데이타 리셋 (재구축이 필요한 경우)
모든 etcd 노드가 망가져서 클러스터를 처음부터 다시 잡아야 할 때:

1. 모든 PostgreSQL 노드 정지
2. etcd 볼륨 데이타 삭제 (`${DEFAULT_DATA_DIR}/etcd/*`)
3. etcd 서비스 가동 및 헬스 체크
4. PostgreSQL 노드 순차적 가동

## Recovery Verification

- `patronictl list` 결과에서 `Leader`가 정상 노드에 할당되었는지 확인.
- `pg-router:15432`로 쓰기 쿼리 테스트 수행.

## Post-Mortem Guidelines

- 장애 원인이 네트워크 순단인지 하드웨어 장애인지 분석.
- 자동 페일오버가 설정된 시간 내에 완료되었는지 검토.

## Canonical References
- [postgresql-cluster Infra README](../../../../infra/04-data/operational/postgresql-cluster/README.md)
- [postgresql-cluster Guide](../../../07.guides/04-data/operational/postgresql-cluster.md)
