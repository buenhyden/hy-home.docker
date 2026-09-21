---
title: "Optional Capability Restructure and CI Recovery"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0007"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
- "SPEC-0180-TSK-0006"
created: "2026-09-21"
---

# Optional Capability Restructure and CI Recovery

## Objective

Recover `validation-full` on main and restructure the newly added MLflow,
JupyterLab, dbt, Debezium CDC, DCGM and Crawl4AI capabilities so that the shared
base (management database, MinIO, Kafka Connect, gateway) stays independent of
optional features. Each feature owns its provisioning, grants, credentials and
operations documents. Preserve completed OpenBao, Open WebUI, Gatus and native
OIDC acceptance (Tasks 0002–0004), Notebook/SurrealDB decisions and all live data.

## Inputs

- Investigation base and branch base: main `ea3a7480d567acefa038417a2620aff497a30b72`
  (local HEAD = `origin/main` on 2026-09-21, clean tree). Branch
  `claude/home-dev-restructure` in an isolated worktree; the main checkout is the
  bind source of the running `hy-home-infra` project (48 containers) and was not edited.
- Failing run `35592775094` / job `106310656903` (`validation-full`, head
  `ea3a7480d`): first failure `metadata repository contracts: violations=36`
  (empty dbt, JupyterLab and MLflow READMEs).
- Owner operating command (not a restart or activation approval):
  `docker compose --profile local --profile core --profile mng --profile ai --profile dev --profile workflow --profile obs --profile admin up -d`.
- [REQ-0027](../../../01.requirements/0027-home-development-host.md),
  [AD-0031](../../../02.architecture/descriptions/0031-home-development-host.md),
  [SPEC-0180](../spec.md), [Plan](../plan.md), Tasks 0001–0006,
  [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md),
  [POL-0079](../../../05.operations/catalog/02-auth/0079-application-auth-integration/policy.md),
  [POL-0086](../../../05.operations/catalog/00-workspace/0086-dependency-version-management/policy.md),
  Stage 99 registry and schemas.
- Official references: MLflow network security and SSO/OIDC-plugin pages,
  Crawl4AI Docker hardening/migration notes, Jupyter Server security, Debezium
  PostgreSQL connector, Kafka KIP-993 `allowed.paths`, Renovate strict validator.

## Work Log

### Declared, deployed and running state (2026-09-21)

| Surface | Declared at `ea3a7480d` | Deployed/running (read-only inspect) |
| --- | --- | --- |
| `mng-pg` | `wal_level=logical` + slot/sender/retention caps | plain `postgres` command (older declaration), healthy |
| `mng-pg-init` | reads MLflow/dbt/Debezium secrets, runs their DDL | last exit 0 about nine hours earlier, before those changes |
| `kafka-connect` | local Debezium build | stock `cp-kafka-connect` image, healthy |
| MLflow, JupyterLab, dbt, DCGM, Crawl4AI | declared (Crawl4AI not included) | not running |
| Renovate units | repo revision with `Requires=`/`[Install]`/global prune | older installed copies; timer enabled, next run 2026-09-28 04:00 KST |

Private checks returned names and status only: `secrets/db/postgres/mlflow_password.txt`
and `dbt_password.txt` absent, `debezium_password.txt` present but empty. `.env`
had four keys absent from `.env.example` (`DBT_DB_USER`, `DBT_DB_NAME`,
`DBT_SCHEMA`, `DBT_THREADS`); `--sync-metadata-check` exit 1 (drift), values untouched.
Host GPU facts (read-only): GeForce GTX 1060 6 GB, NVIDIA driver 580.178.04,
`nvidia` runtime, NVIDIA Container Toolkit 1.20.0. <!-- runtime-version-exception: history — dated read-only host observation, not a runtime pin -->

### Defects reproduced at the base revision

1. **CI**: 36 metadata violations; 9 links to the pre-move SurrealDB paths; 33
   operations-catalog findings (Crawl4AI not included and profile-less, six
   undocumented profiles, unbound services, stale inventory); template baseline
   missing Crawl4AI; version projection could not parse `${DCGM_EXPORTER_TAG}`.
2. **`mng-pg-init` variable gap**: in a disposable PostgreSQL 18.6 the base SQL
   failed at line 197 with `syntax error at or near ":"` because
   `:'mlflow_db_password'` was never passed. The experiment-cluster runner
   (`pg-cluster-init`) had the same appended SQL and passes none of it.
