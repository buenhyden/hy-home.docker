---
title: Resolve the Compose Sibling Pairs
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0171-TSK-0001
parent_ids: [SPEC-0171, SPEC-0171-PLAN-0001]
created: 2026-09-04
updated: 2026-09-04
completed_at: 2026-09-04
---

# Resolve the Compose Sibling Pairs

## Objective

Make both topologies of each of the six sibling pairs selectable, and remove the
duplicate files that made every change a two-place edit.

## Inputs

- The six pair directories under `infra/`
- `docker-compose.yml` and its `include:` list
- `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`
- `.env.example`
- `scripts/hardening/check-all-hardening.sh`

## Work Log

### The fourth approach

The Spec offered three candidates: parameterize and merge, rename and include
both, or reach the variant through a `COMPOSE_FILE` override. Measurement found
a fourth that covers every pair, and the other three were not needed.

`depends_on` accepts `required: false`, and a dependency marked that way renders
when its target is not selected:

```text
required: false   -> renders; the dependant is listed
required omitted  -> service "base" depends on undefined service "extra"
```

That is what lets a second topology sit behind a profile while the services that
depend on it stay in the domain profile. Nested substitution holds too, so a
default can carry its own inner variable, verified in all three states:

```text
'${OUTER:-1@kafka-1:${INNER:-9093}}'
  neither set -> 1@kafka-1:9093
  INNER set   -> 1@kafka-1:7777
  OUTER set   -> 1@k1:9093,2@k2:9093
```

A `secrets:` entry names a top-level secret and cannot be templated, but the
*path* a service reads is an ordinary string. So a service mounts both secrets
and selects between them with a variable.

### What the pairs actually were

Only three of the six were topology choices. The Spec's framing of "two
topologies" held for kafka and opensearch; the rest were something else.

| Pair | What differed | Class |
| :--- | :--- | :--- |
| `06-observability` | cadvisor's cpus/mem_limit, prometheus's config file | near-duplicate, 517 and 509 lines |
| `02-auth/oauth2-proxy` | shared `mng-valkey` or its own, dev or prod Dockerfile | shared vs dedicated broker |
| `07-workflow/n8n` | same | shared vs dedicated broker |
| `07-workflow/airflow` | same | shared vs dedicated broker |
| `04-data/opensearch` | one node or three | scale-out, plus an unintegrated draft |
| `05-messaging/kafka` | one broker or three, plus independent drift | scale-out with drift |

The `profiles` difference was mechanical in every pair: the `.dev.yml` member
carried `[<domain>, dev]` and the other `[<domain>]`. That is the selector, not
a setting.

Two pairs were not peers of their sibling. `opensearch/docker-compose.cluster.yml`
declared no profiles at all, commented out its volume drivers, carried its own
top-level `networks:` and `secrets:` blocks, and its `opensearch-dashboards` was
strictly less wired than the integrated one: list-form traefik labels, no
security-cookie or oauth2 secret, no cert mount, no tmpfs, no fixed address. Its
three nodes were substantive and moved; its dashboards did not. And the kafka
pair had drifted apart on settings unrelated to broker count, so the merge kept
the member the root includes.

### New selectors

