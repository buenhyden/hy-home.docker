---
title: "RedisInsight Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0076"
parent_ids:
- "GDE-0076"
created: "2026-05-17"
---

# RedisInsight Recovery Runbook

## When to Use

Use for gateway login failure, lost/corrupt settings, target auth failure,
credential exposure, settings restore, or upgrade.

## Procedure

1. Validate and inspect from the root:

   ```bash
   docker compose --profile admin-data config --quiet
   docker compose --profile admin-data ps redisinsight
   docker compose --profile admin-data logs --tail=200 redisinsight
   ```

2. Separate gateway/CIDR, RedisInsight settings, and target database symptoms.
   Never test with an administrator target credential unless explicitly approved.
3. If stored credentials may be exposed, stop RedisInsight, rotate them at each
   target, remove/re-add connection definitions after recovery, and preserve only
   sanitized evidence.
4. Restart only after `/data` ownership/free-space and gateway controls pass.

### Settings restore and upgrade

1. Stop RedisInsight and copy all of `/data` to protected storage. Record checksum
   and source commit; protect it as credential-bearing material.
2. Restore to an isolated instance with production target network blocked. Use
   the same `RI_ENCRYPTION_KEY` if the source deployment had one; current tracked
   configuration does not declare it.
3. Verify settings/log counts and UI access without connecting to live targets.
4. For upgrade, review release/license notes, test the target image on the copied
   settings, and verify gateway access plus a disposable test database connection.

## Evidence

Record exits, source commit, settings checksum/counts, gateway/CIDR booleans,
credential-rotation receipt, target account scope, and final state. No passwords,
keys, query history, or data values.

## Rollback or Recovery

Settings restore and upgrade rehearsal are **planned but unexecuted**. Restore of
target Redis/Valkey data belongs to the target engine runbook.

## Escalation

Stop on credential exposure, missing encryption key for encrypted data, unknown
target authority, settings corruption, license ambiguity, or production target
reachability during restore rehearsal.

## Traceability

- [Guide](../guides/0076-redisinsight.md) (`GDE-0076`)
- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [RedisInsight Compose](../../../infra/11-laboratory/redisinsight/docker-compose.yml)

## Related Documents

- [RedisInsight configuration](https://redis.io/docs/latest/operate/redisinsight/configuration/)
