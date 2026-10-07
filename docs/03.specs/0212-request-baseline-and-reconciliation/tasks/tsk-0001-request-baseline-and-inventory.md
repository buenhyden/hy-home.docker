---
title: "Request Baseline and Inventory Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0001"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-07"
---

# Request Baseline and Inventory Task

## Objective

Record the baseline, requirement disposition, per-service-key inventory,
profile probes, conflict map and QA/remote baseline for the 2026-10-07
request, and hand off to the first implementation package.

## Inputs and Authorization

The current user request on 2026-10-07 asks to execute prompt 00 of the
analysis pack in the ignored local `_workspace/rrr/` directory (fifteen items,
additional conditions, `REQUIREMENTS.md`, `GOVERNANCE_CHANGE_MAP.md`,
`SERVICE_REVIEW.md`, `ENVIRONMENT_CONTRACT.md`). The pack's `prompts/`
directory is absent; prompt 00 arrived in the request body. The request
authorizes source, policy and validator changes, per-unit commits and per-Spec
PR merge. It does not supply a HOME runtime target, data target or secret
access; those lanes stay `NOT_RUN`.

Pack statements are dated analysis inputs, not current evidence. Every fact
below was re-observed on 2026-10-07 between 10:40Z and 11:10Z.

## Work Log

### Baseline

| Item | Observed |
| --- | --- |
| Local and remote `main` | `23b0e6959d4f37e8dde6d7d33ffcc0589be32657`, clean tree |
| Pack baseline | same SHA; no drift since the pack was written |
| Pack's previous report baseline | `849ef009a7e0994abb2e7ae7c07c25e1b56732bc` |
| Project-Template `main` | `2583b1e2ea0488c663584841aeaaae2648300af8` (2026-10-06T23:18:08Z) |
| Docker Compose | v5.6.0 |
| Registry issuance | SPEC 211 to 212, ADR 46 to 47 |

### Render Method

All renders use `env -i PATH HOME` so the private root `.env` and the shell
environment are not read. The root uses `docker compose --env-file
.env.example --profile '*' config --format json`. Each LAB uses `docker compose
-f labs/<name>.yml --env-file labs/.env.example --profile '*' config`. Seven
LAB files correctly fail closed on unset required variables. For the inventory
only, `LAB_DATA_DIR`, `LAB_KAFKA_CLUSTER_ID`, `LAB_LOCUST_RESULT_DIR`,
`LAB_LOCUST_SCENARIO_DIR` and `LAB_OPENSEARCH_CERT_DIR` were set to the
synthetic string `synthetic-<name>`. No path was created and nothing was
started. Only keys, names and counts were extracted; no value was recorded.
The scratch generators (`inventory.py` sha256 `523958ab97d8a115…`,
`table.py` `666f224c846f67df…`) are not committed. Reproduce them with the
commands above.

### Profile Probes

| Probe | Command delta | Exit | Services |
| --- | --- | --- | --- |
| P1 no profile | none | 0 | 0 |
| P2 HOME core | `--profile core` | 0 | 8 |
| P3 DEV | `--profile dev` | 0 | 17 |
| P4 quality results | `--profile quality-results` | 0 | 2 |
| P5 unknown profile | `--profile does-not-exist` | 0 | 0 |
| P6 explicit service | `config influxdb`, no profile | 0 | `influxdb` |
| P7 explicit service | `config k6`, no profile | 0 | `k6` |
| P8 root all | `--profile '*'` | 0 | 119 |
| P9 LAB strict | eight files, no synthetic input | 1 for 7, 0 for `mongodb.yml` | 0 / 7 |
| P10 LAB synthetic | eight files | 0 | 42 |

`infra/common-optimizations.yml` contributes only `x-` anchors; no template
became a service key. Root and LAB share zero service names and zero network
names. P5 shows an unknown profile is accepted silently. P6 shows an explicit
service target selects a profiled service, so profiles are not isolation.

### Inventory Summary

161 service keys: 119 root and 42 LAB. Dispositions are `keep` 47,
`preserve+complete` 18, `optional` 53, `lab` 42 and `retire` 1 (`influxdb`).
Source facts that drive follow-on work:

- Only `dev-pg` and `crawl4ai` declare `pids_limit` (2 of 161).
- 39 keys have no health check, including one-shot jobs that should not have one.
- `ollama`, `surrealdb`, three LAB OpenSearch nodes and three LAB `pg-*` nodes
  have no `cap_drop`. `cadvisor` is privileged.
- `nginx` and `traefik` both publish `<HOST_IP>:80` and `:443`, so they cannot
  run together. `alloy`, `loki`, `tempo` and `mng-valkey` publish on the LAN
  IP. Every other published port, including all eight mappings on seven LAB
  keys, binds `127.0.0.1`.
- Backup owners are `pgBackRest` for `mng-pg` and `dev-pg` and an allowlisted
  tree copy for eleven other keys (`infra/09-platform-ops/restic/sets/state-include.txt`). `influxdb` has no backup owner, so
  retirement must check for data before disposal.
- `labs/mongodb.yml` uses named volumes without a required data root, unlike
  the other seven LAB files.

Runtime consumers, image digests, actual UID and measured resources are
`NOT_RUN`. The `depends_on` and Traefik columns are source consumers only.

### Conflict Map

