---
title: "Analytics Labs Migration Task"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-06"
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
progress under the approved parents. Hosted CI passed on PR #747, merged as
`729d16da7`.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0262 | draft | approved | #current-contract-decision |
| SPEC-0262-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0262-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0262-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Decisions

- Grouping: one LAB per Stage 05 document set, `labs/lakehouse/docker-compose.yml`,
  `labs/dbt/docker-compose.yml`, `labs/superset/docker-compose.yml`, `labs/jupyterlab/docker-compose.yml`,
  `labs/sonarqube/docker-compose.yml` and `labs/stalwart/docker-compose.yml`. Assets moved with `git mv` to
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

### Owner confirmations

On 2026-11-04 the owner answered the three open choices:

- "허용 (권장)" for editing the public registry
  `secrets/SENSITIVE_ENV_VARS.md.example`: rows LAB-026 to LAB-036 were added
  and the PG-011, PG-024 and PG-029 user keys renamed to their `LAB_*` names,
  from the OpenBao catalog. All 14 changed value cells are `(비어있음)`.
- "입력 방식 유지 (권장)" for HOME reachability: SPEC-0215 stays unchanged and
  the HOME-dependent LABs keep the required `LAB_*` endpoint inputs.
- "이번 결정을 승인으로 기록 (권장)" for the amended requirements: this owner
  decision is the approval of the amended REQ-0005, REQ-0006, REQ-0010,
  REQ-0011 and REQ-0012 wording, which therefore stay `approved`.

With the registry edit, `test_secret_metadata_sync` and
`test_secret_catalog_contract` give 14 failures and 1 error under the local
system Python, exactly as on `main` `1425b017b` with the same interpreter
(jsonschema 4.10.3 lacks `referencing`). The branch adds no failure there;
Hosted CI with the locked dependencies is the deciding run.

### LAB check follow-up (2026-11-05)

The owner's 2026-11-05 request to review the remaining work and continue led
to a `lab.py check` run. Branch `fix/lab-root-observer-overlap` from
`f0ce46fda`. The run used the tracked `.env.example` and `labs/.env.example`,
the synthetic `LAB_*` inputs that `compose_controls.LAB_INPUTS` already uses,
and a synthetic 64 CPU / 131072 MiB budget. It did not read the private root
`.env`, and `check` starts nothing.

Every LAB was refused with "data path … overlaps root", even for
`/nonexistent/…` paths. There were three causes:

- `cadvisor` and `node-exporter` bind `/` read-only, so the bind nested with
  every LAB path. A read-only `/` bind now owns no path. A LAB that binds `/`
  itself still meets root's data paths (`e5ac910bf`).
- HOME provision jobs and the dbt/superset LABs mount the same tracked
  `run-feature-provision.sh` read-only. It joins `SHARED_PUBLIC_INPUTS`
  (`e5ac910bf`).
- `conftest` binds the `infra/` and `labs/` source trees read-only. The owner
  chose "도구 마운트 무시 (권장)". A read-only, non-sensitive HOME bind of
  exactly one of those trees owns no read-only, non-sensitive LAB path
  strictly inside it. Writable, secret or whole-tree LAB binds, and a
  writable HOME bind of the tree, still conflict (`8b231c5e3`).

A security review returned CHANGES_REQUESTED with two Important findings:

- With the `/` observers exempt, no HOME path covered the top-level secret
  files, the root env file or Docker's data root.
- The source-tree exemption accepted gitignored `.env` files.

`c94497269` fixes both. Compose secret files are sensitive inputs of the model
that declares them, the root env file and `DockerRootDir` are HOME state,
`.env` files are sensitive, and only git-tracked paths qualify.

The re-review approved those fixes but found one more Important gap: no
HOME path covered `.git`, `scripts`, `secrets/.retired`, `.env.*` variants
or host credentials. On 2026-11-05 the owner chose an allowlist,
"목록 도입 + LAB_* 경로 허용 (권장)", and for Locust "결과 폴더만 쓰기 허용
(권장)". Commit `9fa48a5a5` requires every LAB bind and secret source to be
one of:

- under `LAB_DATA_DIR`;
- read-only under `LAB_SECRET_DIR`, which defaults to `secrets/labs`;
- read-only under an operator `LAB_*` path input;
- writable under a `LAB_*_RESULT_DIR`;
- a read-only, non-sensitive, git-tracked repository path.

An identical tracked file that both sides mount read-only counts as a
shared public input, and git uses literal pathspecs.

The next re-review found two more Important gaps. First, a single
`LAB_*` value such as `/`, `$HOME`, the repository, `../secrets` or the
shipped Docker socket path widened the allowlist. Second, `configs`,
`env_file` and build inputs bypassed it. Commit `900aaf350` fixes both:

- A data, secret, operator or results root that covers the repository, its
  `secrets/`, HOME data, Docker's root or the user home admits nothing.
- Operator roots may not sit in the repository, and a sensitive operator
  root, such as the socket, is dropped.
- Config files are footprinted.
- Build contexts must meet the read-only rules, and build `ssh` and
  `secrets` are refused.
- A LAB `env_file` is refused by scanning the raw LAB file, because the
  rendered model inlines its contents.
- A tracked path with local edits no longer counts as public.

The final review found four more gaps. Commit `5eb03ebae` closes them:

