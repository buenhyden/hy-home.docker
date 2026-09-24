---
title: "Kafka Messaging"
version: "1.1.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-24"
created: "2025-11-12"
---

# Kafka

## Overview

This package defines the repository's Kafka-family messaging surface.

## Audience

It is intended for operators and maintainers of Kafka and its companion services.

## Scope

[`docker-compose.yml`](docker-compose.yml) defines `kafka-1`, `kafka-2`,
`kafka-3`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`,
`kafka-exporter`, `kafka-init` and `debezium-db-provision`. Root selectors include
`messaging`, `messaging-broker`, `messaging-cluster`, `messaging-schema`,
`messaging-connect`, `messaging-rest`, `messaging-admin` and `cdc`; brokers 2
and 3 belong only to `messaging-cluster`. `cdc` selects the broker, Schema Registry,
Connect and the CDC source provisioning job.

Connect is built from [`Dockerfile.connect`](Dockerfile.connect) with the Debezium
PostgreSQL plugin. [`connect/render-connect-secrets.sh`](connect/render-connect-secrets.sh)
renders the `FileConfigProvider` input from the `debezium_postgres_password`
secret on every start, restricted by `allowed.paths`. The connector definition
([`postgres-connector.json`](connect/debezium/postgres-connector.json)) and feature SQL
([`provisioning/mng-pg.sql`](connect/debezium/provisioning/mng-pg.sql)) live under `connect/debezium/`; the JSON is
not registered automatically.

## Structure

Broker and Connect state use separate bind-backed volumes under
`${DEFAULT_MESSAGE_BROKER_DIR}/kafka`. Services join `kafka_net`, and the routed ones also join `edge_net`. Broker, controller and published broker/JMX listeners are PLAINTEXT; no broker
TLS/client auth is declared. Schema Registry, Connect, REST and Kafbat HTTP ports
remain internal and selected routes use Traefik. Brokers, Schema Registry, Connect,
REST, Kafbat and exporter declare role-specific health checks; init is a one-shot
job. [`jmx-exporter/kafka-config.yaml`](jmx-exporter/kafka-config.yaml) and the OIDC
template are the mounted configuration sources.

Kafbat renders [`kafbat-ui/dynamic_config.template.yaml`](kafbat-ui/dynamic_config.template.yaml)
into tmpfs, reads `kafbat_client_secret`, trusts the local CA, and uses native
Keycloak OIDC plus `/admins` and `/users` RBAC. Its Traefik route uses
`gateway-standard-chain@file`; no forwarding-auth chain belongs on the route.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
docker compose --env-file .env.example --profile messaging-cluster config --quiet
```

The init job creates two topics at replication factor 3, so valid bootstrap needs
three healthy brokers. Do not assume the single-broker `messaging` selector can
complete initialization.

Recovery must include topic records/configs, partitions, consumer offsets, KRaft
metadata, Schema Registry history/IDs, Connect definitions and internal state.
Restore through approved replay/replication to a fresh isolated cluster; do not
reuse live KRaft identity or piecewise broker directories.

## Related Documents

Use the [documentation entry point](../../../docs/README.md) to locate Stage 05
subject `05-messaging/0036-kafka` and hardening subject 0037. Official sources:
[Kafka operations](https://kafka.apache.org/documentation/#operations),
[Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html),
and [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control).
