---
title: "Compose Container and Host Naming Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0216-TSK-0001"
parent_ids:
- "SPEC-0216-PLAN-0001"
created: "2026-10-08"
---

# Compose Container and Host Naming Task

## Objective

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Naming test | 1 | W1 | RED with previous Compose files, GREEN after | Working tree | PASS | W1 Rule, Exceptions, Test and Compose Edits | accepted |
| Render and catalog | 3 | W1 | Root render; `check-operations-catalog.py`; projection check | `.env.example` | PASS | W1 Rule, Exceptions, Test and Compose Edits | accepted |
| Document references | 2 | W2 | `git grep` for retired names outside history | Working tree | PASS | W2 Documents | accepted |
| HOME recreation | 4 | W3 | Recreate running services; health, volumes, scrape targets | Merged source | NOT_RUN | Review and Completion | pending |

## Review and Completion

W1 and W2 are complete in source. W3 runs after the merge.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
