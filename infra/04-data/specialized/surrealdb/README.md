---
title: "SurrealDB Implementation"
version: "0.2.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
---

# SurrealDB

## Overview

Persistent database for Open Notebook. The entrypoint fixes the internal listener at 8000 and reads a Docker Secret for authentication.

Lifecycle: **OPTIONAL**. Root Compose includes this definition; explicit profiles control activation.

## Audience

Operators and developers reviewing implementation, configuration and validation.

## Scope

Local service definitions and implementation navigation. Operational controls and recovery belong to `OPS-0080` in the operations catalog, reached through the [documentation index](../../../../docs/README.md).

## Structure

- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)
- [docker-entrypoint.sh](docker-entrypoint.sh)

## Tech Stack

Runtime pins belong to [Compose](docker-compose.yml) and its referenced build sources. The [derived Compose image projection](../../../../infra/tech-stack.versions.json) is a curated projection, not a deployment manifest.

## Configuration

| Service | Profiles | Networks | Host ports | Secret references |
| --- | --- | --- | --- | --- |
| `surrealdb` | `admin, notebook, surrealdb` | `infra_net` | `127.0.0.1:${SURREALDB_HOST_PORT:-8000}:8000` | surreal_db_password |

Persistence:

- `surrealdb-data`: `${DEFAULT_MANAGEMENT_DIR}/surrealdb/data`

Environment key names and defaults are declared in Compose and the [public environment example](../../../../.env.example). Mount grants and healthcheck commands in Compose describe the implementation; a passing config check does not prove runtime readiness. Do not print private environment values, credential files or raw rendered configuration.

## Validation

Classification is `OPTIONAL`; exact profiles are `surrealdb`, `notebook`, and `admin`. Recovery exports an explicitly named namespace/database with the appropriate auth scope and imports into a fresh compatible target. Because import can partially apply, any failed target is discarded and recreated empty. Owning artifacts are `GDE-0080`, `POL-0080`, and `RUN-0080`.

From the repository root, select the documented profiles and use `scripts/validation/validate-docker-compose.sh`. Use the owning operations Runbook for targeted runtime checks and recovery after approval. Stop on missing mounts, unexpected exposure or failed initialization.

## How to Work in This Area

Keep Compose, build sources, public environment keys and secret references consistent. Review gateway authentication, persistence, resource budgets and version exceptions before changing them. Update the existing operations subject instead of duplicating commands here.

## Related Documents

- [Infrastructure index](../../../../infra/README.md)
- [Documentation index](../../../../docs/README.md)
- [Public secret contract](../../../../secrets/README.md)
