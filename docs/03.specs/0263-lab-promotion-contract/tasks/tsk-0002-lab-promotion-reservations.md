---
title: "LAB Promotion Reservations Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0263-TSK-0002"
parent_ids:
- "SPEC-0263-PLAN-0001"
created: "2026-11-06"
---

# LAB Promotion Reservations Task

## Overview

### Objective

Carry out Plan work unit W7: the resource rule moves from summed limits to
summed reservations plus an external-workload allowance, and the unmeasured
section 5 sub-checks become owner check items.

## Inputs and Authorization

The owner made these decisions on 2026-11-06, after PR #753 merged:

- the resource rule judges declared reservations, not limits;
- the unmeasured section 5 sub-checks become owner check items;
- reservations are declared in the shared resource templates;
- the values are sized from measured usage plus a margin;
- external containers such as k3d count as a fixed allowance in the
  operations policy.

This Task starts, stops and recreates no container. The HOME services pick up
the new reservations only when they are recreated, in an owner window.

## Work Log

### Current contract decision

SPEC-0263 moves to `in-review` for the amendment to version 0.3.0. It returns
to `approved` when the owner approves the amended Spec. The owner approved
version 0.3.0 on 2026-11-06 ("승인").

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0263 | approved | in-review | #current-contract-decision |
| SPEC-0263 | in-review | approved | #current-contract-decision |
| SPEC-0263-TSK-0002 | draft | ready | #review-and-completion |
| SPEC-0263-TSK-0002 | ready | in-progress | #review-and-completion |

### W7 implementation

- **Code and tests** (`f395b0ec4`). `footprint` reads limits from the short
  form or `deploy.resources.limits` and records per-service reservations and
  their replica totals. `running_containers` records the
  `com.docker.compose.service` label. `reservation_sum` sums each running
  container's rendered reservation through its project and service labels;
  a container outside every rendered project counts only through
  `PROMOTION_EXTERNAL_ALLOWANCE` (2.0 CPUs, 6144 MiB), added once. A running
  LAB project without a render, a service missing from its render, or a
  service without limits or reservations is `NOT_RUN`; a reservation above its
  limit is `FAIL`; an over-budget known sum stays `FAIL`. `readiness` and
  `lab.py check` (`budget`) use the same sum; `lab_models` renders only the
  running LAB projects. `manifest_problems` compares each service's
  `reservations` with the render. `function_fit`, `groups_and_file_modes` and
  `profile_and_consumer_clashes` report `OWNER_JUDGMENT`, are listed in
  `owner_checks`, and never block `PASS`.
- **Templates** (`3aa51f512`). Every `x-resource-*` anchor and the two
  templates that set limits inline (`template-stateful-db-med`,
  `template-stateful-db-high`) declare `deploy.resources.reservations` next to
  the short-form limits. The 13 HOME services that set their own limits
  declare their own reservations. `ollama` adds a CPU reservation and keeps its
  authored 4G memory reservation and GPU device. `dcgm-exporter` inherits the
  `x-resource-med` reservation, and Compose merges it with its GPU device.
- **LABs** (`4375fe35e`). No LAB ran during the measurement, so each of the 69
  LAB services reserves its limit (controller ruling, 2026-11-06). Each
  `promotion.yaml` carries the same reservations. The 15 renders are
  unchanged apart from the reservations, and locust keeps `replicas`.
- **Documents.** POL-0107 0.2.0 replaces the unmeasured section 5 text with
  the reservation rule, the external-workload allowance table, the owner check
  items and the current HOME resource state. RUN-0107 0.2.0 adds the report
  values and the owner checklist for a promotion Task. GDE-0008 step 3 and the
  crawl4ai and restic READMEs name the reservations.
- **HOME runtime.** Nothing was started, stopped or recreated. The readiness
  check reads reservations from the render, so they count at once. Docker
  applies the memory reservation to a HOME service only when the owner
  recreates it in an owner window.
- **Follow-up fixes.** `df02fdd97` makes `main` report an `AttributeError`
  from a malformed render (for example a `deploy` string) as invalid input,
  exit 2, for `check` and `readiness`. `33e38860d` re-pins the supply-chain
  ledger's source binding for the 10 changed HOME Compose inputs (42 rows and
  `include_inputs`), following the SPEC-0262 precedent. It also narrows the
  open-webui wiring contract: `deploy` may hold only CPU and memory
  reservations. `ed5ddeccb` names the declared path in each read-only source
  problem of `lab.py check`.
