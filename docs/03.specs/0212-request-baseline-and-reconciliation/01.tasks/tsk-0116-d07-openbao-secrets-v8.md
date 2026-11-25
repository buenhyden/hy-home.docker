---
title: "D07 v8 OpenBao and Secret Reconciliation Task"
version: "0.1.3"
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
and metadata read paths; `agent.hcl` loses their four templates (the four
`.ctmpl` files were deleted, then re-added; see the health incident below); `protected-restore-inputs.py` drops them from its
input list; `oidc-client-secrets.sh` and `verify-oidc-client-secret.sh` drop
both services, which the verifier now refuses with exit 2. The digests of
`renderer.hcl`, `protected-renderer-roles.py` and `protected-restore-inputs.py`
are re-pinned in `p01-bootstrap.sh` and `protected-renderer-roles.py`. The
agent-contract counts fall from 19 to 15 templates, and the verifier test
covers the removed services as usage refusals. KV data, `operator.hcl`,
catalog rows IAM-011 and IAM-013 and the dated `update-ledger.json` receipts
are unchanged: the catalog still describes the running Agent, which renders
both until the window.

###### Agent health incident and template re-add

The HOME checkout was fast-forwarded to `0bc8e76de` at 16:00 KST, before the
window. The running Agent kept its old 20-template `agent.hcl` while the
template directory lost four files, so `health-agent.sh` exited 1 from
16:00:49 to 16:02:26 KST (four checks; the fifth retry was not reached, so the
container never turned unhealthy). Rendering and consumers were unaffected.
With the owner's approval the four `.ctmpl` files were restored byte-identical
from `767449bf5` in the HOME working tree; the check returned exit 0 at
16:02:58 with a failing streak of 0. A follow-up change re-adds them to `main`.
They are unused by the new `agent.hcl` and are deleted in step 4 below, after
the Agent runs the new configuration.

###### Owner window order

With the four templates back, a HOME pull no longer breaks the running Agent.
`agent.hcl` is a single-file bind, so the Agent keeps its old template list
until it is recreated.

1. Approve the current `main` as the RUN-0105 window commit and recreate
   `openbao-agent` through `owner-window.sh agent-restart` so it reads the new
   `agent.hcl`.
2. Remove `/openbao/out/open-webui` and `/openbao/out/superset` from the Agent
   output volume; `health-agent.sh` refuses group-readable files it does not
   consume.
3. Write the narrowed `renderer` policy through `protected-renderer-roles.py`
   with the new pin, and confirm the Agent stays healthy.
4. Delete the four unused `openwebui_*` and `superset_*` `.ctmpl` files in a
   follow-up change.
5. Update IAM-011 and IAM-013 delivery in the catalog to match.

###### Window steps run on 2026-11-25

The owner asked in this chat to run the window steps and finish D07. The
renderer issuer helper was installed from `ea699b9db`, the owner removed
`/openbao/out/open-webui` and `/openbao/out/superset` and ran RUN-0103
`agent-restart` through `p01_run`: `issue rc=0`, Agent healthy, and only the
seven current output directories remain. Independently afterwards: the Agent
started 07:46:25Z, is healthy with a failing streak of 0, runs a 16-template
`agent.hcl`, and Keycloak, Grafana, oauth2-proxy, kafbat-ui, Dozzle, Gatus and
the Airflow API server are healthy. Step 4 then deleted the four templates.

Step 5 sets IAM-011 and IAM-013 to the catalog shape for a root secret with no
current consumer, as PG-020 uses: no consumers, `BLOCKED_FACTS`,
`RETAINED_FOR_RECOVERY`, `NO_CHANGE`, no destination binding and no
`kv_path`; consumption is `UNKNOWN` and its evidence pointer null. Import and
delivery stay `CONFIRMED` with their TSK-0014 evidence, because those
deliveries happened; the contract test names both as `DELIVERY_RETIRED`.
`check-views` reports `P02_VIEW_DRIFT` on clean `main` as well, so it is not
from this change.

Not done: step 3, writing the narrowed `renderer` policy, needs the W1 root
token (`roles-apply`), and the operator policy cannot write `sys/policy`. The
running Agent no longer reads the two paths; only the renderer token's right
to read them remains, so the write is left for the next owner window. The two
KV values under `hy-home/08-ai/open-webui` and `hy-home/12-analytics/superset`
stay until the owner approves their deletion (D11).

