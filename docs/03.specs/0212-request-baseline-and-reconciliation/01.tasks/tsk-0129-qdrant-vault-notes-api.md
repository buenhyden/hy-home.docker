---
title: "blog-data Qdrant vault-notes Route Task"
version: "0.1.2"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0129"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-28"
---

# blog-data Qdrant vault-notes Route Task

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

Own criterion186/W202 in the [Spec](../spec.md) and [Plan](../plan.md):
request 1 of the blog-data request to server A (2026-11-28), machine access
to Ollama and to one Qdrant collection for blog-data on server B.

##### Inputs and Authority

On 2026-11-28 the user shared the blog-data request page and, asked in this
chat, chose: do request 1 and request 2, give the plugin a separate
collection-scoped JWT instead of sharing `qdrant_read_only_api_key`, and let
blog-data reuse the existing server-B `ollama-api` account. The owner added
the three value-free registry template rows. Work ran in the primary checkout
on branch `feat/qdrant-vault-notes-api` from `main` `e8632820d`; brief
`qdrant-vault-api` bound the changed files. No secret value was read, written
or printed. Direct user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Changes

| Area | Change |
| --- | --- |
| Ollama | None: blog-data uses `AI-012` and `AI-013`, documented for programs on server B (RUN-0056) |
| Qdrant route | `qdrant-api` router: `Authorization: Basic` and exactly `/collections/vault-notes`, `/index`, `/points`, `/points/scroll`, `/points/query` and `/points/delete`; middlewares `blog-export-windows`, `gateway-standard-chain`, `qdrant-api-auth`. The requested `PathPrefix` would also have routed the collection snapshot and shard APIs, so exact paths replace it |
| Middleware | `qdrant-api-auth` basicAuth from `/run/secrets/traefik_qdrant_api_htpasswd` with `removeHeader: true`, so Qdrant sees only its `api-key` header |
| Qdrant | `QDRANT__SERVICE__JWT_RBAC: 'true'`; the API key and read-only key keep working and a `vault-notes` read token is signed with `qdrant_api_key`, so no new secret is stored |
| Secrets | Root secret `traefik_qdrant_api_htpasswd`; catalog `INFRA-010` (derived), `AI-014` (`QDRANT_API_USERNAME`), `AI-015`; `gen-secrets.sh` derives `INFRA-010`; registry template rows added by the owner |
| Docs | RUN-0034 Remote Program Access (owner password, htpasswd, JWT minting, OpenBao delivery, checks, rollback); GDE-0034, the Qdrant and Traefik READMEs, GDE-0013 and GDE-0079 tables |
| Ledger | `ledger_rebind --write` re-bound the qdrant and traefik rows |
| Runbook fix | The owner's first token run stopped at `heredoc>` because the indented list code block carried spaces before `PY`; the blocks are now top-level and unindented, step 1 adds the `.env` username, step 2 keeps an existing password and reports a missing username, and delivery follows the RUN-0110 SSH-to-file pattern because HOME OpenBao has no delivery path to server B |

##### Blockers and Decisions

The route is source-only until the owner sets `QDRANT_API_USERNAME`, creates
`AI-015` and `INFRA-010`, recreates Traefik and Qdrant and mints the read token
(RUN-0034 steps 1 to 3). blog-data's indexing CLI gets `qdrant_api_key` as
requested; a collection read-write JWT is the lower-privilege alternative and
needs the owner to create the collection and its index once.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 186 | W202 | method=automated; tool=Python3 venv; command=python -m unittest test_compose_baseline_gates.OllamaPortContractTests.test_blog_data_reaches_only_vault_notes_with_basic_from_server_b | Qdrant Compose change stashed | FAIL | KeyError on the missing router | required | - |
| E02 | 186 | W202 | method=automated; tool=Python3 venv; command=python -m unittest test_compose_baseline_gates.OllamaPortContractTests.test_blog_data_reaches_only_vault_notes_with_basic_from_server_b | With the change | PASS | OK | required | E01 |
| E03 | 186 | W202 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_compose_baseline_gates | Branch | PASS | 148 tests, 29 skipped | required | - |
| E04 | 186 | W202 | method=automated; tool=Python3; command=python3 -m unittest tests.validation.test_secret_metadata_sync.PublicSecretSchemaTests | Branch with the owner template rows | PASS | OK; the generator tests need the `referencing` module absent locally and run in hosted CI | required | - |
| E05 | 186 | W202 | method=automated; tool=bash; command=validate-docker-compose.sh; ledger_rebind --write | Branch | PASS | Compose valid; 2 rows re-bound | required | - |
| E07 | 186 | W202 | method=automated; tool=bash, zsh; command=bash -n and zsh -n of each RUN-0034 Remote Program Access block | Runbook after the paste-safety fix | PASS | 3 blocks parse, no indented line | required | - |
| E08 | 186 | W202 | method=observation; tool=stat, docker, curl, Prometheus API; command=file modes; traefik secret mount; qdrant JWT_RBAC env; up{job=qdrant}; curl from server A with no and dummy Basic credentials; qdrant log since restart | HOME, 2026-11-28 15:29 KST after the owner ran RUN-0034 steps 1 to 3 | PASS | Password 0600 and htpasswd 0640 present and mounted; traefik and qdrant healthy, JWT RBAC on; Prometheus up=1; /collections/vault-notes 302 without Basic and 403 with Basic from server A; /collections and /collections/vault-notes/snapshots 302; ollama-api still 401 on dummy Basic; no rejected request in the Qdrant log | required | - |
| E09 | 186 | W202 | method=observation; tool=stat, docker logs; command=qdrant_api_key size; qdrant startup warning | HOME, 2026-11-28 | FAIL | qdrant_api_key is 16 bytes and Qdrant warns it should be 32 bytes once it signs JWTs | required | - |
| E06 | 186 | W202 | method=observation; tool=-; command=RUN-0034 step 4 checks from server B and server A | After owner provisioning | NOT_RUN | Owner provisioning pending | required | - |

##### Resolution Links

E02 resolves E01. E06 runs after the owner provisioning.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 186 | pending | E01,E02,E03,E04,E05,E06,E07,E08,E09 | Awaiting owner provisioning, the runtime checks and acceptance | @buenhyden |

##### Remaining Conditions

- E09: rotate `qdrant_api_key` to 32 bytes or more before the values reach
  blog-data, then mint the read token again.
- Step 4 delivery and the server B table from blog-data (E06).

#### Handoff

##### Promotion Receipt

The procedure is promoted to RUN-0034 and the route to the Qdrant README.

##### Next Owner

The owner provisions the credentials and decides criterion186.

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