- The `env_file` text scan could be bypassed by flow style, a quoted key,
  `extends` or `include`. LAB models are now rendered with
  `--no-env-resolution`, and any `env_file` in the model is refused.
- Inside the repository, `LAB_SECRET_DIR` must be `secrets/labs`.
- A sensitive source needs the secret root under every rule.
- Build cache import and export, host network, entitlements and an
  absolute Dockerfile are refused.

The confirm pass and an automated review raised three more gaps. Commit
`ba34798d5` closes them:

- An `include` entry can carry its own `env_file`, so a LAB file may not
  include anything. It is parsed with PyYAML and fails closed.
- Build keys are an allowlist, and the Dockerfile must resolve inside its
  context.
- The protected `secrets` paths are resolved with `realpath`.

The last confirm pass approved those fixes except one case: with `secrets/`
symlinked out of the repository, a `LAB_SECRET_DIR` inside the resolved
tree skipped the `secrets/labs` rule. Commit `6f4eb08dc` decides the rule from
the resolved tree as well.

Container-escape options (`devices`, `volumes_from`, `pid`/`network_mode:
host`, `cap_add`, `privileged` under a `cadvisor` name) are outside this
check and remain a recorded residual risk.

All 16 LABs were checked. In 15 of them no overlap or allowlist problem
remains. supabase is refused, which matches the owner decision
"LAB_SECRET_DIR 복사본으로 전환 (권장)". It reads 11 HOME secret files
directly from `secrets/`, including HOME's SMTP password, and binds the
Docker socket. Moving it to LAB copies is separate follow-up work. Its
Docker socket stays refused until an exception is approved. The remaining problems come from
the synthetic inputs. The 64 CPU budget is below HOME's roughly 64 declared
CPUs on this 12-core host, and the synthetic LAB secret files and Superset CA
file are absent.
The real budget is an operator input.

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

- Operator: provide the `LAB_*` endpoints and LAB secret copies before a
  HOME-dependent LAB runs, and approve a Superset LAB redirect URI.
- Operator: set `LAB_HOST_BUDGET_CPUS` and `LAB_HOST_BUDGET_MEMORY_MIB`. HOME
  already declares about 64 CPUs on a 12-core host, so the budget is a
  policy decision; an empty budget refuses.
- `lab.py check` with the real root `.env` and real LAB inputs is NOT_RUN.
- Residual: lab.py does not check container-escape options (`devices`,
  `volumes_from`, host `pid`/`network_mode`, `cap_add`, a privileged
  service named `cadvisor`).
- supabase: move its 11 secrets to `LAB_SECRET_DIR` copies (owner decision).
  Its Docker socket bind stays BLOCKED until an exception is approved.

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
| E14 | 3 | W2 | unit-tests | `python -m unittest discover -s tests -t .` with the locked controller venv (Python 3.12.3, `--require-hashes`) on `280b6f8fd` | PASS | 3272 tests OK, skipped=108 (opt-in container tests) | required | E6, E7 |
| E15 | 5 | W4 | hosted-ci | GitHub Actions on PR #747 | PASS | candidate-quality pass 16m19s; merged as `729d16da7` | required | E13 |
| E16 | 2 | W1 | lab-controller-overlap | `lab.py --env-file <synthetic> --root-env-file .env.example check <lab>` on `f0ce46fda` | FAIL | every LAB refused: "overlaps root" from read-only `/` and source-tree binds | required | - |
| E17 | 2 | W1 | lab-controller-overlap | same synthetic check on `6f4eb08dc` | PASS | six LABs: zero overlap problems; only the synthetic budget and absent synthetic LAB secret and CA files remain | required | E16 |
| E18 | 2 | W1 | unit-tests | `test_lab_controller` and `test_lab_isolation` on `6f4eb08dc`, plus script manifest, CI routing and compose baseline modules | PASS | observer, shared tracked file, source-tree, HOME secret/env/Docker-root, tracked/clean, literal pathspec, allowlist, root validation, configs/build/env_file tests GREEN after RED | required | - |
| E20 | 2 | W1 | lab-controller-allowlist | synthetic check of all 16 LABs on `6f4eb08dc` | PASS | 15 LABs: no overlap or allowlist problem; supabase refused as decided (HOME secrets; Docker socket refused by the allowlist) | required | - |
| E19 | 2 | W1 | security-review | Independent review of the LAB overlap change through `8b231c5e3` | FAIL | CHANGES_REQUESTED: 2 Important (HOME secrets, root env and Docker root uncovered; gitignored .env accepted), 1 Minor (tests) | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E1 | Owner @buenhyden accepted on 2026-11-06. | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | accepted | E5, E8, E14 | Owner @buenhyden accepted on 2026-11-06. | @buenhyden |
| 4 | accepted | E9 | Owner @buenhyden accepted on 2026-11-06. | @buenhyden |
| 5 | accepted | E10, E11, E12, E15 | Owner @buenhyden accepted on 2026-11-06. | @buenhyden |

## Review and Completion

Local checks and hosted CI for PR #747 are recorded above. The LAB check
follow-up awaits independent review and its own hosted CI. On 2026-11-06 the owner
@buenhyden accepted criteria 1, 3, 4 and 5; criterion 2 stays pending.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [LAB sources](../../../../labs/README.md)
- [Document Registry](../../../99.templates/registry.json)
