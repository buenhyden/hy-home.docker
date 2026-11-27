---
title: "D07 v9 Secret Structure and OpenBao Recheck Task"
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
artifact_id: "SPEC-0212-TSK-0124"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-27"
---

# D07 v9 Secret Structure and OpenBao Recheck Task

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

Own criterion181/W197 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D07 of the v9 task prompts: reuse criterion 172 (TSK-0116) and act only on the
key and metadata changes that came after it: the D03 named mng-valkey
credentials (CACHE-031, CACHE-032), the removal of `VALKEY_MNG_HOSTNAME`, and
the Terrakube retirement (`8fb733101`, `aaef07818`).

##### Inputs and Authority

On 2026-11-27 the user directly requested D07 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`07_openbao_secret_env.md`), limited to that prompt's scope, with commit,
push, PR and merge after checks. Asked in this chat, the owner approved the
agent running `gen-secrets.sh --sync-metadata` once; prune mode was excluded
because it also rewrites `labs/.env`. Work ran in the primary checkout on
branch `docs/d07-v9-secrets` from clean `main` `cbe162720`; brief
`d07-v9-secrets` revision 1 bound this Task and the Spec and Plan rows. No
secret value was read or printed. Direct user authorization is authority;
this record is not.

#### Execution Log

##### Work Performed

###### Census

| Task | Finding | Verdict |
| --- | --- | --- |
| T01 env and registry structure | `secret-structure.py check --read-private` returned DRIFT (env public line 146 `PUBLIC_ASSIGNMENT`, registry public row 87 `PUBLIC_ROW`); TSK-0116 E20 was MATCH | CHANGE_REQUIRED (below) |
| T02 OpenBao and Agent | `openbao` and `openbao-agent` on `hy-home/openbao:2.7.3-go1.27.4-net0.62.0-r1`, healthy; OpenBao initialized, unsealed, raft, HA enabled | REUSE |
| T03 SMTP single source | `secret-structure.py smtp-equality --read-private` returns `OLD_ABSENT`, no comparison performed | REUSE |
| T04 retirement candidates | The private files still carry the entries the public sources dropped (below) | Owner step |
| T05 catalog and metadata tests | 106 tests OK with the project `.venv` first on `PATH`. With the system `python3`, `gen-secrets.sh` exits 2 on the missing `referencing` module and 15 tests fail; that is the local interpreter, not the code | REUSE |

###### Sync

The owner-approved `gen-secrets.sh --sync-metadata` changed the private
registry only; values preserved, secret files untouched, mode 0600 and one
link kept on both files. The following `--sync-metadata-check` reported 0
files to change.

| File | Before | After |
| --- | --- | --- |
| `.env` | 0600, 1 link, 17036 bytes, SHA-256 prefix `b32376d2cbd1e979` | unchanged |
| `secrets/SENSITIVE_ENV_VARS.md` | 0600, 1 link, 34848 bytes, SHA-256 prefix `1d409daff3ae66dc` | 0600, 1 link, 35648 bytes, SHA-256 prefix `482a2fbfb68db3c7` |

After the sync the structure check still returns DRIFT: env public line 146
`PUBLIC_ASSIGNMENT` and registry `PRIVATE_EXTRA`. Plain sync keeps private
entries that public sources dropped; only prune removes them, and prune also
rewrites `labs/.env`.

##### Blockers and Decisions

The remaining private-only entries need the owner. From the public history
they are the env keys `VALKEY_MNG_HOSTNAME`, `TERRAKUBE_UI_PORT`,
`TERRAKUBE_EXECUTOR_PORT` and `TERRAKUBE_DB_USERNAME`, and the Terrakube
registry rows retired in `aaef07818`. The agent cannot list private names
itself: a direct read of the private files outside the registered scripts was
refused. Owner step: remove exactly those entries from the private `.env` and
`secrets/SENSITIVE_ENV_VARS.md`, keep 0600 and one link, then run
`secret-structure.py --root "$PWD" check --read-private` and expect MATCH.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 181 | W197 | method=automated; tool=Python3 venv; command=secret-structure.py --root "$PWD" check --read-private | Private files at `main` cbe162720, before the sync | FAIL | env DRIFT line 146 `PUBLIC_ASSIGNMENT`; registry DRIFT row 87 `PUBLIC_ROW` | required | - |
| E02 | 181 | W197 | method=automated; tool=bash, Python3 venv; command=gen-secrets.sh --sync-metadata-check | Same | FAIL | 2 files would change; the prune check would change 3, the third being `labs/.env` | optional | - |
| E03 | 181 | W197 | method=automated; tool=bash, Python3 venv; command=gen-secrets.sh --sync-metadata | Owner approval in this chat, 2026-11-27 | PASS | files_changed=2, values preserved, secret files untouched; metadata table above | required | - |
| E04 | 181 | W197 | method=automated; tool=bash, Python3 venv; command=gen-secrets.sh --sync-metadata-check | After E03 | PASS | files_changed=0 | optional | E02 |
| E05 | 181 | W197 | method=automated; tool=Python3 venv; command=secret-structure.py --root "$PWD" check --read-private | After E03 | FAIL | env DRIFT line 146 `PUBLIC_ASSIGNMENT`; registry DRIFT `PRIVATE_EXTRA` | required | - |
| E06 | 181 | W197 | method=automated; tool=Python3 venv; command=secret-structure.py --root "$PWD" smtp-equality --read-private | `main` cbe162720 | PASS | `OLD_ABSENT`, no comparison performed | required | - |
| E07 | 181 | W197 | method=automated; tool=Python3 venv on PATH; command=python -m unittest tests.validation.test_secret_metadata_sync tests.validation.test_secret_catalog_contract tests.lib.ops.test_secret_catalog | `main` cbe162720 | PASS | 106 tests OK | required | - |
| E08 | 181 | W197 | method=observation; tool=docker, bao; command=container image and health; bao status -format=json, selected fields | HOME, 2026-11-27 | PASS | 2.7.3, initialized, unsealed, raft, HA; Agent healthy | required | - |
| E09 | 181 | W197 | method=automated; tool=Python3 venv; command=secret-structure.py --root "$PWD" check --read-private | After the owner removes the private-only entries | NOT_RUN | Owner step above | required | - |

##### Resolution Links

E04 resolves E02. E09, once it returns MATCH, is the check that clears E01
and E05.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 181 | pending | E01,E02,E03,E04,E05,E06,E07,E08 | Awaiting the owner step and E09 | @buenhyden |

##### Remaining Conditions

- Owner removes the private-only entries named above; the agent then records
  E09 with MATCH.

#### Handoff

##### Promotion Receipt

None: this Task records verification and routing only.

##### Next Owner

The owner runs the private cleanup and decides criterion 181. No other prompt
is started automatically.

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
