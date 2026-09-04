---
title: Compose Enablement Model Convergence Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0156
parent_ids: [REQ-0023, REQ-0025, ADR-0026]
created: 2026-08-30
updated: 2026-09-04
---

# Compose Enablement Model Convergence Specification

## Overview

The workspace expresses "which services are part of this stack" three different
ways at once: by commenting entries out of the root `include:` list, by choosing
between a `docker-compose.yml` and a sibling variant, and by Compose
`profiles:`. Only the third is a runtime selector. The first two are static and
invisible to Compose, so no root entry point reaches the 20 stacks the root file
comments out or the 10 files it never names.

This specification converges enablement onto Compose profiles for every file
whose services Compose can hold side by side, and makes the coverage evidence
and the per-profile render prove that convergence.

Six sibling pairs cannot converge this way. `include:` merges files into one
model before any profile is selected, and those six pairs declare the same
service names on both sides, so Compose merges them into one broken service
rather than keeping them as alternatives. Resolving them requires renaming
services or reconciling their settings, which is a different change with a
different risk profile; SPEC-0171 owns it.

## Boundaries and Inputs

**Measured inputs.**

| Fact | Value |
| :--- | :--- |
| Compose files under `infra/` | 47 |
| Referenced by an active root `include:` entry | 17 |
| Referenced only by a commented root `include:` entry | 20 |
| Referenced by no root `include:` entry | 10 |
| Services declared under `infra/` | 168 |
| Services declaring no `profiles:` key | 8 |
| Distinct profile names declared | 24 |
| Services carrying the `core` profile | 8 |
| Services carrying the `dev` profile | 48 |
| Default profile used by validation scripts | `core` |
| Root Compose entry points in the repository | 1 |
| `COMPOSE_FILE` or `COMPOSE_PROFILES` in `.env.example` | absent |
| Sibling pairs sharing service names | 6 |
| Service names declared in two files | 30 |

One of the 47 files carries the `.yaml` extension
(`infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml`), so a glob
written as `docker-compose*.yml` does not reach it. The coverage generator
already matches both extensions; the acceptance commands in this Spec now do
too.

The 10 unreferenced files are not dead. Each is cited by documents and scripts,
and each is a genuine alternate topology or an unrouted service:
`infra/05-messaging/kafka/docker-compose.yml` is a three-broker cluster where
the included `.dev.yml` is a single broker. They are unreachable, not unused.

Four files are unreferenced without sharing service names with a sibling
(`01-gateway/nginx`, `04-data/analytics/warehouses`, `09-tooling/k6`, and the
minio `.yaml` cluster), so profiles alone make them reachable. The remaining six
are the pairs SPEC-0171 owns.

**In scope.** The root `docker-compose.yml`, the `include:` list, profile
naming and its registered vocabulary, the `profiles:` key on services that
declare none,
`scripts/operations/generate-compose-profile-service-coverage.sh` and its
snapshot, `scripts/validation/validate-docker-compose.sh`, the
`HYHOME_COMPOSE_PROFILES` default, host-port collisions this change introduces,
and the stray root file `docker-compose.yml.format`.

**Out of scope.** The six sibling pairs that share service names, which SPEC-0171
owns. Service configuration content, image versions, secrets, network addressing
owned by REQ-0023 operations, and any live runtime mutation. Host-port
collisions that already exist between two actively included files are recorded
as findings, not repaired here, because changing a published port of a running
stack is an outward-facing change beyond this Spec's authority. The operations
catalog domains `00-workspace` and `12-infra-net` have no `infra/` counterpart
by design and are not defects.

## Behavior Contract

1. Membership in the stack is expressed by exactly one mechanism. A reader can
   determine from the root file alone which services exist and which are
   selected.
2. Every Compose file under `infra/` whose service names do not collide with a
   sibling is included unconditionally from the root entry point and selected
   only by profile.
3. Every service under `infra/` declares at least one profile, so selecting no
   profile starts nothing.
4. Every declared profile name has a registered definition stating what it
   selects.
5. The generated profile-coverage snapshot enumerates every service under
   `infra/`, and states for each the profiles that select it.
6. Compose configuration renders without error for every declared profile, not
   only for the validation default.
7. No profile this change makes selectable binds a host port already bound by
   another service the same profile selects.
8. No root-level file scaffolds a service outside the Stage 99 template
   authority.

## Technical Approach

### 1. Single enablement mechanism

Replace commented `include:` entries with unconditional `include:` plus
`profiles:` on any service that declares none. Compose omits a service whose
profile is not selected, so inclusion becomes static and selection becomes a
runtime choice. The 20 commented stacks become included and profile-gated; none
of them starts unless its profile is named.

Every service in those 20 files already declares a profile, so they need only
the include restored. The four unreferenced files that share no service name
with a sibling are included the same way; the four minio cluster services that
declare no profile receive one.

### 2. Host-port exclusivity