| ID | Current rule and location | Conflict | Change | Owner |
| --- | --- | --- | --- | --- |
| C01 | `bootstrap.md` precedence item 1; `approval-boundaries.md` separate operations | None for source and policy edits; runtime, remote, credential and destructive acts remain per-lane | Confirm only; no rewrite | 12 |
| C02 | `tests/validation/test_infra_tier_layout.py:42-50,294-314` every infra leaf root-included | Retirement must remove leaf, include and expectation together | Change in one commit | 01 |
| C03 | REQ-0005-FR-0001 (`docs/01.requirements/0005-data-analytics.md:49`) requires InfluxDB | Items 01 and 15 | Amend REQ-0005, AD-0004/0012/0019/0024, ADR-0045 list | 01 |
| C04 | POL-0078 profile row `influxdb` (`docs/05.operations/policies/0078-compose-profile-vocabulary.md:79`) | Item 15 | Remove row and its validator input | 01 |
| C05 | GUIDE/POL/RUNBOOK-0017 InfluxDB, GUIDE-0041 Grafana, `infra/04-data/README.md`, Grafana README row | Item 15 | Retire under the retention policy; update catalogs | 01 |
| C06 | `.github/workflow-contract.yml:697,1404`, `test_influx_mapping.py`, `migration/validate_mapping.py` | Item 15 | Transfer any continuing guarantee, then retire | 01 |
| C07 | `infra/tech-stack.versions.json:1112-1128`, `.env.example` Influx keys | Item 15 | Regenerate with the registered generator | 01 |
| C08 | SPEC-0204 Task line 1524 historical Influx PASS | History only | Keep bytes; supersede any open Influx obligation | 01 |
| C09 | `infra/11-quality/conftest/policy/compose.rego:22` treats any `://` value as a reference | Credential-bearing URL can pass | Structured URI/DSN check with positive and negative fixtures | 05 |
| C10 | Probe P6 explicit target selects profiled service | Profile is not isolation | Keep LAB out of root; state it in POL-0078 | 03 |
| C11 | Probe P5 unknown profile accepted silently | Typo selects nothing | Profile vocabulary check in the gate wrapper | 05 |
| C12 | `labs/mongodb.yml` without required data root | Inconsistent fail-closed LAB data | Require root or record exception | 03 |
| C13 | Storybook MCP loopback only (`projects/storybook/nextjs/mcp/server.ts:77`) | Remote use only with proven consumer | Keep default; remote transport needs auth/TLS design | 06 |
| C14 | `infra/common-optimizations.exceptions.json` has per-service entries but `template_adoption.file_exceptions` is empty | Item 14 per-file/per-control exceptions | Schema, reader and Conftest per file/service/control | 05 |
| C15 | Inventory: PIDs 2/161, `cap_drop` gaps, privileged `cadvisor`, duplicate gateway ports | Item 13 | Tiered budgets with exact exceptions | 05, 03 |

### QA and Remote Baseline

