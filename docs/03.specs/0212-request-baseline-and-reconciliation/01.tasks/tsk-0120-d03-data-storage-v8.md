---
title: "D03 v8 Data Storage and Shared Valkey Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-26"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0120"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-26"
---

# D03 v8 Data Storage and Shared Valkey Task

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

Own criterion177/W193 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D03 of the lifecycle v8 task prompts: record the data-store census, give
OAuth2 Proxy and Airflow their own shared mng-valkey roles, make the named
n8n account the public default, record the ComfyUI anonymous volume risk, and
switch HOME.

##### Inputs and Authority

On 2026-11-26 the user directly requested D03 from
`_workspace/workspace_task_prompts_20261125_lifecycle_v8/` (prompt
`03_data_storage_valkey.md`), limited to that prompt's scope, with commit,
push, PR and merge after checks. Asked in this chat, the owner chose named
users for OAuth2 Proxy and Airflow, the named n8n account as the default, and
a recorded risk (no data move) for ComfyUI. Work ran on branch
`feat/d03-valkey-named-users` in the linked worktree `.claude/worktrees/d03`
from `main` `5eea53931`, fast-forwarded to `e4d8011a2`; brief `d03-v8` bound
the paths before the first edit. Direct user authorization is authority; this
record is not.

#### Execution Log

##### Work Performed

###### Census

Two read-only source censuses and live observation, values never read.

| Task | Finding | Verdict |
| --- | --- | --- |
| D03-T01 DEV/MNG | No DEV variable feeds an MNG service or the reverse; mng-pg reads `mng_postgres_password` and dev-pg `dev_pg_admin_password`. MNG uses generic `POSTGRES_*`/`VALKEY_*` names, DEV uses `DEV_PG_*`/`DEV_VALKEY_*`; RedisInsight reaches both with separate inspector secrets. `SERVICE_POSTGRES_*` exists only as a negative test. `grafana-db-provision` creates the read-only `grafana_reader` role, not a Grafana metadata database. `mng-pg-init` and `dev-platform-provision` are idempotent | REUSE; E01 |
| D03-T02 Valkey | Live mng-valkey: AOF on, last RDB and AOF writes OK, `noeviction`, 2.6 MB of 128 MB, 0 rejected connections; dev-valkey the same shape. HOME n8n already used the named `n8n` role through the local `.env`, but the public default and OAuth2 Proxy and Airflow logged in as `default` (`~* &* +@all`) | CHANGE_REQUIRED; E02 |
| D03-T03 S3/Qdrant | `seaweedfs-s3` listens on plain HTTP `:8333`; TLS ends at Traefik. The Opsflow worker accepts that contract or `https://seaweedfs-s3:443` with a CA, so the document mention of 443 is not a defect. Opsflow Put/Get readback reuses TSK-0051. Qdrant 1.19.2 has separate admin and read-only keys and an SSO route; Prometheus is the only key consumer besides the evaluation script. The exporter shows one collection though the 2026-11-26 probe recorded its deletion | REUSE; Qdrant collection check open (E08) |
| D03-T04 Storage | Placement matches POL-0102: databases on the HDD (`/home/hyunyoun/storage`), Ollama, Prometheus and Tempo on the SSD; SSD free 59 GB, above the 25 GiB alert; `docker` and `containerd` declare `RequiresMountsFor=/home/hyunyoun/storage`; every writable data bind has `create_host_path: false`. The ComfyUI image declares `VOLUME /root`, so an anonymous 365.4 MB volume holds its code under the named volumes | REUSE; ComfyUI risk recorded (E07) |
| D03-T05 Store set | ADR-0062 item 3 and ADR-0047 decide the HOME stores; clustered stores stay LAB. Terrakube points at mng-valkey with `terrakube_valkey_password`, which has no ACL user; Terrakube is a planned LAB and not running | REUSE; Terrakube left to the LAB move |

###### Change

- `render-acl.sh` always renders `oauth2proxy`
  (`~__Secure-sso-cookie-*`, no channels, DB 0, session and lock commands) and
  `airflow` (`~airflow:*`, the literal Celery pidbox and event patterns, DB 0,
  the commands Celery sends); both need their own secret and refuse a shared
  one. `default` stays for administration, health, backup and rollback.
- OAuth2 Proxy selects `OAUTH2_PROXY_VALKEY_USERNAME`/`_SECRET` (default
  `oauth2proxy`/`mng_valkey_oauth2_proxy_password`, rollback empty user with
  `mng_valkey_password`); both entrypoints refuse any other pairing and set
  `OAUTH2_PROXY_REDIS_USERNAME`.
- Airflow `connection_uri.py` maps `mng_valkey_airflow_password` to user
  `airflow` (default) and keeps `mng_valkey_password` as rollback; Compose
  sets Kombu `global_keyprefix` `airflow:`.
- n8n defaults to `n8n`/`mng_valkey_n8n_password`; the shared pairing stays
  the rollback.
