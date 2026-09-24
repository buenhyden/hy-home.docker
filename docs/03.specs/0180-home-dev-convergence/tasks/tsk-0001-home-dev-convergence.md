---
title: "Home and Development Server Convergence Execution"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0001"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
created: "2026-09-19"
requirement_allocation_recovery_decisions:
- comparison_base_commit: d1e6ded52808b02392c52472d5416518a3b959d6
  defect_commit: 70aaeffb84e8f6bc537241615d4743b79ccac079
  valid_predecessor_commit: b66da447f68993dd9bddfd100bdd4c4b90d19be4
  requirement_path: docs/01.requirements/0012-laboratory.md
  allocation_name: REQ-0012.FR
  predecessor_current_issued:
  - 1
  - 2
  - 3
  - 4
  corrupt_declared:
  - 1
  - 2
  - 3
  repaired_current_issued:
  - 1
  - 2
  - 4
  repaired_reserved_history:
  - 3
  repaired_requirement_sha256: 2ba7a18fef3f1523fad0b36b067214fd5a552c48f830264684e97f0aae6d7b22
  disposition: stable-identity-restoration
---

# Home and Development Server Convergence Execution

## Objective

Execute the owner-requested [Spec](../spec.md) and [Plan](../plan.md).

## Inputs

Owner's attached 102-section mission; current tracked main; bootstrap and Codex
provider; applicable governance; public configuration and metadata only.

## Work Log

- 2026-09-19: Read mission and bootstrap. Initial worktree clean on main.
- Fetched all remotes and fast-forward checked main. Baseline remained
  `d1e6ded52808b02392c52472d5416518a3b959d6`.
- Created `codex/home-dev-convergence`. Read-only independent Compose and version
  management audits dispatched. No runtime or secret-value changes performed.
- Sandbox command startup failed with `bwrap: loopback: Failed RTM_NEWADDR`;
  read-only commands were rerun through explicit execution approval.

## Verification Evidence

| Command | Exit | Observation |
| --- | --- | --- |
| `git status --short --branch` | 0 | clean main before work |
| `git fetch --all --prune` | 0 | remote refs refreshed |
| `git switch main` | 0 | main selected |
| `git pull --ff-only` | 0 | already current |
| `git rev-parse HEAD` | 0 | baseline above |
| `git switch -c codex/home-dev-convergence` | 0 | isolated branch created |

| Criterion | Work unit | Result at the time | Owner |
| --- | --- | --- | --- |
| 1 | W1 | source inventory and read-only runtime measured | implementation and operations |
| 2 | W1 | primary-source matrix recorded; installed compatibility/restore unverified | Stage 90 |
| 3 | W2 | source/profile validation passed; runtime not applied | POL-0078 and Compose |
| 4 | W3, W4 | source/document contracts implemented; local final checks passed | Stage 99 and Stage 05 |
| 5 | W5 | sync and strict configuration checks passed | existing synchronization and update configs |
| 6 | W6 | metadata sync completed; values preserved, never output | public schemas and sync owner |
| 7 | W7 | isolated full and changed exited 0; final full includes Ollama correction | existing validation graph |
| 8 | W8 | approved OpenBao bootstrap verified; broader runtime acceptance pending | operational runbooks |
| 9 | W9 | branch pushed; Draft PR #167 created; hosted CI running | Git and PR |

### Baseline findings

- Host: Ubuntu 24.04, 12 logical CPUs, RAM 31 GiB, available 20 GiB; root
  filesystem 73 GiB available and storage filesystem 2.6 TiB available.
- GPU: GTX 1060, 6144 MiB VRAM; 69 MiB used at observation.
- Root includes 42 Compose fragments, with 140 service definitions and 64
  profile names (YAML-parsed, pre-change observation).
- Owner confirmed AI and workflow are required always-on HOME capabilities.
- Pyroscope running but unhealthy; mng-pg-init exited 3. Read-only exec found
  neither /bin/sh nor /usr/bin/wget in Pyroscope (each exit 127); configured
  CMD-SHELL healthcheck cannot execute. No logs or private values read.
- Default metadata check-changed exits 2 before selecting changes because
  trusted main REQ-0012.FR allocation differs from declarations. Git commit
  70aaeffb8 reassigned former FR-0004 to FR-0003. Restored FR-0004 and reserved
  withdrawn FR-0003 in working tree; check-active passes (389 selected, exit 0).
- An explicit pre-defect base check exposed new Task parent/state errors; these
  are corrected by binding both Spec and Plan. New documents remain draft
  as required by the initial-document lifecycle; execution authorization is
  recorded in Rulings. This check is not the default baseline gate.

### Implemented checks (repository only)

- Full Compose profile validation: exit 0, 64 selections, aggregate 261 service
  selections (overlap counted); no runtime mutation.
- PostgreSQL init uses psql-side connection switching, not SQL `\gexec` for a
  meta-command. Focused negative tests failed before repair; regression module
  passed 19 tests, then 21 after OpenBao path regressions.
- Pyroscope native `profilecli ready` replaces unavailable shell/wget; read-only
  readiness invocation eventually exited 0. Listener, health, ingress and host
  mappings agree for synthetic ports 4040 and 5050.
- ComfyUI defaults and host/container direction repaired; public render checks
  passed for ports 8188 and 9191. ComfyUI memory limit is 4 GiB and Open WebUI
  2 GiB, still pending measured runtime acceptance.
- OpenBao Agent config argument now names the mounted file; template destinations
  now use its persistent output mount. Two regression tests failed before repair
  and passed after it. No secret values or private files were accessed.
- Mailpit host mappings are loopback-bound and match explicit listener settings;
  synthetic distinct host/container ports passed. SurrealDB malformed expose
  string repaired to its fixed internal listener, host mapping loopback-bound.
- Version synchronization tests: 16 passed; real registry `--check` exited 0.
- Official Renovate strict repository and global configuration validators exited
  0. Repeated under temporary supported Node 24 with native RE2 rebuilt: both
  repository (`--strict --no-global renovate.json5`) and self-hosted
  (`--strict infra/09-tooling/renovate/config/config.js`) checks exited 0 without
  engine/native-module warnings. No global tool installation was performed.
- Default changed metadata gate still blocked by pre-existing REQ-0012 baseline
  inconsistency; diagnostic explicit-base checks are not a default-gate PASS.

### Subsequent verification and synchronization

- `check-document-links.py --mode all`: exit 0, 914 documents, 7123 links at
  that revision. New Requirement links require the final rerun.
- `python3 -m unittest tests.lib.gate.test_github_workflow_contract -q`:
  exit 0, 43 tests. Updated two registered Node 24 action pins to match existing
  workflow implementation, retained exact-pin validation, validated retrieval dates.
- Public secret metadata sync regression suite: exit 0, 8 tests; combined secret,
  Compose and identity regression invocation: exit 0, 55 tests at that revision.
- `gen-secrets.sh --sync-metadata-check`: exit 1, metadata drift in two files.
- `gen-secrets.sh --sync-metadata`: exit 0, two private metadata files aligned;
  existing values and unknown entries preserved; secret value files untouched.
- Repeated `gen-secrets.sh --sync-metadata-check`: exit 0, zero files changed.
- `gen-secrets.sh --dry-run`: exit 0. Existing generation readiness `--check`:
  exit 1 because `htpasswd` is unavailable; metadata mode does not need it.
- Core template security and optimization checks: exit 0 after explicit management
  PostgreSQL entrypoint capabilities and justified init/bootstrap exceptions.
- All eleven hardening tiers: exit 0. These are static checks, not live acceptance.

### Final public-contract alignment

- Public env assignments: 245 unique keys; 243 directly active Compose variables.
  Four assigned indirect inputs are two path derivations and two htpasswd generator
  usernames; optional `COMFYUI_ARGS` and host `HOME` need no public assignment.
