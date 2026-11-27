---
title: "D05 v9 n8n Notifier and Hermes Delivery Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-27"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0122"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-27"
---

# D05 v9 n8n Notifier and Hermes Delivery Task

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

Own criterion179/W195 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D05 of the v9 task prompts: reuse the accepted n8n queue, notifier and Hermes
delivery results (SPEC-0204 TSK-0022, SPEC-0212 TSK-0044 and TSK-0050, which
are terminal and not edited), and act only on inputs that changed after the
D05 v8 acceptance at `e4d8011a2`.

##### Inputs and Authority

On 2026-11-27 the user directly requested D05 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`05_n8n_hermes_messaging.md`), limited to that prompt's scope, with commit,
push, PR and merge after checks. Work ran in the primary checkout on branch
`docs/d05-v9-notifier` from clean `main` `dc1697d27`; brief `d05-v9-notifier`
revision 1 bound this Task and the Spec and Plan rows. Direct user
authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Changed inputs since `e4d8011a2`

| Input | Change | Owner of the change |
| --- | --- | --- |
| Broker login | Named `n8n` mng-valkey user by default | D03 (TSK-0120 E19 to E21) |
| Opsflow notifier node | nodemailer 10.1.4 → 10.6.0, axios override 1.20.0 → 1.21.1 (PR #1251); rebuilt and recreated, but "loading the node in a workflow was not exercised" (SPEC-0212 TSK-0052) | D05 here |
| Sandbox | 1.8.1 → 1.16.0 | D06 |
| Hermes workload, routes, plugin | No change; plugin `research-report` 0.4.5 | - |

###### Census

| Task | Finding | Verdict |
| --- | --- | --- |
| T01 queue and runner | n8n and n8n-worker on `hyhome/n8n:2.46.6-local`, healthy; 0 NOPERM or WRONGPASS lines in 24 h (TSK-0120 E19) | REUSE |
| T02 notifier | The DEV notifier workflow "Operations manifest outbox to Mailpit (DEV draft)" stays inactive; the node `opsflowSmtp` v1 loads in the live worker and resolves nodemailer 10.6.0 from its own package | VERIFIED (below) |
| T03 Hermes delivery | `hermes-gateway` (user unit) and the system units `hermes-attester.timer` and `hyhome-hermes-dashboard.service` are active; the attester ran every 5 minutes for 24 h with 0 error lines, last success 16:17 KST; plugin 0.4.5 equals TSK-0022 | REUSE |
| T04 mail TLS and uncertainty | The live send below used the plain capture profile; the STARTTLS profile and same-ID refresh stay at the TSK-0044 criterion 75 isolated scope | REUSE |
| T05 native notifier rehearsal | `tests/validation/_opsflow_native_inputs.py` pins the 2.43.6 candidate `hy-home/sec01-n8n:2.43.6-opsflow-03892eb1a9a4` with source-binding labels, runner 2.43.6, PostgreSQL 18.6, Valkey 9.1.2 and Mailpit 1.31.5; HOME runs n8n 2.46.6 without those labels and Mailpit 1.34.0. A current rehearsal needs a reviewed SEC01 candidate build of n8n 2.46.6 with the opsflow node | Handed to D09 |

###### Live notifier check

In `n8n-worker`, `transport.sendClaim` from the installed node
(`/opt/hyhome/n8n-custom/opsflow/dist/transport.js`) ran with one synthetic
claim (run id
`62c27e17adb998f81f009a1ded380c46a4faf2185561560c1b13e959d1ce9f35`) and the
plain capture credential:

| Case | Result |
| --- | --- |
| Normal | `accepted_by_smtp`; Mailpit holds exactly one message, subject "DEV manifest publication", to `manifest@opsflow.invalid` |
| Credential naming another host | `OPSFLOW_INVALID_CREDENTIAL`, nothing sent |
| Lease too short to finish | `cancelled`, nothing sent |

The synthetic message was then deleted by its Mailpit ID (HTTP 200) and a
search for its Message-ID returns 0. No outbox row, database or workflow was
touched.

##### Blockers and Decisions

None that need an owner choice. The isolated notifier rehearsal on the current
image waits for the D09 candidate build named above.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 179 | W195 | method=review; tool=git; command=git diff and git log e4d8011a2..HEAD over the n8n, Hermes route and mail paths | `main` dc1697d27 | PASS | Changed inputs above | required | - |
| E02 | 179 | W195 | method=observation; tool=docker, node in n8n-worker; command=require the node module, resolve nodemailer through createRequire, n8n list:workflow | HOME, 2026-11-27 | PASS | `opsflowSmtp` v1 loads; nodemailer 10.6.0; notifier workflow inactive | required | - |
| E03 | 179 | W195 | method=automated; tool=node in n8n-worker, Mailpit API; command=transport.sendClaim normal, wrong host, short lease; search by Message-ID; delete by ID | HOME n8n 2.46.6 and Mailpit 1.34.0, 2026-11-27 | PASS | accepted_by_smtp with one captured message; OPSFLOW_INVALID_CREDENTIAL; cancelled; message deleted, 0 remain | required | - |
| E04 | 179 | W195 | method=observation; tool=systemctl, journalctl; command=is-active and list-timers for the Hermes units; attester journal for 24 h; installed plugin.yaml version | Server A, 2026-11-27 | PASS | Units active; 0 attester error lines; plugin 0.4.5 | required | - |
| E05 | 179 | W195 | method=review; tool=-; command=compare `_opsflow_native_inputs.py` pins with the HOME images | `main` dc1697d27 | FAIL | Rehearsal pins 2.43.6 and older companions; no current candidate image exists | optional | - |

##### Resolution Links

None: no row resolves another. E05 stays open for D09.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 179 | pending | E01,E02,E03,E04 | Awaiting owner acceptance | @buenhyden |

##### Remaining Conditions

- E05: D09 builds a reviewed SEC01 n8n 2.46.6 candidate with the opsflow node
  and its source-binding labels, repins `_opsflow_native_inputs.py`, and the
  isolated notifier rehearsal runs on it.
- External SMTP delivery, live 409, the same-UID limit, the external SDK
  Call-ID and DNS deadline, and Blog-data cursor fairness keep their recorded
  owners in TSK-0022, TSK-0044 and TSK-0050.

#### Handoff

##### Promotion Receipt

None: this Task records verification and routing only.

##### Next Owner

The owner decides criterion 179. D09 owns E05. No other prompt is started
automatically.

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