- Catalog entries CACHE-031 and CACHE-032 (CACHE-028 to 030 are reserved
  retired IDs); root secrets, READMEs, GDE-0028, GDE-0053, the n8n runbook and
  the ComfyUI runbook updated.

###### Isolated rehearsal

A throwaway `valkey/valkey:9.1.3-alpine` and Celery from the cached
`hy-home/airflow:3.3.2-keycloak` ran on an internal network with synthetic
secrets. The first run refused PSUBSCRIBE on `airflow:/0.celery.pidbox`:
Valkey matches PSUBSCRIBE patterns literally, so `&airflow:*` does not admit
them. MONITOR captured the channels and commands Celery sends, and the final
rules list them. Containers, their anonymous volumes and the network were
removed.

###### Left open

| Item | Owner | Resume condition |
| --- | --- | --- |
| Empty Qdrant collection `open-webui_knowledge` left by the retired Open WebUI consumer | D11 | Owner decision to delete it |
| Old file `secrets/db/mng-valkey/airflow_password.txt` of the retired dedicated identity | D11 | Owner deletes it after confirming no consumer |
| A single OAuth2 Proxy session key TTL read back | @buenhyden | Needs a role password; the configured cookie_expire is 12h |
| Terrakube Valkey login without an ACL user | LAB move owner | Terrakube leaves HOME or gets its own role |

##### Blockers and Decisions

Files under `secrets/` are outside the agent's read permission, so the owner
edits the public catalog view and creates the secret files. On 2026-11-26 the
owner ran the one-off row script, which added CACHE-031 and CACHE-032 to
`secrets/SENSITIVE_ENV_VARS.md.example` and updated the CACHE-007 and
CACHE-027 purposes (E09).

