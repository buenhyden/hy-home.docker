---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md -->

# SeaweedFS Operations Policy

> This policy governs the current SeaweedFS services under `04-data/lake-and-object`.

---

## Overview

이 정책은 SeaweedFS data-profile stack의 master, volume, filer, S3 gateway, mount service 운영 통제를 정의한다. 정책 기준은 현재 compose에 실제로 선언된 image, route, healthcheck, volume, mount privilege, and network surface다.

## Policy Scope

- **Systems**: `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`
- **Configs**: `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`;
  `config/security.toml.example` remains as a future scaffold and is not
  mounted by current compose
- **Profiles**: `data`
- **Networks**: `infra_net`
- **Agents**: AI agents reviewing or updating operations docs, compose references, validation evidence, or file/object-storage runtime boundaries

## Controls

- **Required**:
  - Compose-facing documentation must list image `chrislusf/seaweedfs:4.31` and the current five-service set.
  - Health checks are documented for `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, and `seaweedfs-s3`; `seaweedfs-mount` has no compose healthcheck.
  - `seaweedfs-mount` privileged/SYS_ADMIN behavior must be treated as host-impacting.
  - Public access must use the declared Traefik routes: `seaweedfs.${DEFAULT_URL}`, `cdn.${DEFAULT_URL}`, and `s3.${DEFAULT_URL}`.
- **Allowed**:
  - Metadata-only compose validation with `docker compose ... config`.
  - Read-only service health/log checks.
  - Mount container restart only after capturing evidence and confirming host-impacting scope.
- **Disallowed**:
  - Claiming SeaweedFS authentication is active unless a reviewed security
    config is created, mounted, and used by the compose file.
  - Running destructive master metadata restore, volume deletion, unmount, or reshard operations as documentation-only actions.
  - Treating the S3 gateway as credential-protected by the current compose unless credential config is explicitly added and documented.
  - Recording private data, tokens, or credentials in documentation or task evidence.

## Exceptions

Exceptions require explicit owner or user approval and must record scope, affected services, commands, host-impact considerations, validation output, and rollback/escalation state in related task or incident evidence.

## Verification

- Run `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config` after changing compose-facing documentation.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy, guide, runbook, README, or link updates.
- Run `bash scripts/validation/check-doc-implementation-alignment.sh` when the change is part of implementation-vs-doc drift remediation.
- Search updated docs for stale image versions, unmounted security config claims, single-container log commands, and destructive recovery commands before committing.

## Review Cadence

Review on any change to SeaweedFS compose services, image tag, routes, ports, profile, network, volume declarations, mount privilege, security config usage, or linked operations documents. Otherwise review during the regular Stage 05 operations audit.

---

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/lake-and-object/seaweedfs.md)
- [Recovery runbook](../../../runbooks/04-data/lake-and-object/seaweedfs.md)
- [Infrastructure service README](../../../../../infra/04-data/lake-and-object/seaweedfs/README.md)
