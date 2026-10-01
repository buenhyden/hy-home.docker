---
title: "PostgreSQL Cluster Usage Guide"
version: "1.0.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0031"
parent_ids:
- "POL-0031"
implementation_services:
  infra/04-data/postgresql-cluster/docker-compose.yml:
  - 'etcd-1'
  - 'etcd-2'
  - 'etcd-3'
  - 'pg-0'
  - 'pg-0-exporter'
  - 'pg-1'
  - 'pg-1-exporter'
  - 'pg-2'
  - 'pg-2-exporter'
  - 'pg-cluster-init'
  - 'pg-router'
created: "2026-05-10"
---

# PostgreSQL Cluster Usage Guide

## Usage

### Overview

이 문서는 [PostgreSQL cluster Compose 구현](../../../infra/04-data/postgresql-cluster/docker-compose.yml)의 etcd/Patroni/HAProxy stack을 설명한다. 열한 서비스는 모두 exact `postgres-ha` profile에서 동작한다. frozen classification은 `LAB`이고 모든 members가 한 Docker host에 있으므로 host-level HA나 off-host disaster recovery를 제공하지 않는다.

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Consumer와 data 근거 | PostgreSQL leadership/routing과 logical upgrade 복구를 위한 LAB rehearsal용이며 확인된 HOME database가 아니다. |
| Source·update 책임 | [Compose](../../../infra/04-data/postgresql-cluster/docker-compose.yml), entrypoint, HAProxy template과 init SQL이 runtime source를 소유한다. 관련 변경을 함께 검토하여 upgrade한다. |
| 서비스·profile | etcd 3개, router, init, PostgreSQL 3개, exporter 3개; 정확한 profile은 `postgres-ha`. |
| 흐름·의존성 | etcd가 Patroni DCS state를 보관한다. HAProxy는 primary 쓰기/replica 읽기를 라우팅하며 init은 service/exporter role과 database를 생성한다. |
| 노출·영속성 | write/read port와 stats route는 source에 선언되어 있다. etcd/PGDATA에는 별도의 bind 기반 volume을 둔다. |
| 환경 설정·secret | Patroni/service 식별자는 환경 key이다. HAProxy, superuser, replication, exporter와 service password는 Docker Secret이다. |
| Health·자원 | etcd health, `patronictl list`, HAProxy 점검, exporter를 사용한다. service는 Compose에 선언된 template을 사용하며 LAB 전체에 필요한 용량을 확보해야 한다. |
| 보안 | secret을 처리하는 Spilo entrypoint와 라우팅된 client 연결을 사용한다. 같은 host의 member는 다른 host를 통한 DR이 아니다. |
| Backup·upgrade | globals와 database별 logical dump를 보존한다. upgrade/제거 전에 새 DCS/cluster에 복구하고 `RUN-0032`를 사용한다(synthetic single-DB rehearsal만 해당하며 HA globals/ACL/router 복원은 미구현). |
| License·edition | PostgreSQL에는 PostgreSQL License가 적용된다. Spilo, Patroni, etcd, HAProxy와 exporter는 각각 별도 license가 적용되는 의존성이다. |


### Identity-specific behavior