###### AI-011/INFRA-008 rotation run on 2026-11-25

The first procedure was wrong: it relied on `gen-secrets.sh`, which neither
creates AI-011 (`VERIFY_RUNTIME`) nor rebuilds INFRA-008 (`derived_runtime`).
The owner's first run moved the old value to tmpfs and recreated Traefik
without a change (no secret file changed). The next command ran the old/new
check before a new value existed (old 200, new 401 without a file) and
shredded the tmpfs copy, so the old value no longer exists on server A. The
corrected run at 17:12:57 KST wrote a new random value (0600), rebuilt the
bcrypt htpasswd from stdin (0640) and recreated Traefik (started 08:13:15Z,
healthy). From server A through 192.168.0.13 with the public CA: the new value
in a 0600 netrc returns 200 on `/search`, an invalid Basic credential 401, and
other routes are unchanged. The old-value refusal can only be checked from
192.168.0.22, whose netrc still holds it. `gen-secrets.sh
--sync-metadata-check` reports `files_changed=0`; `--sync-metadata-prune-check`
still rejects its input, as before the rotation (E01). RUN-0110 step 6 now
carries the manual procedure.

###### AI-011/INFRA-008 rotation procedure as first written (superseded)

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
| Owner | T01 `.env` value diagnosis, old SearXNG credential refusal and netrc update on 192.168.0.22, narrowed renderer policy in the next window | Owner access to private files, OpenBao root and 192.168.0.22 |
| D11 | Delete the two retained KV values once approved | Owner approval |
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
| E09 | 172 | W188 | method=observation; tool=docker; command=docker inspect openbao-agent health log | HOME `0bc8e76de`, 16:00–16:02 KST | FAIL | `health-agent.sh` exit 1 four times after the early pull; four templates missing from the directory mount | required | - |
| E10 | 172 | W188 | method=observation; tool=docker; command=docker inspect openbao-agent health log | HOME with the four templates restored from `767449bf5`, 16:02:58 KST | PASS | exit 0, status healthy, failing streak 0 | required | E09 |
| E11 | 172 | W188 | method=observation; tool=owner-window.sh; command=p01_run ea699b9db owner-window.sh agent-restart | Owner run, 2026-11-25 07:46Z | PASS | `issue rc=0`, Agent healthy, seven output directories | required | - |
| E12 | 172 | W188 | method=observation; tool=docker; command=docker inspect and exec on openbao-agent and the seven consumers | After E11 | PASS | 16 templates, no stale output directory, all healthy | required | - |
| E13 | 172 | W188 | method=automated; tool=Python3 venv; command=secret-catalog.py --root "$PWD" check | Template removal and IAM-011/IAM-013 change | PASS | `P02_METADATA_VALID`, 152 entries, 6 aliases | required | - |
| E14 | 172 | W188 | method=automated; tool=Python3 venv; command=python -m unittest over the 25 OpenBao, secret catalog and secret metadata modules | Template removal and IAM-011/IAM-013 change | PASS | 534 OK, 15 skipped (opt-in integration, NOT_RUN) | required | - |
| E15 | 172 | W188 | method=observation; tool=curl, stat, docker; command=new-value netrc on `/search`, invalid Basic, file modes, Traefik health | Server A after the corrected rotation, 17:13 KST | PASS | new 200, invalid 401, files 0600/0640, Traefik healthy | required | - |
| E16 | 172 | W188 | method=observation; tool=curl; command=old-value netrc on `/search` from 192.168.0.22 | Server B | NOT_RUN | Owner check; the old value exists only in that host's netrc | required | - |

##### Resolution Links

E05 resolves E04; E10 resolves E09.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 172 | pending | E01,E02,E03,E05,E06,E07,E08,E10,E11,E12,E13,E14,E15,E16 | Source change, Agent restart, template removal, catalog update and the server A rotation are done; E01 and E16 are open, and the narrowed policy waits for the next window | @buenhyden |

##### Remaining Conditions

E01 owner diagnosis of the private `.env` value; E16, the old-credential
refusal from 192.168.0.22; the narrowed renderer policy in the next root
window; then owner acceptance.

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
