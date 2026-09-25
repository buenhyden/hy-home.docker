---
title: "Dozzle Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0072"
parent_ids:
- "GDE-0072"
created: "2026-05-17"
---

# Dozzle Recovery Runbook

## When to Use

Use for OIDC/CIDR denial, missing log streams, socket errors, settings loss, a
suspected compromise, or an approved upgrade.

## Procedure

1. Validate and inspect from the root:

   ```bash
   docker compose --profile admin-logs config --quiet
   docker compose --profile admin-logs ps dozzle
   docker compose --profile admin-logs logs --tail=200 dozzle
   ```

2. Separate OIDC issuer/client/secret/CA, CIDR, Docker socket, target container,
   and Docker log-driver symptoms. Do not capture raw application logs by default.
3. On suspected auth bypass or socket compromise, stop Dozzle, revoke/rotate the
   OIDC client secret, and preserve sanitized audit evidence. The `:ro` socket
   flag is not proof that Docker API mutation was impossible.
4. Restart only after OIDC/CIDR/socket controls are reviewed. Verify allowed and
   denied identities/CIDRs and expected filtered visibility.

### Settings recovery and upgrade

Stop Dozzle, copy the complete bind-backed `/data` to protected storage, and
restore it first to an isolated instance without the production socket. For an
upgrade, review advisories/releases and test OIDC, roles/filters, streaming, and
actions/shell defaults against that copy. Roll back image plus settings copy if incompatible.

## Evidence

Record exits, source commit, OIDC/CIDR allow/deny booleans, visible container
count, settings checksum, and final socket/service disposition. Redact log content.

## Rollback or Recovery

Settings restore and upgrade rehearsal are **planned but unexecuted**. Docker
logs require their own logging backend recovery; Dozzle cannot restore them.

## Escalation

Stop on suspected socket compromise, auth/CIDR bypass, secret exposure, missing
log authority, or settings incompatibility.

## Traceability

- [Guide](../guides/0072-dozzle.md) (`GDE-0072`)
- [Policy](../policies/0072-dozzle.md) (`POL-0072`)
- [Dozzle Compose](../../../infra/11-laboratory/dozzle/docker-compose.yml)

## Related Documents

- [Dozzle authentication](https://dozzle.dev/guide/authentication)