etcd3.7.1 의 3member 는 각 ID/URL/data, Spilo17:4.0-p3 의 3member 는 각 identity/data 가 다르다. helper postgres18.6 은 server major 를 뜻하지 않는다. router3.4.4 는 write/read backend 와 stats 를 제공하며 config syntax health 는 실제 routing 을 증명하지 않는다. init 는 roles/grants/database mutation, exporter0/1/2 는 서로 다른 PG target 이다. 실제 HA globals/모든 DB/ACL/extension/router restore 는 미구현이며 RUN0032 의 synthetic17→18 와 분리한다. 한 host 의 quorum 은 host disaster recovery 가 아니다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `etcd-1` | DCS member 1; 고유 URL/identity/data | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `etcd-2` | DCS member 2; 고유 URL/identity/data | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `etcd-3` | DCS member 3; 고유 URL/identity/data | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-0` | Spilo/Patroni member 0; 고유 identity/data, secret wrapper | PG 연결 수락; SQL 권한/업무 정합성 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-0-exporter` | 해당 PG member만 수집하는 exporter | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-1` | Spilo/Patroni member 1; 고유 identity/data, secret wrapper | PG 연결 수락; SQL 권한/업무 정합성 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-1-exporter` | 해당 PG member만 수집하는 exporter | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-2` | Spilo/Patroni member 2; 고유 identity/data, secret wrapper | PG 연결 수락; SQL 권한/업무 정합성 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-2-exporter` | 해당 PG member만 수집하는 exporter | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-cluster-init` | role/database mutation job; HA restore 아님 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |
| `pg-router` | write/read router + stats; backend readiness 별도 | HAProxy config syntax; write/read routing 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/postgresql-cluster/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.


### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

관계형 데이터베이스 연결과 일반 점검을 현재 compose의 service name, host port, secret mount, init job, exporter 경계와 맞춰 수행하도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../docker-compose.yml)는 cluster 파일을 include하며, 열한 서비스의 exact profile은 `postgres-ha`다.
- `DEFAULT_DATA_DIR`, `POSTGRES_DEFAULT_DB`, Patroni usernames, service DB/user variables, PostgreSQL/HAProxy secret files가 준비되어 있어야 한다.
- secret 값은 `/run/secrets/*`에서 container 내부로만 읽고 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

정상 운영 중 점검은 선택 클러스터 compose 렌더링, 핵심 서비스 상태, `patronictl list` 기준 Patroni cluster 상태 확인으로 구성된다. 실행 가능한 명령 순서와 기대 결과는 [PostgreSQL Cluster runbook](../runbooks/0031-postgresql-cluster.md#steps)을 따른다.

1. 애플리케이션 연결은 `pg-router`를 기준으로 한다.

   | Endpoint | Host | Port | Purpose |
   | --- | --- | --- | --- |
   | Write | `pg-router` (`${HOST_LAN_BIND_IP:-192.168.0.13}`) | `${POSTGRES_WRITE_PORT:-15432}` | Patroni primary backend |
   | Read | `pg-router` (`${HOST_LAN_BIND_IP:-192.168.0.13}`) | `${POSTGRES_READ_PORT:-15433}` | Patroni replica backends |
   | Stats | `pg-haproxy.${DEFAULT_URL}` | `${HAPROXY_PORT:-7000}` via Traefik | HAProxy stats route |

2. `pg-cluster-init`는 `pg-router` write endpoint가 준비된 뒤 `init_users_dbs.sql`로 exporter role, service role, service database를 동기화한다.

3. Exporter는 `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`가 각 node와 `patroni_exporter_password` secret을 기준으로 `${POSTGRES_EXPORTER_PORT:-9187}`에 metrics를 expose한다.

### Common Pitfalls

- 루트 compose는 이 클러스터 파일을 무조건 include하지만 어떤 서비스도 `core` profile에 속하지 않는다. 기본 `core` validation에 이 클러스터가 포함된 것처럼 설명하지 않는다.
- 직접 PostgreSQL node에 application traffic을 붙이면 failover 라우팅이 보장되지 않는다. 일반 연결 문서는 `pg-router`를 기준으로 한다.
- Patroni/Spilo node secrets는 `spilo-entrypoint-with-secrets.sh`가 `/run/secrets/patroni_*`에서 읽는다. plain password variables를 전제로 한 예시는 사용하지 않는다.
- DCS destructive recovery, leadership mutation 같은 운영 변경은 guide가 아니라 승인된 runbook/escalation 영역이다.
- logical recovery set에는 `pg_dumpall --globals-only` 역할/권한과 각 database의 schema/data dump가 모두 필요하다. Patroni/etcd state를 logical data backup처럼 복사하지 않는다.


## Common Checks

- `docker compose --profile postgres-ha config --quiet`
- `docker compose ps etcd-1 etcd-2 etcd-3 pg-router pg-0 pg-1 pg-2`
- `docker exec pg-0 patronictl -c /home/postgres/postgres.yml list`
- `docker compose logs --tail=120 pg-router pg-cluster-init`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [PostgreSQL cluster runbook](../runbooks/0031-postgresql-cluster.md)을 따른다.

## Traceability

- Declared parent: [PostgreSQL Cluster Operations Policy](../policies/0031-postgresql-cluster.md) (`POL-0031`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0031-postgresql-cluster.md) (`POL-0031`), [Runbook](../runbooks/0031-postgresql-cluster.md) (`RUN-0031`)

## Related Documents

- [PostgreSQL pg_dumpall reference](https://www.postgresql.org/docs/18/app-pg-dumpall.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Logical upgrade restore rehearsal](../runbooks/0032-postgresql-logical-upgrade-restore-rehearsal.md) (`RUN-0032`(synthetic single-DB rehearsal만 해당; HA globals/ACL/router 복원은 미구현))

- [Operations index](../README.md)
- [Operations policy](../policies/0031-postgresql-cluster.md)
- [Recovery runbook](../runbooks/0031-postgresql-cluster.md)
- [Infra README](../../../infra/04-data/postgresql-cluster/README.md)
- [Compose implementation: infra/04-data/postgresql-cluster/docker-compose.yml](../../../infra/04-data/postgresql-cluster/docker-compose.yml)
