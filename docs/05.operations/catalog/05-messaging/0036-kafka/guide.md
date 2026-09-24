---
title: "Kafka Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "operations"
artifact_id: "GDE-0036"
parent_ids:
- "POL-0036"
implementation_services:
  infra/05-messaging/kafka/docker-compose.yml:
  - 'debezium-db-provision'
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
defines ten services:

| Service | Role | Current selectors |
| --- | --- | --- |
| `kafka-1` | KRaft broker/controller | `messaging`, `messaging-broker`, `messaging-cluster`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc` |
| `kafka-2`, `kafka-3` | additional same-host brokers/controllers | `messaging-cluster` |
| `schema-registry` | schema storage/API | `messaging`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc` |
| `kafka-connect` | connector runtime with the Debezium PostgreSQL plugin | `messaging`, `messaging-connect`, `messaging-admin`, `cdc` |
| `debezium-db-provision` | CDC source role, grants and publication on `mng-pg` | `cdc` |
| `kafka-rest-proxy` | REST producer/consumer API | `messaging`, `messaging-rest` |
| `kafbat-ui` | administrative UI with native OIDC/RBAC | `messaging`, `messaging-admin` |
| `kafka-exporter`, `kafka-init` | metrics and topic bootstrap | `messaging`, `messaging-broker`, `messaging-cluster` |

`kafka-1-data`, `kafka-2-data`, `kafka-3-data`, and `kafka-connect-data` are
bind-backed named volumes under `${DEFAULT_MESSAGE_BROKER_DIR}/kafka`. Broker
listeners are currently `PLAINTEXT`, including published host listeners; there is
no broker authentication or TLS. All services use `kafka_net` and shared resource
and health templates.

Kafbat renders its native `auth.type: OAUTH2` configuration into tmpfs, reads
`kafbat_client_secret`, trusts the local CA and applies group-based RBAC. Its
Traefik route uses `gateway-standard-chain@file`; the gateway is transport and
header protection, while Kafbat itself performs authentication. No forwarding-auth gateway chain belongs on this native-OIDC route.
The Kafka Connect REST route now adds `sso-errors`/`sso-auth`: the API can create
connectors that resolve provider files, so anonymous gateway access was a
credential-exfiltration path. `kafka_net` peers (including Kafbat) still reach
port 8083 directly without authentication; that internal path is a recorded gap.

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

### Change data capture (`cdc`)

`cdc` selects the broker, Schema Registry, Connect, `mng-pg` and
`debezium-db-provision`. The job runs the feature SQL in
[`connect/debezium/provisioning/mng-pg.sql`](../../../../../infra/05-messaging/kafka/connect/debezium/provisioning/mng-pg.sql):
a `debezium` login with `REPLICATION` but no superuser, `CONNECT`, `USAGE` and
`SELECT` on the published schema (plus default privileges for later tables), a
`debezium_heartbeat` schema it owns with one `heartbeat` table, and the
publication `hyhome_app_publication` over exactly those two schemas. It never
creates or drops replication slots, and it refuses to alter a role it did not
create (roles carry the comment marker `hy-home:feature:debezium`).

Connect renders `/tmp/connect-secrets/debezium.properties` from the
`debezium_postgres_password` secret on every start (Java-properties escaping,
mode 0600, tmpfs) and restricts `FileConfigProvider` to that directory with
`allowed.paths`. The connector definition
[`postgres-connector.json`](../../../../../infra/05-messaging/kafka/connect/debezium/postgres-connector.json)
references `${file:/tmp/connect-secrets/debezium.properties:password}` and uses
`pgoutput`, slot `hyhome_app_slot` and `publication.autocreate.mode=disabled`.
Because `mng-pg` hosts several databases, WAL written by Keycloak, n8n or Airflow
does not advance a slot on a quiet `app_db`; every 60 seconds the connector's
`heartbeat.action.query` upserts `debezium_heartbeat.heartbeat`, and that change
lets it confirm a newer LSN. This bounds retained WAL only while the connector
runs; a stopped or paused connector still pins WAL up to `max_slot_wal_keep_size`.

These states are distinct and each needs its own evidence:

| State | Evidence |
| --- | --- |
| JSON file exists | Git only; nothing is registered |
| Registered | `GET /connectors/<name>` returns the config |
| Running | `GET /connectors/<name>/status` shows connector and task `RUNNING` |
| Snapshot complete | Connector metrics or log show the initial snapshot finished |
| Changes captured | A test change appears on the `hyhome.app.*` topic |

`mng-pg` declares `wal_level=logical`, `max_replication_slots`,
`max_wal_senders` and `max_slot_wal_keep_size` (2048 MB by default). The
running instance still uses its old command until an approved recreate, which
restarts the management database for Keycloak, n8n, Airflow and others. Once a
slot exists, WAL is retained until the connector confirms it, bounded by
`max_slot_wal_keep_size`; exceeding it invalidates the slot and forces a new
snapshot. Registering the connector, changing it or triggering a snapshot is a
runtime change that needs an approval naming the connector and database.

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
- Runtime authority: `infra/05-messaging/kafka/docker-compose.yml` and the
  [Connect image Dockerfile](../../../../../infra/05-messaging/kafka/Dockerfile.connect).

## Related Documents

- [Operations policy](policy.md)
- [Cluster recovery runbook](runbook.md)
- [Messaging architecture](../../../../02.architecture/descriptions/0005-messaging-architecture.md)