3. **Startup coupling**: `core`/`mng`/`dev`/`local` declared the new secrets on
   `mng-pg-init`, so the next start would fail on the absent files.
4. Publication created in the wrong context by hard-coded names; dbt command was
   `--version`; five JupyterLab pins do not exist on PyPI; Jupyter empty token;
   MLflow used the shared all-bucket MinIO credential and a password in argv;
   Connect REST route had no authentication; Alloy's command dropped
   `--storage.path`; OAuth2 Proxy `trusted_ips` skipped SSO for all of
   `infra_net`; the generic `sso-auth` forwarded user access/ID tokens to every
   upstream; Grafana allowed anonymous Viewer, a catch-all role and unverified
   OAuth TLS; Open Notebook's API was published on all interfaces.

### Option comparison and decision

| Option | Effect | Decision |
| --- | --- | --- |
| Keep structure, patch in place | Fix variables inside `mng-pg-init` | Rejected: base start would still depend on optional credentials and DDL |
| Domain-selective restructure | Common base unchanged; each capability owns a provisioning job, SQL, grants, secret and docs; one shared input runner | **Chosen**: smallest change that removes the coupling |
| Full change | Separate DB clusters or projects per capability | Rejected: duplicates databases, changes data paths and needs migration approval |

### Before/after tree (changed paths only)

```text
before (ea3a7480d)                                   after (this branch)
infra/04-data/operational/mng-db/                    infra/04-data/operational/mng-db/
├── docker-compose.yml  (init reads 3 new secrets)   ├── docker-compose.yml  (init: base secrets only)
└── pg/init-scripts/init_users_dbs.sql (+§5–7)       ├── pg/init-scripts/init_users_dbs.sql (base only)
                                                     └── pg/provision/run-feature-provision.sh   (new, shared)
infra/04-data/relational/postgresql-cluster/         infra/04-data/relational/postgresql-cluster/
└── init-scripts/init_users_dbs.sql (+§5–7)          └── init-scripts/init_users_dbs.sql (base only)
infra/05-messaging/kafka/connect/debezium/           infra/05-messaging/kafka/connect/
└── postgres-connector.json                          ├── render-connect-secrets.sh             (new)
                                                     └── debezium/{postgres-connector.json, provisioning/mng-pg.sql (new)}
infra/09-tooling/dbt/ (empty README, --version)      infra/09-tooling/dbt/{README.md, requirements.txt, provisioning/mng-pg.sql,
                                                         projects/models/platform/*}
infra/11-laboratory/mlflow/ (empty README)           infra/11-laboratory/mlflow/{README.md, provisioning/{mng-pg.sql, minio-artifacts.sh}}
infra/11-laboratory/jupyterlab/ (empty README)       infra/11-laboratory/jupyterlab/README.md
infra/08-ai/crawl4ai/{docker-compose.yml, .llm.env}  infra/08-ai/crawl4ai/{docker-compose.yml, README.md}   (.llm.env removed)
docs/05.operations/catalog/ (no 0088–0091)           …/11-laboratory/0088-mlflow, 0089-jupyterlab; 09-tooling/0090-dbt; 08-ai/0091-crawl4ai
```

### File move and ownership table

| Current path (before) | Target path (after) | Reason | Stable ID / owner service | Impacted references |
| --- | --- | --- | --- | --- |
| `mng-db/pg/init-scripts/init_users_dbs.sql` §5 MLflow | `infra/11-laboratory/mlflow/provisioning/mng-pg.sql` | Feature owns role/DB | `mlflow-db-provision` (GDE/POL/RUN-0088) | MLflow Compose, 0028 docs |
| same §6 dbt | `infra/09-tooling/dbt/provisioning/mng-pg.sql` | Feature owns grants/schema | `dbt-db-provision` (0090) | dbt Compose |
| same §7 Debezium publication | `infra/05-messaging/kafka/connect/debezium/provisioning/mng-pg.sql` | Feature owns replication role/publication | `debezium-db-provision` (0036) | Kafka Compose, connector JSON |
| `postgresql-cluster/init-scripts/init_users_dbs.sql` §5–7 | removed (restored to prior content) | Capabilities target `mng-pg`, not the LAB cluster | `pg-cluster-init` | none |
| inline secret reads in `mng-pg-init` | `mng-db/pg/provision/run-feature-provision.sh` | Shared validation, env-only secret hand-off | three feature jobs | tests |
| `minio-create-buckets` line `mlflow-artifacts` + its `mlops`/`data-science` profiles | `infra/11-laboratory/mlflow/provisioning/minio-artifacts.sh` | Bucket plus bucket-scoped user owned by MLflow | `mlflow-artifact-provision` | MinIO README/guide |
| `dbt/Dockerfile` ARG pins + Compose build args | `infra/09-tooling/dbt/requirements.txt` | One Renovate-owned pin | `dbt` | renovate.json5 |
| `jupyterlab` Compose `build.args.JUPYTER_BASE_TAG` | Dockerfile ARG default only | Remove duplicate pin | `jupyterlab` | — |
| `infra/08-ai/crawl4ai/.llm.env` (tracked, empty) | removed | Provider keys must not live in a tracked file | `crawl4ai` | Compose `env_file` removed |

