---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md -->

# Reference: Docker Compose and Infrastructure Harness

## Overview

This reference analyzes Docker Compose and infrastructure as part of the
`hy-home.docker` workspace harness. It compares official Docker Compose guidance
with repo-local Compose, infra, validation, hardening, network, profile, secret,
and healthcheck boundaries.

## Purpose

Explain how Docker Compose and infrastructure evidence support agentic harness
engineering without replacing runtime configuration, operations procedures, or
active policy.

## Repository Role

This reference supports Stage 00 governance, infra docs, HAFE documents, QA
evidence, and Stage 90 research. It does not define runtime Compose behavior,
deployment procedure, service ownership, secret values, or operations runbooks.

## Scope

### In Scope

- Compose project, service, profile, network, volume, secret, and healthcheck
  concepts
- Repo-local infrastructure evidence and validation scripts
- Infrastructure harness follow-up gaps

### Out of Scope

- Runtime Compose edits
- Secret values or generated secret files
- Deployment execution
- Active operations runbooks or service procedures

## Definitions / Facts

- **Compose project**: Docker Compose treats an application as a set of services
  configured with a Compose file and managed together through the Compose CLI.
- **Compose file**: The Compose file reference defines service, network, volume,
  config, secret, profile, and healthcheck syntax that can be validated without
  treating a research document as runtime truth.
- **Profiles**: Compose profiles allow optional service groups to be enabled by
  profile name, which maps to the repo-local profile model described in
  `infra/README.md`.
- **Networking**: Compose creates service-name based network reachability inside
  a project network unless the Compose file defines more specific networks.
- **Secrets**: Compose secrets are intended to avoid exposing sensitive data in
  image layers or plaintext environment values. This repository documents secret
  names and paths, not values.
- **Production guidance**: Docker's Compose production guidance is useful
  reference context, but production readiness for this repository still depends
  on repo-local active specs, operations docs, validators, and approvals.

## Analysis

Docker Compose is the runtime harness boundary for this repository. The root
`docker-compose.yml` aggregates service definitions, while `infra/README.md`
classifies root-active, optional, standalone, and variant Compose files. This
lets agents reason about what is part of the active root execution surface
without editing runtime configuration during a research pass.

The infrastructure harness has several evidence classes:

| Evidence Class | Repo-local Surface | Harness Role |
| --- | --- | --- |
| Runtime declaration | `docker-compose.yml`, `infra/**/docker-compose*.yml` | Describes services, profiles, networks, volumes, secrets, and healthchecks. |
| Inventory and rubric | `infra/README.md` | Explains tiering, root-active status, profile model, and service README expectations. |
| Compose rendering | `scripts/validation/validate-docker-compose.sh` | Checks root and profile-aware Compose configuration without starting services. |
| Hardening baseline | `scripts/hardening/check-all-hardening.sh` | Checks selected security and runtime hardening expectations. |
| Harness routing | `docs/00.agent-governance/harness-implementation-map.md` | Maps Compose, secrets, scripts, validation, and evidence paths to canonical sources. |

This is a harness because it gives agents a controlled way to inspect, validate,
and report infrastructure state. It is not a substitute for the Compose files
themselves. When runtime behavior changes, the active source remains the Compose
and infra files, with Stage 01-05 documents providing requirements,
architecture, specs, execution evidence, and operations guidance.

## Potential Follow-up / Gap

- A future active task could add a generated infrastructure inventory report,
  but this reference should not become that generator.
- A future operations pass could align service README rubric coverage for any
  new Compose services discovered after this research pass.
- Compose production guidance should be rechecked before any deployment or
  production-hardening change is approved.

## Source Rules

- Prefer Docker official docs and repo-local canonical files.
- Re-check Docker facts before using them for active runtime decisions.
- Do not document secret values, token-bearing logs, shell history, or full
  generated secret files.

## Sources

- [Docker Compose docs](https://docs.docker.com/compose/) - Compose product and workflow context
- [Compose file reference](https://docs.docker.com/reference/compose-file/) - service, network, volume, profile, secret, and healthcheck syntax context
- [Using profiles with Compose](https://docs.docker.com/compose/how-tos/profiles/) - optional service-group activation model
- [Networking in Compose](https://docs.docker.com/compose/how-tos/networking/) - Compose service networking context
- [Use secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/) - Compose secret handling model
- [Use Compose in production](https://docs.docker.com/compose/how-tos/production/) - production-oriented Compose guidance
- [Root Compose file](../../../../docker-compose.yml) - repo-local root include and profile context
- [Infra README](../../../../infra/README.md) - repo-local infrastructure index, tier model, and service documentation rubric
- [Compose validation script](../../../../scripts/validation/validate-docker-compose.sh) - repo-local Compose validation gate
- [Hardening script](../../../../scripts/hardening/check-all-hardening.sh) - repo-local infrastructure hardening gate
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - repo-local harness surface routing

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Docker Compose guidance, `infra/`, root
  Compose, validation scripts, or hardening checks change
- **Update Trigger**: Update when infrastructure harness assumptions or runtime
  validation boundaries change

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [harness engineering](./harness-engineering.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [HAFE spec](../../../03.specs/094-harness-agent-first-engineering/spec.md)
