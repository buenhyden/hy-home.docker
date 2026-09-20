---
title: "PostgreSQL Cluster Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0031"
parent_ids:
- "POL-0031"
implementation_services:
  infra/04-data/relational/postgresql-cluster/docker-compose.yml:
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

이 문서는 [PostgreSQL cluster Compose 구현](../../../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml)의 etcd/Patroni/HAProxy stack을 설명한다. 열한 서비스는 모두 exact `postgres-ha` profile에서 동작한다. frozen classification은 `LAB`이고 모든 members가 한 Docker host에 있으므로 host-level HA나 off-host disaster recovery를 제공하지 않는다.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | LAB rehearsal of PostgreSQL leadership/routing and logical upgrade recovery; not a confirmed HOME database. |
| Source / updater | [Compose](../../../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml), entrypoint, HAProxy template and init SQL own runtime sources; coordinated review owns upgrades. |
| Services / profile | 3 etcd, router, init, 3 PostgreSQL, 3 exporters; exact `postgres-ha`. |
| Flow / dependency | etcd holds Patroni DCS state; HAProxy routes primary writes/replica reads; init creates service/exporter roles and database. |
| Exposure / persistence | write/read ports and stats route are source-declared; separate bind-backed etcd/PGDATA volumes. |
| Environment / secrets | Patroni/service identifiers are environment keys; HAProxy, superuser, replication, exporter and service passwords are Docker Secrets. |
| Health / resources | etcd health, `patronictl list`, HAProxy checks, exporters; services use Compose-declared templates and require aggregate LAB capacity. |
| Security | secret-aware Spilo entrypoint and routed client connections; same-host members are not off-host DR. |
| Backup / upgrade | globals plus per-database logical dumps; restore into a fresh DCS/cluster and use `RUN-0032` before upgrade/removal. |
| License / edition | PostgreSQL uses the PostgreSQL License; Spilo, Patroni, etcd, HAProxy and exporter remain separately licensed dependencies. |

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

관계형 데이터베이스 연결과 일반 점검을 현재 compose의 service name, host port, secret mount, init job, exporter 경계와 맞춰 수행하도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../../../docker-compose.yml)는 cluster 파일을 include하며, 열한 서비스의 exact profile은 `postgres-ha`다.
- `DEFAULT_DATA_DIR`, `POSTGRES_DEFAULT_DB`, Patroni usernames, service DB/user variables, PostgreSQL/HAProxy secret files가 준비되어 있어야 한다.
- secret 값은 `/run/secrets/*`에서 container 내부로만 읽고 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

1. 선택 클러스터 구성을 렌더링한다.

   ```bash
   docker compose --profile postgres-ha config --quiet
   ```

2. 핵심 서비스 상태를 확인한다.

   ```bash
   docker compose ps etcd-1 etcd-2 etcd-3 pg-router pg-cluster-init pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

3. Patroni cluster 상태는 한 PostgreSQL node 내부에서 확인한다.

   ```bash
   docker exec pg-0 patronictl -c /home/postgres/postgres.yml list
   ```

4. 애플리케이션 연결은 `pg-router`를 기준으로 한다.

   | Endpoint | Host | Port | Purpose |
   | --- | --- | --- | --- |
   | Write | `pg-router` | `${POSTGRES_WRITE_PORT:-15432}` | Patroni primary backend |
   | Read | `pg-router` | `${POSTGRES_READ_PORT:-15433}` | Patroni replica backends |
   | Stats | `pg-haproxy.${DEFAULT_URL}` | `${HAPROXY_PORT:-7000}` via Traefik | HAProxy stats route |

5. `pg-cluster-init`는 `pg-router` write endpoint가 준비된 뒤 `init_users_dbs.sql`로 exporter role, service role, service database를 동기화한다.

6. Exporter는 `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`가 각 node와 `patroni_exporter_password` secret을 기준으로 `${POSTGRES_EXPORTER_PORT:-9187}`에 metrics를 expose한다.

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

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [PostgreSQL cluster runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [PostgreSQL Cluster Operations Policy](policy.md) (`POL-0031`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](policy.md) (`POL-0031`), [Runbook](runbook.md) (`RUN-0031`)

## Related Documents

- [PostgreSQL pg_dumpall reference](https://www.postgresql.org/docs/18/app-pg-dumpall.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Logical upgrade restore rehearsal](../0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) (`RUN-0032`)

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/relational/postgresql-cluster/README.md)
- [Compose implementation: infra/04-data/relational/postgresql-cluster/docker-compose.yml](../../../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml)
