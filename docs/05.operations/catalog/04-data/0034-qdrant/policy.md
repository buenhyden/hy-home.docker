---
title: Qdrant Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0034
parent_ids:
  - AD-0004
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/04-data/0034-qdrant/policy.md -->

# Qdrant Operations Policy

## Overview

이 정책은 root-active specialized data service인 Qdrant 운영 기준을 정의한다. 기준은 현재 tracked compose의 `qdrant/qdrant:v1.18.1-unprivileged`, 단일 `qdrant` service, `ai`/`data`/`dev` profiles, `infra_net`, no-secret state, REST Traefik route, gRPC TCP route, `/readyz` healthcheck다.

## Policy Scope

- `infra/04-data/specialized/qdrant/docker-compose.yml`
- `qdrant` service and `qdrant-data` volume
- REST route `qdrant.${DEFAULT_URL}` and gRPC route `qdrant-grpc.${DEFAULT_URL}`
- `QDRANT__STORAGE__SNAPSHOTS_PATH=/qdrant/storage/snapshots`
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Documentation must describe Qdrant as a root-active single unprivileged service, not as a cluster.
- **Required**: Secret guidance must state the current no-secret compose state. API-key requirements require a compose change before being documented as active policy.
- **Required**: External access guidance must stay behind declared Traefik REST/TCP routes and must not imply host port publishing.
- **Required**: Persistence and snapshot-path wording must match `qdrant-data:/qdrant/storage:rw` and `/qdrant/storage/snapshots`.
- **Allowed**: Read-only `/readyz`, `/collections`, compose config rendering, service logs, and `docker compose ps` for evidence capture.
- **Allowed**: Documentation-only corrections that keep image tag, profile, route, healthcheck, and volume descriptions aligned with compose.
- **Disallowed**: Collection delete, snapshot restore, volume replacement, cluster repair, or data mutation steps presented as approved policy without separate owner approval and verified runbook evidence.
- **Disallowed**: Claiming a Qdrant API-key secret is active unless compose declares it.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Qdrant guide](guide.md), [Qdrant runbook](runbook.md), and [infra README](../../../../../infra/04-data/specialized/qdrant/README.md) after compose changes.
- Run `docker compose --profile data --profile ai config qdrant` before approving service-name, image, route, secret, healthcheck, or volume documentation updates.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` and `python3 scripts/validation/check-document-links.py --mode alignment` after policy or linked operations document updates.

## Review Cadence

- Review on Qdrant compose image/profile/secret/route/snapshot-path changes.
- Review during the Stage 05 operations documentation audit cadence.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0034`), [Runbook](runbook.md) (`RUN-0034`)

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0034`), [Runbook](runbook.md) (`RUN-0034`)

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0034`), [Runbook](runbook.md) (`RUN-0034`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/specialized/qdrant/README.md)