- **TDD.** RED: with only the constant added, `test_lab_controller` ran 98
  tests with 10 failures and 33 errors, all in the new or changed contracts.
  GREEN: `test_lab_controller` and `test_lab_isolation` ran 109 tests OK.
- **Task review fixes.** The independent task review passed spec compliance
  and approved quality with four Minor findings. `budget` now requires
  `known`, so a caller can no longer omit the HOME render and sum only the
  allowance. The footprint tests now assert reservations multiplied by
  replicas and the `deploy.resources.limits` fallback; with the fallback
  removed, the new test fails.
- **Deferred TSK-0001 minor.** `c79e51526` closes the final-review minor
  "alias skip scope in private parse": the metadata sync skips a two-cell row
  only inside the `| Retired ID | Canonical ID |` table. A two-cell row
  anywhere else in either registry is refused (exit 2) instead of silently
  dropping out of the parse. RED with the old parser, GREEN after;
  `test_secret_metadata_sync` passes in the controller venv. Under system
  `python3` it errors because `referencing` (jsonschema) is missing, which
  also explains the 15 local failures seen earlier.

### Measurements

On 2026-11-06, read-only:

- 60 running containers used about 3.18 CPUs and 9358 MiB in total
  (`docker stats --no-stream`).
- The five k3d containers used about 1.0 CPU and 4.1 GiB.
- Of the 97 HOME services in the root render, 97 declare limits and 2
  (`dcgm-exporter`, `ollama`) declare reservations.

#### Reservation samples

Four `docker stats --no-stream` samples of the 60 running containers were
taken at 2026-11-05T15:55:13Z, 15:56:19Z, 15:58:06Z and 16:01:02Z (2026-11-06
local time). Each call takes about 30 to 60 s, so the samples are 66 to 176 s
apart. A container's value is its peak over the samples, and a template's peak
is its highest member. Each running container was mapped to its template
through its service's `extends` in the root include files, and its own
`cpus` or `mem_limit` decided whether it is a template member or its own
group. A reservation is the peak times 1.5, rounded up to 0.05 CPU and 32 MiB,
at least 0.05 CPU and 32 MiB, and at most the limit. An unmeasured reservation
equals the limit. `gatus` and `pyroscope` appeared in one sample only. No LAB
project was running.

| Template | Limit | Running members | Peak CPU | Peak MiB | Peak x 1.5, rounded | Reservation | Basis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `x-resource-dev-tiny` | 0.10 / 64M | 0 | - | - | - | 0.10 / 64M | unmeasured: reservation = limit |
| `x-resource-dev-small` | 0.20 / 128M | 0 | - | - | - | 0.20 / 128M | unmeasured: reservation = limit |
| `x-resource-low` | 0.50 / 256M | 17 | 0.045 | 72.8 | 0.10 / 128M | 0.10 / 128M | measured |
| `x-resource-med` | 1.00 / 512M | 16 | 0.185 | 217.4 | 0.30 / 352M | 0.30 / 352M | measured |
| `x-resource-obs-high` | 1.50 / 1024M | 0 | - | - | - | 1.50 / 1024M | unmeasured: reservation = limit |
| `x-resource-high` | 2.00 / 2048M | 1 | 0.045 | 571.4 | 0.10 / 864M | 0.10 / 864M | measured |
| `x-resource-db` | 2.00 / 2048M | 10 | 1.654 | 462.4 | 2.50 / 704M | 2.00 / 704M | measured; capped at the limit |
| `template-stateful-db-med` | 1.00 / 512M | 1 | 0.098 | 71.2 | 0.15 / 128M | 0.15 / 128M | measured |
| `template-stateful-db-high` | 2.00 / 2048M | 0 | - | - | - | 2.00 / 2048M | unmeasured: reservation = limit |

