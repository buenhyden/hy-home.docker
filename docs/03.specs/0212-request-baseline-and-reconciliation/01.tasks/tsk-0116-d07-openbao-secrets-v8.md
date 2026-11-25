---
title: "D07 v8 OpenBao and Secret Reconciliation Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-25"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0116"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-25"
---

# D07 v8 OpenBao and Secret Reconciliation Task

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

Own criterion172/W188 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply D07 of the lifecycle v8 task prompts: reuse the accepted OpenBao,
catalog and SMTP results, remove the renderer grants and Agent templates no
HOME consumer uses, and hand the live window and the AI-011/INFRA-008
rotation to the owner. SPEC-0204 TSK-0014 keeps criterion 20; its legacy
evidence tables are frozen, so this pass is recorded here.

##### Inputs and Authority

On 2026-11-25 the user directly requested D07 from
`_workspace/workspace_task_prompts_20261125_lifecycle_v8/` (prompt
`07_openbao_secret_env.md`), limited to that prompt's scope, with commit, push,
PR and merge after checks. In this chat the owner chose to remove the two
stale grants from source now, keeping the HOME checkout un-pulled until the
window, and to run the rotation as an owner step. Work ran on branch
`fix/openbao-stale-lab-grants` in the linked worktree `.claude/worktrees/d07`
from clean `main` `767449bf5`; brief `d07-openbao-stale-grants` bound the
paths before the first edit (revision 2 after this Task replaced the frozen
TSK-0014). The 2026-11-25 OpenBao 2.7.3 window and the accepted -07 restore
(SPEC-0204 TSK-0006) are reused, not repeated. Direct user authorization is
authority; this record is not.

#### Execution Log

##### Work Performed

###### Findings

| Prompt item | Observation (value-free) | State |
| --- | --- | --- |
| T01 env structure | `secret-structure.py check --read-private` returns `BLOCKED`: one private `.env` value fails the inline-comment or quoting rule (`env_structure` → `_comment`). Locating it needs a read of the private file, which the session permission classifier refused | BLOCKED, owner |
| T02 P06 scope | The prompt's nine-path versus Keycloak/Grafana two-path premise is stale: TSK-0014 records owner cutovers for Keycloak, Grafana (2026-10-27), dozzle, gatus, open-webui, oauth2-proxy, kafbat-ui and airflow-apiserver (2026-10-28). Seven HOME consumers mount Agent output. Open WebUI and Superset are LAB with LAB-only secrets, yet `renderer.hcl` granted and the Agent rendered their KV paths | CHANGE_REQUIRED, fixed in source |
| T03 SMTP | `smtp-equality` returns `OLD_ABSENT`; the single SMTP source is in place | REUSE |
| T04 catalog | `secret-catalog.py check` returns `P02_METADATA_VALID`, 152 entries, 6 aliases | REUSE |
| T05 AI-011/INFRA-008 | Printed on 2026-11-25 (SPEC-0204 TSK-0022); no rotation record. Only consumers: `gen-secrets.sh`, which derives the INFRA-008 htpasswd, and Traefik `searxng-api-auth` | open, owner |
| Test environment | 15 `test_secret_metadata_sync` failures on clean `main` came from the system `python3` lacking `referencing`; with the repository venv on `PATH` all 57 pass | no change |

###### Source change

`renderer.hcl` loses the `08-ai/open-webui` and `12-analytics/superset` data
and metadata read paths; `agent.hcl` loses their four templates and the four
`.ctmpl` files are deleted; `protected-restore-inputs.py` drops them from its
input list; `oidc-client-secrets.sh` and `verify-oidc-client-secret.sh` drop
both services, which the verifier now refuses with exit 2. The digests of
`renderer.hcl`, `protected-renderer-roles.py` and `protected-restore-inputs.py`
are re-pinned in `p01-bootstrap.sh` and `protected-renderer-roles.py`. The
agent-contract counts fall from 19 to 15 templates, and the verifier test
covers the removed services as usage refusals. KV data, `operator.hcl`,
catalog rows IAM-011 and IAM-013 and the dated `update-ledger.json` receipts
are unchanged: the catalog still describes the running Agent, which renders
both until the window.

###### Owner window order

Pull this commit into the HOME checkout only inside a RUN-0105 window:
`agent.hcl` is a single-file bind and the templates are a directory bind, so
the running Agent fails its health check from the pull until step 3.

1. Fast-forward the HOME checkout to the merge commit and approve it as the
   window commit.
