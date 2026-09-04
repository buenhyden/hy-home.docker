---
title: Compose Sibling Pair Resolution Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: draft
owner: "@buenhyden"
artifact_id: SPEC-0171
parent_ids: [REQ-0023, REQ-0025, ADR-0026]
created: 2026-09-04
updated: 2026-09-04
---

# Compose Sibling Pair Resolution Specification

## Overview

Six directories under `infra/` hold two Compose files that declare the same
service names. Each pair expresses one topology twice: a development variant and
a fuller variant. Only one member of each pair is reachable from the root entry
point, so the other topology cannot be selected at all.

SPEC-0156 converged every other file onto Compose profiles by including it
unconditionally and gating it behind a profile. That mechanism cannot resolve
these six. `include:` merges files into a single model before any profile is
evaluated, so including both members produces one merged service rather than two
alternatives. The merge is not merely wrong, it is invalid: rendering all
members together fails with
`services.airflow-triggerer.security_opt items at 0 and 1 are equal`.

This specification resolves the six pairs so that both topologies become
selectable without a broken merge.

## Boundaries and Inputs

**Measured inputs.**

| Directory | Shared service names | Only in the fuller member | Differing keys on shared services |
| :--- | ---: | :--- | ---: |
| `infra/06-observability` | 9 | none | 11 |
| `infra/07-workflow/airflow` | 8 | `airflow-valkey`, `airflow-valkey-exporter` | 28 |
| `infra/05-messaging/kafka` | 7 | `kafka-2`, `kafka-3` | 20 |
| `infra/07-workflow/n8n` | 4 | `n8n-valkey`, `n8n-valkey-exporter` | 10 |
| `infra/02-auth/oauth2-proxy` | 1 | `oauth2-proxy-valkey`, `oauth2-proxy-valkey-exporter` | 2 |
| `infra/04-data/analytics/opensearch` | 1 | `opensearch-node1`, `opensearch-node2`, `opensearch-node3` | 11 |

Thirty service names are declared in two files. The `06-observability` pair is
the hardest case: it shares all nine service names, adds none, and differs only
in settings, so a profile has nothing to select.

**In scope.** The six pairs above, the service names they declare, the settings
that differ between members, the root `include:` list entries for them, and the
documents and scripts that cite the currently unreachable member.

**Out of scope.** Every file SPEC-0156 already converged, the profile vocabulary
POL-0078 registers, and any live runtime mutation.

## Behavior Contract

1. Both topologies of each pair are selectable from the root entry point.
2. Rendering the union of every declared profile succeeds.
3. Selecting no profile resolves no service.
4. A reader can determine which topology a profile selects without opening the
   Compose files.

## Technical Approach

The approach is not yet decided. Three candidates exist and each pair may take a
different one.

1. **Parameterize and merge.** Collapse the pair into one file whose shared
   services read their differing settings from environment variables, and gate
   the extra services behind a profile. Applies where the differences are
   values rather than structure.
2. **Rename and include both.** Give the non-default member distinct service
   names so Compose holds both, then gate each set behind its own profile.
   Applies where the differences are structural. Costs a rename across the
   documents and scripts that cite the service.
3. **Keep the file out of `include:`.** Reach the variant through a documented
   `COMPOSE_FILE` override instead. Applies where neither of the above is
   proportionate.

Selecting among them requires reading the differing keys per pair, which this
Spec defers to its Plan.

## Interfaces and Data

| Interface | Change |
| :--- | :--- |
| `infra/**/docker-compose*.{yml,yaml}` for the six pairs | resolved by one of the three approaches |
| `docker-compose.yml` `include:` | entries added for the members that become includable |
| `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md` | extended with any new topology selector |
| `docs/90.references/data/0059-compose-profile-service-coverage/` | regenerated |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Merging a pair silently drops a topology | The Plan records the differing keys per pair before any member is changed |
| A rename breaks an inbound citation | Every citing document and script is updated in the same logical change |
| Parameterizing changes the effective settings of a running stack | The rendered settings are compared against the pre-change render per member |
| Including both members reintroduces the invalid merge | The union render is checked before each pair is committed |

## Acceptance Contract

1. `docker compose config --quiet` succeeds for every declared profile name.
2. `docker compose config --services` with no profile selected prints nothing.
3. Each of the six directories has both topologies selectable, by include or by
   a documented override recorded in POL-0078.
4. No service name is declared in two included files.
5. `bash scripts/validation/validate-docker-compose.sh` exits 0.
6. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0.
7. The Task records the chosen approach and the measured difference per pair.

## Traceability

| Upstream | Relation |
| :--- | :--- |
| REQ-0023 | `infra_net` standardization constrains inclusion changes |
| REQ-0025 | Operational readiness closure is the need a selectable topology serves |
| ADR-0026 | Standardized `infra_net` decision bounds network handling |
| SPEC-0156 | Converged every other file and measured the six pairs this Spec owns |
| POL-0078 | Registers the profile vocabulary any new selector must join |

## Related Documents

- [Compose enablement model convergence](../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md)
- [Compose profile vocabulary](../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md)
- [Compose profile service coverage](../../90.references/data/0059-compose-profile-service-coverage/README.md)
