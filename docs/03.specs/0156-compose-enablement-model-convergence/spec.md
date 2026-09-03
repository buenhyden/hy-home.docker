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
updated: 2026-09-02
---

# Compose Enablement Model Convergence Specification

## Overview

The workspace expresses "which services are part of this stack" three different
ways at once: by commenting entries out of the root `include:` list, by choosing
between a `docker-compose.yml` and a `docker-compose.dev.yml` sibling, and by
Compose `profiles:`. Only the third is a runtime selector. The first two are
static and invisible to Compose, so the generated profile-coverage snapshot
cannot see the 20 stacks the root file comments out or the 9 topology variants
it never names.

This specification converges enablement onto one mechanism, makes the
non-default topologies reachable, and makes the generated coverage evidence
describe the whole `infra/` tree rather than the subset the root file happens to
include.

## Boundaries and Inputs

**Measured inputs.**

| Fact | Value |
| :--- | :--- |
| Compose files under `infra/` | 46 |
| Referenced by an active root `include:` entry | 17 |
| Referenced only by a commented root `include:` entry | 20 |
| Referenced by no root `include:` entry | 9 |
| `profiles:` declarations under `infra/` | 147 |
| Distinct profile names declared | 15 |
| Services carrying the `core` profile | 8 |
| Services carrying the `dev` profile | 44 |
| Default profile used by validation scripts | `core` |
| Root Compose entry points in the repository | 1 |
| `COMPOSE_FILE` or `COMPOSE_PROFILES` in `.env.example` | absent |

The 9 unreferenced files are not dead. Each is cited by 25 to 74 documents and
scripts, and each is a genuine alternate topology: `infra/05-messaging/kafka/docker-compose.yml`
is a three-broker cluster where the included `.dev.yml` is a single broker.
They are unreachable, not unused.

**In scope.** The root `docker-compose.yml`, the `include:` list, the
`.dev.yml`/`.yml` sibling pattern under `infra/`, profile naming,
`scripts/operations/generate-compose-profile-service-coverage.sh` and its
snapshot, the `HYHOME_COMPOSE_PROFILES` default, and the stray root file
`docker-compose.yml.format`.

**Out of scope.** Service configuration content, image versions, secrets,
network addressing owned by REQ-0023 operations, and any live runtime mutation.
The operations catalog domains `00-workspace` and `12-infra-net` have no
`infra/` counterpart by design and are not defects.

## Behavior Contract

1. Membership in the stack is expressed by exactly one mechanism. A reader can
   determine from the root file alone which services exist and which are
   selected.
2. Every Compose file under `infra/` is reachable from a root entry point.
3. The generated profile-coverage snapshot enumerates every service under
   `infra/`, and states for each the profiles that select it.
4. Compose configuration renders without error for every declared profile, not
   only for the validation default.
5. No root-level file scaffolds a service outside the Stage 99 template
   authority.

## Technical Approach

### 1. Single enablement mechanism

Replace commented `include:` entries with unconditional `include:` plus
`profiles:` on the services those files declare. Compose omits a service whose
profile is not selected, so inclusion becomes static and selection becomes a
runtime choice. The 20 commented stacks become included and profile-gated; none
of them starts unless its profile is named.

Files whose services already declare profiles need only the include restored.
Files whose services declare none receive a profile named for their operations
domain.

### 2. Topology variants

Resolve each `.yml` and `.dev.yml` sibling pair by making the variant a profile
rather than a file choice, where the two differ only in topology. Where the
divergence is larger than a profile can express, keep both files, include both,
and give them mutually exclusive profiles so that neither is unreachable.

Record the decision per pair in the Task, with the measured difference that
justified it.

### 3. Profile vocabulary

Fifteen profile names exist without a registered definition. Define the set in
one place, state which names are topology selectors and which are domain
selectors, and make the validation default cover a meaningful stack rather than
the 8 services that currently carry `core`.

### 4. Coverage evidence

Change `generate-compose-profile-service-coverage.sh` to enumerate services from
the `infra/` tree rather than from the resolved root configuration, so the
snapshot cannot silently omit an excluded stack. Extend
`validate-docker-compose.sh` to render every declared profile.

### 5. Root scaffold removal

Delete `docker-compose.yml.format`. It is tracked at the repository root, is not
valid YAML, duplicates two `networks.infra_net` keys, and asserts a service
template outside the Stage 99 template authority. Its useful content is the
logging anchor, which already exists in `infra/common-optimizations.yml`.

## Interfaces and Data

| Interface | Change |
| :--- | :--- |
| `docker-compose.yml` `include:` | commented entries restored; unreferenced files added |
| `infra/**/docker-compose*.yml` | `profiles:` added where absent; sibling pairs resolved |
| `scripts/operations/generate-compose-profile-service-coverage.sh` | enumerates the tree, not the resolved config |
| `scripts/validation/validate-docker-compose.sh` | renders every declared profile |
| `HYHOME_COMPOSE_PROFILES` | default reviewed against the defined vocabulary |
| `docker-compose.yml.format` | removed |
| `docs/90.references/data/0059-compose-profile-service-coverage/` | regenerated against the full tree |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Restoring an include starts a service that was intentionally off | Every restored include lands with an explicit `profiles:` on each of its services; the change is proven by `docker compose config` with no profile selected |
| Port or volume collision between a restored stack and an active one | `docker compose config` is rendered per profile and for the union before the change is committed |
| A sibling pair is merged and loses a topology | The Task records the measured difference per pair; merges happen only where the difference is expressible as a profile |
| Coverage snapshot changes shape and breaks its freshness gate | The generator and the snapshot are regenerated in the same logical change |
| Live runtime is mutated | The Spec authorizes configuration rendering only; no `up`, `down`, or restart is in scope |

## Acceptance Contract

1. `grep -c '^  # - infra/' docker-compose.yml` returns 0.
2. Every file matching `infra/**/docker-compose*.yml` appears in the root `include:` list.
3. `docker compose config --quiet` succeeds with no profile selected and starts no service.
4. `docker compose config --quiet` succeeds for every declared profile name.
5. `bash scripts/validation/validate-docker-compose.sh` exits 0 across the declared profile set.
6. `bash scripts/operations/generate-compose-profile-service-coverage.sh --check` exits 0 and the snapshot lists every service under `infra/`.
7. `git ls-files docker-compose.yml.format` returns nothing.
8. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0.
9. The Task records the per-pair topology decision and the rendered-profile evidence.

## Traceability

| Upstream | Relation |
| :--- | :--- |
| REQ-0023 | `infra_net` standardization constrains network and inclusion changes |
| REQ-0025 | Operational readiness closure is the need a single enablement model serves |
| ADR-0026 | Standardized `infra_net` decision bounds network handling |
| SPEC-0155 | Supplies the deduplicated generated-evidence rules the coverage snapshot follows |

## Related Documents

- [Infrastructure operational policy](../../00.agent-governance/policies/environment-constraints.md)
- [Operations catalog](../../05.operations/catalog/README.md)
- [Infra net standardization](../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- [Compose profile service coverage](../../90.references/data/0059-compose-profile-service-coverage/README.md)
