---
title: "Terrakube Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "GDE-0069"
parent_ids:
- "POL-0069"
implementation_services:
  infra/09-tooling/terrakube/docker-compose.yml:
  - terrakube-api
  - terrakube-executor
  - terrakube-ui
created: "2026-05-10"
---

# Terrakube Usage Guide

## Usage

### Purpose and classification

Terrakube is an on-demand DEV IaC automation/control plane. The API, UI, and
executor belong only to `iac`; broad `tooling` and HOME do not start them. It is
retained for reviewed collaborative runs and private module/registry workflows.
The tracked topology has one replica of each component and single-host external
dependencies; it does not provide or claim high availability.

### Implementation and data flow

- [Terrakube Compose](../../../infra/09-tooling/terrakube/docker-compose.yml)
  owns services, profiles, images, secrets, healthchecks, routes, and executor
  Docker socket access. The derived image projection does not own runtime pins.
- Browser -> Traefik -> `terrakube-ui`; UI -> `terrakube-api`; API dispatches to
  `terrakube-executor`. The existing routes apply gateway ForwardAuth while UI/API
  settings also use Keycloak/Dex-style OIDC. Both layers must be tested; static
  configuration does not prove native login or role mapping.
- PostgreSQL (`mng-pg`) holds Terrakube metadata. SeaweedFS bucket `tfstate` holds
  state and outputs. Management Valkey coordinates work. These are dependencies,
  not services declared in the Terrakube leaf.
- Secrets are `terrakube_db_password`, `seaweedfs_s3_terrakube_secret_key`,
  `terrakube_valkey_password`, `terrakube_pat_secret`, and
  `terrakube_internal_secret`; values never enter evidence.
- The executor mounts `/var/run/docker.sock` read-write. This is host-equivalent
  execution authority and requires the same trust as local Docker administration.
- Health endpoints prove component process readiness only. They do not prove DB,
  object-state, VCS, OIDC, or executor end-to-end acceptance.

### Normal use

1. Identify organization/workspace, VCS repository/ref, provider credentials,
   expected resources, state key, and approval boundary.
2. From the root run `docker compose --profile iac config --quiet` and confirm
   all three Terrakube services plus the separately selected dependencies.
3. Verify PostgreSQL, SeaweedFS `tfstate`, Valkey, Keycloak, and gateway readiness
   without printing credentials or state.
4. Start only the Terrakube services after dependency and Docker-socket authority
   review. Verify UI login, API authorization, executor registration, and a
   non-applying plan separately.
5. Applying or destroying infrastructure is a separate remote mutation approval.

### State, backup, and upgrade

Recovery needs a consistent set: Terrakube PostgreSQL database, SeaweedFS `tfstate`
objects/versions, relevant Keycloak client/role configuration, tracked Compose,
and secret metadata/custody. Valkey is coordination state and must be empty or
consistent with a quiesced control plane. Stop new runs and quiesce API/executor
before coordinated database/object snapshots. Restore only in an isolated
environment with provider and webhook egress disabled, then verify DB/state-key
referential consistency and a non-applying plan. Do not infer recoverability from
one SeaweedFS copy or one DB dump.

Before upgrade, take that coordinated backup, read Terrakube release/migration
notes, test against restored copies, and roll forward one component set together.
Image rollback without database/state rollback is unsafe after migrations.
Backup/restore and upgrade rehearsal remain unexecuted in this documentation task.

## Common Checks

- `docker compose --profile iac config --quiet`
- `docker compose --profile iac config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

Use the [runbook](../runbooks/0069-terrakube.md) for failed runs, coordinated backup/restore, OIDC
diagnosis, or upgrades.

## Traceability

- [Policy](../policies/0069-terrakube.md) (`POL-0069`)
- [Runbook](../runbooks/0069-terrakube.md) (`RUN-0069`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Terrakube architecture](https://docs.terrakube.io/architecture)
- [Terrakube Amazon-compatible storage](https://docs.terrakube.io/getting-started/deployment/storage-backend/amazon-cloud-storage)
- [Terrakube project and Apache-2.0 license](https://github.com/terrakube-io/terrakube)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
