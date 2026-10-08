---
title: "LAB Isolation and Service Selection"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0215"
parent_ids:
- "REQ-0004"
- "REQ-0027"
- "AD-0026"
created: "2026-10-08"
---

# LAB Isolation and Service Selection

## Overview

PostgreSQL HA, the Valkey cluster, the three-broker Kafka, the NoSQL replica
sets and Locust already run only from standalone `labs/*.yml` entrypoints.
This package keeps them there, removes the remaining root and HOME coupling,
gives LAB runs a lifecycle with a lease, an exact cleanup scope and a budget
check, and records why each optional service is or is not resident.

## Scope

Included: root closure regression checks, the retired root `lab_net`, LAB
data, network, port, routing and tier boundaries, a LAB controller with a
ledger, the HOME plus LAB budget check, the optional service disposition
ledger, and documents that call a single node HA.

Excluded: resource template values and common exception files (prompt 05),
the Locust worker code (prompt 02, merged), moving or deleting existing LAB
or HOME data, and observing which services run on the HOME host.

## Contracts

1. Root closure. Rendering the root with `--profile '*'` contains no LAB
   service, and targeting a LAB service by name through the root fails. The
   root declares no LAB network, `LAB_` variable or `secrets/labs` path.
2. LAB independence. Each LAB has its own project, container, network and
   loopback port names, keeps all state under the required `LAB_DATA_DIR`
   (MongoDB and the OpenSearch cluster included), and reads secrets only from
   `LAB_SECRET_DIR`. No LAB registers routers or middleware with HOME Traefik.
   Every LAB service carries `hy-home.tier: lab`.
3. Lifecycle. `scripts/operations/lab.py` starts a LAB only with a purpose and
   a finite lease, records a ledger entry naming the project and its cleanup
   targets, stops only that project without deleting volumes or data, and
   stops expired leases on `reap`. Each command exits non-zero on failure.
4. Collision and budget. Before start, the controller refuses a LAB whose
   names, host ports or data paths collide with the rendered root, another
   selected LAB or a running container, whose data root sits inside a HOME
   data path, or whose declared limits plus running containers exceed the
   operator budget, or when more LABs would run than the concurrency limit.
   Declared limits are ceilings, not measurements.
5. Kafka. The HOME broker is one node with replication factor 1 and no fault
   tolerance. The LAB has three brokers with replication factor 3 and
   `min.insync.replicas=2`, which survives one broker loss on the same host
   and is not host HA. Schema Registry stays because Debezium Avro uses it.
6. Disposition. Every optional, DEV and LAB service group has a role, a
   consumer or `none`, a decision and its reason. A service without an
   observed host state is not reported as stopped.
7. Wording. No current document calls a single-node service HA or a cluster.
8. Exceptions. No common exception names a LAB path or service; the result is
   handed to prompt 05.

9. Inventory. Each `labs/<name>.md` names its Compose project and exactly
   the services its entrypoint renders; a test keeps them equal.
10. Cluster identity. A LAB whose `CLUSTER_ID` equals the root's or another
    selected LAB's is refused before start, like a shared name or path.
11. Observability boundary. HOME Prometheus scrapes no LAB container, and no
    LAB joins a root network. A LAB exporter is read only from inside its
    LAB; an exporter without a runnable image or a reader is retired.
12. Selection. No current document, script or unit starts the root with
    every profile. The HOME named selection holds no LAB service and not the
    Nginx alternate gateway, which shares 80/443 with Traefik.
13. Disposition columns. Every optional service group also states its
    declared cost from the rendered root, its retained data and a
    retirement condition.
14. Host residue. Containers, restart policies and systemd or cron launchers
    on the HOME host are read before any cleanup; only exact, confirmed LAB
    or orphan targets are stopped, and data is kept.

## Acceptance Criteria

1. A test renders the root and fails if a LAB service appears or a LAB
   service can be targeted through it; `lab_net` is gone from root and HOME.
2. Tests fail if a LAB lacks a data root, uses HOME Traefik routing, or is not
   tiered `lab`; every LAB still renders with its own inputs.
3. Controller tests cover lease, ledger, project-scoped stop without volume
   removal, reap, collisions between two LABs and with HOME, data roots
   inside HOME paths, budget and concurrency refusal, and exit codes.
4. POL-0078 carries the LAB lifecycle, budget and disposition rules, and the
   documents in contract 7 are corrected.
5. HOME runs, real LAB starts on the HOME host and data moves stay `NOT_RUN`
   unless observed.
6. Tests for contracts 9 to 12 fail against the 0.1.0 source or documents
   and pass now.
7. Each LAB starts on the HOME host through `lab.py` with synthetic inputs,
   reaches its own readiness signal or records why not, and stops without
   leaving containers or networks and without changing the HOME project.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-lab-isolation-and-service-selection.md)
- [Closure and HOME LAB run Task](tasks/tsk-0002-lab-closure-and-home-runs.md)
- [Data requirement](../../01.requirements/0004-data.md)
- [HOME development host requirement](../../01.requirements/0027-home-development-host.md)
- [Profile vocabulary policy](../../05.operations/policies/0078-compose-profile-vocabulary.md)
