---
title: "Pact Broker Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0093"
parent_ids:
- "POL-0093"
implementation_services:
  infra/09-tooling/pact-broker/docker-compose.yml:
  - pact-broker
  - pact-broker-db-provision
created: "2026-09-23"
---

# Pact Broker Usage Guide

## Usage

### Purpose and classification

The Pact Broker is an OPTIONAL contract store selected by `contract-testing`.
Consumer tests publish pacts to it, provider builds fetch and verify them, and
`can-i-deploy` answers from the recorded verification results. It complements
WireMock, which stubs a dependency without checking the stub against the real
provider.

### Current implementation

- [Pact Broker Compose](../../../infra/09-tooling/pact-broker/docker-compose.yml)
  defines `pact-broker-db-provision`, which creates the feature-owned role and
  database on `mng-pg`, and `pact-broker`.
- The broker stores pacts, versions, tags and verification results in the
  `PACT_BROKER_DB_NAME` database owned by `PACT_BROKER_DB_USER`. The container
  keeps nothing on disk and runs with a read-only root filesystem.
- Basic auth protects the UI and the whole API; only
  `/diagnostic/status/heartbeat` is public, for the healthcheck. The image reads
  credentials only from the environment, so the service entrypoint exports both
  passwords from Docker secrets into the broker process.
- The host port `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}` is loopback-only;
  basic auth over plain HTTP must not leave the host. No Traefik route or OIDC
  client exists.
- `PACT_DO_NOT_TRACK` disables the image's analytics ping.

### Publishing and verifying

| Command | Effect |
| --- | --- |
| `docker compose --profile core --profile contract-testing up -d pact-broker` | Provisions the database and starts the broker |
| `curl -s http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}/diagnostic/status/heartbeat` | Liveness without credentials |
| `pact-broker publish <dir> --consumer-app-version <sha> --broker-base-url http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292} --broker-username ${PACT_BROKER_BASIC_AUTH_USERNAME:-pact} --broker-password <secret>` | Records pacts for a consumer version |
| `pact-broker can-i-deploy --pacticipant <name> --version <sha> …` | Reads verification results; writes nothing |

The credential is the `pact_broker_basic_auth_password` secret. Pass it through
the client's environment (`PACT_BROKER_PASSWORD`), not the command line.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=contract-testing bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`

## Runbook Handoff

Use the [runbook](../runbooks/0093-pact-broker.md) for provisioning failure, an unhealthy broker,
authentication errors and credential rotation.

## Traceability

- [Policy](../policies/0093-pact-broker.md) (`POL-0093`)
- [Runbook](../runbooks/0093-pact-broker.md) (`RUN-0093`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Pact Broker package README](../../../infra/09-tooling/pact-broker/README.md) and [derived version projection](../../../infra/tech-stack.versions.json)
- [WireMock guide](0092-wiremock.md)
- [Pact Broker Docker configuration](https://docs.pact.io/pact_broker/docker_images/pactfoundation)
