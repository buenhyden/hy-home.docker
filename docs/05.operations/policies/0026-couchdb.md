---
title: "CouchDB Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0026"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# CouchDB Operations Policy

## Overview

이 정책은 `hy-home.docker`의 선택 NoSQL 서비스인 CouchDB 3노드 클러스터 운영 기준을 정의한다. 기준은 현재 tracked compose의 [couchdb image declaration](../../../infra/04-data/nosql/couchdb/docker-compose.yml), [curlimages/curl image declaration](../../../infra/04-data/nosql/couchdb/docker-compose.yml), `couchdb-cluster-init`, Traefik sticky route, Docker Secret 기반 admin password와 Erlang cookie 구성이다.

## Policy Scope

- `infra/04-data/nosql/couchdb/docker-compose.yml`
- `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`
- `couchdb1-data`, `couchdb2-data`, `couchdb3-data`
- `couchdb_password`, `couchdb_cookie`, `COUCHDB_USERNAME`
- Traefik route `couchdb.${DEFAULT_URL}` and `couchdb_sticky` load-balancer cookie
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Documentation must use current service names `couchdb-1`, `couchdb-2`, `couchdb-3`, and `couchdb-cluster-init`.
- **Required**: Cluster cookie guidance must reference `/run/secrets/couchdb_cookie`; legacy shared-secret environment variables are not the current compose control.
- **Required**: Health and membership checks must use the CouchDB HTTP API and container-local secret reads, not copied password values.
- **Required**: External access guidance must stay behind Traefik `websecure` routing; direct host port exposure is not declared in compose.
- **Required**: All services use the exact `couchdb` profile, and the three same-host nodes must not be represented as host-level HA.
- **Required**: A recoverable set includes database/shard files or replication targets, system databases, `_dbs` metadata, security objects, configuration, cluster membership, Erlang cookie custody, checksums, retention, and a tested restore record.
- **Required**: Restore rehearsal uses a fresh isolated cluster with compatible version/topology. Database replication is preferred; file restore follows upstream ordering with indexes before database files and never copies live files.
- **Required**: Capacity and compaction headroom are reviewed before retention changes; upgrades follow upstream sequencing and require a restore-tested backup.
- **Required**: Removal requires confirmed consumer shutdown, retained replication/file backup evidence with expiry/owner, and separate approval before node or volume deletion.
- **Allowed**: Read-only `_up`, `_membership`, `_scheduler/docs`, and logs checks for evidence capture.
- **Allowed**: Documentation-only corrections that preserve the 3-node cluster-init model and sticky routing.
- **Disallowed**: Manual node rejoin, compaction, or cluster surgery guidance without current evidence and runbook escalation.
- **Disallowed**: Secret values, credential dumps, or Erlang cookie material in policy text or evidence.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [CouchDB guide](../guides/0026-couchdb.md), [CouchDB runbook](../runbooks/0026-couchdb.md), and [infra README](../../../infra/04-data/nosql/couchdb/README.md) after compose changes.
- Run `docker compose --profile couchdb config --quiet` before approving service-name, port, Traefik, secret, or cluster-init documentation updates.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy or linked operations document updates.

## Review Cadence

- Review on CouchDB compose image/profile/secret/Traefik/cluster-init changes.
- Review during the Stage 05 operations documentation audit cadence.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0026-couchdb.md) (`GDE-0026`), [Runbook](../runbooks/0026-couchdb.md) (`RUN-0026`)

## Related Documents

- [CouchDB backup guidance](https://docs.couchdb.org/en/stable/maintenance/backups.html)
- [CouchDB upgrade guidance](https://docs.couchdb.org/en/stable/install/upgrading.html)
- [CouchDB database security](https://docs.couchdb.org/en/stable/api/database/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0026-couchdb.md)
- [Recovery runbook](../runbooks/0026-couchdb.md)
- [Infra README](../../../infra/04-data/nosql/couchdb/README.md)
