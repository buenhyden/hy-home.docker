---
title: "RedisInsight Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0076"
parent_ids:
- "POL-0076"
implementation_services:
  infra/11-laboratory/redisinsight/docker-compose.yml:
  - redisinsight
created: "2026-05-10"
---

# RedisInsight Usage Guide

## Usage

### Purpose and classification

RedisInsight is an OPTIONAL admin UI under `admin` and `admin-data`; it is not a
Redis/Valkey server and does not back up target databases. It persists connection
definitions, credentials, workbench history, and logs under
`${DEFAULT_MANAGEMENT_DIR}/redisinsight` mounted at `/data`.

### Current implementation and gap

- [RedisInsight Compose](../../../infra/11-laboratory/redisinsight/docker-compose.yml)
  owns profiles, volume, route, CIDR, middleware, and healthcheck.
- The UI is reachable only through Traefik, with admin CIDR and OAuth2 Proxy
  ForwardAuth. No host port is published.
- Current source declares no `RI_ENCRYPTION_KEY`. Upstream states this key encrypts
  locally stored database passwords/workbench history. Until configured and
  migrated, treat `/data` and its backups as sensitive plaintext-at-rest risk.
- Directory health proves only `/data` availability. It does not prove gateway
  auth, target credentials, or target database authorization.
- Upstream identifies RedisInsight as SSPL-licensed and requires applicable terms
  acceptance; this repository does not assert another edition/license.

### Normal use, backup, and upgrade

Validate `docker compose --profile admin-data config --quiet`. Verify gateway
auth/CIDR, then add only least-privilege target credentials. Destructive commands
in Workbench require target-owner approval; ForwardAuth does not constrain Redis
permissions.

Stop RedisInsight before copying `/data`. Protect the backup as credential-bearing
material; a UI settings backup is not a target database backup. Restore first
into an isolated RedisInsight with no access to production Redis/Valkey and the
same encryption key if one is later configured. Before upgrade, review release
and license terms and test stored connections/history. No backup/restore ran here.

## Common Checks

- `docker compose --profile admin-data config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

Use the [runbook](../runbooks/0076-redisinsight.md) for auth, settings, credential, target, or upgrade recovery.

## Traceability

- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [Runbook](../runbooks/0076-redisinsight.md) (`RUN-0076`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [RedisInsight configuration and encryption key](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight usage, telemetry, logs, and SSPL license](https://redis.io/docs/latest/develop/tools/insight/)
