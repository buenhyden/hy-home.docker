---
title: "D06 v8 Sandbox HOME Selection Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-25"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0118"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-25"
---

# D06 v8 Sandbox HOME Selection Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion174/W190 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply D06 of the lifecycle v8 task prompts: add the n8n Assistant sandbox API
and runner to the HOME selection (D06-T04 item 4), keep the certs job
one-shot, update the privileged exception, and record the D06 items left
open.

##### Inputs and Authority

On 2026-11-25 the user directly requested D06 from
`_workspace/workspace_task_prompts_20261125_lifecycle_v8/` (prompt
`06_ai_ollama_local_cloud_sandbox.md`), limited to that prompt's scope, with
commit, push, PR and merge after checks. The package treats the sandbox API
and runner joining HOME as decided, which conflicted with the POL-0078 row
that kept `n8n-sandbox` out of the default selection (owner decision
2026-11-09) and with the privileged exception that cited the opt-in profile
as a mitigation. Asked in this chat, the owner chose to add the profile to
HOME. Work ran on branch `feat/sandbox-home-selection` in the linked worktree
`.claude/worktrees/sbx` from `main` `20b188aab`; brief `d06-sandbox-home`
bound the paths before the first edit. Direct user authorization is
authority; this record is not.

#### Execution Log

##### Work Performed

###### Change

- POL-0078: `n8n-sandbox` joins the HOME row; the profile row now says it is
  in the HOME selection since the owner decision of 2026-11-25, with certs as
  a one-shot job.
- `infra/common-optimizations.exceptions.json`: the runner's privileged
  exception no longer cites an opt-in profile as mitigation and is re-reviewed
  on 2026-11-25; its recorded impact (a sandbox break-out reaches host-level
  rights, the internet and, through NAT, the host LAN) is unchanged.
- The n8n Compose file is unchanged. A first attempt reworded its section
  comment, which still says opt-in, but the update ledger and the
  2026-11-11 advisory review pin that file's exact bytes; rebinding a dated
  security review to input it never examined would misstate it, so the edit
  was reverted (E05). POL-0078 owns the selection.

###### Verification

The read-only HOME plan grows from 16 profiles and 48 targets to 17 and 51:
`n8n-sandbox-api`, `n8n-sandbox-runner-1` and the job `n8n-sandbox-certs`.
The running runner is privileged as declared, publishes no host port, mounts
no host Docker socket (only its TLS volume, two secret files and its own
Docker data volume), joins only `n8n_sandbox_runner_net` and
`n8n_sandbox_outbound_net`, has 4 GiB, 3 CPU and 4096 pids limits and is
healthy; the API publishes no host port and is healthy. No container was
started or recreated.

###### Left open

| Item | State | Owner |
| --- | --- | --- |
| D06-T01 local Ollama consumption by server A/B agents | Not run in this pass | D06 follow-up |
| D06-T03/T04 negative tests inside the sandbox (forbidden IP, metadata, other DB, cancel and cleanup) | Not run | D06 follow-up with owner approval |
| Stale "opt-in" comment on the n8n Compose sandbox section | Kept; changes with the next reviewed n8n Compose update | n8n Compose owner |
| D06-T05 Wiki preparation and D06-T06 tool comparison | Not run | D06 follow-up |

##### Blockers and Decisions

The owner chose the HOME selection over keeping the privileged runner opt-in;
the security impact stays recorded in the exception.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 174 | W190 | method=automated; tool=Python3 venv; command=compose-start.py --root "$PWD" plan --selection HOME --dev-data-expected on | Change | PASS | 17 profiles, 51 targets including the three sandbox services | required | - |
| E02 | 174 | W190 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_compose_start tests.validation.test_p02_service_contracts tests.validation.test_service_wiring_contracts | Change | PASS | 100 OK | required | - |
| E03 | 174 | W190 | method=automated; tool=Python3 venv, bash; command=check-document-metadata.py; check-operations-catalog.py; check-conftest-policy.sh --mode corpus; check-supply-chain-policy.py --check; check-all-hardening.sh | Change | PASS | 0 violations; catalog pass; 45/45; supply chain pass; all hardening checks passed | required | - |
| E05 | 174 | W190 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.supply_chain.test_update_gates | PR #1213 head f26032a58 (hosted candidate-core) | FAIL | The comment edit changed the n8n Compose hash pinned by the update ledger and the advisory review; the Compose file and ledger were restored to main | required | - |
| E06 | 174 | W190 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.supply_chain.test_update_gates | Compose file and ledger identical to main | PASS | update-gates suite OK | required | E05 |
| E04 | 174 | W190 | method=observation; tool=docker; command=docker inspect n8n-sandbox-runner-1 and n8n-sandbox-api | HOME, 2026-11-25 | PASS | Privileged runner without host port or host socket, two sandbox networks, 4 GiB/3 CPU/4096 pids, healthy; API without host port, healthy | required | - |

##### Resolution Links

E06 resolves E05.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 174 | pending | E01,E02,E03,E04,E06 | The HOME selection change and its checks are complete; owner acceptance is not given | @buenhyden |

##### Remaining Conditions

Owner acceptance of criterion174. The items under Left open stay with their
owner.

#### Handoff

##### Promotion Receipt

POL-0078 and the exception register carry the change.

##### Next Owner

The owner decides acceptance and whether to run the left-open D06 items.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