Final relationships (unchanged data paths): `mng-pg-data`, MinIO data, Kafka and
Connect volumes, Open Notebook/SurrealDB volumes and all existing roles/databases
are untouched. New data locations: MLflow database on `mng-pg`, bucket
`mlflow-artifacts`, dbt target schema in the application DB, JupyterLab work
directory `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work` (create owned by UID 1000).
New secrets (all Docker secrets): PG-021/023/025, STRG-006, AI-006/007. Mounts and
builds: feature SQL and runner are read-only bind mounts; images `hy-home/mlflow`,
`hy-home/jupyterlab`, `hy-home/dbt-postgres`, `hy-home/kafka-connect` are local
builds. Systemd: repository units only; the host keeps the older installed copies.

Each row is verified by `test_compose_baseline_gates` (static contracts plus the
opt-in rehearsal), the Compose validator and the catalog checker. Rollback is a
revert of the logical commit; no data migration is involved. Owner: this Task.

### Implementation summary

- **DB provisioning**: base init restored; three feature jobs run feature SQL via
  the shared runner. The runner rejects bad identifiers, missing/empty/multi-line/
  oversized secrets and non-regular files with exit 64 before connecting, and
  passes secrets only through the psql environment (`\getenv`); a bounded wait
  fails after 180 seconds. Feature SQL sets `log_statement=none` and
  `log_min_error_statement=panic` for its session so password-bearing statements
  do not reach the server log, serializes with advisory locks, refuses
  administrator roles, any existing role without its `hy-home:feature:<name>`
  comment marker (so another service's login is never altered) and
  foreign-owned databases/schemas, and sets `NOBYPASSRLS`.
- **Profiles**: `mlops`, `data-science`, `analytics-engineering`, `cdc` select
  `mng-pg`/`mng-pg-init` (and `minio`, Kafka broker/Schema Registry for `cdc`)
  for closure; the base job never reads their credentials. POL-0078 rows and
  companion rules added.
- **CDC**: dedicated `REPLICATION` role without superuser, schema-scoped read and
  default privileges, publication over the source and an owned
  `debezium_heartbeat` schema with a heartbeat action query (quiet `app_db` on a
  multi-database server would otherwise pin WAL); Connect renders
  `/tmp/connect-secrets/debezium.properties` (Java-properties escaping, 0600) on
  each start, `allowed.paths` limits `FileConfigProvider`, connector JSON uses the
  new path and a heartbeat; Connect REST route requires SSO.
- **dbt**: default `debug`, smoke model, read-only project, tmpfs artifacts,
  password in `DBT_ENV_SECRET_PASSWORD` so dbt redacts it.
- **MLflow**: DB password via `PGPASSWORD`, S3 secret via env, bucket-scoped MinIO
  identity, artifact proxy, wildcard-port allowed hosts, health on `MLFLOW_PORT`.
  OIDC plugin not adopted (conditions unverified); gateway SSO retained.
- **JupyterLab**: mandatory token secret, `trust_xheaders`, work directory outside
  the repo with `create_host_path: false`, unauthenticated `/api` health, real pins.
- **Observability**: DCGM literal pin, no `SYS_ADMIN`, GPU alert rules (promtool
  pass); Alloy `--storage.path` restored.
- **Gateway/auth**: `trusted_ips` removed; generic `sso-auth` forwards identity
  headers only; Grafana anonymous off, group-only roles, CA-verified OAuth TLS,
  Viewer default; Open Notebook API loopback-bound (SSO removal kept as owner decision).
- **Crawl4AI**: pinned `0.9.3`, opt-in profile, token secret, isolated
  `crawl4ai_net`, template adoption, no host port.
- **Renovate**: timer no longer `Requires=` the service, service has no `[Install]`,
  no host-wide prune, `--no-deps`; `pip_requirements` limited to `infra/**` as the
  single owner of image-local Python pins (no automerge, major approval).
- **Env/secret metadata**: `.env.example` gains `MLFLOW_S3_USER`, `DBT_DB_USER`,
  `DBT_DB_NAME`, `DBT_SCHEMA`, `DBT_THREADS`; drops unused `DCGM_EXPORTER_TAG`. Public
  registry gains nine rows (dry-run plans 103 rows, IDs unique).

### Service dispositions and data boundaries

| Service | Class | Decision | Data boundary |
| --- | --- | --- | --- |
| `mlflow`, `mlflow-db-provision`, `mlflow-artifact-provision` | OPTIONAL | Retain opt-in | MLflow DB + bucket; nothing created yet |
| `jupyterlab` | OPTIONAL | Retain opt-in, single user | Work directory; not created |
| `dbt`, `dbt-db-provision` | OPTIONAL | Retain opt-in | Derived relations only |
| `debezium-db-provision`, `kafka-connect` (cdc) | OPTIONAL | Retain; connector not registered | Slot/offsets are recovery state |
| `dcgm-exporter` | OPTIONAL | Retain opt-in; collection unverified | Stateless |
| `crawl4ai` | OPTIONAL | Retain hardened; remove at next review if still unconsumed | Stateless |
| `open_notebook`, `surrealdb` | OPTIONAL | Keep owner's `admin` exclusion, co-location, data and keys | Volumes untouched |

No service is removed in this change; no container was stopped, no credential
revoked and no data deleted. AI and workflow HOME services are unchanged.

### Authentication inventory (ForwardAuth targets and native status)

| Target | Current | Classification | Action here |
| --- | --- | --- | --- |
| Grafana, Kafbat, Airflow, Open WebUI, Gatus, Dozzle, OpenBao | native OIDC (Task 0004 / earlier) | completed native | Grafana hardened only |
| Terrakube API/UI/executor | native Keycloak OIDC plus ForwardAuth | native declared; proxy stacked | Token header no longer overwritten; proxy removal needs acceptance |
| Stalwart | ForwardAuth | direct OIDC support upstream | Deferred: needs Keycloak client (remote change) and acceptance |
| n8n | ForwardAuth | OIDC is an Enterprise feature | Keep proxy |
| SonarQube | ForwardAuth | OIDC via plugin; SAML edition-dependent | Keep proxy; bearer collision removed |
| MLflow | ForwardAuth | community OIDC plugin conditional | Keep proxy (GDE-0088) |
| JupyterLab | ForwardAuth + token | OIDC needs JupyterHub | Keep proxy + token (GDE-0089) |
| Prometheus, Alertmanager, Pushgateway, cAdvisor, Loki, Tempo, Alloy, Pyroscope, Ollama, ComfyUI, Mailpit, RedisInsight, Flower, Kafka Connect | ForwardAuth | no native generic OIDC in the deployed edition | Keep proxy; machine clients use internal paths |

`groups` scope authorizes nothing; `allowed_groups` remains an owner decision.
Measured: unauthenticated GET to the SSO-protected Alloy route returned 401 from
host loopback and the LAN address; Grafana returned 200 (then anonymous login
page). No authenticated, role-removal, logout or Valkey-failure test was run.

### Stage 99 template review

All 40 registry template sources and the registry entries were read by a
read-only reviewer against this branch. Consumed templates: package README
(12 infra READMEs), domain README (3 catalog indexes), operations
guide/policy/runbook (new 0088–0091 and edited subjects), research member (m0021)
and task (this Task, Task 0001 link fix); the Plan template is consumed by the
Plan update. Every template's existing prompts already cover profiles,
provisioning, secrets, authentication and the runtime-literal exception. Verdict:
**no template, registry or schema change** — no demonstrated contract gap. The
unconsumed architecture, archive, governance, reference-pack, requirement,
runtime-projection and contract templates also need no change; none gains
infrastructure or OIDC fields.

## Verification Evidence

Commands ran in the isolated worktree on the branch head before commit.

| Check | Result | Scope and limitation |
| --- | --- | --- |
| Base reproduction of mng-pg-init (disposable PG 18.6) | FAIL as expected at base | Synthetic secrets; container and network removed |
| New static contract tests (5) at base / branch | RED (4 errors, 2 fails) / GREEN 5/5 | `FeatureProvisioningContractTests` |
| Disposable PostgreSQL rehearsal (5 scenarios) | PASS 5/5 | `HYHOME_PG_REHEARSAL=1`; fresh, rerun, invalid input exit 64, non-default names, foreign owner and admin refusal, mid-run failure then convergence, 3-way concurrency; skipped in CI without the variable |
| MinIO `mc` stdin credential probe (disposable) | PASS | alias import, user add/re-add, policy create/attach idempotent |
| `validate-docker-compose.sh` (all 71 selections + HOME) | PASS | Static render with public example env |
| Eight-profile owner selection before/after | 43 = 43 services, identical names | New capabilities are not auto-selected |
| Add-on alone and with the eight profiles | all render | `cdc` now includes broker/Schema Registry |
| `check-operations-catalog.py` | PASS (was 33 findings) | |
| `promtool check rules` / `check config --syntax-only` | PASS | Prometheus v3.14.0 image, read-only mounts |
| `alloy fmt` per file (2 files separately) | PASS | Not a directory-combined check |
| `sync-tech-stack-versions.sh --check` | PASS after regeneration | Was a parse failure at base |
| `test_tech_stack_version_contract` | PASS 50/50 (base 18 failures) | Schedule expectation aligned with owner commit `8d93673b2` |
| Renovate `renovate-config-validator --strict` (repo and global) | PASS | `renovate@latest` via npx |
| `systemd-analyze verify` on both units | no findings | Host units not reinstalled |
| `gen-secrets.sh --dry-run` | 103 rows, 9 new create/update actions | Public example only |
| `check-document-metadata.py --mode check-contracts --history-scope full` | PASS, violations=0 (base 36) | CI's first failure is resolved |
| `check-document-links.py --mode all` | PASS (base 9 failures) | SurrealDB links point to the current subject |
| Agent governance, corpus lifecycle, script manifest, workflow contract, supply chain, quickwin, template security, `check-all-hardening.sh` | PASS | Template baseline and hardening were failing at base |
| Ruff 0.15.12 format/check on changed tests (official container) | PASS | Host has no pip/uvx |
| `run-ci-gate.py --profile full` at `f0737491d` | exit 1: 11 suites OK, 1 failure `test_automatic_pre_commit_sees_index_content_and_untracked_paths` (`exec: pre-commit: not found`) | Environment prerequisite absent locally; CI installs it. Earlier local runs also failed two file-mode tests caused by this worktree's umask 002 checkout (Git stores only the exec bit); normalizing the local modes cleared them. Hosted `validation-full` has not run on this branch |

## Review Evidence

- Stage 99 template review (read-only reviewer, all 40 sources): no template,
  registry or schema change required; see the section above.
- Independent specification and security review of the staged branch:
  Spec compliance PASS, Security FAIL on one Major and eight Minor findings,
  all corrected before commit:

| Finding | Correction | Evidence |
| --- | --- | --- |
| Major: feature job could `ALTER` another service's existing role (e.g. `DBT_DB_USER=app_user`) | Ownership comment marker set in the creating transaction; any existing role without it is refused | Rehearsal: `DBT_DB_USER=app_user` exits non-zero and `app_user` still logs in |
| Identifier with an embedded line break passed `grep -E` | Explicit single-line guard | Rehearsal case `multi-line identifier` exits 64 |
| Password text could reach the server log on error | Session `log_statement=none`, `log_min_error_statement=panic` | SQL review |
| Heartbeat claim without an action query | `debezium_heartbeat` schema/table, publication and `heartbeat.action.query` | Rehearsal: publication has 3 tables; heartbeat upsert succeeds as `debezium` |
| Debezium DB name hard-coded | `${SERVICE_POSTGRES_DB:-app_db}`; contract test compares the default with the connector | Static test |
| Missing `NOBYPASSRLS` on MLflow/dbt roles | Added | SQL review |
| Only a leading space escaped in properties | Any leading blank or form feed escaped | Static escaping test with tab and form feed |
| dbt password not redacted | `DBT_ENV_SECRET_PASSWORD` | Entrypoint and profile |
| Unbounded readiness wait | 90 tries / 180 seconds then exit 64 | Runner review |

- Unverified items the reviewer named were then checked: `mc admin policy
  attach` re-run succeeded in the disposable MinIO probe; Keycloak's served
  certificate is issued by the local mkcert CA and verifies against
  `rootCA.pem` (so Grafana's pinned CA is correct); Crawl4AI's token variable is
  the documented upstream contract.

## Commit Ledger

Branch `claude/home-dev-restructure` from `ea3a7480d`; local only, not pushed.

| Commit | Scope |
| --- | --- |
| `30228fc69` fix(infra) | Provisioning split, feature jobs/SQL, MLflow/Jupyter/dbt/Connect wiring, env/secret metadata, version projection, tests |
| `d19af851d` fix(obs) | Alloy storage path, DCGM pin/capability, GPU alerts, Grafana auth hardening |
| `a456e9380` fix(auth) | `trusted_ips` removal, identity-only headers, Open Notebook loopback, hardening baseline |
| `6857c42c2` feat(ai) | Crawl4AI inclusion and isolation |
| `c89f8caa4` fix(deps) | Renovate units and `pip_requirements` ownership |
| `145dd5d5e` docs(ops) | READMEs, Stage 05 triplets, POL-0078, inventory, links, this Task, Plan and Spec |
| `f0737491d` docs(ops) | Inventory refresh for the heartbeat schema |
| this commit | Final evidence and ledger |

Intermediate commits are grouped by concern; only the branch head is gate-verified.

## Rulings

| Decision | Basis | What could be wrong / cost |
| --- | --- | --- |
| Feature-owned provisioning with a shared runner | Removes base coupling without duplicating databases | Three extra one-shot jobs; mitigated by tests |
| Feature profiles select `mng-pg`/`mng-pg-init` | POL-0078 requires closure; base job no longer needs feature secrets | Selecting an add-on alone starts the management DB |
| Remove `trusted_ips` | No consumer found; broad auth bypass | A hidden in-network caller through Traefik gets 401; revert restores it |
| Identity-only `sso-auth` headers | Token replay and bearer collisions | An upstream relying on injected tokens would need its own middleware |
| Grafana anonymous off and group-only roles | User instruction; anonymous exposure measured | Users outside `/admins`/`/editors`/`/viewers` lose access; Kiali (k3d, outside this repo) was the recorded reason for anonymous access and may need a Grafana service-account token; confirm both before activation |
| Keep Open Notebook without SSO | Owner commit `b90b74837` | App password is the only identity control |
| Keep Crawl4AI opt-in instead of removal | Owner added it for Open Notebook today | Unused service remains; review deadline recorded |
| MLflow OIDC plugin not adopted | Compatibility and maintenance unverified | SDK path stays unauthenticated inside `infra_net` |

## Deferred Items

Each item needs the named approval; nothing below was executed.

1. **Merge/activation**: merging into the main checkout changes the watched
   Traefik dynamic middleware immediately (token headers) and bind-mounted files
   for the next restart. Approval must name the merge and the gateway effect.
2. **Recreates**: `oauth2-proxy` (trusted_ips), `infra-grafana` (after Keycloak
   group check), `infra-alloy` (storage path; one-time log re-read/skip),
   `open_notebook` (loopback API), `kafka-connect` (image build + renderer),
   `mng-pg` (logical WAL; restarts every management-DB consumer).
3. **Private preparation**: `gen-secrets.sh --sync-metadata` after merge to add the
   nine rows and five env keys with values preserved; exact-key prune of
   `DCGM_EXPORTER_TAG` from `.env`; generating PG-021/023/025, STRG-006, AI-006/007
   values; the empty `debezium_password.txt` needs a real value. Host secret files
   are mostly mode 664; tightening modes needs a container-read plan.
4. **Builds and first starts** of `mlops`, `data-science`, `analytics-engineering`,
   `cdc`, `obs-gpu`, `crawl4ai`, and creating the JupyterLab work directory.
5. **CDC**: connector registration, snapshot and change-capture evidence; slot
   lag monitoring; no slot/offset deletion.
6. **Auth acceptance**: route 401/403 matrix, non-allowed user, logout, role
   removal and Valkey outage for SSO routes; Stalwart native OIDC client;
   Terrakube proxy removal; `allowed_groups` policy.
7. **Host**: reinstall Renovate units by copy (not symlink); reboot, backup and
   isolated restore rehearsals for MLflow, JupyterLab and CDC; RPO/RTO remain
   the unverified planning ceilings of the owning policies.
