---
title: "Qdrant Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0034"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Qdrant Operations Policy

## Overview

이 정책은 root-active `HOME` Qdrant 운영 기준을 정의한다. 기준은 [Qdrant Compose 구현](../../../../../infra/04-data/specialized/qdrant/docker-compose.yml)의 단일 service, exact `ai`/`ai-llm`/`qdrant` profiles, `infra_net`, no-secret state, REST/gRPC routes와 `/readyz` healthcheck다.

## Policy Scope

- `infra/04-data/specialized/qdrant/docker-compose.yml`
- `qdrant` service and `qdrant-data` volume
- REST route `qdrant.${DEFAULT_URL}` and gRPC route `qdrant-grpc.${DEFAULT_URL}`
- `QDRANT__STORAGE__SNAPSHOTS_PATH=/qdrant/storage/snapshots`
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Documentation must describe Qdrant as a single unprivileged service, not as a cluster.
- **Required**: Secret guidance must state the current no-secret compose state. API-key requirements require a compose change before being documented as active policy.
- **Required**: External access guidance must stay behind declared Traefik REST/TCP routes and must not imply host port publishing.
- **Required**: Persistence and snapshot-path wording must match `qdrant-data:/qdrant/storage:rw` and `/qdrant/storage/snapshots`.
- **Required**: Backup inventory records collection or full-storage snapshot identifier, engine minor version, aliases, vector counts/config, checksum, retention and restore evidence. Snapshot files remain protected even though current Compose lacks API authentication.
- **Required**: Restore rehearsal uses a fresh isolated target with same minor or next minor compatibility, absent target collection unless an explicitly reviewed force action applies, and approximately twice the snapshot size in free disk.
- **Required**: Verify aliases, collection config/status, point counts and representative searches before promotion. Upgrade/removal requires a restore-tested snapshot and capacity review.
- **Allowed**: Read-only `/readyz`, `/collections`, compose config rendering, service logs, and `docker compose ps` for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tag, profile, route, healthcheck, and volume descriptions aligned with compose.
- **Disallowed**: Collection delete, snapshot restore, volume replacement, cluster repair, or data mutation steps presented as approved policy without separate owner approval and verified runbook evidence.
- **Disallowed**: Claiming a Qdrant API-key secret is active unless compose declares it.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Qdrant guide](guide.md), [Qdrant runbook](runbook.md), and [infra README](../../../../../infra/04-data/specialized/qdrant/README.md) after compose changes.
- Run `docker compose --profile qdrant config --quiet` before approving service-name, image, route, secret, healthcheck, or volume documentation updates.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy or linked operations document updates.

## Review Cadence

- Review on Qdrant compose image/profile/secret/route/snapshot-path changes.
- Review during the Stage 05 operations documentation audit cadence.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0034`), [Runbook](runbook.md) (`RUN-0034`)

## Related Documents

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/specialized/qdrant/README.md)
