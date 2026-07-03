---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/relational/postgresql-cluster.md -->

# PostgreSQL Cluster Operations Policy

## Overview

이 정책은 `hy-home.docker`의 선택 relational service인 PostgreSQL HA cluster 운영 기준을 정의한다. 기준은 현재 tracked compose의 etcd 3노드 3.6.12 tag, HAProxy `haproxy:3.3.10`, Spilo/Patroni `ghcr.io/zalando/spilo-17:4.0-p3`, init job `postgres:18.4-alpine`, postgres exporters `prometheuscommunity/postgres-exporter:v0.19.1`, Docker Secret 기반 credential 구성이다.

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

- **Required**: Documentation must identify the cluster as an optional/commented root include unless root compose changes.
- **Required**: Application connection guidance must use `pg-router` write/read endpoints, not direct writes to `pg-0`, `pg-1`, or `pg-2`.
- **Required**: Credential guidance must reference Docker Secret mounts and secret-aware entrypoints; secret values must never be copied into docs or evidence.
- **Required**: HAProxy stats guidance must use the declared Traefik route `pg-haproxy.${DEFAULT_URL}` and `pg_haproxy_stats_password`.
- **Required**: Service/init guidance must describe `pg-cluster-init` as the compose job that syncs exporter role, service role, and service database through `init_users_dbs.sql`.
- **Allowed**: Read-only `patronictl list`, `pg_isready`, HAProxy config validation, compose config rendering, logs, and exporter metrics checks for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tags, service names, profiles, ports, networks, secrets, and links aligned with compose.
- **Disallowed**: DCS data deletion, forced cluster bootstrap, leadership mutation, backup restore, volume replacement, credential rotation, or database mutation steps presented as approved policy without separate owner approval and verified runbook evidence.
- **Disallowed**: Claiming WAL archiving, daily backup, or DR drills are active controls unless tracked implementation evidence is added.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [PostgreSQL cluster guide](../../../guides/04-data/relational/postgresql-cluster.md), [PostgreSQL cluster runbook](../../../runbooks/04-data/relational/postgresql-cluster.md), and [infra README](../../../../../infra/04-data/relational/postgresql-cluster/README.md) after compose changes.
- Run `docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config` before approving service-name, image, route, secret, port, or volume documentation updates.
- Run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after policy or linked operations document updates.

## Review Cadence

- Review on PostgreSQL cluster compose image/profile/secret/port/network/init/exporter changes.
- Review during the Stage 05 operations documentation audit cadence.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/relational/postgresql-cluster.md)
- [Recovery runbook](../../../runbooks/04-data/relational/postgresql-cluster.md)
- [Infra README](../../../../../infra/04-data/relational/postgresql-cluster/README.md)