Restoring includes makes profile combinations selectable that were previously
unreachable, which can surface a host-port collision. Render the union of every
declared profile, extract the published bindings, and require that no two
services selected by one profile bind the same host port.

Where two services are alternatives by design, the collision is resolved by
keeping their profiles disjoint and recording the exclusivity in the profile
vocabulary. Where they are not alternatives, one host port is reassigned.
A collision between two files that were already both included predates this
change and is recorded as a finding rather than repaired here.

### 3. Profile vocabulary

Fifteen profile names exist without a registered definition. Define the set in
one place, state which names are topology selectors and which are domain
selectors, and make the validation default cover a meaningful stack rather than
the 8 services that currently carry `core`.

### 4. Coverage evidence

`generate-compose-profile-service-coverage.sh` already enumerates services from
the tracked tree rather than from the resolved root configuration, so the
snapshot cannot silently omit an excluded stack; it needs regeneration, not
redesign. The gap is on the render side: `validate-docker-compose.sh` renders
only the default profile, so a profile that fails to render is not observed.
Extend it to render every declared profile and to fail on a host-port collision
within a single profile.

### 5. Root scaffold removal

Delete `docker-compose.yml.format`. It is tracked at the repository root, is not
valid YAML, duplicates two `networks.infra_net` keys, and asserts a service
template outside the Stage 99 template authority. Its useful content is the
logging anchor, which already exists in `infra/common-optimizations.yml`.

## Interfaces and Data

| Interface | Change |
| :--- | :--- |
| `docker-compose.yml` `include:` | commented entries restored; the four non-colliding unreferenced files added |
| `infra/**/docker-compose*.{yml,yaml}` | `profiles:` added to the services that declare none |
| `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md` | new; registers the profile vocabulary |
| `scripts/validation/validate-docker-compose.sh` | renders every declared profile and fails on an in-profile host-port collision |
| `scripts/operations/generate-compose-profile-service-coverage.sh` | unchanged; snapshot regenerated |
| `HYHOME_COMPOSE_PROFILES` | default reviewed against the registered vocabulary |
| `docker-compose.yml.format` | removed |
| `docs/90.references/data/0059-compose-profile-service-coverage/` | regenerated |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Restoring an include starts a service that was intentionally off | Every restored include lands with an explicit `profiles:` on each of its services; the change is proven by `docker compose config` with no profile selected resolving zero services |
| Port collision between a restored stack and an active one | The union of every declared profile is rendered and its published host bindings are compared before the change is committed; `validate-docker-compose.sh` keeps the check |
| Including both halves of a sibling pair merges them into one broken service | The six pairs that share service names are excluded from this Spec and owned by SPEC-0171; the render proves the remaining set merges cleanly |
| Coverage snapshot changes shape and breaks its freshness gate | The snapshot is regenerated in the same logical change and `--check` is recorded |
| Live runtime is mutated | The Spec authorizes configuration rendering only; no `up`, `down`, or restart is in scope |

## Acceptance Contract

1. `grep -c '^  # - infra/' docker-compose.yml` returns 0.
2. Every tracked file matching `infra/**/docker-compose*.yml` or
   `infra/**/docker-compose*.yaml`, except the six SPEC-0171 pair members,
   appears in the root `include:` list.
3. `docker compose config --services` with no profile selected prints nothing.
4. `docker compose config --quiet` succeeds for every declared profile name.
5. No two services selected by one profile publish the same host port, except a
   pair recorded as pre-existing in the Task.
6. Every profile name declared under `infra/` appears in the registered profile
   vocabulary, and the vocabulary names no profile that no service declares.
7. `bash scripts/validation/validate-docker-compose.sh` exits 0 across the
   declared profile set.
8. `bash scripts/operations/generate-compose-profile-service-coverage.sh --check`
   exits 0 and the snapshot lists every service under `infra/`.
9. `git ls-files docker-compose.yml.format` returns nothing.
10. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0.
11. The Task records the rendered-profile evidence and every port finding.

## Traceability

| Upstream | Relation |
| :--- | :--- |
| REQ-0023 | `infra_net` standardization constrains network and inclusion changes |
| REQ-0025 | Operational readiness closure is the need a single enablement model serves |
| ADR-0026 | Standardized `infra_net` decision bounds network handling |
| SPEC-0155 | Supplies the deduplicated generated-evidence rules the coverage snapshot follows |

| Downstream | Relation |
| :--- | :--- |
| SPEC-0171 | Owns the six sibling pairs whose shared service names `include:` cannot hold side by side |
| POL-0078 | Registers the profile vocabulary this Spec requires every declared name to have |

## Related Documents

- [Infrastructure operational policy](../../00.agent-governance/policies/environment-constraints.md)
- [Operations catalog](../../05.operations/catalog/README.md)
- [Infra net standardization](../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- [Compose profile service coverage](../../90.references/data/0059-compose-profile-service-coverage/README.md)
