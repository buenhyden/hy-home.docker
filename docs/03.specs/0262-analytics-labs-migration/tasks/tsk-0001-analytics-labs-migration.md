---
title: "Analytics Labs Migration Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0262-TSK-0001"
parent_ids:
- "SPEC-0262-PLAN-0001"
created: "2026-11-04"
---

# Analytics Labs Migration Task

## Overview

### Objective

Move the OPTIONAL analytics services, SonarQube and Stalwart from the root
Compose into standalone LAB entrypoints and reconcile every current reference.

## Inputs and Authorization

On 2026-11-04 the owner decided to move these OPTIONAL services out of the
root Compose into `labs/`: the lakehouse bundle (`spark`, `flink-jobmanager`,
`flink-taskmanager`, `trino`, `great-expectations`, `seaweedfs-table-bucket`),
`dbt` with `dbt-db-provision`, `superset` with `superset-init` and
`superset-db-provision`, and `jupyterlab`. Kafka and all `05-messaging`
services, `mlflow` and `mlflow-db-provision`, the SeaweedFS master, volume,
filer, S3 and bucket job, `mng-pg`, `dev-pg` and Keycloak stay in the root.

The same day the owner added a second decision, "sonarqube, stalwart 도 labs로
이전": `sonarqube` and `stalwart` with `stalwart-config` also move. `mng-pg-init`,
its SonarQube role and database provisioning and the root
`sonarqube_db_password` secret stay unchanged; Mailpit and `mail_net` stay.

Evidence gathered before the change: none of the moved services has a
consumer outside its own cluster; all are OPTIONAL in the lifecycle ledger
`docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`;
Airflow, n8n, Opsflow and scripts do not call them at runtime, and the Opsflow
notifier rejects host `stalwart` and sends only to Mailpit. This Task pushes,
merges and starts nothing.

## Work Log

### Current contract decision

The owner decisions authorize this Spec and Plan as written.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0262 | draft | approved | #current-contract-decision |
| SPEC-0262-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0262-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0262-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Decisions

- Grouping: one LAB per Stage 05 document set, `labs/lakehouse.yml`,
  `labs/dbt.yml`, `labs/superset.yml`, `labs/jupyterlab.yml`,
  `labs/sonarqube.yml` and `labs/stalwart.yml`. Assets moved with `git mv` to
  `labs/lakehouse/{spark,flink,trino,great-expectations}/`,
  `labs/lakehouse/seaweedfs-table-bucket.sh`, `labs/dbt/`, `labs/superset/`,
  `labs/jupyterlab/`, `labs/sonarqube/` and `labs/stalwart/`. The Stage 05
  guides bind each LAB through `implementation_services`, so no separate
  `labs/<name>.md` guide was added.
- HOME reachability (owner to confirm): SPEC-0215 forbids a LAB from sharing a
  root network (`test_lab_isolation`, `lab.py` collision checks), and no
  existing LAB reaches a HOME service over a network. The smallest documented
  option chosen: each LAB has its own network and takes each HOME dependency
  as a required `LAB_*` endpoint input (`LAB_LAKEHOUSE_S3_ENDPOINT`,
  `LAB_LAKEHOUSE_CATALOG_URI`, `LAB_DBT_DB_HOST`, `LAB_SUPERSET_DB_HOST`,
  `LAB_SUPERSET_DEFAULT_URL`, `LAB_SUPERSET_CA_FILE`, `LAB_SONARQUBE_DB_HOST`,
  optional `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`). HOME publishes none of these
  services to a LAB network, so these LABs are render-only until the owner
  approves a reachable endpoint or a SPEC-0215 amendment. Stalwart needs no
  HOME service.
- Secrets: the secret contract allows canonical root secret paths only for the
  Supabase LAB, so the new LABs declare LAB-only `lab_<lab>_*` secrets under
  `${LAB_SECRET_DIR:-../secrets/labs}/<lab>/`, mounted at the original
  `/run/secrets` names. No value was copied; the operator must provision LAB
  copies (including copies of HOME database passwords and SeaweedFS keys) under
  a separate approval. OpenBao KV paths such as `hy-home/12-analytics/superset`
  are logical names and stay; renaming one is a runtime migration.
- Gateway: no LAB has a Traefik route. Superset, JupyterLab, SonarQube and the
  Stalwart admin UI publish on `LAB_HOST_BIND_IP` (default `127.0.0.1`) ports
  18092, 18888, 18094 and 18093; Trino and Flink stay on literal loopback
  18090 and 18091. The Keycloak client `home-superset` still registers the old
  gateway redirect; a LAB login needs an owner-approved redirect. The Superset
  OpenBao Agent bind was dropped.
- Data: Flink checkpoints, notebooks, SonarQube data and logs and the Stalwart
  datastore bind under `LAB_DATA_DIR`. No data was moved.
- Profiles: LAB profiles that the root also declares were renamed to avoid the
  operations catalog `compose-lab-profile-overlap` finding: `lab-lakehouse`,
  `lab-dbt`, `lab-superset`, and `sast` only for SonarQube; JupyterLab uses
  `jupyterlab` and Stalwart keeps `mail-server`.
  The root `lakehouse`, `bi` and `data-science` profiles keep selecting only
  their HOME base services; `data-science` now means MLflow and its
  provisioner.
- Requirements: REQ-0012 (FR-0002, FR-0004), REQ-0011 (FR-0002), REQ-0010
  (FR-0002), REQ-0005 and REQ-0006 were amended in place with a minor version
  bump and stay `approved`. The Registry permits only `approved` to
  `in-review`; the amendments restate the owner's 2026-11-04 decisions and add
  no new obligation, so no transition was recorded. If the owner wants the
  amended wording re-reviewed, the registered path is `approved` to
  `in-review` to `approved`; that confirmation is open below.
