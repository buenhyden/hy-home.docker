---
title: "SurrealDB Implementation"
version: "0.2.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
---

# SurrealDB Implementation

> Custom SurrealDB build context and storage engine for Open Notebook.

## Overview

This directory provides the custom container build context and runtime entrypoint for SurrealDB, serving as the dedicated persistence database for Open Notebook.

Open Notebook upstream strictly supports SurrealDB v2 only. The Dockerfile base image is explicitly pinned to SurrealDB v2, as SurrealDB v3 introduces breaking query and protocol incompatibilities with Open Notebook.

## Audience

- **Operators**: Managing database persistence, versions, and credential custody.
- **Developers**: Extending database schemas or debugging query connectivity.
- **AI Agents**: Discovering image build boundaries and version compatibility rules.

## Scope

### In Scope

- Multi-stage image build context (`Dockerfile`) pinning the `surrealdb/surrealdb:v2` base image.
- Secret-aware container entrypoint (`docker-entrypoint.sh`) reading `surreal_db_password` from Docker secrets.
- Version boundary enforcement for Open Notebook storage compatibility.

### Out of Scope

- Standalone SurrealDB cluster clustering or high availability.
- Application-level Open Notebook schemas and user data.

## Structure

```text
surrealdb/
├── Dockerfile            # Multi-stage build pinning surrealdb:v2
├── docker-entrypoint.sh  # Secret-aware entrypoint script
└── README.md             # This file
```

- [Dockerfile](Dockerfile)
- [docker-entrypoint.sh](docker-entrypoint.sh)
- [docker-compose.yml](../docker-compose.yml)

## Tech Stack

Runtime image pins are declared in [Dockerfile](Dockerfile) and [Compose](../docker-compose.yml). The [version registry](../../../tech-stack.versions.json) is a derived Compose image projection.

| Component | Source | Target Version | Notes |
| --- | --- | --- | --- |
| `surrealdb` | [Dockerfile](Dockerfile) | SurrealDB v2 | Base image pinned to `surrealdb/surrealdb:v2` for Open Notebook compatibility |

## Configuration

### Version Compatibility

Open Notebook upstream only supports SurrealDB v2. Upgrading this service to SurrealDB v3 or higher is strictly prohibited until Open Notebook officially provides v3 compatibility.

### Authentication & Entrypoint

The entrypoint script reads authentication credentials directly from `/run/secrets/surreal_db_password` and starts SurrealDB with:

- Internal listen endpoint: `0.0.0.0:8000`
- User: `${SURREALDB_USERNAME}`
- Storage engine: `surrealkv:/mydata/open_notebook.db`

## How to Work in This Area

1. Review [Dockerfile](Dockerfile) and [docker-entrypoint.sh](docker-entrypoint.sh) before proposing image changes.
2. Validate the Compose build with `docker compose --profile notebook build surrealdb`.
3. Do not bump the base image to `v3` without verified upstream Open Notebook support.
4. Ensure credentials are never hardcoded in scripts or environment files.

## Validation

- Build the custom image: `docker compose -f ../docker-compose.yml build surrealdb`.
- Validate container healthcheck: `/usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`.
- Verify database compatibility with Open Notebook by checking that `open_notebook` container establishes its RPC connection successfully.

## Troubleshooting

- **SurrealDB v3 Incompatibility**: If `open_notebook` fails to connect or execute queries after an image rebuild, verify that the base image was not upgraded to SurrealDB v3.
- **Secret File Missing**: Ensure `surreal_db_password` is declared in Compose and mounted to `/run/secrets/surreal_db_password`.

## Related Documents

- [Open Notebook README](../README.md)
- [Documentation index](../../../../docs/README.md)
- [Infrastructure index](../../../README.md)

Runtime pins are owned by the Compose/Dockerfile declarations; the [derived Compose image projection](../../../tech-stack.versions.json) provides drift verification.