- Retired 98 root/public readiness-example assignments with no current consumer;
  preserved two dynamically consumed generator inputs. Readiness example key set
  now equals root (245). Existing private assignments remain preserved, including
  retired and unknown keys; public schema retirement does not delete local values.
- Root secret declarations and granted identities both equal 67. Five unused root
  declarations were retired while private files and metadata rows were preserved.
- Eight public registry env mappings are now metadata-only. Re-sync changed one
  private registry; follow-up metadata check exited 0 with zero drift.
- Both private metadata files were gitignored but mode 0664; constrained to 0600.
  Only names, modes and ignore status were observed, never their contents.
- Profile semantic tests: 17 PASS; complete operations catalog module: 53 PASS;
  operations-catalog CLI: exit 0. New semantic tests failed before implementation.
- Full Compose profile validation repeated after env/declaration cleanup: exit 0,
  64 selections, 261 aggregate service selections. No containers started.
- Current active metadata: exit 0, 452 selected documents, zero violations.
- Workflow/CI model/secret regression invocation: exit 0, 58 tests.
- npm lockfile audit: exit 0, zero reported vulnerabilities. Python audit initially
  blocked by missing host ensurepip; isolated complete dependency-resolution audit
  subsequently exited 0 with no known vulnerabilities.

### Consolidated owner report (A–M)

This report distinguishes delivered source changes from runtime acceptance. Draft
Requirements, Architecture, Spec and new operational subjects do not imply stage
approval. The current running containers still use their previous configuration.

#### A. Baseline

Baseline HEAD: `d1e6ded52808b02392c52472d5416518a3b959d6`; working branch:
`codex/home-dev-convergence`. Host measurements and 42 Compose fragments / 140
services / 64 profiles are recorded above. The final read-only observation found
36 running containers: 34 healthy, Pyroscope unhealthy and Airflow StatsD exporter
without a declared health status. No container was restarted by this task.

#### B. Structural drift

| Surface | Change and remaining boundary |
| --- | --- |
| INFRA / SECURITY / NETWORK | Fixed observed listener, health, path and capability defects; live acceptance pending. |
| README / OPERATIONS | Runtime pins link to implementation; added missing operational owners and retired removed Syncthing guidance. |
| TEMPLATES | Stage 99 defines evidence-based runtime-version exceptions and canonical source ownership. |
| PROFILES | POL-0078 enumerates actual selectors, categories, purposes and services; semantic validator checks exact coverage. |
| ENV / SECRETS | Public contracts reconciled; private values preserved, metadata synchronized and file modes restricted. |
| VERSIONS | Curated source projection fails closed on ambiguous or missing image authority. |
| RENOVATE / DEPENDABOT | Unique surface ownership, separate major updates, security fast path, normal soak window and no infra automerge. |
| DATA | Persistent paths preserved; backup and restore readiness not established by source validation. |
| CI | Corrected workflow pin/date contract and documented the exact historical allocation recovery; full gate results below. |

#### C. Service disposition

