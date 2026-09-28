---
title: "04-Data Hardening Gate and Staged Expansion"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0040"
parent_ids:
- "AD-0019"
supersedes:
- "ADR-0019"
created: "2026-09-24"
---

# ADR-0040: 04-Data Hardening Gate and Staged Expansion

## Context

ADR-0019 decided to apply the immediate hardening items of the `04-data` layer
first, and to introduce HA, lifecycle, and backup/recovery expansion
gradually through policy and procedure. Among the immediate items,
normalizing the `ksql` tier label no longer has a target because ksqlDB was
removed in SPEC-0180 S19 (ADR-0039). The remaining decisions stay valid, so
this ADR rewrites the same decisions against the current services.

04-data consists of several engines, so changing them all at once has a large
blast radius. An automated validation gate is therefore needed to prevent
regressions.

## Decision

- Implement immediate hardening items as Compose contracts and protect them
  with a gate.
  - `supabase` core service healthcheck contract.
  - Normalize the `valkey-cluster-exporter` secret path to
    `service_valkey_password`.
  - Ban malformed expose tokens in `seaweedfs`.
  - `scripts/hardening/check-all-hardening.sh 04-data` and the CI
    `infrastructure-hardening` gate.
- New 04-data services (for example, SPEC-0180's lakehouse engines) add their
  own checks to the same gate.
- Manage expansions such as HA, lifecycle, and backup/recovery drills through
  the approved transition procedure in policy and runbooks.
- Keep the `template-stateful-*` and `template-infra-*` inheritance model.

## Consequences

- **Positive**:
  - Catches 04-data configuration regressions early in CI.
  - Expansion work is tied to operations policy, making priority clear.
- **Trade-offs**:
  - Healthchecks start from liveness; readiness refinement is a later stage.
  - Per-engine performance and HA improvements must happen incrementally.

### Explicit Non-goals

- Large-scale HA topology restructuring for each engine.
- Business query optimization and schema refactoring.
- Migration to cloud-managed services.

## Options Considered

### Expand all 04-data services to an HA standard at once

- **Good**: Can raise availability quickly.
- **Bad**: Large change radius makes it hard to isolate regression causes.

### Update only documentation and defer Compose and CI changes

- **Good**: Low short-term change risk.
- **Bad**: Does not prevent actual operational regressions.

## Traceability

The basis is `check-all-hardening.sh`'s 04-data checks, the CI
`infrastructure-hardening` gate, and the current repository configuration.
Unrecorded runtime state is not claimed.

## Related Documents

- **Superseded ADR**: `ADR-0019` (preserved under `docs/98.archive/superseded/`)
- **Architecture Description**: [0019-data-optimization-hardening-architecture.md](../descriptions/0019-data-optimization-hardening-architecture.md)
- **Requirements**: [0004-data.md](../../01.requirements/0004-data.md)
- **Related ADR**: [ADR-0004](0004-postgresql-ha-patroni.md), [ADR-0039](0039-analytics-engines-after-lakehouse-convergence.md)
