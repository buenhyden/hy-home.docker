---
title: "11-laboratory - Management & Laboratory Tier"
version: "1.1.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
created: "2026-03-26"
---

# 11-laboratory - Management & Laboratory Tier

## Overview

This tier contains optional administrative tools. The root project includes the
five leaves, while profiles select services:

| Service | Profiles | Authority and risk |
| --- | --- | --- |
| `dozzle` | `admin`, `admin-logs` | Docker logs; read-only socket still grants powerful Docker API visibility |
| `redisinsight` | `admin`, `admin-data` | local connection/settings database; target Redis/Valkey data remains external |
| `open_notebook` | `notebook` | application data/provider credentials plus encryption-key custody; app password and admin CIDR, no shared SSO |
| `surrealdb` | `notebook`, `surrealdb` | co-located Open Notebook database under `open-notebook/surrealdb/` |
| `mlflow`, `mlflow-db-provision`, `mlflow-artifact-provision` | `mlops`, `data-science` | tracking database on `mng-pg` and bucket-scoped MinIO artifacts; SDK path on `infra_net` is unauthenticated |
| `jupyterlab` | `data-science` | single-user code execution with a mandatory server token; not JupyterHub |

There is no `dev` profile for these services. Dozzle and RedisInsight can run
without Open Notebook. Selecting `notebook` brings both Open Notebook and its
SurrealDB dependency through the root project.

## Audience

Infrastructure administrators, laboratory users, security reviewers, and
documentation agents responsible for optional admin-tool boundaries.

## Scope

This tier owns the Dozzle, RedisInsight, Open Notebook (with its co-located
SurrealDB), MLflow and JupyterLab declarations and their access/persistence
contracts. `admin` selects only Dozzle and RedisInsight.
It does not own target Redis/Valkey data, copied Docker logs, provider accounts,
production notebook workloads, or Metabase.

## Structure

```text
11-laboratory/
├── dozzle/
├── open-notebook/
├── redisinsight/
└── README.md
```

## Configuration

All three UIs use Traefik routes with the tracked gateway/allowlist/ForwardAuth
controls. Dozzle also has native OIDC configuration; its Docker socket remains a
host-security boundary. Dozzle `/data` stores settings, not copied container logs.
RedisInsight `/data` stores sensitive connection metadata and currently lacks a
tracked `RI_ENCRYPTION_KEY`. Open Notebook `/app/data`, SurrealDB `/mydata`, and
the Open Notebook encryption key form one recovery set; losing the key can make
stored provider secrets unreadable. Target Redis/Valkey backup is owned by the
target data service.

## How to Work in This Area

Use the [documentation index](../../docs/README.md), then exact Stage 05 subjects
`0072-dozzle`, `0073-open-notebook`, and `0076-redisinsight` under
`docs/05.operations/catalog/11-laboratory/`. Run from the repository root:

```bash
HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 11-laboratory
```

Static validation is not runtime access, Docker API safety, provider egress, or
restore evidence. Compose/Dockerfile declarations own runtime pins;
[tech-stack.versions.json](../tech-stack.versions.json) is a derived image projection.

## Related Documents

- [Documentation index](../../docs/README.md)
- [Infrastructure index](../README.md)
- Stage 05 laboratory package: `docs/05.operations/catalog/11-laboratory/README.md`