- The infra tiers `10-communication` and `12-analytics` keep only a README,
  because ADR-0046 registers the tier names.
- The supply-chain ledger moved the 15 rows to `historical_lab_entries`, as
  for Supabase, with a new `source_refreshes` record.

### Changed

- `42413743a`: this package, the Registry `spec` high-water 262 and next
  263, the specs index row, and the new LAB asset README paths in the
  Registry.
- `d109d7f58`: six `labs/*.yml` entrypoints, assets moved with `git mv`, root
  includes, the `seaweedfs-table-bucket` service, root secrets and example
  inputs only the moved services used, `labs/.env.example`, the LAB and infra
  READMEs.
- `96f23d8f5`: hardening tiers 10, 11 and 12 read the LAB sources; tier
  layout, LAB isolation, secret, wiring and the opt-in rehearsal tests; the
  metadata check finds an Operations predecessor moved between two numbered
  families of the same role.
- `24eb479af`: secret catalog LAB rows and retired root rows, the
  secret-file support table, the OpenBao consumer note and the update ledger.
- `88806a761`: 18 Stage 05 documents moved into `15-labs`, their indexes, the
  profile vocabulary, the other Stage 05, Stage 01 and Stage 02 statements, and
  the m0021 inventory rows and its Stalwart link.
- `db86e8c95`: the link check resolves a historical link from a terminal Task
  across a numbered family move, so the completed SPEC-0204 TSK-0009 body
  stays unchanged; feature provisioning, Trino and Grafana inventory tests.

### Open issues

- Owner: approve reachable endpoints (or a SPEC-0215 amendment) before any LAB
  that needs HOME runs; provision LAB secret copies; approve a Superset LAB
  redirect URI; confirm the amended requirement wording.
- BLOCKED: the public registry `secrets/SENSITIVE_ENV_VARS.md.example` must
  gain rows LAB-026 to LAB-036 and the renamed `LAB_*_DB_USER` keys of PG-011,
  PG-024 and PG-029 to match the catalog. The file is under `secrets/`, and the
  permission classifier refused the edit, so it needs the owner's own change or
  approval. Until then 16 `test_secret_metadata_sync` tests and one
  `test_secret_catalog_contract` test fail.
- The local Python has jsonschema 4.10.3 without the `referencing` module, so
  catalog schema checks error here (one catalog test, the SMTP generator
  dry run, and two modules that fail to import); a supported environment must
  rerun them.
- `lab.py check` needs the root `.env`, which this worktree has not and the
  Task must not read; it was not run.
- Hosted CI has not run.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | compose-root | `docker compose --env-file .env.example config -q` and `--profile '*' config --services` on `db86e8c95` | PASS | exit 0; services 112 before, 97 after, the 15 moved services exactly | required | - |
| E2 | 2 | W1 | compose-lab | six `labs/*.yml` rendered with `--profile '*' config -q` and synthetic `LAB_*` inputs on `db86e8c95` | PASS | all six exit 0; 15 services | required | - |
| E3 | 2 | W1 | lab-isolation | `python3 -m unittest tests.validation.test_lab_isolation`, `test_infra_tier_layout` within the 12-module run on `db86e8c95` | PASS | no failure in these modules; 15 LAB files rendered | required | - |
| E4 | 2 | W1 | lab-controller | `scripts/operations/lab.py check <lab>` | NOT_RUN | needs the root `.env`, see Open issues | optional | - |
| E5 | 3 | W2 | hardening | `bash scripts/hardening/check-all-hardening.sh` on `db86e8c95` | PASS | "ALL checks passed successfully" | required | - |
| E6 | 3 | W2 | unit-tests | `python3 -m unittest discover -s tests -t .` on `88806a761` before `db86e8c95` | FAIL | 3228 tests, failures=23, errors=3, skipped=108 | required | - |
| E7 | 3 | W2 | unit-tests | 12 affected modules (compose baseline, SEC01 version, lifecycle public, SMTP generator, secret catalog and metadata sync, links, registry, LAB isolation, tier layout, workspace inventory, update gates) on `db86e8c95` | FAIL | 536 tests, failures=18, errors=1; 16 metadata-sync and 1 catalog test wait on the blocked registry, the SMTP dry run and one error lack `referencing` | required | - |
| E8 | 3 | W2 | script-manifest | `python3 scripts/validation/check-script-manifest.py` on `d109d7f58` and later | PASS | "script manifest is valid" | required | - |
| E9 | 4 | W3 | operations-catalog | `python3 scripts/validation/check-operations-catalog.py` on `db86e8c95` | PASS | operations-catalog: PASS | required | - |
| E10 | 5 | W4 | metadata | `check-document-metadata.py --mode check-changed --base-ref b08e1bdbf` and `--mode check-active` on `db86e8c95` | PASS | selected 102, zero violations; selected 544, zero violations | required | - |
| E11 | 5 | W4 | links | `check-document-links.py --mode all` on `db86e8c95` | PASS | 882 documents, 8017 links, zero failures | required | - |
| E12 | 5 | W4 | corpus-lifecycle | `check-document-corpus-lifecycle.py`, default and `--base-ref b08e1bdbf`, on `db86e8c95` | PASS | lifecycle zero, occupancy zero | required | - |
| E13 | 5 | W4 | hosted-ci | GitHub Actions | NOT_RUN | branch not pushed | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |
| 5 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. Independent review and hosted CI have not
run, and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [LAB sources](../../../../labs/README.md)
- [Document Registry](../../../99.templates/registry.json)
