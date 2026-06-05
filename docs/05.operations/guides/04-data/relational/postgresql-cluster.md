---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/relational/postgresql-cluster.md -->

# PostgreSQL Cluster Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/relational/postgresql-cluster/docker-compose.yml`에 정의된 PostgreSQL HA cluster 사용 기준을 설명한다. 현재 루트 compose에서는 `postgresql-cluster` include가 주석 처리된 선택 서비스이며, 활성화 시 etcd 3노드, Spilo/Patroni PostgreSQL 3노드, `pg-router`, `pg-cluster-init`, per-node postgres exporter가 `data`/`service` 프로파일에서 동작한다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

관계형 데이터베이스 연결과 일반 점검을 현재 compose의 service name, host port, secret mount, init job, exporter 경계와 맞춰 수행하도록 한다.

### Prerequisites

- `infra/04-data/relational/postgresql-cluster/docker-compose.yml`와 루트 [docker-compose.yml](../../../../../docker-compose.yml)의 선택 include 상태를 확인한다.
- `DEFAULT_DATA_DIR`, `POSTGRES_DEFAULT_DB`, Patroni usernames, service DB/user variables, PostgreSQL/HAProxy secret files가 준비되어 있어야 한다.
- secret 값은 `/run/secrets/*`에서 container 내부로만 읽고 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

1. 선택 클러스터 구성을 렌더링한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config
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

- 현재 구현은 root-active가 아니라 optional/commented include다. root compose 기본 `core` validation에 이 클러스터가 포함된 것처럼 설명하지 않는다.
- 직접 PostgreSQL node에 application traffic을 붙이면 failover 라우팅이 보장되지 않는다. 일반 연결 문서는 `pg-router`를 기준으로 한다.
- Patroni/Spilo node secrets는 `spilo-entrypoint-with-secrets.sh`가 `/run/secrets/patroni_*`에서 읽는다. plain password variables를 전제로 한 예시는 사용하지 않는다.
- DCS destructive recovery, leadership mutation 같은 운영 변경은 guide가 아니라 승인된 runbook/escalation 영역이다.

## Common Checks

- `docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config`
- `docker compose ps etcd-1 etcd-2 etcd-3 pg-router pg-0 pg-1 pg-2`
- `docker exec pg-0 patronictl -c /home/postgres/postgres.yml list`
- `docker compose logs --tail=120 pg-router pg-cluster-init`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [PostgreSQL cluster runbook](../../../runbooks/04-data/relational/postgresql-cluster.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/relational/postgresql-cluster.md)
- [Recovery runbook](../../../runbooks/04-data/relational/postgresql-cluster.md)
- [Infra README](../../../../../infra/04-data/relational/postgresql-cluster/README.md)