The [dated 140-service inventory](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md#dated-service-disposition-inventory)
records every service's classification, dependencies/consumers, data mounts,
resource declarations, network, environment key names, secret grants and rationale.
AI and workflow remain always-on HOME requirements. Optional databases, clustered
topologies, analysis tools and maintenance jobs require explicit selection.

#### D. Profile matrix

[POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md)
is the single vocabulary and matrix owner. The proposed HOME selection is `core`,
`mng`, `ai`, `workflow`, `obs-core`, `obs-host`, `availability`, `logs`, `alerting`
and `storage`. Selecting it is not deployment approval. OpenBao bootstrap and
persistent-store readiness must be resolved before a complete HOME rollout.

#### E. Version ownership

[POL-0086](../../../05.operations/catalog/00-workspace/0086-dependency-version-management/policy.md)
owns the surface/update-owner/authority matrix. Compose and Dockerfile pins remain
the runtime source; `infra/tech-stack.versions.json` is a curated machine-readable
projection. Narrative exact literals require a documented exception.

#### F. Documentation coverage

New draft operational subjects cover SurrealDB, ComfyUI, OpenTofu, Renovate,
Mailpit, OpenBao, dependency management and Gatus. Existing subjects retain stable
IDs. Vault is migration-only; Stalwart owns mail-server operations. Syncthing has
no current service and its three records are retained with exact original bodies.
Coverage presence does not certify backup, upgrade or restore rehearsal.

Path coverage is 140/140 service triplets: 130 active, two active migration-only
and eight draft-only. Each row links to its shared component owner; drafts are
not operational approval. Version-literal compliance is checked by the final
metadata gate across the current corpus, not by the existence of these links.

| Service | Guide | Policy | Runbook | External refs | Version literals |
| --- | --- | --- | --- | --- | --- |
| airflow-apiserver | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-dag-processor | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-init | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-scheduler | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-statsd-exporter | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-triggerer | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-valkey | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-valkey-exporter | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| airflow-worker | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| alertmanager | [active](../../../05.operations/catalog/06-observability/0039-alertmanager/guide.md) | [active](../../../05.operations/catalog/06-observability/0039-alertmanager/policy.md) | [active](../../../05.operations/catalog/06-observability/0039-alertmanager/runbook.md) | linked | metadata gate |
| alloy | [active](../../../05.operations/catalog/06-observability/0040-alloy/guide.md) | [active](../../../05.operations/catalog/06-observability/0040-alloy/policy.md) | [active](../../../05.operations/catalog/06-observability/0040-alloy/runbook.md) | linked | metadata gate |
| analytics | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| auth | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| cadvisor | [active](../../../05.operations/catalog/06-observability/0044-optimization-hardening/guide.md) | [active](../../../05.operations/catalog/06-observability/0044-optimization-hardening/policy.md) | [active](../../../05.operations/catalog/06-observability/0044-optimization-hardening/runbook.md) | linked | metadata gate |
| cassandra-exporter | [active](../../../05.operations/catalog/04-data/0025-cassandra/guide.md) | [active](../../../05.operations/catalog/04-data/0025-cassandra/policy.md) | [active](../../../05.operations/catalog/04-data/0025-cassandra/runbook.md) | linked | metadata gate |
| cassandra-node1 | [active](../../../05.operations/catalog/04-data/0025-cassandra/guide.md) | [active](../../../05.operations/catalog/04-data/0025-cassandra/policy.md) | [active](../../../05.operations/catalog/04-data/0025-cassandra/runbook.md) | linked | metadata gate |
| comfyui | [draft](../../../05.operations/catalog/08-ai/0081-comfyui/guide.md) | [draft](../../../05.operations/catalog/08-ai/0081-comfyui/policy.md) | [draft](../../../05.operations/catalog/08-ai/0081-comfyui/runbook.md) | linked | metadata gate |
| couchdb-1 | [active](../../../05.operations/catalog/04-data/0026-couchdb/guide.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/policy.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/runbook.md) | linked | metadata gate |
| couchdb-2 | [active](../../../05.operations/catalog/04-data/0026-couchdb/guide.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/policy.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/runbook.md) | linked | metadata gate |
| couchdb-3 | [active](../../../05.operations/catalog/04-data/0026-couchdb/guide.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/policy.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/runbook.md) | linked | metadata gate |
| couchdb-cluster-init | [active](../../../05.operations/catalog/04-data/0026-couchdb/guide.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/policy.md) | [active](../../../05.operations/catalog/04-data/0026-couchdb/runbook.md) | linked | metadata gate |
| db | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| dozzle | [active](../../../05.operations/catalog/11-laboratory/0072-dozzle/guide.md) | [active](../../../05.operations/catalog/11-laboratory/0072-dozzle/policy.md) | [active](../../../05.operations/catalog/11-laboratory/0072-dozzle/runbook.md) | linked | metadata gate |
| etcd-1 | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| etcd-2 | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| etcd-3 | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| flower | [active](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | [active](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | linked | metadata gate |
| functions | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| gatus | [draft](../../../05.operations/catalog/06-observability/0087-gatus/guide.md) | [draft](../../../05.operations/catalog/06-observability/0087-gatus/policy.md) | [draft](../../../05.operations/catalog/06-observability/0087-gatus/runbook.md) | linked | metadata gate |
| grafana | [active](../../../05.operations/catalog/06-observability/0041-grafana/guide.md) | [active](../../../05.operations/catalog/06-observability/0041-grafana/policy.md) | [active](../../../05.operations/catalog/06-observability/0041-grafana/runbook.md) | linked | metadata gate |
| imgproxy | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| influxdb | [active](../../../05.operations/catalog/04-data/0017-influxdb/guide.md) | [active](../../../05.operations/catalog/04-data/0017-influxdb/policy.md) | [active](../../../05.operations/catalog/04-data/0017-influxdb/runbook.md) | linked | metadata gate |
| k6 | [active](../../../05.operations/catalog/09-tooling/0061-k6/guide.md) | [active](../../../05.operations/catalog/09-tooling/0061-k6/policy.md) | [active](../../../05.operations/catalog/09-tooling/0061-k6/runbook.md) | linked | metadata gate |
| kafbat-ui | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-1 | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-2 | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-3 | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-connect | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-exporter | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-init | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| kafka-rest-proxy | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| keycloak | [active](../../../05.operations/catalog/02-auth/0014-keycloak/guide.md) | [active](../../../05.operations/catalog/02-auth/0014-keycloak/policy.md) | [active](../../../05.operations/catalog/02-auth/0014-keycloak/runbook.md) | linked | metadata gate |
| kong | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| ksql-datagen | `GDE-0018` (superseded) | `POL-0018` (superseded) | `RUN-0018` (superseded) | linked | metadata gate |
| ksqldb-cli | `GDE-0018` (superseded) | `POL-0018` (superseded) | `RUN-0018` (superseded) | linked | metadata gate |
| ksqldb-server | `GDE-0018` (superseded) | `POL-0018` (superseded) | `RUN-0018` (superseded) | linked | metadata gate |
| locust-master | [active](../../../05.operations/catalog/09-tooling/0062-locust/guide.md) | [active](../../../05.operations/catalog/09-tooling/0062-locust/policy.md) | [active](../../../05.operations/catalog/09-tooling/0062-locust/runbook.md) | linked | metadata gate |
| locust-worker | [active](../../../05.operations/catalog/09-tooling/0062-locust/guide.md) | [active](../../../05.operations/catalog/09-tooling/0062-locust/policy.md) | [active](../../../05.operations/catalog/09-tooling/0062-locust/runbook.md) | linked | metadata gate |
| loki | [active](../../../05.operations/catalog/06-observability/0043-loki/guide.md) | [active](../../../05.operations/catalog/06-observability/0043-loki/policy.md) | [active](../../../05.operations/catalog/06-observability/0043-loki/runbook.md) | linked | metadata gate |
| mailpit | [draft](../../../05.operations/catalog/10-communication/0084-mailpit/guide.md) | [draft](../../../05.operations/catalog/10-communication/0084-mailpit/policy.md) | [draft](../../../05.operations/catalog/10-communication/0084-mailpit/runbook.md) | linked | metadata gate |
| meta | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| minio | `GDE-0023` (superseded) | `POL-0023` (superseded) | `RUN-0023` (superseded) | linked | metadata gate |
| minio-create-buckets | `GDE-0023` (superseded) | `POL-0023` (superseded) | `RUN-0023` (superseded) | linked | metadata gate |
| minio1 | `GDE-0023` (superseded) | `POL-0023` (superseded) | `RUN-0023` (superseded) | linked | metadata gate |
| minio2 | `GDE-0023` (superseded) | `POL-0023` (superseded) | `RUN-0023` (superseded) | linked | metadata gate |
| minio3 | `GDE-0023` (superseded) | `POL-0023` (superseded) | `RUN-0023` (superseded) | linked | metadata gate |
| minio4 | `GDE-0023` (superseded) | `POL-0023` (superseded) | `RUN-0023` (superseded) | linked | metadata gate |
| mng-pg | [active](../../../05.operations/catalog/04-data/0028-management-database/guide.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/policy.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/runbook.md) | linked | metadata gate |
| mng-pg-exporter | [active](../../../05.operations/catalog/04-data/0028-management-database/guide.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/policy.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/runbook.md) | linked | metadata gate |
| mng-pg-init | [active](../../../05.operations/catalog/04-data/0028-management-database/guide.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/policy.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/runbook.md) | linked | metadata gate |
| mng-valkey | [active](../../../05.operations/catalog/04-data/0028-management-database/guide.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/policy.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/runbook.md) | linked | metadata gate |
| mng-valkey-exporter | [active](../../../05.operations/catalog/04-data/0028-management-database/guide.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/policy.md) | [active](../../../05.operations/catalog/04-data/0028-management-database/runbook.md) | linked | metadata gate |
| mongo-express | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| mongo-init | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| mongo-key-generator | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| mongodb-arbiter | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| mongodb-exporter | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| mongodb-rep1 | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| mongodb-rep2 | [active](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | [active](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | linked | metadata gate |
| n8n | [active](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | linked | metadata gate |
| n8n-task-runner | [active](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | linked | metadata gate |
| n8n-task-runner-worker | [active](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | linked | metadata gate |
| n8n-valkey | [active](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | linked | metadata gate |
| n8n-valkey-exporter | [active](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | linked | metadata gate |
| n8n-worker | [active](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | [active](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | linked | metadata gate |
| neo4j | [active](../../../05.operations/catalog/04-data/0033-neo4j/guide.md) | [active](../../../05.operations/catalog/04-data/0033-neo4j/policy.md) | [active](../../../05.operations/catalog/04-data/0033-neo4j/runbook.md) | linked | metadata gate |
| nginx | [active](../../../05.operations/catalog/01-gateway/0011-nginx/guide.md) | [active](../../../05.operations/catalog/01-gateway/0011-nginx/policy.md) | [active](../../../05.operations/catalog/01-gateway/0011-nginx/runbook.md) | linked | metadata gate |
| node-exporter | [active](../../../05.operations/catalog/06-observability/0045-prometheus/guide.md) | [active](../../../05.operations/catalog/06-observability/0045-prometheus/policy.md) | [active](../../../05.operations/catalog/06-observability/0045-prometheus/runbook.md) | linked | metadata gate |
| oauth2-proxy | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/guide.md) | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/policy.md) | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/runbook.md) | linked | metadata gate |
| oauth2-proxy-valkey | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/guide.md) | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/policy.md) | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/runbook.md) | linked | metadata gate |
| oauth2-proxy-valkey-exporter | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/guide.md) | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/policy.md) | [active](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/runbook.md) | linked | metadata gate |
| ollama | [active](../../../05.operations/catalog/08-ai/0056-ollama/guide.md) | [active](../../../05.operations/catalog/08-ai/0056-ollama/policy.md) | [active](../../../05.operations/catalog/08-ai/0056-ollama/runbook.md) | linked | metadata gate |
| ollama-exporter | [active](../../../05.operations/catalog/08-ai/0056-ollama/guide.md) | [active](../../../05.operations/catalog/08-ai/0056-ollama/policy.md) | [active](../../../05.operations/catalog/08-ai/0056-ollama/runbook.md) | linked | metadata gate |
| open-webui | [active](../../../05.operations/catalog/08-ai/0057-open-webui/guide.md) | [active](../../../05.operations/catalog/08-ai/0057-open-webui/policy.md) | [active](../../../05.operations/catalog/08-ai/0057-open-webui/runbook.md) | linked | metadata gate |
| open_notebook | [active](../../../05.operations/catalog/11-laboratory/0073-open-notebook/guide.md) | [active](../../../05.operations/catalog/11-laboratory/0073-open-notebook/policy.md) | [active](../../../05.operations/catalog/11-laboratory/0073-open-notebook/runbook.md) | linked | metadata gate |
| openbao | [draft](../../../05.operations/catalog/03-security/0085-openbao/guide.md) | [draft](../../../05.operations/catalog/03-security/0085-openbao/policy.md) | [draft](../../../05.operations/catalog/03-security/0085-openbao/runbook.md) | linked | metadata gate |
| openbao-agent | [draft](../../../05.operations/catalog/03-security/0085-openbao/guide.md) | [draft](../../../05.operations/catalog/03-security/0085-openbao/policy.md) | [draft](../../../05.operations/catalog/03-security/0085-openbao/runbook.md) | linked | metadata gate |
| opensearch | [active](../../../05.operations/catalog/04-data/0019-opensearch/guide.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/policy.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/runbook.md) | linked | metadata gate |
| opensearch-dashboards | [active](../../../05.operations/catalog/04-data/0019-opensearch/guide.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/policy.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/runbook.md) | linked | metadata gate |
| opensearch-node1 | [active](../../../05.operations/catalog/04-data/0019-opensearch/guide.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/policy.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/runbook.md) | linked | metadata gate |
| opensearch-node2 | [active](../../../05.operations/catalog/04-data/0019-opensearch/guide.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/policy.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/runbook.md) | linked | metadata gate |
| opensearch-node3 | [active](../../../05.operations/catalog/04-data/0019-opensearch/guide.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/policy.md) | [active](../../../05.operations/catalog/04-data/0019-opensearch/runbook.md) | linked | metadata gate |
| opentofu | [draft](../../../05.operations/catalog/09-tooling/0082-opentofu/guide.md) | [draft](../../../05.operations/catalog/09-tooling/0082-opentofu/policy.md) | [draft](../../../05.operations/catalog/09-tooling/0082-opentofu/runbook.md) | linked | metadata gate |
| pg-0 | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-0-exporter | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-1 | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-1-exporter | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-2 | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-2-exporter | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-cluster-init | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| pg-router | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | linked | metadata gate |
| prometheus | [active](../../../05.operations/catalog/06-observability/0045-prometheus/guide.md) | [active](../../../05.operations/catalog/06-observability/0045-prometheus/policy.md) | [active](../../../05.operations/catalog/06-observability/0045-prometheus/runbook.md) | linked | metadata gate |
| pushgateway | [active](../../../05.operations/catalog/06-observability/0046-pushgateway/guide.md) | [active](../../../05.operations/catalog/06-observability/0046-pushgateway/policy.md) | [active](../../../05.operations/catalog/06-observability/0046-pushgateway/runbook.md) | linked | metadata gate |
| pyroscope | [active](../../../05.operations/catalog/06-observability/0047-pyroscope/guide.md) | [active](../../../05.operations/catalog/06-observability/0047-pyroscope/policy.md) | [active](../../../05.operations/catalog/06-observability/0047-pyroscope/runbook.md) | linked | metadata gate |
| qdrant | [active](../../../05.operations/catalog/04-data/0034-qdrant/guide.md) | [active](../../../05.operations/catalog/04-data/0034-qdrant/policy.md) | [active](../../../05.operations/catalog/04-data/0034-qdrant/runbook.md) | linked | metadata gate |
| realtime | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| redisinsight | [active](../../../05.operations/catalog/11-laboratory/0076-redisinsight/guide.md) | [active](../../../05.operations/catalog/11-laboratory/0076-redisinsight/policy.md) | [active](../../../05.operations/catalog/11-laboratory/0076-redisinsight/runbook.md) | linked | metadata gate |
| registry | [active](../../../05.operations/catalog/09-tooling/0065-registry/guide.md) | [active](../../../05.operations/catalog/09-tooling/0065-registry/policy.md) | [active](../../../05.operations/catalog/09-tooling/0065-registry/runbook.md) | linked | metadata gate |
| renovate | [draft](../../../05.operations/catalog/09-tooling/0083-renovate/guide.md) | [draft](../../../05.operations/catalog/09-tooling/0083-renovate/policy.md) | [draft](../../../05.operations/catalog/09-tooling/0083-renovate/runbook.md) | linked | metadata gate |
| rest | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| schema-registry | [active](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | [active](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | linked | metadata gate |
| seaweedfs-filer | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/guide.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/policy.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/runbook.md) | linked | metadata gate |
| seaweedfs-master | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/guide.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/policy.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/runbook.md) | linked | metadata gate |
| seaweedfs-mount | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/guide.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/policy.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/runbook.md) | linked | metadata gate |
| seaweedfs-s3 | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/guide.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/policy.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/runbook.md) | linked | metadata gate |
| seaweedfs-volume | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/guide.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/policy.md) | [active](../../../05.operations/catalog/04-data/0024-seaweedfs/runbook.md) | linked | metadata gate |
| sonarqube | [active](../../../05.operations/catalog/09-tooling/0066-sonarqube/guide.md) | [active](../../../05.operations/catalog/09-tooling/0066-sonarqube/policy.md) | [active](../../../05.operations/catalog/09-tooling/0066-sonarqube/runbook.md) | linked | metadata gate |
| stalwart | [active](../../../05.operations/catalog/10-communication/0070-mail/guide.md) | [active](../../../05.operations/catalog/10-communication/0070-mail/policy.md) | [active](../../../05.operations/catalog/10-communication/0070-mail/runbook.md) | linked | metadata gate |
| starrocks-be | `GDE-0020` (superseded) | `POL-0020` (superseded) | `RUN-0020` (superseded) | linked | metadata gate |
| starrocks-fe | `GDE-0020` (superseded) | `POL-0020` (superseded) | `RUN-0020` (superseded) | linked | metadata gate |
| storage | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| studio | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| supavisor | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |
| surrealdb | [draft](../../../05.operations/catalog/11-laboratory/0080-surrealdb/guide.md) | [draft](../../../05.operations/catalog/11-laboratory/0080-surrealdb/policy.md) | [draft](../../../05.operations/catalog/11-laboratory/0080-surrealdb/runbook.md) | linked | metadata gate |
| tempo | [active](../../../05.operations/catalog/06-observability/0049-tempo/guide.md) | [active](../../../05.operations/catalog/06-observability/0049-tempo/policy.md) | [active](../../../05.operations/catalog/06-observability/0049-tempo/runbook.md) | linked | metadata gate |
| terrakube-api | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/guide.md) | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/policy.md) | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/runbook.md) | linked | metadata gate |
| terrakube-executor | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/guide.md) | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/policy.md) | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/runbook.md) | linked | metadata gate |
| terrakube-ui | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/guide.md) | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/policy.md) | [active](../../../05.operations/catalog/09-tooling/0069-terrakube/runbook.md) | linked | metadata gate |
| traefik | [active](../../../05.operations/catalog/01-gateway/0013-traefik/guide.md) | [active](../../../05.operations/catalog/01-gateway/0013-traefik/policy.md) | [active](../../../05.operations/catalog/01-gateway/0013-traefik/runbook.md) | linked | metadata gate |
| valkey-cluster-exporter | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-cluster-init | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-node-0 | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-node-1 | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-node-2 | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-node-3 | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-node-4 | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| valkey-node-5 | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | [active](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | linked | metadata gate |
| vault | `GDE-0016` (superseded) | `POL-0016` (superseded) | `RUN-0016` (superseded) | linked | metadata gate |
| vault-agent | `GDE-0016` (superseded) | `POL-0016` (superseded) | `RUN-0016` (superseded) | linked | metadata gate |
| vector | [active](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | [active](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | linked | metadata gate |

#### G. Environment contract

Root and readiness-example assignments both have 245 unique keys. Added root keys
are `COMFYUI_HOST_PORT`, `COMFYUI_PORT` and `DOZZLE_OIDC_CLIENT_ID`; 98 obsolete
assignments were retired. Active Compose references 243 variables; optional
`COMFYUI_ARGS` and host `HOME` need no assignment. Four assigned indirect inputs
are path derivations and htpasswd usernames. Private values and unknown/retired
local assignments remain preserved; metadata alignment is not exact key deletion.
No private values were displayed. Both private metadata files are ignored and 0600.

#### H. Secret contract

The public registry has 107 unique IDs and 75 paths. New IDs: `AUTO-017`,
`OBS-009`, `PG-020`; no IDs were retired. All 67 root secret declarations have
service grants. Five unused declarations were removed while private files and
registry identities were preserved. Eight mappings are metadata-only. Actual
metadata sync and repeated zero-drift check succeeded without reading secret
value files or displaying private values. Generation prerequisite `htpasswd`
remains unavailable on this host; `--check` therefore remains exit 1.

#### I. Renovate / Dependabot

Renovate owns configured infrastructure managers; Dependabot owns Storybook npm.
Normal Renovate updates use a seven-day release age and Monday-before-06:00
schedule; npm runs Wednesday at 05:00 Asia/Seoul. Patch/minor groups preserve
reviewable component boundaries; majors are separate. Security updates bypass
normal timing and waiting. Infrastructure automerge stays disabled. Existing
floating-image exceptions require owner/risk/review/exit evidence; this change
does not invent image digests or claim mutable tags are immutable.

#### J. External references

The [canonical research member](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md)
contains official framework comparisons, HOME product evidence and supporting
product evidence with concrete local consequences. Source discovery is not a
complete installed-version license or compatibility audit. Rehearsed upgrades,
application acceptance and usable restores remain distinct evidence.

#### K. Change ledger

| Paths | Reason / change | Verification owner |
| --- | --- | --- |
| `infra/**`, root Compose | Concrete configuration drift and retained-service navigation | Compose selections, hardening and focused regression suites |
| Stage 01/02/03 | Actual host requirement, architecture and execution evidence | Metadata, traceability and lifecycle checks |
| Stage 05/99 and infra READMEs | Operations coverage, selector semantics and version authority | Operations catalog, metadata and links |
| `scripts/operations/**`, env/schema examples | Fail-closed source sync and value-preserving metadata sync | Source-sync and metadata-sync regression suites |
| `scripts/lib/document_governance/**`, tests | Runtime literal/source coverage and exact baseline repair | Negative/positive regression suites and registered CI graph |
| Renovate / Dependabot / workflow contract | Unique dependency ownership and accurate existing action pins | Official strict validators and workflow tests |
| Stage 90/98 | Dated primary-source evidence and preserved retired documents | Reference-package and frozen-archive contracts |

#### L. Runtime result and deployment boundary

Only read-only observations were authorized and performed. The source repair for
Pyroscope is not yet installed, so its running container remains unhealthy. AI
and workflow containers were healthy at observation; their persistence, resource
headroom under load, cold start and reboot recovery remain unverified. Mailpit
and Tempo are currently running even though the proposed HOME selection excludes
them; stopping either requires confirming current consumers and explicit approval.

A deployment approval must name its wave and recovery: Pyroscope's healthcheck
replacement can be isolated; ComfyUI and Open WebUI replacement requires queued
work to finish and protected application-data backups; management PostgreSQL
capability/init changes require a verified database backup and an approved outage.
OpenBao initialization/unseal and credential migration require operator-controlled
key custody. Do not start the entire HOME selection or run init jobs implicitly.
No volume deletion, credential rotation, server reboot or data downgrade is
included in repository implementation authorization.

All service definitions are listed below; only 36 were running at observation. Profiles and route/publication
intent come from source; runtime authentication, backup and restored persistence
have not been accepted. Resource values are a single idle observation, not a load
budget or post-deployment measurement.

| Service | Class | Profiles | Observed health | Route/port intent | Persistence | Observed CPU / memory |
| --- | --- | --- | --- | --- | --- | --- |
| pyroscope | OPTIONAL | obs,profiling | unhealthy | all:4040->4040/tcp | declared; restore unverified | 0.21% / 123.9MiB / 512MiB |
| minio | HOME | storage,obs,logs,tracing,nginx | healthy | internal only | declared; restore unverified | 0.00% / 138.7MiB / 512MiB |
| alertmanager | HOME | obs,alerting | healthy | internal only | declared; restore unverified | 0.09% / 15.7MiB / 256MiB |
| tempo | OPTIONAL | obs,tracing | healthy | all:3200->3200/tcp | declared; restore unverified | 0.41% / 51.93MiB / 2GiB |
| loki | HOME | obs,logs | healthy | all:3100->3100/tcp | declared; restore unverified | 0.81% / 83.74MiB / 2GiB |
| pushgateway | OPTIONAL | obs,batch-metrics | healthy | internal only | declared; restore unverified | 0.00% / 6.125MiB / 256MiB |
| traefik | HOME | core,dev,local | healthy | all:80->80/tcp, all:443->443/tcp | declared; restore unverified | 0.00% / 26.29MiB / 512MiB |
| mng-pg-exporter | HOME | mng,dev | healthy | internal only | declared; restore unverified | 0.00% / 8.727MiB / 256MiB |
| grafana | HOME | obs,obs-core,dev,logs,tracing,profiling,alerting,batch-metrics | healthy | internal only | declared; restore unverified | 0.88% / 229.7MiB / 512MiB |
| alloy | HOME | obs,logs,tracing,profiling | healthy | all:4317->4317/tcp, all:4318->4318/tcp | declared; restore unverified | 2.11% / 174.5MiB / 512MiB |
| mng-valkey-exporter | HOME | mng,dev | healthy | internal only | declared; restore unverified | 0.00% / 7.953MiB / 256MiB |
| open-webui | HOME | ai,ai-llm | healthy | internal only | declared; restore unverified | 1.22% / 503.8MiB / 512MiB |
| comfyui | HOME | ai,ai-image | healthy | 127.0.0.1:8188->8188/tcp | declared; restore unverified | 0.05% / 456.6MiB / 512MiB |
| ollama-exporter | HOME | ai,ai-llm,ollama | healthy | internal only | declared; restore unverified | 0.00% / 35.71MiB / 256MiB |
| n8n-task-runner-worker | HOME | workflow,workflow-n8n | healthy | internal only | declared; restore unverified | 0.00% / 4.312MiB / 256MiB |
| flower | HOME | workflow,workflow-airflow | healthy | internal only | declared; restore unverified | 0.02% / 234.9MiB / 256MiB |
| airflow-worker | HOME | workflow,workflow-airflow | healthy | internal only | declared; restore unverified | 100.29% / 775.8MiB / 2GiB |
| prometheus | HOME | obs,obs-core,dev,alerting,batch-metrics | healthy | internal only | declared; restore unverified | 0.48% / 431MiB / 2GiB |
| mng-pg | HOME | mng,core,dev,local | healthy | all:25432->5432/tcp | declared; restore unverified | 3.78% / 73.27MiB / 512MiB |
| cadvisor | HOME | obs,obs-host,dev | healthy | internal only | declared; restore unverified | 130.83% / 986.7MiB / 1GiB |
| keycloak | HOME | core,auth,dev,local | healthy | internal only | declared; restore unverified | 0.19% / 488.2MiB / 2GiB |
| n8n-worker | HOME | workflow,workflow-n8n | healthy | internal only | declared; restore unverified | 0.06% / 176.5MiB / 2GiB |
| n8n-task-runner | HOME | workflow,workflow-n8n | healthy | internal only | declared; restore unverified | 0.00% / 4.363MiB / 256MiB |
| oauth2-proxy | HOME | core,auth,dev,local | healthy | internal only | declared; restore unverified | 0.00% / 5.348MiB / 512MiB |
| airflow-triggerer | HOME | workflow,workflow-airflow | healthy | internal only | declared; restore unverified | 50.29% / 157.6MiB / 256MiB |
| airflow-scheduler | HOME | workflow,workflow-airflow | healthy | internal only | declared; restore unverified | 3.19% / 255MiB / 2GiB |
| airflow-apiserver | HOME | workflow,workflow-airflow | healthy | internal only | declared; restore unverified | 0.12% / 243.4MiB / 2GiB |
| airflow-dag-processor | HOME | workflow,workflow-airflow | healthy | internal only | declared; restore unverified | 102.16% / 405.2MiB / 2GiB |
| airflow-statsd-exporter | HOME | workflow,workflow-airflow | no health status | internal only | declared; restore unverified | 0.27% / 20.59MiB / 256MiB |
| node-exporter | HOME | obs,obs-host,dev | healthy | internal only | declared; restore unverified | 0.00% / 11.8MiB / 256MiB |
| mng-valkey | HOME | mng,core,dev,local | healthy | all:26379->6379/tcp | declared; restore unverified | 0.48% / 5.02MiB / 256MiB |
| qdrant | HOME | ai,ai-llm,qdrant | healthy | internal only | declared; restore unverified | 0.02% / 18.3MiB / 512MiB |
| gatus | HOME | obs,availability,dev | healthy | internal only | declared; restore unverified | 0.01% / 12.46MiB / 256MiB |
| n8n | HOME | workflow,workflow-n8n | healthy | internal only | declared; restore unverified | 0.40% / 237.4MiB / 2GiB |
| mailpit | DEV | dev,local,mail-dev | healthy | all:8025->8025/tcp, all:1025->1025/tcp | declared; restore unverified | 0.00% / 6.57MiB / 512MiB |
| ollama | HOME | ai,ai-llm,ollama | healthy | all:11434->11434/tcp | declared; restore unverified | 0.00% / 188.5MiB / 8GiB |
| airflow-init | HOME | workflow,workflow-airflow | not in running snapshot | internal only | unverified | not sampled |
| airflow-valkey | OPTIONAL | dedicated-valkey | not in running snapshot | internal only | unverified | not sampled |
| airflow-valkey-exporter | OPTIONAL | dedicated-valkey | not in running snapshot | internal only | unverified | not sampled |
| analytics | OPTIONAL | supabase | not in running snapshot | all:4000->4000/tcp | unverified | not sampled |
| auth | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| cassandra-exporter | LAB | cassandra | not in running snapshot | internal only | unverified | not sampled |
| cassandra-node1 | LAB | cassandra | not in running snapshot | internal only | unverified | not sampled |
| couchdb-1 | LAB | couchdb | not in running snapshot | internal only | unverified | not sampled |
| couchdb-2 | LAB | couchdb | not in running snapshot | internal only | unverified | not sampled |
| couchdb-3 | LAB | couchdb | not in running snapshot | internal only | unverified | not sampled |
| couchdb-cluster-init | LAB | couchdb | not in running snapshot | internal only | unverified | not sampled |
| db | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| dozzle | OPTIONAL | admin,admin-logs | not in running snapshot | internal only | unverified | not sampled |
| etcd-1 | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| etcd-2 | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| etcd-3 | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| functions | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| imgproxy | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| influxdb | OPTIONAL | influxdb | not in running snapshot | internal only | unverified | not sampled |
| k6 | DEV | testing | not in running snapshot | internal only | unverified | not sampled |
| kafbat-ui | OPTIONAL | messaging,messaging-admin | not in running snapshot | internal only | unverified | not sampled |
| kafka-1 | LAB | messaging,messaging-broker,messaging-cluster,messaging-schema,messaging-connect,messaging-rest,messaging-admin,ksql | not in running snapshot | all:9092->9092/tcp, all:19101->9101/tcp, all:19404->9404/tcp | unverified | not sampled |
| kafka-2 | LAB | messaging-cluster | not in running snapshot | all:9094->9092/tcp, all:29101->9101/tcp, all:29404->9404/tcp | unverified | not sampled |
| kafka-3 | LAB | messaging-cluster | not in running snapshot | all:9096->9092/tcp, all:39101->9101/tcp, all:39404->9404/tcp | unverified | not sampled |
| kafka-connect | OPTIONAL | messaging,messaging-connect,messaging-admin | not in running snapshot | internal only | unverified | not sampled |
| kafka-exporter | LAB | messaging,messaging-broker,messaging-cluster | not in running snapshot | internal only | unverified | not sampled |
| kafka-init | LAB | messaging,messaging-broker,messaging-cluster | not in running snapshot | internal only | unverified | not sampled |
| kafka-rest-proxy | OPTIONAL | messaging,messaging-rest | not in running snapshot | internal only | unverified | not sampled |
| kong | OPTIONAL | supabase | not in running snapshot | all:8000->8000/tcp, all:8443->8443/tcp | unverified | not sampled |
| ksql-datagen | OPTIONAL | ksql | not in running snapshot | internal only | unverified | not sampled |
| ksqldb-cli | OPTIONAL | ksql | not in running snapshot | internal only | unverified | not sampled |
| ksqldb-server | OPTIONAL | ksql | not in running snapshot | all:8088->8088/tcp | unverified | not sampled |
| locust-master | DEV | tooling,testing | not in running snapshot | all:18089->8089/tcp | unverified | not sampled |
| locust-worker | OPTIONAL | tooling | not in running snapshot | internal only | unverified | not sampled |
| meta | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| minio-create-buckets | HOME | storage,obs,logs,tracing | not in running snapshot | internal only | unverified | not sampled |
| minio1 | LAB | storage-cluster | not in running snapshot | internal only | unverified | not sampled |
| minio2 | LAB | storage-cluster | not in running snapshot | internal only | unverified | not sampled |
| minio3 | LAB | storage-cluster | not in running snapshot | internal only | unverified | not sampled |
| minio4 | LAB | storage-cluster | not in running snapshot | internal only | unverified | not sampled |
| mng-pg-init | HOME | mng,core,dev,local | not in running snapshot | internal only | unverified | not sampled |
| mongo-express | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| mongo-init | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| mongo-key-generator | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| mongodb-arbiter | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| mongodb-exporter | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| mongodb-rep1 | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| mongodb-rep2 | LAB | mongodb | not in running snapshot | internal only | unverified | not sampled |
| n8n-valkey | OPTIONAL | dedicated-valkey | not in running snapshot | internal only | unverified | not sampled |
| n8n-valkey-exporter | OPTIONAL | dedicated-valkey | not in running snapshot | internal only | unverified | not sampled |
| neo4j | OPTIONAL | graph | not in running snapshot | internal only | unverified | not sampled |
| nginx | OPTIONAL | nginx | not in running snapshot | all:80->80/tcp, all:443->443/tcp | unverified | not sampled |
| oauth2-proxy-valkey | OPTIONAL | dedicated-valkey | not in running snapshot | internal only | unverified | not sampled |
| oauth2-proxy-valkey-exporter | OPTIONAL | dedicated-valkey | not in running snapshot | internal only | unverified | not sampled |
| open_notebook | OPTIONAL | admin,notebook | not in running snapshot | all:5055->5055/tcp | unverified | not sampled |
| openbao | HOME | security,secrets,core,local,dev | not in running snapshot | internal only | unverified | not sampled |
| openbao-agent | HOME | security,secrets,core,local,dev | not in running snapshot | internal only | unverified | not sampled |
| opensearch | OPTIONAL | opensearch | not in running snapshot | internal only | unverified | not sampled |
| opensearch-dashboards | LAB | opensearch,opensearch-cluster | not in running snapshot | internal only | unverified | not sampled |
| opensearch-node1 | LAB | opensearch-cluster | not in running snapshot | all:9600->9600/tcp | unverified | not sampled |
| opensearch-node2 | LAB | opensearch-cluster | not in running snapshot | internal only | unverified | not sampled |
| opensearch-node3 | LAB | opensearch-cluster | not in running snapshot | internal only | unverified | not sampled |
| opentofu | DEV | tooling,iac | not in running snapshot | internal only | unverified | not sampled |
| pg-0 | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-0-exporter | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-1 | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-1-exporter | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-2 | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-2-exporter | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-cluster-init | LAB | postgres-ha | not in running snapshot | internal only | unverified | not sampled |
| pg-router | LAB | postgres-ha | not in running snapshot | all:15432->15432/tcp, all:15433->15433/tcp | unverified | not sampled |
| realtime | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| redisinsight | OPTIONAL | admin,admin-data | not in running snapshot | internal only | unverified | not sampled |
| registry | OPTIONAL | tooling,registry | not in running snapshot | all:5000->5000/tcp | unverified | not sampled |
| renovate | DEV | dependency-update | not in running snapshot | internal only | unverified | not sampled |
| rest | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| schema-registry | OPTIONAL | messaging,messaging-schema,messaging-connect,messaging-rest,messaging-admin,ksql | not in running snapshot | internal only | unverified | not sampled |
| seaweedfs-filer | OPTIONAL | seaweedfs-mount,seaweedfs,storage-seaweedfs | not in running snapshot | internal only | unverified | not sampled |
| seaweedfs-master | OPTIONAL | seaweedfs-mount,seaweedfs,storage-seaweedfs | not in running snapshot | internal only | unverified | not sampled |
| seaweedfs-mount | OPTIONAL | seaweedfs-mount | not in running snapshot | internal only | unverified | not sampled |
| seaweedfs-s3 | OPTIONAL | seaweedfs,storage-seaweedfs | not in running snapshot | internal only | unverified | not sampled |
| seaweedfs-volume | OPTIONAL | seaweedfs-mount,seaweedfs,storage-seaweedfs | not in running snapshot | internal only | unverified | not sampled |
| sonarqube | OPTIONAL | tooling,sast | not in running snapshot | internal only | unverified | not sampled |
| stalwart | OPTIONAL | mail-server | not in running snapshot | all:25->25/tcp, all:587->587/tcp, all:465->465/tcp, all:993->993/tcp, all:4190->4190/tcp | unverified | not sampled |
| starrocks-be | OPTIONAL | starrocks | not in running snapshot | all:8040->8040/tcp | unverified | not sampled |
| starrocks-fe | OPTIONAL | starrocks | not in running snapshot | all:9030->9030/tcp, all:8030->8030/tcp | unverified | not sampled |
| storage | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| studio | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |
| supavisor | OPTIONAL | supabase | not in running snapshot | all:5432->5432/tcp, all:6543->6543/tcp | unverified | not sampled |
| surrealdb | OPTIONAL | admin,notebook,surrealdb | not in running snapshot | all:8000->8000/tcp | unverified | not sampled |
| terrakube-api | DEV | tooling,iac | not in running snapshot | internal only | unverified | not sampled |
| terrakube-executor | DEV | tooling,iac | not in running snapshot | internal only | unverified | not sampled |
| terrakube-ui | DEV | tooling,iac | not in running snapshot | internal only | unverified | not sampled |
| valkey-cluster-exporter | LAB | valkey-cluster | not in running snapshot | internal only | unverified | not sampled |
| valkey-cluster-init | LAB | valkey-cluster | not in running snapshot | internal only | unverified | not sampled |
| valkey-node-0 | LAB | valkey-cluster | not in running snapshot | all:6379->6379/tcp | unverified | not sampled |
| valkey-node-1 | LAB | valkey-cluster | not in running snapshot | all:6380->6380/tcp | unverified | not sampled |
| valkey-node-2 | LAB | valkey-cluster | not in running snapshot | all:6381->6381/tcp | unverified | not sampled |
| valkey-node-3 | LAB | valkey-cluster | not in running snapshot | all:6382->6382/tcp | unverified | not sampled |
| valkey-node-4 | LAB | valkey-cluster | not in running snapshot | all:6383->6383/tcp | unverified | not sampled |
| valkey-node-5 | LAB | valkey-cluster | not in running snapshot | all:6384->6384/tcp | unverified | not sampled |
| vault | MIGRATE | legacy-vault | not in running snapshot | internal only | unverified | not sampled |
| vault-agent | MIGRATE | legacy-vault | not in running snapshot | internal only | unverified | not sampled |
| vector | OPTIONAL | supabase | not in running snapshot | internal only | unverified | not sampled |

Entries outside the running snapshot include one-shot jobs and stopped services;
absence does not imply they never ran, their data is empty or deletion is safe.

The first independently deployable wave is deliberately bounded to `pyroscope`:

```bash
docker compose --profile profiling up -d --no-deps --pull never --no-build pyroscope
docker compose --profile profiling exec -T pyroscope /usr/bin/profilecli ready --url=http://127.0.0.1:${PYROSCOPE_PORT:-4040}
```

Approval for this wave would authorize recreation of that service with its already
present pinned image, existing storage and reviewed health/listener settings.
Before executing, compare the selected service, mounted storage and image identity
with the read-only baseline; stop if an image pull or storage change is required.
Observe native readiness and container health repeatedly, then verify the existing
gateway route without exposing response bodies. On failure, restore only the prior
Pyroscope service configuration from the baseline commit in an isolated checkout
and recreate that named service; preserve data and do not downgrade an image.
The previous broken healthcheck is not a successful recovery criterion: native
readiness and serving state must be checked independently.

Subsequent waves require separate concrete backup evidence before authorization:
`comfyui` and `open-webui` (queued work, application database/files and GPU checks),
`mng-pg` / `mng-pg-init` (database restore rehearsal and maintenance window), and
OpenBao (operator-held initialization/unseal material and tested recovery).
Existing Airflow and n8n daemons remain running throughout this proposed first
wave. A complete HOME rollout and host reboot are not part of this narrow request.

#### M. Validation

The command/exit ledger above records actual executions. Additional final results:
Python dependency audit used a complete pinned resolution of 21 packages in an
isolated temporary tool environment and exited 0 with no known vulnerabilities;
npm audit exited 0. Earlier individual pre-commit hook checks exited 0 after
formatter corrections, but are diagnostic evidence, not the governed all-files
wrapper route. Subsequent checks use public profiles and registered tools; the
final staged Gitleaks scan exited 0 with no findings. The first complete registered gate runs reached
453 document-governance tests and failed (full: 6; changed: 5); these are not
reported as PASS. The next full/changed runs passed those tests but stopped at four new Task report
relative links; these links were corrected and the full link check passed. Final
registered results: isolated `--profile changed` exited 0; final serialized
`--profile full` exited 0 with the Ollama source correction included.

### Syncthing retirement receipt

Syncthing has no retained current operational obligation or successor. GDE-0067,
POL-0067 and RUN-0067 transitioned active to retired and moved to the Stage 98
retired operations path. Three Retention Catalog rows bind the preserved files
to baseline `d1e6ded52808b02392c52472d5416518a3b959d6`. Bodies, key order and modes
are preserved; only registered status/updated fields changed. The active tooling
index row was removed. ADR-0024 and AD-0024 consumer cutovers are complete; the
REQ-0010/ADR-0009/AD-0009 cutovers also passed final validation. REQ-0010-FR-0005 was withdrawn without replacement or reuse; current issued
children are 1–4, reserved history is 5, high-water remains 5 and next number 6.
Actual origin/main changed metadata passed with zero violations, and identity/
recovery suites passed 39 tests. Operational subject IDs are not reused. The obsolete optional Syncthing secret validation
path was retired; private files remain untouched.

The exact frozen-body comparison passed for all three files. Corpus lifecycle
exited 0 (zero violations, 212 preserved units, 374 recovery rows), operations
catalog exited 0 and the full link check exited 0 at that revision.

### Host-permission fixture correction

The subsequent registered runs passed document governance and reached 237 rehearsal
contract tests, then failed 29 cases. The host uses umask 0002. Positive test
fixtures inherited group-writable files/intermediate directories, which production
input guards correctly rejected before the intended assertions. The two PostgreSQL
cases reproduced 16 subtest failures independently; setting only their temporary
handoff parent to 0700 produced a 2/2 pass; the complete PostgreSQL module
passed 55 tests. Isolated delivery fixtures passed 55 tests under umask 0002
and a held gate-root descriptor. Supply-chain wrapper fixtures then exposed
three more writable-ancestor failures; explicit private temporary ancestors
resolved them, and all 29 wrapper tests passed, including a new writable-ancestor
rejection. No production permission guard is relaxed and no repository or private
data file is chmodded by these tests. The complete supply-chain/rehearsal
fixture batch passed 239 tests (exit 0). The isolated changed and final serialized full profiles subsequently exited 0.

A separate late integrity run found five failures across 112 tests: two stale
script-manifest contracts and three standalone CLI import failures. The manifest
now registers the allocation-recovery library with its actual registry consumer
and removes the retired Vault-guide invocation; its complete 51-test module passed.
Three registered standalone Python entrypoints now bootstrap canonical imports
from their own file location. Existing CLI tests reproduced the three failures and
passed after correction; the complete 112-test integrity batch then exited 0.
Final changed metadata passed (311 selected, zero violations), and link validation
passed for 916 documents and 7678 links.

### Isolated public verification

Both original-workspace profiles reached all 64 Compose selections, then exited
60 because the PostgreSQL configuration leaf rejects pre-existing ignored
canonical task/output directories with mode 0775. Those paths were not changed.
Toolchain reruns were stopped (exit 143) when this shared local-state limitation
was identified. A detached linked worktree at the pinned baseline received only
the exact public diff, with byte equality verified before execution; no ignored
private config or prior evidence was copied. Its PostgreSQL configuration leaf
passed (exit 0), and full/changed public profiles run with the temporary validation
tools on PATH. The isolated changed profile exited 0. The parallel full run
exited 1 when the other Compose validator cleaned up their shared generated
`.env`; this was execution interference, not a passing result. Final full
verification ran alone after the last bounded Ollama correction and exited 0. No production
guard or canonical evidence contract was weakened.

### Final Ollama boundary correction

The public Compose integration test reproduced wildcard host publication and a
custom-port listener mismatch before correction. Host publication is now loopback;
`OLLAMA_HOST` includes the declared container port. Distinct host/container ports
21434/12434 verify publication, listener, gateway backend and exporter DNS together.
The complete baseline module passed 24 tests and AI hardening exited 0. POL-0056
requires this boundary; its major revision and LAN consumer cutover were reviewed.
The Guide now names the actual `ai`, `ai-llm`, `ollama` selectors. Host commands
use `OLLAMA_HOST_PORT`; internal consumers retain `OLLAMA_PORT`. Independent
specification and quality re-review approved the corrected boundary. The public
resource inventory was rechecked across all 140 services: only Ollama needed a
correction, to its declared 4 CPUs / 8 GiB. The running-state snapshot is unchanged.
Live Ollama recreation requires separate approval and active-client cutover checks.

### Coverage scope and final review

Coverage was measured before the final standalone-import bootstrap correction,
with temporary tooling and without installing host-wide tools.
The focused 162-test run and the 106-test metadata discovery run both exited 0;
the real active-metadata integration command also exited 0. Across four measured
Python validation modules, total statement coverage is 77%; changed executable
lines are 272/294 (92.5%). Scope is `metadata/heading.py`, `operations_catalog.py`,
`requirement_recovery.py` and `github_workflow_contract.py`. These figures are not
whole-repository coverage and do not include inline Python executed by Bash.
Domain-code coverage is N/A under the quality policy's validation/configuration
exception; shell-owned contracts are covered by their negative/positive suites.

Policy review approved the protected quality wording, exact historical recovery,
REQ-0010 withdrawal and all 64 profile rows. Final bounded security review approved
specification compliance and code quality after the Mailpit correction, with no
remaining findings. The three permission-fixture files, three CLI bootstraps and
script manifest also received independent specification and quality approval.
Runtime PostgreSQL startup/init, live resources and restoration
remain explicit forward dependencies of separately approved deployment.

## Review Evidence

Independent policy review found an invalid REQ-0025 synthetic-only parent, stale
profile policy, runtime-version coverage gaps and the corrupt trusted baseline.
REQ-0027 now records the requested actual-host scope as a draft; AD-0031 and
SPEC-0180 parent it. Requirements-to-design approval is not claimed. Template
ownership wording was corrected. Profile and Stage 99 wording re-review passed. Pinned baseline recovery passed
independent review and the actual origin/main changed metadata check (295 selected,
zero violations). Runtime validator boundary fixes and canonical quality policy passed independent review.
Public environment review passed. Security review identified a Mailpit source/gate contract gap: the current image
already supplied native readiness, but Compose and hardening did not preserve it
explicitly. Added native CMD readiness and a strict gate; two tests failed before
the fix and the complete baseline module passed 23 tests afterward. Final
independent review approved the corrected specification and quality with no
remaining findings; two focused tests and the communication gate passed again. The six
initial full-gate document failures were independently diagnosed: three introduced
document shape/index fixtures, two stale baseline inventories and one baseline
timestamp-sensitive test. Corrected focused targets passed 6/6 without weakening
validation assertions; isolated full and changed profiles subsequently exited 0.

## Commit Ledger

The rehearsal fixture repair was committed separately as `52036c3`, after 239
tests and independent specification/quality approval.
The reviewed implementation was committed as one coupled source/document contract
commit; subsequent changes record verification evidence only. The baseline repair,
new Task declarations and registry contracts remain coherent. Git history owns
commit IDs. Broader runtime acceptance remains incomplete.

Draft PR approval source is the owner's mission sequence ending in Pull Request /
Final Report. Target is `buenhyden/hy-home.docker`, branch
`codex/home-dev-convergence` against `main`; authenticated preflight found no
existing PR for this branch. Branch push with upstream succeeded;
[Draft PR #167](https://github.com/buenhyden/hy-home.docker/pull/167) was created
and read back as draft at the committed implementation head. Required hosted
`validation-changed` was in progress; post-commit metadata check passed with
311 selected documents and zero violations. Recovery is a follow-up source commit or closure of the draft;
no force push, merge or protected-branch mutation is authorized. Branch protection
readback requires `validation-changed`, with zero required approving reviews and
no enforced code-owner review; effective branch rulesets returned an empty list.
No remote settings were changed. All touched paths route to @buenhyden.

## Rulings

Tracked implementation and documentation are authorized by the mission. Private
sync is limited to preserving values and aligning metadata without output.
Runtime targets and recovery must be reviewed before deployment approval.

## Deferred Items

Closure (2026-09-24): PR #167 merged on 2026-09-19 with its last hosted `validation-changed` run failing; later main runs pass. So the hosted-CI and draft-PR states above are historical. Broader runtime acceptance from criterion 8 moves to [SPEC-0181](../../0181-home-residual-operations/spec.md).

No scope dropped. Runtime acceptance and required hosted CI remain outstanding.

OpenBao bootstrap, OIDC acceptance and subsequent private-schema reconciliation
continue in [Task 0002](tsk-0002-openbao-access-and-env-convergence.md). The owner
approved the named operations there; broader runtime acceptance remains pending.
