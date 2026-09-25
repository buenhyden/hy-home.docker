---
title: "Valkey Cluster Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0022"
parent_ids:
- "POL-0022"
implementation_services:
  infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml:
  - 'valkey-cluster-exporter'
  - 'valkey-cluster-init'
  - 'valkey-node-0'
  - 'valkey-node-1'
  - 'valkey-node-2'
  - 'valkey-node-3'
  - 'valkey-node-4'
  - 'valkey-node-5'
created: "2026-05-10"
---

# Valkey Cluster Usage Guide

## Usage

This package describes the optional six-node Valkey Cluster laboratory. M0021
classifies every service as **LAB** because all nodes share one Docker host. It is
not the HOME workflow broker; Airflow and n8n use `mng-valkey` by default.

### Current implementation

The root Compose project includes
[`infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`](../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml).
The only selector is `valkey-cluster`. It starts `valkey-node-0` through
`valkey-node-5`, the one-shot `valkey-cluster-init`, and
`valkey-cluster-exporter`. The initializer forms three primaries and three
replicas on `lab_net`.

Each node owns one bind-backed volume, `valkey0-data` through `valkey5-data`,
resolved under `${DEFAULT_DATA_DIR}/valkey/data-0` through `data-5`. Nodes publish
client ports 6379–6384 and expose cluster-bus ports 16379–16384. The shared
`service_valkey_password` Docker secret is read by the startup, init and exporter
paths. The tracked configuration enables both periodic RDB snapshots and AOF with
`appendfsync everysec`; `/data/nodes.conf` is node-local cluster identity.
Resource limits and health checks come from the shared Compose templates and must
be inspected in rendered root configuration before selection.

### Images, configuration and resource controls

The Compose file is authoritative for the pinned `valkey/valkey` and
`oliver006/redis_exporter` images; repository Renovate configuration may propose
updates and `infra/tech-stack.versions.json` is derived drift evidence. `PORT` and
`NODE_NAME` configure nodes, while root `VALKEY*_PORT`, `VALKEY*_BUS_PORT` and
`VALKEY_EXPORTER_PORT` keys control exposure. Nodes extend
`template-stateful-med`, init `template-job-low`, and exporter
`template-infra-readonly-low`; each declares a health check except the one-shot
initializer. Clients flow directly to cluster-aware node endpoints and the
exporter observes all six nodes.

### Static preflight and normal use

Run from the repository root; do not render the leaf file alone because shared
networks, secrets and `extends` paths are root-owned.

```bash
docker compose --env-file .env.example --profile valkey-cluster config --quiet
docker compose --env-file .env.example --profile valkey-cluster config --services
```

Starting the profile, writing test keys, changing membership or stopping nodes is
a runtime action and needs a separately approved task. When selected, record
cluster-aware client compatibility, intended dataset, retention, capacity and the
fact that same-host replicas do not protect against host loss.

### Backup, restore and upgrade boundary

Use [RUN-0022](../runbooks/0022-valkey-cluster.md). A usable backup must contain a coordinated persistence
set from every primary (and any intentionally retained replica), the complete
multi-part AOF directory and manifest when AOF is used, RDB checkpoints, engine
version, slot ownership and checksums. Never mix files from different points in
time or treat `nodes.conf` as portable identity.

Restore is rehearsed on an isolated compatible six-node target. Recreate cluster
identity, restore complete persistence sets, validate all slots and replica links,
and compare key counts/application reads before any cutover. Upgrades use a
separate plan with release notes, client compatibility and rollback; no in-place
major jump is authorized by this guide.

### Security and license

The password secret does not provide transport encryption. Published host ports
and cluster-bus reachability must be restricted to the intended trusted host and
network; Valkey's own guidance warns that Cluster is designed for trusted
networks. Valkey uses the BSD 3-Clause license; clients and images retain their
own licenses.

### Official references

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial and security boundary](https://valkey.io/topics/cluster-tutorial/)
- [Valkey security](https://valkey.io/topics/security/)
- [Valkey license](https://github.com/valkey-io/valkey/blob/unstable/COPYING)

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0022`; governing policy: `POL-0022`.
- Runtime authority: `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`.

## Related Documents

- [Operations policy](../policies/0022-valkey-cluster.md)
- [Health and recovery runbook](../runbooks/0022-valkey-cluster.md)
- [Data backup policy](../policies/0021-backup-and-restore.md)
