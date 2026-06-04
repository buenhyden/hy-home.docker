---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/specialized/neo4j.md -->

# Neo4j Operations Policy

## Overview (KR)

이 정책은 root-active specialized data service인 Neo4j 운영 기준을 정의한다. 기준은 현재 tracked compose의 `neo4j:5.26.26-community`, 단일 `neo4j` service, `data`/`graph` profiles, `infra_net`, `neo4j_password` Docker Secret, secret-aware entrypoint, Traefik HTTP Browser route다.

## Policy Scope

- `infra/04-data/specialized/neo4j/docker-compose.yml`
- `infra/04-data/specialized/neo4j/scripts/neo4j-entrypoint-with-secrets.sh`
- `neo4j` service and `neo4j-data` volume
- `neo4j_password` Docker Secret and `/run/secrets/neo4j_password` mount
- Traefik route `neo4j.${DEFAULT_URL}` for Neo4j Browser
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Documentation must describe Neo4j as a root-active single Community service, not as a cluster or Enterprise deployment.
- **Required**: Authentication guidance must reference the `neo4j_password` Docker Secret and secret-aware entrypoint; secret values must never be copied into docs or evidence.
- **Required**: Public access guidance must describe the declared HTTP Browser route only. Public Bolt routing requires a separate gateway change and documentation update.
- **Required**: Memory controls must match compose values: heap initial `128M`, heap max `256M`, pagecache `128M`.
- **Allowed**: Read-only `cypher-shell RETURN 1`, compose config rendering, service logs, and `docker compose ps` for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tag, profile, route, healthcheck, secret, and volume descriptions aligned with compose.
- **Disallowed**: Backup retention schedules, offline dump/restore procedures, password rotation, or data mutation steps presented as approved policy without separate owner approval and runbook evidence.
- **Disallowed**: Claiming APOC/plugin mounts or public Bolt/TCP routers are active unless compose declares them.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Neo4j guide](../../../guides/04-data/specialized/neo4j.md), [Neo4j runbook](../../../runbooks/04-data/specialized/neo4j.md), and [infra README](../../../../../infra/04-data/specialized/neo4j/README.md) after compose changes.
- Run `docker compose --profile data --profile graph config neo4j` before approving service-name, image, memory, route, secret, or volume documentation updates.
- Run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after policy or linked operations document updates.

## Review Cadence

- Review on Neo4j compose image/profile/secret/route/memory changes.
- Review during the Stage 05 operations documentation audit cadence.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/specialized/neo4j.md)
- [Recovery runbook](../../../runbooks/04-data/specialized/neo4j.md)
- [Infra README](../../../../../infra/04-data/specialized/neo4j/README.md)
