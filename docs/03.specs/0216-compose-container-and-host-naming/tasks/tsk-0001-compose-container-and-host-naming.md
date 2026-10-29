---
title: "Compose Container and Host Naming Task"
version: "0.3.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0216-TSK-0001"
parent_ids:
- "SPEC-0216-PLAN-0001"
created: "2026-10-08"
---

# Compose Container and Host Naming Task

## Overview

### Objective

Give every `infra/` Compose service a `container_name` and a `hostname` equal
to its service key, register the exceptions, enforce the rule, and run HOME
under the new names.

## Inputs and Authorization

The user request on 2026-10-08 states that every service in the `infra/`
Compose files must have `container_name` and `hostname`, and recommends the
service name for both. The owner chose to keep `supabase-*` container names as
registered exceptions and to recreate HOME right after the merge. Baseline:
`main` `4e6d094b1`. Registry issues SPEC-0216.

## Work Log

### Baseline

The rendered root model (`--profile '*'`, `.env.example`) had 121 services:
82 with a matching `container_name` and no `hostname`, 21 with a different
`container_name` and no `hostname`, 8 with neither, and 10 with both matching.
No service sets `replicas` or `scale`. Three use `network_mode: none`, which
still allows a hostname. The differing names were seven `infra-*`
observability containers, thirteen `supabase-*` containers and
`oauth2-proxy-redis-exporter`.

### W1 Rule, Exceptions, Test and Compose Edits

A one-off script, not committed, edited each service block as text so comments
and anchors survive. It set `container_name` (inserted after `image` when
missing) and added `hostname` after it, then re-parsed every file with the
repository's Compose loader to confirm both keys. 39 Compose files changed.
`naming_exceptions` in `infra/common-optimizations.exceptions.json` lists the
thirteen Supabase services with their container names and reasons. POL-0001
states the rule and the allowed exception.

`test_every_infra_service_names_its_container_and_host` in
`test_infra_tier_layout.py`, which the compose regression leaf already runs,
reads every `infra/` Compose file. Against the previous Compose files it
failed 111 sub-tests (RED); after the edits it passes. An exception without a
`reason` is ignored, so its service fails the test.

### W2 Documents

Seven guides, seven policies, nine runbooks and eight READMEs named the
`infra-*` containers in `docker logs`, `docker exec` and inventory lines. They
now use the service names. A search afterwards found no active reference to a
retired container name; history and archives keep theirs.

### W3 HOME Recreation

Run on 2026-10-08 from the HOME checkout at merge `948fd7e3b`. The 51 running
`hy-home-infra` services were recreated with `docker compose up -d --no-deps`
after pulling the new Ollama and Open WebUI images. Seven of them (`comfyui`,
`dev-pg`, `kafka-1`, `keycloak`, `mng-pg`, `mng-valkey`, `traefik`) already
had a matching hostname and container name, so Compose left them unchanged.

`up` exited 1. Recreating `openbao` restarted it sealed (`initialized`,
`sealed`, Shamir, raft), so it reports unhealthy and `openbao-agent` was not
recreated; the old agent container keeps running healthy. Unsealing needs the
owner-held key shares, and RUN-0085 forbids restarting OpenBao without a ready
unseal administrator. Including `openbao` in the bulk recreation was the
error: the next recreation of a restartable stack must exclude it and handle
OpenBao through RUN-0085.

Afterwards 48 containers were healthy, two ran without a health check and only
`openbao` was unhealthy. Recreated containers report their service name as
container name and hostname (`prometheus`, `grafana`, `alloy`). Prometheus had
27 targets up and 7 down; six of those services (`airflow-valkey-exporter`,
`cadvisor`, `n8n-valkey-exporter`, `oauth2-proxy-valkey-exporter`,
`opensearch`, `pyroscope`) were not running before the recreation, and the
seventh is `openbao`. The never-started `infra-pyroscope` container
(`Created`) predates this change and is replaced on the next `pyroscope` start.

Later on 2026-10-08 the owner unsealed OpenBao with the held key shares per
RUN-0085. `bao status` then reported `initialized`, not `sealed`, raft storage
in HA mode `active`, version 2.6.2, and the `openbao` container was healthy.
`openbao-agent` was then recreated and runs healthy with container name and
hostname `openbao-agent`.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0216 | draft | approved | #owner-decision-2026-10-29 |
| SPEC-0216-PLAN-0001 | draft | approved | #owner-decision-2026-10-29 |
| SPEC-0216-TSK-0001 | draft | ready | #inputs-and-authorization |
| SPEC-0216-TSK-0001 | ready | in-progress | #w1-rule-exceptions-test-and-compose-edits |
| SPEC-0216-TSK-0001 | in-progress | completed | #owner-decision-2026-10-29 |

### Owner decision 2026-10-29

The work already landed. On 2026-10-29 the owner approved SPEC-0216 and its
Plan after the fact and closed the package on documents alone. Criterion 4 is
now accepted: the sealed OpenBao FAIL row is resolved by the PASS row
"Owner acceptance 2026-10-29", which rests on the earlier PASS row
"OpenBao unseal and agent recreation" (owner unseal per RUN-0085, healthy
`openbao`, recreated `openbao-agent`). Criteria 1 to 3 keep their earlier
acceptance. No runtime check was rerun.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Naming test | 1 | W1 | RED with previous Compose files, GREEN after | Working tree | PASS | W1 Rule, Exceptions, Test and Compose Edits | required | - |
| Render and catalog | 3 | W1 | Root render; `check-operations-catalog.py`; projection check | `.env.example` | PASS | W1 Rule, Exceptions, Test and Compose Edits | required | - |
| Document references | 2 | W2 | `git grep` for retired names outside history | Working tree | PASS | W2 Documents | required | - |
| HOME recreation | 4 | W3 | Recreate running services; health, names, scrape targets | Merged `948fd7e3b`; HOME 2026-10-08 | PASS | W3 HOME Recreation | required | - |
| OpenBao after recreation | 4 | W3 | `bao status`; container health | HOME 2026-10-08 | FAIL | W3 HOME Recreation | required | - |
| OpenBao unseal and agent recreation | 4 | W3 | Owner unseal per RUN-0085, then recreate `openbao-agent`; `bao status`; container health | HOME 2026-10-08 | PASS | W3 HOME Recreation | required | - |
| Owner acceptance 2026-10-29 | 4 | W3 | `bao status`; container health | Recorded unseal and agent result re-read by the owner; no rerun | PASS | Owner decision 2026-10-29 | required | OpenBao after recreation |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Naming test | Generation 5 row acceptance | SPEC-0216 TSK-0001 |
| 2 | accepted | Document references | Generation 5 row acceptance | SPEC-0216 TSK-0001 |
| 3 | accepted | Render and catalog | Generation 5 row acceptance | SPEC-0216 TSK-0001 |
| 4 | accepted | OpenBao unseal and agent recreation, Owner acceptance 2026-10-29 | Owner accepted on 2026-10-29; the unseal PASS row resolves the sealed FAIL. | SPEC-0216 TSK-0001 |

## Review and Completion

W1 and W2 are complete in source. W3 recreated HOME under the new names. The
recreation left OpenBao sealed, which remains a recorded FAIL; the owner then
unsealed it and `openbao-agent` was recreated, as recorded in the resolving
PASS row.

The 2026-10-22 readback distinguished that recovery from acceptance: criterion
4 was then `rejected`; the owner accepted it on 2026-10-29, as recorded in
the owner decision above. Current source also reflects
SPEC-0225's node-exporter hostname omission and the LAB-owned Supabase naming
registry, now stated in the [Spec contracts](../spec.md#contracts).

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
