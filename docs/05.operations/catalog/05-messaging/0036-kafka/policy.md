---
title: "Kafka Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "POL-0036"
parent_ids:
- "AD-0005"
created: "2026-05-17"
---

# Kafka Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

Kafka-family services remain OPTIONAL. A named producer/consumer and approved
capacity, retention, security and recovery plan are required before activation.
Controls for removed broker families do not apply to the current implementation.

## Controls

- Select exact root profiles; never operate the leaf file as a separate Compose
  project. Treat `messaging-cluster` as same-host LAB topology.
- Keep broker and Connect volumes distinct and preserve `infra_net`, health checks
  and shared resource limits.
- Current broker, controller and host listeners are PLAINTEXT. Do not claim
  transport confidentiality or client authentication. Restrict exposure and plan
  broker TLS/SASL as a separate architectural change before sensitive workloads.
- Kafbat must retain native OIDC/RBAC, local CA trust and
  `kafbat_client_secret`. Its route uses only the standard gateway chain; do not
  substitute forwarding-header authentication.
- Topic creation/deletion, partition increase, retention reduction, consumer
  offset movement and connector changes require explicit change scope and rollback.
- The bootstrap topics request replication factor 3 and therefore require three
  healthy brokers. A one-broker selection must not run that initialization as if
  it were valid.

### Change data capture

- CDC credentials, grants and publication belong to the `debezium-db-provision`
  job. Never give the connector superuser, database ownership or write grants
  beyond the `debezium_heartbeat` schema it owns for the heartbeat query.
- Keep `FileConfigProvider` restricted by `allowed.paths` and the Connect REST
  gateway route behind SSO. Treat direct `infra_net` access to port 8083 as a
  recorded gap, not an authorization control.
- Registering, reconfiguring, restarting with a new snapshot mode or deleting a
  connector needs approval naming the connector and source database.
- Replication slots and connector offsets are recovery state. Deleting a slot or
  resetting offsets is a destructive resynchronization, never a routine fix; it
  needs approval, a downstream duplicate/gap plan and a new snapshot.
- Monitor slot lag against `max_slot_wal_keep_size`. An invalidated slot means
  missed changes until a new snapshot completes.

### Data protection

Recovery scope includes topic records/configuration, consumer offsets, KRaft
metadata, Schema Registry history and IDs, Connect definitions and internal
config/offset/status topics. Prefer producer replay or approved cross-cluster
replication to a separate compatible target. A raw live copy of broker log dirs is
not a backup. Store manifests and artifacts on an encrypted distinct destination.

For selected workloads, set workload-specific data retention and RPO/RTO; the
planning recovery-artifact retention is daily 30 days and weekly 90 days. Until
then, the planning ceiling is RPO 24 hours and RTO 8 hours and is unverified.
Shared resource-template limits remain mandatory. Removal requires producer,
consumer, topic, schema, offset and connector inventory plus replay/restore proof. A restore must be
rehearsed in isolation and prove schema compatibility, end offsets, record counts
or checksums, consumer positions and paused-then-resumed connector behavior.

### Upgrade and license policy

Review Apache Kafka protocol/storage compatibility, Confluent component
compatibility and license/edition terms, Kafbat release/security notes and client
support before a pin change. Preserve rollback and current recovery artifacts.
Do not assume Cluster Linking or other commercial/edition-specific capability is
available.

## Exceptions

The optional stack may be absent; no listener-security exception is implied. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Runtime source: [Kafka Compose](../../../../../infra/05-messaging/kafka/docker-compose.yml).
- Artifact: `POL-0036`; parent: `AD-0005`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

### References

- [Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Runbook](runbook.md)

## Related Documents

- [Domain catalog](../README.md)
