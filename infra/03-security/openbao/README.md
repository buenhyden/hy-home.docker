---
title: "OpenBao Implementation"
version: "0.1.1"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
---

# OpenBao

## Overview

The secret control plane uses Raft storage and an AppRole Agent. It is a bootstrap dependency; sealed-container health is not secret-delivery readiness.

Lifecycle: **HOME**. Root Compose includes this definition; explicit profiles control activation.

## Audience

Operators and developers reviewing implementation, configuration and validation.

## Scope

Local service definitions and implementation navigation. Operational controls and recovery belong to `OPS-0085` in the operations catalog, reached through the [documentation index](../../../docs/README.md).

## Structure

- `config/`: [Agent configuration](config/agent.hcl) and template sources
- [docker-compose.yml](docker-compose.yml)

## Tech Stack

Runtime pins belong to [Compose](docker-compose.yml) and its referenced build sources. The [version registry](../../../infra/tech-stack.versions.json) is a derived Compose image projection, not a deployment manifest.

## Configuration

| Service | Profiles | Networks | `edge_net`, `obs_net`, `secrets_net` | Secret references |
| --- | --- | --- | --- | --- |
| `openbao` | `security, secrets, core, local, dev` | `secrets_net, edge_net, obs_net` | `No host publication` | No Compose Secret grant; inspect configured bootstrap file metadata |
| `openbao-agent` | `security, secrets, core, local, dev` | `secrets_net` | `No host publication` | No Compose Secret grant; inspect configured bootstrap file metadata |

Persistence:

- `openbao-data`: `${DEFAULT_SECURITY_DIR}/openbao/data`
- `openbao-agent-data`: `${DEFAULT_SECURITY_DIR}/openbao/agent`
- `openbao-agent-out`: `${DEFAULT_SECURITY_DIR}/openbao/out`

Environment key names and defaults are declared in Compose and the [public environment example](../../../.env.example). Mount grants and healthcheck commands in Compose describe the implementation; a passing config check does not prove runtime readiness. Do not print private environment values, credential files or raw rendered configuration.

## Validation

From the repository root, select the documented profiles and use `scripts/validation/validate-docker-compose.sh`. Use the owning operations Runbook for targeted runtime checks and recovery after approval. Stop on missing mounts, unexpected exposure or failed initialization.

## How to Work in This Area

Keep Compose, build sources, public environment keys and secret references consistent. Review gateway authentication, persistence, resource budgets and version exceptions before changing them. Update the existing operations subject instead of duplicating commands here.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [Public secret contract](../../../secrets/README.md)
