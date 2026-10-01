---
title: "Capability Tiers and Quality Boundary"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "ADR-0046"
parent_ids:
- "AD-0009"
created: "2026-10-01"
---

# ADR-0046: Capability Tiers and Quality Boundary

## Context

Tooling mixed platform operations with software verification, Communication mixed
real mail with test capture, and Laboratory grouped unrelated administration and
research capabilities by activation style. The user approved SPEC-0197 option C
and its additional implementation Plan on2026-10-01. Initial registration uses
proposed status without inventing a prior lifecycle transition.

## Decision Drivers

Use capability ownership, retain cohesive packages and helper jobs, preserve
runtime configuration and persistent data, and keep existing Operations IDs.
Directory placement must not imply activation order or security isolation.

## Options Considered

- A: retain the current directories and clarify navigation only.
- B: move six packages/eight labels into existing capability tiers.
- C: establish a Quality capability and relocate twelve packages/sixteen labels.

## Decision

Adopt C. `11-quality` owns k6, Locust, WireMock, Pact Broker, SonarQube, Conftest
and Mailpit. `09-platform-ops` retains OpenTofu, Terrakube, Registry, Renovate and
Restic. `10-communication` retains Stalwart and its configuration helper.
Move Dozzle to Observability, RedisInsight to Data, Open Notebook with nested
SurrealDB and MLflow with its provisioner to AI, and JupyterLab to Analytics.
Remove the retired Laboratory directory after transferring its useful navigation.

Great Expectations remains Analytics data quality; Quality owns software
verification. Restic remains cross-platform backup orchestration. Shared profile
names, host paths and every service, network and volume identity remain intact.
Only approved source paths, tier labels and Conftest's exact entrypoint script
path change. ADR-0045's storage/processing decision remains unchanged.

The user subsequently approved the Platform Operations naming amendment.
The retained five platform lifecycle packages use09-platform-ops and nine
platform-ops labels; existing Compose profiles, including tooling, remain intact.
The tracked Restic unit source path follows the move; installed-unit refresh
is a separately controlled operational handoff.

## Consequences

Requirements and architecture descriptions retain their issued logical obligations
across the new physical owners. Existing Guide, Policy and Runbook identities
stay stable; active links, hardening dispatch and derived inventories follow the
move. Dozzle keeps a leaf Compose file. A package move grants no new runtime,
profile, authentication exception or deployment permission.

## Traceability

- [AD-0009](../descriptions/0009-tooling-architecture.md)
- [AD-0011](../descriptions/0011-laboratory-architecture.md)
- [SPEC-0197](../../03.specs/0197-infra-tier-layout/spec.md)
- [SPEC-0198](../../03.specs/0198-operations-documentation-system/spec.md)

## Compliance

Require exact before/after public-model comparison, source-content preservation,
retained hardening controls and negative regressions, current document contracts,
and independent read-only review. Record actual outcomes in the existing Tasks.

## Follow-up

Future container recreation must account for relocated source mounts. Runtime,
image builds, deployment and data recovery need separately scoped authorization;
static source acceptance does not prove their success.
