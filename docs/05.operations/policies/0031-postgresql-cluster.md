---
title: "PostgreSQL Cluster Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0031"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# PostgreSQL Cluster Operations Policy

## Overview

이 정책은 `hy-home.docker`의 선택 relational service인 PostgreSQL HA cluster 운영 기준을 정의한다. 기준은 현재 tracked compose의 etcd 3노드 [quay.io/coreos/etcd image declaration](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml) tag, HAProxy [haproxy image declaration](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml), Spilo/Patroni [ghcr.io/zalando/spilo-17 image declaration](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml), init job [postgres image declaration](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml), postgres exporters [prometheuscommunity/postgres-exporter image declaration](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml), Docker Secret 기반 credential 구성이다.

## Policy Scope

- `infra/04-data/relational/postgresql-cluster/docker-compose.yml`
- `etcd-1`, `etcd-2`, `etcd-3`
- `pg-router`, `pg-cluster-init`
- `pg-0`, `pg-1`, `pg-2`
- `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`
- `haproxy.cfg.tpl`, `init_users_dbs.sql`, `spilo-entrypoint-with-secrets.sh`
- `pg_haproxy_stats_password`, `patroni_superuser_password`, `patroni_replication_password`, `patroni_exporter_password`, `service_postgres_password`
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: 문서는 cluster를 정확한 `postgres-ha` profile 아래에서만
  서비스가 해석되는 unconditional root include로 식별해야 하며, `core`
  surface의 일부로 기술해서는 안 된다.
- **Required**: Application 연결 가이드는 `pg-0`, `pg-1`, `pg-2`에 직접 쓰지
  않고 `pg-router`의 write/read endpoint를 사용해야 한다.
- **Required**: Credential 가이드는 Docker Secret mount와 secret-aware
  entrypoint를 참조해야 한다. Secret 값은 문서나 evidence에 절대 복사해서는
  안 된다.
- **Required**: HAProxy stats 가이드는 선언된 Traefik route
  `pg-haproxy.${DEFAULT_URL}`와 `pg_haproxy_stats_password`를 사용해야 한다.
- **Required**: 서비스/init 가이드는 `pg-cluster-init`을 `init_users_dbs.sql`을
  통해 exporter role, service role, service database를 동기화하는 compose
  job으로 기술해야 한다.
- **Required**: Logical backup은 cluster globals/role/privilege와 범위에 속한
  모든 database schema/data dump, extension/ownership evidence, version,
  checksum, retention, 검증된 restore 기록을 포함한다. Password는 별도로
  보호하는 secret으로 유지한다.
- **Required**: Restore rehearsal은 빈 isolated compatible cluster를 사용하며,
  database 이전에 globals를 복원하고, owner/ACL/extension/sequence/data를
  검증하며, test를 `pg-router`를 통해 라우팅한다. Patroni/etcd state는
  logical data로 복원하지 않고 재구축한다.
- **Required**: Upgrade나 removal 전에 용량, WAL/dump 공간, 호환성, rollback
  evidence를 검토한다. Physical restore를 즉석에서 만들지 말고 연결된
  `RUN-0032` rehearsal을 사용한다.
- **Allowed**: Evidence 수집을 위한 read-only `patronictl list`,
  `pg_isready`, HAProxy config 검증, compose config 렌더링, 로그, exporter
  metrics 확인.
- **Allowed**: Image tag, 서비스 이름, profile, port, network, secret, 링크를
  compose와 일치시키는 문서 전용 수정.
- **Disallowed**: 별도의 owner 승인과 검증된 runbook evidence 없이 승인된
  policy로 제시되는 DCS data 삭제, 강제 cluster bootstrap, leadership
  mutation, backup restore, volume 교체, credential rotation, database
  mutation 단계.
- **Disallowed**: 추적된 구현 evidence가 추가되지 않는 한 WAL archiving, 일일
  backup, DR drill이 활성 통제라고 주장하는 것.

## Exceptions

N/A - 현재 승인된 예외 없음.

## Verification

- Compose 변경 후 이 정책을
  [PostgreSQL cluster guide](../guides/0031-postgresql-cluster.md),
  [PostgreSQL cluster runbook](../runbooks/0031-postgresql-cluster.md),
  [infra README](../../../infra/04-data/relational/postgresql-cluster/README.md)와
  비교한다.
- 서비스 이름, image, route, secret, port, volume 문서 갱신을 승인하기 전에
  `docker compose --profile postgres-ha config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

## Review Cadence

- PostgreSQL cluster compose image/profile/secret/port/network/init/exporter
  변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0031-postgresql-cluster.md) (`GDE-0031`), [Runbook](../runbooks/0031-postgresql-cluster.md) (`RUN-0031`)

## Related Documents

- [PostgreSQL pg_dumpall reference](https://www.postgresql.org/docs/18/app-pg-dumpall.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Logical upgrade restore rehearsal](../runbooks/0032-postgresql-logical-upgrade-restore-rehearsal.md) (`RUN-0032`)

- [Operations index](../README.md)
- [Usage guide](../guides/0031-postgresql-cluster.md)
- [Recovery runbook](../runbooks/0031-postgresql-cluster.md)
- [Infra README](../../../infra/04-data/relational/postgresql-cluster/README.md)
