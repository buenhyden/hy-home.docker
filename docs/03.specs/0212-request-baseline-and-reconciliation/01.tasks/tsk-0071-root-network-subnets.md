---
title: "Root Network Subnets Task"
version: "0.3.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-15"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0071"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-15"
---

# Root Network Subnets Task

## Scope

### Objective and Parent

#### Objective

Own W132/criterion 127. Give the three root Compose networks that take an
address from Docker's pool an explicit `10.250.x.0/24` subnet, as AD-0026
requires, prove it with a contract test, and apply it to the running HOME
networks by recreating only the networks and the four containers attached to
them.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W02 disposition](tsk-0070-w02-disposition-3-0-1.md)

### Inputs and Authority

On 2026-11-15, in this chat, the owner approved fixing the gap recorded in
AD-0026 1.9.0 (PR 1041): `n8n_ollama_net`, `opsflow_capture_net` and
`opsflow_notifier_db_net` had no explicit subnet. The approval covers the
Compose change and recreating those networks. It does not cover starting any
other service (Q07).

## Execution Log

### Work Performed

#### Design summary

| Item | Content |
| --- | --- |
| Target | Every network the root `docker-compose.yml` defines has an explicit subnet; AD-0026 matches Compose |
| Choice | `10.250.47.0/24`, `.48` and `.49`, above the highest subnet in use (`.46`); retired gaps (`.9`, `.12`, `.22`, `.29`, `.30`, `.38`) stay unused |
| Rejected | Reusing a retired range; changing leaf-owned networks, which AD-0026 lets their package declare |
| Interface | `ipam.config[0].subnet` on the three networks; `test_every_root_network_declares_an_explicit_subnet` |
| Failure | A live network with the old pool subnet makes Compose refuse to reuse it until it is recreated |
| Risk | High (Compose, runtime): independent `iac-reviewer` review before the runtime step |
| Rollback | Revert the commit, then recreate the same networks and containers the same way |

#### Runtime state before the change

Read-only `docker network inspect` on 2026-11-15:

| Network | Live subnet | Members |
| --- | --- | --- |
| `hy-home-infra_n8n_ollama_net` | 172.22.0.0/16 | `n8n-worker`, `ollama` |
| `hy-home-infra_opsflow_capture_net` | 172.30.0.0/16 | `n8n-worker`, `mailpit` |
| `hy-home-infra_opsflow_notifier_db_net` | 172.18.0.0/16 | `n8n-worker`, `dev-pg` |

#### Consumers fixed after the first hosted run

The author's local checks missed three consumers of the root Compose file.
The two contract tests now expect the explicit subnets, and
`ledger_rebind --write` re-bound only the `docker-compose.yml` include hash
in `update-ledger.json` (0 image rows; review, scan and acceptance fields
untouched).

#### Runtime apply

Before applying, no host route or Docker network used 10.250.47.0/24 to
10.250.49.0/24, the three networks had the four planned members, and
`n8n-worker` had logged no activity for 30 minutes. A first attempt passed the
profile flags as one shell word, so Compose rejected both `stop` commands and
`docker network rm` refused while the containers were attached; nothing
changed. The rerun with the flags written out applied the change. During the
apply, consumers of `ollama`, `dev-pg` and `mailpit` lost them for about two
minutes; no volume was touched.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0071 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0071 | ready | in-progress | #design-summary |
| SPEC-0212-TSK-0071 | in-progress | completed | #criterion-decisions |

### Blockers and Decisions

The runtime step runs only after the review passes and the change merges.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Subnet RED | 127 | W132 | red-green-proof | `test_every_root_network_declares_an_explicit_subnet` before the change | FAIL | the three networks named | required | - |
| Subnet GREEN | 127 | W132 | red-green-proof | `tests.validation.test_p02_service_contracts` at `3ebaef3ef` | PASS | module OK | required | Subnet RED |
| Compose render | 127 | W132 | compose-config | `docker compose config -q`, same tree | PASS | exit 0 | required | - |
| Compose controls | 127 | W132 | compose-policy | `check-template-security-baseline.sh`; `check-conftest-policy.sh --mode corpus`, same tree | PASS | findings 0; 45 of 45 policy tests | required | - |
| Independent review | 127 | W132 | independent-review | `iac-reviewer`, read-only, commit `3ebaef3ef` | PASS | No HIGH; subnets collide with nothing and nothing depends on the old addresses; MEDIUM: stop `n8n-worker` with a 60 s grace after confirming no running execution; LOW: GDE-0077 now lists the three ranges | required | - |
| Hosted candidate first run | 127 | W132 | remote-candidate | PR 1042 at the first head, run 43716166319 | FAIL | `candidate-core` failed: `test_service_wiring_contracts` and `test_n8n_outbox_contract` pinned the old network definitions, and the SEC01 ledger still held the old `docker-compose.yml` hash; `candidate-documents` PASS | required | - |
| Runtime apply | 127 | W132 | runtime-recreate | Recreate the three networks and their four containers from merged `main` | NOT_RUN | waits for review and merge | required | - |
| Hosted candidate final | 127 | W132 | remote-candidate | PR 1042 at `778a53534`, run 43717341955 | PASS | `candidate-core` 14 min 42 s, `candidate-documents` 3 min 3 s, `candidate-quality` success; merged as `feabde558` | required | Hosted candidate first run |
| Runtime apply live | 127 | W132 | runtime-recreate | From `main` `feabde558` at 22:22 KST: `stop -t 60 n8n-worker`; `stop ollama mailpit dev-pg`; `docker network rm` of the three networks; `up -d --no-deps --no-build --force-recreate` of the four services with their four profiles | PASS | `n8n_ollama_net` 10.250.47.0/24 (ollama .2, n8n-worker .3), `opsflow_capture_net` 10.250.48.0/24 (mailpit .2, n8n-worker .3), `opsflow_notifier_db_net` 10.250.49.0/24 (dev-pg .2, n8n-worker .3), all internal; the four containers healthy after 80 s; task broker ready on 10.250.23.2 and `n8n-task-runner-worker` reconnected at 13:25:49 UTC | required | Runtime apply |

### Resolution Links

Subnet RED is resolved by Subnet GREEN.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 127 | accepted | Subnet GREEN, Compose render, Compose controls, Independent review, Hosted candidate final, Runtime apply live | Owner @buenhyden accepted on 2026-11-15 in this chat | SPEC-0212 TSK-0071 |

### Remaining Conditions

None. The owner accepted criterion 127 on 2026-11-15 after the merge and the
live apply.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 127 | W132 | Subnet GREEN | Root `docker-compose.yml`, AD-0026 | `test_every_root_network_declares_an_explicit_subnet` |

### Next Owner

Criterion 127 is accepted; no owner action remains.
