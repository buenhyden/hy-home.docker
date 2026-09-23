---
title: "OpenTofu Implementation"
version: "0.1.1"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
---

# OpenTofu

## Overview

Operator-triggered infrastructure CLI. The inline Dockerfile is the source for the tool image; workspace and credential mounts can authorize real remote changes.

Lifecycle: **DEV job**. Root Compose includes this definition; explicit profiles control activation.

## Audience

Operators and developers reviewing implementation, configuration and validation.

## Scope

Local service definitions and implementation navigation. Operational controls and recovery belong to `OPS-0082` in the operations catalog, reached through the [documentation index](../../../docs/README.md).

## Structure

- [docker-compose.yml](docker-compose.yml)

## Tech Stack

Runtime pins belong to [Compose](docker-compose.yml) and its referenced build sources. The [version registry](../../../infra/tech-stack.versions.json) is a derived Compose image projection, not a deployment manifest.

## Configuration

| Service | Profiles | Networks | Host ports | Secret references |
| --- | --- | --- | --- | --- |
| `opentofu` | `iac` | project default | `No host publication` | No Compose Secret grant; inspect configured bootstrap file metadata |

Persistence:

See service bind mounts in Compose; no top-level named volume is declared.

Environment key names and defaults are declared in Compose and the [public environment example](../../../.env.example). Mount grants and healthcheck commands in Compose describe the implementation; a passing config check does not prove runtime readiness. Do not print private environment values, credential files or raw rendered configuration.

## Validation

From the repository root, select the documented profiles and use `scripts/validation/validate-docker-compose.sh`. Use the owning operations Runbook for targeted runtime checks and recovery after approval. Stop on missing mounts, unexpected exposure or failed initialization.

## How to Work in This Area

Keep Compose, build sources, public environment keys and secret references consistent. Review gateway authentication, persistence, resource budgets and version exceptions before changing them. Update the existing operations subject instead of duplicating commands here.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [Public secret contract](../../../secrets/README.md)
