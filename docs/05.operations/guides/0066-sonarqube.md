---
title: "SonarQube Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0066"
parent_ids:
- "POL-0066"
implementation_services:
  infra/09-tooling/sonarqube/docker-compose.yml:
  - sonarqube
created: "2026-05-10"
---

# SonarQube Usage Guide

## Usage

### Purpose and classification

SonarQube Community Build is an on-demand **OPTIONAL** code-quality/SAST service
under `tooling` and `sast`, excluded from HOME. This repository does not define a
universal merge quality gate in this service guide; project/CI owners decide how
analysis results gate delivery.

### Current implementation and flow

- [SonarQube Compose](../../../infra/09-tooling/sonarqube/docker-compose.yml)
  owns the runtime image, profiles, DB secret, JVM heap, routes, volumes, and health.
- Browser/scanner -> Traefik -> SonarQube. The route uses OAuth2 Proxy
  ForwardAuth. No tracked SonarQube SAML/OIDC configuration proves native
  Keycloak login or group provisioning; SonarQube users, permissions, and analysis
  tokens remain application-owned.
- PostgreSQL at `${POSTGRES_MNG_HOSTNAME}` stores authoritative projects,
  settings, issues, users, and analysis state. `/opt/sonarqube/data` stores local
  search indexes and `/opt/sonarqube/logs` stores logs. The Compose leaf has no
  persistent extensions/plugins/config volume.
- `sonarqube_db_password` is file-mounted. Analysis tokens are created in
  SonarQube and never belong in Compose or evidence.
- Both web and search JVMs are capped at 512 MiB heap by tracked environment;
  the service inherits `template-stateful-high`.
- `/api/system/health` proves process health only; it does not prove DB backup,
  index consistency, scanner authorization, or gateway login.

### Normal use

1. Validate `docker compose --profile sast config --quiet` from the root and
   verify the management PostgreSQL dependency separately.
2. Start only SonarQube, wait for system health, then verify gateway access and
   SonarQube permissions as separate controls.
3. Use an expiring project/global analysis token with the minimum permission.
   Keep it out of shell history and logs.
4. Run a scanner for the intended project and record project key, commit, quality
   result, and task ID without token or source content.

### Backup, restore, and upgrade

The database is the backup authority. Official guidance uses database-native
backup and rebuilds Elasticsearch indexes after restore. A consistent recovery
also preserves tracked config, DB secret custody, and any externally installed
plugins/config not represented here. Restore to an isolated DB, start SonarQube
with local indexes absent, allow reindexing, and verify projects/settings/users
and representative scans. Deleting active indexes is never a first-line repair.

Before upgrade, back up/verify the DB, read all release/upgrade notes, confirm DB
and host prerequisites, inventory plugins, and test on a restored copy. Rollback
requires both the previous image and the pre-upgrade database; image rollback
alone cannot undo schema migration. No backup/restore/upgrade ran here.

## Common Checks

- `docker compose --profile sast config --quiet`
- `docker compose --profile sast config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

Use the [runbook](../runbooks/0066-sonarqube.md) for DB failures, indexing recovery, analysis queues,
or upgrades.

## Traceability

- [Policy](../policies/0066-sonarqube.md) (`POL-0066`)
- [Runbook](../runbooks/0066-sonarqube.md) (`RUN-0066`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [SonarQube backup and restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade guide](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
- [Community Build authentication capabilities](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [Community Build Web API authentication](https://docs.sonarsource.com/sonarqube-community-build/extension-guide/web-api)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
