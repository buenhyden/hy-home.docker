---
title: "D04 v9 Airflow Business Path on 3.4.0 Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-27"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0121"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-27"
---

# D04 v9 Airflow Business Path on 3.4.0 Task

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

Own criterion178/W194 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D04 of the v9 task prompts: reuse the accepted Opsflow installation
(criterion 103), the D03 broker recheck and the Airflow 3.4.0 switch, find
what the 3.4.0 upgrade broke on the business path, fix it, and prove the
publication, retry, replay, restore and storage-permission contract on the
current image in the isolated native rehearsal.

##### Inputs and Authority

On 2026-11-27 the user directly requested D04 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`04_airflow_cdc_analytics.md`), limited to that prompt's scope, with commit,
push, PR and merge after checks. Work ran in the primary checkout on branch
`fix/d04-airflow-340-rehearsal` from clean `main` `85830008e`; brief
`d04-v9-airflow` bound the paths before each edit. The package is an ignored
input, read only. Direct user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Census

| Task | Finding | Verdict |
| --- | --- | --- |
| T01 business DAG | `source_manifest_ingest` is loaded and unpaused on 3.4.0, pool `manifest_ingest` has 1 slot, `/run/opsflow/pg.json` and `s3.json` are mode 0640. No business run exists after the 3.4.0 switch; the last ones are the 2026-11-10 TSK-0051 step 5 runs on 3.3.x | CHANGE_REQUIRED (defect below) |
| T01 3.4.0 defect | The upstream `apache/airflow` 3.4.0 base image sets `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt` in every container; 3.3.2 did not. `PgPublisher.publish` refuses any name in `LIBPQ_ENVIRONMENT`, so on the HOME worker every DB publication would fail with `pg_publish_failed` after the validated object is stored. Reproduced in the live worker without DB I/O: the guard trips on `SSL_CERT_FILE` and clears when it is unset. The value resolves to the same file as OpenSSL's default `openssl_cafile`, so it changes no trust | FIXED |
| T01 rehearsal | The native rehearsal pinned the 3.3.2 candidate (`sha256:8c139ddd…`) while its probe required Airflow 3.4.0 and Celery provider 3.26.0, so no image could pass. Its single-row `task_instance` reads also broke on 3.4.0, which archives each try and inserts a successor row (`prepare_db_for_next_try`) | FIXED |
| T01 OTel | Unchanged; the disabled decision is not reversed for the upgrade alone | REUSE |
| T01 empty input | The current contract requires 1 to MAX records; `records: []` is an explicit `record_count` error with quarantine, not a no-op | REUSE (contract, no schema change) |
| T02 URI and roles | `connection_uri.py` and the named broker user are rechecked in TSK-0120 E20 and E21 on 3.4.0; migrations are unchanged | REUSE |
| T03 Kafka | `kafka-1` runs outside the HOME selection; 7 topics, 0 consumer groups; no HOME service outside `05-messaging` produces or consumes. `_connect-*` and `_schemas` are leftovers of the retired Connect and Schema Registry | OUT_OF_SCOPE for CDC (LAB); leftover topics to D11 |
| T04 analytics | Criterion 70 not-required and 71 accepted stay; no dataset, owner or LAB engine is added | REUSE |
| T05 notifier | The n8n workflow "Operations manifest outbox to Mailpit (DEV draft)" exists and is inactive; criteria 73 to 75 (TSK-0044) stay. A new outbox row would stay pending with no delivery | REUSE |

###### Change

- `workflow_lib/adapters.py`: `_libpq_environment_overrides()` drops
  `SSL_CERT_FILE` from the refused names only when its real path equals
  OpenSSL's default CA file; any other value, `SSL_CERT_DIR` and every `PG*`
  name still refuse before the driver is used.
- `tests/validation/test_opsflow_airflow_contract.py`: new
  `test_default_trust_store_ssl_cert_file_is_not_an_override` (RED before the
  change, GREEN after); the existing poisoned-value case still refuses.
- Native rehearsal: `AIRFLOW_ID`, manifest and config digests pinned to the
  running 3.4.0 image (`7f956efc…`, `b793527e…`, `e4f0f56c…`); the probe
  applies the same default-store exemption; `wait_state`, the retry count and
  the worker identity read the latest try; on a wait failure the receipt keeps
  only enum-shaped states and try counters.

###### Isolated rehearsal

The owned, serial native rehearsal ran three times on the 3.4.0 image. Run 1
stopped at the probe (`SSL_CERT_FILE`). Run 2 stopped at the retry wait and its
receipt showed `failed 1 2`, `failed 2 2`, `failed 3 2`: retries happened, the
single-row read could not see them. Run 3 passed all 17 tests. The companion
images stay as pinned (PostgreSQL 18.6, Valkey 9.1.2, SeaweedFS 4.48), not the
HOME 18.7, 9.1.4 and 4.54.

###### Cleanup

Run 2 reported cleanup FAIL with one container ID retained; the container was
already absent when inspected, no resource carried the owner label, and the
retained attempt directory held only the synthetic input and synthetic
secrets of that attempt. That exact directory was removed. Runs 1 and 3
cleaned up with PASS and retained nothing.

##### Blockers and Decisions

