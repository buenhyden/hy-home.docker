---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/nosql/couchdb.md -->

# CouchDB Operations Policy

## Overview (KR)

이 정책은 `hy-home.docker`의 선택 NoSQL 서비스인 CouchDB 3노드 클러스터 운영 기준을 정의한다. 기준은 현재 tracked compose의 `couchdb:3.5.2`, `curlimages/curl:8.20.0`, `couchdb-cluster-init`, Traefik sticky route, Docker Secret 기반 admin password와 Erlang cookie 구성이다.

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
- **Allowed**: Read-only `_up`, `_membership`, `_scheduler/docs`, and logs checks for evidence capture.
- **Allowed**: Documentation-only corrections that preserve the 3-node cluster-init model and sticky routing.
- **Disallowed**: Manual node rejoin, compaction, or cluster surgery guidance without current evidence and runbook escalation.
- **Disallowed**: Secret values, credential dumps, or Erlang cookie material in policy text or evidence.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [CouchDB guide](../../../guides/04-data/nosql/couchdb.md), [CouchDB runbook](../../../runbooks/04-data/nosql/couchdb.md), and [infra README](../../../../../infra/04-data/nosql/couchdb/README.md) after compose changes.
- Run `docker compose -f docker-compose.yml -f infra/04-data/nosql/couchdb/docker-compose.yml --profile data config` before approving service-name, port, Traefik, secret, or cluster-init documentation updates.
- Run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after policy or linked operations document updates.

## Review Cadence

- Review on CouchDB compose image/profile/secret/Traefik/cluster-init changes.
- Review during the Stage 05 operations documentation audit cadence.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/nosql/couchdb.md)
- [Recovery runbook](../../../runbooks/04-data/nosql/couchdb.md)
- [Infra README](../../../../../infra/04-data/nosql/couchdb/README.md)
