---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/lake-and-object/minio.md -->

# MinIO Object Storage Operations Policy

> This policy governs the current MinIO object storage services under `04-data/lake-and-object`.

---

## Overview (KR)

이 정책은 root-active MinIO 단일 service와 bucket bootstrap job의 운영 통제를 정의한다. 정책 기준은 `infra/04-data/lake-and-object/minio/docker-compose.yml`의 실제 service, profile, network, secret, bucket initialization surface다.

## Policy Scope

- **Systems**: `minio`, `minio-create-buckets`
- **Configs**: `infra/04-data/lake-and-object/minio/docker-compose.yml`; optional variant `docker-compose.cluster.yaml` only when explicitly invoked
- **Profiles**: `storage`, `obs`, `dev`
- **Networks**: `infra_net`
- **Agents**: AI agents reviewing or updating operations docs, compose references, validation evidence, or object-storage runtime boundaries

## Controls

- **Required**:
  - Root and app credentials are injected through Docker Secrets under `/run/secrets/`.
  - Compose-facing documentation must distinguish the root-active single-node compose from the optional cluster variant.
  - Bucket bootstrap behavior must match `minio-create-buckets`: `tempo-bucket`, `loki-bucket`, `cdn-bucket`, `doc-intel-assets`, and public anonymous read only for `cdn-bucket`.
  - Public access changes beyond the bootstrap policy require explicit approval and evidence.
- **Allowed**:
  - Metadata-only compose validation with `docker compose ... config`.
  - Read-only service health/log checks that do not expose secret values.
  - Optional cluster variant review when clearly scoped to `docker-compose.cluster.yaml` and not presented as root-active infrastructure.
- **Disallowed**:
  - Recording secret values, access keys, tokens, or private bucket content in documentation or task evidence.
  - Treating optional cluster nodes as active root include services.
  - Performing destructive bucket deletion, credential rotation, or volume restore as a documentation-only action.
  - Assuming direct host-port exposure when current root-active compose uses Traefik routing and no direct `ports` entries.

## Exceptions

Exceptions require explicit owner or user approval and must record scope, affected buckets/services, commands, secret-safety considerations, validation output, and rollback/escalation state in related task or incident evidence.

## Verification

- Run `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config` after changing compose-facing documentation.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy, guide, runbook, README, or link updates.
- Run `bash scripts/validation/check-doc-implementation-alignment.sh` when the change is part of implementation-vs-doc drift remediation.
- Search updated docs for active/optional cluster confusion, direct secret values, unapproved public access claims, and direct host-port assumptions before committing.

## Review Cadence

Review on any change to MinIO compose services, image tag, profiles, network, secret refs, Traefik routes, bucket bootstrap job, optional cluster variant, or linked operations documents. Otherwise review during the regular Stage 05 operations audit.

---

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/lake-and-object/minio.md)
- [Recovery runbook](../../../runbooks/04-data/lake-and-object/minio.md)
- [Infrastructure service README](../../../../../infra/04-data/lake-and-object/minio/README.md)
