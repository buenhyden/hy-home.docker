---
title: "WireMock Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0092"
parent_ids:
- "POL-0092"
implementation_services:
  infra/09-tooling/wiremock/docker-compose.yml:
  - wiremock
created: "2026-09-23"
---

# WireMock Usage Guide

## Usage

### Purpose and classification

WireMock is an OPTIONAL HTTP stub server selected only by `api-mock`. It stands
in for an external HTTP dependency during development and tests, so a consumer
can be exercised without calling the real service. It holds no primary data and
has no web UI, so no route or OIDC client exists or is needed.

### Current implementation

- [WireMock Compose](../../../infra/09-tooling/wiremock/docker-compose.yml)
  defines one service on the project default network. The host reaches it at
  `http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}`; containers on that network
  reach `http://wiremock:8080` and so hold full admin rights.
- Stubs are the JSON files in `infra/09-tooling/wiremock/mappings/`, mounted
  read-only. The tracked `hyhome-ping.json` answers `GET /hyhome/ping` and exists
  to prove that mappings load.
- The admin API under `/__admin` has no authentication. It can add, reset and
  list stubs and read the request journal. The host port is bound to loopback
  only; on the container side the project default network is the trust boundary. Stubs added through it live in memory and vanish on restart.
- The request journal is capped at 1000 entries so a long test run cannot grow
  the JVM past the template memory limit.

### Adding a stub

Add a mapping file under `mappings/`, then restart the service or call
`POST /__admin/mappings/reset`, which reloads the files. Keep stub bodies
synthetic: a mapping is a tracked file, so it must not contain a real response
captured from a production system, a token or personal data.

| Command | Effect |
| --- | --- |
| `docker compose --profile api-mock up -d wiremock` | Starts the stub server |
| `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/health` | Health, version and uptime |
| `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/requests` | Requests received since start |
| `curl -s -X POST http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/mappings/reset` | Reloads the tracked mappings and drops in-memory ones |

## Common Checks

- `HYHOME_COMPOSE_PROFILES=api-mock bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/check-operations-catalog.py`

## Runbook Handoff

Use the [runbook](../runbooks/0092-wiremock.md) when the service is unhealthy, a stub does not
match, or the memory limit is reached.

## Traceability

- [Policy](../policies/0092-wiremock.md) (`POL-0092`)
- [Runbook](../runbooks/0092-wiremock.md) (`RUN-0092`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [WireMock package README](../../../infra/09-tooling/wiremock/README.md) and [derived version projection](../../../infra/tech-stack.versions.json)
- [WireMock stubbing reference](https://wiremock.org/docs/stubbing/)
- [WireMock standalone Docker](https://wiremock.org/docs/standalone/docker/)
