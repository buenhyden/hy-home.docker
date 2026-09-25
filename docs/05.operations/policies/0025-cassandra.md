---
title: "Cassandra Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0025"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Cassandra Operations Policy

## Overview

이 정책은 `hy-home.docker`의 `LAB` Cassandra 단일 노드와 exporter 운영 기준을 정의한다. runtime image/version은 Compose declaration이 소유하며, 정책 기준은 `cassandra` profile, `lab_net`, Docker Secret, `${DEFAULT_DATA_DIR}/cassandra/node1` persistence다.

## Policy Scope

- `infra/04-data/nosql/cassandra/docker-compose.yml`
- `cassandra-node1` service and `cassandra-exporter` service
- `cassandra-node1-volume`, `cassandra-exporter-volume`
- `cassandra_password` Docker Secret and `CASSANDRA_USERNAME` identity variable
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Cassandra documentation must identify the current implementation as a single node selected by the exact `cassandra` profile, not as an active multi-node high-availability cluster.
- **Required**: Credential handling must reference `/run/secrets/cassandra_password`; plaintext password variables or copied secret values are disallowed in docs, examples, and evidence.
- **Required**: Volume descriptions must match `${DEFAULT_DATA_DIR}/cassandra/node1` mounted to `/bitnami/cassandra`.
- **Required**: Monitoring references must identify `cassandra-exporter` as a separate service in the same `cassandra` profile.
- **Required**: A backup set must bind its snapshot tag to schema, keyspace/replication metadata, release compatibility, topology/token evidence, and all required SSTables; credentials remain a separate protected artifact.
- **Required**: Restore rehearsal uses an empty, isolated, compatible target. Create schema first, load SSTables with the upstream-supported method, verify ownership/permissions, and reject the rehearsal on missing tables or failed reads.
- **Required**: Retention records backup identifier, capture time, scope, checksum/location, restore test, and expiry. Capacity must leave room for snapshots plus compaction; resource or retention changes require review.
- **Required**: Upgrade requires release/schema/SSTable compatibility review and a successful isolated restore. Removal requires confirmed consumer shutdown, retained backup evidence, expiry/owner, and separate approval before volume deletion.
- **Allowed**: Local status checks, `nodetool status`, compose rendering, and read-only CQL queries for verification.
- **Allowed**: Documentation-only corrections that keep service names, image tags, profiles, and links aligned with compose.
- **Disallowed**: Unverified multi-node repair, quorum, or zero-downtime rotation procedures presented as current implementation; in-place restore over the tracked volume is prohibited.
- **Disallowed**: Runtime data mutation, volume replacement, credential rotation, or backup restore from this policy document alone.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Cassandra guide](../guides/0025-cassandra.md), [Cassandra runbook](../runbooks/0025-cassandra.md), and [infra README](../../../infra/04-data/nosql/cassandra/README.md) after compose changes.
- Run `docker compose --profile cassandra config --quiet` before approving service-name, volume, profile, or secret documentation updates.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy or linked operations document updates.

## Review Cadence

- Review on Cassandra compose image/profile/secret/volume changes.
- Review during the Stage 05 operations documentation audit cadence.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0025-cassandra.md) (`GDE-0025`), [Runbook](../runbooks/0025-cassandra.md) (`RUN-0025`)

## Related Documents

- [Compose implementation: infra/04-data/nosql/cassandra/docker-compose.yml](../../../infra/04-data/nosql/cassandra/docker-compose.yml)

- [Cassandra backup and restore](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
- [Cassandra security](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0025-cassandra.md)
- [Recovery runbook](../runbooks/0025-cassandra.md)
- [Infra README](../../../infra/04-data/nosql/cassandra/README.md)
