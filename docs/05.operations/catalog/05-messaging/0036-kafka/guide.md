---
title: "Kafka Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0036"
parent_ids:
- "POL-0036"
implementation_services:
  infra/05-messaging/kafka/docker-compose.yml:
  - 'kafbat-ui'
  - 'kafka-1'
  - 'kafka-2'
  - 'kafka-3'
  - 'kafka-connect'
  - 'kafka-exporter'
  - 'kafka-init'
  - 'kafka-rest-proxy'
  - 'schema-registry'
created: "2026-05-10"
---

# Kafka Usage Guide

## Usage

Kafka is an OPTIONAL event-streaming capability. No current HOME consumer proves
that it should run continuously. The three brokers share one Docker host, so the
`messaging-cluster` profile tests KRaft/replication behavior without providing
host availability. The current implementation contains no second broker family.

### Current implementation

[`infra/05-messaging/kafka/docker-compose.yml`](../../../../../infra/05-messaging/kafka/docker-compose.yml)
defines nine services:

| Service | Role | Current selectors |
| --- | --- | --- |
| `kafka-1` | KRaft broker/controller | `messaging`, `messaging-broker`, `messaging-cluster`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `ksql` |
| `kafka-2`, `kafka-3` | additional same-host brokers/controllers | `messaging-cluster` |
| `schema-registry` | schema storage/API | `messaging`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `ksql` |
| `kafka-connect` | connector runtime | `messaging`, `messaging-connect`, `messaging-admin` |
| `kafka-rest-proxy` | REST producer/consumer API | `messaging`, `messaging-rest` |
| `kafbat-ui` | administrative UI with native OIDC/RBAC | `messaging`, `messaging-admin` |
| `kafka-exporter`, `kafka-init` | metrics and topic bootstrap | `messaging`, `messaging-broker`, `messaging-cluster` |

`kafka-1-data`, `kafka-2-data`, `kafka-3-data`, and `kafka-connect-data` are
bind-backed named volumes under `${DEFAULT_MESSAGE_BROKER_DIR}/kafka`. Broker
listeners are currently `PLAINTEXT`, including published host listeners; there is
no broker authentication or TLS. All services use `infra_net` and shared resource
and health templates.

Kafbat renders its native `auth.type: OAUTH2` configuration into tmpfs, reads
`kafbat_client_secret`, trusts the local CA and applies group-based RBAC. Its
Traefik route uses `gateway-standard-chain@file`; the gateway is transport and
header protection, while Kafbat itself performs authentication. No forwarding-auth gateway chain belongs on this native-OIDC route.

### Images, configuration and resource controls

The Compose file owns pinned Confluent Kafka/Schema/Connect/REST, Kafbat and Kafka
exporter image families; repository Renovate may propose updates and the version
projection is derived. Broker keys include `CLUSTER_ID`, `KAFKA_PROCESS_ROLES`,
quorum/listener/advertised-listener/log/replication settings and node IDs. Schema,
Connect and REST use their namespaced keys; Kafbat uses
`KAFKA_CLUSTERS_0_*`, `DYNAMIC_CONFIG_ENABLED`, and `KAFBAT_OAUTH_CLIENT_ID` plus
the client-secret file. Brokers and Connect extend high stateful templates;
Schema, REST and Kafbat medium infrastructure templates; exporter low and init job
low. All long-running services declare health checks.

### Static preflight and profile choice

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
docker compose --env-file .env.example --profile messaging-cluster config --quiet
```

Run from the repository root. The init job creates `infra-events` and
`application-logs` with replication factor 3, so its bootstrap is valid only when
three healthy brokers are available; do not treat the single-broker `messaging`
selection as successful topic initialization without a separately approved fix.
Starting services, creating topics or producing test records is runtime work.

## Runbook Handoff

Kafka recovery includes more than broker directories. Inventory topic data and
configs, partition counts, consumer-group offsets, KRaft cluster metadata,
Schema Registry `_schemas` history/IDs, Connect connector definitions and its
config/offset/status topics. Prefer replay from an authoritative producer source
or approved cross-cluster replication to a fresh isolated cluster. Raw broker
log-directory reuse and live KRaft identity reuse are prohibited.

[RUN-0036](runbook.md) restores schemas before dependent records, recreates topic
configuration, restores/repositions offsets, keeps connectors paused, and proves
end offsets plus application consumption before cutover. An image or protocol
upgrade requires official compatibility review for Kafka, Confluent components,
Kafbat, clients and stored formats, with a current recovery artifact and rollback.

### License and source boundary

Apache Kafka and Kafbat are Apache-2.0 projects. Schema Registry, Connect and REST
images come from Confluent and require separate current license/edition review;
Cluster Linking or other edition-specific features are not declared or assumed.

### Official references

- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Kafka KRaft](https://kafka.apache.org/documentation/#kraft)
- [Kafka license](https://kafka.apache.org/licensing)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat configuration](https://ui.docs.kafbat.io/configuration/configuration-file)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Kafbat license](https://github.com/kafbat/kafka-ui/blob/main/LICENSE)

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0036`; governing policy: `POL-0036`.
- Runtime authority: `infra/05-messaging/kafka/docker-compose.yml`.

## Related Documents

- [Operations policy](policy.md)
- [Cluster recovery runbook](runbook.md)
- [Messaging architecture](../../../../02.architecture/descriptions/0005-messaging-architecture.md)
