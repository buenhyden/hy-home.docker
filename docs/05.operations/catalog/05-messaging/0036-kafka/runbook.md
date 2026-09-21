---
title: "Kafka Cluster Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "RUN-0036"
parent_ids:
- "GDE-0036"
created: "2026-05-17"
---

# Kafka Cluster Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

## Procedure

From the repository root:

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
docker compose --env-file .env.example --profile messaging-cluster config --quiet
```

Confirm the ten expected services, distinct broker/Connect volumes, `infra_net`,
health checks, Kafbat native OIDC secret/config, standard gateway chain and
PLAINTEXT listeners. Confirm `kafka-init` replication factor 3 is paired with the
three-broker selector before any runtime use.

### CDC connector lifecycle

1. Preconditions: `debezium-db-provision` exited `0`; `mng-pg` reports
   `SHOW wal_level` = `logical`; Connect logs `debezium.properties rendered`;
   the plugin class is listed by `GET /connector-plugins`.
2. Registration is an approved runtime change. From a container on `infra_net`:
   `PUT /connectors/hyhome-app-postgres/config` with the tracked JSON body.
3. Verify each state separately: `GET .../status` shows connector and task
   `RUNNING`; the log reports the snapshot completed; a test change in an
   approved table appears on its `hyhome.app.*` topic.
4. Lag: query `pg_replication_slots` for `hyhome_app_slot` (`active`,
   `wal_status`, `pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)`).
   `wal_status = lost` means the slot was invalidated.
5. Pause with `PUT .../pause` for maintenance; the slot keeps WAL while paused,
   so bound the pause by the free disk and `max_slot_wal_keep_size`.
6. Resynchronization (approved only): stop the connector, record the
   downstream boundary, drop the slot and reset offsets together, re-register
   with a new snapshot, and reconcile duplicates downstream. Never drop the
   slot alone as a quick fix.
7. Password rotation: replace the secret, re-run `debezium-db-provision`,
   restart Connect (re-renders the properties file), then restart the connector.

### Planned backup or replication capture

1. Identify producers, consumers, schemas, connectors, retention and an accepted
   recovery point. Pause or fence changes to topics, schemas and connectors.
2. Export a manifest of cluster ID, broker/storage format, topic configurations,
   partition counts, high-water marks and consumer-group offsets.
3. Replicate/replay user topic records to a separate compatible Kafka target using
   an approved mechanism. Verify per-partition source and target end offsets and
   record counts/checksums where the data format supports them.
4. Migrate Schema Registry history with an official compatible procedure that
   preserves schema subjects, versions and IDs required by serialized data.
5. Export Connect connector definitions without secrets and preserve its
   config/offset/status state through a compatible supported method. Record how
   each external system will be reconciled.
6. Protect manifests and any exported data on a separate encrypted destination.
   Do not copy active broker log directories or KRaft metadata piecemeal.

### Planned isolated restore

1. Provision a fresh network-isolated Kafka target at a compatible version with a
   new cluster identity. Keep external producers, consumers and connectors blocked.
2. Recreate topic configurations and partition counts. Restore schemas/IDs before
   loading records that depend on them.
3. Replay/replicate topic records and validate every partition's expected end
   offset, sample key/value/checksum and retention behavior.
4. Restore or deliberately reposition consumer offsets, documenting any replay or
   skipped range. Recreate connector definitions with credentials from protected
   custody; keep connectors paused while validating their offset/status state.
5. Run disposable producer/consumer schema-compatible tests. Resume a connector
   only against isolated test endpoints and verify idempotency/reconciliation.
6. Record observed recovery point, elapsed time and gaps. A separate cutover task
   fences source writes, captures final deltas, switches clients and preserves
   rollback. Do not reuse the live KRaft cluster ID.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

A failed cutover returns producers and consumers to the preserved source cluster
after offset/write-boundary validation; the replay source and target remain retained. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

Stop on schema-ID drift, missing partitions, offset gaps, checksum mismatch,
connector side effects, incompatible storage/protocol format or pressure to
repair raw broker directories. No backup or restore was executed by this
documentation task.

## Traceability

- Runtime source: [Kafka Compose](../../../../../infra/05-messaging/kafka/docker-compose.yml)
  and the [Connect image Dockerfile](../../../../../infra/05-messaging/kafka/Dockerfile.connect).
- Artifact: `RUN-0036`; parent guide: `GDE-0036`.
- Procedures are planned unless a dated verification record explicitly says they ran.

### References

- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Policy](policy.md)

## Related Documents

- [Domain catalog](../README.md)
