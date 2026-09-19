---
title: "Neo4j Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0033"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Neo4j Operations Policy

## Overview

이 정책은 root-active `OPTIONAL` Neo4j 운영 기준을 정의한다. 기준은 [Neo4j Compose 구현](../../../../../infra/04-data/specialized/neo4j/docker-compose.yml)의 단일 Community service, exact `graph` profile, `infra_net`, `neo4j_password` Docker Secret, secret-aware entrypoint와 Traefik Browser route다.

## Policy Scope

- `infra/04-data/specialized/neo4j/docker-compose.yml`
- `infra/04-data/specialized/neo4j/scripts/neo4j-entrypoint-with-secrets.sh`
- `neo4j` service and `neo4j-data` volume
- `neo4j_password` Docker Secret and `/run/secrets/neo4j_password` mount
- Traefik route `neo4j.${DEFAULT_URL}` for Neo4j Browser
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Documentation must describe Neo4j as a single Community service selected by exact `graph` profile, not as a cluster or Enterprise deployment.
- **Required**: Authentication guidance must reference the `neo4j_password` Docker Secret and secret-aware entrypoint; secret values must never be copied into docs or evidence.
- **Required**: Public access guidance must describe the declared HTTP Browser route only. Public Bolt routing requires a separate gateway change and documentation update.
- **Required**: Memory controls must match compose values: heap initial `128M`, heap max `256M`, pagecache `128M`.
- **Required**: A backup set uses Community-compatible offline `neo4j-admin database dump`, records database name, engine version, schema/index/constraint inventory, checksum, retention and restore evidence; credentials remain separate.
- **Required**: Restore rehearsal loads into a fresh isolated compatible Community target, validates database availability, constraints/indexes, counts and representative Cypher, and discards the target on failure.
- **Required**: Online backup or cluster recovery must not be claimed because those upstream capabilities are edition/topology dependent. Upgrade/removal requires restore-tested dump and capacity review.
- **Allowed**: Read-only `cypher-shell RETURN 1`, compose config rendering, service logs, and `docker compose ps` for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tag, profile, route, healthcheck, secret, and volume descriptions aligned with compose.
- **Disallowed**: Password rotation or data mutation without separate approval; in-place load over the tracked volume and invented Enterprise online-backup commands are prohibited.
- **Disallowed**: Claiming APOC/plugin mounts or public Bolt/TCP routers are active unless compose declares them.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Neo4j guide](guide.md), [Neo4j runbook](runbook.md), and [infra README](../../../../../infra/04-data/specialized/neo4j/README.md) after compose changes.
- Run `docker compose --profile graph config --quiet` before approving service-name, image, memory, route, secret, or volume documentation updates.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy or linked operations document updates.

## Review Cadence

- Review on Neo4j compose image/profile/secret/route/memory changes.
- Review during the Stage 05 operations documentation audit cadence.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0033`), [Runbook](runbook.md) (`RUN-0033`)

## Related Documents

- [Neo4j backup and restore](https://neo4j.com/docs/operations-manual/current/backup-restore/)
- [Neo4j backup planning and edition scope](https://neo4j.com/docs/operations-manual/current/backup-restore/planning/)
- [Neo4j open-source licensing](https://neo4j.com/open-source-project/)

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/specialized/neo4j/README.md)