| Selector | Gates | Coupled variables |
| :--- | :--- | :--- |
| `dedicated-valkey` | 6 broker and exporter services across three domains | `OAUTH2_PROXY_VALKEY_HOST`, `N8N_VALKEY_HOST`, `N8N_VALKEY_SECRET`, `AIRFLOW_VALKEY_HOST`, `AIRFLOW_VALKEY_SECRET` |
| `data-cluster` | 3 opensearch nodes | `OPENSEARCH_HOSTS` |
| `messaging-cluster` | 2 extra kafka brokers | `KAFKA_QUORUM_VOTERS`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_BOOTSTRAP_SERVERS_URI`, `KAFKA_REPLICATION_FACTOR`, `KAFKA_HEAP_OPTS` |

Compose cannot couple a profile to an environment value, so each selector's
variables must be set with it. POL-0078 records that, because selecting the
profile alone starts a broker nothing points at.

## Verification Evidence

### Baseline comparison

Every merge was checked against a pre-merge render of both members, service by
service and key by key. `profiles` is reported separately, because a merged file
necessarily carries the union of both selectors.

| Member | Profiles | Unexplained | Declared | Selector-only |
| :--- | :--- | ---: | ---: | ---: |
| observability-dev | `obs,dev` | 0 | 0 | 0 |
| observability-full | overrides | 0 | 0 | 9 |
| oauth2-dev | `core,auth,dev` | 0 | 1 | 0 |
| oauth2-full | `core,auth,dedicated-valkey` | 0 | 1 | 2 |
| n8n-dev | `workflow,dev` | 0 | 4 | 0 |
| n8n-full | `workflow,dedicated-valkey` | 0 | 5 | 6 |
| airflow-dev | `workflow,dev` | 0 | 13 | 0 |
| airflow-full | `workflow,dedicated-valkey` | 0 | 14 | 10 |
| opensearch-single | `data` | 0 | 2 | 1 |
| opensearch-cluster | `data-cluster` | 0 | 9 | 4 |
| kafka-dev | `messaging,dev` | 0 | 6 | 0 |
| kafka-full | `messaging,messaging-cluster` | see below | — | — |

The declared differences are the secrets superset, the `required: false` flag,
and for opensearch-cluster the deliberate choice of the integrated dashboards.

`kafka-full` is the one member the merge does not reproduce, by design. Its
`kafka-2` and `kafka-3` are identical key for key; the other services differ
exactly where the unreachable file had drifted from the running one. Nothing
ever ran with those settings, because no root entry point reached that file.

### Acceptance contract

| Item | Command | Result |
| :--- | :--- | :--- |
| 1 | `docker compose config --quiet` per declared profile | 28 of 28 render |
| 2 | `docker compose config --services` with no profile | prints nothing |
| 3 | both topologies selectable per directory | 6 of 6, by profile |
| 4 | service names declared in two included files | 0 |
| 5 | `bash scripts/validation/validate-docker-compose.sh` | `selections=28 services_total=232`, exit 0 |
| 6 | `python3 scripts/validation/run-ci-gate.py --profile full` | `GATE_EXIT=0`, 18 `OK` suites |
| 7 | this section | recorded |

Compose files under `infra/` fell from 47 to 41, and the root now includes all
41. No file under `infra/` is unreachable.

### Vocabulary parity

`declared=28 registered=28`, with neither set holding an extra.

### Mutation evidence

| Check | Mutation | Observed |
| :--- | :--- | :--- |
| profile-crossing dependency | drop `required: false` | `depends on undefined service` |
| baseline comparison | merge airflow with two services left on the old selector | the comparison flagged both; the first pass had skipped them because they wrote `- workflow` unquoted where the rest wrote `- 'workflow'` |

## Review Evidence

- `python3 scripts/validation/check-document-metadata.py --mode check-contracts`: `violations=0`
- `python3 scripts/validation/check-document-links.py --mode all`: `failures=0`
- `python3 -m unittest tests.lib.target_surface.test_target_surface_contracts`: 43 tests, OK
- `bash scripts/hardening/check-all-hardening.sh`: fails at `oauth2-proxy valkey image tag mismatch`, expecting valkey 9.1.0 where the file has 9.1.1. Reproduced on `main` before this work; `set -euo pipefail` makes the suite stop at its first failure, so this one was masked while a failure of ours came earlier. Left as a finding.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `5d274dec` | Merge the observability pair |
| `c45e7923` | Merge the three shared-broker pairs |
| `ac4b8a6b` | Fold the opensearch cluster nodes |
| `5b7bca9a` | Merge kafka onto the running configuration |

## Rulings

- The Spec's three candidate approaches were replaced by a fourth. `required:
  false` and templatable secret paths cover every pair, so no rename and no
  `COMPOSE_FILE` override was needed.
- Where two members disagreed, the one the root includes wins. It is the
  configuration in service; the other was unreachable and unexercised.
- The opensearch draft's dashboards definition was discarded rather than merged.
  Importing it would have removed gateway and security wiring the integrated
  definition has.
- The kafka exporter keeps one `--kafka.server`. Parameterizing the list made
  the default scrape kafka-1 three times, and the flag is a seed list from which
  the exporter discovers the rest.
- The hardening suite's pre-existing failure was left in place. Changing the
  expected image tag is an image-version decision belonging to the domain owner.

## Deferred Items

| Item | Owner |
| :--- | :--- |
| `oauth2-proxy valkey image tag mismatch` in the hardening suite | operations domain owner for `02-auth` |
| `n8n-valkey-exporter` scraping `redis://mng-n8n-valkey`, a host no service declares | operations domain owner for `07-workflow` |
| `kong` and `surrealdb` both publishing host 8000 | operations domain owners for `04-data` and `11-laboratory` |
| `infra/09-tooling/k6/` running locust with a missing Dockerfile | operations domain owner for `09-tooling` |

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Compose profile vocabulary](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md)