| Service | Limit | Peak CPU | Peak MiB | Reservation | Basis |
| --- | --- | --- | --- | --- | --- |
| `dev-pg` | 2.00 / 2048M | 0.008 | 48.5 | 0.05 / 96M | measured |
| `grafana` | 1.00 / 1024M | 0.011 | 299.9 | 0.05 / 480M | measured |
| `cadvisor` | 1.50 / 1024M | 0.000 | 29.7 | 0.05 / 64M | measured |
| `airflow-triggerer` | 0.50 / 384M | 0.520 | 279.7 | 0.50 / 384M | measured; capped at the limit |
| `flower` | 0.50 / 384M | 0.003 | 25.5 | 0.05 / 64M | measured |
| `comfyui` | 2.00 / 4096M | 0.001 | 38.0 | 0.05 / 64M | measured |
| `crawl4ai` | 2.00 / 4096M | 0.065 | 64.7 | 0.10 / 128M | measured |
| `mlflow` | 1.00 / 1024M | 0.005 | 27.1 | 0.05 / 64M | measured |
| `ollama` | 4.00 / 8192M | 0.000 | 46.9 | 0.05 / 4096M | CPU measured; the authored 4G memory reservation is kept |
| `open-webui` | 2.00 / 2048M | 0.005 | 525.6 | 0.05 / 800M | measured |
| `renovate` | 1.00 / 1024M | - | - | 1.00 / 1024M | not running; unmeasured: reservation = limit |
| `restic` | 0.50 / 1024M | - | - | 0.50 / 1024M | not running; unmeasured: reservation = limit |
| `restic-offsite` | 0.50 / 1024M | - | - | 0.50 / 1024M | not running; unmeasured: reservation = limit |

| Template | Container peaks (CPU cores / MiB) |
| --- | --- |
| `x-resource-low` | dev-valkey 0.045 / 3, mng-valkey 0.042 / 7, alertmanager 0.018 / 30, airflow-statsd-exporter 0.008 / 23, n8n-task-runner 0.002 / 4, n8n-task-runner-worker 0.001 / 73, ollama-exporter 0.001 / 39, mng-pg-exporter 0.000 / 10, mng-valkey-exporter 0.000 / 8, dev-valkey-exporter 0.000 / 14, pushgateway 0.000 / 8, dev-pg-exporter 0.000 / 15, node-exporter 0.000 / 46, storybook 0.000 / 4, storybook-mcp 0.000 / 38, crawl4ai-egress 0.000 / 71, gatus 0.000 / 0 (1 sample) |
| `x-resource-med` | openbao 0.185 / 21, blog-ingestion 0.117 / 66, dozzle 0.066 / 25, alloy 0.023 / 217, traefik 0.013 / 51, seaweedfs-s3 0.011 / 81, seaweedfs-filer 0.011 / 194, dcgm-exporter 0.010 / 39, seaweedfs-master 0.005 / 38, qdrant 0.005 / 9, openbao-agent 0.002 / 14, registry 0.001 / 25, redisinsight 0.000 / 116, oauth2-proxy 0.000 / 9, mailpit 0.000 / 11, pyroscope 0.000 / 0 (1 sample) |
| `x-resource-high` | keycloak 0.045 / 571 |
| `x-resource-db` | airflow-dag-processor 1.654 / 329, airflow-scheduler 0.077 / 160, tempo 0.074 / 386, loki 0.056 / 285, airflow-apiserver 0.050 / 27, n8n 0.007 / 257, seaweedfs-volume 0.007 / 98, prometheus 0.007 / 462, airflow-worker 0.004 / 61, n8n-worker 0.002 / 210 |
| `template-stateful-db-med` | mng-pg 0.098 / 71 |

LAB services (69 in 15 LABs) were not running. Each is "unmeasured:
reservation = limit until measured in an approved LAB lease run
(`lab.py run`)".

| LAB | Services | Reserved CPUs | Reserved MiB |
| --- | --- | --- | --- |
| cassandra | 1 | 2 | 2048 |
| couchdb | 4 | 3.5 | 1792 |
| dbt | 2 | 1.5 | 768 |
| jupyterlab | 1 | 2 | 2048 |
| kafka-cluster | 5 | 3.25 | 5120 |
| lakehouse | 6 | 8.5 | 8192 |
| locust | 2 | 3 | 1536 |
| mongodb | 6 | 6.5 | 5376 |
| opensearch-cluster | 4 | 7 | 6656 |
| postgresql-ha | 11 | 10.5 | 8448 |
| sonarqube | 1 | 2 | 2048 |
| stalwart | 2 | 1.5 | 768 |
| supabase | 13 | 14.5 | 10496 |
| superset | 3 | 2.5 | 1792 |
| valkey-cluster | 8 | 7 | 3584 |

#### HOME reservation sum

