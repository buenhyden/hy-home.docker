---
title: "RedisInsight Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0076"
parent_ids:
- "AD-0011"
created: "2026-05-17"
---

# RedisInsight Operations Policy

## Overview

RedisInsight is an OPTIONAL credential-bearing admin client. Gateway access does
not replace least-privilege authorization on each target database.

## Policy Scope

Activation, gateway/CIDR, stored target credentials/history, target actions,
telemetry/license, settings backup/restore, upgrade, and removal.

## Controls

- Use only `admin`/`admin-data`; keep outside HOME.
- Preserve ForwardAuth and admin CIDR. Use unique least-privilege target accounts;
  destructive Workbench commands require target-owner approval.
- Treat `/data` and backups as sensitive. Current source lacks
  `RI_ENCRYPTION_KEY`; track that as a security gap, not an assurance.
- A RedisInsight backup covers client settings only. Target Redis/Valkey backups
  follow each engine's owner and cannot be replaced by `/data`.
- Stop the service for a consistent settings copy; restore with production target
  network disabled and the matching encryption key when configured.
- Review release notes, telemetry settings, and applicable SSPL/license terms
  before upgrades. Revoke stored target credentials before removal.

## Exceptions

No exception may bypass target authorization or treat gateway login as database
permission. Unencrypted credential storage cannot be called secure.

## Verification

Verify gateway/CIDR allow/deny, target account scope, settings persistence, and
that restore testing cannot reach production targets.

## Review Cadence

Review on image/license, auth/CIDR, encryption-key, target, or storage changes.

## Traceability

- [Guide](guide.md) (`GDE-0076`)
- [Runbook](runbook.md) (`RUN-0076`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [RedisInsight Compose source](../../../../../infra/11-laboratory/redisinsight/docker-compose.yml)
- [RedisInsight configuration](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight documentation](https://redis.io/docs/latest/develop/tools/insight/)
