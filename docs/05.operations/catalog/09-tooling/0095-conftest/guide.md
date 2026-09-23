---
title: "Conftest Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0095"
parent_ids:
- "POL-0095"
implementation_services:
  infra/09-tooling/conftest/docker-compose.yml:
  - conftest
created: "2026-09-23"
---

# Conftest Usage Guide

## Usage

### Purpose and classification

Conftest is an OPTIONAL one-shot policy test selected by `policy-check`. It
evaluates Open Policy Agent (Rego) rules against the infrastructure source, not
against running containers, so it catches a bad declaration before any start.

### Current implementation

- [Conftest Compose](../../../../../infra/09-tooling/conftest/docker-compose.yml)
  runs the pinned `openpolicyagent/conftest` image as UID 1000 with a read-only
  root, no network, and only `infra/` mounted read-only. It never sees
  `secrets/` or `.env`.
- `run.sh` first runs `conftest verify` on the policies' own tests, then tests
  every `docker-compose*.yml` and every `Dockerfile*` under `infra/`. A `deny`
  fails the job; a `warn` is printed only.

### Rules

| Namespace | Deny | Warn |
| --- | --- | --- |
| `compose` | privileged service outside the allowlist (`cadvisor`); service without a profile; image `:latest` or untagged; a password, secret, token or key variable with a literal value | host port published on all interfaces |
| `dockerfile` | `FROM` untagged or `:latest` (build stages and `scratch` excepted); `ADD` from a URL without `--checksum` | — |

A literal means anything except empty, `${…}` interpolation, a
`/run/secrets/` path, a boolean or a URL; `*_FILE` and `*_CMD` keys name a
secret's source and are exempt.

### Commands

| Command | Effect |
| --- | --- |
| `docker compose --profile policy-check run --rm conftest` | Verify the policies, then test all Compose files and Dockerfiles |
| `docker run --rm -v "$PWD/infra:/project/infra:ro" -w /project openpolicyagent/conftest:<tag> test --policy infra/09-tooling/conftest/policy --namespace compose <file>` | Test one file |

## Common Checks

- CI runs the job as `leaf.conftest-policy` (`scripts/validation/check-conftest-policy.sh`) in the `repository-integrity` suite.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`

## Runbook Handoff

Use the [runbook](runbook.md) when the job fails.

## Traceability

- [Policy](policy.md) (`POL-0095`)
- [Runbook](runbook.md) (`RUN-0095`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Conftest package README](../../../../../infra/09-tooling/conftest/README.md)
- [Conftest documentation](https://www.conftest.dev/)
- [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-language/)