With the new values, the 55 running HOME containers reserve 27.75 CPUs and
22080 MiB. `x-resource-db` gives 20.00 CPUs of that (10 members at 2.00),
`x-resource-med` 4.80 and `x-resource-low` 1.70. The `x-resource-db` value
comes from `airflow-dag-processor`, which peaked at 1.654 CPU while parsing
DAGs; the next member peak is 0.077 CPU.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 8 | W7 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` on the amendment working tree over `5989bf1c9` | PASS | selected=4 violations=0 | required | - |
| E2 | 8 | W7 | RED | `test_lab_controller` with only `PROMOTION_EXTERNAL_ALLOWANCE` added, over `5e270cf08` | FAIL | 98 tests, failures=10, errors=33, all in the new or changed contracts; expected RED | required | - |
| E3 | 8 | W7 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` at `ed5ddeccb` | PASS | 116 tests OK | required | - |
| E4 | 8 | W7 | Compose acceptance | `docker compose --env-file .env.example --profile '*' config -q` and the JSON render at `493efe01c` | PASS | exit 0; 97 of 97 services declare limits and reservations, each reservation at most its limit; `dcgm-exporter` and `ollama` keep their GPU devices; no container started | required | - |
| E5 | 8 | W7 | LAB renders, synthetic inputs | the E40 method: `labs/.env.example` plus 13 synthetic `LAB_*` inputs, `config --format json` for the 15 LABs at `493efe01c` | PASS | 15 of 15 exit 0; 69 services reserve their limits; otherwise identical to the pre-change renders; locust keeps `replicas` | required | - |
| E6 | 8 | W7 | hardening | `bash scripts/hardening/check-all-hardening.sh` over the template and service changes | PASS | "ALL checks passed successfully" | required | - |
| E7 | 8 | W7 | common-optimizations controls | `bash scripts/validation/check-template-security-baseline.sh` | PASS | scopes=24 services=942 findings=0 | required | - |
| E8 | 8 | W7 | HOME readiness | `lab.py --env-file labs/.env readiness valkey-cluster`, read-only, at `493efe01c` | FAIL | exit 3; tier, composition, linux and docker PASS; resources FAIL: reserved CPUs 36.55 exceed budget 10, reserved memory 31552 MiB exceeds budget 27924 MiB; owner_checks lists the three `OWNER_JUDGMENT` items; 5 k3d containers count through the allowance | required | - |
| E9 | 8 | W7 | HOME readiness | `lab.py --env-file labs/.env readiness postgresql-ha`, read-only, at `493efe01c` | FAIL | exit 3; tier, composition, linux and docker PASS; resources FAIL: 40.1 CPUs and 36448 MiB against 10 and 27924 | required | - |
| E10 | 8 | W7 | LAB check | `lab.py --env-file labs/.env check valkey-cluster`, read-only, at `ed5ddeccb` | FAIL | exit 3; only problems: reserved CPUs 36.75 exceed the LAB budget 4, reserved memory 31808 MiB exceeds 8192 MiB | required | - |
| E11 | 8 | W7 | metadata | `check-document-metadata.py --mode check-active` | PASS | selected=543 violations=0 | required | - |
| E12 | 8 | W7 | links | `check-document-links.py --mode all` | PASS | documents=893 links=8156 failures=0 | required | - |
| E13 | 8 | W7 | operations catalog | `check-operations-catalog.py` after `3aa51f512` | FAIL | 96 `service-inventory-drift` findings: stale Resources in the m0021 service inventory | required | - |
| E14 | 8 | W7 | operations catalog | `check-operations-catalog.py` after the inventory re-projection in `493efe01c` (`render_service_inventory`; only the Resources column changed, in 96 rows) | PASS | operations-catalog: PASS | required | E13 |
| E15 | 8 | W7 | full unit suite | `env -u LAB_DATA_DIR PATH=~/.local/share/hy-home/controller-venv-py312/bin:$PATH python -m unittest discover -s tests -t .` at `493efe01c` | FAIL | 3344 tests, failures=44, skipped=108: 43 in `test_update_gates` (stale Compose source SHAs) and 1 in `test_service_wiring_contracts` (open-webui `deploy`) | required | - |
| E16 | 8 | W7 | full unit suite | the E15 command at `ed5ddeccb` (with this Task edit in the working tree) | PASS | 3344 tests OK, skipped=108 | required | E15 |
| E17 | 8 | W7 | task review | independent review of `5e270cf08..3cf6dde9e` | PASS | spec compliance PASS, quality APPROVED; 4 Minor findings: 2 fixed (E18), 2 recorded under Review and Completion | required | - |
| E18 | 8 | W7 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` after the review fixes | PASS | 117 tests OK; the new limits-fallback test fails with the fallback removed | required | - |
| E19 | 8 | W7 | full unit suite | the E15 command at `c79e51526` (code identical at `b2c1d3658`) | PASS | 3346 tests OK, skipped=108 | required | - |
| E20 | 8 | W7 | HOME readiness | `lab.py --env-file labs/.env readiness valkey-cluster`, read-only, after the dag-processor reservation | FAIL | resources FAIL: running 11.1 CPUs / 21888 MiB, needed 19.9 CPUs / 31360 MiB against 10 / 27924; no unrendered project | required | - |
| E21 | 8 | W7 | HOME readiness | the E20 command for `postgresql-ha` | FAIL | resources FAIL: needed 23.45 CPUs / 36256 MiB against 10 / 27924 | required | - |
| E22 | 8 | W7 | HOME readiness | the E20 command after the valkey-cluster lease-run reservations | FAIL | tier, composition, linux, docker PASS; resources FAIL: candidate 1.15 CPUs / 480 MiB, needed 14.05 CPUs / 28256 MiB against 10 / 27924 | required | - |
| E23 | 8 | W7 | HOME readiness | `lab.py --env-file labs/.env readiness valkey-cluster`, read-only, after the HOME outlier reservations | PASS | all five criteria PASS; needed 9.8 CPUs / 25536 MiB against 10 / 27924 | required | E22 |
| E24 | 8 | W7 | HOME readiness | the E23 command for `postgresql-ha` | FAIL | resources FAIL: candidate unmeasured at its limit, needed 19.2 CPUs / 33440 MiB | required | - |
| E25 | 8 | W7 | full unit suite | the E15 command at `19d6040b2` | FAIL | 3346 tests, failures=2: `test_workflow_version_bundle` (stale n8n source binding) and `test_sec01_ci_routing`, which runs it | required | - |
| E26 | 8 | W7 | full unit suite | the E15 command at `63d5b78a0`, after re-pinning the current n8n source binding in the update ledger and build inputs | PASS | 3346 tests OK, skipped=108 | required | E25 |
| E27 | 8 | W7 | HOME readiness | `lab.py --env-file labs/.env readiness` for the six measured LABs, read-only, at `ea012d83b` | FAIL | postgresql-ha resources FAIL (10.45 CPUs / 10); opensearch-cluster resources FAIL (31808 / 27924 MiB); cassandra, couchdb, jupyterlab, mongodb resources PASS, tier and composition FAIL (destination undecided); valkey-cluster PASS | required | - |
| E28 | 8 | W7 | RED | `test_lab_controller` at `961b5d475` | PASS | 100 tests OK | required | E2 |
| E29 | 8 | W7 | HOME readiness | `lab.py --env-file labs/.env readiness valkey-cluster`, read-only, at `961b5d475` | PASS | all five criteria PASS; needed 9.8 CPUs / 25536 MiB against 10 / 27924 | required | E8, E20 |
| E30 | 8 | W7 | LAB check | `lab.py --env-file labs/.env check valkey-cluster`, read-only, at `961b5d475` | FAIL | exit 3; only the LAB budget: 9.95 CPUs / 25696 MiB against `LAB_HOST_BUDGET_*` 4 / 8192 | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 8 | pending | E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E14, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, E28, E29, E30 | - | @buenhyden |

## Review and Completion

The owner approved Spec 0.3.0. W7 is implemented. Criterion 8 waits for owner
acceptance.

The HOME readiness resource `FAIL` (E8, E9) is a real result, not a defect of
the check. Reservations come from the render, so they count before any
recreation. The owner decides the next step:

- `x-resource-db` carries the peak of `airflow-dag-processor` for all ten
  running members. Giving that service its own reservation would lower the
  running sum to about 9.25 CPUs.
- The LAB candidates reserve their limits until a LAB lease run measures them:
  7.0 CPUs for valkey-cluster and 10.5 for postgresql-ha.
- The host budget is 10 CPUs.

The memory reservations take effect in Docker only when the owner recreates
the HOME services in an owner window.

Status (2026-11-06): the owner asked to move this Task forward, so it is
`in-progress`. Criterion 8 stays pending on real results: postgresql-ha
readiness refuses on resources (E9, E21, E24, E27), and `lab.py check`
(E10, E30) sums HOME reservations against the LAB budget of 4 CPUs / 8192
MiB, which no LAB can meet now; 10 / 27924 would pass valkey-cluster.

Owner decisions on the review findings and the resource `FAIL` (2026-11-06):

- `ollama` keeps its authored 4G memory reservation for model loading, as an
  approved exception to the sizing rule (measured peak 47 MiB). POL-0107 0.2.1
  records it.
- A running container of a Compose project without a render is `NOT_RUN`.
  Only a container without Compose labels (k3d and similar) counts through the
  allowance (`6b8f29334`).
- `airflow-dag-processor` gets its own reservation, 2.00 CPUs (its 2.48 peak
  margin capped at the limit) and 512M (329 MiB x 1.5). The `x-resource-db`
  anchor drops to 0.15 CPUs (the next member peak, 0.077 x 1.5) and keeps
  704M. The running sum falls from 27.75 to 11.1 CPUs (E20, E21). The update
  ledger re-pins the airflow Compose source binding (10 rows and
  `include_inputs`), and the m0021 inventory is re-projected (12 rows).
- The candidates still fail, so the next step is a LAB lease measurement in
  an owner window; until then each candidate reserves its limit.
- **valkey-cluster lease run (2026-11-06).** The owner ran the LAB under a
  30-minute lease with a temporarily raised LAB budget and took five
  `docker stats` samples, all idle (no synthetic load). Node peak 0.044 CPU
  and 7.7 MiB, applied to all six symmetric nodes, so each reserves 0.10 CPU
  and 32M; the exporter peaked at 0.00 CPU and 17.3 MiB and reserves 0.05 CPU
  and 32M. `valkey-cluster-init` is a one-shot job that did not run in the
  samples, so it keeps its limit. The candidate reservation falls from 7.0
  CPUs / 3584 MiB to 1.15 CPUs / 480 MiB (E22). Readiness still fails: the
  running HOME sum (11.1 CPUs) alone exceeds the 10-CPU budget. Idle samples
  understate a loaded cluster; a load run should re-measure before promotion.
- **HOME outlier reservations (owner request, 2026-11-06).** One anchor
  reservation carried its highest member's peak to every member, so seven
  outliers from the W7 samples reserve their own peak x 1.5: `openbao` 0.30
  CPU / 32M, `blog-ingestion` 0.20 / 128M, `dozzle` 0.10 / 64M, `alloy` 0.05
  / 352M, `seaweedfs-filer` 0.05 / 320M, `dev-valkey` and `mng-valkey` 0.10 /
  32M. `x-resource-med` drops to 0.05 CPU / 192M (next peaks: alloy 0.023 CPU
  excluded, redisinsight 116 MiB) and `x-resource-low` to 0.05 CPU (next
  peak: alertmanager 0.018). The running HOME sum falls to 6.8 CPUs / 19072
  MiB. The update ledger re-pins only `entries[*].source_input_sha256` (41)
  and `include_inputs` (7); a first blanket replacement that also touched
  historical bindings was discarded before commit. valkey-cluster now passes
  resources with 0.2 CPU of headroom (E23); postgresql-ha still fails (E24).
- **Six more LAB lease runs (2026-11-06, `ea012d83b`).** The owner measured
  cassandra, couchdb, jupyterlab, mongodb, opensearch-cluster and
  postgresql-ha with five idle `docker stats` samples each. Symmetric replicas
  share their group peak; one-shot init jobs that did not run keep their
  limit. The first postgresql-ha run failed because the pg data directories
  were `1000:1000 770` and Spilo runs as `101:103` (`initdb: Permission
  denied`), an instance of the `groups_and_file_modes` owner check; the owner
  changed their ownership and re-ran. Readiness (E27):
  - postgresql-ha: candidate 1.75 CPUs / 1664 MiB; resources `FAIL`, 10.45
    CPUs against 10. `pg-cluster-init` is unmeasured and reserves 0.50 CPU.
  - opensearch-cluster: candidate 0.65 CPUs / 6592 MiB; resources `FAIL` on
    memory (31808 against 27924 MiB); each node's JVM peak (1630 MiB x 1.5)
    is capped at its 2048M limit.
  - cassandra, couchdb, jupyterlab and mongodb: resources `PASS`; tier and
    composition `FAIL` because their destination `kind` is `undecided`.
- **Owner decision (2026-11-06): no LAB is promoted.** The owner decides
  every promotion, and nothing in `labs/` is to be promoted now. The readiness
  results above are measurements, not promotion requests. The open questions
  they raised (`pg-cluster-init` measurement, opensearch heap, destinations for
  the `undecided` LABs) are closed without action, and the manifests stay
  as they are.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Task 0001](tsk-0001-lab-promotion-contract.md)
