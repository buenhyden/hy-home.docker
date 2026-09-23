---
title: "Valkey Distributed Cluster"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2025-11-20"
---

# Valkey Cluster

## Overview

This package defines the repository's six-node Valkey cluster.

## Audience

It is intended for operators and maintainers of the Valkey LAB deployment.

## Scope

Source: [`docker-compose.yml`](docker-compose.yml). Profile: `valkey-cluster`.
Services: `valkey-node-0` through `valkey-node-5`, one-shot
`valkey-cluster-init`, and `valkey-cluster-exporter`. The initializer creates three
primaries and three replicas on `lab_net`.

## Structure

Each node owns `valkey0-data` through `valkey5-data`, backed by
`${DEFAULT_DATA_DIR}/valkey/data-0` through `data-5`. Client ports 6379–6384 and
cluster-bus ports 16379–16384 are published/exposed. Startup, init and exporter read `service_valkey_password`.
[`config/valkey.conf`](config/valkey.conf),
[`scripts/valkey-start.sh`](./scripts/valkey-start.sh), and
[`scripts/valkey-cluster-init.sh`](./scripts/valkey-cluster-init.sh) own configuration.
Every node has an authenticated `PING` health check, the exporter has an HTTP
health check, and init is a one-shot completion job; `nodes.conf` is node-local
identity.

## How to Work in This Area

From the repository root:

```bash
docker compose --env-file .env.example --profile valkey-cluster config --quiet
docker compose --env-file .env.example --profile valkey-cluster config --services
```

This is a same-host LAB and does not replace HOME `mng-valkey`. Selection needs a
named cluster-aware client. No TLS is declared, so restrict published ports to the
intended trusted boundary.

Backup and restore must coordinate every primary, complete AOF sets/manifests,
RDB checkpoints and slot ownership. Restore on an isolated compatible cluster
with fresh identity; never reuse live `nodes.conf`.

## Related Documents

Use the
[documentation entry point](../../../../docs/README.md) to locate Stage 05 subject
`04-data/0022-valkey-cluster` and POL-0021.

Official sources: [persistence](https://valkey.io/topics/persistence/),
[cluster operations](https://valkey.io/topics/cluster-tutorial/), and
[license](https://github.com/valkey-io/valkey/blob/unstable/COPYING).