On clean `main`, `run-ci-gate.py --profile changed --local-only --explain`
exited 0 with no selection. On this diff the explain selected only
`leaf.docs-traceability`, and the real run passed: 1111 documents, 11127
links, 0 failures and 1 pre-existing historical-link warning in the retention
catalog. Metadata, relationship and lifecycle checks are remote
`candidate-quality` leaves. `run-ci-precommit.sh --mode local-staged` exited
2 with the global pre-commit 4.6.2 ("version does not match the registered
pin"). It passed (exit 0) with the pinned 4.6.1 from
`scripts/requirements-pre-commit.txt`, installed in a scratch `uv` venv. The
user-global tool was not changed.

Remote, read with `gh api` on 2026-10-07: `main` protection has `strict`
true, `contexts` `[]`, `checks` `[]`, required approving reviews 0,
required conversation resolution true, force push and deletion disabled,
`enforce_admins` false. The repository rulesets list is empty. Workflow
`ci-quality.yml` defines `candidate-quality` (pull request) and
`main-security` (push to `main`). At `23b0e6959` the push run of CI Quality
Gates and CodeQL succeeded. Empty required contexts mean candidate checks are
not merge-blocking by protection; they are not a missing workflow. This
package does not change protection.

The first PR #369 candidate run (head `69958e2c2`, run 37612764550) failed:
`metadata check-changed` reported 147 violations. Two were in this package:
a new Task must start at `draft`, and a draft package cannot hold an active
Task. The other 145 were archive `type-mismatch` findings that cascade when
the package is invalid: the spec-lifecycle load fails and the legacy archive
type binding is skipped. The same Registry-triggered check on clean `main`
reports 0. After the Task returned to `draft`, a local
`check-document-metadata.py --mode check-changed` against base `23b0e6959`
reported `violations=0`. An independent read-only review confirmed the
spot-checked facts and raised six wording corrections, all applied.

### Dependencies and Spec Bundles

Order: 12, then 01 and 03, then 02, 04 and 05, then 06 and 07, then 08. 09 and
10 are independent discovery work, and 11 runs at each merge. Each prompt
issues its own Spec number from the Registry when it starts. One writer at a
time owns `docs/99.templates/registry.json`, `docs/03.specs/README.md` and
`.github/workflow-contract.yml`. Prompt 05 alone writes
`infra/common-optimizations*`. The first implementation entry is prompt 12,
whose only confirmed conflict is C01 (confirm only), so 01 can start next.

### Service-Key Inventory

| Service | Owner | Scope | Profiles | User/RO | cap_drop/add | Networks | Host ports | Secrets | depends_on / reverse | Health | CPU/Mem/PIDs | Traefik | Backup | Disposition | Prompt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `airflow-apiserver` | 07-workflow/airflow | root | workflow, workflow-airflow | 1000:0/rw | ALL / - | airflow_net, edge_net, mng_data_net | - | 6 | airflow-init, airflow-valkey / airflow-worker, flower | yes | 2/2048M/- | airflow | - | keep | 04 |
| `airflow-dag-processor` | 07-workflow/airflow | root | workflow, workflow-airflow | 1000:0/rw | ALL / - | airflow_net, mng_data_net | - | 6 | airflow-init, airflow-valkey / - | yes | 2/2048M/- | - | - | keep | 04 |
| `airflow-init` | 07-workflow/airflow | root | workflow, workflow-airflow | 0:0/rw | ALL / - | airflow_net, mng_data_net | - | 6 | - / airflow-apiserver, airflow-dag-processor +5 | no | 0.5/256M/- | - | - | keep | 04 |
| `airflow-scheduler` | 07-workflow/airflow | root | workflow, workflow-airflow | 1000:0/rw | ALL / - | airflow_net, mng_data_net | - | 6 | airflow-init, airflow-valkey / - | yes | 2/2048M/- | - | tree(dags/config/plugins) | keep | 04 |
| `airflow-statsd-exporter` | 07-workflow/airflow | root | workflow, workflow-airflow | -/ro | ALL / - | airflow_net, obs_net | - | 0 | airflow-init / - | no | 0.5/256M/- | - | - | keep | 04 |
| `airflow-triggerer` | 07-workflow/airflow | root | workflow, workflow-airflow | 1000:0/rw | ALL / - | airflow_net, mng_data_net | - | 6 | airflow-init, airflow-valkey / - | yes | 0.5/384M/- | - | - | keep | 04 |
| `airflow-valkey` | 07-workflow/airflow | root | dedicated-valkey | 999:999/rw | ALL / - | airflow_net | - | 1 | - / airflow-apiserver, airflow-dag-processor +5 | yes | 0.5/256M/- | - | - | keep | 04 |
| `airflow-valkey-exporter` | 07-workflow/airflow | root | dedicated-valkey | -/ro | ALL / - | airflow_net, obs_net | - | 1 | airflow-valkey / - | no | 0.5/256M/- | - | - | keep | 04 |
| `airflow-worker` | 07-workflow/airflow | root | workflow, workflow-airflow | 1000:0/rw | ALL / - | airflow_net, mng_data_net | - | 6 | airflow-apiserver, airflow-init +1 / - | yes | 2/2048M/- | - | - | keep | 04 |
| `alertmanager` | 06-observability | root | obs, alerting | -/rw | ALL / - | edge_net, obs_net | - | 3 | grafana, prometheus / - | yes | 0.5/256M/- | alertmanager | - | keep | 02 |
| `alloy` | 06-observability | root | obs, logs, tracing +1 | 473:473/rw | ALL / - | edge_net, obs_net | <HOST_IP>:4317->4317, <HOST_IP>:4318->4318 | 0 | loki, prometheus +1 / - | yes | 1/512M/- | alloy | - | preserve+complete | 02 |
| `analytics` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | 127.0.0.1:4000->4000 | 2 | db / auth, functions +5 | yes | 2/2048M/- | - | - | optional | 03 |
| `auth` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 3 | analytics, db / - | yes | 1/512M/- | - | - | optional | 03 |
| `backup-sqlite-export` | 09-platform-ops/restic | root | backup | 0:0/ro | ALL / DAC_OVERRIDE, CHOWN | - | - | 0 | - / - | no | 0.5/256M/- | - | - | keep | 04 |
| `cadvisor` | 06-observability | root | obs, obs-host, dev | -/rw | ALL / - | edge_net, obs_net | - | 0 | - / - | yes | 1.5/1024M/- | cadvisor | - | keep | 02 |
| `comfyui` | 08-ai/comfyui | root | ai, ai-image | -/rw | ALL / - | edge_net | 127.0.0.1:8188->8188 | 0 | - / - | yes | 2/4096M/- | comfyui | tree(partial) | optional | 05 |
| `conftest` | 11-quality/conftest | root | policy-check | 1000:1000/ro | ALL / - | - | - | 0 | - / - | no | 0.5/256M/- | - | - | preserve+complete | 05 |
| `crawl4ai` | 08-ai/crawl4ai | root | crawl4ai | appuser/ro | ALL / - | crawl4ai_net | - | 1 | - / - | yes | 2/4096M/512 | - | - | preserve+complete | 07 |
| `db` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 2 | vector / analytics, auth +5 | yes | 2/2048M/- | - | - | optional | 03 |
| `dbt` | 12-analytics/dbt | root | analytics-engineering | -/ro | ALL / - | dev_data_net | - | 1 | dbt-db-provision, dev-pg / - | no | 1/512M/- | - | - | preserve+complete | 01 |
| `dbt-db-provision` | 12-analytics/dbt | root | analytics-engineering | -/ro | ALL / - | dev_data_net | - | 2 | dev-pg, dev-platform-provision / dbt | no | 0.5/256M/- | - | - | preserve+complete | 01 |
| `dcgm-exporter` | 06-observability | root | obs-gpu | -/rw | ALL / - | obs_net | - | 0 | - / - | no | 1/512M/- | - | - | keep | 02 |
| `debezium-db-provision` | 05-messaging/kafka | root | cdc | -/ro | ALL / - | dev_data_net | - | 2 | dev-pg, dev-platform-provision / - | no | 0.5/256M/- | - | - | preserve+complete | 01 |
| `dev-perf-provision` | 04-data/dev-db | root | quality-results | -/ro | ALL / - | dev_data_net | - | 1 | dev-pg / - | no | 0.5/256M/- | - | - | preserve+complete | 01 |
| `dev-pg` | 04-data/dev-db | root | dev-data, analytics-engineering, cdc +1 | -/rw | ALL / CHOWN, DAC_OVERRIDE +3 | dev_data_net | 127.0.0.1:25433->5432 | 2 | - / dbt, dbt-db-provision +3 | yes | 2/2048M/256 | - | pgBackRest | preserve+complete | 01 |
| `dev-platform-provision` | 04-data/dev-db | root | analytics-engineering, cdc | -/ro | ALL / - | dev_data_net | - | 4 | dev-pg / dbt-db-provision, debezium-db-provision | no | 1/512M/- | - | - | preserve+complete | 01 |
| `dev-valkey` | 04-data/dev-db | root | dev-data | 999:999/ro | ALL / - | dev_data_net | - | 1 | - / - | yes | 0.5/256M/- | - | - | preserve+complete | 01 |
| `dozzle` | 06-observability/dozzle | root | admin, admin-logs | -/rw | ALL / - | edge_net | - | 1 | - / - | yes | 1/512M/- | dozzle | - | optional | 05 |
| `flink-jobmanager` | 12-analytics/flink | root | lakehouse | 9999:9999/ro | ALL / - | kafka_net, object_net | 127.0.0.1:18091->8081 | 1 | seaweedfs-s3, seaweedfs-table-bucket / flink-taskmanager | yes | 1/1280M/- | - | - | optional | 04 |
| `flink-taskmanager` | 12-analytics/flink | root | lakehouse | 9999:9999/ro | ALL / - | kafka_net, object_net | - | 1 | flink-jobmanager, seaweedfs-s3 +1 / - | no | 2/2048M/- | - | - | optional | 04 |
| `flower` | 07-workflow/airflow | root | workflow, workflow-airflow | 1000:0/rw | ALL / - | airflow_net, edge_net, mng_data_net +1 | - | 6 | airflow-apiserver, airflow-init +1 / - | yes | 0.5/384M/- | flower | - | keep | 04 |
| `functions` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 4 | analytics / - | yes | 2/2048M/- | - | - | optional | 03 |
| `gatus` | 06-observability | root | obs, availability, dev | 1000:1000/rw | ALL / - | edge_net, mng_data_net, obs_net | - | 1 | - / - | yes | 0.5/256M/- | gatus | - | keep | 02 |
| `grafana` | 06-observability | root | obs, obs-core, dev +5 | -/rw | ALL / - | edge_net, mng_data_net, obs_net | - | 3 | loki, prometheus +1 / alertmanager, pushgateway | yes | 1/1024M/- | grafana, grafana-static | - | keep | 01 |
| `grafana-db-provision` | 06-observability | root | obs, obs-core, dev | -/ro | ALL / - | mng_data_net | - | 2 | mng-pg / - | no | 0.5/256M/- | - | - | keep | 02 |
| `great-expectations` | 12-analytics/great-expectations | root | lakehouse | -/ro | ALL / - | object_net | - | 0 | trino / - | no | 1/512M/- | - | - | optional | 04 |
| `imgproxy` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 0 | - / storage | yes | 0.5/256M/- | - | - | optional | 03 |
| `influxdb` | 04-data/influxdb | root | influxdb | -/rw | ALL / - | edge_net | - | 0 | - / - | yes | 1/512M/- | influxdb | - | retire | 01 |
| `jupyterlab` | 12-analytics/jupyterlab | root | data-science | -/rw | ALL / - | ai_net, edge_net | - | 1 | mlflow / - | yes | 2/2048M/- | jupyter | tree | optional | 05 |
| `k6` | 11-quality/k6 | root | testing | -/ro | ALL / - | obs_net | - | 0 | - / - | no | 1/512M/- | - | - | preserve+complete | 02 |
| `kafbat-ui` | 05-messaging/kafka | root | messaging, messaging-admin | -/ro | ALL / - | edge_net, kafka_net | - | 1 | kafka-1, kafka-connect +1 / - | yes | 1/512M/- | kafka-ui | - | optional | 04 |
| `kafka-1` | 05-messaging/kafka | root | messaging, messaging-broker, messaging-schema +4 | -/rw | ALL / - | kafka_net, obs_net | 127.0.0.1:19101->9101, 127.0.0.1:19404->9404 +1 | 0 | - / kafbat-ui, kafka-connect +4 | yes | 2/2048M/- | - | - | optional | 04 |
| `kafka-connect` | 05-messaging/kafka | root | messaging, messaging-connect, messaging-admin +1 | -/ro | ALL / - | dev_data_net, edge_net, kafka_net +1 | - | 1 | kafka-1, schema-registry / kafbat-ui | yes | 2/2048M/- | kafka-connect | - | optional | 04 |
| `kafka-exporter` | 05-messaging/kafka | root | messaging, messaging-broker | -/ro | ALL / - | kafka_net, obs_net | - | 0 | kafka-1 / - | yes | 0.5/256M/- | - | - | optional | 04 |
| `kafka-init` | 05-messaging/kafka | root | messaging, messaging-broker | -/ro | ALL / - | kafka_net | - | 0 | kafka-1 / - | no | 0.5/256M/- | - | - | optional | 04 |
| `kafka-rest-proxy` | 05-messaging/kafka | root | messaging, messaging-rest | -/ro | ALL / - | edge_net, kafka_net | - | 0 | kafka-1, schema-registry / - | yes | 1/512M/- | kafka-rest | - | optional | 04 |
| `keycloak` | 02-auth/keycloak | root | core, auth, dev +1 | -/rw | ALL / - | edge_net, mng_data_net, obs_net | - | 2 | - / - | yes | 2/2048M/- | keycloak | tree | keep | 04 |
| `kong` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | 127.0.0.1:8000->8000, 127.0.0.1:8443->8443 | 3 | - / - | yes | 1/512M/- | - | - | optional | 03 |
| `loki` | 06-observability | root | obs, logs | 10001:10001/rw | ALL / - | edge_net, object_net, obs_net | <HOST_IP>:3100->3100 | 1 | seaweedfs-buckets / alloy, grafana | yes | 2/2048M/- | loki | - | keep | 02 |
| `mailpit` | 11-quality/mailpit | root | dev, local, mail-dev | 1000:1000/rw | ALL / - | edge_net, mail_net | 127.0.0.1:1025->1025, 127.0.0.1:8025->8025 | 0 | - / - | yes | 1/512M/- | mailpit-ui | - | optional | 04 |
| `meta` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 2 | analytics, db / - | yes | 0.5/256M/- | - | - | optional | 03 |
| `mlflow` | 08-ai/mlflow | root | mlops, data-science | -/rw | ALL / - | ai_net, edge_net, mng_data_net +1 | - | 2 | mlflow-db-provision, mng-pg +1 / jupyterlab | yes | 1/1024M/- | mlflow | - | optional | 05 |
| `mlflow-db-provision` | 08-ai/mlflow | root | mlops, data-science | -/ro | ALL / - | mng_data_net | - | 2 | mng-pg, mng-pg-init / mlflow | no | 0.5/256M/- | - | - | optional | 05 |
| `mng-pg` | 04-data/mng-db | root | mng, core, dev +5 | -/rw | ALL / CHOWN, DAC_OVERRIDE +3 | mng_data_net | 127.0.0.1:25432->5432 | 2 | - / grafana-db-provision, mlflow +6 | yes | 1/512M/- | - | pgBackRest+globals | keep | 01 |
| `mng-pg-exporter` | 04-data/mng-db | root | mng, dev | -/ro | ALL / - | mng_data_net, obs_net | - | 1 | mng-pg / - | yes | 0.5/256M/- | - | - | keep | 01 |
| `mng-pg-init` | 04-data/mng-db | root | mng, core, dev +5 | -/ro | ALL / - | mng_data_net | - | 6 | mng-pg / mlflow-db-provision, pact-broker-db-provision +1 | no | 0.5/256M/- | - | - | keep | 01 |
| `mng-valkey` | 04-data/mng-db | root | mng, core, dev +1 | 999:999/rw | ALL / - | mng_data_net | <HOST_IP>:26379->6379 | 1 | - / mng-valkey-exporter | yes | 0.5/256M/- | - | - | keep | 01 |
| `mng-valkey-exporter` | 04-data/mng-db | root | mng, dev | -/ro | ALL / - | mng_data_net, obs_net | - | 1 | mng-valkey / - | yes | 0.5/256M/- | - | - | keep | 01 |
| `n8n` | 07-workflow/n8n | root | workflow, workflow-n8n | -/rw | ALL / - | edge_net, mng_data_net, n8n_net +1 | - | 4 | - / n8n-task-runner, n8n-worker | yes | 2/2048M/- | n8n | tree | preserve+complete | 04 |
| `n8n-task-runner` | 07-workflow/n8n | root | workflow, workflow-n8n | -/rw | ALL / - | n8n_net | - | 1 | n8n, n8n-valkey / - | yes | 0.5/256M/- | - | tree | preserve+complete | 04 |
| `n8n-task-runner-worker` | 07-workflow/n8n | root | workflow, workflow-n8n | -/rw | ALL / - | n8n_net | - | 1 | n8n-worker / - | yes | 0.5/256M/- | - | tree | preserve+complete | 04 |
| `n8n-valkey` | 07-workflow/n8n | root | dedicated-valkey | 999:999/rw | ALL / - | n8n_net | - | 1 | - / n8n-task-runner, n8n-valkey-exporter +1 | yes | 0.5/256M/- | - | - | preserve+complete | 04 |
| `n8n-valkey-exporter` | 07-workflow/n8n | root | dedicated-valkey | -/ro | ALL / - | n8n_net, obs_net | - | 1 | n8n-valkey / - | no | 0.5/256M/- | - | - | preserve+complete | 04 |
| `n8n-worker` | 07-workflow/n8n | root | workflow, workflow-n8n | -/rw | ALL / - | mng_data_net, n8n_net | - | 4 | n8n, n8n-valkey / n8n-task-runner-worker | yes | 2/2048M/- | - | - | preserve+complete | 04 |
| `neo4j` | 04-data/neo4j | root | graph | -/rw | ALL / CHOWN, DAC_OVERRIDE +3 | edge_net | - | 1 | - / - | yes | 1/512M/- | neo4j | - | optional | 04 |
| `nginx` | 01-gateway/nginx | root | nginx | -/ro | ALL / - | edge_net, object_net | <HOST_IP>:443->443, <HOST_IP>:80->80 | 0 | seaweedfs-s3 / - | yes | 0.5/256M/- | - | - | optional | 03 |
| `node-exporter` | 06-observability | root | obs, obs-host, dev | -/ro | ALL / - | obs_net | - | 0 | - / - | yes | 0.5/256M/- | - | - | keep | 02 |
| `oauth2-proxy` | 02-auth/oauth2-proxy | root | core, auth, dev +1 | -/ro | ALL / - | edge_net, mng_data_net, obs_net | - | 4 | - / - | yes | 1/512M/- | oauth2-proxy | - | keep | 04 |
| `oauth2-proxy-valkey` | 02-auth/oauth2-proxy | root | dedicated-valkey | 999:999/rw | ALL / - | mng_data_net | - | 1 | - / oauth2-proxy-valkey-exporter | yes | 0.5/256M/- | - | - | keep | 04 |
| `oauth2-proxy-valkey-exporter` | 02-auth/oauth2-proxy | root | dedicated-valkey | -/ro | ALL / - | mng_data_net, obs_net | - | 1 | oauth2-proxy-valkey / - | no | 0.5/256M/- | - | - | keep | 04 |
| `ollama` | 08-ai/ollama | root | ai, ai-llm, ollama | -/rw | - / - | ai_net, edge_net | 127.0.0.1:11434->11434 | 0 | - / ollama-exporter, open-webui | yes | 4/8192M/- | ollama | - | keep | 05 |
| `ollama-exporter` | 08-ai/ollama | root | ai, ai-llm, ollama | -/ro | ALL / - | ai_net, obs_net | - | 0 | ollama / - | yes | 0.5/256M/- | - | - | keep | 05 |
| `open-webui` | 08-ai/open-webui | root | ai, ai-llm | -/rw | ALL / - | ai_net, edge_net | - | 1 | ollama / - | yes | 2/2048M/- | open-webui | tree(uploads) | keep | 05 |
| `open_notebook` | 08-ai/open-notebook | root | notebook | -/rw | ALL / - | ai_net, edge_net | 127.0.0.1:5055->5055 | 3 | surrealdb / - | yes | 0.5/256M/- | open-notebook | - | optional | 05 |
| `openbao` | 03-security/openbao | root | security, secrets, core +2 | -/rw | ALL / - | edge_net, obs_net, secrets_net | - | 0 | - / openbao-agent | yes | 1/512M/- | openbao | - | keep | 04 |
| `openbao-agent` | 03-security/openbao | root | security, secrets, core +2 | -/rw | ALL / - | secrets_net | - | 0 | openbao / - | yes | 1/512M/- | - | - | keep | 04 |
| `opensearch` | 04-data/opensearch | root | opensearch | -/rw | ALL / - | edge_net, obs_net | - | 4 | - / opensearch-dashboards | yes | 2/2048M/- | opensearch | - | optional | 04 |
| `opensearch-dashboards` | 04-data/opensearch | root | opensearch | -/rw | ALL / - | edge_net | - | 3 | opensearch / - | yes | 1/512M/- | opensearch-dashboards | - | optional | 04 |
| `opentofu` | 09-platform-ops/opentofu | root | iac | -/rw | ALL / - | default | - | 0 | - / - | no | 0.5/256M/- | - | - | optional | 05 |
| `pact-broker` | 11-quality/pact-broker | root | contract-testing | -/ro | ALL / - | mng_data_net | 127.0.0.1:19292->9292 | 2 | mng-pg, pact-broker-db-provision / - | yes | 1/512M/- | - | - | optional | 02 |
| `pact-broker-db-provision` | 11-quality/pact-broker | root | contract-testing | -/ro | ALL / - | mng_data_net | - | 2 | mng-pg, mng-pg-init / pact-broker | no | 0.5/256M/- | - | - | optional | 02 |
| `prometheus` | 06-observability | root | obs, obs-core, dev +2 | -/rw | ALL / - | edge_net, obs_net | - | 3 | - / alertmanager, alloy +2 | yes | 2/2048M/- | prometheus, prometheus-api | - | keep | 02 |
| `pushgateway` | 06-observability | root | obs, batch-metrics | -/ro | ALL / - | edge_net, obs_net | - | 0 | grafana, prometheus / - | yes | 0.5/256M/- | pushgateway | - | keep | 02 |
| `pyroscope` | 06-observability | root | obs, profiling | -/rw | ALL / - | edge_net, obs_net | 127.0.0.1:4040->4040 | 0 | - / - | yes | 1/512M/- | pyroscope | - | keep | 02 |
| `qdrant` | 04-data/qdrant | root | ai, ai-llm, qdrant | 1000:1000/rw | ALL / - | ai_net, edge_net, obs_net | - | 2 | - / - | yes | 1/512M/- | qdrant | - | optional | 04 |
| `realtime` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 3 | analytics, db / - | yes | 1/512M/- | - | - | optional | 03 |
| `redisinsight` | 04-data/redisinsight | root | admin, admin-data | -/rw | ALL / - | airflow_net, edge_net, lab_net +2 | - | 0 | - / - | yes | 1/512M/- | redisinsight, redisinsight-static | - | optional | 05 |
| `registry` | 09-platform-ops/registry | root | tooling, registry | 1000:1000/rw | ALL / - | obs_net | 127.0.0.1:5000->5000 | 0 | - / - | yes | 1/512M/- | - | tree | optional | 05 |
| `renovate` | 09-platform-ops/renovate | root | dependency-update | -/rw | ALL / - | default | - | 1 | - / - | no | 1/1024M/- | - | - | keep | 05 |
| `rest` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 2 | analytics, db / storage | yes | 0.5/256M/- | - | - | optional | 03 |
| `restic` | 09-platform-ops/restic | root | backup | 0:0/ro | ALL / DAC_OVERRIDE | - | - | 1 | - / - | no | 0.5/1024M/- | - | owner | keep | 04 |
| `restic-offsite` | 09-platform-ops/restic | root | backup | 0:0/ro | ALL / DAC_READ_SEARCH | restic_offsite_net | - | 4 | - / - | no | 0.5/1024M/- | - | - | keep | 04 |
| `schema-registry` | 05-messaging/kafka | root | messaging, messaging-schema, messaging-connect +3 | -/ro | ALL / - | edge_net, kafka_net, obs_net | - | 0 | kafka-1 / kafbat-ui, kafka-connect +1 | yes | 1/512M/- | schema-registry | - | optional | 04 |
| `seaweedfs-buckets` | 04-data/seaweedfs | root | seaweedfs, storage-seaweedfs, storage +7 | -/ro | ALL / - | object_net | - | 1 | seaweedfs-s3 / loki, mlflow +3 | no | 0.5/256M/- | - | - | keep | 04 |
| `seaweedfs-filer` | 04-data/seaweedfs | root | seaweedfs, storage-seaweedfs, storage +7 | 1000:1000/rw | ALL / - | seaweed_internal | - | 2 | seaweedfs-master, seaweedfs-volume / seaweedfs-s3 | yes | 1/512M/- | - | fs.meta.save | keep | 04 |
| `seaweedfs-master` | 04-data/seaweedfs | root | seaweedfs, storage-seaweedfs, storage +7 | 1000:1000/rw | ALL / - | seaweed_internal | - | 2 | - / seaweedfs-filer, seaweedfs-volume | yes | 1/512M/- | - | tree | keep | 04 |
| `seaweedfs-s3` | 04-data/seaweedfs | root | seaweedfs, storage-seaweedfs, storage +7 | 1000:1000/rw | ALL / - | edge_net, object_net, seaweed_internal | - | 8 | seaweedfs-filer / flink-jobmanager, flink-taskmanager +5 | yes | 1/512M/- | s3 | - | keep | 04 |
| `seaweedfs-table-bucket` | 04-data/seaweedfs | root | lakehouse | -/ro | ALL / - | object_net | - | 1 | seaweedfs-s3 / flink-jobmanager, flink-taskmanager +2 | no | 0.5/256M/- | - | - | keep | 04 |
| `seaweedfs-volume` | 04-data/seaweedfs | root | seaweedfs, storage-seaweedfs, storage +7 | 1000:1000/rw | ALL / - | seaweed_internal | - | 2 | seaweedfs-master / seaweedfs-filer | yes | 2/2048M/- | - | tree | keep | 04 |
| `sonarqube` | 11-quality/sonarqube | root | tooling, sast | -/rw | ALL / - | edge_net, mng_data_net | - | 1 | - / - | yes | 2/2048M/- | sonarqube | - | optional | 02 |
| `spark` | 12-analytics/spark | root | lakehouse | -/ro | ALL / - | object_net | - | 1 | seaweedfs-s3, seaweedfs-table-bucket / - | no | 2/2048M/- | - | - | optional | 04 |
| `stalwart` | 10-communication/stalwart | root | mail-server | -/ro | ALL / NET_BIND_SERVICE | edge_net, mail_net | - | 1 | - / stalwart-config | yes | 1/512M/- | stalwart-ui | - | optional | 04 |
| `stalwart-config` | 10-communication/stalwart | root | mail-server | 1000:1000/ro | ALL / - | mail_net | - | 1 | stalwart / - | no | 0.5/256M/- | - | - | optional | 04 |
| `storage` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 4 | db, imgproxy +1 / - | yes | 1/512M/- | - | - | optional | 03 |
| `storybook` | 13-experience/storybook | root | experience | 101:101/ro | ALL / - | experience_ingress_net | - | 0 | - / - | yes | 0.5/256M/- | storybook | - | preserve+complete | 06 |
| `studio` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 7 | analytics / - | yes | 1/512M/- | - | - | optional | 03 |
| `supavisor` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | 127.0.0.1:5432->5432, 127.0.0.1:6543->6543 | 4 | analytics, db / - | yes | 1/512M/- | - | - | optional | 03 |
| `superset` | 12-analytics/superset | root | bi | -/ro | ALL / - | edge_net, mng_data_net, object_net | - | 3 | superset-init / - | yes | 1/1024M/- | superset | - | optional | 04 |
| `superset-db-provision` | 12-analytics/superset | root | bi | -/ro | ALL / - | mng_data_net | - | 2 | mng-pg, mng-pg-init / superset-init | no | 0.5/256M/- | - | - | optional | 04 |
| `superset-init` | 12-analytics/superset | root | bi | -/ro | ALL / - | mng_data_net | - | 3 | superset-db-provision / superset | no | 1/512M/- | - | - | optional | 04 |
| `surrealdb` | 08-ai/open-notebook | root | notebook, surrealdb | -/rw | - / - | ai_net | - | 1 | - / open_notebook | yes | 1/512M/- | - | - | optional | 05 |
| `tempo` | 06-observability | root | obs, tracing | 10001:10001/rw | ALL / - | edge_net, object_net, obs_net | <HOST_IP>:3200->3200 | 1 | seaweedfs-buckets / alloy, grafana | yes | 2/2048M/- | tempo | - | keep | 02 |
| `terrakube-api` | 09-platform-ops/terrakube | root | iac | -/rw | ALL / - | edge_net, mng_data_net, object_net +1 | - | 5 | seaweedfs-buckets / terrakube-executor, terrakube-ui | yes | 1/512M/- | terrakube-api | - | optional | 05 |
| `terrakube-executor` | 09-platform-ops/terrakube | root | iac | -/rw | ALL / - | edge_net, mng_data_net, object_net +1 | - | 3 | seaweedfs-buckets, terrakube-api / - | yes | 2/2048M/- | terrakube-executor | - | optional | 05 |
| `terrakube-ui` | 09-platform-ops/terrakube | root | iac | -/rw | ALL / - | edge_net, terrakube_net | - | 0 | terrakube-api / - | yes | 1/512M/- | terrakube-ui | - | optional | 05 |
| `traefik` | 01-gateway/traefik | root | core, dev, local | -/ro | ALL / - | edge_net, experience_ingress_net, obs_net | <HOST_IP>:443->443, <HOST_IP>:80->80 | 3 | - / - | yes | 1/512M/- | dashboard | - | keep | 04 |
| `trino` | 12-analytics/trino | root | lakehouse | -/ro | ALL / - | object_net | 127.0.0.1:18090->8080 | 1 | seaweedfs-s3, seaweedfs-table-bucket / great-expectations | yes | 2/2048M/- | - | - | optional | 04 |
| `vector` | 04-data/supabase | root | supabase | -/rw | ALL / - | supabase_net | - | 0 | - / db | yes | 1/512M/- | - | - | optional | 03 |
| `wiremock` | 11-quality/wiremock | root | api-mock | 1000:1000/ro | ALL / - | default | 127.0.0.1:18088->8080 | 0 | - / - | yes | 1/512M/- | - | - | optional | 02 |
| `cassandra-node1` | labs/cassandra.yml | lab | cassandra | -/rw | ALL / - | lab_cassandra_core_net | - | 0 | - / - | yes | 2/2048M/- | - | - | lab | 03 |
| `couchdb-1` | labs/couchdb.yml | lab | couchdb | -/rw | ALL / - | lab_couchdb_core_net, lab_couchdb_edge_net | - | 2 | - / couchdb-cluster-init | yes | 1/512M/- | couchdb | - | lab | 03 |
| `couchdb-2` | labs/couchdb.yml | lab | couchdb | -/rw | ALL / - | lab_couchdb_core_net, lab_couchdb_edge_net | - | 2 | - / couchdb-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `couchdb-3` | labs/couchdb.yml | lab | couchdb | -/rw | ALL / - | lab_couchdb_core_net, lab_couchdb_edge_net | - | 2 | - / couchdb-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `couchdb-cluster-init` | labs/couchdb.yml | lab | couchdb | -/ro | ALL / - | lab_couchdb_core_net | - | 1 | couchdb-1, couchdb-2 +1 / - | no | 0.5/256M/- | - | - | lab | 03 |
| `lab-kafka-1` | labs/kafka-cluster.yml | lab | lab-kafka | -/rw | ALL / - | lab_kafka_net | - | 0 | - / lab-kafka-exporter, lab-kafka-init | yes | 0.75/1536M/- | - | - | lab | 03 |
| `lab-kafka-2` | labs/kafka-cluster.yml | lab | lab-kafka | -/rw | ALL / - | lab_kafka_net | - | 0 | - / lab-kafka-exporter, lab-kafka-init | yes | 0.75/1536M/- | - | - | lab | 03 |
| `lab-kafka-3` | labs/kafka-cluster.yml | lab | lab-kafka | -/rw | ALL / - | lab_kafka_net | - | 0 | - / lab-kafka-exporter, lab-kafka-init | yes | 0.75/1536M/- | - | - | lab | 03 |
| `lab-kafka-exporter` | labs/kafka-cluster.yml | lab | lab-kafka | -/ro | ALL / - | lab_kafka_net | - | 0 | lab-kafka-1, lab-kafka-2 +1 / - | yes | 0.5/256M/- | - | - | lab | 03 |
| `lab-kafka-init` | labs/kafka-cluster.yml | lab | lab-kafka | -/ro | ALL / - | lab_kafka_net | - | 0 | lab-kafka-1, lab-kafka-2 +1 / - | no | 0.5/256M/- | - | - | lab | 03 |
| `lab-locust-master` | labs/locust.yml | lab | lab-locust | -/ro | ALL / - | lab_locust_net | - | 0 | - / lab-locust-worker | yes | 1/512M/- | - | - | lab | 02 |
| `lab-locust-worker` | labs/locust.yml | lab | lab-locust | -/ro | ALL / - | lab_locust_net | - | 0 | lab-locust-master / - | yes | 1/512M/- | - | - | lab | 02 |
| `mongo-express` | labs/mongodb.yml | lab | mongodb | -/ro | ALL / - | lab_mongodb_core_net, lab_mongodb_edge_net | - | 2 | mongo-init / - | no | 0.5/256M/- | mongo-express | - | lab | 03 |
| `mongo-init` | labs/mongodb.yml | lab | mongodb | -/ro | ALL / - | lab_mongodb_core_net | - | 1 | mongodb-arbiter, mongodb-rep1 +1 / mongo-express, mongodb-exporter | no | 0.5/256M/- | - | - | lab | 03 |
| `mongo-key-generator` | labs/mongodb.yml | lab | mongodb | -/rw | ALL / - | - | - | 0 | - / mongodb-arbiter, mongodb-rep1 +1 | no | 0.5/256M/- | - | - | lab | 03 |
| `mongodb-arbiter` | labs/mongodb.yml | lab | mongodb | -/rw | ALL / - | lab_mongodb_core_net | - | 0 | mongo-key-generator / mongo-init | yes | 0.5/256M/- | - | - | lab | 03 |
| `mongodb-exporter` | labs/mongodb.yml | lab | mongodb | -/ro | ALL / - | lab_mongodb_core_net, lab_mongodb_obs_net | - | 1 | mongo-init / - | no | 0.5/256M/- | - | - | lab | 03 |
| `mongodb-rep1` | labs/mongodb.yml | lab | mongodb | -/rw | ALL / - | lab_mongodb_core_net | - | 1 | mongo-key-generator / mongo-init | yes | 2/2048M/- | - | - | lab | 03 |
| `mongodb-rep2` | labs/mongodb.yml | lab | mongodb | -/rw | ALL / - | lab_mongodb_core_net | - | 1 | mongo-key-generator / mongo-init | yes | 2/2048M/- | - | - | lab | 03 |
| `lab-opensearch-dashboards` | labs/opensearch-cluster.yml | lab | opensearch-cluster | -/rw | ALL / - | lab_opensearch_core_net | - | 2 | opensearch-node1, opensearch-node2 +1 / - | yes | 1/512M/- | - | - | lab | 03 |
| `opensearch-node1` | labs/opensearch-cluster.yml | lab | opensearch-cluster | -/rw | - / IPC_LOCK | lab_opensearch_core_net | - | 3 | - / lab-opensearch-dashboards | yes | 2/2048M/- | - | - | lab | 03 |
| `opensearch-node2` | labs/opensearch-cluster.yml | lab | opensearch-cluster | -/rw | - / IPC_LOCK | lab_opensearch_core_net | - | 3 | - / lab-opensearch-dashboards | yes | 2/2048M/- | - | - | lab | 03 |
| `opensearch-node3` | labs/opensearch-cluster.yml | lab | opensearch-cluster | -/rw | - / IPC_LOCK | lab_opensearch_core_net | - | 3 | - / lab-opensearch-dashboards | yes | 2/2048M/- | - | - | lab | 03 |
| `etcd-1` | labs/postgresql-ha.yml | lab | postgres-ha | -/rw | ALL / - | lab_pg_core_net, lab_pg_obs_net | - | 0 | - / pg-0, pg-1 +1 | yes | 0.5/256M/- | - | - | lab | 03 |
| `etcd-2` | labs/postgresql-ha.yml | lab | postgres-ha | -/rw | ALL / - | lab_pg_core_net, lab_pg_obs_net | - | 0 | - / pg-0, pg-1 +1 | yes | 0.5/256M/- | - | - | lab | 03 |
| `etcd-3` | labs/postgresql-ha.yml | lab | postgres-ha | -/rw | ALL / - | lab_pg_core_net, lab_pg_obs_net | - | 0 | - / pg-0, pg-1 +1 | yes | 0.5/256M/- | - | - | lab | 03 |
| `pg-0` | labs/postgresql-ha.yml | lab | postgres-ha | -/rw | - / - | lab_pg_core_net | - | 3 | etcd-1, etcd-2 +1 / pg-0-exporter, pg-router | yes | 2/2048M/- | - | - | lab | 03 |
| `pg-0-exporter` | labs/postgresql-ha.yml | lab | postgres-ha | -/ro | ALL / - | lab_pg_core_net, lab_pg_obs_net | - | 1 | pg-0 / - | yes | 0.5/256M/- | - | - | lab | 03 |
| `pg-1` | labs/postgresql-ha.yml | lab | postgres-ha | -/rw | - / - | lab_pg_core_net | - | 3 | etcd-1, etcd-2 +1 / pg-1-exporter, pg-router | yes | 2/2048M/- | - | - | lab | 03 |
| `pg-1-exporter` | labs/postgresql-ha.yml | lab | postgres-ha | -/ro | ALL / - | lab_pg_core_net, lab_pg_obs_net | - | 1 | pg-1 / - | yes | 0.5/256M/- | - | - | lab | 03 |
| `pg-2` | labs/postgresql-ha.yml | lab | postgres-ha | -/rw | - / - | lab_pg_core_net | - | 3 | etcd-1, etcd-2 +1 / pg-2-exporter, pg-router | yes | 2/2048M/- | - | - | lab | 03 |
| `pg-2-exporter` | labs/postgresql-ha.yml | lab | postgres-ha | -/ro | ALL / - | lab_pg_core_net, lab_pg_obs_net | - | 1 | pg-2 / - | yes | 0.5/256M/- | - | - | lab | 03 |
| `pg-cluster-init` | labs/postgresql-ha.yml | lab | postgres-ha | -/ro | ALL / - | lab_pg_core_net | - | 3 | pg-router / - | no | 0.5/256M/- | - | - | lab | 03 |
| `pg-router` | labs/postgresql-ha.yml | lab | postgres-ha | -/ro | ALL / - | lab_pg_core_net, lab_pg_edge_net, lab_pg_obs_net | 127.0.0.1:35432->15432, 127.0.0.1:35433->15433 | 1 | pg-0, pg-1 +1 / pg-cluster-init | yes | 1/512M/- | haproxy-stats | - | lab | 03 |
| `valkey-cluster-exporter` | labs/valkey-cluster.yml | lab | valkey-cluster | -/ro | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | - | 1 | valkey-node-0, valkey-node-1 +4 / - | yes | 0.5/256M/- | - | - | lab | 03 |
| `valkey-cluster-init` | labs/valkey-cluster.yml | lab | valkey-cluster | -/ro | ALL / - | lab_valkey_core_net | - | 1 | valkey-node-0, valkey-node-1 +4 / - | no | 0.5/256M/- | - | - | lab | 03 |
| `valkey-node-0` | labs/valkey-cluster.yml | lab | valkey-cluster | -/rw | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | 127.0.0.1:17379->6379 | 1 | - / valkey-cluster-exporter, valkey-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `valkey-node-1` | labs/valkey-cluster.yml | lab | valkey-cluster | -/rw | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | 127.0.0.1:17380->6380 | 1 | - / valkey-cluster-exporter, valkey-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `valkey-node-2` | labs/valkey-cluster.yml | lab | valkey-cluster | -/rw | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | 127.0.0.1:17381->6381 | 1 | - / valkey-cluster-exporter, valkey-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `valkey-node-3` | labs/valkey-cluster.yml | lab | valkey-cluster | -/rw | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | 127.0.0.1:17382->6382 | 1 | - / valkey-cluster-exporter, valkey-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `valkey-node-4` | labs/valkey-cluster.yml | lab | valkey-cluster | -/rw | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | 127.0.0.1:17383->6383 | 1 | - / valkey-cluster-exporter, valkey-cluster-init | yes | 1/512M/- | - | - | lab | 03 |
| `valkey-node-5` | labs/valkey-cluster.yml | lab | valkey-cluster | -/rw | ALL / - | lab_valkey_core_net, lab_valkey_obs_net | 127.0.0.1:17384->6384 | 1 | - / valkey-cluster-exporter, valkey-cluster-init | yes | 1/512M/- | - | - | lab | 03 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Source baseline | 1 | W1 | `git rev-parse HEAD origin/main`; `gh api` Project-Template commit | main `23b0e6959` | PASS | Baseline | accepted |
| Requirement disposition | 2 | W2 | Pack REQUIREMENTS against current source | 15 items + A1-A4 | PASS | SPEC-0212 Contract 1 | accepted |
| Inventory render | 3 | W3 | Root and eight LAB renders | `.env.example`; synthetic LAB vars | PASS | Service-Key Inventory | accepted |
| Profile probes | 4 | W3 | P1-P10 | `.env.example` | PASS | Profile Probes | accepted |
| Conflict map and ADR | 5 | W4 | `git grep` and source reads | main `23b0e6959` | PASS | Conflict Map; ADR-0047 | accepted |
| QA and remote baseline | 6 | W5 | Gate explain; branch protection; rulesets | main `23b0e6959` | PASS | QA and Remote Baseline | accepted |
| Local change validation | 6 | W5 | `run-ci-gate.py --profile changed --local-only`; `run-ci-precommit.sh --mode local-staged` with pinned pre-commit 4.6.1 (global 4.6.2 exits 2) | This diff, seven files | PASS | QA and Remote Baseline | accepted |
| Remote candidate | 6 | W5 | PR `candidate-quality` | Head `69958e2c2` | FAIL | QA and Remote Baseline | rejected |
| Remote candidate rerun | 6 | W5 | PR `candidate-quality` | Corrected head | NOT_RUN | Pending PR rerun | pending |
| HOME runtime state | 3 | W3 | Container, digest, UID and resource observation | No target authorized | NOT_RUN | Not observed | pending |

## Review and Completion

Not complete. Local validation passed; the remote PR candidate result is pending.
HOME runtime observation is outside this package and stays `NOT_RUN`.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0047](../../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