2. Recreate `openbao-agent` so it reads the new `agent.hcl`.
3. Remove `/openbao/out/open-webui` and `/openbao/out/superset` from the Agent
   output volume; `health-agent.sh` refuses group-readable files it does not
   consume.
4. Write the narrowed `renderer` policy through `protected-renderer-roles.py`
   with the new pin, and confirm the Agent stays healthy.
5. Update IAM-011 and IAM-013 delivery in the catalog to match.

###### AI-011/INFRA-008 rotation, owner-run

1. Replace `secrets/tools/searxng/searxng_api_password.txt` with a new random
   value at mode 0600 without printing it.
2. Run `bash scripts/operations/gen-secrets.sh` with the repository venv on
   `PATH`; it rebuilds `secrets/auth/traefik/traefik_searxng_api_htpasswd.txt`
   because the old hash no longer verifies.
3. Recreate `traefik` so the `/run/secrets` file is re-read.
4. From 192.168.0.22 with TLS verified and a 0600 netrc: the old credential
   returns 401 on `/search` and the new one 200; browser SSO is unchanged.
5. Record the four results in SPEC-0204 TSK-0022 without values.

###### Next prompts and preconditions

| Prompt | Item | Precondition |
| --- | --- | --- |
| Owner | T01 `.env` value diagnosis, window steps 1–5, rotation 1–5 | Owner access to private files, OpenBao and 192.168.0.22 |
| D02 | Old SearXNG credential refused; B route acceptance | Rotation done |
| D06 | Sandbox default selection (REQ-27) | Owner choice against POL-0078 |
| D10 | Task lifecycle states of TSK-0098 to TSK-0114 | None |
| D12 | Final A/B acceptance | Other prompts' results |

##### Blockers and Decisions

The private `.env` diagnosis is blocked for this session by the permission
classifier and is not worked around. Two owner choices were taken in this
chat, as listed under Inputs and Authority.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 172 | W188 | method=automated; tool=Python3 venv; command=secret-structure.py --root "$PWD" check --read-private | `main` 767449bf5, private `.env` | ERROR | exit 2, `{"result": "BLOCKED"}`; `_comment` rejects one private value | required | - |
| E02 | 172 | W188 | method=automated; tool=Python3 venv; command=secret-structure.py --root "$PWD" smtp-equality --read-private | `main` 767449bf5 | PASS | `OLD_ABSENT`, no comparison performed | required | - |
| E03 | 172 | W188 | method=automated; tool=Python3 venv; command=secret-catalog.py --root "$PWD" check | Change | PASS | `P02_METADATA_VALID`, 152 entries, 6 aliases | required | - |
| E04 | 172 | W188 | method=automated; tool=Python3 venv; command=python -m unittest over the 25 OpenBao, secret catalog and secret metadata modules | Change before test updates, system python3 on PATH | FAIL | 22 failures: 15 `referencing` missing, 7 from the removal | required | - |
| E05 | 172 | W188 | method=automated; tool=Python3 venv; command=python -m unittest over the 25 OpenBao, secret catalog and secret metadata modules | Change after test updates, venv on PATH | PASS | 534 tests OK, 15 skipped (opt-in integration, NOT_RUN) | required | E04 |
| E06 | 172 | W188 | method=automated; tool=Python3 venv; command=check-supply-chain-policy.py --check; check-template-security-baseline.sh; check-conftest-policy.sh --mode corpus | Change | PASS | pass; 326 services, 0 findings; 45/45 | required | - |
| E07 | 172 | W188 | method=automated; tool=bash; command=validate-docker-compose.sh; check-all-hardening.sh; check-script-manifest.py | Change | PASS | exit 0; all hardening checks passed; manifest valid | required | - |
| E08 | 172 | W188 | method=observation; tool=-; command=- | HOME runtime | NOT_RUN | Window steps and rotation are owner steps above | required | - |

##### Resolution Links

E05 resolves E04.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 172 | pending | E01,E02,E03,E05,E06,E07,E08 | Source change and findings are recorded; E01 is blocked and E08 waits for the owner window and rotation | @buenhyden |

##### Remaining Conditions

E01 owner diagnosis of the private `.env` value; the owner window steps; the
AI-011/INFRA-008 rotation with old-credential refusal; then owner acceptance.

#### Handoff

##### Promotion Receipt

None: the source change carries its own contract in the OpenBao and
consumer-migration files; no long-lived rule is promoted.

##### Next Owner

The owner runs the window and the rotation and records the results; no other
prompt is started automatically.

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