The path `secrets/db/mng-valkey/airflow_password.txt` belonged to the
retired dedicated identities (`3d0a39084`) and its file still exists. The
generator keeps existing files, so reusing that path would revive a retired
credential; CACHE-032 uses the fresh path
`secrets/db/mng-valkey/airflow_broker_password.txt`, and the old file stays
for D11 cleanup.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 177 | W193 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_dev_data_boundary tests.validation.test_dev_valkey_acl tests.validation.test_mng_pg_init_sql | Branch, 2026-11-26 | PASS | 23 tests OK, 2 skipped | required | - |
| E02 | 177 | W193 | method=observation; tool=Prometheus API; command=query redis_aof_enabled, redis_rdb_last_bgsave_status, redis_aof_last_write_status, redis_memory_used_bytes, redis_memory_max_bytes, redis_rejected_connections_total | HOME mng-valkey and dev-valkey exporters, 2026-11-26 | PASS | AOF 1, RDB and AOF status 1, 2.6 MB and 1.2 MB of 128 MB, 0 rejected | required | - |
| E03 | 177 | W193 | method=automated; tool=docker, valkey 9.1.3, Celery 5.6.3 and kombu 5.6.2; command=isolated worker, send, inspect ping, kill during an acks_late task, restart | Synthetic secrets, internal network, 2026-11-26 | PASS | Task ran, ping answered, the killed task was redelivered and finished; 0 NOPERM in worker log and ACL LOG | required | - |
| E04 | 177 | W193 | method=automated; tool=docker, valkey-cli; command=allow and refuse matrix for oauth2proxy and airflow | Same isolated Valkey | PASS | Own keys, lock script and DB 0 allowed; other prefixes, n8n keys and channels, SCAN, KEYS, FLUSHDB, CONFIG, ACL, SELECT 1, wrong and swapped passwords refused | required | - |
| E05 | 177 | W193 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_mng_valkey_acl tests.validation.test_airflow_connection_uri tests.validation.test_service_runtime_compatibility tests.validation.test_service_wiring_contracts tests.validation.test_p02_valkey_mount_scope | Branch, 2026-11-26 | PASS | 85 tests OK, 3 skipped | required | - |
| E06 | 177 | W193 | method=observation; tool=lsblk, df, docker info, systemctl, docker compose config; command=device, mount, data-root, unit and bind census | HOME host, 2026-11-26 | PASS | Placement equals POL-0102; SSD 59 GB free; RequiresMountsFor set; writable binds create_host_path false | required | - |
| E07 | 177 | W193 | method=observation; tool=docker; command=inspect comfyui mounts and image volumes; system df | HOME host, 2026-11-26 | PASS | Image `VOLUME /root`; anonymous volume 365.4 MB under seven named volumes; runbook records the upgrade step | optional | - |
| E08 | 177 | W193 | method=observation; tool=Qdrant API; command=list collection names and point counts with the read-only key | HOME qdrant | NOT_RUN | Exporter `collections_total` 1; the agent's key read was denied, so the owner runs it | optional | - |
| E09 | 177 | W193 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_secret_catalog_contract tests.validation.test_secret_metadata_sync | Branch with the owner's rows, 2026-11-26 | PASS | 70 tests; the 15 failures and 1 error left are the missing local `referencing` module, the same set as on main | required | - |
| E10 | 177 | W193 | method=automated; tool=bash; command=bash scripts/hardening/check-all-hardening.sh, then the same run with the Airflow key prefix changed and restored | Branch, 2026-11-26 | PASS | All checks passed; the changed prefix failed the new airflow prefix check. The oauth2-proxy checks follow the named secret and username, and the Airflow, n8n and ACL role wiring is now checked | required | - |
| E11 | 177 | W193 | method=automated; tool=Python3.12.3; command=python3 -m scripts.lib.supply_chain.ledger_rebind --write --source-revision 2b7bc69f3; python3 -m unittest tests.lib.supply_chain.test_update_gates tests.lib.supply_chain.test_ledger_rebind tests.validation.test_workflow_version_bundle | Branch, 2026-11-26 | PASS | 22 ledger rows and the n8n source binding re-bound hash-only, the old binding kept in history; the 2026-11-11 review hashes re-bound in release-lookups and the ledger rows; with hashes mapped back, no other value changed; 57 and the bundle tests OK | required | - |
| E12 | 177 | W193 | method=observation; tool=Qdrant API; command=list collection names and point counts with the read-only key | HOME qdrant, run by the owner, 2026-11-26 | PASS | One collection, `open-webui_knowledge`, 0 points: an empty leftover of Open WebUI, which moved to LAB; no D03 or D06 probe collection remains. Not deleted; handed to D11 | optional | E08 |
| E13 | 177 | W193 | method=automated; tool=bash, docker compose 5.6.1; command=gen-secrets.sh --dry-run, --sync-metadata-check, --sync-metadata, run; compose up -d --no-deps --force-recreate mng-valkey | HOME, 2026-11-26, owner ran the generator | PASS | Dry run planned exactly CACHE-031 and CACHE-032 (118 protected, 37 kept); both files mode 640, one link. mng-valkey healthy with six ACL users; db0 keys 18 before and after; the Airflow worker reconnected 6 s after the restart | required | - |
| E14 | 177 | W193 | method=automated; tool=docker compose 5.6.1; command=compose build oauth2-proxy airflow-worker; recreate oauth2-proxy and the five Airflow core services | HOME, 2026-11-26, Airflow queue empty first | PASS | Both images built from cache with no layer download; in-image connection_uri.py and entrypoint equal main; previous images tagged `pre-d03` for rollback. oauth2-proxy mounts only the named secret and its process carries username oauth2proxy; Airflow connects as `redis://airflow:**@mng-valkey` with prefix `airflow:` | required | - |
| E15 | 177 | W193 | method=automated; tool=Airflow CLI, redis-py in airflow-worker; command=trigger example_simplest_dag, then refuse matrix with the broker URL built in process, then restart mng-valkey and trigger again | HOME, 2026-11-26 | PASS | SI-12: the task went scheduler to broker to worker and succeeded; own keys allowed; the oauth2 session key, n8n keys and channel, KEYS, SCAN, FLUSHDB, CONFIG and SELECT 1 refused NOPERM; after the restart the worker reconnected as airflow and the second run succeeded; the DAG is paused again; n8n and oauth2-proxy logged 0 NOPERM or WRONGPASS | required | - |
| E16 | 177 | W193 | method=observation; tool=browser (owner), oauth2-proxy log, Prometheus; command=SSO login on qdrant, sign_out, reopen | HOME, 2026-11-26 06:33 UTC | PASS | SI-05: AuthSuccess through /oauth2/callback, sign_out, then redirect to login; no NOPERM or WRONGPASS in the oauth2-proxy log. A single key's TTL was not read because that needs a role password; the configured cookie_expire is 12h | required | - |
| E17 | 177 | W193 | method=automated; tool=Python3.12.3 project .venv; command=python -m unittest tests.validation.test_secret_metadata_sync tests.validation.test_secret_catalog_contract tests.lib.ops.test_secret_catalog tests.validation.test_smtp_generator tests.validation.test_root_resource_contract tests.validation.test_wiki_preparation_contracts tests.lib.ops.test_openbao_consumer_migration | main `9f549a64e`, 2026-11-26 | PASS | 171 tests OK; the earlier local failures were the system interpreter without `referencing`, not this change | required | - |

##### Resolution Links

E12 resolves E08.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 177 | accepted | E01,E02,E03,E04,E05,E06,E07,E09,E10,E11,E12,E13,E14,E15,E16,E17 | Owner @buenhyden accepted on 2026-11-26 in this chat after the HOME switch and the live SI-05 and SI-12 checks; a single session key TTL was not read back (configured 12h) | @buenhyden |

##### Remaining Conditions

None for criterion 177. The items under Left open stay with their owners:
D11 holds the empty Qdrant collection and the retired secret file, the LAB
move owner holds Terrakube, and @buenhyden holds the TTL readback.

#### Handoff

##### Promotion Receipt

GDE-0028, GDE-0053, the n8n and ComfyUI runbooks and the mng-db, n8n, Airflow
and OAuth2 Proxy READMEs carry the change.

##### Next Owner

Criterion 177 is accepted. D11 holds the Qdrant collection and the retired
secret file; the LAB move owner holds Terrakube.

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
