---
title: "PostgreSQL Cluster Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
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

- **Required**: Documentation must identify the cluster as an unconditional root include whose services resolve only under the exact `postgres-ha` profile, and must not describe it as part of the `core` surface.
- **Required**: Application connection guidance must use `pg-router` write/read endpoints, not direct writes to `pg-0`, `pg-1`, or `pg-2`.
- **Required**: Credential guidance must reference Docker Secret mounts and secret-aware entrypoints; secret values must never be copied into docs or evidence.
- **Required**: HAProxy stats guidance must use the declared Traefik route `pg-haproxy.${DEFAULT_URL}` and `pg_haproxy_stats_password`.
- **Required**: Service/init guidance must describe `pg-cluster-init` as the compose job that syncs exporter role, service role, and service database through `init_users_dbs.sql`.
- **Required**: Logical backup includes cluster globals/roles/privileges plus every in-scope database schema/data dump, extensions/ownership evidence, versions, checksums, retention and a tested restore record. Passwords remain separate protected secrets.
- **Required**: Restore rehearsal uses an empty isolated compatible cluster, restores globals before databases, verifies owners/ACLs/extensions/sequences/data and routes tests through `pg-router`; Patroni/etcd state is rebuilt, not restored as logical data.
- **Required**: Capacity, WAL/dump space, compatibility and rollback evidence are reviewed before upgrade or removal. Use the linked `RUN-0032` rehearsal rather than inventing a physical restore.
- **Allowed**: Read-only `patronictl list`, `pg_isready`, HAProxy config validation, compose config rendering, logs, and exporter metrics checks for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tags, service names, profiles, ports, networks, secrets, and links aligned with compose.
- **Disallowed**: DCS data deletion, forced cluster bootstrap, leadership mutation, backup restore, volume replacement, credential rotation, or database mutation steps presented as approved policy without separate owner approval and verified runbook evidence.
- **Disallowed**: Claiming WAL archiving, daily backup, or DR drills are active controls unless tracked implementation evidence is added.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [PostgreSQL cluster guide](../guides/0031-postgresql-cluster.md), [PostgreSQL cluster runbook](../runbooks/0031-postgresql-cluster.md), and [infra README](../../../infra/04-data/relational/postgresql-cluster/README.md) after compose changes.
- Run `docker compose --profile postgres-ha config --quiet` before approving service-name, image, route, secret, port, or volume documentation updates.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy or linked operations document updates.

## Review Cadence

- Review on PostgreSQL cluster compose image/profile/secret/port/network/init/exporter changes.
- Review during the Stage 05 operations documentation audit cadence.

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
