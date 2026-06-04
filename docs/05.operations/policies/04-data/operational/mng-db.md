---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/operational/mng-db.md -->

# Management Database Operations Policy

> This policy governs current `mng-db` operations and implementation-aligned controls.

---

## Overview (KR)

이 정책은 `infra/04-data/operational/mng-db`의 PostgreSQL, Valkey, init job, exporter 운영 기준을 정의한다. 정책 목적은 플랫폼 관리 메타데이터를 안전하게 유지하고, 문서와 compose의 서비스/네트워크/secret 경계가 서로 어긋나지 않도록 하는 것이다.

## Policy Scope

- **Systems**: `mng-pg`, `mng-pg-init`, `mng-pg-exporter`, `mng-valkey`, `mng-valkey-exporter`
- **Configs**: `infra/04-data/operational/mng-db/docker-compose.yml`, `pg/init-scripts/init_users_dbs.sql`
- **Networks**: `infra_net`; `k3d-hyhome` only for `mng-pg` and `mng-valkey`
- **Environments**: local, dev, and approved infrastructure hosts using the `mng` or `dev` compose profile
- **Agents**: AI agents reviewing or updating operations docs, compose references, or validation evidence

## Controls

- **Required**:
  - Passwords and service credentials are injected through Docker Secrets under `/run/secrets/`.
  - Compose references must use the current service set: `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`.
  - `mng-pg-init` is the approved database/role synchronization path for `n8n`, `keycloak`, `airflow`, `terrakube`, `sonarqube`, and the declared service DB.
  - Documentation changes that alter service, network, secret, or runbook behavior must update the paired guide, policy, runbook, and relevant README links.
- **Allowed**:
  - Metadata-only compose validation with `docker compose ... config`.
  - Read-only service status checks and exporter metric availability checks.
  - Re-running `mng-pg-init` after compose render, secret readiness, and policy/runbook context are confirmed.
- **Disallowed**:
  - Referencing or creating legacy shared-network names for this stack.
  - Recording secret values, generated passwords, tokens, or certificate material in documentation or task evidence.
  - Treating this non-HA management database as the HA relational PostgreSQL cluster.
  - Adding external direct exposure beyond the host ports declared in the compose file without an approved implementation change and updated operations docs.

## Exceptions

Exceptions require explicit user or owner approval and must record the reason, scope, commands, verification result, and rollback/escalation state in the related task or incident evidence.

## Verification

- Run `docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng config` after changing compose-facing documentation.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy, guide, runbook, README, or link updates.
- Run `bash scripts/validation/check-doc-implementation-alignment.sh` when the change is part of implementation-vs-doc drift remediation.
- Search updated docs for legacy network names, old Compose CLI spelling, or secret values before committing.

## Review Cadence

Review on any change to `mng-db` compose services, networks, profiles, ports, secret refs, initialization SQL, or linked operations documents. Otherwise review during the regular Stage 05 operations audit.

---

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/operational/mng-db.md)
- [Recovery runbook](../../../runbooks/04-data/operational/mng-db.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/mng-db/README.md)
