---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/specialized/qdrant.md -->

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

- Compare this policy with [Qdrant guide](../../../guides/04-data/specialized/qdrant.md), [Qdrant runbook](../../../runbooks/04-data/specialized/qdrant.md), and [infra README](../../../../../infra/04-data/specialized/qdrant/README.md) after compose changes.
- Run `docker compose --profile data --profile ai config qdrant` before approving service-name, image, route, secret, healthcheck, or volume documentation updates.
- Run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after policy or linked operations document updates.

## Review Cadence

- Review on Qdrant compose image/profile/secret/route/snapshot-path changes.
- Review during the Stage 05 operations documentation audit cadence.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/specialized/qdrant.md)
- [Recovery runbook](../../../runbooks/04-data/specialized/qdrant.md)
- [Infra README](../../../../../infra/04-data/specialized/qdrant/README.md)
