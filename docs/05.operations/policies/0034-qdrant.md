---
title: "Qdrant Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "operations"
artifact_id: "POL-0034"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Qdrant Operations Policy

## Overview

이 정책은 root-active `HOME` Qdrant 운영 기준을 정의한다. 기준은 [Qdrant Compose 구현](../../../infra/04-data/specialized/qdrant/docker-compose.yml)의 단일 service, exact `ai`/`ai-llm`/`qdrant` profiles, `ai_net`, API key secret, SSO 뒤의 REST route와 `/readyz` healthcheck다.

## Policy Scope

- `infra/04-data/specialized/qdrant/docker-compose.yml`
- `qdrant` service and `qdrant-data` volume
- REST route `qdrant.${DEFAULT_URL}` behind SSO (`sso-auth@file`) and the API key; no gRPC route
- API key from `qdrant_api_key` (AI-008); only the health endpoints answer without it
- Read-only API key from `qdrant_read_only_api_key` (AI-009), the only key Prometheus holds; it must differ from the full key
- `QDRANT__STORAGE__SNAPSHOTS_PATH=/qdrant/storage/snapshots`
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Documentation must describe Qdrant as a single unprivileged service, not as a cluster.
- **Required**: Every Qdrant client reads the key from a secret file; the key never appears in Compose environment values, logs or evidence.
- **Required**: External access guidance must stay behind the declared SSO REST route and must not imply host port publishing or a gRPC route.
- **Required**: Persistence and snapshot-path wording must match `qdrant-data:/qdrant/storage:rw` and `/qdrant/storage/snapshots`.
- **Required**: Backup inventory records collection or full-storage snapshot identifier, engine minor version, aliases, vector counts/config, checksum, retention and restore evidence. Snapshot files stay protected on disk; the API key guards only API access to them.
- **Required**: Restore rehearsal uses a fresh isolated target with same minor or next minor compatibility, absent target collection unless an explicitly reviewed force action applies, and approximately twice the snapshot size in free disk.
- **Required**: Verify aliases, collection config/status, point counts and representative searches before promotion. Upgrade/removal requires a restore-tested snapshot and capacity review.
- **Allowed**: Read-only `/readyz`, `/collections` (with the key from the secret file), compose config rendering, service logs, and `docker compose ps` for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tag, profile, route, healthcheck, and volume descriptions aligned with compose.
- **Disallowed**: Collection delete, snapshot restore, volume replacement, cluster repair, or data mutation steps presented as approved policy without separate owner approval and verified runbook evidence.
- **Disallowed**: Removing the API key or adding a client that calls Qdrant without it.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Qdrant guide](../guides/0034-qdrant.md), [Qdrant runbook](../runbooks/0034-qdrant.md), and [infra README](../../../infra/04-data/specialized/qdrant/README.md) after compose changes.
- Run `docker compose --profile qdrant config --quiet` before approving service-name, image, route, secret, healthcheck, or volume documentation updates.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy or linked operations document updates.

## Review Cadence

- Review on Qdrant compose image/profile/secret/route/snapshot-path changes.
- Review during the Stage 05 operations documentation audit cadence.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0034-qdrant.md) (`GDE-0034`), [Runbook](../runbooks/0034-qdrant.md) (`RUN-0034`)

## Related Documents

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)

- [Operations index](../README.md)
- [Usage guide](../guides/0034-qdrant.md)
- [Recovery runbook](../runbooks/0034-qdrant.md)
- [Infra README](../../../infra/04-data/specialized/qdrant/README.md)