A HOME business run needs a synthetic input under `manifest-input/`, which
only the SeaweedFS admin identity can write; the agent cannot read that
secret. The source fix is live for the bind-mounted worker code, so the owner
check is: upload a new synthetic input for an unused business date, trigger
`source_manifest_ingest` with that date, and read back `ops_flow.runs`,
`published_documents` and `outbox` (RUN-0050 scenario 5 step 5). The notifier
stays inactive, so no mail is sent.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 178 | W194 | method=observation; tool=docker, Airflow CLI; command=dags list, pools list, /run/opsflow listing, n8n list:workflow | HOME, 2026-11-27 | PASS | Census above | required | - |
| E02 | 178 | W194 | method=observation; tool=docker, Python in airflow-worker; command=image env, PID 1 env name, LIBPQ_ENVIRONMENT guard with and without SSL_CERT_FILE, PgPublisher.publish with synthetic identifiers | HOME worker on `hy-home/airflow:3.4.0-keycloak`, 2026-11-27 | FAIL | Guard trips on `SSL_CERT_FILE`; publish refused as `pg_publish_failed` before DB I/O | required | - |
| E03 | 178 | W194 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_opsflow_airflow_contract | Branch with the new default-store case, before the adapter change | FAIL | connect called 0 times | required | - |
| E04 | 178 | W194 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_opsflow_airflow_contract | Branch after the adapter change | PASS | 22 tests OK; poisoned SSL_CERT_FILE still refused | required | E03 |
| E05 | 178 | W194 | method=automated; tool=docker, native fixture; command=OPSFLOW_AIRFLOW_NATIVE_IMAGE=sha256:7f956efc… python3 -m unittest tests.validation.test_opsflow_airflow_native_rehearsal.AirflowNativeRehearsal | Isolated, 2026-11-27, run 1 | FAIL | Probe rejected `SSL_CERT_FILE`; cleanup PASS | required | - |
| E06 | 178 | W194 | method=automated; tool=docker, native fixture; command=OPSFLOW_AIRFLOW_NATIVE_IMAGE=sha256:7f956efc… python3 -m unittest tests.validation.test_opsflow_airflow_native_rehearsal.AirflowNativeRehearsal | Isolated, 2026-11-27, run 2, probe exemption added | FAIL | Retry wait timed out; tries `failed 1 2`, `failed 2 2`, `failed 3 2`; cleanup FAIL, then exact attempt directory removed | required | - |
| E07 | 178 | W194 | method=automated; tool=docker, native fixture; command=OPSFLOW_AIRFLOW_NATIVE_IMAGE=sha256:7f956efc… python3 -m unittest tests.validation.test_opsflow_airflow_native_rehearsal.AirflowNativeRehearsal | Isolated, 2026-11-27, run 3, current-try reads; the same invocation of the whole module also ran the storage-permission rehearsal and 15 boundary tests | PASS | 17 tests OK. Publication: retry reached try 2, replay without a second publication, artifact checksum match, Celery worker identity. Recovery: serial empty PG, S3 and metadata restore with object metadata readback and worker replay. Invalid input quarantined, data_version RED rejected before migration 005. Storage matrix: allowed read and write 200; delete, foreign bucket, prefix and write 403; RED canary caught a permitted delete. Cleanup PASS | required | E05,E06 |
| E08 | 178 | W194 | method=automated; tool=Python3.12.3, ruff; command=python3 -m unittest tests.validation.test_opsflow_airflow_native_rehearsal tests.validation.test_opsflow_airflow_native_scenario tests.validation.test_opsflow_airflow_native_data tests.validation.test_opsflow_airflow_native_evidence tests.validation.test_opsflow_airflow_native_quiescence; ruff check; ruff format --check | Branch | PASS | OK (2 native skipped without the selector) | required | - |
| E09 | 178 | W194 | method=observation; tool=Prometheus API; command=kafka_topic_partitions, kafka_consumergroup_members; Compose reference census | HOME, 2026-11-27 | PASS | 7 topics, 0 consumer groups, no HOME client | optional | - |
| E11 | 178 | W194 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_opsflow_airflow_contract tests.lib.ops.test_opsflow_manifest tests.lib.ops.test_opsflow_adapters tests.lib.ops.test_opsflow_provision_contract | Branch after the adapter change | PASS | 82 tests OK | required | - |
| E10 | 178 | W194 | method=observation; tool=-; command=- | HOME business run on 3.4.0 with a new synthetic input | NOT_RUN | Needs the S3 admin upload (Blockers and Decisions) | required | - |

##### Resolution Links

E04 resolves E03; E07 resolves E05 and E06. E02 is the defect the change
fixes; its live confirmation is E10.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 178 | pending | E01,E02,E03,E04,E05,E06,E07,E08,E11 | Awaiting owner acceptance and the HOME business run (E10) | @buenhyden |

##### Remaining Conditions

- E10: the owner uploads one synthetic input and triggers one HOME run; the
  agent reads back the rows and the object.
- Resolved 2026-11-27 (SPEC-0212 TSK-0052): the rehearsal companions now pin
  the HOME PostgreSQL 18.7, Valkey 9.1.4 and SeaweedFS 4.54, and the native
  rehearsals pass 17/17 on them.
- Timescale, OIDC and a HOME restore are NOT_RUN in the rehearsal scope.

#### Handoff

##### Promotion Receipt

The manifest-pipeline README records the 3.4.0 default-store exemption and
the current-attempt read.

##### Next Owner

The owner runs E10 and decides criterion 178. D09 owns the companion image
pins; D11 owns the leftover Connect and Schema Registry topics. No other
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
