---
title: "Pact Broker Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0093"
parent_ids:
- "GDE-0093"
created: "2026-09-23"
---

# Pact Broker Recovery Runbook

## When to Use

Provisioning failure, an unhealthy broker, 401 errors for a client that should
be authorized, a lost database, or credential rotation.

## Procedure

1. Inspect:

   ```bash
   docker compose --profile core --profile contract-testing config --quiet
   docker compose --profile core --profile contract-testing ps pact-broker pact-broker-db-provision
   docker compose --profile core --profile contract-testing logs --tail=100 pact-broker-db-provision pact-broker
   curl -s http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}/diagnostic/status/heartbeat
   ```

2. Provisioning exit `64` is an input problem before any change; exit `3` names
   the refused condition (an administrator role, a role this job did not create,
   or a database with another owner). Fix the cause and re-run
   `pact-broker-db-provision`; it converges.
3. Broker exit `64` means a credential secret is present but empty; exit `1`
   means it is missing or unreadable. A database connection
   error after start usually means the role password and the secret diverged:
   re-run `pact-broker-db-provision`, which resets the role password from the
   secret, then restart `pact-broker`.
4. A 401 for a client means its username or password differs from
   `PACT_BROKER_BASIC_AUTH_USERNAME` and the `pact_broker_basic_auth_password`
   secret.

### Credential rotation

Replace the secret through the registered workflow. For
`pact_broker_db_password`, re-run `pact-broker-db-provision` and restart the
broker; for `pact_broker_basic_auth_password`, restart the broker and update
every publishing and verifying client.

## Evidence

Record exit codes, the heartbeat status, pacticipant and pact counts and the
source commit; never a credential or a pact body.

## Rollback or Recovery

The broker database is the only state. It is part of the `mng-pg` pgBackRest
backups (RUN-0021); restoring `mng-pg` restores it. Losing it loses the
verification history `can-i-deploy` relies on, but consumers can republish
pacts and providers re-verify. Dropping the database is a data change that
needs approval.

## Escalation

Stop on any request to disable basic auth, allow public read, expose the port
beyond loopback, or grant the role more than its own database.

## Traceability

- [Guide](../guides/0093-pact-broker.md) (`GDE-0093`)
- [Policy](../policies/0093-pact-broker.md) (`POL-0093`)
- [Pact Broker Compose](../../../infra/09-tooling/pact-broker/docker-compose.yml)

## Related Documents

- [Management database runbook](0028-management-database.md)
- [Backup and restore runbook](0021-backup-and-restore.md) (`RUN-0021`)
